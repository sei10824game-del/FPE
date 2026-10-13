package com.fpe.entity;

import java.util.HashSet;
import java.util.Set;
import java.util.UUID;

import javax.annotation.Nullable;

import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.network.protocol.Packet;
import net.minecraft.network.protocol.game.ClientGamePacketListener;
import net.minecraft.network.syncher.EntityDataAccessor;
import net.minecraft.network.syncher.EntityDataSerializers;
import net.minecraft.network.syncher.SynchedEntityData;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.Vec3;
import net.minecraftforge.network.NetworkHooks;

/**
 * Timed world effect: ground spikes, tentacles, drawn circles, shockwaves and slash-arc visuals.
 * Spawn with FpeUtil.fx(...). Visuals: client/render/FpeFxRenderer. Entity yaw = direction (for ARC).
 *
 *  SPIKE      black spike erupts after `warmup`, damages (radius ~1.2) once at eruption, then lingers until life.
 *  TENTACLE   warns, erupts, sways, re-hits every 20 ticks and slows victims (grab).
 *  RING_TRAP  compass-drawn circle on the ground: draws itself over warmup, at the end everything inside takes damage.
 *  RING_SHOCK flat shockwave expanding 0 -> radius over life, damages each entity crossing the band once.
 *  ARC        visual-only crescent slash (radius = outer radius, param = sweep degrees, color = ARGB, entity xRot = tilt).
 */
public class FpeFx extends Entity {
    public enum Kind { SPIKE, TENTACLE, RING_TRAP, RING_SHOCK, ARC }

    private static final EntityDataAccessor<Integer> KIND = SynchedEntityData.defineId(FpeFx.class, EntityDataSerializers.INT);
    private static final EntityDataAccessor<Integer> WARM = SynchedEntityData.defineId(FpeFx.class, EntityDataSerializers.INT);
    private static final EntityDataAccessor<Integer> LIFE = SynchedEntityData.defineId(FpeFx.class, EntityDataSerializers.INT);
    private static final EntityDataAccessor<Float> RADIUS = SynchedEntityData.defineId(FpeFx.class, EntityDataSerializers.FLOAT);
    private static final EntityDataAccessor<Float> PARAM = SynchedEntityData.defineId(FpeFx.class, EntityDataSerializers.FLOAT);
    private static final EntityDataAccessor<Integer> COLOR = SynchedEntityData.defineId(FpeFx.class, EntityDataSerializers.INT);

    @Nullable private UUID ownerId;
    private float damage;
    private final Set<UUID> hit = new HashSet<>();

    public FpeFx(EntityType<? extends FpeFx> type, Level level) { super(type, level); noPhysics = true; }

    public void setOwner(Entity o) { ownerId = o.getUUID(); }
    @Nullable public Entity getOwner() { return ownerId != null && level() instanceof ServerLevel s ? s.getEntity(ownerId) : null; }

    public void setup(Kind k, int warmup, int life, float radius, float damage) {
        entityData.set(KIND, k.ordinal()); entityData.set(WARM, warmup); entityData.set(LIFE, life); entityData.set(RADIUS, radius); this.damage = damage;
    }
    public FpeFx param(float p) { entityData.set(PARAM, p); return this; }
    public FpeFx color(int argb) { entityData.set(COLOR, argb); return this; }

    public Kind kind() { return Kind.values()[Math.floorMod(entityData.get(KIND), Kind.values().length)]; }
    public int warmup() { return entityData.get(WARM); }
    public int life() { return entityData.get(LIFE); }
    public float radius() { return entityData.get(RADIUS); }
    public float param() { return entityData.get(PARAM); }
    public int color() { return entityData.get(COLOR); }

    @Override
    protected void defineSynchedData() {
        entityData.define(KIND, 0); entityData.define(WARM, 10); entityData.define(LIFE, 40);
        entityData.define(RADIUS, 2f); entityData.define(PARAM, 0f); entityData.define(COLOR, 0xFFFFFFFF);
    }

    @Override
    public void tick() {
        super.tick();
        Kind k = kind();
        int t = tickCount, warm = warmup();
        if (level().isClientSide) { clientTick(k, t, warm); return; }
        ServerLevel s = (ServerLevel) level();
        if (t > life()) { discard(); return; }
        Entity o = getOwner();
        FpeEntity owner = o instanceof FpeEntity f ? f : null;
        switch (k) {
            case SPIKE -> {
                if (t == warm) {
                    s.sendParticles(ParticleTypes.LARGE_SMOKE, getX(), getY(), getZ(), 10, 0.4, 0.1, 0.4, 0.05);
                    s.playSound(null, getX(), getY(), getZ(), SoundEvents.EVOKER_FANGS_ATTACK, SoundSource.HOSTILE, 0.8f, 0.6f);
                    for (LivingEntity v : FpeUtil.enemiesInRadius(this, position(), 1.25, 3, 0.5)) strike(v, owner, 1.0, 0.55);
                }
            }
            case TENTACLE -> {
                if (t == warm) s.playSound(null, getX(), getY(), getZ(), SoundEvents.SLIME_SQUISH, SoundSource.HOSTILE, 1f, 0.5f);
                if (t >= warm && (t - warm) % 20 == 0) {
                    hit.clear();
                    for (LivingEntity v : FpeUtil.enemiesInRadius(this, position(), 1.6, 4, 0.5)) {
                        strike(v, owner, 0.8, 0.45);
                        v.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 50, 3));
                    }
                }
                if (t > warm && t % 3 == 0) s.sendParticles(ParticleTypes.SQUID_INK, getX(), getY() + 0.3, getZ(), 1, 0.3, 0.3, 0.3, 0.01);
            }
            case RING_TRAP -> {
                if (t == warm) {
                    s.playSound(null, getX(), getY(), getZ(), SoundEvents.GENERIC_EXPLODE, SoundSource.HOSTILE, 0.8f, 1.4f);
                    s.sendParticles(ParticleTypes.EXPLOSION, getX(), getY() + 0.3, getZ(), 6, radius() * 0.4, 0.1, radius() * 0.4, 0);
                    for (LivingEntity v : FpeUtil.enemiesInRadius(this, position(), radius(), 3, 0.5)) strike(v, owner, 1.1, 0.6);
                }
            }
            case RING_SHOCK -> {
                double cur = radius() * Math.min(1.0, t / (double) Math.max(1, life() - 4));
                for (LivingEntity v : FpeUtil.enemiesInRadius(this, position(), cur + 0.7, 1.6, 0.5)) {
                    double d = Math.sqrt((v.getX() - getX()) * (v.getX() - getX()) + (v.getZ() - getZ()) * (v.getZ() - getZ()));
                    if (d >= cur - 1.1 && !hit.contains(v.getUUID()) && v.getY() - getY() < 1.5) strike(v, owner, 1.0, 0.5);
                }
                if (t % 2 == 0) FpeUtil.arc(this, ParticleTypes.CLOUD, position().add(0, 0.1, 0), 0, 180, cur, (int) Math.min(40, 8 + cur * 6));
            }
            case ARC -> { }
        }
    }

    private void strike(LivingEntity v, @Nullable FpeEntity owner, double knock, double up) {
        if (hit.contains(v.getUUID())) return;
        hit.add(v.getUUID());
        Entity o = getOwner();
        if (v.hurt(damageSources().mobAttack(o instanceof LivingEntity l ? l : null), damage)) {
            FpeUtil.knock(v, position(), knock, up);
        }
    }

    private void clientTick(Kind k, int t, int warm) {
        switch (k) {
            case SPIKE -> {
                if (t < warm && t % 2 == 0) level().addParticle(ParticleTypes.SMOKE, getX() + (random.nextDouble() - 0.5), getY() + 0.05, getZ() + (random.nextDouble() - 0.5), 0, 0.02, 0);
                if (t == warm) for (int i = 0; i < 12; i++) level().addParticle(ParticleTypes.LARGE_SMOKE, getX(), getY() + 0.2, getZ(), (random.nextDouble() - 0.5) * 0.3, 0.2 + random.nextDouble() * 0.2, (random.nextDouble() - 0.5) * 0.3);
            }
            case TENTACLE -> {
                if (t < warm && t % 2 == 0) level().addParticle(ParticleTypes.SQUID_INK, getX() + (random.nextDouble() - 0.5), getY() + 0.05, getZ() + (random.nextDouble() - 0.5), 0, 0.02, 0);
            }
            default -> {}
        }
    }

    @Override public boolean isPickable() { return false; }
    @Override public boolean shouldRenderAtSqrDistance(double d) { return d < 160 * 160; }

    @Override
    protected void readAdditionalSaveData(CompoundTag t) { discard(); /* transient */ }
    @Override
    protected void addAdditionalSaveData(CompoundTag t) { }

    @Override
    public Packet<ClientGamePacketListener> getAddEntityPacket() { return NetworkHooks.getEntitySpawningPacket(this); }
}
