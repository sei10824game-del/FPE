package com.fpe.entity.characters;

import java.util.List;

import javax.annotation.Nullable;

import com.fpe.entity.Ability;
import com.fpe.entity.FpeEntity;
import com.fpe.entity.FpeFx;
import com.fpe.entity.FpeProjectile;
import com.fpe.entity.FpeUtil;

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
import net.minecraft.world.phys.Vec3;

/**
 * ∆iden – silent, blood-stained child who works through the tool wall: axe, sledgehammer, saw, knives, crowbar,
 * pliers, drill and nail gun. Variant 1 = enraged (synced so the model can show the second axe).
 */
public class Aiden extends FpeEntity {
    @Nullable private LivingEntity grabbed;

    public Aiden(EntityType<? extends FpeEntity> type, Level level) { super(type, level); }

    @Override public Faction faction() { return Faction.STUDENT; }

    public static AttributeSupplier.Builder attributes() { return baseAttributes(75, 6, 0.27, 3, 0.25); }

    @Override public double preferredDistance() { return 2.2; }

    @Override
    public void tick() {
        super.tick();
        if (!level().isClientSide && isAlive()) {
            int v = isEnraged() ? 1 : 0;
            if (getVariant() != v) setVariant(v);
        }
    }

    private Vec3 hand(boolean right, double fwd, double y) {
        return FpeUtil.ahead(this, fwd, y).add(FpeUtil.right(this).scale(right ? 0.35 : -0.35));
    }

    private void fan(FpeProjectile.Kind kind, Vec3 from, LivingEntity t, int n, double stepDeg, double speed, float dmg) {
        Vec3 base = FpeUtil.aim(from, t, speed, 0.3);
        for (int i = 0; i < n; i++) FpeUtil.projectile(this, kind, from, base.yRot((float) Math.toRadians((i - (n - 1) / 2.0) * stepDeg)), dmg);
    }

    private void slash(double dist, double y, float r, float sweep, float tilt) {
        FpeUtil.fx(this, FpeFx.Kind.ARC, FpeUtil.ahead(this, dist, y), 0, 6, r, 0).param(sweep).color(0xD0C8CCD4).setXRot(tilt);
    }

    private void chop(float mult) {
        FpeUtil.hitCone(this, 3.2, 60, dmg(mult), 0.6, 0.2);
        slash(0.6, 0.9, 2.4f, 110, 85);
        FpeUtil.particles(this, ParticleTypes.CRIT, FpeUtil.ahead(this, 1.8, 0.2), 14, 0.4, 0.2, 0.4, 0.25);
        FpeUtil.particles(this, ParticleTypes.POOF, FpeUtil.ahead(this, 1.8, 0.1), 5, 0.3, 0.05, 0.3, 0.03);
        FpeUtil.sound(this, SoundEvents.ZOMBIE_ATTACK_WOODEN_DOOR, 0.9f, 1.1f);
    }

    private void slam(float mult) {
        Vec3 p = FpeUtil.ahead(this, 1.4, 0);
        FpeUtil.fx(this, FpeFx.Kind.RING_SHOCK, p.add(0, 0.05, 0), 0, 14, 5.5f, dmg(0.9f));
        FpeUtil.hitRadius(this, p, 1.8, dmg(mult), 0.8, 0.5);
        FpeUtil.particles(this, ParticleTypes.EXPLOSION, p, 1, 0, 0, 0, 0);
        FpeUtil.particles(this, ParticleTypes.LARGE_SMOKE, p, 10, 0.6, 0.1, 0.6, 0.03);
        FpeUtil.sound(this, SoundEvents.ANVIL_LAND, 1f, 0.6f);
    }

    private void sawCut() {
        FpeUtil.hitCone(this, 2.8, 50, dmg(0.55f), 0.1, 0);
        FpeUtil.particles(this, ParticleTypes.CRIT, FpeUtil.ahead(this, 1.2, 1.0), 6, 0.3, 0.2, 0.3, 0.15);
        FpeUtil.sound(this, SoundEvents.GRINDSTONE_USE, 0.8f, 1.5f);
    }

    @Override
    protected void registerAbilities(List<Ability> out) {
        // 1 axe chop – slow, huge wind-up
        out.add(Ability.of("axechop", 36, 50).range(0, 3.6).weight(4).faceUntil(14)
                .tick((e, t, k) -> {
                    if (k == 3) FpeUtil.sound(this, SoundEvents.ARMOR_EQUIP_CHAIN, 0.8f, 0.7f);
                    if (k == 15) dashForward(0.25, getDeltaMovement().y);
                    if (k == 16) chop(1.9f);
                    if (k == 24) FpeUtil.sound(this, SoundEvents.AXE_STRIP, 1f, 0.6f);
                }));
        // 2 axe throw (boomerang); a second axe when enraged
        out.add(Ability.of("axethrow", 30, 70).range(4.5, 14).weight(3)
                .tick((e, t, k) -> {
                    if (k == 12 || (k == 20 && isEnraged())) {
                        Vec3 from = hand(k == 12, 0.4, 1.6);
                        FpeUtil.projectile(this, FpeProjectile.Kind.AXE, from, FpeUtil.aim(from, t, 1.0, 0.4), dmg(1.2f));
                        FpeUtil.sound(this, SoundEvents.TRIDENT_THROW, 1f, 0.7f);
                    }
                }));
        // 3 sledgehammer slam + shockwave
        out.add(Ability.of("hammer", 38, 90).range(0, 4.5).weight(3).faceUntil(15)
                .tick((e, t, k) -> {
                    if (k == 12) dashForward(0.25, 0.35);
                    if (k == 17) slam(1.6f);
                }));
        // 4 hand-saw cuts
        out.add(Ability.of("hacksaw", 40, 60).range(0, 3).weight(3)
                .tick((e, t, k) -> {
                    if (k == 7) dashForward(0.2, getDeltaMovement().y);
                    if (k == 10 || k == 16 || k == 22 || k == 28) sawCut();
                }));
        // 5 knife fans
        out.add(Ability.of("knives", 28, 60).range(4, 14).weight(3)
                .tick((e, t, k) -> {
                    if (k == 4) FpeUtil.sound(this, SoundEvents.SHEEP_SHEAR, 0.8f, 1.4f);
                    if (k == 10 || k == 18) {
                        fan(FpeProjectile.Kind.KNIFE, hand(k == 10, 0.5, 1.2), t, isEnraged() ? 7 : 5, 10, 1.15, dmg(0.6f));
                        FpeUtil.sound(this, SoundEvents.PLAYER_ATTACK_SWEEP, 0.8f, 1.6f);
                    }
                }));
        // 6 crowbar uppercut + hook
        out.add(Ability.of("crowbar", 28, 45).range(0, 3.4).weight(3)
                .tick((e, t, k) -> {
                    if (k == 9) dashForward(0.25, getDeltaMovement().y);
                    if (k == 10) { FpeUtil.hitCone(this, 3.0, 60, dmg(1.1f), 0.2, 0.75); slash(0.7, 0.8, 2.2f, 120, -80); FpeUtil.sound(this, SoundEvents.ANVIL_HIT, 0.6f, 1.6f); }
                    if (k == 19) { FpeUtil.hitCone(this, 3.0, 70, dmg(0.9f), 0.9, 0.2); slash(0.7, 1.0, 2.4f, 150, 12); FpeUtil.sound(this, SoundEvents.ANVIL_HIT, 0.6f, 1.3f); }
                }));
        // 7 pliers grab & yank
        out.add(Ability.of("pliers", 36, 90).range(2, 7).weight(2).faceUntil(11)
                .start((e, t, k) -> grabbed = null)
                .tick((e, t, k) -> {
                    if (k == 11) {
                        Vec3 from = position().add(0, 1.1, 0);
                        Vec3 to = from.add(FpeUtil.forward(this).scale(7));
                        FpeUtil.particles(this, ParticleTypes.CRIT, from.lerp(to, 0.5), 8, 1.2, 0.05, 1.2, 0.05);
                        FpeUtil.sound(this, SoundEvents.CHAIN_BREAK, 1f, 1.4f);
                        if (FpeUtil.hitLine(this, from, to, 0.7, dmg(0.5f), 0, 0) > 0 && distanceTo(t) < 7.5) {
                            grabbed = t;
                            t.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 30, 3));
                        }
                    }
                    LivingEntity g = grabbed;
                    if (g == null || !g.isAlive()) return;
                    if (k > 11 && k <= 20) {
                        Vec3 d = position().add(FpeUtil.forward(this).scale(1.2)).subtract(g.position());
                        if (d.length() > 0.4) { Vec3 v = d.normalize().scale(Math.min(0.9, d.length() * 0.45)); g.setDeltaMovement(v.x, 0.08, v.z); g.hurtMarked = true; }
                    }
                    if (k == 22) {
                        if (distanceTo(g) < 3) { g.invulnerableTime = 0; FpeUtil.hit(this, g, dmg(1.1f), 0.6, 0.25); }
                        FpeUtil.particles(this, ParticleTypes.DAMAGE_INDICATOR, g.position().add(0, 1, 0), 6, 0.3, 0.3, 0.3, 0.1);
                        FpeUtil.sound(this, SoundEvents.SHEEP_SHEAR, 1f, 0.6f);
                        grabbed = null;
                    }
                })
                .end((e, t, k) -> grabbed = null));
        // 8 power drill thrusts
        out.add(Ability.of("drill", 36, 60).range(0, 4).weight(3)
                .tick((e, t, k) -> {
                    if (k >= 5 && k < 30 && k % 4 == 1) FpeUtil.sound(this, SoundEvents.BEEHIVE_WORK, 1.2f, 0.6f);
                    for (int i = 0; i < 4; i++) {
                        int pk = 10 + 6 * i;
                        if (k == pk - 1) dashForward(0.3, getDeltaMovement().y);
                        if (k == pk) {
                            Vec3 from = position().add(0, 0.9, 0);
                            FpeUtil.hitLine(this, from, from.add(FpeUtil.forward(this).scale(2.7)), 0.5, dmg(0.55f), 0.2, 0.05);
                            FpeUtil.particles(this, ParticleTypes.CRIT, FpeUtil.ahead(this, 1.6, 0.9), 6, 0.1, 0.1, 0.1, 0.25);
                        }
                    }
                }));
        // 9 nail gun stream
        out.add(Ability.of("nailgun", 32, 70).range(3, 14).weight(2)
                .tick((e, t, k) -> {
                    if (k >= 8 && k <= 24 && k % 2 == 0) {
                        Vec3 from = hand(true, 0.8, 1.15);
                        Vec3 v = FpeUtil.aim(from, t, 1.6, 0.5).add((random.nextDouble() - 0.5) * 0.12, (random.nextDouble() - 0.5) * 0.08, (random.nextDouble() - 0.5) * 0.12);
                        FpeUtil.projectile(this, FpeProjectile.Kind.BULLET, from, v, dmg(0.3f));
                        FpeUtil.sound(this, SoundEvents.CROSSBOW_SHOOT, 0.6f, 1.8f);
                    }
                }));
        // 10 workshop (enraged combo through every tool)
        out.add(Ability.of("workshop", 64, 200).range(0, 6).weight(4).when(FpeEntity::isEnraged)
                .tick((e, t, k) -> {
                    if (k == 8) { fan(FpeProjectile.Kind.KNIFE, hand(true, 0.5, 1.2), t, 7, 9, 1.15, dmg(0.55f)); FpeUtil.sound(this, SoundEvents.PLAYER_ATTACK_SWEEP, 0.8f, 1.6f); }
                    if (k == 14) dashToward(t.position(), 0.5, getDeltaMovement().y);
                    if (k == 18 || k == 22) sawCut();
                    if (k == 30) dashToward(t.position(), 0.3, 0.35);
                    if (k == 34) slam(1.4f);
                    if (k == 47) dashForward(0.25, getDeltaMovement().y);
                    if (k == 48) chop(1.6f);
                    if (k == 56) {
                        for (int i = 0; i < 3; i++) {
                            Vec3 from = position().add(0, 1.2, 0);
                            FpeUtil.projectile(this, FpeProjectile.Kind.AXE, from, FpeUtil.aim(from, t, 0.9, 0.2).yRot((float) Math.toRadians((i - 1) * 25)), dmg(1.0f));
                        }
                        FpeUtil.sound(this, SoundEvents.TRIDENT_THROW, 1f, 0.5f);
                    }
                }));
        // 11 saw blade waves: flat sweep (12) + backhand (21), each launches a piercing crescent
        out.add(Ability.of("bladewave", 30, 80).range(3.5, 12).weight(3)
                .tick((e, t, k) -> {
                    if (k == 4) FpeUtil.sound(this, SoundEvents.GRINDSTONE_USE, 0.8f, 0.8f);
                    if (k == 12 || k == 21) {
                        Vec3 from = FpeUtil.ahead(this, 0.6, 1.0);
                        FpeUtil.projectile(this, FpeProjectile.Kind.BLADE_WAVE, from, FpeUtil.aim(from, t, 1.1, 0.3), dmg(k == 12 ? 0.9f : 1.0f));
                        if (isEnraged()) for (int s = -1; s <= 1; s += 2)
                            FpeUtil.projectile(this, FpeProjectile.Kind.BLADE_WAVE, from, FpeUtil.aim(from, t, 1.1, 0.3).yRot((float) Math.toRadians(18 * s)), dmg(0.7f));
                        slash(0.8, 1.0, 2.6f, 160, k == 12 ? 4 : -4);
                        FpeUtil.hitCone(this, 2.6, 70, dmg(0.6f), 0.4, 0.1);
                        FpeUtil.sound(this, SoundEvents.PLAYER_ATTACK_SWEEP, 1f, 0.7f);
                    }
                }));
        // 12 bear trap: underhand toss (12) onto the target's predicted spot; snaps shut after a short warm-up
        out.add(Ability.of("beartrap", 34, 110).range(3, 10).weight(2)
                .tick((e, t, k) -> {
                    if (k == 6) FpeUtil.sound(this, SoundEvents.IRON_TRAPDOOR_OPEN, 1f, 0.6f);
                    if (k == 12) {
                        Vec3 at = t.position().add(t.getDeltaMovement().multiply(6, 0, 6));
                        FpeUtil.fx(this, FpeFx.Kind.RING_TRAP, at.add(0, 0.05, 0), 14, 20, 1.8f, dmg(1.4f));
                        FpeUtil.particles(this, ParticleTypes.CRIT, at.add(0, 0.2, 0), 10, 0.6, 0.05, 0.6, 0.05);
                        FpeUtil.sound(this, SoundEvents.CHAIN_PLACE, 1f, 0.8f);
                    }
                    if (k == 26) {
                        for (LivingEntity v : FpeUtil.enemiesInRadius(this, t.position(), 2.4, 2, 0.5))
                            v.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 40, 3));
                        FpeUtil.sound(this, SoundEvents.IRON_TRAPDOOR_CLOSE, 1.2f, 0.5f);
                    }
                }));
        // 13 tool rain (enraged): flings blades skyward (10), five waves rain down around the target, last wave a falling axe
        out.add(Ability.of("toolrain", 50, 220).range(0, 12).weight(3).when(FpeEntity::isEnraged).blind()
                .tick((e, t, k) -> {
                    if (k == 10) {
                        FpeUtil.particles(this, ParticleTypes.CRIT, position().add(0, 2.2, 0), 20, 0.4, 0.8, 0.4, 0.3);
                        FpeUtil.sound(this, SoundEvents.PLAYER_ATTACK_SWEEP, 1f, 1.4f);
                    }
                    if (k == 16 || k == 22 || k == 28 || k == 34 || k == 40) {
                        int n = k == 40 ? 1 : 3;
                        for (int i = 0; i < n; i++) {
                            double a = random.nextDouble() * Math.PI * 2, r = k == 40 ? 0 : 0.6 + random.nextDouble() * 1.8;
                            Vec3 from = t.position().add(Math.cos(a) * r, 7, Math.sin(a) * r);
                            FpeUtil.projectile(this, k == 40 ? FpeProjectile.Kind.AXE : FpeProjectile.Kind.KNIFE, from, new Vec3(0, -1.1, 0), dmg(k == 40 ? 1.3f : 0.55f));
                        }
                        FpeUtil.sound(this, SoundEvents.ARROW_SHOOT, 0.8f, 0.6f);
                    }
                }));
    }

    // ------------------------------------------------------------------ sounds (quiet, unsettling child)
    @Override protected SoundEvent getAmbientSound() { return SoundEvents.AMBIENT_CAVE.value(); }
    @Override protected SoundEvent getHurtSound(DamageSource s) { return SoundEvents.PLAYER_HURT; }
    @Override protected SoundEvent getDeathSound() { return SoundEvents.PLAYER_DEATH; }
    @Override public float getVoicePitch() { return 1.35f; }
    @Override public int getAmbientSoundInterval() { return 240; }
}
