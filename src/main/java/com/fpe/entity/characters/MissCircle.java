package com.fpe.entity.characters;

import java.util.List;

import com.fpe.entity.Ability;
import com.fpe.entity.FpeEntity;
import com.fpe.entity.FpeFx;
import com.fpe.entity.FpeProjectile;
import com.fpe.entity.FpeUtil;

import net.minecraft.core.BlockPos;
import net.minecraft.core.particles.BlockParticleOption;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.Vec3;

/**
 * Miss Circle (pyromaniac AU). Giant drawing compass + thigh-holstered flamethrower.
 * Abilities: sweep, lunge, splitSlam, compassThrow, drawCircle, flame, fireball, charge, hairWhip, combo (rage), inferno (rage).
 */
public class MissCircle extends FpeEntity {
    /** direction locked at the start of directional moves (slam crack lines) */
    private Vec3 lockDir = new Vec3(0, 0, 1);
    private Vec3 lockPos = Vec3.ZERO;

    public MissCircle(EntityType<? extends FpeEntity> type, Level level) { super(type, level); }

    public static AttributeSupplier.Builder attributes() { return baseAttributes(90, 7, 0.3, 5, 0.4); }

    @Override public double preferredDistance() { return 2.5; }
    @Override protected SoundEvent getAmbientSound() { return SoundEvents.WITCH_AMBIENT; }
    @Override protected SoundEvent getHurtSound(DamageSource s) { return SoundEvents.WITCH_HURT; }
    @Override protected SoundEvent getDeathSound() { return SoundEvents.WITCH_DEATH; }
    @Override public float getVoicePitch() { return 0.8f; }

    // ------------------------------------------------------------------ helpers
    private static Vec3 rotY(Vec3 f, double deg) {
        double r = Math.toRadians(deg), c = Math.cos(r), s = Math.sin(r);
        return new Vec3(f.x * c - f.z * s, 0, f.x * s + f.z * c);
    }

    /** direction "deg" degrees toward her right of her facing (matches positive model yaw) */
    private static Vec3 dirRight(FpeEntity e, double deg) {
        double r = Math.toRadians(deg);
        return FpeUtil.forward(e).scale(Math.cos(r)).add(FpeUtil.right(e).scale(Math.sin(r)));
    }

    /** fire cone: damage + ignite everything within range/halfAngle of dir */
    private static void fireCone(FpeEntity e, Vec3 origin, Vec3 dir, double range, double halfAngle, float dmg, int fireSecs) {
        AABB box = new AABB(origin, origin).inflate(range + 1, 2, range + 1);
        for (LivingEntity v : e.level().getEntitiesOfClass(LivingEntity.class, box, x -> FpeUtil.canHurt(e, x))) {
            Vec3 d = new Vec3(v.getX() - origin.x, 0, v.getZ() - origin.z);
            double len = d.length();
            if (len - v.getBbWidth() * 0.5 > range) continue;
            if (len > 0.3 && Math.toDegrees(Math.acos(Math.max(-1, Math.min(1, d.normalize().dot(dir))))) > halfAngle) continue;
            v.invulnerableTime = Math.min(v.invulnerableTime, 10);
            if (FpeUtil.hit(e, v, dmg, 0.15, 0.05)) v.setSecondsOnFire(fireSecs);
        }
    }

    private static void sprayParticles(FpeEntity e, Vec3 origin, Vec3 dir, double range) {
        for (int i = 0; i < 7; i++) {
            double d = 0.6 + e.getRandom().nextDouble() * range;
            Vec3 at = origin.add(dir.scale(d));
            double s = 0.1 + d * 0.12;
            FpeUtil.particles(e, ParticleTypes.FLAME, at, 2, s, s * 0.6, s, 0.02);
        }
        FpeUtil.particles(e, ParticleTypes.LARGE_SMOKE, origin.add(dir.scale(range * 0.9)), 1, 0.4, 0.3, 0.4, 0.01);
    }

    private static void debris(FpeEntity e, Vec3 at) {
        BlockState st = e.level().getBlockState(BlockPos.containing(at.x, at.y - 0.5, at.z));
        if (!st.isAir()) FpeUtil.particles(e, new BlockParticleOption(ParticleTypes.BLOCK, st), at.add(0, 0.2, 0), 14, 0.35, 0.15, 0.35, 0.15);
    }

    private static Vec3 muzzle(FpeEntity e) { return e.position().add(0, 1.35, 0).add(FpeUtil.forward(e).scale(1.1)).add(FpeUtil.right(e).scale(-0.35)); }

    // ------------------------------------------------------------------ abilities
    @Override
    protected void registerAbilities(List<Ability> out) {
        // 1. 360° compass sweep
        out.add(Ability.of("sweep", 34, 70).range(0, 4.5).weight(4)
                .tick((e, t, k) -> {
                    if (k == 2) FpeUtil.sound(e, SoundEvents.ARMOR_EQUIP_IRON, 1f, 0.6f);
                    if (k == 13) FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_SWEEP, 1.4f, 0.7f);
                    if (k == 14) FpeUtil.fx(e, FpeFx.Kind.ARC, e.position().add(0, 1.0, 0), 0, 9, 4.6f, 0).param(360).color(0xFFE6E8F4);
                    if (k == 15) {
                        FpeUtil.hitRadius(e, e.position(), 4.6, e.dmg(1.5f), 1.1, 0.35);
                        FpeUtil.arc(e, ParticleTypes.SWEEP_ATTACK, e.position().add(0, 1, 0), e.getYRot(), 180, 3.6, 10);
                    }
                }));

        // 2. long lunging stab
        out.add(Ability.of("lunge", 30, 60).range(2.5, 8).weight(3).faceUntil(9)
                .tick((e, t, k) -> {
                    if (k == 3) FpeUtil.sound(e, SoundEvents.ARMOR_EQUIP_CHAIN, 1f, 0.6f);
                    if (k == 10) { e.dashForward(1.45, 0.08); FpeUtil.sound(e, SoundEvents.TRIDENT_THROW, 1.2f, 0.8f); }
                    if (k >= 11 && k <= 14) {
                        Vec3 from = e.position().add(0, 1.2, 0), to = from.add(FpeUtil.forward(e).scale(4.2));
                        if (FpeUtil.hitLine(e, from, to, 0.6, e.dmg(1.8f), 1.2, 0.25) > 0) FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_CRIT, 1f, 0.8f);
                        FpeUtil.particles(e, ParticleTypes.CRIT, to, 4, 0.2, 0.2, 0.2, 0.1);
                    }
                }));

        // 3. hop + overhead split-legs slam: two diverging ground cracks
        out.add(Ability.of("splitSlam", 40, 110).range(0, 7).weight(3).faceUntil(17)
                .tick((e, t, k) -> {
                    if (k == 8) { e.dashForward(0.35, 0.5); FpeUtil.sound(e, SoundEvents.GOAT_LONG_JUMP, 1f, 0.7f); }
                    if (k == 17) { lockDir(e); }
                    if (k == 20) {
                        FpeUtil.hitCone(e, 3.6, 55, e.dmg(2.0f), 0.6, 0.8);
                        FpeUtil.sound(e, SoundEvents.GENERIC_EXPLODE, 1f, 0.7f);
                        FpeUtil.sound(e, SoundEvents.ANVIL_LAND, 0.8f, 0.5f);
                        debris(e, e.position().add(lockDir.scale(2)));
                    }
                    if (k > 20 && k <= 29) {
                        int i = k - 20;
                        for (int s = -1; s <= 1; s += 2) {
                            Vec3 at = lockPos.add(rotY(lockDir, s * 14).scale(1.6 + i * 1.05));
                            FpeUtil.hitRadius(e, at, 1.1, e.dmg(1.1f), 0.3, 0.7);
                            debris(e, at);
                            FpeUtil.particles(e, ParticleTypes.CRIT, at.add(0, 0.2, 0), 5, 0.3, 0.1, 0.3, 0.2);
                        }
                        if (i % 2 == 0) FpeUtil.sound(e, SoundEvents.STONE_BREAK, 1f, 0.6f);
                    }
                }));

        // 4. compass boomerang
        out.add(Ability.of("compassThrow", 40, 120).range(4, 16).weight(3)
                .tick((e, t, k) -> {
                    if (k == 13) {
                        Vec3 from = e.position().add(0, 1.4, 0).add(FpeUtil.right(e).scale(0.6));
                        FpeUtil.projectile(e, FpeProjectile.Kind.COMPASS, from, FpeUtil.aim(from, t, 1.05, 0.3), e.dmg(1.3f));
                        FpeUtil.sound(e, SoundEvents.TRIDENT_THROW, 1.2f, 0.6f);
                    }
                    if (k == 34) FpeUtil.sound(e, SoundEvents.ARMOR_EQUIP_IRON, 1f, 0.8f);
                }));

        // 5. draw a huge circle around herself while spinning -> it bursts
        out.add(Ability.of("drawCircle", 46, 160).range(0, 5).weight(2)
                .tick((e, t, k) -> {
                    if (k == 4) {
                        FpeUtil.fx(e, FpeFx.Kind.RING_TRAP, e.position(), 30, 40, 5.5f, e.dmg(2.0f));
                        if (e.isEnraged()) FpeUtil.fx(e, FpeFx.Kind.RING_TRAP, t.position(), 30, 40, 2.8f, e.dmg(1.4f));
                        lockPos = e.position();
                    }
                    if (k >= 6 && k <= 30) {
                        // the pencil leg traces the circle in sync with her spin (model yaw goes 0 -> -360)
                        double spin = -360.0 * (k - 6) / 24.0;
                        Vec3 d = dirRight(e, spin + 90);
                        FpeUtil.particles(e, ParticleTypes.FLAME, lockPos.add(d.scale(5.5)).add(0, 0.1, 0), 3, 0.15, 0.02, 0.15, 0.01);
                        FpeUtil.particles(e, ParticleTypes.ELECTRIC_SPARK, e.position().add(d.scale(1.8)).add(0, 0.1, 0), 2, 0.1, 0.05, 0.1, 0.05);
                        if (k % 4 == 0) FpeUtil.sound(e, SoundEvents.GRINDSTONE_USE, 0.5f, 1.4f);
                    }
                    if (k == 31) FpeUtil.sound(e, SoundEvents.WITCH_CELEBRATE, 1.2f, 0.8f);
                }));

        // 6. flamethrower stream (pyromaniac)
        out.add(Ability.of("flame", 52, 140).range(0, 6.5).weight(3)
                .tick((e, t, k) -> {
                    if (k == 6) FpeUtil.sound(e, SoundEvents.ARMOR_EQUIP_LEATHER, 1f, 0.8f);
                    if (k == 12) FpeUtil.sound(e, SoundEvents.FLINTANDSTEEL_USE, 1f, 0.8f);
                    if (k >= 14 && k <= 42) {
                        double sweep = Math.sin((k - 14) * 0.22) * 18;
                        Vec3 dir = dirRight(e, sweep);
                        Vec3 o = muzzle(e);
                        sprayParticles(e, o, dir, 6);
                        if (k % 3 == 0) fireCone(e, o.subtract(dir.scale(1.0)), dir, 6.5, 20, e.dmg(0.35f), 4);
                        if (k % 6 == 2) FpeUtil.sound(e, SoundEvents.BLAZE_SHOOT, 0.7f, 0.6f);
                    }
                }));

        // 7. fireball shot(s)
        out.add(Ability.of("fireball", 30, 80).range(5, 20).weight(3)
                .tick((e, t, k) -> {
                    if (k == 14 || (k == 20 && e.isEnraged())) {
                        Vec3 o = muzzle(e);
                        Vec3 v = FpeUtil.aim(o, t, 0.9, 0.5);
                        FpeUtil.projectile(e, FpeProjectile.Kind.FIREBALL, o, v, e.dmg(1.4f));
                        if (e.isEnraged()) for (int s = -1; s <= 1; s += 2) FpeUtil.projectile(e, FpeProjectile.Kind.FIREBALL, o, rotY(v, s * 14).add(0, v.y, 0), e.dmg(1.0f));
                        FpeUtil.sound(e, SoundEvents.GHAST_SHOOT, 1f, 0.9f);
                        FpeUtil.particles(e, ParticleTypes.FLAME, o, 12, 0.2, 0.2, 0.2, 0.08);
                    }
                }));

        // 8. sprinting chase with the compass scraping behind, rising slash
        out.add(Ability.of("charge", 34, 100).range(5, 18).weight(3)
                .tick((e, t, k) -> {
                    if (k == 4) FpeUtil.sound(e, SoundEvents.WITCH_CELEBRATE, 1f, 1.2f);
                    if (k >= 6 && k < 24) {
                        e.dashToward(t.position(), e.isEnraged() ? 0.72 : 0.62, e.getDeltaMovement().y);
                        Vec3 tip = e.position().add(FpeUtil.forward(e).scale(-1.4)).add(FpeUtil.right(e).scale(0.6));
                        FpeUtil.particles(e, ParticleTypes.ELECTRIC_SPARK, tip.add(0, 0.1, 0), 3, 0.1, 0.05, 0.1, 0.1);
                        if (k % 3 == 0) FpeUtil.sound(e, SoundEvents.GRINDSTONE_USE, 0.4f, 1.6f);
                        if (e.distanceTo(t) < 2.0) FpeUtil.hitCone(e, 2.0, 80, e.dmg(0.8f), 0.5, 0.2);
                    }
                    if (k == 24) e.setDeltaMovement(e.getDeltaMovement().scale(0.2));
                    if (k == 27) {
                        FpeUtil.hitCone(e, 3.4, 70, e.dmg(1.4f), 0.4, 0.95);
                        FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_SWEEP, 1.2f, 0.8f);
                        FpeUtil.fx(e, FpeFx.Kind.ARC, e.position().add(0, 1.1, 0), 0, 8, 3.2f, 0).param(150).color(0xFFE6E8F4).setXRot(80);
                    }
                }));

        // 9. hair whip
        out.add(Ability.of("hairWhip", 28, 70).range(0, 4).weight(3)
                .tick((e, t, k) -> {
                    if (k == 11) FpeUtil.sound(e, SoundEvents.PHANTOM_FLAP, 1.2f, 0.6f);
                    if (k == 13) {
                        if (FpeUtil.hitCone(e, 4.2, 110, e.dmg(1.0f), 1.5, 0.3) > 0)
                            for (LivingEntity v : FpeUtil.enemiesInRadius(e, e.position(), 4.4, 3, 1)) v.addEffect(new MobEffectInstance(MobEffects.BLINDNESS, 40, 0));
                        FpeUtil.arc(e, ParticleTypes.SQUID_INK, e.position().add(0, 1.2, 0), e.getYRot(), 80, 3.2, 14);
                    }
                }));

        // 10. enraged three-hit combo
        out.add(Ability.of("combo", 44, 90).range(0, 5).weight(4).when(FpeEntity::isEnraged)
                .tick((e, t, k) -> {
                    if (k == 6 || k == 15) e.dashForward(0.45, 0);
                    if (k == 22) e.dashForward(0.4, 0.45);
                    if (k == 8) {
                        FpeUtil.hitCone(e, 3.6, 80, e.dmg(1.1f), 0.5, 0.2);
                        FpeUtil.fx(e, FpeFx.Kind.ARC, e.position().add(0, 1.1, 0), 0, 7, 3.6f, 0).param(170).color(0xFFFFB050);
                        FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_SWEEP, 1f, 0.9f);
                    }
                    if (k == 17) {
                        FpeUtil.hitCone(e, 3.6, 80, e.dmg(1.1f), 0.5, 0.4);
                        FpeUtil.fx(e, FpeFx.Kind.ARC, e.position().add(0, 1.3, 0), 0, 7, 3.6f, 0).param(170).color(0xFFFFB050).setXRot(-35);
                        FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_SWEEP, 1f, 1.1f);
                    }
                    if (k == 30) {
                        FpeUtil.hitCone(e, 3.2, 60, e.dmg(1.6f), 0.7, 0.7);
                        FpeUtil.fx(e, FpeFx.Kind.RING_SHOCK, e.position().add(FpeUtil.forward(e).scale(2)), 0, 12, 4f, e.dmg(0.8f));
                        FpeUtil.sound(e, SoundEvents.GENERIC_EXPLODE, 0.9f, 0.8f);
                        debris(e, e.position().add(FpeUtil.forward(e).scale(2)));
                    }
                }));

        // 11. enraged inferno: two spinning fire spirals, then compass plant + fireball nova
        out.add(Ability.of("inferno", 64, 220).range(0, 9).weight(3).when(FpeEntity::isEnraged).faceUntil(10)
                .tick((e, t, k) -> {
                    if (k == 2) FpeUtil.sound(e, SoundEvents.WITCH_CELEBRATE, 1.4f, 0.6f);
                    if (k >= 10 && k <= 46) {
                        // gun points to her left (+x) and the model spins 0 -> -720 over ticks 10..46
                        double spin = -720.0 * (k - 10) / 36.0;
                        Vec3 dir = dirRight(e, spin - 90);
                        Vec3 o = e.position().add(0, 1.3, 0).add(dir.scale(0.9));
                        sprayParticles(e, o, dir, 6);
                        fireCone(e, o.subtract(dir), dir, 6.5, 18, e.dmg(0.4f), 5);
                        if (k % 5 == 0) FpeUtil.sound(e, SoundEvents.BLAZE_SHOOT, 0.8f, 0.5f);
                    }
                    if (k == 48) {
                        FpeUtil.fx(e, FpeFx.Kind.RING_SHOCK, e.position(), 0, 16, 7f, e.dmg(1.2f));
                        FpeUtil.hitRadius(e, e.position(), 2.5, e.dmg(1.5f), 1.0, 0.6);
                        for (int i = 0; i < 6; i++) {
                            Vec3 d = dirRight(e, i * 60);
                            FpeUtil.projectile(e, FpeProjectile.Kind.FIREBALL, e.position().add(0, 1.2, 0).add(d), d.scale(0.6).add(0, 0.05, 0), e.dmg(1.0f));
                        }
                        FpeUtil.sound(e, SoundEvents.GENERIC_EXPLODE, 1.3f, 0.6f);
                        FpeUtil.arc(e, ParticleTypes.FLAME, e.position().add(0, 0.2, 0), 0, 180, 3, 40);
                        debris(e, e.position().add(FpeUtil.forward(e).scale(1.5)));
                    }
                }));
    }

    private void lockDir(FpeEntity e) { lockDir = FpeUtil.forward(e); lockPos = e.position(); }
}
