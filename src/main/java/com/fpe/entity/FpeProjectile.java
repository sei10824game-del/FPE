package com.fpe.entity;

import java.util.HashSet;
import java.util.Set;
import java.util.UUID;

import javax.annotation.Nullable;

import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.network.syncher.EntityDataAccessor;
import net.minecraft.network.syncher.EntityDataSerializers;
import net.minecraft.network.syncher.SynchedEntityData;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.projectile.Projectile;
import net.minecraft.world.entity.projectile.ProjectileUtil;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.BlockHitResult;
import net.minecraft.world.phys.EntityHitResult;
import net.minecraft.world.phys.HitResult;
import net.minecraft.world.phys.Vec3;

/**
 * Generic FPE projectile. Behaviour is driven by {@link Kind}. Spawn with FpeUtil.projectile(...).
 * Models are defined in client/spec/ProjectileSpecs (one ModelSpec per Kind).
 */
public class FpeProjectile extends Projectile {
    public enum Kind {
        //          gravity drag  pierce boomerang explodeR fuse life spin(deg/tick) homing
        COMPASS     (0.00f, 1.00f, true,  true,  0f,   0,  60, 40f, 0f),   // spinning compass boomerang, returns to owner
        PENCIL      (0.02f, 0.99f, false, false, 0f,   0,  50, 0f,  0f),   // thrown pencil dart
        GRENADE     (0.06f, 0.98f, false, false, 3.2f, 45, 80, 25f, 0f),   // bouncing, explodes on fuse end
        BOMBLET     (0.06f, 0.98f, false, false, 1.8f, 30, 60, 30f, 0f),   // small cluster grenade
        ROCKET      (0.00f, 1.00f, false, false, 3.0f, 0,  60, 0f,  0f),   // explodes on impact
        BULLET      (0.00f, 1.00f, false, false, 0f,   0,  30, 0f,  0f),   // fast tracer
        SHADOW_ORB  (0.00f, 1.00f, false, false, 1.6f, 0, 120, 8f,  0.12f),// slow homing dark orb
        DIAMOND     (0.00f, 1.00f, false, false, 0f,   0,  50, 20f, 0f),   // white diamond shard
        AXE         (0.04f, 0.99f, false, true,  0f,   0,  50, 45f, 0f),   // spinning tool (boomerang)
        KNIFE       (0.03f, 0.99f, false, false, 0f,   0,  50, 0f,  0f),
        ABC_BLOCK   (0.05f, 0.99f, false, false, 1.4f, 0,  70, 15f, 0f),   // bouncy letter block, small blast
        BLADE_WAVE  (0.00f, 1.00f, true,  false, 0f,   0,  25, 0f,  0f),   // flat crescent slash wave (pierces)
        FIREBALL    (0.00f, 1.00f, false, false, 1.5f, 0,  60, 0f,  0f);   // pyromaniac fireball

        public final float gravity, drag, explodeRadius, spin, homing;
        public final boolean pierce, boomerang;
        public final int fuse, life;
        Kind(float g, float d, boolean pierce, boolean boom, float exp, int fuse, int life, float spin, float homing) {
            gravity = g; drag = d; this.pierce = pierce; boomerang = boom; explodeRadius = exp; this.fuse = fuse; this.life = life; this.spin = spin; this.homing = homing;
        }
    }

    private static final EntityDataAccessor<Integer> KIND = SynchedEntityData.defineId(FpeProjectile.class, EntityDataSerializers.INT);

    private float damage = 4f;
    private int age;
    private boolean returning;
    private final Set<UUID> hitSet = new HashSet<>();
    private int rehit;
    @Nullable private LivingEntity homingTarget;

    public FpeProjectile(EntityType<? extends FpeProjectile> type, Level level) { super(type, level); }

    public Kind kind() { return Kind.values()[Math.floorMod(entityData.get(KIND), Kind.values().length)]; }
    public void setKind(Kind k) { entityData.set(KIND, k.ordinal()); }
    public void setDamage(float d) { damage = d; }
    public int ageTicks() { return age; }

    @Override
    protected void defineSynchedData() { entityData.define(KIND, 0); }

    @Override
    protected boolean canHitEntity(Entity e) {
        if (!(e instanceof LivingEntity l) || !l.isAlive() || e.isSpectator() || (getOwner() != null && FpeUtil.isAlly(getOwner(), e))) return false;
        if (hitSet.contains(e.getUUID())) return false;
        return !(e instanceof net.minecraft.world.entity.player.Player p && p.isCreative());
    }

    @Override
    public void tick() {
        super.tick();
        Kind k = kind();
        age++;
        Entity owner = getOwner();
        Vec3 v = getDeltaMovement();

        if (level().isClientSide) { clientTrail(k); }

        // ---- boomerang return
        if (k.boomerang && !returning && age > k.life / 2) { returning = true; hitSet.clear(); }
        if (k.boomerang && returning) {
            if (owner == null || !owner.isAlive()) { discard(); return; }
            Vec3 to = owner.position().add(0, owner.getBbHeight() * 0.6, 0).subtract(position());
            if (to.length() < 1.6) { discard(); return; }
            v = v.scale(0.85).add(to.normalize().scale(0.35 * Math.max(0.6, v.length() / 0.8)));
            if (v.length() > 1.6) v = v.normalize().scale(1.6);
        }
        // ---- homing
        if (k.homing > 0 && !level().isClientSide) {
            if (homingTarget == null || !homingTarget.isAlive()) {
                homingTarget = level().getNearestEntity(LivingEntity.class, net.minecraft.world.entity.ai.targeting.TargetingConditions.forCombat().range(24).selector(x -> FpeUtil.canHurt(this, x)), null, getX(), getY(), getZ(), getBoundingBox().inflate(24));
            }
            if (homingTarget != null) {
                Vec3 to = homingTarget.position().add(0, homingTarget.getBbHeight() * 0.6, 0).subtract(position()).normalize();
                double sp = v.length();
                v = v.normalize().scale(1 - k.homing).add(to.scale(k.homing)).normalize().scale(sp);
            }
        }
        v = v.scale(k.drag).add(0, -k.gravity, 0);
        setDeltaMovement(v);

        if (!level().isClientSide) {
            // ---- fuse
            if (k.fuse > 0 && age >= k.fuse) { detonate(null); return; }
            if (age > k.life) { if (k.explodeRadius > 0 && k.fuse == 0 && k != Kind.ROCKET) detonate(null); discard(); return; }
            if (k.boomerang && --rehit <= 0) { rehit = 6; hitSet.clear(); }
        }

        HitResult hit = ProjectileUtil.getHitResultOnMoveVector(this, this::canHitEntity);
        if (hit.getType() == HitResult.Type.ENTITY) onHitEntity((EntityHitResult) hit);
        else if (hit.getType() == HitResult.Type.BLOCK) onHitBlock((BlockHitResult) hit);

        Vec3 d = getDeltaMovement();
        setPos(getX() + d.x, getY() + d.y, getZ() + d.z);
        if (k.spin == 0f && d.lengthSqr() > 1.0E-5) {
            double h = Math.sqrt(d.x * d.x + d.z * d.z);
            setYRot((float) Math.toDegrees(Math.atan2(-d.x, d.z)));
            setXRot((float) Math.toDegrees(Math.atan2(-d.y, h)));
            yRotO = getYRot(); xRotO = getXRot();
        }
    }

    @Override
    protected void onHitEntity(EntityHitResult r) {
        if (level().isClientSide) return;
        Kind k = kind();
        Entity e = r.getEntity();
        if (!(e instanceof LivingEntity l)) return;
        Entity o = getOwner();
        if (k.explodeRadius > 0 && !k.pierce) { detonate(l); return; }
        if (l.hurt(damageSources().thrown(this, o == null ? this : o), damage)) {
            if (o != null) FpeUtil.knock(l, position().subtract(getDeltaMovement()), 0.5, 0.15);
        }
        hitSet.add(e.getUUID());
        if (!k.pierce && !k.boomerang) discard();
    }

    @Override
    protected void onHitBlock(BlockHitResult r) {
        Kind k = kind();
        if (level().isClientSide) return;
        if (k == Kind.GRENADE || k == Kind.BOMBLET || k == Kind.ABC_BLOCK && age < 30) { // bounce
            Vec3 v = getDeltaMovement();
            Vec3 n = Vec3.atLowerCornerOf(r.getDirection().getNormal());
            Vec3 refl = v.subtract(n.scale(2 * v.dot(n))).scale(0.55);
            setDeltaMovement(refl);
            setPos(r.getLocation().add(n.scale(0.1)));
            playSound(SoundEvents.STONE_HIT, 0.5f, 1.4f);
            return;
        }
        if (k.explodeRadius > 0) { detonate(null); return; }
        if (k.boomerang) { returning = true; return; }
        if (k == Kind.BULLET) ((ServerLevel) level()).sendParticles(ParticleTypes.CRIT, getX(), getY(), getZ(), 3, 0.05, 0.05, 0.05, 0.1);
        discard();
    }

    private void detonate(@Nullable LivingEntity direct) {
        Kind k = kind();
        if (!(level() instanceof ServerLevel s)) { discard(); return; }
        Entity o = getOwner();
        float r = k.explodeRadius;
        s.sendParticles(r >= 2.5f ? ParticleTypes.EXPLOSION_EMITTER : ParticleTypes.EXPLOSION, getX(), getY(), getZ(), 1, 0, 0, 0, 0);
        s.sendParticles(ParticleTypes.LARGE_SMOKE, getX(), getY(), getZ(), 12, r * 0.25, r * 0.25, r * 0.25, 0.02);
        if (k == Kind.FIREBALL) s.sendParticles(ParticleTypes.FLAME, getX(), getY(), getZ(), 25, r * 0.3, r * 0.3, r * 0.3, 0.05);
        s.playSound(null, getX(), getY(), getZ(), SoundEvents.GENERIC_EXPLODE, net.minecraft.sounds.SoundSource.HOSTILE, Math.min(1.5f, r * 0.5f), 1.1f);
        for (LivingEntity v : FpeUtil.enemiesInRadius(this, position(), r, r, r)) {
            double f = 1.0 - Math.min(1.0, v.position().add(0, v.getBbHeight() / 2, 0).distanceTo(position()) / (r + 0.01)) * 0.6;
            if (v.hurt(damageSources().explosion(this, o == null ? this : o), (float) (damage * f))) {
                FpeUtil.knock(v, position(), 1.1 * f, 0.4);
                if (k == Kind.FIREBALL) v.setSecondsOnFire(5);
            }
        }
        discard();
    }

    private void clientTrail(Kind k) {
        switch (k) {
            case GRENADE, BOMBLET -> { if (age % 2 == 0) level().addParticle(ParticleTypes.SMOKE, getX(), getY() + 0.2, getZ(), 0, 0.02, 0); }
            case ROCKET -> level().addParticle(ParticleTypes.FLAME, getX(), getY(), getZ(), 0, 0, 0);
            case FIREBALL -> { level().addParticle(ParticleTypes.FLAME, getX(), getY(), getZ(), 0, 0.01, 0); level().addParticle(ParticleTypes.SMOKE, getX(), getY(), getZ(), 0, 0.02, 0); }
            case SHADOW_ORB -> { level().addParticle(ParticleTypes.SQUID_INK, getX(), getY(), getZ(), 0, 0, 0); level().addParticle(ParticleTypes.SMOKE, getX(), getY(), getZ(), 0, 0, 0); }
            case BULLET -> level().addParticle(ParticleTypes.CRIT, getX(), getY(), getZ(), 0, 0, 0);
            case BLADE_WAVE -> level().addParticle(ParticleTypes.SWEEP_ATTACK, getX(), getY(), getZ(), 0, 0, 0);
            case DIAMOND -> level().addParticle(ParticleTypes.END_ROD, getX(), getY(), getZ(), 0, 0, 0);
            default -> {}
        }
    }

    @Override public boolean isNoGravity() { return true; }
    @Override public boolean shouldRenderAtSqrDistance(double d) { return d < 128 * 128; }

    @Override
    protected void addAdditionalSaveData(CompoundTag t) { super.addAdditionalSaveData(t); t.putInt("Kind", entityData.get(KIND)); t.putFloat("Damage", damage); }
    @Override
    protected void readAdditionalSaveData(CompoundTag t) { super.readAdditionalSaveData(t); entityData.set(KIND, t.getInt("Kind")); damage = t.getFloat("Damage"); }
}
