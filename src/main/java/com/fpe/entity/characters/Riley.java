package com.fpe.entity.characters;

import java.util.List;

import com.fpe.entity.Ability;
import com.fpe.entity.FpeEntity;
import com.fpe.entity.FpeFx;
import com.fpe.entity.FpeProjectile;
import com.fpe.entity.FpeUtil;

import net.minecraft.core.particles.DustParticleOptions;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.util.Mth;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.Vec3;
import org.joml.Vector3f;

/**
 * Riley (original FPE student): paper-cutout girl with a huge fanged grin, white ponytail + black bow, a black devil tail,
 * and a KNIFE. Fast knife combos, stabs, throws, feints, a vanishing backstab and bleeding cuts; enraged = frenzy + carve.
 * Every tick index below matches the key poses in tools/bbgen/chars/riley.py.
 */
public class Riley extends FpeEntity {
    private static final DustParticleOptions BLOOD = new DustParticleOptions(new Vector3f(0.55f, 0.04f, 0.06f), 1.1f);
    private static final DustParticleOptions INK = new DustParticleOptions(new Vector3f(0.1f, 0.08f, 0.13f), 1.5f);
    private static final int STEEL_ARC = 0xD0E8EAF0, DARK_ARC = 0xD0231E2A;
    private boolean grabbed;
    /** crowd-control victim of knife_pin / tail_snare / ambush_grab (null = nobody caught) */
    private LivingEntity victim;
    private Vec3 pinPos;

    public Riley(EntityType<? extends FpeEntity> type, Level level) { super(type, level); }

    @Override public Faction faction() { return Faction.STUDENT; }

    @Override public boolean meleeFocus() { return true; }

    public static AttributeSupplier.Builder attributes() { return baseAttributes(80, 6, 0.36, 2, 0.15); }

    @Override public double preferredDistance() { return 1.6; }
    @Override protected int restTicks() { return isEnraged() ? 4 : 10; }

    @Override protected SoundEvent getAmbientSound() { return SoundEvents.WITCH_CELEBRATE; }
    @Override protected SoundEvent getHurtSound(DamageSource s) { return SoundEvents.PLAYER_HURT; }
    @Override protected SoundEvent getDeathSound() { return SoundEvents.PLAYER_DEATH; }
    @Override public float getVoicePitch() { return 1.45f; }

    // ------------------------------------------------------------------ helpers
    private void arc(float radius, float sweep, float tilt, double y, int color) {
        FpeFx f = FpeUtil.fx(this, FpeFx.Kind.ARC, position().add(0, y, 0), 0, 6, radius, 0).param(sweep).color(color);
        f.setYRot(getYRot());
        f.setXRot(tilt);
    }

    /** bleed: a short wither tick + red droplets */
    private void bleed(LivingEntity v, int ticks) {
        v.addEffect(new MobEffectInstance(MobEffects.WITHER, ticks, 0));
        FpeUtil.particles(this, BLOOD, v.position().add(0, v.getBbHeight() * 0.6, 0), 10, 0.25, 0.3, 0.25, 0.05);
    }

    /** a knife cut in front: cone hit, then bleed on everything it touched */
    private void cut(float mult, double reach, double halfAngle, double knock, int bleedTicks) {
        FpeUtil.hitCone(this, reach, halfAngle, dmg(mult), knock, 0.1);
        for (LivingEntity v : FpeUtil.enemiesInRadius(this, FpeUtil.ahead(this, reach * 0.55, 0), reach * 0.6, 2.5, 1)) bleed(v, bleedTicks);
        FpeUtil.particles(this, ParticleTypes.CRIT, FpeUtil.ahead(this, 1.3, 1.1), 8, 0.3, 0.3, 0.3, 0.2);
        FpeUtil.sound(this, SoundEvents.PLAYER_ATTACK_SWEEP, 0.9f, 1.5f);
        FpeUtil.sound(this, SoundEvents.TRIDENT_HIT, 0.6f, 1.7f);
    }

    private void stab(float mult, double reach, int bleedTicks) {
        FpeUtil.hitLine(this, FpeUtil.ahead(this, 0.3, 1.0), FpeUtil.ahead(this, reach, 1.0), 0.7, dmg(mult), 0.35, 0.05);
        for (LivingEntity v : FpeUtil.enemiesInRadius(this, FpeUtil.ahead(this, reach * 0.7, 0), 0.9, 2.5, 1)) bleed(v, bleedTicks);
        FpeUtil.particles(this, ParticleTypes.CRIT, FpeUtil.ahead(this, reach * 0.8, 1.0), 10, 0.15, 0.15, 0.15, 0.25);
        FpeUtil.sound(this, SoundEvents.TRIDENT_HIT, 1f, 1.4f);
        FpeUtil.sound(this, SoundEvents.PLAYER_ATTACK_STRONG, 0.8f, 1.5f);
    }

    private void giggle(float pitch) { FpeUtil.sound(this, SoundEvents.WITCH_CELEBRATE, 1.1f, pitch); }

    private Vec3 hand(boolean right) { return FpeUtil.ahead(this, 0.45, 1.35).add(FpeUtil.right(this).scale(right ? 0.3 : -0.3)); }

    private void throwKnives(Vec3 from, LivingEntity t, int n, double spreadDeg, double speed, float dmg) {
        Vec3 dir = FpeUtil.aim(from, t, speed, 0.5);
        for (int i = 0; i < n; i++) {
            double a = Math.toRadians((i - (n - 1) / 2.0) * spreadDeg);
            double c = Math.cos(a), s = Math.sin(a);
            FpeUtil.projectile(this, FpeProjectile.Kind.KNIFE, from, new Vec3(dir.x * c - dir.z * s, dir.y, dir.x * s + dir.z * c), dmg);
        }
        FpeUtil.sound(this, SoundEvents.TRIDENT_THROW, 1f, 1.5f);
    }

    /** nearest valid enemy in a horizontal cone in front of her (same rules as hitCone), or null */
    private LivingEntity pick(double range, double halfAngle) {
        Vec3 f = FpeUtil.forward(this);
        LivingEntity best = null;
        double bd = Double.MAX_VALUE;
        for (LivingEntity v : FpeUtil.enemiesInRadius(this, position(), range + 0.5, 2.5, 1.5)) {
            Vec3 d = new Vec3(v.getX() - getX(), 0, v.getZ() - getZ());
            double dist = d.length() - v.getBbWidth() * 0.5 - getBbWidth() * 0.5;
            if (dist > range || dist >= bd) continue;
            if (d.lengthSqr() > 0.01 && Math.toDegrees(Math.acos(Mth.clamp(d.normalize().dot(f), -1, 1))) > halfAngle) continue;
            best = v; bd = dist;
        }
        return best;
    }

    /** the caught victim while it is still a legal target; otherwise releases it */
    private LivingEntity held() {
        if (victim != null && (!FpeUtil.canHurt(this, victim) || victim.distanceToSqr(this) > 64)) victim = null;
        return victim;
    }

    private void release(FpeEntity e, LivingEntity t, int k) { victim = null; pinPos = null; }

    // ------------------------------------------------------------------ abilities
    @Override
    protected void registerAbilities(List<Ability> out) {
        // 1. Slash combo: forehand slash t7, backhand t13, thrusting stab t21
        out.add(Ability.of("slash_combo", 32, 30).range(0, 3.2).weight(5).tick((e, t, k) -> {
            Riley c = (Riley) e;
            if (k == 5 || k == 11 || k == 19) { e.snapFace(t); e.dashForward(k == 19 ? 0.4 : 0.22, 0); }
            if (k == 7 || k == 13) { t.invulnerableTime = 0; c.cut(0.7f, 2.8, 70, 0.2, 20); c.arc(2.2f, 140, k == 7 ? 8 : -8, 1.1, STEEL_ARC); }
            if (k == 21) { t.invulnerableTime = 0; c.stab(1.0f, 3.0, 40); }
        }));

        // 2. Overhead stab (the art pose): knife raised overhead, trembling grin (0-13), PLUNGE t16 - heavy bleed
        out.add(Ability.of("overhead_stab", 32, 55).range(0, 3.0).weight(4).faceUntil(13).tick((e, t, k) -> {
            Riley c = (Riley) e;
            if (k == 4) c.giggle(1.6f);
            if (k == 14) e.dashForward(0.35, 0);
            if (k == 16) {
                FpeUtil.hitCone(e, 2.6, 45, e.dmg(1.6f), 0.2, -0.1);
                for (LivingEntity v : FpeUtil.enemiesInRadius(e, FpeUtil.ahead(e, 1.4, 0), 1.3, 2.5, 1)) {
                    c.bleed(v, 80);
                    v.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 40, 1));
                }
                c.arc(2.0f, 70, 85, 1.2, DARK_ARC);
                FpeUtil.sound(e, SoundEvents.TRIDENT_HIT, 1.2f, 0.9f);
                FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_CRIT, 1f, 0.8f);
            }
        }));

        // 3. Lunge stab: coiled crouch (0-8), dash t9, arm-extended stab t12
        out.add(Ability.of("lunge_stab", 30, 50).range(2.8, 8).weight(4).faceUntil(9).tick((e, t, k) -> {
            Riley c = (Riley) e;
            if (k == 9) {
                e.dashToward(t.position(), Mth.clamp(e.distanceTo(t) * 0.17, 0.6, 1.3), 0.05);
                FpeUtil.particles(e, ParticleTypes.CLOUD, e.position(), 6, 0.3, 0.05, 0.3, 0.03);
                FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_SWEEP, 0.8f, 1.8f);
            }
            if (k == 12) c.stab(1.4f, 3.2, 40);
        }));

        // 4. Knife throw: overhead wind-up, single fast knife t11 (draws a new one t19)
        out.add(Ability.of("knife_throw", 26, 35).range(5, 18).weight(4).tick((e, t, k) -> {
            Riley c = (Riley) e;
            if (k == 11) c.throwKnives(c.hand(true).add(0, 0.4, 0), t, 1, 0, 1.6, e.dmg(0.9f));
            if (k == 19) FpeUtil.sound(e, SoundEvents.ARMOR_EQUIP_IRON, 0.6f, 1.8f);
        }));

        // 5. Knife fan: right-hand throw t14, then a backhand fan of 3 (5 enraged) from the claw t22
        out.add(Ability.of("knife_fan", 36, 70).range(4, 16).weight(3).tick((e, t, k) -> {
            Riley c = (Riley) e;
            if (k == 5) FpeUtil.sound(e, SoundEvents.ARMOR_EQUIP_IRON, 0.8f, 1.6f);
            if (k == 14) c.throwKnives(c.hand(true).add(0, 0.4, 0), t, 1, 0, 1.5, e.dmg(0.7f));
            if (k == 22) c.throwKnives(c.hand(false), t, e.isEnraged() ? 5 : 3, 11, 1.3, e.dmg(0.6f));
        }));

        // 6. Feint stab: fake overhead swing t6, side-hop t10, low gut stab from the other side t17 (bonus damage + bleed)
        out.add(Ability.of("feint_stab", 30, 55).range(0, 3.6).weight(3).tick((e, t, k) -> {
            Riley c = (Riley) e;
            if (k == 6) { FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_NODAMAGE, 1f, 1.4f); c.arc(1.8f, 100, 60, 1.4, STEEL_ARC); }
            if (k == 10) {
                Vec3 side = FpeUtil.right(e).scale(-0.55);
                e.setDeltaMovement(side.x, 0.28, side.z);
                e.hurtMarked = true;
                c.giggle(1.8f);
            }
            if (k == 15) { e.snapFace(t); e.dashForward(0.35, 0); }
            if (k == 17) { t.invulnerableTime = 0; c.stab(1.5f, 2.8, 60); }
        }));

        // 7. Tail whip: coil (0-8), full spin - the arrow-tipped tail lashes everything around t12
        out.add(Ability.of("tail_whip", 28, 60).range(0, 3.0).weight(3).tick((e, t, k) -> {
            Riley c = (Riley) e;
            if (k == 12) {
                FpeUtil.hitRadius(e, e.position().add(0, 0.6, 0), 2.8, e.dmg(0.9f), 1.1, 0.3);
                FpeUtil.arc(e, ParticleTypes.SWEEP_ATTACK, e.position().add(0, 0.6, 0), e.getYRot(), 180, 2.2, 10);
                c.arc(2.6f, 360, 0, 0.6, DARK_ARC);
                FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_SWEEP, 1.1f, 0.9f);
            }
        }));

        // 8. Backstab: giggle, POOF vanish t10, teleports behind the target t14, reappears t16, overhead stab t22
        out.add(Ability.of("backstab", 44, 110).range(3, 14).weight(3).faceUntil(9).tick((e, t, k) -> {
            Riley c = (Riley) e;
            if (k == 2) c.giggle(1.5f);
            if (k == 10) {
                FpeUtil.particles(e, ParticleTypes.LARGE_SMOKE, e.position().add(0, 0.8, 0), 20, 0.3, 0.5, 0.3, 0.02);
                FpeUtil.particles(e, INK, e.position().add(0, 0.8, 0), 16, 0.3, 0.5, 0.3, 0.02);
                FpeUtil.sound(e, SoundEvents.ENDERMAN_TELEPORT, 0.8f, 1.6f);
                e.addEffect(new MobEffectInstance(MobEffects.INVISIBILITY, 6, 0, false, false));
            }
            if (k == 14) {
                Vec3 look = Vec3.directionFromRotation(0, t.getYRot());
                Vec3 to = t.position().subtract(look.scale(1.4));
                if (e.level().noCollision(e, e.getBoundingBox().move(to.subtract(e.position())))) e.teleportTo(to.x, to.y, to.z);
                e.snapFace(t);
            }
            if (k == 16) {
                e.snapFace(t);
                FpeUtil.particles(e, ParticleTypes.LARGE_SMOKE, e.position().add(0, 0.8, 0), 14, 0.3, 0.5, 0.3, 0.02);
                FpeUtil.sound(e, SoundEvents.ENDERMAN_TELEPORT, 0.6f, 1.9f);
            }
            if (k == 20) e.snapFace(t);
            if (k == 22) {
                t.invulnerableTime = 0;
                FpeUtil.hitCone(e, 2.6, 55, e.dmg(1.8f), 0.3, 0.05);
                for (LivingEntity v : FpeUtil.enemiesInRadius(e, FpeUtil.ahead(e, 1.2, 0), 1.3, 2.5, 1)) c.bleed(v, 80);
                c.arc(1.8f, 80, 80, 1.2, DARK_ARC);
                FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_CRIT, 1.2f, 0.8f);
            }
        }));

        // 9. Pounce stab: coil (0-9), leap t10, lands on the target t20 stabbing, again t27, last t34
        out.add(Ability.of("pounce_stab", 42, 90).range(3.5, 10).weight(3).faceUntil(10).tick((e, t, k) -> {
            Riley c = (Riley) e;
            if (k == 4) c.giggle(1.7f);
            if (k == 10) {
                e.dashToward(t.position(), Mth.clamp(e.distanceTo(t) * 0.11, 0.45, 1.15), 0.55);
                FpeUtil.particles(e, ParticleTypes.CLOUD, e.position(), 8, 0.4, 0.05, 0.4, 0.05);
                FpeUtil.sound(e, SoundEvents.GOAT_LONG_JUMP, 1f, 1.4f);
            }
            if (k > 10 && k < 22) e.fallDistance = 0;
            if (k == 20 || k == 27 || k == 34) {
                t.invulnerableTime = 0;
                float mult = k == 34 ? 1.2f : 0.7f;
                FpeUtil.hitRadius(e, FpeUtil.ahead(e, 0.7, 0), 1.5, e.dmg(mult), k == 34 ? 0.8 : 0.0, 0.1);
                for (LivingEntity v : FpeUtil.enemiesInRadius(e, FpeUtil.ahead(e, 0.7, 0), 1.5, 2.5, 1)) {
                    c.bleed(v, 30);
                    if (k < 34) v.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 14, 4));
                }
                FpeUtil.sound(e, SoundEvents.TRIDENT_HIT, 1f, 1.2f + k * 0.01f);
                if (k == 20) FpeUtil.particles(e, ParticleTypes.POOF, e.position(), 10, 0.6, 0.1, 0.6, 0.04);
            }
        }));

        // 10. Blade spin: arms flung out, spinning top - cuts t10 / t16 / t22 all around
        out.add(Ability.of("blade_spin", 34, 70).range(0, 3.2).weight(3).moving().tick((e, t, k) -> {
            Riley c = (Riley) e;
            if (k == 8 || k == 14 || k == 20) e.dashToward(t.position(), 0.18, 0);
            if (k == 10 || k == 16 || k == 22) {
                for (LivingEntity v : FpeUtil.enemiesInRadius(e, e.position(), 2.6, 2.5, 1)) {
                    v.invulnerableTime = 0;
                    FpeUtil.hit((FpeEntity) e, v, e.dmg(0.6f), 0.4, 0.1);
                    c.bleed(v, 20);
                }
                c.arc(2.4f, 360, 0, 1.0, STEEL_ARC);
                FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_SWEEP, 1f, 1.3f + k * 0.02f);
            }
        }));

        // 11. Giggle: crazed laughing fit - fear pulse t14 (slow + weakness on nearby enemies), she gets faster/stronger
        out.add(Ability.of("giggle", 36, 220).range(2, 12).weight(2).blind().tick((e, t, k) -> {
            Riley c = (Riley) e;
            if (k == 10 || k == 16 || k == 22) c.giggle(1.3f + k * 0.03f);
            if (k == 14) {
                for (LivingEntity v : FpeUtil.enemiesInRadius(e, e.position(), 7, 3, 2)) {
                    v.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 60, 1));
                    v.addEffect(new MobEffectInstance(MobEffects.WEAKNESS, 80, 0));
                }
                e.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SPEED, 120, 1));
                e.addEffect(new MobEffectInstance(MobEffects.DAMAGE_BOOST, 120, 0));
                FpeUtil.fx(e, FpeFx.Kind.RING_SHOCK, e.position().add(0, 0.1, 0), 0, 12, 6f, 0);
                FpeUtil.particles(e, INK, e.position().add(0, 1.2, 0), 30, 1.5, 0.6, 1.5, 0.05);
            }
        }));

        // 12. Frenzy (enraged): six manic stabs t8..t28, final wide slash t34
        out.add(Ability.of("frenzy", 46, 80).range(0, 3.6).weight(4).when(FpeEntity::isEnraged).tick((e, t, k) -> {
            Riley c = (Riley) e;
            if (k >= 6 && k <= 26 && (k - 6) % 4 == 0) { e.snapFace(t); e.dashForward(0.18, 0); }
            if (k >= 8 && k <= 28 && (k - 8) % 4 == 0) { t.invulnerableTime = 0; c.stab(0.45f, 2.6, 20); }
            if (k == 32) e.dashForward(0.3, 0);
            if (k == 34) { t.invulnerableTime = 0; c.cut(1.1f, 3.0, 90, 0.9, 40); c.arc(2.6f, 170, 0, 1.1, DARK_ARC); }
        }));

        // 13. Carve (enraged signature): claw grab t10, holds the victim, cuts t20 / t28 / deep stab t36, kicks them off t48
        out.add(Ability.of("carve", 60, 160).range(0, 3.0).weight(4).when(FpeEntity::isEnraged).faceUntil(9)
                .start((e, t, k) -> ((Riley) e).grabbed = false).tick((e, t, k) -> {
            Riley c = (Riley) e;
            if (k == 8) e.dashForward(0.45, 0);
            if (k == 10) {
                Vec3 to = t.position().subtract(e.position());
                double ang = Math.toDegrees(Math.acos(Mth.clamp(new Vec3(to.x, 0, to.z).normalize().dot(FpeUtil.forward(e)), -1, 1)));
                c.grabbed = e.distanceTo(t) < 3.0 && ang < 60 && FpeUtil.canHurt(e, t);
                FpeUtil.sound(e, c.grabbed ? SoundEvents.PLAYER_ATTACK_KNOCKBACK : SoundEvents.PLAYER_ATTACK_NODAMAGE, 1f, 1.3f);
                if (c.grabbed) { FpeUtil.hit(c, t, e.dmg(0.3f), 0, 0); c.giggle(1.6f); }
            }
            if (c.grabbed && !FpeUtil.canHurt(e, t)) c.grabbed = false;
            if (c.grabbed && k > 10 && k < 48) {
                FpeUtil.hold(e, t, 1.1, 0.2, 0);
                FpeUtil.stun(t, 4);
                if (k == 20 || k == 28 || k == 36) {
                    t.invulnerableTime = 0;
                    FpeUtil.hit(c, t, e.dmg(k == 36 ? 1.0f : 0.7f), 0, 0);
                    c.bleed(t, 60);
                    c.arc(1.6f, 90, k == 20 ? 40 : (k == 28 ? -40 : 0), 1.1, DARK_ARC);
                    FpeUtil.sound(e, SoundEvents.TRIDENT_HIT, 1.1f, 1.1f);
                }
            }
            if (k == 48 && c.grabbed) {
                t.invulnerableTime = 0;
                FpeUtil.hit(c, t, e.dmg(0.6f), 0, 0);
                FpeUtil.fling(t, FpeUtil.forward(e), 1.6, 0.5);
                FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_KNOCKBACK, 1.2f, 1.0f);
                c.giggle(1.9f);
            }
        }).end((e, t, k) -> ((Riley) e).grabbed = false));

        // 14. Knife pin (CC: root): reverse-grip wind-up (0-8), low dash t9, PLUNGES the knife through the victim's foot t12 and kneels
        //     on it - victim pinned in place 12-24 (twist t17), rips it out t24 -> still rooted ~2s, bleeding
        out.add(Ability.of("knife_pin", 34, 160).range(0, 3.4).weight(2).faceUntil(9).start(this::release).end(this::release).tick((e, t, k) -> {
            Riley c = (Riley) e;
            if (k == 3) c.giggle(1.7f);
            if (k == 9) e.dashForward(0.35, 0);
            if (k == 12) {
                c.victim = c.pick(2.6, 55);
                LivingEntity v = c.victim;
                if (v == null) { FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_NODAMAGE, 1f, 1.2f); return; }
                c.pinPos = v.position();
                v.invulnerableTime = 0;
                FpeUtil.hit(c, v, e.dmg(0.8f), 0, 0);
                FpeUtil.root(v, 64);
                c.bleed(v, 60);
                FpeUtil.particles(e, ParticleTypes.CRIT, v.position().add(0, 0.2, 0), 12, 0.2, 0.1, 0.2, 0.2);
                FpeUtil.sound(e, SoundEvents.TRIDENT_HIT, 1.2f, 0.8f);
                FpeUtil.sound(e, SoundEvents.ANVIL_LAND, 0.4f, 1.8f);
            }
            LivingEntity v = c.held();
            if (v == null || c.pinPos == null) return;
            if (k > 12 && k < 24) FpeUtil.holdAt(v, c.pinPos);
            if (k == 17) {
                v.invulnerableTime = 0;
                FpeUtil.hit(c, v, e.dmg(0.3f), 0, 0);
                FpeUtil.particles(e, BLOOD, v.position().add(0, 0.2, 0), 8, 0.2, 0.1, 0.2, 0.05);
                FpeUtil.sound(e, SoundEvents.TRIDENT_HIT, 0.8f, 1.4f);
                c.giggle(1.9f);
            }
            if (k == 24) {
                c.bleed(v, 40);
                FpeUtil.particles(e, BLOOD, v.position().add(0, 0.4, 0), 16, 0.2, 0.4, 0.2, 0.1);
                FpeUtil.sound(e, SoundEvents.TRIDENT_RETURN, 1f, 1.6f);
                c.victim = null;
            }
        }));

        // 15. Tail snare (CC: pull + disarm + stun): tail coils overhead (0-8), LASHES out t10 and wraps the nearest enemy in a narrow
        //     line (knocks the held item loose), reels it in 11-18, trips it t19 (stunned), overhead stab on the downed victim t22
        out.add(Ability.of("tail_snare", 34, 140).range(2.5, 6.5).weight(2).faceUntil(10).start(this::release).end(this::release).tick((e, t, k) -> {
            Riley c = (Riley) e;
            if (k == 4) FpeUtil.sound(e, SoundEvents.PHANTOM_FLAP, 0.8f, 1.6f);
            if (k == 10) {
                c.victim = c.pick(6.5, 22);
                Vec3 from = FpeUtil.ahead(e, 0.4, 1.4);
                Vec3 to = c.victim != null ? c.victim.position().add(0, c.victim.getBbHeight() * 0.4, 0) : FpeUtil.ahead(e, 6.5, 1.0);
                for (int i = 0; i <= 12; i++) FpeUtil.particles(e, INK, from.lerp(to, i / 12.0), 1, 0.02, 0.02, 0.02, 0);
                FpeUtil.sound(e, SoundEvents.FISHING_BOBBER_THROW, 1f, 0.7f);
                if (c.victim != null) {
                    c.victim.invulnerableTime = 0;
                    FpeUtil.hit(c, c.victim, e.dmg(0.3f), 0, 0);
                    FpeUtil.disarm(c.victim);
                    FpeUtil.sound(e, SoundEvents.LEASH_KNOT_PLACE, 1f, 0.8f);
                }
            }
            LivingEntity v = c.held();
            if (v == null) return;
            if (k > 10 && k < 19) {
                FpeUtil.pull(v, FpeUtil.ahead(e, 1.3, 0), 0.75);
                FpeUtil.root(v, 3);
                if (k % 3 == 0) FpeUtil.particles(e, INK, v.position().add(0, 0.4, 0), 3, 0.15, 0.15, 0.15, 0);
            }
            if (k == 19) {
                FpeUtil.stun(v, 40);
                FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_KNOCKBACK, 1f, 0.9f);
                c.giggle(1.8f);
            }
            if (k > 19 && k < 22 && v.distanceTo(e) < 3.0) FpeUtil.hold(e, v, 1.3, 0, 0);
            if (k == 22) {
                if (v.distanceTo(e) < 3.2) {
                    v.invulnerableTime = 0;
                    FpeUtil.hit(c, v, e.dmg(1.1f), 0.2, 0);
                    c.bleed(v, 50);
                    c.arc(1.8f, 70, 85, 1.0, DARK_ARC);
                    FpeUtil.sound(e, SoundEvents.TRIDENT_HIT, 1.2f, 1.0f);
                }
                c.victim = null;
            }
        }));

        // 16. Ambush grab (CC: hold + stun -> daze + disarm): sinks into an ink puddle giggling (0-8), gone t9, reappears BEHIND the
        //     target t14, claw grabs it t16 and holds it in front of her (stunned) - side stabs t22 / t30, deep stab t38, kicks it
        //     away t44 dazed and disarmed
        out.add(Ability.of("ambush_grab", 56, 240).range(2, 10).weight(2).faceUntil(8).start(this::release).end(this::release).tick((e, t, k) -> {
            Riley c = (Riley) e;
            if (k == 2) c.giggle(1.4f);
            if (k == 9) {
                FpeUtil.particles(e, INK, e.position().add(0, 0.3, 0), 24, 0.5, 0.1, 0.5, 0.02);
                FpeUtil.particles(e, ParticleTypes.LARGE_SMOKE, e.position().add(0, 0.6, 0), 12, 0.3, 0.4, 0.3, 0.02);
                FpeUtil.sound(e, SoundEvents.HONEY_BLOCK_SLIDE, 1f, 0.6f);
                e.addEffect(new MobEffectInstance(MobEffects.INVISIBILITY, 6, 0, false, false));
            }
            if (k == 12 && FpeUtil.canHurt(e, t)) {
                Vec3 to = t.position().subtract(Vec3.directionFromRotation(0, t.getYRot()).scale(1.2));
                if (e.level().noCollision(e, e.getBoundingBox().move(to.subtract(e.position())))) e.teleportTo(to.x, to.y, to.z);
                e.snapFace(t);
            }
            if (k == 14) {
                e.snapFace(t);
                FpeUtil.particles(e, INK, e.position().add(0, 0.3, 0), 20, 0.5, 0.1, 0.5, 0.03);
                FpeUtil.sound(e, SoundEvents.HONEY_BLOCK_SLIDE, 1f, 1.2f);
            }
            if (k == 16) {
                c.victim = c.pick(2.4, 60);
                FpeUtil.sound(e, c.victim != null ? SoundEvents.PLAYER_ATTACK_KNOCKBACK : SoundEvents.PLAYER_ATTACK_NODAMAGE, 1f, 1.3f);
                if (c.victim != null) c.giggle(1.6f);
            }
            LivingEntity v = c.held();
            if (v == null) return;
            if (k >= 16 && k < 44) {
                FpeUtil.hold(e, v, 0.95, 0.15, -0.1);
                FpeUtil.stun(v, 4);
            }
            if (k == 22 || k == 30 || k == 38) {
                v.invulnerableTime = 0;
                FpeUtil.hit(c, v, e.dmg(k == 38 ? 1.0f : 0.55f), 0, 0);
                c.bleed(v, 40);
                FpeUtil.particles(e, ParticleTypes.CRIT, v.position().add(0, v.getBbHeight() * 0.6, 0), 8, 0.2, 0.2, 0.2, 0.2);
                FpeUtil.sound(e, SoundEvents.TRIDENT_HIT, 1.1f, k == 38 ? 0.9f : 1.3f);
            }
            if (k == 44) {
                v.invulnerableTime = 0;
                FpeUtil.hit(c, v, e.dmg(0.4f), 0, 0);
                FpeUtil.fling(v, FpeUtil.forward(e), 1.3, 0.35);
                FpeUtil.daze(v, 60);
                FpeUtil.disarm(v);
                FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_KNOCKBACK, 1.2f, 0.9f);
                c.giggle(1.9f);
                c.victim = null;
            }
        }));
    }
}
