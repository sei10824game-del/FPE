package com.fpe.entity.characters;

import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.UUID;

import org.joml.Vector3f;

import com.fpe.entity.Ability;
import com.fpe.entity.FpeEntity;
import com.fpe.entity.FpeFx;
import com.fpe.entity.FpeProjectile;
import com.fpe.entity.FpeUtil;

import net.minecraft.core.BlockPos;
import net.minecraft.core.particles.DustParticleOptions;
import net.minecraft.core.particles.ItemParticleOption;
import net.minecraft.core.particles.ParticleOptions;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.tags.DamageTypeTags;
import net.minecraft.world.BossEvent;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.EntityDimensions;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.Pose;
import net.minecraft.world.entity.ai.attributes.AttributeInstance;
import net.minecraft.world.entity.ai.attributes.AttributeModifier;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.ClipContext;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.Vec3;

/**
 * Alice – two-phase boss (docs/ref/confirmed/alice_phase1.jpg / alice_phase2.jpg).
 * Phase 1 (variant 0): crowned girl in a long black coat; her shadow bursts out as spike wings, claws and a whip.
 * At <=50 % hp she is forced into an invulnerable "transform" sequence and becomes (variant 1) a 6.5-block pitch-black
 * giant with shoulder spines, hooked claws, a tail, back tentacles and a glowing yellow grin: ground-tentacle / spike-field attacks.
 * Transformation state == variant, which is saved by FpeEntity, so it happens exactly once.
 * Phase 2 also has a QUADRUPED stance (stance 1): she drops onto her huge claws ("drop_down") when the target runs off,
 * when enraged or every ~200-400 ticks, gallops faster, uses the quad_* attacks and rears back up ("rise_up").
 */
public class Alice extends FpeEntity {
    /** transform timeline (ticks of the "transform" ability) */
    public static final int T_FLIP = 90, T_ROAR = 112, T_END = 130;

    private static final ParticleOptions RED = new DustParticleOptions(new Vector3f(1f, 0.78f, 0.25f), 2.2f);
    private static final ParticleOptions BANDAGE = new ItemParticleOption(ParticleTypes.ITEM, new ItemStack(Items.INK_SAC));

    /** 0 = not transforming, else ticks into the transformation (server only, transient on purpose) */
    private int transformT;
    private boolean holding, flag;
    private Vec3 beamDir = Vec3.ZERO;
    /** ticks spent in the current stance and when to switch again (server only) */
    private int stanceT, nextSwap = 300;
    private final Set<Integer> hitIds = new HashSet<>();
    private static final UUID QUAD_SPEED = UUID.fromString("7d3c1f0a-5b8e-4c2a-9f61-a11ce00d4a01");

    public Alice(EntityType<? extends FpeEntity> type, Level level) { super(type, level); }

    @Override public Faction faction() { return Faction.ALICE; }

    public static AttributeSupplier.Builder attributes() { return baseAttributes(500, 9, 0.34, 6, 0.4); }

    // ------------------------------------------------------------------ phase / boss plumbing
    private static boolean phase(FpeEntity e, int v) { return e.getVariant() == v && ((Alice) e).transformT == 0; }
    private static Ability p1(String id, int dur, int cd) { return Ability.of(id, dur, cd).when(e -> phase(e, 0)); }
    private static Ability p2(String id, int dur, int cd) { return Ability.of(id, dur, cd).when(e -> phase(e, 1) && e.getStance() == 0); }
    /** phase 2, on all fours */
    private static Ability q2(String id, int dur, int cd) { return Ability.of(id, dur, cd).when(e -> phase(e, 1) && e.getStance() == 1); }

    @Override protected boolean hasBossBar() { return true; }
    @Override protected BossEvent.BossBarColor bossColor() { return BossEvent.BossBarColor.RED; }
    @Override public boolean isEnraged() { return getVariant() == 1 && getHealth() < getMaxHealth() * 0.25f; }
    @Override public double preferredDistance() { return getVariant() == 1 ? (getStance() == 1 ? 2.5 : 4.0) : 1.2; }
    @Override protected int restTicks() { return getVariant() == 0 ? 12 : isEnraged() ? 10 : 20; }

    @Override
    public EntityDimensions getDimensions(Pose pose) {
        if (getVariant() != 1) return super.getDimensions(pose);
        return getStance() == 1 ? EntityDimensions.scalable(4.6f, 4.82f) : EntityDimensions.scalable(3.5f, 7.12f);
    }

    @Override
    protected float getStandingEyeHeight(Pose pose, EntityDimensions d) { return d.height * (d.height > 3 ? 0.82f : 0.86f); }

    @Override
    public boolean causeFallDamage(float dist, float mult, DamageSource src) { return false; }

    @Override
    public boolean hurt(DamageSource s, float amount) {
        boolean bypass = s.is(DamageTypeTags.BYPASSES_INVULNERABILITY);
        if (transformT > 0 && !bypass) return false;
        if (getVariant() == 0 && !bypass) // phase 1 can't skip the transformation with one huge hit
            amount = Math.min(amount, Math.max(0.5f, getHealth() - getMaxHealth() * 0.5f + 0.5f));
        return super.hurt(s, amount);
    }

    @Override
    public void tick() {
        super.tick();
        setMaxUpStep(getVariant() == 1 ? 1.6f : 0.6f);
        if (level().isClientSide || !isAlive()) return;
        if (transformT == 0 && getVariant() == 0 && getHealth() <= getMaxHealth() * 0.5f) {
            transformT = 1;
            forceAbility("transform");
            sound(SoundEvents.WARDEN_HEARTBEAT, 2f, 0.6f);
        }
        if (transformT > 0) transformTick(transformT++);
        stanceTick();
    }

    // ------------------------------------------------------------------ quadruped stance switching (phase 2)
    private void stanceTick() {
        stanceT++;
        boolean quad = getStance() == 1;
        AttributeInstance sp = getAttribute(Attributes.MOVEMENT_SPEED);
        if (sp != null && quad != (sp.getModifier(QUAD_SPEED) != null)) {
            if (quad) sp.addTransientModifier(new AttributeModifier(QUAD_SPEED, "alice quad gallop", 0.55, AttributeModifier.Operation.MULTIPLY_TOTAL));
            else sp.removeModifier(QUAD_SPEED);
        }
        if (getVariant() != 1) { if (quad) setStance(0); return; }
        if (transformT > 0 || isBusy()) return;
        LivingEntity t = getTarget();
        if (t == null || !t.isAlive()) return;
        double d = distanceTo(t);
        if (!quad) {
            if (stanceT < 50) return;
            if ((d > 9 && stanceT > 70) || stanceT > nextSwap || (isEnraged() && random.nextInt(90) == 0)) forceAbility("drop_down");
        } else {
            int stay = isEnraged() ? nextSwap * 3 / 2 : nextSwap;
            if (stanceT > stay || (d < 4.5 && stanceT > 120 && random.nextInt(isEnraged() ? 70 : 35) == 0)) forceAbility("rise_up");
        }
    }

    private void switchStance(int s) {
        setStance(s);
        stanceT = 0;
        nextSwap = 200 + random.nextInt(200);
    }

    private void transformTick(int t) {
        Vec3 c = position();
        float k = Math.min(1f, t / (float) T_FLIP);
        setDeltaMovement(0, getDeltaMovement().y, 0);
        if (t < T_FLIP) {
            FpeUtil.particles(this, ParticleTypes.SQUID_INK, c.add(0, 1, 0), 2 + (int) (k * 8), 0.4 + k, 0.8, 0.4 + k, 0.05);
            if (t % 3 == 0) FpeUtil.particles(this, ParticleTypes.LARGE_SMOKE, c.add(0, 0.2, 0), 3 + (int) (k * 10), 1 + k * 2, 0.1, 1 + k * 2, 0.02);
            if (t % 20 == 0) {
                sound(SoundEvents.WARDEN_HEARTBEAT, 2.5f, 0.5f + k * 0.4f);
                FpeUtil.arc(this, ParticleTypes.LARGE_SMOKE, c.add(0, 0.1, 0), 0, 180, 2 + k * 5, 30);
                for (LivingEntity v : FpeUtil.enemiesInRadius(this, c, 8, 3, 1)) FpeUtil.knock(v, c, 0.25, 0.25); // tremor
            }
            if (t == 40 || t == 62 || t == 80) { // bandages tearing off
                FpeUtil.particles(this, BANDAGE, c.add(0, 1, 0), 30, 0.4, 0.8, 0.4, 0.25);
                sound(SoundEvents.WOOL_BREAK, 2f, 0.6f);
                sound(SoundEvents.ZOMBIE_VILLAGER_CURE, 0.6f, 1.6f);
            }
        }
        if (t == T_FLIP) {
            setVariant(1);
            setHealth(getMaxHealth() * 0.6f);
            getAttribute(Attributes.KNOCKBACK_RESISTANCE).setBaseValue(1.0);
            getAttribute(Attributes.ARMOR).setBaseValue(12);
            FpeUtil.particles(this, ParticleTypes.SQUID_INK, c.add(0, 2, 0), 120, 1.5, 2, 1.5, 0.3);
            FpeUtil.particles(this, BANDAGE, c.add(0, 1.5, 0), 50, 1, 1.5, 1, 0.4);
            sound(SoundEvents.WARDEN_EMERGE, 3f, 0.8f);
        }
        if (t > T_FLIP && t < T_ROAR && t % 4 == 0) FpeUtil.particles(this, ParticleTypes.LARGE_SMOKE, c, 10, 1.5, 0.2, 1.5, 0.05);
        if (t == T_ROAR) {
            sound(SoundEvents.WARDEN_ROAR, 4f, 0.7f);
            sound(SoundEvents.GENERIC_EXPLODE, 3f, 0.5f);
            FpeUtil.particles(this, ParticleTypes.EXPLOSION_EMITTER, c.add(0, 1, 0), 1, 0, 0, 0, 0);
            FpeUtil.particles(this, ParticleTypes.SONIC_BOOM, c.add(0, 5, 0), 3, 1, 0.5, 1, 0);
            FpeUtil.fx(this, FpeFx.Kind.RING_SHOCK, c.add(0, 0.1, 0), 0, 18, 13f, dmg(0.6f));
            FpeUtil.hitRadius(this, c, 7, dmg(0.8f), 2.4, 0.6);
            for (LivingEntity v : FpeUtil.enemiesInRadius(this, c, 18, 6, 4)) {
                v.addEffect(new MobEffectInstance(MobEffects.DARKNESS, 120, 0));
                v.addEffect(new MobEffectInstance(MobEffects.BLINDNESS, 30, 0));
            }
        }
        if (t >= T_END) transformT = 0;
    }

    // ------------------------------------------------------------------ sounds
    @Override protected SoundEvent getAmbientSound() { return getVariant() == 1 ? SoundEvents.WARDEN_AMBIENT : SoundEvents.VEX_AMBIENT; }
    @Override protected SoundEvent getHurtSound(DamageSource s) { return getVariant() == 1 ? SoundEvents.WARDEN_HURT : SoundEvents.VEX_HURT; }
    @Override protected SoundEvent getDeathSound() { return getVariant() == 1 ? SoundEvents.WARDEN_DEATH : SoundEvents.VEX_DEATH; }
    @Override protected void playStepSound(BlockPos pos, BlockState st) {
        if (getVariant() == 1) playSound(SoundEvents.WARDEN_STEP, 1.4f, 0.7f); else super.playStepSound(pos, st);
    }
    @Override public float getVoicePitch() { return getVariant() == 1 ? 0.7f : 1.25f; }

    private void sound(SoundEvent s, float vol, float pitch) { FpeUtil.sound(this, s, vol, pitch); }

    // ------------------------------------------------------------------ helpers
    /** top of the first solid block near (x,z) around refY, falls back to refY */
    private double groundY(double x, double z, double refY) {
        BlockPos.MutableBlockPos p = new BlockPos.MutableBlockPos(x, refY + 3, z);
        for (int i = 0; i < 10; i++, p.move(0, -1, 0)) {
            BlockPos b = p.below();
            if (level().getBlockState(p).getCollisionShape(level(), p).isEmpty() && !level().getBlockState(b).getCollisionShape(level(), b).isEmpty()) return p.getY();
        }
        return refY;
    }

    private FpeFx spike(double x, double z, double refY, int warm, int life, float dmg, float h) {
        return FpeUtil.fx(this, FpeFx.Kind.SPIKE, new Vec3(x, groundY(x, z, refY), z), warm, life, 1.2f, dmg).param(h);
    }

    private FpeFx tentacle(double x, double z, double refY, int warm, int life, float h) {
        return FpeUtil.fx(this, FpeFx.Kind.TENTACLE, new Vec3(x, groundY(x, z, refY), z), warm, life, 1.6f, dmg(0.55f)).param(h);
    }

    private void spikeRing(Vec3 c, double r, int n, int warm, float h, float off) {
        for (int i = 0; i < n; i++) {
            double a = Math.PI * 2 * (i + off) / n;
            spike(c.x + Math.cos(a) * r, c.z + Math.sin(a) * r, c.y, warm, 34, dmg(0.8f), h);
        }
    }

    private void arcFx(double up, float radius, float sweep, float tilt, float yawOff, int color) {
        FpeFx f = FpeUtil.fx(this, FpeFx.Kind.ARC, position().add(0, up, 0), 0, 8, radius, 0).param(sweep).color(color);
        f.setYRot(getYRot() + yawOff); f.yRotO = f.getYRot();
        f.setXRot(tilt); f.xRotO = tilt;
    }

    private void lineParticles(ParticleOptions p, Vec3 a, Vec3 b, double step) {
        Vec3 d = b.subtract(a);
        int n = (int) Math.max(1, d.length() / step);
        for (int i = 0; i <= n; i++) FpeUtil.particles(this, p, a.add(d.scale(i / (double) n)), 1, 0.05, 0.05, 0.05, 0);
    }

    private static Vec3 chest(LivingEntity t) { return t.position().add(0, t.getBbHeight() * 0.6, 0); }
    private Vec3 flatDir(LivingEntity t) {
        Vec3 d = new Vec3(t.getX() - getX(), 0, t.getZ() - getZ());
        return d.lengthSqr() < 1e-4 ? FpeUtil.forward(this) : d.normalize();
    }
    private boolean inFront(LivingEntity t, double range, double halfDeg) {
        Vec3 d = new Vec3(t.getX() - getX(), 0, t.getZ() - getZ());
        if (d.length() - getBbWidth() * 0.5 - t.getBbWidth() * 0.5 > range) return false;
        return d.lengthSqr() < 0.01 || Math.toDegrees(Math.acos(Math.max(-1, Math.min(1, d.normalize().dot(FpeUtil.forward(this)))))) <= halfDeg;
    }
    /** drag a held victim toward a point (smooth, works for players since hurtMarked syncs velocity) */
    private static void holdAt(LivingEntity v, Vec3 p) {
        v.setDeltaMovement(p.subtract(v.position()).scale(0.6));
        v.hurtMarked = true;
        v.fallDistance = 0;
    }

    // ------------------------------------------------------------------ abilities
    @Override
    protected void registerAbilities(List<Ability> out) {
        // ======================= PHASE 1 =======================
        // two black wing-spikes lance out at the target one after another
        out.add(p1("wing_stab", 36, 50).range(0, 6.5).weight(3).faceUntil(22).tick((e, t, tk) -> {
            if (tk == 6) sound(SoundEvents.PHANTOM_FLAP, 1f, 1.6f);
            if (tk == 12 || tk == 23) {
                Alice a = (Alice) e;
                Vec3 from = a.position().add(0, 1.4, 0).add(FpeUtil.right(a).scale(tk == 12 ? 0.5 : -0.5));
                Vec3 to = from.add(chest(t).subtract(from).normalize().scale(6.5));
                FpeUtil.hitLine(a, from, to, 0.55, a.dmg(0.9f), 0.5, 0.15);
                a.lineParticles(ParticleTypes.SQUID_INK, from, to, 0.5);
                a.sound(SoundEvents.TRIDENT_THROW, 1f, 0.6f);
            }
        }));
        // 360 degree sweep with all six wings extended
        out.add(p1("wing_whirl", 32, 70).range(0, 4.5).weight(2).faceUntil(10).tick((e, t, tk) -> {
            Alice a = (Alice) e;
            if (tk == 10) a.sound(SoundEvents.PLAYER_ATTACK_SWEEP, 1.2f, 0.6f);
            if (tk == 15) {
                FpeUtil.hitRadius(a, a.position(), 4.3, a.dmg(1.3f), 1.2, 0.4);
                a.arcFx(1.1, 4.3f, 360, 0, 0, 0xEE101016);
                FpeUtil.arc(a, ParticleTypes.SQUID_INK, a.position().add(0, 1.1, 0), 0, 180, 3.6, 28);
            }
        }));
        // a shadow whip lashes out of her sleeve, hooks the target and yanks it in
        out.add(p1("shadow_whip", 34, 60).range(2.5, 10).weight(2).faceUntil(12).start((e, t, tk) -> ((Alice) e).flag = false).tick((e, t, tk) -> {
            Alice a = (Alice) e;
            if (tk == 6) a.sound(SoundEvents.WOOL_PLACE, 1f, 0.5f);
            if (tk == 12) {
                Vec3 from = a.position().add(0, 1.5, 0).add(FpeUtil.right(a).scale(0.4));
                Vec3 to = from.add(chest(t).subtract(from).normalize().scale(10));
                a.lineParticles(ParticleTypes.SQUID_INK, from, to, 0.6);
                a.sound(SoundEvents.FISHING_BOBBER_THROW, 1.2f, 0.6f);
                if (t.getBoundingBox().inflate(0.6).clip(from, to).isPresent() && FpeUtil.hit(a, t, a.dmg(0.7f), 0, 0)) a.flag = true;
            }
            if (tk == 22 && a.flag) {
                Vec3 d = a.position().subtract(t.position());
                Vec3 v = new Vec3(d.x, 0, d.z).normalize().scale(Math.min(1.7, d.length() * 0.24));
                t.setDeltaMovement(v.x, 0.4, v.z);
                t.hurtMarked = true;
                t.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 40, 1));
                a.sound(SoundEvents.FISHING_BOBBER_RETRIEVE, 1.2f, 0.5f);
            }
        }));
        // slams a hand down: a line of black spikes races toward the target
        out.add(p1("spike_line", 38, 70).range(3, 14).weight(2).faceUntil(13).tick((e, t, tk) -> {
            Alice a = (Alice) e;
            if (tk == 14) {
                Vec3 d = a.flatDir(t), side = new Vec3(-d.z, 0, d.x);
                for (int i = 0; i < 12; i++) {
                    Vec3 p = a.position().add(d.scale(1.5 + i * 1.2)).add(side.scale((i % 2 == 0 ? 0.35 : -0.35)));
                    a.spike(p.x, p.z, a.getY(), 3 + i * 2, 30 + i * 2, a.dmg(0.9f), 1f + i * 0.06f);
                }
                FpeUtil.particles(a, ParticleTypes.SQUID_INK, FpeUtil.ahead(a, 1, 0.1), 20, 0.4, 0.1, 0.4, 0.1);
                a.sound(SoundEvents.EVOKER_PREPARE_ATTACK, 1f, 0.6f);
            }
        }));
        // melts into shadow, reappears behind the target and rakes twice
        out.add(p1("blink_rake", 30, 90).range(3, 16).weight(2).blind().tick((e, t, tk) -> {
            Alice a = (Alice) e;
            if (tk == 8) {
                FpeUtil.particles(a, ParticleTypes.SQUID_INK, a.position().add(0, 1, 0), 30, 0.3, 0.7, 0.3, 0.05);
                FpeUtil.particles(a, ParticleTypes.PORTAL, a.position().add(0, 1, 0), 30, 0.3, 0.7, 0.3, 0.5);
                a.sound(SoundEvents.ENDERMAN_TELEPORT, 1f, 0.6f);
            }
            if (tk == 10) {
                Vec3[] tries = { t.position().subtract(FpeUtil.forward(t).scale(1.8)), t.position().add(FpeUtil.right(t).scale(1.8)), t.position().subtract(FpeUtil.right(t).scale(1.8)) };
                for (Vec3 p : tries) {
                    if (a.level().noCollision(a, a.getBoundingBox().move(p.subtract(a.position())))) { a.teleportTo(p.x, p.y, p.z); break; }
                }
                a.snapFace(t);
                FpeUtil.particles(a, ParticleTypes.SQUID_INK, a.position().add(0, 1, 0), 30, 0.3, 0.7, 0.3, 0.05);
                a.sound(SoundEvents.ENDERMAN_TELEPORT, 1f, 0.8f);
            }
            if (tk == 15 || tk == 21) {
                FpeUtil.hitCone(a, 2.8, 70, a.dmg(tk == 15 ? 0.8f : 1.0f), tk == 15 ? 0.2 : 0.9, 0.25);
                a.arcFx(1.2, 2.6f, 140, tk == 15 ? 35 : -35, 0, 0xDD2A0A0A);
                a.sound(SoundEvents.PLAYER_ATTACK_SWEEP, 1f, 1.3f);
            }
        }));
        // hovers, wings spread, and spits shadow orbs from the wing tips
        out.add(p1("shadow_volley", 40, 80).range(5, 18).weight(2).tick((e, t, tk) -> {
            Alice a = (Alice) e;
            if (tk == 4) a.sound(SoundEvents.EVOKER_PREPARE_SUMMON, 1f, 1.3f);
            if (tk >= 10 && tk <= 26 && (tk - 10) % 4 == 0) {
                int i = (tk - 10) / 4;
                Vec3 from = a.position().add(0, 1.8 + (i % 3) * 0.3, 0).add(FpeUtil.right(a).scale(i % 2 == 0 ? 1.2 : -1.2)).subtract(FpeUtil.forward(a).scale(0.3));
                FpeUtil.projectile(a, FpeProjectile.Kind.SHADOW_ORB, from, FpeUtil.aim(from, t, 0.55, 0.2), a.dmg(0.6f));
                a.sound(SoundEvents.EVOKER_CAST_SPELL, 0.8f, 1.4f);
            }
        }));
        // pounces, pins the victim, mauls it with wings and throws it
        out.add(p1("grab_maul", 48, 90).range(0, 3.2).weight(2).faceUntil(12).start((e, t, tk) -> ((Alice) e).holding = false).tick((e, t, tk) -> {
            Alice a = (Alice) e;
            if (tk == 8) a.dashToward(t.position(), 0.6, 0.1);
            if (tk == 11 && a.inFront(t, 2.4, 50) && FpeUtil.hit(a, t, a.dmg(0.5f), 0, 0)) { a.holding = true; a.sound(SoundEvents.PHANTOM_BITE, 1f, 0.7f); }
            if (!a.holding) return;
            if (tk > 11 && tk < 38) holdAt(t, FpeUtil.ahead(a, 1.2, 0.1));
            if (tk == 18 || tk == 28) {
                FpeUtil.hit(a, t, a.dmg(0.55f), 0, 0);
                FpeUtil.particles(a, ParticleTypes.DAMAGE_INDICATOR, chest(t), 6, 0.3, 0.3, 0.3, 0.1);
                a.sound(SoundEvents.PHANTOM_BITE, 1f, 0.6f);
            }
            if (tk == 38) {
                a.holding = false;
                if (FpeUtil.hit(a, t, a.dmg(0.9f), 1.9, 0.7)) a.sound(SoundEvents.PLAYER_ATTACK_KNOCKBACK, 1f, 0.6f);
            }
        }));
        // shrieking blast: knockback, nausea, weakness
        out.add(p1("scream", 36, 110).range(0, 6).weight(1).tick((e, t, tk) -> {
            Alice a = (Alice) e;
            if (tk == 14) {
                a.sound(SoundEvents.GHAST_SCREAM, 2f, 1.5f);
                a.sound(SoundEvents.VEX_CHARGE, 2f, 0.6f);
                FpeUtil.particles(a, ParticleTypes.SONIC_BOOM, a.position().add(0, 1.5, 0), 1, 0, 0, 0, 0);
                for (int r = 2; r <= 6; r += 2) FpeUtil.arc(a, ParticleTypes.SQUID_INK, a.position().add(0, 1, 0), 0, 180, r, 10 + r * 4);
                FpeUtil.hitRadius(a, a.position(), 6, a.dmg(0.5f), 1.7, 0.5);
                for (LivingEntity v : FpeUtil.enemiesInRadius(a, a.position(), 7, 3, 1)) {
                    v.addEffect(new MobEffectInstance(MobEffects.CONFUSION, 100, 0));
                    v.addEffect(new MobEffectInstance(MobEffects.WEAKNESS, 80, 0));
                }
            }
        }));
        // drives all wings into the floor: three widening rings of spikes burst around her
        out.add(p1("wing_burrow", 40, 90).range(0, 6).weight(2).tick((e, t, tk) -> {
            Alice a = (Alice) e;
            if (tk == 14) { a.sound(SoundEvents.EVOKER_FANGS_ATTACK, 1.2f, 0.5f); a.spikeRing(a.position(), 2.2, 6, 2, 1.1f, 0); }
            if (tk == 20) a.spikeRing(a.position(), 4.0, 10, 2, 1.3f, 0.5f);
            if (tk == 26) a.spikeRing(a.position(), 5.8, 14, 2, 1.5f, 0.25f);
        }));
        // skittering dash that ends in a double wing lance
        out.add(p1("skitter", 26, 50).range(4, 12).weight(2).faceUntil(8).tick((e, t, tk) -> {
            Alice a = (Alice) e;
            if (tk == 6) { a.dashToward(t.position(), 1.3, 0.15); a.sound(SoundEvents.SPIDER_AMBIENT, 1f, 1.6f); }
            if (tk > 6 && tk < 15) FpeUtil.particles(a, ParticleTypes.SQUID_INK, a.position().add(0, 0.5, 0), 2, 0.2, 0.3, 0.2, 0.01);
            if (tk == 15) { FpeUtil.hitCone(a, 3.0, 50, a.dmg(1.1f), 0.8, 0.25); a.sound(SoundEvents.TRIDENT_HIT, 1f, 0.7f); }
        }));
        // heel stomp: shadow hands claw up under and around the target, she clenches her fist to squeeze
        out.add(p1("ground_grasp", 40, 90).range(2, 14).weight(2).blind().tick((e, t, tk) -> {
            Alice a = (Alice) e;
            if (tk == 6) a.sound(SoundEvents.SCULK_CLICKING, 1.2f, 0.6f);
            if (tk == 14) {
                a.sound(SoundEvents.WARDEN_STEP, 1.5f, 1.2f);
                FpeUtil.fx(a, FpeFx.Kind.RING_SHOCK, a.position().add(0, 0.1, 0), 0, 8, 3f, 0);
                Vec3 c = t.position();
                FpeUtil.fx(a, FpeFx.Kind.TENTACLE, new Vec3(c.x, a.groundY(c.x, c.z, c.y), c.z), 6, 40, 1.3f, a.dmg(0.6f)).param(1.0f);
                for (int i = 0; i < 3; i++) {
                    double ang = Math.PI * 2 * i / 3 + a.random.nextDouble();
                    a.spike(c.x + Math.cos(ang) * 1.6, c.z + Math.sin(ang) * 1.6, c.y, 8 + i * 2, 26, a.dmg(0.6f), 0.9f);
                }
            }
            if (tk == 24) for (LivingEntity v : FpeUtil.enemiesInRadius(a, t.position(), 2.5, 2, 1)) {
                FpeUtil.hit(a, v, a.dmg(0.6f), 0, 0.1);
                v.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 50, 2));
                a.sound(SoundEvents.SCULK_SHRIEKER_BREAK, 1f, 0.6f);
            }
        }));
        // forced by tick(): the transformation (logic lives in transformTick so it survives a lost target)
        out.add(Ability.of("transform", T_END, 0).when(e -> false).blind());

        // ======================= PHASE 2 =======================
        // smashes both claws into the ground: tentacles burst under and around the target
        out.add(p2("tentacle_field", 46, 110).range(3, 16).weight(3).blind().tick((e, t, tk) -> {
            Alice a = (Alice) e;
            if (tk == 6) a.sound(SoundEvents.WARDEN_ANGRY, 2f, 0.7f);
            if (tk == 18) {
                FpeUtil.particles(a, ParticleTypes.SQUID_INK, FpeUtil.ahead(a, 3.5, 0.2), 40, 1.2, 0.2, 1.2, 0.15);
                a.sound(SoundEvents.GENERIC_EXPLODE, 1.5f, 0.6f);
                Vec3 c = t.position();
                a.tentacle(c.x, c.z, c.y, 10, 90, 1.7f);
                for (int i = 0; i < 6; i++) {
                    double ang = Math.PI * 2 * i / 6 + a.random.nextDouble() * 0.4;
                    a.tentacle(c.x + Math.cos(ang) * 2.7, c.z + Math.sin(ang) * 2.7, c.y, 14 + i * 2, 90, 1.2f + a.random.nextFloat() * 0.5f);
                }
                for (int s = -1; s <= 1; s += 2) { Vec3 h = FpeUtil.ahead(a, 3.5, 0).add(FpeUtil.right(a).scale(s * 1.8)); a.tentacle(h.x, h.z, a.getY(), 6, 60, 1.0f); }
            }
        }));
        // claws rake the floor: a widening carpet of black spikes rolls toward the target
        out.add(p2("spike_carpet", 48, 100).range(3, 14).weight(3).faceUntil(14).tick((e, t, tk) -> {
            Alice a = (Alice) e;
            if (tk == 16) {
                a.sound(SoundEvents.EVOKER_FANGS_ATTACK, 2f, 0.4f);
                Vec3 d = a.flatDir(t), side = new Vec3(-d.z, 0, d.x);
                for (int r = 0; r < 10; r++) {
                    int w = 1 + r / 3;
                    for (int s = -w; s <= w; s++) {
                        Vec3 p = a.position().add(d.scale(2.6 + r * 1.3)).add(side.scale(s * 1.3 + (r % 2) * 0.6));
                        a.spike(p.x, p.z, a.getY(), 4 + r * 2, 30 + r * 2, a.dmg(0.85f), 1.3f + r * 0.08f + a.random.nextFloat() * 0.3f);
                    }
                }
            }
        }));
        // huge overhead claw slam with shockwave
        out.add(p2("claw_slam", 44, 70).range(0, 7.5).weight(3).faceUntil(16).tick((e, t, tk) -> {
            Alice a = (Alice) e;
            if (tk == 4) a.sound(SoundEvents.WARDEN_ATTACK_IMPACT, 1f, 0.5f);
            if (tk == 21) {
                Vec3 p = FpeUtil.ahead(a, 4.5, 0);
                FpeUtil.hitRadius(a, p, 3.2, a.dmg(1.9f), 1.2, 0.7);
                FpeUtil.fx(a, FpeFx.Kind.RING_SHOCK, new Vec3(p.x, a.groundY(p.x, p.z, a.getY()) + 0.1, p.z), 0, 14, 8f, a.dmg(0.7f));
                FpeUtil.particles(a, ParticleTypes.EXPLOSION, p, 4, 1, 0.2, 1, 0);
                FpeUtil.particles(a, ParticleTypes.SQUID_INK, p, 30, 1.5, 0.3, 1.5, 0.2);
                a.sound(SoundEvents.GENERIC_EXPLODE, 2f, 0.55f);
            }
        }));
        // two giant crescent claw sweeps
        out.add(p2("double_sweep", 46, 70).range(0, 8.5).weight(3).tick((e, t, tk) -> {
            Alice a = (Alice) e;
            if (tk == 15 || tk == 27) {
                FpeUtil.hitCone(a, 7.5, 100, a.dmg(1.3f), 1.4, 0.4);
                a.arcFx(2.6, 7.5f, 200, tk == 15 ? 15 : -15, 0, 0xEE0A0A0E);
                a.sound(SoundEvents.PLAYER_ATTACK_SWEEP, 2f, 0.5f);
                a.sound(SoundEvents.WARDEN_ATTACK_IMPACT, 1f, 0.8f);
            }
        }));
        // snatches the target, lifts it, crushes it twice and smashes it into the ground
        out.add(p2("grab_crush", 56, 120).range(0, 6.5).weight(2).faceUntil(16).start((e, t, tk) -> ((Alice) e).holding = false).tick((e, t, tk) -> {
            Alice a = (Alice) e;
            if (tk == 16 && a.inFront(t, 6.0, 40) && FpeUtil.hit(a, t, a.dmg(0.6f), 0, 0)) { a.holding = true; a.sound(SoundEvents.WARDEN_ATTACK_IMPACT, 1.5f, 0.6f); }
            if (!a.holding) return;
            if (tk > 16 && tk < 46) holdAt(t, a.position().add(FpeUtil.forward(a).scale(3.0)).add(0, 2.5 + 2.2 * Math.min(1, (tk - 16) / 10.0), 0));
            if (tk == 26 || tk == 36) {
                FpeUtil.hit(a, t, a.dmg(0.7f), 0, 0);
                FpeUtil.particles(a, ParticleTypes.CRIT, chest(t), 15, 0.4, 0.4, 0.4, 0.2);
                a.sound(SoundEvents.SKELETON_HURT, 1f, 0.4f);
            }
            if (tk == 46) {
                a.holding = false;
                t.setDeltaMovement(0, -1.5, 0); t.hurtMarked = true;
                FpeUtil.hit(a, t, a.dmg(1.3f), 1.4, 0.3);
                Vec3 p = FpeUtil.ahead(a, 3.0, 0);
                FpeUtil.fx(a, FpeFx.Kind.RING_SHOCK, new Vec3(p.x, a.groundY(p.x, p.z, a.getY()) + 0.1, p.z), 0, 10, 5f, a.dmg(0.4f));
                a.sound(SoundEvents.GENERIC_EXPLODE, 1.5f, 0.7f);
            }
        }));
        // three hard beats of the bug wings: gale that hurls everything away
        out.add(p2("wing_gust", 48, 100).range(0, 12).weight(2).tick((e, t, tk) -> {
            Alice a = (Alice) e;
            if (tk == 18 || tk == 26 || tk == 34) {
                FpeUtil.hitCone(a, 12, 55, a.dmg(0.25f), 1.8, 0.35);
                for (int i = 0; i < 6; i++) {
                    Vec3 o = a.position().add(0, 1 + i * 0.8, 0).add(FpeUtil.right(a).scale((a.random.nextDouble() - 0.5) * 4));
                    a.lineParticles(ParticleTypes.CLOUD, o, o.add(FpeUtil.forward(a).scale(9)), 1.0);
                }
                a.sound(SoundEvents.ENDER_DRAGON_FLAP, 2f, 0.8f);
            }
        }));
        // rears up and vomits a barrage of homing shadow orbs
        out.add(p2("orb_barrage", 52, 110).range(6, 20).weight(2).tick((e, t, tk) -> {
            Alice a = (Alice) e;
            if (tk == 6) a.sound(SoundEvents.WARDEN_SONIC_CHARGE, 2f, 1.2f);
            if (tk >= 14 && tk <= 38 && (tk - 14) % 3 == 0) {
                Vec3 from = a.position().add(0, 5.2, 0).add(FpeUtil.forward(a).scale(1.2));
                Vec3 v = FpeUtil.aim(from, t, 0.5, 0.2).add((a.random.nextDouble() - 0.5) * 0.3, a.random.nextDouble() * 0.15, (a.random.nextDouble() - 0.5) * 0.3);
                FpeUtil.projectile(a, FpeProjectile.Kind.SHADOW_ORB, from, v, a.dmg(0.5f));
                a.sound(SoundEvents.EVOKER_CAST_SPELL, 1f, 0.7f);
            }
        }));
        // deafening roar: darkness, blindness, shockwave
        out.add(p2("roar", 50, 220).range(0, 14).weight(1).blind().tick((e, t, tk) -> {
            Alice a = (Alice) e;
            if (tk == 18) {
                a.sound(SoundEvents.WARDEN_ROAR, 4f, 0.8f);
                FpeUtil.particles(a, ParticleTypes.SONIC_BOOM, a.position().add(0, 5, 0).add(FpeUtil.forward(a).scale(2)), 3, 1, 0.5, 1, 0);
                FpeUtil.fx(a, FpeFx.Kind.RING_SHOCK, a.position().add(0, 0.1, 0), 0, 16, 12f, a.dmg(0.6f));
                FpeUtil.hitRadius(a, a.position(), 6, a.dmg(0.6f), 2.3, 0.6);
                for (LivingEntity v : FpeUtil.enemiesInRadius(a, a.position(), 16, 6, 4)) {
                    v.addEffect(new MobEffectInstance(MobEffects.DARKNESS, 120, 0));
                    v.addEffect(new MobEffectInstance(MobEffects.BLINDNESS, 25, 0));
                }
            }
        }));
        // crouches, leaps onto the target and lands with a spike-ringed shockwave
        out.add(p2("leap_slam", 52, 100).range(6, 16).weight(2).faceUntil(14).start((e, t, tk) -> ((Alice) e).flag = false).tick((e, t, tk) -> {
            Alice a = (Alice) e;
            if (tk == 14) {
                a.dashToward(t.position(), Math.max(0.4, Math.min(1.5, a.distanceTo(t) / 11.0)), 0.95);
                a.sound(SoundEvents.RAVAGER_ROAR, 2f, 0.6f);
            }
            if (!a.flag && tk >= 22 && (a.onGround() || tk == 40)) {
                a.flag = true;
                FpeUtil.hitRadius(a, a.position(), 5, a.dmg(1.7f), 1.6, 0.7);
                FpeUtil.fx(a, FpeFx.Kind.RING_SHOCK, a.position().add(0, 0.1, 0), 0, 16, 10f, a.dmg(0.6f));
                a.spikeRing(a.position(), 3.6, 10, 3, 1.6f, 0);
                FpeUtil.particles(a, ParticleTypes.EXPLOSION, a.position(), 6, 2, 0.2, 2, 0);
                a.sound(SoundEvents.GENERIC_EXPLODE, 2.5f, 0.5f);
            }
        }));
        // charges, then sweeps a crimson eye beam that slowly tracks the target
        out.add(p2("eye_beam", 62, 110).range(6, 24).weight(2).faceUntil(30).tick((e, t, tk) -> {
            Alice a = (Alice) e;
            Vec3 eye = a.getEyePosition().add(FpeUtil.forward(a).scale(1.2));
            if (tk < 30) {
                if (tk % 2 == 0) FpeUtil.particles(a, RED, eye, 4, 0.8, 0.8, 0.8, 0.02);
                if (tk == 2) a.sound(SoundEvents.WARDEN_SONIC_CHARGE, 3f, 0.8f);
                return;
            }
            if (tk > 52) return;
            Vec3 want = chest(t).subtract(eye).normalize();
            a.beamDir = tk == 30 ? want : a.beamDir.add(want.subtract(a.beamDir).scale(0.08)).normalize();
            Vec3 end = eye.add(a.beamDir.scale(24));
            end = a.level().clip(new ClipContext(eye, end, ClipContext.Block.COLLIDER, ClipContext.Fluid.NONE, a)).getLocation();
            float yaw = (float) Math.toDegrees(Math.atan2(a.beamDir.z, a.beamDir.x)) - 90f;
            a.setYRot(yaw); a.yBodyRot = yaw; a.yHeadRot = yaw;
            a.lineParticles(RED, eye, end, 0.7);
            FpeUtil.particles(a, ParticleTypes.LAVA, end, 2, 0.2, 0.1, 0.2, 0);
            if ((tk - 30) % 5 == 0) {
                FpeUtil.hitLine(a, eye, end, 0.7, a.dmg(0.45f), 0.3, 0.05);
                a.sound(SoundEvents.WARDEN_SONIC_BOOM, 0.7f, 1.6f);
            }
        }));
        // spreads arms and wings: a vortex drags everything in, then claps it shut
        out.add(p2("vortex", 72, 160).range(3, 16).weight(2).blind().tick((e, t, tk) -> {
            Alice a = (Alice) e;
            Vec3 c = a.position();
            if (tk == 16) a.sound(SoundEvents.ELYTRA_FLYING, 2f, 0.5f);
            if (tk >= 18 && tk < 58) {
                for (LivingEntity v : FpeUtil.enemiesInRadius(a, c, 16, 6, 3)) {
                    Vec3 d = new Vec3(c.x - v.getX(), 0, c.z - v.getZ());
                    if (d.lengthSqr() < 4) continue;
                    v.setDeltaMovement(v.getDeltaMovement().add(d.normalize().scale(0.085)));
                    v.hurtMarked = true;
                }
                if (tk % 2 == 0) {
                    double r = 14 - (tk - 18) * 0.28;
                    FpeUtil.arc(a, ParticleTypes.SQUID_INK, c.add(0, 0.4, 0), tk * 23f, 50, r, 8);
                    FpeUtil.arc(a, ParticleTypes.PORTAL, c.add(0, 0.8, 0), tk * 23f + 180, 50, r * 0.8, 8);
                }
            }
            if (tk == 60) {
                FpeUtil.hitRadius(a, c, 5, a.dmg(1.6f), 2.2, 0.6);
                FpeUtil.fx(a, FpeFx.Kind.RING_SHOCK, c.add(0, 0.1, 0), 0, 12, 8f, a.dmg(0.5f));
                FpeUtil.particles(a, ParticleTypes.EXPLOSION, FpeUtil.ahead(a, 2, 3), 5, 1, 1, 1, 0);
                a.sound(SoundEvents.GENERIC_EXPLODE, 2f, 0.6f);
            }
        }));
        // arms to the sky: spikes rain up out of the ground all around the target
        out.add(p2("black_rain", 66, 140).range(0, 20).weight(2).blind().tick((e, t, tk) -> {
            Alice a = (Alice) e;
            if (tk == 12) a.sound(SoundEvents.WITHER_AMBIENT, 2f, 0.5f);
            if (tk >= 20 && tk <= 60 && tk % 3 == 0) {
                double x, z;
                if (tk % 9 == 0) { x = t.getX() + t.getDeltaMovement().x * 6; z = t.getZ() + t.getDeltaMovement().z * 6; }
                else { double ang = a.random.nextDouble() * Math.PI * 2, r = a.random.nextDouble() * 6; x = t.getX() + Math.cos(ang) * r; z = t.getZ() + Math.sin(ang) * r; }
                a.spike(x, z, t.getY(), 12, 40, a.dmg(0.75f), 1.2f + a.random.nextFloat() * 1.2f);
                FpeUtil.particles(a, ParticleTypes.SQUID_INK, new Vec3(x, t.getY() + 5, z), 6, 0.2, 2.5, 0.2, 0);
            }
        }));
        // quick stomp for targets under her feet
        out.add(p2("stomp", 30, 40).range(0, 4.5).weight(3).tick((e, t, tk) -> {
            Alice a = (Alice) e;
            if (tk == 12) {
                FpeUtil.hitRadius(a, FpeUtil.ahead(a, 1.2, 0), 3.2, a.dmg(1.2f), 1.3, 0.5);
                FpeUtil.fx(a, FpeFx.Kind.RING_SHOCK, a.position().add(0, 0.1, 0), 0, 10, 5f, a.dmg(0.4f));
                a.sound(SoundEvents.WARDEN_STEP, 3f, 0.5f);
                a.sound(SoundEvents.GENERIC_EXPLODE, 1f, 0.8f);
            }
        }));
        // tail sweep: spins round, the spiked tail mows a full circle and flings everything outward
        out.add(p2("tail_lash", 40, 70).range(0, 7).weight(3).tick((e, t, tk) -> {
            Alice a = (Alice) e;
            if (tk == 8) a.sound(SoundEvents.WARDEN_ATTACK_IMPACT, 1.2f, 0.4f);
            if (tk == 16) {
                FpeUtil.hitRadius(a, a.position(), 6.5, a.dmg(1.2f), 2.2, 0.5);
                a.arcFx(0.8, 6.5f, 360, 0, 0, 0xEE08080B);
                FpeUtil.arc(a, ParticleTypes.SQUID_INK, a.position().add(0, 0.6, 0), 0, 180, 6, 40);
                a.sound(SoundEvents.PLAYER_ATTACK_SWEEP, 2f, 0.4f);
            }
        }));
        // four back tentacles whip over her shoulders one after another (long reach lances)
        out.add(p2("tentacle_lash", 44, 80).range(3, 11).weight(3).faceUntil(26).tick((e, t, tk) -> {
            Alice a = (Alice) e;
            if (tk == 4) a.sound(SoundEvents.SCULK_SHRIEKER_SHRIEK, 1.2f, 0.5f);
            if (tk == 14 || tk == 19 || tk == 24 || tk == 29) {
                int i = (tk - 14) / 5;
                Vec3 from = a.position().add(0, 5.2 - (i / 2) * 0.8, 0).add(FpeUtil.right(a).scale(i % 2 == 0 ? 1.2 : -1.2));
                Vec3 to = from.add(chest(t).subtract(from).normalize().scale(11));
                FpeUtil.hitLine(a, from, to, 0.9, a.dmg(0.8f), 0.6, 0.2);
                a.lineParticles(ParticleTypes.SQUID_INK, from, to, 0.5);
                a.sound(SoundEvents.TRIDENT_THROW, 1.4f, 0.4f);
            }
        }));
        // drives both claws into the ground: six lines of black spikes and tentacles erupt outward like a starburst
        out.add(p2("eruption", 60, 140).range(0, 14).weight(2).blind().tick((e, t, tk) -> {
            Alice a = (Alice) e;
            if (tk == 6) { a.sound(SoundEvents.WARDEN_ROAR, 2.5f, 1.1f); }
            if (tk == 16) {
                a.sound(SoundEvents.GENERIC_EXPLODE, 2.5f, 0.5f);
                FpeUtil.fx(a, FpeFx.Kind.RING_SHOCK, a.position().add(0, 0.1, 0), 0, 14, 7f, a.dmg(0.6f));
                FpeUtil.particles(a, ParticleTypes.SQUID_INK, a.position(), 60, 2, 0.3, 2, 0.3);
                double base = Math.atan2(t.getZ() - a.getZ(), t.getX() - a.getX());
                for (int l = 0; l < 6; l++) {
                    double ang = base + Math.PI * 2 * l / 6;
                    for (int i = 0; i < 7; i++) {
                        double r = 2.8 + i * 1.6;
                        double x = a.getX() + Math.cos(ang) * r, z = a.getZ() + Math.sin(ang) * r;
                        a.spike(x, z, a.getY(), 2 + i * 3, 30, a.dmg(0.85f), 1.4f + i * 0.15f);
                    }
                    double r = 2.8 + 7 * 1.6;
                    a.tentacle(a.getX() + Math.cos(ang) * r, a.getZ() + Math.sin(ang) * r, a.getY(), 24, 60, 1.6f);
                }
            }
            if (tk == 40) FpeUtil.hitRadius(a, a.position(), 4, a.dmg(0.9f), 1.6, 0.6);
        }));
        // ENRAGED finisher: tentacle cage, three spike rings, then a world-shaking double-claw slam
        out.add(Ability.of("abyss", 86, 300).when(e -> phase(e, 1) && e.getStance() == 0 && e.isEnraged()).range(0, 16).weight(4).blind().tick((e, t, tk) -> {
            Alice a = (Alice) e;
            if (tk == 4) { a.sound(SoundEvents.WARDEN_ROAR, 4f, 0.5f); a.sound(SoundEvents.WITHER_SPAWN, 1.5f, 0.6f); }
            if (tk == 20) {
                Vec3 c = t.position();
                a.tentacle(c.x, c.z, c.y, 8, 80, 1.8f);
                for (int i = 0; i < 8; i++) { double ang = Math.PI * 2 * i / 8; a.tentacle(c.x + Math.cos(ang) * 3, c.z + Math.sin(ang) * 3, c.y, 10 + i, 80, 1.5f); }
            }
            if (tk == 34) a.spikeRing(a.position(), 3.5, 10, 3, 1.6f, 0);
            if (tk == 42) a.spikeRing(a.position(), 6.5, 18, 3, 1.9f, 0.5f);
            if (tk == 50) a.spikeRing(a.position(), 9.5, 26, 3, 2.2f, 0.25f);
            if (tk == 66) {
                Vec3 p = FpeUtil.ahead(a, 4, 0);
                FpeUtil.hitRadius(a, p, 5, a.dmg(2.2f), 2.0, 0.8);
                FpeUtil.fx(a, FpeFx.Kind.RING_SHOCK, a.position().add(0, 0.1, 0), 0, 20, 14f, a.dmg(0.9f));
                FpeUtil.particles(a, ParticleTypes.EXPLOSION_EMITTER, p, 1, 0, 0, 0, 0);
                FpeUtil.particles(a, ParticleTypes.SQUID_INK, p, 80, 3, 0.5, 3, 0.3);
                a.sound(SoundEvents.GENERIC_EXPLODE, 3f, 0.4f);
            }
        }));
        // ======================= PHASE 2 - QUADRUPED STANCE =======================
        // forced by stanceTick(): topples forward onto her claws (stance flips on the claw slam)
        out.add(Ability.of("drop_down", 26, 0).when(e -> false).blind().tick((e, t, tk) -> {
            Alice a = (Alice) e;
            if (tk == 2) a.sound(SoundEvents.WARDEN_ANGRY, 2f, 0.6f);
            if (tk == 14) {
                a.switchStance(1);
                Vec3 p = FpeUtil.ahead(a, 2.6, 0);
                FpeUtil.fx(a, FpeFx.Kind.RING_SHOCK, new Vec3(p.x, a.groundY(p.x, p.z, a.getY()) + 0.1, p.z), 0, 10, 4.5f, a.dmg(0.4f));
                FpeUtil.hitRadius(a, p, 2.6, a.dmg(0.6f), 0.9, 0.4);
                FpeUtil.particles(a, ParticleTypes.SQUID_INK, p, 30, 1.4, 0.2, 1.4, 0.15);
                a.sound(SoundEvents.WARDEN_STEP, 3f, 0.5f);
                a.sound(SoundEvents.RAVAGER_STEP, 2f, 0.6f);
            }
        }));
        // forced by stanceTick(): shoves off the ground and rears up with a short roar that pushes enemies off her
        out.add(Ability.of("rise_up", 26, 0).when(e -> false).blind().tick((e, t, tk) -> {
            Alice a = (Alice) e;
            if (tk == 10) {
                a.switchStance(0);
                a.sound(SoundEvents.RAVAGER_ROAR, 2f, 0.6f);
                FpeUtil.hitRadius(a, a.position(), 3.8, a.dmg(0.4f), 1.6, 0.4);
                FpeUtil.particles(a, ParticleTypes.LARGE_SMOKE, a.position(), 20, 1.6, 0.2, 1.6, 0.05);
            }
        }));
        // lowers her head and gallops straight through everything, then tosses whatever is in front with a head-butt
        out.add(q2("quad_charge", 52, 90).range(6, 22).weight(3).closer().faceUntil(13).start((e, t, tk) -> { ((Alice) e).hitIds.clear(); ((Alice) e).flag = false; }).tick((e, t, tk) -> {
            Alice a = (Alice) e;
            if (tk == 3) a.sound(SoundEvents.RAVAGER_ROAR, 2.5f, 0.55f);
            if (tk == 6 || tk == 9) { FpeUtil.particles(a, ParticleTypes.CAMPFIRE_COSY_SMOKE, FpeUtil.ahead(a, 2.2, 0.1), 6, 0.5, 0.1, 0.5, 0.02); a.sound(SoundEvents.RAVAGER_STEP, 1.5f, 0.5f); }
            if (tk >= 13 && tk <= 33 && !a.flag) {
                Vec3 f = FpeUtil.forward(a);
                a.setDeltaMovement(f.x * 1.05, a.getDeltaMovement().y, f.z * 1.05);
                a.hasImpulse = true;
                FpeUtil.particles(a, ParticleTypes.SQUID_INK, a.position().add(0, 0.6, 0), 4, 1.2, 0.3, 1.2, 0.02);
                if (tk % 3 == 0) a.sound(SoundEvents.WARDEN_STEP, 2f, 0.7f);
                for (LivingEntity v : FpeUtil.enemiesInRadius(a, FpeUtil.ahead(a, 2.2, 0), 2.6, 3, 1)) {
                    if (a.hitIds.add(v.getId())) { FpeUtil.hit(a, v, a.dmg(1.1f), 1.8, 0.55); a.sound(SoundEvents.PLAYER_ATTACK_KNOCKBACK, 1.5f, 0.5f); }
                }
                if (a.horizontalCollision && tk > 15) { a.flag = true; a.sound(SoundEvents.GENERIC_EXPLODE, 1.5f, 0.7f); FpeUtil.particles(a, ParticleTypes.EXPLOSION, FpeUtil.ahead(a, 2.4, 1.5), 3, 0.6, 0.6, 0.6, 0); }
            }
            if (tk == 34) a.setDeltaMovement(a.getDeltaMovement().scale(0.2));
            if (tk == 37) {
                FpeUtil.hitCone(a, 4.8, 70, a.dmg(1.3f), 1.0, 1.0);
                a.arcFx(2.2, 4.5f, 120, -70, 0, 0xEE0A0A0E);
                a.sound(SoundEvents.WARDEN_ATTACK_IMPACT, 2f, 0.6f);
            }
        }));
        // butt-wiggle, then a huge leap onto the target: claws crash down, pinning shockwave + spike ring
        out.add(q2("quad_pounce", 46, 80).range(4, 15).weight(3).closer().faceUntil(13).start((e, t, tk) -> ((Alice) e).flag = false).tick((e, t, tk) -> {
            Alice a = (Alice) e;
            if (tk == 4) a.sound(SoundEvents.CAT_HISS, 2.5f, 0.4f);
            if (tk == 13) { a.dashToward(t.position(), Math.max(0.5, Math.min(1.5, a.distanceTo(t) / 8.0)), 0.5); a.sound(SoundEvents.RAVAGER_ATTACK, 2f, 0.6f); }
            if (!a.flag && tk >= 21 && (a.onGround() || tk == 27)) {
                a.flag = true;
                Vec3 p = FpeUtil.ahead(a, 2.0, 0);
                for (LivingEntity v : FpeUtil.enemiesInRadius(a, p, 3.4, 3, 1)) {
                    FpeUtil.hit(a, v, a.dmg(1.6f), 0.5, 0.2);
                    v.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 50, 3));
                }
                FpeUtil.fx(a, FpeFx.Kind.RING_SHOCK, a.position().add(0, 0.1, 0), 0, 12, 7f, a.dmg(0.5f));
                a.spikeRing(p, 3.0, 7, 3, 1.3f, 0);
                FpeUtil.particles(a, ParticleTypes.EXPLOSION, p, 3, 1.2, 0.2, 1.2, 0);
                a.sound(SoundEvents.GENERIC_EXPLODE, 2f, 0.6f);
            }
        }));
        // rears half up: right rake, left rake, then both claws hammer the floor
        out.add(q2("quad_rake", 40, 50).range(0, 6.5).weight(4).faceUntil(18).tick((e, t, tk) -> {
            Alice a = (Alice) e;
            if (tk == 4) a.sound(SoundEvents.WARDEN_ANGRY, 1.5f, 0.8f);
            if (tk == 12 || tk == 20) {
                FpeUtil.hitCone(a, 5.5, 80, a.dmg(1.05f), 0.5, 0.25);
                a.arcFx(1.8, 5.2f, 150, tk == 12 ? 50 : -50, 0, 0xEE0A0A0E);
                a.sound(SoundEvents.PLAYER_ATTACK_SWEEP, 2f, 0.5f);
            }
            if (tk == 28) {
                Vec3 p = FpeUtil.ahead(a, 3.2, 0);
                FpeUtil.hitRadius(a, p, 3.0, a.dmg(1.3f), 1.3, 0.5);
                FpeUtil.fx(a, FpeFx.Kind.RING_SHOCK, new Vec3(p.x, a.groundY(p.x, p.z, a.getY()) + 0.1, p.z), 0, 10, 5f, a.dmg(0.4f));
                FpeUtil.particles(a, ParticleTypes.SQUID_INK, p, 25, 1.2, 0.2, 1.2, 0.15);
                a.sound(SoundEvents.WARDEN_ATTACK_IMPACT, 2f, 0.5f);
            }
        }));
        // pivots on her front claws: the spiked tail and hindquarters mow a full circle
        out.add(q2("quad_tail_sweep", 40, 70).range(0, 7.5).weight(3).tick((e, t, tk) -> {
            Alice a = (Alice) e;
            if (tk == 6) a.sound(SoundEvents.WARDEN_ATTACK_IMPACT, 1.2f, 0.4f);
            if (tk == 16) {
                FpeUtil.hitRadius(a, a.position(), 7.2, a.dmg(1.2f), 2.4, 0.5);
                a.arcFx(0.7, 7.2f, 360, 0, 0, 0xEE08080B);
                FpeUtil.arc(a, ParticleTypes.SQUID_INK, a.position().add(0, 0.4, 0), 0, 180, 6.5, 44);
                a.sound(SoundEvents.PLAYER_ATTACK_SWEEP, 2f, 0.4f);
            }
        }));
        // rears, buries both claws in the floor: a fan of spikes and tentacles erupts toward the target, then a second burst under it
        out.add(q2("quad_eruption", 54, 120).range(3, 16).weight(3).blind().faceUntil(16).tick((e, t, tk) -> {
            Alice a = (Alice) e;
            if (tk == 6) a.sound(SoundEvents.WARDEN_ROAR, 2.5f, 1.0f);
            if (tk == 18) {
                Vec3 p0 = FpeUtil.ahead(a, 3, 0);
                FpeUtil.fx(a, FpeFx.Kind.RING_SHOCK, new Vec3(p0.x, a.groundY(p0.x, p0.z, a.getY()) + 0.1, p0.z), 0, 12, 6f, a.dmg(0.5f));
                FpeUtil.particles(a, ParticleTypes.SQUID_INK, p0, 50, 1.6, 0.3, 1.6, 0.25);
                a.sound(SoundEvents.GENERIC_EXPLODE, 2.5f, 0.5f);
                Vec3 d = a.flatDir(t), side = new Vec3(-d.z, 0, d.x);
                for (int r = 0; r < 9; r++) {
                    int w = 1 + r / 2;
                    for (int s = -w; s <= w; s++) {
                        Vec3 p = a.position().add(d.scale(3 + r * 1.5)).add(side.scale(s * 1.1 + (r % 2) * 0.5));
                        if ((r == 5 || r == 8) && s % 2 == 0) a.tentacle(p.x, p.z, a.getY(), 4 + r * 2, 50, 1.3f);
                        else a.spike(p.x, p.z, a.getY(), 2 + r * 2, 28, a.dmg(0.8f), 1.2f + r * 0.12f + a.random.nextFloat() * 0.3f);
                    }
                }
            }
            if (tk == 30) {
                Vec3 c = t.position();
                a.tentacle(c.x, c.z, c.y, 6, 60, 1.6f);
                for (int i = 0; i < 4; i++) { double ang = Math.PI * 0.5 * i + 0.4; a.spike(c.x + Math.cos(ang) * 2, c.z + Math.sin(ang) * 2, c.y, 8, 26, a.dmg(0.7f), 1.5f); }
                a.sound(SoundEvents.EVOKER_FANGS_ATTACK, 2f, 0.5f);
            }
            if (tk == 40) { FpeUtil.hitRadius(a, FpeUtil.ahead(a, 2.6, 0), 4.0, a.dmg(0.9f), 1.5, 0.6); a.sound(SoundEvents.ROOTED_DIRT_BREAK, 2f, 0.5f); }
        }));
        // snaps forward with the giant grin: withering bite, then shakes the victim and flings it
        out.add(q2("quad_bite", 32, 45).range(0, 5.5).weight(4).faceUntil(10).tick((e, t, tk) -> {
            Alice a = (Alice) e;
            if (tk == 3) a.sound(SoundEvents.WARDEN_SNIFF, 2f, 0.6f);
            if (tk == 9) a.dashForward(0.7, 0.05);
            if (tk == 11) {
                for (LivingEntity v : FpeUtil.enemiesInRadius(a, FpeUtil.ahead(a, 2.4, 2.4), 2.6, 3, 3)) {
                    FpeUtil.hit(a, v, a.dmg(1.6f), 0.2, 0.1);
                    v.addEffect(new MobEffectInstance(MobEffects.WITHER, 60, 1));
                }
                a.sound(SoundEvents.EVOKER_FANGS_ATTACK, 2f, 0.4f);
                a.sound(SoundEvents.PHANTOM_BITE, 2f, 0.5f);
            }
            if (tk == 18) {
                FpeUtil.hitCone(a, 4.4, 60, a.dmg(0.7f), 1.7, 0.6);
                FpeUtil.particles(a, ParticleTypes.SQUID_INK, FpeUtil.ahead(a, 2.6, 2.2), 20, 0.6, 0.6, 0.6, 0.2);
                a.sound(SoundEvents.PLAYER_ATTACK_KNOCKBACK, 2f, 0.5f);
            }
        }));
        // arches her back like a cat: three volleys of black spines shot from her shoulders
        out.add(q2("quad_spine_volley", 44, 90).range(5, 20).weight(2).faceUntil(30).tick((e, t, tk) -> {
            Alice a = (Alice) e;
            if (tk == 6) a.sound(SoundEvents.CAT_HISS, 2.5f, 0.5f);
            if (tk == 18 || tk == 24 || tk == 30) {
                Vec3 from = a.position().add(0, 3.6, 0).add(FpeUtil.forward(a).scale(0.6));
                Vec3 aim = FpeUtil.aim(from, t, 1.1, 0.4);
                for (int i = -2; i <= 2; i++) {
                    double ang = Math.toRadians(i * 13 + (tk == 24 ? 6 : 0)), c = Math.cos(ang), sn = Math.sin(ang);
                    Vec3 v = new Vec3(aim.x * c - aim.z * sn, aim.y + 0.05, aim.x * sn + aim.z * c);
                    FpeUtil.projectile(a, FpeProjectile.Kind.KNIFE, from.add(FpeUtil.right(a).scale(i * 0.5)), v, a.dmg(0.55f));
                }
                FpeUtil.particles(a, ParticleTypes.SQUID_INK, from, 20, 1.2, 0.3, 1.2, 0.2);
                a.sound(SoundEvents.TRIDENT_THROW, 1.6f, 0.5f);
                a.sound(SoundEvents.ARROW_SHOOT, 1.6f, 0.5f);
            }
        }));
        // ENRAGED: three bounding claw-slams that chase the target, then a rearing double-claw crater
        out.add(Ability.of("quad_stampede", 64, 200).when(e -> phase(e, 1) && e.getStance() == 1 && e.isEnraged()).range(3, 20).weight(5).closer().faceUntil(40).blind().tick((e, t, tk) -> {
            Alice a = (Alice) e;
            if (tk == 3) { a.sound(SoundEvents.WARDEN_ROAR, 3f, 0.6f); a.sound(SoundEvents.RAVAGER_ROAR, 2f, 0.5f); }
            if (tk == 10 || tk == 22 || tk == 34) a.dashToward(t.position(), Math.max(0.5, Math.min(1.2, a.distanceTo(t) / 6.0)), 0.25);
            if (tk == 16 || tk == 28 || tk == 40) {
                Vec3 p = FpeUtil.ahead(a, 2.2, 0);
                FpeUtil.hitRadius(a, p, 3.6, a.dmg(1.0f), 1.0, 0.45);
                FpeUtil.fx(a, FpeFx.Kind.RING_SHOCK, a.position().add(0, 0.1, 0), 0, 10, 5.5f, a.dmg(0.4f));
                Vec3 d = FpeUtil.forward(a);
                for (int i = 0; i < 3; i++) { Vec3 s = a.position().add(d.scale(3.5 + i * 1.4)); a.spike(s.x, s.z, a.getY(), 2 + i * 2, 24, a.dmg(0.7f), 1.3f + i * 0.2f); }
                a.sound(SoundEvents.WARDEN_STEP, 3f, 0.5f);
                a.sound(SoundEvents.GENERIC_EXPLODE, 1.2f, 0.8f);
            }
            if (tk == 52) {
                Vec3 p = FpeUtil.ahead(a, 3.5, 0);
                FpeUtil.hitRadius(a, p, 4.8, a.dmg(2.0f), 1.8, 0.7);
                FpeUtil.fx(a, FpeFx.Kind.RING_SHOCK, new Vec3(p.x, a.groundY(p.x, p.z, a.getY()) + 0.1, p.z), 0, 16, 11f, a.dmg(0.7f));
                a.spikeRing(p, 4.0, 12, 3, 1.8f, 0);
                FpeUtil.particles(a, ParticleTypes.EXPLOSION_EMITTER, p, 1, 0, 0, 0, 0);
                FpeUtil.particles(a, ParticleTypes.SQUID_INK, p, 60, 2.5, 0.4, 2.5, 0.3);
                a.sound(SoundEvents.GENERIC_EXPLODE, 3f, 0.45f);
            }
        }));
    }
}
