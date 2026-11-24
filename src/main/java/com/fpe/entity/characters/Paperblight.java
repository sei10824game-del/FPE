package com.fpe.entity.characters;

import java.util.List;

import javax.annotation.Nullable;

import com.fpe.entity.Ability;
import com.fpe.entity.FpeCombat;
import com.fpe.entity.FpeEntity;
import com.fpe.entity.FpeProjectile;
import com.fpe.entity.FpeUtil;

import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.tags.DamageTypeTags;
import net.minecraft.util.Mth;
import net.minecraft.world.BossEvent;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.EntityDimensions;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.Pose;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.level.ClipContext;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.Vec3;

public final class Paperblight extends FpeEntity {
    private static final String TRANSFORM_SECOND = "transform_second";
    private static final String TRANSFORM_THIRD = "transform_third";
    private static final int SECOND_FLIP = 30;
    private static final int THIRD_FLIP = 35;
    private static final float SECOND_THRESHOLD = 0.70f;
    private static final float THIRD_THRESHOLD = 0.35f;
    private static final int ECHO_LIFETIME = 240;

    private float damageFloor;
    private long echoExpiresAt;
    private long nextEchoAt;
    @Nullable private LivingEntity held;
    private Vec3 grabOrigin = Vec3.ZERO;

    public Paperblight(EntityType<? extends FpeEntity> type, Level level) {
        super(type, level);
    }

    public static AttributeSupplier.Builder attributes() {
        return baseAttributes(540, 9, 0.29, 5, 0.45);
    }

    @Override public Faction faction() { return Faction.PAPERBLIGHT; }
    @Override protected boolean hasBossBar() { return !isEcho(); }
    @Override protected BossEvent.BossBarColor bossColor() { return BossEvent.BossBarColor.PURPLE; }

    @Override
    public AABB getBoundingBoxForCulling() {
        return getBoundingBox().inflate(5 + getVariant(), 2, 5 + getVariant());
    }

    @Override
    public void setVariant(int variant) { super.setVariant(Mth.clamp(variant, 0, 2)); }

    @Override
    public EntityDimensions getDimensions(Pose pose) {
        return switch (getVariant()) {
            case 1 -> EntityDimensions.scalable(1.35f, 3.6f);
            case 2 -> EntityDimensions.scalable(2.2f, 4.8f);
            default -> super.getDimensions(pose);
        };
    }

    @Override
    protected float getStandingEyeHeight(Pose pose, EntityDimensions dimensions) {
        return dimensions.height * 0.87f;
    }

    @Override public double preferredDistance() { return 2.3 + getVariant() * 0.6; }

    @Override
    public boolean isEnraged() {
        if (isEcho()) return super.isEnraged();
        float rageThreshold = switch (getVariant()) {
            case 0 -> (1f + SECOND_THRESHOLD) / 2f;
            case 1 -> (SECOND_THRESHOLD + THIRD_THRESHOLD) / 2f;
            default -> THIRD_THRESHOLD / 2f;
        };
        return getHealth() < getMaxHealth() * rageThreshold;
    }

    private float phaseHealthFloor() {
        if (isEcho()) return 0;
        return switch (getVariant()) {
            case 0 -> getMaxHealth() * SECOND_THRESHOLD;
            case 1 -> getMaxHealth() * THIRD_THRESHOLD;
            default -> 0;
        };
    }

    private static boolean isTransform(String id) {
        return TRANSFORM_SECOND.equals(id) || TRANSFORM_THIRD.equals(id);
    }

    private boolean isTransforming() {
        return isBusy() && isTransform(currentAbilityId());
    }

    @Override
    public boolean forceAbility(String id) {
        if (isEcho() && (isTransform(id) || "host_echo".equals(id))) return false;
        return super.forceAbility(id);
    }

    @Override
    public boolean hurt(DamageSource source, float amount) {
        if (isTransforming() && !source.is(DamageTypeTags.BYPASSES_INVULNERABILITY)) return false;
        boolean hit = super.hurt(source, amount);
        if (hit && !level().isClientSide) startTransformIfReady();
        return hit;
    }

    @Override
    protected void actuallyHurt(DamageSource source, float amount) {
        // Clamp the health change after armor, resistance, and absorption have taken effect.
        float previousFloor = damageFloor;
        damageFloor = source.is(DamageTypeTags.BYPASSES_INVULNERABILITY) ? 0 : Math.min(getHealth(), phaseHealthFloor());
        try {
            super.actuallyHurt(source, amount);
        } finally {
            damageFloor = previousFloor;
        }
    }

    @Override
    public void setHealth(float health) {
        super.setHealth(Math.max(damageFloor, health));
    }

    private void startTransformIfReady() {
        float floor = phaseHealthFloor();
        if (floor <= 0 || getHealth() > floor || !isAlive() || isTransforming()) return;
        cancelAbility();
        forceAbility(getVariant() == 0 ? TRANSFORM_SECOND : TRANSFORM_THIRD);
        getNavigation().stop();
        FpeUtil.sound(this, SoundEvents.WARDEN_HEARTBEAT, 1.3f, 0.65f);
    }

    @Override
    public void tick() {
        if (!level().isClientSide) {
            if (isEcho() && level().getGameTime() >= echoExpiresAt) {
                discard();
                return;
            }
            startTransformIfReady();
        }
        super.tick();
        if (level().isClientSide) return;

        String ability = currentAbilityId();
        if (held != null && (!isAlive() || (!"grasp_pull".equals(ability) && !"assimilation_bite".equals(ability)))) releaseGrab();
        if (isAlive() && isTransform(ability)) tickTransform(ability);
    }

    private void tickTransform(String id) {
        setDeltaMovement(0, getDeltaMovement().y, 0);
        boolean second = TRANSFORM_SECOND.equals(id);
        int flip = second ? SECOND_FLIP : THIRD_FLIP;
        if (animTime == flip) {
            setVariant(Math.max(getVariant(), second ? 1 : 2));
            FpeUtil.particles(this, ParticleTypes.SQUID_INK, getBoundingBox().getCenter(), 34, 0.65, 0.85, 0.65, 0.06);
            FpeUtil.sound(this, SoundEvents.WARDEN_EMERGE, 1.4f, second ? 0.9f : 0.65f);
        } else if (animTime < flip && animTime % 5 == 0) {
            FpeUtil.particles(this, ParticleTypes.LARGE_SMOKE, getBoundingBox().getCenter(), 5, 0.55, 0.7, 0.55, 0.015);
        }
    }

    @Override
    protected void registerAbilities(List<Ability> out) {
        out.add(Ability.of(TRANSFORM_SECOND, 60, 0).when(e -> false).faceUntil(0));
        out.add(Ability.of(TRANSFORM_THIRD, 70, 0).when(e -> false).faceUntil(0));

        out.add(Ability.of("long_sweep", 36, 62).range(0, 5.3).weight(4).faceUntil(12).tick((e, target, tick) -> {
            if (tick == 16) sweep(4.0, 100, 1.25f, 0.9, 8, 0);
        }));

        out.add(Ability.of("double_rake", 42, 74).range(0, 4.8).weight(4).faceUntil(9).tick((e, target, tick) -> {
            if (tick == 12) sweep(3.4, 68, 0.75f, 0.1, -24, -22);
            if (tick == 26) sweep(3.7, 76, 1.05f, 0.65, 25, 18);
        }));

        out.add(Ability.of("elastic_thrust", 38, 80).range(2.5, 8.4).weight(3).closer().faceUntil(12).tick((e, target, tick) -> {
            if (tick == 12) dashForward(Math.min(0.95, distanceTo(target) * 0.13), 0.08);
            if (tick == 18) {
                strikeLine(target, reach(5.3), 0.5, 1.45f, 0.75);
                FpeUtil.sound(this, SoundEvents.PLAYER_ATTACK_KNOCKBACK, 1.1f, 0.74f);
            }
        }));

        out.add(Ability.of("grasp_pull", 48, 135).range(1.5, 7.6).weight(3).faceUntil(12)
                .start((e, target, tick) -> releaseGrab()).end((e, target, tick) -> releaseGrab())
                .tick((e, target, tick) -> graspPull(target, tick)));

        out.add(Ability.of("assimilation_bite", 54, 155).range(0, 4.0).weight(3).faceUntil(14)
                .start((e, target, tick) -> releaseGrab()).end((e, target, tick) -> releaseGrab())
                .tick((e, target, tick) -> assimilationBite(target, tick)));

        out.add(Ability.of("eye_flash", 42, 145).range(0, 8.5).weight(2).faceUntil(16).tick((e, target, tick) -> {
            if (tick == 20) eyeFlash();
        }));

        out.add(Ability.of("paper_shards", 38, 88).range(4.0, 17).weight(3).faceUntil(18).tick((e, target, tick) -> {
            if (tick == 18 || tick == 22 || tick == 26) paperShard(target, (tick - 22) / 4);
        }));

        out.add(Ability.of("stalking_step", 40, 88).range(4.0, 10).weight(3).faceUntil(8).tick((e, target, tick) -> {
            if (tick == 8) {
                FpeUtil.particles(this, ParticleTypes.SQUID_INK, position().add(0, 0.3, 0), 14, 0.4, 0.25, 0.4, 0.035);
                dashForward(Math.min(1.15, distanceTo(target) * 0.13), 0.17);
            }
            if (tick == 20) sweep(3.4, 70, 1.3f, 0.8, -16, 0);
        }));

        out.add(Ability.of("ground_slam", 46, 105).range(0, 5.8).weight(3).faceUntil(18).tick((e, target, tick) -> {
            if (tick == 24) groundBurst(FpeUtil.ahead(this, 0.75, 0), 3.9, 1.65f, 1.05, 0.42);
        }));

        out.add(Ability.of("wing_rush", 44, 90).range(2.0, 10).weight(3).faceUntil(12).tick((e, target, tick) -> {
            if (tick == 12) dashForward(Math.min(1.4, distanceTo(target) * 0.17), getVariant() == 2 ? 0.22 : 0.13);
            if (tick == 20) sweep(3.6, 90, 1.35f, 1.25, 12, 0);
        }));

        out.add(Ability.of("host_echo", 64, 275).range(1.5, 13).weight(2).faceUntil(24)
                .when(e -> canCreateEcho()).tick((e, target, tick) -> {
                    if (tick == 32) spawnEcho(target);
                }));

        out.add(Ability.of("frenzy", 66, 155).range(0, 5.8).weight(4).faceUntil(13).when(FpeEntity::isEnraged)
                .tick((e, target, tick) -> {
                    if (tick == 14) sweep(3.9, 100, 0.80f, 0.12, -28, -20);
                    if (tick == 30) sweep(4.1, 115, 0.95f, 0.2, 30, 18);
                    if (tick == 46) groundBurst(position(), 4.5, 1.35f, 1.2, 0.4);
                }));
    }

    private double reach(double base) {
        return base + getVariant() * 0.55;
    }

    private float strikeDamage(float multiplier) {
        return dmg(multiplier * (1f + getVariant() * 0.13f));
    }

    private void sweep(double range, float halfAngle, float damage, double knock, float tilt, float yaw) {
        double attackReach = reach(range);
        for (LivingEntity victim : FpeCombat.cone(this, attackReach, halfAngle)) {
            if (hasLineOfSight(victim)) FpeUtil.hit(this, victim, strikeDamage(damage), knock, 0.1);
        }
        FpeCombat.slashArc(this, (float) attackReach, halfAngle * 2, tilt, yaw, getBbHeight() * 0.46, FpeCombat.SLASH);
        FpeUtil.sound(this, SoundEvents.PLAYER_ATTACK_SWEEP, 1f, 0.85f - getVariant() * 0.12f);
    }

    private List<LivingEntity> strikeLine(LivingEntity target, double range, double radius, float damage, double knock) {
        Vec3 from = position().add(0, getBbHeight() * 0.4, 0);
        double rise = target.getY() + target.getBbHeight() * 0.55 - from.y;
        double horizontal = Math.max(1, target.position().subtract(position()).horizontalDistance());
        double endRise = Mth.clamp(rise / horizontal, -0.7, 0.7) * range;
        Vec3 end = from.add(FpeUtil.forward(this).scale(range)).add(0, endRise, 0);
        end = level().clip(new ClipContext(from, end, ClipContext.Block.COLLIDER, ClipContext.Fluid.NONE, this)).getLocation();
        FpeUtil.particles(this, ParticleTypes.SQUID_INK, from.lerp(end, 0.6), 9, 0.32, 0.2, 0.32, 0.025);
        return FpeUtil.hitLineVictims(this, from, end, radius, strikeDamage(damage), knock, 0.12);
    }

    private void graspPull(LivingEntity target, int tick) {
        if (tick == 14 && hasLineOfSight(target) && strikeLine(target, reach(6.6), 0.6, 0.45f, 0).contains(target)) {
            latch(target);
        }
        if (held != target) return;
        if (tick >= 15 && tick <= 27) reelIn(target, (tick - 14) / 13.0);
        if (tick == 30) {
            if (distanceTo(target) <= reach(3.5) && hasLineOfSight(target)) {
                FpeUtil.hit(this, target, strikeDamage(1.4f), 1.15, 0.25);
                FpeUtil.sound(this, SoundEvents.PLAYER_ATTACK_STRONG, 1.1f, 0.65f);
            }
            releaseGrab();
        }
    }

    private void assimilationBite(LivingEntity target, int tick) {
        if (tick == 16 && hasLineOfSight(target) && FpeCombat.cone(this, reach(2.35), 52).contains(target)
                && FpeUtil.hit(this, target, strikeDamage(0.5f), 0, 0)) {
            latch(target);
        }
        if (held != target) return;
        if (tick > 16 && tick < 30) reelIn(target, Math.min(1, (tick - 16) / 8.0));
        if (tick == 30) {
            if (distanceTo(target) <= reach(3.3) && hasLineOfSight(target)
                    && FpeUtil.hit(this, target, strikeDamage(1.6f), 0.85, 0.18)) {
                heal(isEcho() ? 2 : 3 + getVariant());
                FpeUtil.particles(this, ParticleTypes.SOUL, getBoundingBox().getCenter(), 12, 0.4, 0.55, 0.4, 0.04);
                FpeUtil.sound(this, SoundEvents.EVOKER_FANGS_ATTACK, 1.05f, 0.65f);
            }
            releaseGrab();
        }
    }

    private void latch(LivingEntity victim) {
        held = victim;
        grabOrigin = victim.position();
        FpeUtil.sound(this, SoundEvents.SLIME_ATTACK, 1f, 0.75f);
    }

    private void reelIn(LivingEntity victim, double progress) {
        double separation = (getBbWidth() + victim.getBbWidth()) * 0.5 + 0.35;
        Vec3 pin = FpeUtil.ahead(this, separation, 0.08);
        double eased = progress * progress * (3 - 2 * progress);
        Vec3 next = grabOrigin.lerp(pin, eased);
        AABB path = victim.getBoundingBox().expandTowards(next.subtract(victim.position()));
        if (level().getWorldBorder().isWithinBounds(path) && level().noCollision(victim, path)) {
            FpeUtil.holdAt(victim, next);
        } else {
            releaseGrab();
        }
    }

    private void releaseGrab() {
        held = null;
        grabOrigin = Vec3.ZERO;
    }

    @Override
    public void cancelAbility() {
        releaseGrab();
        super.cancelAbility();
    }

    private void eyeFlash() {
        FpeUtil.particles(this, ParticleTypes.END_ROD, FpeUtil.ahead(this, 0.5, getEyeHeight()), 18, 0.38, 0.22, 0.38, 0.045);
        FpeUtil.sound(this, SoundEvents.AMETHYST_BLOCK_CHIME, 1.3f, 0.65f);
        for (LivingEntity enemy : FpeCombat.cone(this, reach(7), 62)) {
            if (!hasLineOfSight(enemy)) continue;
            enemy.addEffect(new MobEffectInstance(MobEffects.BLINDNESS, 32 + getVariant() * 8), this);
            enemy.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 42 + getVariant() * 10, 1), this);
        }
    }

    private void paperShard(LivingEntity target, int side) {
        Vec3 from = FpeUtil.ahead(this, getBbWidth() * 0.45, getBbHeight() * 0.67)
                .add(FpeUtil.right(this).scale(side * (0.25 + getVariant() * 0.12)));
        Vec3 velocity = FpeUtil.aim(from, target, 1.35, 0.35);
        FpeUtil.projectile(this, FpeProjectile.Kind.DIAMOND, from, FpeCombat.rotY(velocity, side * 3), strikeDamage(0.73f));
        FpeUtil.sound(this, SoundEvents.ARROW_SHOOT, 0.65f, 1.25f);
    }

    private void groundBurst(Vec3 center, double radius, float damage, double knock, double lift) {
        double attackReach = reach(radius);
        FpeUtil.arc(this, ParticleTypes.CLOUD, center.add(0, 0.14, 0), getYRot(), 180, attackReach, 30);
        FpeUtil.particles(this, ParticleTypes.SQUID_INK, center.add(0, 0.2, 0), 15, 0.7, 0.2, 0.7, 0.02);
        FpeUtil.sound(this, SoundEvents.GENERIC_EXPLODE, 1.2f, 0.68f);
        for (LivingEntity victim : FpeUtil.enemiesInRadius(this, center, attackReach, 1.2, 0.8)) {
            if (hasLineOfSight(victim)) FpeUtil.hit(this, victim, strikeDamage(damage), knock, lift);
        }
    }

    public boolean isEcho() { return echoExpiresAt > 0; }

    private boolean canCreateEcho() {
        return !isEcho() && level().getGameTime() >= nextEchoAt;
    }

    private void spawnEcho(LivingEntity target) {
        if (!canCreateEcho() || !(getType().create(level()) instanceof Paperblight echo)) return;
        echo.echoExpiresAt = level().getGameTime() + ECHO_LIFETIME;
        echo.xpReward = 0;
        echo.setVariant(getVariant());
        echo.getAttribute(Attributes.MAX_HEALTH).setBaseValue(36);
        echo.getAttribute(Attributes.ATTACK_DAMAGE).setBaseValue(echo.getAttributeBaseValue(Attributes.ATTACK_DAMAGE) * 0.5);
        echo.setHealth(echo.getMaxHealth());
        double separation = (getBbWidth() + echo.getBbWidth()) * 0.5 + 0.5;
        Vec3 side = FpeUtil.right(this).scale(separation);
        Vec3 forward = FpeUtil.forward(this);
        for (Vec3 offset : List.of(side, side.reverse(), forward.scale(-separation))) {
            Vec3 at = position().add(offset);
            echo.moveTo(at.x, at.y, at.z, getYRot(), 0);
            AABB bounds = echo.getBoundingBox();
            if (!level().getWorldBorder().isWithinBounds(bounds) || !level().noCollision(echo, bounds)
                    || !level().getBlockCollisions(echo, bounds.move(0, -0.35, 0)).iterator().hasNext()) continue;
            echo.setTarget(target);
            if (!level().addFreshEntity(echo)) return;
            nextEchoAt = echo.echoExpiresAt;
            FpeUtil.particles(this, ParticleTypes.SQUID_INK, echo.getBoundingBox().getCenter(), 27, 0.52, 0.72, 0.52, 0.075);
            FpeUtil.sound(this, SoundEvents.SLIME_SQUISH, 1.35f, 0.55f);
            return;
        }
    }

    @Override public boolean shouldBeSaved() { return !isEcho() && super.shouldBeSaved(); }
    @Override public boolean shouldDropExperience() { return !isEcho() && super.shouldDropExperience(); }

    @Override
    protected void dropAllDeathLoot(DamageSource source) {
        if (!isEcho()) super.dropAllDeathLoot(source);
    }

    @Override
    public void addAdditionalSaveData(CompoundTag tag) {
        super.addAdditionalSaveData(tag);
        if (isEcho()) tag.putLong("PaperblightEchoExpiresAt", echoExpiresAt);
        if (nextEchoAt > level().getGameTime()) tag.putLong("PaperblightNextEchoAt", nextEchoAt);
    }

    @Override
    public void readAdditionalSaveData(CompoundTag tag) {
        super.readAdditionalSaveData(tag);
        echoExpiresAt = tag.getLong("PaperblightEchoExpiresAt");
        nextEchoAt = tag.getLong("PaperblightNextEchoAt");
        if (isEcho()) xpReward = 0;
    }
}
