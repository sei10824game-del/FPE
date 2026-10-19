package com.fpe.entity.characters;

import java.util.ArrayList;
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
import net.minecraft.world.effect.MobEffect;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.Vec3;
import org.joml.Vector3f;

/**
 * Green Bloomie - FPE Green science teacher: spiky black hair, gas mask + goggles, lab coat, lime boots,
 * a GIANT syringe of green poison (left hand) and a grey briefcase (right hand).
 * Mostly melee (needle stabs / sweeps, briefcase bashes, heel kick) + toxic zone control (gas clouds that linger),
 * two sparse ranged moves (flask lob, needle spray); enraged = overdose ground injection + lethal_dose impale.
 * Every tick index below matches the key poses in tools/bbgen/chars/green_bloomie.py.
 */
public class GreenBloomie extends FpeEntity {
    private static final DustParticleOptions TOXIC = new DustParticleOptions(new Vector3f(0.55f, 1.0f, 0.23f), 1.4f);
    private static final DustParticleOptions TOXIC_BIG = new DustParticleOptions(new Vector3f(0.45f, 0.85f, 0.2f), 2.6f);
    private static final int GREEN_ARC = 0xD08CFF3A, GREY_ARC = 0xD0C8CCD2;

    /** lingering gas clouds: x, y, z, radius, ticks left, damage multiplier */
    private final List<double[]> clouds = new ArrayList<>();
    private boolean impaled;
    private Vec3 lobAt = Vec3.ZERO;

    public GreenBloomie(EntityType<? extends FpeEntity> type, Level level) { super(type, level); }

    @Override public Faction faction() { return Faction.GREEN_TEACHER; }

    public static AttributeSupplier.Builder attributes() { return baseAttributes(100, 7, 0.31, 3, 0.3); }

    @Override public double preferredDistance() { return 2.0; }
    @Override protected int restTicks() { return isEnraged() ? 8 : 16; }

    // ------------------------------------------------------------------ helpers
    static void arc(FpeEntity e, float radius, float sweep, float tilt, double y, int color) {
        FpeFx f = FpeUtil.fx(e, FpeFx.Kind.ARC, e.position().add(0, y, 0), 0, 7, radius, 0).param(sweep).color(color);
        f.setYRot(e.getYRot());
        f.setXRot(tilt);
    }

    static void dose(LivingEntity v, MobEffect eff, int ticks, int amp) {
        v.addEffect(new MobEffectInstance(eff, ticks, amp));
    }

    static void puff(FpeEntity e, Vec3 at, int n, double spread) {
        FpeUtil.particles(e, TOXIC, at, n, spread, spread * 0.6, spread, 0.02);
        FpeUtil.particles(e, ParticleTypes.SNEEZE, at, n / 3 + 1, spread, spread * 0.5, spread, 0.02);
    }

    /** hits that also poison */
    static void stab(FpeEntity e, double range, double half, float mult, double knock, double up, int poison, int amp) {
        Vec3 f = FpeUtil.forward(e);
        for (LivingEntity v : FpeUtil.enemiesInRadius(e, e.position(), range + 0.6, 2.5, 1.0)) {
            Vec3 d = new Vec3(v.getX() - e.getX(), 0, v.getZ() - e.getZ());
            if (d.lengthSqr() > 0.01 && Math.toDegrees(Math.acos(Mth.clamp(d.normalize().dot(f), -1, 1))) > half) continue;
            v.invulnerableTime = 0;
            if (FpeUtil.hit(e, v, e.dmg(mult), knock, up) && poison > 0) dose(v, MobEffects.POISON, poison, amp);
        }
    }

    static boolean inFront(FpeEntity e, LivingEntity t, double reach, double halfAngle) {
        Vec3 to = t.position().subtract(e.position());
        Vec3 flat = new Vec3(to.x, 0, to.z);
        if (flat.lengthSqr() < 1.0E-4) return true;
        double ang = Math.toDegrees(Math.acos(Mth.clamp(flat.normalize().dot(FpeUtil.forward(e)), -1, 1)));
        return e.distanceTo(t) < reach && ang < halfAngle && FpeUtil.canHurt(e, t);
    }

    void cloud(Vec3 at, double r, int life, double dmg) {
        if (clouds.size() < 6) clouds.add(new double[]{at.x, at.y, at.z, r, life, dmg});
        FpeUtil.sound(this, SoundEvents.FIRE_EXTINGUISH, 0.9f, 0.6f);
    }

    /** needle tip position (syringe held forward at chest height) */
    static Vec3 tip(FpeEntity e, double reach) {
        return FpeUtil.ahead(e, reach, 1.25).add(FpeUtil.right(e).scale(-0.25));
    }

    @Override
    public void tick() {
        super.tick();
        if (level().isClientSide || clouds.isEmpty()) return;
        clouds.removeIf(c -> {
            Vec3 at = new Vec3(c[0], c[1] + 0.5, c[2]);
            int left = (int) --c[4];
            if (left % 3 == 0) {
                FpeUtil.particles(this, TOXIC_BIG, at, (int) (c[3] * 4), c[3] * 0.55, 0.4, c[3] * 0.55, 0.01);
                FpeUtil.particles(this, ParticleTypes.SNEEZE, at, 2, c[3] * 0.5, 0.3, c[3] * 0.5, 0.01);
            }
            if (left % 10 == 0) {
                for (LivingEntity v : FpeUtil.enemiesInRadius(this, new Vec3(c[0], c[1], c[2]), c[3], 2.2, 0.8)) {
                    v.invulnerableTime = 0;
                    FpeUtil.hit(this, v, dmg((float) c[5]), 0, 0);
                    dose(v, MobEffects.POISON, 50, 0);
                    dose(v, MobEffects.MOVEMENT_SLOWDOWN, 30, 0);
                }
            }
            return left <= 0;
        });
    }

    // ------------------------------------------------------------------ abilities
    @Override
    protected void registerAbilities(List<Ability> out) {
        // 1. Needle jab: pulls the syringe back (0-6), lunging stab t9, retract
        out.add(Ability.of("needle_jab", 24, 40).range(0, 3.8).weight(4).faceUntil(7).tick((e, t, tk) -> {
            if (tk == 3) FpeUtil.sound(e, SoundEvents.GLASS_HIT, 0.8f, 1.6f);
            if (tk == 7) e.dashForward(0.3, 0);
            if (tk == 9) {
                stab(e, 3.7, 30, 1.0f, 0.3, 0.05, 60, 0);
                puff(e, tip(e, 2.8), 6, 0.2);
                FpeUtil.sound(e, SoundEvents.TRIDENT_HIT, 1f, 1.5f);
            }
        }));

        // 2. Needle sweep: winds the syringe across her body (0-10), wide backhand sweep t13
        out.add(Ability.of("needle_sweep", 30, 55).range(0, 4.0).weight(3).faceUntil(10).tick((e, t, tk) -> {
            if (tk == 11) e.dashForward(0.2, 0);
            if (tk == 13) {
                FpeUtil.hitCone(e, 4.0, 75, e.dmg(1.2f), 0.8, 0.2);
                arc(e, 3.4f, 150, 4, 1.1, GREEN_ARC);
                FpeUtil.arc(e, TOXIC, e.position().add(0, 1.1, 0), e.getYRot(), 70, 3.0, 16);
                FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_SWEEP, 1f, 0.8f);
            }
        }));

        // 3. Briefcase bash: swings the case back (0-9), rising uppercut swing t12 (launch + slow)
        out.add(Ability.of("case_bash", 28, 60).range(0, 3.2).weight(3).faceUntil(10).tick((e, t, tk) -> {
            if (tk == 10) e.dashForward(0.25, 0);
            if (tk == 12) {
                for (LivingEntity v : FpeUtil.enemiesInRadius(e, FpeUtil.ahead(e, 1.6, 0), 1.7, 2.5, 1))
                    if (FpeUtil.hit(e, v, e.dmg(1.3f), 1.1, 0.5)) dose(v, MobEffects.MOVEMENT_SLOWDOWN, 40, 1);
                arc(e, 2.4f, 110, 70, 1.0, GREY_ARC);
                FpeUtil.particles(e, ParticleTypes.CRIT, FpeUtil.ahead(e, 1.6, 1.4), 10, 0.3, 0.3, 0.3, 0.2);
                FpeUtil.sound(e, SoundEvents.ANVIL_PLACE, 0.6f, 1.6f);
            }
        }));

        // 4. Inoculate: two quick jabs t8 / t15, then drives the needle in and empties the plunger t26 (strong poison + weakness)
        out.add(Ability.of("inoculate", 44, 90).range(0, 3.4).weight(3).faceUntil(14).tick((e, t, tk) -> {
            if (tk == 6 || tk == 13 || tk == 23) e.dashForward(0.2, 0);
            if (tk == 8 || tk == 15) {
                stab(e, 3.5, 30, 0.55f, 0.1, 0, 0, 0);
                FpeUtil.sound(e, SoundEvents.TRIDENT_HIT, 0.8f, 1.7f);
            }
            if (tk == 26) {
                for (LivingEntity v : FpeUtil.enemiesInRadius(e, tip(e, 2.4), 1.5, 2.5, 1)) {
                    v.invulnerableTime = 0;
                    if (FpeUtil.hit(e, v, e.dmg(1.0f), 0, 0)) { dose(v, MobEffects.POISON, 100, 1); dose(v, MobEffects.WEAKNESS, 100, 0); }
                }
                FpeUtil.sound(e, SoundEvents.HONEY_BLOCK_SLIDE, 1.2f, 0.6f);
            }
            if (tk >= 26 && tk <= 32 && tk % 2 == 0) puff(e, tip(e, 2.4), 5, 0.3);
            if (tk == 32) FpeUtil.sound(e, SoundEvents.BOTTLE_EMPTY, 1f, 0.8f);
        }));

        // 5. Heel kick: raises the stiletto boot high (0-8), axe-kick chop down t11
        out.add(Ability.of("heel_kick", 26, 50).range(0, 3.0).weight(3).faceUntil(8).tick((e, t, tk) -> {
            if (tk == 9) e.dashForward(0.2, 0);
            if (tk == 11) {
                for (LivingEntity v : FpeUtil.enemiesInRadius(e, FpeUtil.ahead(e, 1.5, 0), 1.5, 2.5, 1))
                    if (FpeUtil.hit(e, v, e.dmg(1.15f), 0.5, -0.2)) dose(v, MobEffects.MOVEMENT_SLOWDOWN, 30, 2);
                FpeUtil.particles(e, ParticleTypes.CRIT, FpeUtil.ahead(e, 1.5, 0.3), 10, 0.3, 0.1, 0.3, 0.2);
                FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_STRONG, 1f, 1.1f);
            }
        }));

        // 6. Plunger slam: hoists the syringe overhead (0-14), slams the needle into the ground t18 (blast + gas puddle), yanks it out t26
        out.add(Ability.of("plunger_slam", 38, 90).range(1.0, 4.6).weight(2).faceUntil(14).tick((e, t, tk) -> {
            if (tk == 16) e.dashForward(0.2, 0);
            if (tk == 18) {
                Vec3 at = FpeUtil.ahead(e, 2.6, 0.05);
                FpeUtil.hitRadius(e, at, 1.8, e.dmg(1.5f), 0.5, 0.45);
                FpeUtil.hitLine(e, e.position().add(0, 1, 0), at.add(0, 1, 0), 0.5, e.dmg(0.5f), 0.2, 0.1);
                ((GreenBloomie) e).cloud(at, 2.2, 60, 0.3);
                puff(e, at, 20, 0.7);
                FpeUtil.particles(e, ParticleTypes.EXPLOSION, at, 1, 0, 0, 0, 0);
                FpeUtil.sound(e, SoundEvents.GLASS_BREAK, 1f, 0.6f);
                FpeUtil.sound(e, SoundEvents.GENERIC_EXPLODE, 0.6f, 1.4f);
            }
            if (tk == 26) FpeUtil.sound(e, SoundEvents.TRIDENT_RETURN, 0.8f, 1.2f);
        }));

        // 7. Lunge inject: crouches aiming (0-8), dashes t9, needle skewers along the path t12 + t14, skids to a stop
        out.add(Ability.of("lunge_inject", 34, 80).range(3.0, 9.0).weight(3).faceUntil(8).tick((e, t, tk) -> {
            if (tk == 9) { e.dashForward(1.15, 0.1); FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_SWEEP, 1f, 1.4f); }
            if (tk == 12 || tk == 14) {
                for (LivingEntity v : FpeUtil.enemiesInRadius(e, tip(e, 1.6), 1.4, 2.5, 1)) {
                    v.invulnerableTime = 0;
                    if (FpeUtil.hit(e, v, e.dmg(0.8f), 0.4, 0.1)) dose(v, MobEffects.POISON, 80, 0);
                }
                puff(e, tip(e, 1.8), 6, 0.2);
                if (tk == 12) FpeUtil.sound(e, SoundEvents.TRIDENT_HIT, 1f, 1.3f);
            }
            if (tk >= 15 && tk <= 20) FpeUtil.particles(e, ParticleTypes.CLOUD, e.position(), 2, 0.2, 0.05, 0.2, 0.02);
        }));

        // 8. Syringe spin: coils (0-6), whirls three full turns with syringe + case held out, hits t10 / t18 / t26, dizzy wobble
        out.add(Ability.of("syringe_spin", 36, 80).range(0, 3.6).weight(2).faceUntil(6).tick((e, t, tk) -> {
            if (tk == 10 || tk == 18 || tk == 26) {
                for (LivingEntity v : FpeUtil.enemiesInRadius(e, e.position(), 3.2, 2.5, 1)) {
                    v.invulnerableTime = 0;
                    if (FpeUtil.hit(e, v, e.dmg(0.7f), 0.6, 0.15)) dose(v, MobEffects.POISON, 40, 0);
                }
                FpeUtil.arc(e, TOXIC, e.position().add(0, 1.1, 0), 0, 180, 2.8, 24);
                FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_SWEEP, 1f, 0.9f + tk * 0.01f);
            }
        }));

        // 9. Gas vent: hunches and exhales through the respirator - pulses t12 / t20 / t28, leaves a lingering cloud around her
        out.add(Ability.of("gas_vent", 44, 140).range(0, 5.0).weight(2).blind().tick((e, t, tk) -> {
            if (tk == 6) FpeUtil.sound(e, SoundEvents.PLAYER_BREATH, 1f, 0.5f);
            if (tk == 12) ((GreenBloomie) e).cloud(e.position(), 3.4, 80, 0.35);
            if (tk == 12 || tk == 20 || tk == 28) {
                for (LivingEntity v : FpeUtil.enemiesInRadius(e, e.position(), 3.2, 2.5, 1)) {
                    v.invulnerableTime = 0;
                    if (FpeUtil.hit(e, v, e.dmg(0.3f), 0.25, 0)) {
                        dose(v, MobEffects.POISON, 60, 0);
                        if (tk == 28) dose(v, MobEffects.CONFUSION, 100, 0);
                    }
                }
                puff(e, FpeUtil.ahead(e, 1.2, 1.6), 30, 1.2);
                FpeUtil.sound(e, SoundEvents.FIRE_EXTINGUISH, 1f, 0.5f);
            }
        }));

        // 10. Flask lob (sparse ranged): swings the briefcase underhand, lid pops open t13, a poison flask flies out t14; puddle cloud on landing t30
        out.add(Ability.of("flask_lob", 34, 160).range(5.0, 14.0).weight(1).faceUntil(13).tick((e, t, tk) -> {
            GreenBloomie g = (GreenBloomie) e;
            if (tk == 13) FpeUtil.sound(e, SoundEvents.CHEST_OPEN, 0.8f, 1.6f);
            if (tk == 14) {
                Vec3 from = e.position().add(0, 1.3, 0).add(FpeUtil.right(e).scale(0.45)).add(FpeUtil.forward(e).scale(0.5));
                Vec3 to = t.position();
                double flight = 16, dx = to.x - from.x, dz = to.z - from.z;
                double vx = dx / (flight * 0.86), vz = dz / (flight * 0.86);
                double vy = 0.5 * FpeProjectile.Kind.BOMBLET.gravity * flight + (to.y - from.y) / flight;
                FpeUtil.projectile(e, FpeProjectile.Kind.BOMBLET, from, new Vec3(vx, vy, vz), e.dmg(0.8f));
                g.lobAt = to;
                FpeUtil.sound(e, SoundEvents.SPLASH_POTION_THROW, 1f, 0.7f);
            }
            if (tk == 30) {
                g.cloud(g.lobAt, 2.6, 80, 0.35);
                puff(e, g.lobAt.add(0, 0.3, 0), 20, 0.9);
                FpeUtil.sound(e, SoundEvents.SPLASH_POTION_BREAK, 1f, 0.8f);
            }
            if (tk == 20) FpeUtil.sound(e, SoundEvents.CHEST_CLOSE, 0.8f, 1.6f);
        }));

        // 11. Needle spray (sparse ranged): levels the syringe (0-10), squirts three jets of poison t14 / t18 / t22
        out.add(Ability.of("needle_spray", 34, 140).range(3.0, 8.0).weight(1).faceUntil(12).tick((e, t, tk) -> {
            if (tk == 8) FpeUtil.sound(e, SoundEvents.BREWING_STAND_BREW, 1f, 1.2f);
            if (tk == 14 || tk == 18 || tk == 22) {
                Vec3 a = tip(e, 2.6), b = a.add(FpeUtil.forward(e).scale(6.5)).add(0, -0.4, 0);
                for (LivingEntity v : FpeUtil.enemiesInRadius(e, e.position(), 9.5, 3, 2)) {
                    if (v.getBoundingBox().inflate(0.7).clip(a, b).isPresent()) {
                        v.invulnerableTime = 0;
                        if (FpeUtil.hit(e, v, e.dmg(0.5f), 0.15, 0)) dose(v, MobEffects.POISON, 60, 0);
                    }
                }
                for (int i = 0; i <= 12; i++) {
                    Vec3 p = a.lerp(b, i / 12.0).add(0, -0.15 * Math.pow(i / 6.0, 2), 0);
                    FpeUtil.particles(e, TOXIC, p, 2, 0.06, 0.06, 0.06, 0.01);
                }
                FpeUtil.particles(e, ParticleTypes.DRIPPING_HONEY, a, 2, 0.1, 0.1, 0.1, 0);
                FpeUtil.sound(e, SoundEvents.BUCKET_EMPTY, 1f, 1.5f);
            }
        }));

        // 12. Overdose (ENRAGED): stabs the syringe into the floor t16, hammers the plunger with the briefcase t22 / t28 / t34 -
        //     toxic shockwaves ripple out, the last one huge (poison II + nausea) and the ground keeps fuming
        out.add(Ability.of("overdose", 50, 160).range(0, 6.0).weight(3).when(FpeEntity::isEnraged).faceUntil(14).tick((e, t, tk) -> {
            Vec3 at = FpeUtil.ahead(e, 1.6, 0.05);
            if (tk == 16) {
                FpeUtil.hitRadius(e, at, 1.3, e.dmg(0.8f), 0.3, 0.3);
                puff(e, at, 10, 0.3);
                FpeUtil.sound(e, SoundEvents.TRIDENT_HIT_GROUND, 1.2f, 0.7f);
            }
            if (tk == 22 || tk == 28) {
                FpeUtil.fx(e, FpeFx.Kind.RING_SHOCK, at, 0, 10, tk == 22 ? 2.6f : 3.6f, e.dmg(0.5f));
                puff(e, at, 12, 0.5);
                FpeUtil.sound(e, SoundEvents.ANVIL_LAND, 0.5f, 1.6f);
            }
            if (tk == 34) {
                FpeUtil.fx(e, FpeFx.Kind.RING_SHOCK, at, 0, 14, 5.5f, e.dmg(0.6f));
                for (LivingEntity v : FpeUtil.enemiesInRadius(e, at, 4.5, 2.5, 1)) {
                    v.invulnerableTime = 0;
                    if (FpeUtil.hit(e, v, e.dmg(1.6f), 0.9, 0.4)) { dose(v, MobEffects.POISON, 120, 1); dose(v, MobEffects.CONFUSION, 80, 0); }
                }
                ((GreenBloomie) e).cloud(at, 4.0, 100, 0.4);
                puff(e, at.add(0, 0.5, 0), 40, 2.0);
                FpeUtil.particles(e, ParticleTypes.EXPLOSION_EMITTER, at, 1, 0, 0, 0, 0);
                FpeUtil.sound(e, SoundEvents.GENERIC_EXPLODE, 1f, 0.8f);
            }
            if (tk == 42) FpeUtil.sound(e, SoundEvents.TRIDENT_RETURN, 1f, 0.9f);
        }));

        // 13. Lethal dose (ENRAGED signature): dash t8, impales the target t12 and hoists it (12-30), slams the plunger home
        //     with the briefcase t30 (huge damage + wither + poison II), flings the body off the needle t40
        out.add(Ability.of("lethal_dose", 60, 220).range(0, 5.0).weight(3).when(FpeEntity::isEnraged).faceUntil(10)
                .start((e, t, tk) -> ((GreenBloomie) e).impaled = false).tick((e, t, tk) -> {
            GreenBloomie g = (GreenBloomie) e;
            if (tk == 2) FpeUtil.sound(e, SoundEvents.PLAYER_BREATH, 1f, 0.4f);
            if (tk == 8) e.dashForward(0.9, 0);
            if (tk == 12) {
                g.impaled = inFront(e, t, 3.4, 55);
                FpeUtil.sound(e, g.impaled ? SoundEvents.TRIDENT_HIT : SoundEvents.PLAYER_ATTACK_NODAMAGE, 1.2f, 0.7f);
                if (g.impaled) { FpeUtil.hit(e, t, e.dmg(0.5f), 0, 0); dose(t, MobEffects.POISON, 60, 0); }
            }
            if (g.impaled && tk > 12 && tk < 40) {
                double lift = Math.min(2.0, 0.6 + (tk - 12) * 0.08);
                Vec3 hold = FpeUtil.ahead(e, 2.0, lift).add(FpeUtil.right(e).scale(-0.3));
                t.setDeltaMovement(hold.subtract(t.position()).scale(0.5));
                t.hurtMarked = true;
                t.fallDistance = 0;
                if (tk % 4 == 0) puff(e, t.position().add(0, t.getBbHeight() * 0.5, 0), 4, 0.3);
            }
            if (tk == 30) {
                FpeUtil.sound(e, SoundEvents.ANVIL_LAND, 0.6f, 1.4f);
                FpeUtil.sound(e, SoundEvents.HONEY_BLOCK_SLIDE, 1.2f, 0.5f);
                if (g.impaled) {
                    t.invulnerableTime = 0;
                    FpeUtil.hit(e, t, e.dmg(2.0f), 0, 0);
                    dose(t, MobEffects.WITHER, 80, 0);
                    dose(t, MobEffects.POISON, 120, 1);
                    puff(e, t.position().add(0, t.getBbHeight() * 0.5, 0), 25, 0.6);
                }
            }
            if (tk == 40) {
                if (g.impaled) {
                    t.invulnerableTime = 0;
                    FpeUtil.hit(e, t, e.dmg(0.6f), 1.6, 0.6);
                }
                arc(e, 3.0f, 120, -30, 1.4, GREEN_ARC);
                FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_KNOCKBACK, 1.2f, 0.7f);
            }
        }));
    }

    @Override protected SoundEvent getAmbientSound() { return SoundEvents.PLAYER_BREATH; }
    @Override protected SoundEvent getHurtSound(DamageSource s) { return SoundEvents.WITCH_HURT; }
    @Override protected SoundEvent getDeathSound() { return SoundEvents.WITCH_DEATH; }
    @Override public int getAmbientSoundInterval() { return 200; }
}
