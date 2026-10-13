package com.fpe.entity;

import java.util.ArrayList;
import java.util.EnumSet;
import java.util.List;

import javax.annotation.Nullable;

import net.minecraft.nbt.CompoundTag;
import net.minecraft.network.chat.Component;
import net.minecraft.network.syncher.EntityDataAccessor;
import net.minecraft.network.syncher.EntityDataSerializers;
import net.minecraft.network.syncher.SynchedEntityData;
import net.minecraft.server.level.ServerBossEvent;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.world.BossEvent;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.ai.goal.FloatGoal;
import net.minecraft.world.entity.ai.goal.Goal;
import net.minecraft.world.entity.ai.goal.RandomLookAroundGoal;
import net.minecraft.world.entity.ai.goal.target.HurtByTargetGoal;
import net.minecraft.world.entity.ai.goal.target.NearestAttackableTargetGoal;
import net.minecraft.world.entity.monster.Monster;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.Vec3;

/**
 * Base of every FPE character. Subclasses only declare attributes + abilities
 * (override {@link #registerAbilities}); AI, target selection, ability scheduling and animation
 * syncing are handled here.
 */
public abstract class FpeEntity extends Monster {
    public static final int DEATH_TICKS = 40;
    protected static final EntityDataAccessor<Integer> ANIM = SynchedEntityData.defineId(FpeEntity.class, EntityDataSerializers.INT);
    protected static final EntityDataAccessor<Integer> VARIANT = SynchedEntityData.defineId(FpeEntity.class, EntityDataSerializers.INT);

    /** ticks since current ability started (client counts locally, server authoritative) */
    public int animTime;
    private List<Ability> abilities;
    private int[] cooldowns;
    @Nullable private Ability current;
    private int rest = 30;
    @Nullable private ServerBossEvent bossEvent;

    protected FpeEntity(EntityType<? extends FpeEntity> type, Level level) {
        super(type, level);
        this.xpReward = 30;
    }

    // ------------------------------------------------------------------ attributes helper
    public static AttributeSupplier.Builder baseAttributes(double health, double damage, double speed, double armor, double kbResist) {
        return Monster.createMonsterAttributes()
                .add(Attributes.MAX_HEALTH, health)
                .add(Attributes.ATTACK_DAMAGE, damage)
                .add(Attributes.MOVEMENT_SPEED, speed)
                .add(Attributes.ARMOR, armor)
                .add(Attributes.KNOCKBACK_RESISTANCE, kbResist)
                .add(Attributes.FOLLOW_RANGE, 40.0)
                .add(Attributes.ATTACK_KNOCKBACK, 0.5);
    }

    // ------------------------------------------------------------------ abilities
    /** Declare all abilities (both phases for multi-phase mobs; use Ability.when for gating). Index+1 is the synced anim id. */
    protected abstract void registerAbilities(List<Ability> out);

    public final List<Ability> abilities() {
        if (abilities == null) { abilities = new ArrayList<>(); registerAbilities(abilities); cooldowns = new int[abilities.size()]; }
        return abilities;
    }

    /** damage helper: attack-damage attribute * multiplier */
    public float dmg(float mult) { return (float) getAttributeValue(Attributes.ATTACK_DAMAGE) * mult; }

    public boolean isEnraged() { return getHealth() < getMaxHealth() * 0.5f; }

    /** ticks of idle between two abilities */
    protected int restTicks() { return isEnraged() ? 8 : 18; }

    /** preferred standoff distance while approaching (0 = melee range) */
    public double preferredDistance() { return 2.0; }

    public int getVariant() { return entityData.get(VARIANT); }
    public void setVariant(int v) { entityData.set(VARIANT, v); }

    public String currentAbilityId() {
        int id = entityData.get(ANIM);
        List<Ability> a = abilities();
        return id > 0 && id <= a.size() ? a.get(id - 1).id : "";
    }

    public int currentAbilityDuration() {
        int id = entityData.get(ANIM);
        List<Ability> a = abilities();
        return id > 0 && id <= a.size() ? a.get(id - 1).duration : 1;
    }

    public boolean isRooted() { return current != null && current.rooted; }
    public boolean isBusy() { return current != null; }

    /** force-start an ability by id (server) e.g. for phase transitions. Ignores range/cooldown. */
    public boolean forceAbility(String id) {
        if (level().isClientSide) return false;
        List<Ability> a = abilities();
        for (int i = 0; i < a.size(); i++) if (a.get(i).id.equals(id)) { beginAbility(i, getTarget()); return true; }
        return false;
    }

    public void cancelAbility() {
        if (current != null) { current = null; animTime = 0; entityData.set(ANIM, 0); }
    }

    private void beginAbility(int idx, @Nullable LivingEntity target) {
        current = abilities().get(idx);
        animTime = 0;
        cooldowns[idx] = current.cooldown;
        entityData.set(ANIM, idx + 1);
        if (current.onStart != null && target != null) current.onStart.run(this, target, 0);
    }

    private void endAbility(@Nullable LivingEntity target) {
        Ability a = current;
        current = null; animTime = 0; rest = restTicks();
        entityData.set(ANIM, 0);
        if (a != null && a.onEnd != null && target != null) a.onEnd.run(this, target, a.duration);
    }

    private void serverAbilityTick() {
        List<Ability> list = abilities();
        for (int i = 0; i < cooldowns.length; i++) if (cooldowns[i] > 0) cooldowns[i]--;
        LivingEntity target = getTarget();
        boolean valid = target != null && target.isAlive();
        if (current != null) {
            if (!valid) { endAbility(null); return; }
            Ability a = current;
            if (animTime < a.faceUntil) snapFace(target);
            if (a.onTick != null) a.onTick.run(this, target, animTime);
            if (a.rooted) getNavigation().stop();
            animTime++;
            if (animTime >= a.duration) endAbility(target);
            return;
        }
        if (rest > 0) { rest--; return; }
        if (!valid) return;
        double dist = distanceTo(target);
        boolean sight = hasLineOfSight(target);
        int total = 0;
        int[] w = new int[list.size()];
        for (int i = 0; i < list.size(); i++) {
            Ability a = list.get(i);
            if (cooldowns[i] > 0 || dist < a.min || dist > a.max || (a.needsSight && !sight) || !a.cond.test(this)) continue;
            w[i] = a.weight; total += a.weight;
        }
        if (total <= 0) return;
        int r = random.nextInt(total);
        for (int i = 0; i < w.length; i++) {
            if (w[i] == 0) continue;
            if (r < w[i]) { beginAbility(i, target); return; }
            r -= w[i];
        }
    }

    // ------------------------------------------------------------------ movement helpers for abilities
    /** instantly face the target (yaw + head) */
    public void snapFace(LivingEntity t) {
        double dx = t.getX() - getX(), dz = t.getZ() - getZ();
        float yaw = (float) (Math.toDegrees(Math.atan2(dz, dx)) - 90.0);
        setYRot(yaw); yBodyRot = yaw; yHeadRot = yaw;
        double dy = t.getEyeY() - getEyeY();
        setXRot((float) -Math.toDegrees(Math.atan2(dy, Math.sqrt(dx * dx + dz * dz))));
    }

    /** horizontal impulse toward a point (lunges, leaps). vy>0 adds a jump. */
    public void dashToward(Vec3 to, double speed, double vy) {
        Vec3 d = new Vec3(to.x - getX(), 0, to.z - getZ());
        if (d.lengthSqr() < 1.0E-4) d = calculateViewVector(0, getYRot());
        d = d.normalize().scale(speed);
        setDeltaMovement(d.x, vy, d.z);
        hasImpulse = true;
    }

    /** impulse along facing direction */
    public void dashForward(double speed, double vy) {
        Vec3 d = calculateViewVector(0, getYRot()).scale(speed);
        setDeltaMovement(d.x, vy, d.z);
        hasImpulse = true;
    }

    // ------------------------------------------------------------------ AI
    @Override
    protected void registerGoals() {
        goalSelector.addGoal(0, new FloatGoal(this));
        goalSelector.addGoal(2, new ApproachGoal(this));
        goalSelector.addGoal(8, new RandomLookAroundGoal(this));
        targetSelector.addGoal(1, new HurtByTargetGoal(this, FpeEntity.class).setAlertOthers());
        targetSelector.addGoal(2, new NearestAttackableTargetGoal<>(this, Player.class, true));
        targetSelector.addGoal(3, new NearestAttackableTargetGoal<>(this, Mob.class, 10, true, false, t -> !(t instanceof FpeEntity)));
    }

    /** chases the target until preferredDistance(), never attacks itself (abilities do) */
    static final class ApproachGoal extends Goal {
        private final FpeEntity e;
        private int repath;
        ApproachGoal(FpeEntity e) { this.e = e; setFlags(EnumSet.of(Flag.MOVE, Flag.LOOK)); }
        @Override public boolean canUse() { LivingEntity t = e.getTarget(); return t != null && t.isAlive() && !e.isRooted(); }
        @Override public boolean canContinueToUse() { return canUse(); }
        @Override public void tick() {
            LivingEntity t = e.getTarget();
            if (t == null) return;
            e.getLookControl().setLookAt(t, 30f, 30f);
            if (--repath <= 0) {
                repath = 4 + e.random.nextInt(4);
                if (e.distanceTo(t) > e.preferredDistance()) e.getNavigation().moveTo(t, 1.0);
                else e.getNavigation().stop();
            }
        }
    }

    // ------------------------------------------------------------------ boss bar
    protected boolean hasBossBar() { return false; }
    protected BossEvent.BossBarColor bossColor() { return BossEvent.BossBarColor.PURPLE; }

    @Override public void startSeenByPlayer(ServerPlayer p) { super.startSeenByPlayer(p); if (hasBossBar()) bossBar().addPlayer(p); }
    @Override public void stopSeenByPlayer(ServerPlayer p) { super.stopSeenByPlayer(p); if (bossEvent != null) bossEvent.removePlayer(p); }

    private ServerBossEvent bossBar() {
        if (bossEvent == null) bossEvent = new ServerBossEvent(getDisplayName(), bossColor(), BossEvent.BossBarOverlay.PROGRESS);
        return bossEvent;
    }

    @Override public void setCustomName(@Nullable Component n) { super.setCustomName(n); if (bossEvent != null) bossEvent.setName(getDisplayName()); }

    // ------------------------------------------------------------------ lifecycle
    @Override
    protected void defineSynchedData() {
        super.defineSynchedData();
        entityData.define(ANIM, 0);
        entityData.define(VARIANT, 0);
    }

    @Override
    public void onSyncedDataUpdated(EntityDataAccessor<?> key) {
        super.onSyncedDataUpdated(key);
        if (ANIM.equals(key)) animTime = 0;
        if (VARIANT.equals(key)) refreshDimensions();
    }

    @Override
    public void tick() {
        super.tick();
        if (level().isClientSide) {
            if (entityData.get(ANIM) != 0) animTime++; else animTime = 0;
        } else {
            if (isAlive()) serverAbilityTick();
            if (bossEvent != null) bossEvent.setProgress(getHealth() / getMaxHealth());
        }
    }

    @Override
    protected void tickDeath() {
        ++deathTime;
        if (deathTime >= DEATH_TICKS && !level().isClientSide() && !isRemoved()) {
            level().broadcastEntityEvent(this, (byte) 60);
            remove(RemovalReason.KILLED);
        }
    }

    @Override public boolean removeWhenFarAway(double d) { return false; }

    @Override
    public boolean hurt(DamageSource s, float amount) {
        if (s.getEntity() instanceof FpeEntity) return false;
        return super.hurt(s, amount);
    }

    @Override public boolean canAttack(LivingEntity t) { return !(t instanceof FpeEntity) && super.canAttack(t); }

    @Override
    public void addAdditionalSaveData(CompoundTag t) { super.addAdditionalSaveData(t); t.putInt("FpeVariant", getVariant()); }

    @Override
    public void readAdditionalSaveData(CompoundTag t) {
        super.readAdditionalSaveData(t);
        setVariant(t.getInt("FpeVariant"));
        if (bossEvent != null) bossEvent.setName(getDisplayName());
    }
}
