package com.fpe.entity.characters;

import java.util.ArrayList;
import java.util.List;

import javax.annotation.Nullable;

import com.fpe.entity.Ability;
import com.fpe.entity.FpeCombat;
import com.fpe.entity.FpeEntity;
import com.fpe.entity.FpeFx;
import com.fpe.entity.FpeProjectile;
import com.fpe.entity.FpeUtil;

import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.BossEvent;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.EntityDimensions;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.Pose;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.level.ClipContext;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.Vec3;

/** Six individually registered characters sharing the same animation contact timeline. */
public final class PaperblightHost extends FpeEntity {
    public enum Role { LANA, EDWARD, OLIVER, THAVEL, CLAIRE, ZIP }

    private final Role role;
    @Nullable private LivingEntity held;
    private Vec3 grabOrigin = Vec3.ZERO;
    private Vec3 beamDirection = Vec3.ZERO;
    private float beamYaw, beamPitch;

    public PaperblightHost(EntityType<? extends FpeEntity> type, Level level, Role role) {
        super(type, level);
        this.role = role;
    }

    public Role role() { return role; }

    public static AttributeSupplier.Builder attributes(Role role) {
        return switch (role) {
            case LANA -> baseAttributes(140, 7, 0.31, 2, 0.2);
            case EDWARD -> baseAttributes(160, 7.5, 0.32, 3, 0.2);
            case OLIVER -> baseAttributes(180, 8, 0.33, 3, 0.25);
            case THAVEL -> baseAttributes(280, 10, 0.30, 5, 0.45);
            case CLAIRE -> baseAttributes(420, 18, 0.34, 6, 0.5);
            case ZIP -> baseAttributes(180, 8, 0.35, 3, 0.2);
        };
    }

    @Override public Faction faction() { return role == Role.CLAIRE ? Faction.PAPERBLIGHT_CLAIRE : Faction.PAPERBLIGHT; }
    @Override protected boolean hasBossBar() { return role == Role.CLAIRE; }
    @Override protected BossEvent.BossBarColor bossColor() { return BossEvent.BossBarColor.WHITE; }
    @Override public double preferredDistance() { return role == Role.THAVEL ? 2.6 : 1.9; }
    @Override public boolean meleeFocus() { return role != Role.CLAIRE; }

    @Override protected float getStandingEyeHeight(Pose pose, EntityDimensions dimensions) {
        return dimensions.height * 0.87f;
    }

    @Override public AABB getBoundingBoxForCulling() {
        // Include Zip's full wing span and the long arms/claws throughout their swings.
        return super.getBoundingBoxForCulling().inflate(role == Role.ZIP ? 3.0 : 2.6, 1.6, role == Role.ZIP ? 3.0 : 2.6);
    }

    @Override protected void onAbilityStart(Ability ability, LivingEntity target) {
        releaseGrab();
        beamDirection = Vec3.ZERO;
    }

    @Override public void cancelAbility() {
        releaseGrab();
        beamDirection = Vec3.ZERO;
        super.cancelAbility();
    }

    @Override public void tick() {
        super.tick();
        if (!level().isClientSide && held != null
                && (!isAlive() || !"grasp".equals(currentAbilityId()) || !validVictim(held))) releaseGrab();
    }

    @Override protected void registerAbilities(List<Ability> out) {
        out.add(Ability.of("sweep", 34, 48).range(0, reach(3.5)).weight(4).faceUntil(10).tick((e, target, tick) -> {
            if (tick == 14) sweep(2.8, 88, 1.05f, 0.55, 0.12, 10);
        }));
        out.add(Ability.of("double_cut", 40, 68).range(0, reach(3.6)).weight(4).faceUntil(9).tick((e, target, tick) -> {
            if (tick == 12) sweep(2.8, 65, 0.7f, 0.12, 0.08, -24);
            if (tick == 26) sweep(3.0, 80, 1.0f, 0.6, 0.12, 24);
        }));
        out.add(Ability.of("lunge", 36, 72).range(2, 9).weight(3).closer().faceUntil(10).tick((e, target, tick) -> {
            if (tick == 10) dashForward(dashSpeed(target, 1.05), 0.1);
            if (tick == 16) strikeLine(reach(3.9), 0.55, 1.25f, 0.75, 0.12, false);
        }));
        out.add(Ability.of("grasp", 42, 125).range(1, reach(5.6)).weight(3).faceUntil(10)
                .end((e, target, tick) -> releaseGrab()).tick((e, target, tick) -> grasp(target, tick)));
        out.add(Ability.of("slam", 40, 92).range(0, reach(4.0)).weight(3).faceUntil(15).tick((e, target, tick) -> {
            if (tick == 20) burst(reach(3.0), 1.5f, role == Role.THAVEL ? 1.25 : 0.85, 0.35);
        }));
        out.add(Ability.of("uppercut", 32, 60).range(0, reach(3.1)).weight(3).faceUntil(10).tick((e, target, tick) -> {
            if (tick == 14) sweep(2.5, 52, 1.15f, 0.45, role == Role.ZIP ? 0.72 : 0.55, -72);
        }));
        out.add(Ability.of("backhand", 30, 51).range(0, reach(3.3)).weight(3).faceUntil(8).tick((e, target, tick) -> {
            if (tick == 12) sweep(2.7, 105, 0.95f, role == Role.THAVEL ? 1.4 : 1.0, 0.16, 22);
        }));
        out.add(Ability.of("leap_strike", 44, 100).range(3, 11).weight(3).closer().faceUntil(12).tick((e, target, tick) -> {
            if (tick == 12) dashForward(dashSpeed(target, role == Role.ZIP ? 1.4 : 1.1), role == Role.ZIP ? 0.6 : 0.42);
            if (tick == 24) {
                sweep(3.1, 85, 1.45f, 0.9, 0.2, -36);
                FpeUtil.particles(this, ParticleTypes.CLOUD, position().add(0, 0.15, 0), 18, 0.8, 0.12, 0.8, 0.03);
            }
        }));
        out.add(Ability.of("shard_fan", 36, 96).range(4, 16).weight(2).faceUntil(16).tick((e, target, tick) -> {
            if (tick == 16 || tick == 22) shardFan(target);
        }));
        out.add(Ability.of("eye_ray", 52, 155).range(2, role == Role.CLAIRE ? 18 : 8).weight(2).faceUntil(24)
                .tick((e, target, tick) -> eyeRay(tick)));
        out.add(Ability.of("guard_pulse", 44, 110).range(0, reach(4)).weight(2).faceUntil(18).tick((e, target, tick) -> {
            if (tick == 22) {
                burst(reach(3.2), 0.65f, 1.45, 0.15);
                for (LivingEntity victim : FpeUtil.enemiesInRadius(this, position(), reach(3.2), 2, 0.7)) {
                    if (hasLineOfSight(victim)) victim.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 45, 1), this);
                }
            }
        }));
        out.add(Ability.of("frenzy", 60, 155).range(0, reach(4.3)).weight(4).faceUntil(9).when(FpeEntity::isEnraged)
                .tick((e, target, tick) -> {
                    if (tick == 12) sweep(3.0, 90, 0.85f, 0.15, 0.12, -26);
                    if (tick == 28) sweep(3.3, 100, 1.0f, 0.2, 0.15, 26);
                    if (tick == 44) burst(reach(3.5), 1.35f, 1.1, 0.3);
                }));
    }

    private double reach(double base) {
        return base + switch (role) {
            case LANA -> 0.2;
            case EDWARD -> 0.45;
            case OLIVER -> 0.7;
            case THAVEL -> 1.0;
            case CLAIRE -> 0.65;
            case ZIP -> 0.8;
        };
    }

    private double dashSpeed(LivingEntity target, double cap) {
        return Math.min(cap, Math.max(0.35, distanceTo(target) * 0.16));
    }

    private boolean validVictim(@Nullable LivingEntity victim) {
        return victim != null && victim.level() == level() && FpeUtil.canHurt(this, victim);
    }

    /** Claire's lethal contact is a recipient-specific rule, never an attack attribute. */
    private boolean strike(LivingEntity victim, float multiplier, double knock, double up, boolean resetIframes) {
        if (!validVictim(victim)) return false;
        boolean lethal = role == Role.CLAIRE && victim instanceof PaperblightHost host
                && (host.role == Role.LANA || host.role == Role.EDWARD || host.role == Role.OLIVER);
        if (resetIframes || lethal) victim.invulnerableTime = 0;
        if (!FpeUtil.hit(this, victim, lethal ? 20000f : dmg(multiplier), knock, up)) return false;
        if (victim.isAlive()) {
            switch (role) {
                case LANA -> victim.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 32, 0), this);
                case EDWARD -> victim.addEffect(new MobEffectInstance(MobEffects.WEAKNESS, 40, 0), this);
                case OLIVER -> FpeCombat.bleed(this, victim, 35);
                case THAVEL -> victim.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 28, 1), this);
                case CLAIRE -> victim.addEffect(new MobEffectInstance(MobEffects.WITHER, 40, 0), this);
                case ZIP -> FpeCombat.bleed(this, victim, 24);
            }
        }
        return true;
    }

    private int slashColor() { return role == Role.CLAIRE ? 0xFFE9C8FF : role == Role.EDWARD ? 0xFFE7EEE9 : 0xFFEDE7DB; }

    private void sweep(double baseRange, float angle, float damage, double knock, double up, float tilt) {
        double range = reach(baseRange);
        for (LivingEntity victim : FpeCombat.cone(this, range, angle)) {
            if (hasLineOfSight(victim)) strike(victim, damage, knock, up, false);
        }
        FpeCombat.slashArc(this, (float) range, angle * 2, tilt, 0, getBbHeight() * 0.5, slashColor());
        FpeUtil.sound(this, SoundEvents.PLAYER_ATTACK_SWEEP, 0.9f, role == Role.THAVEL ? 0.6f : 0.9f);
    }

    private Vec3 clippedEnd(Vec3 from, Vec3 direction, double length) {
        return level().clip(new ClipContext(from, from.add(direction.scale(length)), ClipContext.Block.COLLIDER,
                ClipContext.Fluid.NONE, this)).getLocation();
    }

    private List<LivingEntity> strikeSegment(Vec3 from, Vec3 to, double radius, float damage, double knock, double up, boolean resetIframes) {
        List<LivingEntity> hits = new ArrayList<>();
        for (LivingEntity victim : level().getEntitiesOfClass(LivingEntity.class, new AABB(from, to).inflate(radius + 1), this::validVictim)) {
            AABB box = victim.getBoundingBox().inflate(radius);
            if ((box.contains(from) || box.clip(from, to).isPresent()) && hasLineOfSight(victim)
                    && strike(victim, damage, knock, up, resetIframes)) hits.add(victim);
        }
        return hits;
    }

    private List<LivingEntity> strikeLine(double range, double radius, float damage, double knock, double up, boolean resetIframes) {
        Vec3 from = position().add(0, getBbHeight() * 0.6, 0);
        Vec3 end = clippedEnd(from, Vec3.directionFromRotation(getXRot(), getYRot()), range);
        FpeUtil.particles(this, ParticleTypes.SQUID_INK, from.lerp(end, 0.65), 9, 0.25, 0.25, 0.25, 0.02);
        return strikeSegment(from, end, radius, damage, knock, up, resetIframes);
    }

    private void grasp(LivingEntity target, int tick) {
        if (tick == 12 && strikeLine(reach(4.8), 0.5, 0.4f, 0, 0, false).contains(target) && validVictim(target)) {
            held = target;
            grabOrigin = target.position();
            FpeUtil.sound(this, SoundEvents.SLIME_ATTACK, 0.9f, 0.65f);
        }
        if (held != target || !validVictim(target)) { releaseGrab(); return; }
        if (tick >= 13 && tick <= 23) {
            double separation = (getBbWidth() + target.getBbWidth()) * 0.5 + 0.45;
            double p = (tick - 12) / 11.0;
            Vec3 next = grabOrigin.lerp(FpeUtil.ahead(this, separation, 0.08), p * p * (3 - 2 * p));
            AABB path = target.getBoundingBox().expandTowards(next.subtract(target.position()));
            if (level().getWorldBorder().isWithinBounds(path) && level().noCollision(target, path) && hasLineOfSight(target)) {
                FpeUtil.holdAt(target, next);
            } else releaseGrab();
        }
        if (tick == 26) {
            if (distanceTo(target) <= reach(3.0) && hasLineOfSight(target)) strike(target, 1.5f, 1.05, 0.25, false);
            releaseGrab();
        }
    }

    private void releaseGrab() { held = null; grabOrigin = Vec3.ZERO; }

    private void burst(double radius, float damage, double knock, double up) {
        FpeUtil.arc(this, ParticleTypes.CLOUD, position().add(0, 0.15, 0), getYRot(), 180, radius, 32);
        FpeUtil.particles(this, ParticleTypes.SQUID_INK, position().add(0, 0.3, 0), 18, 0.7, 0.2, 0.7, 0.03);
        FpeUtil.sound(this, SoundEvents.GENERIC_EXPLODE, 0.85f, role == Role.THAVEL ? 0.55f : 0.9f);
        for (LivingEntity victim : FpeUtil.enemiesInRadius(this, position(), radius, 1.6, 0.8)) {
            if (hasLineOfSight(victim)) strike(victim, damage, knock, up, false);
        }
    }

    private void shardFan(LivingEntity target) {
        Vec3 from = FpeUtil.ahead(this, 0.45, getBbHeight() * 0.68);
        Vec3 velocity = FpeUtil.aim(from, target, role == Role.EDWARD ? 1.5 : 1.25, 0.15);
        int spread = role == Role.ZIP ? 12 : 9;
        for (int side = -1; side <= 1; side++) {
            FpeUtil.projectile(this, FpeProjectile.Kind.KNIFE, from, FpeCombat.rotY(velocity, side * spread), dmg(0.45f));
        }
        FpeUtil.sound(this, SoundEvents.ARROW_SHOOT, 0.7f, 1.3f);
    }

    private void eyeRay(int tick) {
        if (tick < 24 && tick % 4 == 0) {
            FpeUtil.particles(this, role == Role.CLAIRE ? ParticleTypes.END_ROD : ParticleTypes.SQUID_INK,
                    getEyePosition(), 5, 0.12, 0.12, 0.12, 0.008);
        }
        if (role != Role.CLAIRE) {
            // Hosts glare through puppet faces; only Claire has a literal laser.
            if (tick == 24) {
                FpeUtil.sound(this, SoundEvents.AMETHYST_BLOCK_CHIME, 1.0f, 0.65f);
                FpeUtil.particles(this, ParticleTypes.END_ROD, getEyePosition(), 20, 0.32, 0.22, 0.32, 0.035);
                for (LivingEntity victim : FpeCombat.cone(this, reach(6.0), role == Role.THAVEL ? 75 : 55)) {
                    if (hasLineOfSight(victim) && strike(victim, 0.65f, 0.15, 0.05, false)) {
                        victim.addEffect(new MobEffectInstance(MobEffects.BLINDNESS, 45, 0), this);
                    }
                }
            }
            return;
        }
        if (tick != 24 && tick != 28 && tick != 32) return;
        if (tick == 24) {
            beamYaw = getYRot(); beamPitch = getXRot();
            beamDirection = Vec3.directionFromRotation(beamPitch, beamYaw);
            FpeUtil.sound(this, SoundEvents.BEACON_ACTIVATE, 1.2f, 1.35f);
        }
        if (beamDirection.lengthSqr() < 0.5) return;
        Vec3 from = getEyePosition();
        Vec3 end = clippedEnd(from, beamDirection, 18);
        FpeUtil.fx(this, FpeFx.Kind.BEAM, from, 0, 4, 0.15f, 0, beam -> {
            beam.param((float) from.distanceTo(end)).color(0xFFE9C8FF);
            beam.setYRot(beamYaw); beam.setXRot(beamPitch);
        });
        // These intentional pulses bypass ordinary hit cooldown only after segment intersection.
        strikeSegment(from, end, 0.15, 0.9f, 0.2, 0.05, true);
    }
}
