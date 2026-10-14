package com.fpe.entity.characters;

import java.util.List;
import java.util.UUID;

import org.joml.Vector3f;

import com.fpe.entity.Ability;
import com.fpe.entity.FpeEntity;
import com.fpe.entity.FpeFx;
import com.fpe.entity.FpeProjectile;
import com.fpe.entity.FpeUtil;

import net.minecraft.core.BlockPos;
import net.minecraft.core.particles.BlockParticleOption;
import net.minecraft.core.particles.DustParticleOptions;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.ai.attributes.AttributeInstance;
import net.minecraft.world.entity.ai.attributes.AttributeModifier;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.Vec3;

/**
 * Red Circle (DANGER AU): relentless twin-blade (giant pencil + compass leg) berserker.
 * Abilities: xSlash, flurry, tornado, pencilVolley, bladeWave, bloodRing, leapSlam, rush, twinThrow,
 * frenzy (rage), execution (rage), roar (forced once at 50% hp: rage mode = faster, shorter rests).
 */
public class RedCircle extends FpeEntity {
    private static final UUID RAGE_SPEED = UUID.fromString("6f0f2b1e-3c0d-4d7e-9a51-6c2b7d1e0a11");
    private static final DustParticleOptions BLOOD = new DustParticleOptions(new Vector3f(0.75f, 0.03f, 0.08f), 1.6f);
    private static final int ARC_RED = 0xFFD0101E;

    private boolean roared;
    private Vec3 mark = Vec3.ZERO;

    public RedCircle(EntityType<? extends FpeEntity> type, Level level) { super(type, level); }

    public static AttributeSupplier.Builder attributes() { return baseAttributes(80, 7, 0.34, 4, 0.3); }

    @Override public double preferredDistance() { return 1.5; }
    @Override protected int restTicks() { return isEnraged() ? 3 : 10; }
    @Override protected SoundEvent getAmbientSound() { return SoundEvents.VINDICATOR_CELEBRATE; }
    @Override protected SoundEvent getHurtSound(DamageSource s) { return SoundEvents.VINDICATOR_HURT; }
    @Override protected SoundEvent getDeathSound() { return SoundEvents.VINDICATOR_DEATH; }
    @Override public float getVoicePitch() { return 1.25f; }

    @Override
    public void aiStep() {
        super.aiStep();
        if (level().isClientSide) return;
        AttributeInstance sp = getAttribute(Attributes.MOVEMENT_SPEED);
        boolean rage = isEnraged() && isAlive();
        if (sp != null && rage != (sp.getModifier(RAGE_SPEED) != null)) {
            if (rage) sp.addTransientModifier(new AttributeModifier(RAGE_SPEED, "red circle rage", 0.4, AttributeModifier.Operation.MULTIPLY_TOTAL));
            else sp.removeModifier(RAGE_SPEED);
        }
        if (rage && !roared && !isBusy() && getTarget() != null) { roared = true; forceAbility("roar"); }
        if (rage && tickCount % 4 == 0) FpeUtil.particles(this, BLOOD, position().add(0, 1.8, 0), 1, 0.3, 0.3, 0.3, 0);
    }

    // ------------------------------------------------------------------ helpers
    /** rapid multi-hit: clears the victim's i-frames so fast combos actually land each hit */
    private static int rapidCone(FpeEntity e, double range, double half, float dmg, double knock, double up) {
        Vec3 f = FpeUtil.forward(e);
        int n = 0;
        for (LivingEntity v : e.level().getEntitiesOfClass(LivingEntity.class, e.getBoundingBox().inflate(range, 1.5, range), x -> FpeUtil.canHurt(e, x))) {
            Vec3 d = new Vec3(v.getX() - e.getX(), 0, v.getZ() - e.getZ());
            if (d.length() - v.getBbWidth() * 0.5 - e.getBbWidth() * 0.5 > range) continue;
            if (d.lengthSqr() > 0.01 && Math.toDegrees(Math.acos(Math.max(-1, Math.min(1, d.normalize().dot(f))))) > half) continue;
            v.invulnerableTime = 0;
            if (FpeUtil.hit(e, v, dmg, knock, up)) { n++; FpeUtil.particles(e, BLOOD, v.position().add(0, v.getBbHeight() * 0.6, 0), 6, 0.2, 0.2, 0.2, 0); }
        }
        return n;
    }

    private static int rapidLine(FpeEntity e, Vec3 from, Vec3 to, double r, float dmg) {
        int n = 0;
        for (LivingEntity v : e.level().getEntitiesOfClass(LivingEntity.class, new AABB(from, to).inflate(r + 1), x -> FpeUtil.canHurt(e, x))) {
            AABB bb = v.getBoundingBox().inflate(r);
            if (bb.clip(from, to).isPresent() || bb.contains(from)) {
                v.invulnerableTime = 0;
                if (FpeUtil.hit(e, v, dmg, 0.15, 0.05)) { n++; FpeUtil.particles(e, BLOOD, v.position().add(0, v.getBbHeight() * 0.6, 0), 4, 0.2, 0.2, 0.2, 0); }
            }
        }
        return n;
    }

    private static void arc(FpeEntity e, double y, float radius, float sweep, float tilt) {
        FpeUtil.fx(e, FpeFx.Kind.ARC, e.position().add(0, y, 0), 0, 7, radius, 0).param(sweep).color(ARC_RED).setXRot(tilt);
    }

    private static void debris(FpeEntity e, Vec3 at) {
        BlockState st = e.level().getBlockState(BlockPos.containing(at.x, at.y - 0.5, at.z));
        if (!st.isAir()) FpeUtil.particles(e, new BlockParticleOption(ParticleTypes.BLOCK, st), at.add(0, 0.2, 0), 16, 0.4, 0.15, 0.4, 0.15);
    }

    private static void bloodRing(FpeEntity e, Vec3 c, double r) {
        FpeUtil.arc(e, BLOOD, c.add(0, 0.15, 0), 0, 180, r, (int) Math.min(48, 10 + r * 6));
    }

    // ------------------------------------------------------------------ abilities
    @Override
    protected void registerAbilities(List<Ability> out) {
        // 1. X cross slash
        out.add(Ability.of("xSlash", 24, 45).range(0, 4).weight(4)
                .tick((e, t, k) -> {
                    if (k == 3) FpeUtil.sound(e, SoundEvents.ARMOR_EQUIP_IRON, 1f, 1.2f);
                    if (k == 9) e.dashForward(0.45, 0);
                    if (k == 11) {
                        rapidCone(e, 3.8, 75, e.dmg(1.6f), 0.8, 0.3);
                        arc(e, 1.2, 3.6f, 160, 40);
                        arc(e, 1.2, 3.6f, 160, -40);
                        FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_SWEEP, 1.2f, 1.2f);
                        FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_CRIT, 1f, 0.8f);
                    }
                }));

        // 2. twin-rod flurry of thrusts (every 3 ticks, alternating hands)
        out.add(Ability.of("flurry", 36, 70).range(0, 4.5).weight(3)
                .tick((e, t, k) -> {
                    if (k >= 7 && k <= 28 && (k - 7) % 3 == 0) {
                        Vec3 from = e.position().add(0, 1.25, 0).add(FpeUtil.right(e).scale(((k - 7) / 3) % 2 == 0 ? 0.35 : -0.35));
                        Vec3 to = from.add(FpeUtil.forward(e).scale(3.6));
                        rapidLine(e, from, to, 0.55, e.dmg(0.32f));
                        FpeUtil.particles(e, ParticleTypes.CRIT, to, 3, 0.15, 0.15, 0.15, 0.1);
                        FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_STRONG, 0.7f, 1.4f + e.getRandom().nextFloat() * 0.3f);
                        if ((k - 7) % 6 == 0) e.dashForward(0.22, 0);
                    }
                }));

        // 3. blade tornado: spins toward the target
        out.add(Ability.of("tornado", 48, 120).range(0, 9).weight(3)
                .tick((e, t, k) -> {
                    if (k > 8 && k < 40) {
                        e.dashToward(t.position(), e.isEnraged() ? 0.36 : 0.3, e.getDeltaMovement().y);
                        if (k % 4 == 0) {
                            for (LivingEntity v : FpeUtil.enemiesInRadius(e, e.position(), 2.6, 2.5, 1)) {
                                v.invulnerableTime = 0;
                                FpeUtil.hit(e, v, e.dmg(0.35f), 0.5, 0.2);
                            }
                            FpeUtil.arc(e, ParticleTypes.SWEEP_ATTACK, e.position().add(0, 1.1, 0), (k * 45) % 360, 180, 2.0, 6);
                            FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_SWEEP, 0.8f, 1.3f);
                        }
                        if (k % 2 == 0) bloodRing(e, e.position(), 2.2);
                    }
                    if (k == 40) e.setDeltaMovement(e.getDeltaMovement().scale(0.2));
                }));

        // 4. pencil volley (fan)
        out.add(Ability.of("pencilVolley", 30, 70).range(4, 18).weight(3)
                .tick((e, t, k) -> {
                    if (k == 12 || (k == 21 && e.isEnraged())) {
                        int n = e.isEnraged() ? 7 : 5;
                        Vec3 from = e.position().add(0, 1.4, 0);
                        Vec3 aim = FpeUtil.aim(from, t, 1.35, 0.35);
                        for (int i = 0; i < n; i++) {
                            double ang = Math.toRadians(-32 + 64.0 * i / (n - 1) + (k == 21 ? 5 : 0));
                            double c = Math.cos(ang), s = Math.sin(ang);
                            Vec3 v = new Vec3(aim.x * c - aim.z * s, aim.y, aim.x * s + aim.z * c);
                            FpeUtil.projectile(e, FpeProjectile.Kind.PENCIL, from.add(v.normalize().scale(0.6)), v, e.dmg(0.7f));
                        }
                        FpeUtil.sound(e, SoundEvents.ARROW_SHOOT, 1.2f, 0.7f);
                        FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_SWEEP, 0.8f, 1.5f);
                    }
                }));

        // 5. blade waves
        out.add(Ability.of("bladeWave", 30, 80).range(4, 16).weight(3)
                .tick((e, t, k) -> {
                    if (k == 11 || k == 17) {
                        Vec3 from = e.position().add(0, 1.0, 0).add(FpeUtil.forward(e).scale(0.8));
                        FpeUtil.projectile(e, FpeProjectile.Kind.BLADE_WAVE, from, FpeUtil.aim(from, t, 1.2, 0.2), e.dmg(1.2f));
                        arc(e, 1.1, 2.6f, 140, k == 11 ? 70 : 0);
                        FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_SWEEP, 1.2f, 0.8f);
                    }
                }));

        // 6. plunge twin blades -> blood-red expanding shockwave
        out.add(Ability.of("bloodRing", 38, 130).range(0, 7).weight(3)
                .tick((e, t, k) -> {
                    if (k == 6) e.setDeltaMovement(0, 0.45, 0);
                    if (k == 16 || (k == 25 && e.isEnraged())) {
                        FpeUtil.fx(e, FpeFx.Kind.RING_SHOCK, e.position(), 0, 18, 8f, e.dmg(1.4f));
                        FpeUtil.hitRadius(e, e.position(), 2.0, e.dmg(1.2f), 0.8, 0.5);
                        FpeUtil.sound(e, SoundEvents.GENERIC_EXPLODE, 1f, 0.6f);
                        FpeUtil.sound(e, SoundEvents.TRIDENT_HIT_GROUND, 1.2f, 0.6f);
                        debris(e, e.position().add(FpeUtil.forward(e).scale(1.2)));
                    }
                    if (k > 16 && k < 34) bloodRing(e, e.position(), 8.0 * Math.min(1, (k - 16) / 14.0));
                }));

        // 7. leaping front-flip slam
        out.add(Ability.of("leapSlam", 38, 100).range(4, 13).weight(3).faceUntil(8)
                .tick((e, t, k) -> {
                    if (k == 8) {
                        double d = e.distanceTo(t);
                        e.dashToward(t.position(), Math.min(1.3, d / 11.0), 0.75);
                        FpeUtil.sound(e, SoundEvents.GOAT_LONG_JUMP, 1f, 1.1f);
                    }
                    if (k == 22) {
                        FpeUtil.hitRadius(e, e.position(), 3.2, e.dmg(1.8f), 0.9, 0.5);
                        FpeUtil.fx(e, FpeFx.Kind.RING_SHOCK, e.position(), 0, 10, 4f, e.dmg(0.8f));
                        FpeUtil.sound(e, SoundEvents.GENERIC_EXPLODE, 0.9f, 0.9f);
                        debris(e, e.position());
                        bloodRing(e, e.position(), 1.5);
                    }
                }));

        // 8. rush-down: dash-slash, dash-slash, rising X
        out.add(Ability.of("rush", 42, 90).range(3, 10).weight(4)
                .tick((e, t, k) -> {
                    if (k == 4 || k == 14) { e.dashToward(t.position(), 1.05, 0.05); FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_NODAMAGE, 1f, 0.6f); }
                    if (k == 24) e.dashToward(t.position(), 0.7, 0.05);
                    if (k == 8 || k == 18) {
                        rapidCone(e, 3.0, 80, e.dmg(1.0f), 0.4, 0.15);
                        arc(e, 1.1, 3f, 150, k == 8 ? 15 : -15);
                        FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_SWEEP, 1f, 1.2f);
                    }
                    if (k == 28) {
                        rapidCone(e, 3.2, 90, e.dmg(1.4f), 0.5, 0.95);
                        arc(e, 1.3, 3.2f, 140, 75);
                        arc(e, 1.3, 3.2f, 140, -75);
                        FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_CRIT, 1.2f, 0.8f);
                    }
                }));

        // 9. dual boomerang throw
        out.add(Ability.of("twinThrow", 44, 120).range(5, 16).weight(2)
                .tick((e, t, k) -> {
                    if (k == 14) {
                        Vec3 from = e.position().add(0, 1.7, 0);
                        Vec3 aim = FpeUtil.aim(from, t, 1.1, 0.3);
                        for (int s = -1; s <= 1; s += 2) {
                            double a = Math.toRadians(18 * s), c = Math.cos(a), sn = Math.sin(a);
                            Vec3 v = new Vec3(aim.x * c - aim.z * sn, aim.y, aim.x * sn + aim.z * c);
                            FpeUtil.projectile(e, FpeProjectile.Kind.COMPASS, from.add(FpeUtil.right(e).scale(-0.5 * s)), v, e.dmg(1.2f));
                        }
                        FpeUtil.sound(e, SoundEvents.TRIDENT_THROW, 1.2f, 1.0f);
                    }
                    if (k == 37) FpeUtil.sound(e, SoundEvents.ARMOR_EQUIP_IRON, 1f, 1.2f);
                }));

        // 10. enraged frenzy: 6 alternating slashes + X finisher
        out.add(Ability.of("frenzy", 52, 90).range(0, 5).weight(5).when(FpeEntity::isEnraged)
                .tick((e, t, k) -> {
                    if (k >= 5 && k < 35 && (k - 5) % 5 == 0) e.dashForward(0.32, 0);
                    if (k >= 7 && k < 37 && (k - 7) % 5 == 0) {
                        boolean even = ((k - 7) / 5) % 2 == 0;
                        rapidCone(e, 3.2, 85, e.dmg(0.6f), 0.25, 0.1);
                        arc(e, 1.1, 3f, 160, even ? 25 : -25);
                        FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_SWEEP, 0.9f, 1.1f + e.getRandom().nextFloat() * 0.4f);
                    }
                    if (k == 42) {
                        rapidCone(e, 3.6, 80, e.dmg(1.5f), 1.0, 0.4);
                        arc(e, 1.2, 3.6f, 160, 40);
                        arc(e, 1.2, 3.6f, 160, -40);
                        FpeUtil.fx(e, FpeFx.Kind.RING_SHOCK, e.position(), 0, 10, 3.5f, e.dmg(0.6f));
                        FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_CRIT, 1.3f, 0.7f);
                    }
                }));

        // 11. enraged execution: mark a circle under the target, spinning leap into it, plunge
        out.add(Ability.of("execution", 46, 200).range(3, 12).weight(3).when(FpeEntity::isEnraged).faceUntil(16)
                .tick((e, t, k) -> {
                    if (k == 4) {
                        mark = t.position();
                        FpeUtil.fx(e, FpeFx.Kind.RING_TRAP, mark, 28, 34, 3.2f, e.dmg(1.6f));
                        FpeUtil.sound(e, SoundEvents.VINDICATOR_CELEBRATE, 1.3f, 0.8f);
                    }
                    if (k > 4 && k < 32 && k % 2 == 0) bloodRing(e, mark, 3.2);
                    if (k == 17) {
                        double d = Math.sqrt(e.distanceToSqr(mark));
                        e.dashToward(mark, Math.min(1.4, d / 10.0), 0.8);
                        FpeUtil.sound(e, SoundEvents.GOAT_LONG_JUMP, 1f, 0.9f);
                    }
                    if (k == 32) {
                        FpeUtil.hitRadius(e, e.position(), 2.5, e.dmg(1.5f), 1.0, 0.6);
                        FpeUtil.fx(e, FpeFx.Kind.RING_SHOCK, e.position(), 0, 14, 5f, e.dmg(0.8f));
                        FpeUtil.sound(e, SoundEvents.GENERIC_EXPLODE, 1.1f, 0.7f);
                        debris(e, e.position());
                    }
                }));

        // 12. rage roar (forced once when dropping below 50%)
        out.add(Ability.of("roar", 30, 9999).range(0, 64).blind().when(e -> false)
                .tick((e, t, k) -> {
                    if (k == 9) {
                        FpeUtil.sound(e, SoundEvents.RAVAGER_ROAR, 1.3f, 1.3f);
                        FpeUtil.fx(e, FpeFx.Kind.RING_SHOCK, e.position(), 0, 12, 4.5f, e.dmg(0.5f));
                    }
                    if (k > 9 && k < 24) {
                        bloodRing(e, e.position(), (k - 9) * 0.35);
                        FpeUtil.particles(e, ParticleTypes.ANGRY_VILLAGER, e.position().add(0, 2.3, 0), 1, 0.3, 0.1, 0.3, 0);
                    }
                }));
    }
}
