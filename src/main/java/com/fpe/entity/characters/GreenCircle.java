package com.fpe.entity.characters;

import java.util.List;

import com.fpe.entity.Ability;
import com.fpe.entity.FpeEntity;
import com.fpe.entity.FpeFx;
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
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.Vec3;
import org.joml.Vector3f;

/**
 * Green Circle - FPE Green lab teacher: huge spiky black mane, safety goggles, sharp-toothed grin, lab coat,
 * tall black boots and a green-acid sprayer canister with a hose. Melee focus: canister club, nozzle jabs,
 * mane whips, hose lash, kicks, bites; short-range acid spray, acid puddle/mortar zone control;
 * enraged: spinning toxic overdrive and hair spikes erupting from the floor.
 * Crowd control: grin_bite (hold + bite), hose_lasso (pull + choke + throw), specimen_pin (pin + face spray), glove_snatch (disarm + daze).
 * Every tick index below matches the key poses in tools/bbgen/chars/green_circle.py.
 */
public class GreenCircle extends FpeEntity {
    private static final DustParticleOptions ACID = new DustParticleOptions(new Vector3f(0.55f, 1.0f, 0.23f), 1.3f);
    private static final DustParticleOptions ACID_S = new DustParticleOptions(new Vector3f(0.75f, 1.0f, 0.5f), 0.8f);
    private static final int GREEN_ARC = 0xD08CFF3A, BLACK_ARC = 0xE0141218, WHITE_ARC = 0xD0F0F2F4;
    /** victim currently lassoed / choked / pinned / bitten (null = nobody) */
    private LivingEntity held;
    private Vec3 puddle, snag;

    public GreenCircle(EntityType<? extends FpeEntity> type, Level level) { super(type, level); }

    @Override public Faction faction() { return Faction.GREEN_TEACHER; }

    @Override public boolean meleeFocus() { return true; }

    public static AttributeSupplier.Builder attributes() { return baseAttributes(130, 8, 0.31, 4, 0.4); }

    @Override public double preferredDistance() { return 1.6; }
    @Override protected int restTicks() { return isEnraged() ? 8 : 14; }

    // ------------------------------------------------------------------ helpers
    static void arc(FpeEntity e, float radius, float sweep, float tilt, double y, int color) {
        FpeFx f = FpeUtil.fx(e, FpeFx.Kind.ARC, e.position().add(0, y, 0), 0, 7, radius, 0).param(sweep).color(color);
        f.setYRot(e.getYRot());
        f.setXRot(tilt);
    }

    static void acid(LivingEntity v, int ticks) {
        v.addEffect(new MobEffectInstance(MobEffects.POISON, ticks, 0));
    }

    static void puff(FpeEntity e, Vec3 at, int n, double spread) {
        FpeUtil.particles(e, ACID, at, n, spread, spread, spread, 0.02);
    }

    /** nozzle position: gun held in the left hand (entity's -right side), at chest height */
    static Vec3 nozzle(FpeEntity e, double reach) {
        return FpeUtil.ahead(e, reach, 1.5).add(FpeUtil.right(e).scale(-0.45));
    }

    static void sprayStream(FpeEntity e, double len) {
        Vec3 from = nozzle(e, 1.1), dir = FpeUtil.forward(e);
        for (int i = 0; i < 6; i++) {
            double d = len * i / 6.0;
            FpeUtil.particles(e, ACID, from.add(dir.scale(d)).add(0, -d * 0.08, 0), 2, 0.1 + d * 0.12, 0.1 + d * 0.08, 0.1 + d * 0.12, 0.01);
        }
        FpeUtil.particles(e, ACID_S, from, 3, 0.05, 0.05, 0.05, 0.08);
    }

    static boolean inFront(FpeEntity e, LivingEntity t, double reach, double halfAngle) {
        Vec3 to = t.position().subtract(e.position());
        Vec3 flat = new Vec3(to.x, 0, to.z);
        if (flat.lengthSqr() < 1.0E-4) return true;
        double ang = Math.toDegrees(Math.acos(Mth.clamp(flat.normalize().dot(FpeUtil.forward(e)), -1, 1)));
        return e.distanceTo(t) < reach && ang < halfAngle && FpeUtil.canHurt(e, t);
    }

    /** nearest valid enemy whose box crosses the segment (null if none) */
    static LivingEntity pickLine(FpeEntity e, Vec3 from, Vec3 to, double r) {
        LivingEntity best = null;
        double bd = Double.MAX_VALUE;
        for (LivingEntity v : e.level().getEntitiesOfClass(LivingEntity.class, new AABB(from, to).inflate(r + 1), x -> FpeUtil.canHurt(e, x))) {
            AABB bb = v.getBoundingBox().inflate(r);
            if (!bb.clip(from, to).isPresent() && !bb.contains(from)) continue;
            double d = v.distanceToSqr(e);
            if (d < bd) { bd = d; best = v; }
        }
        return best;
    }

    /** nearest valid enemy in a horizontal cone in front of her (null if none) */
    static LivingEntity pickCone(FpeEntity e, double reach, double halfAngle) {
        LivingEntity best = null;
        double bd = Double.MAX_VALUE;
        for (LivingEntity v : FpeUtil.enemiesInRadius(e, e.position(), reach, 2.5, 1)) {
            if (!inFront(e, v, reach + v.getBbWidth() * 0.5 + 0.4, halfAngle)) continue;
            double d = v.distanceToSqr(e);
            if (d < bd) { bd = d; best = v; }
        }
        return best;
    }

    /** grab still valid? drops the victim when it died / became invalid (creative, ally, removed) or got far away */
    boolean grabbing() {
        if (held != null && (!FpeUtil.canHurt(this, held) || held.distanceTo(this) > 12)) held = null;
        return held != null;
    }

    /** hose particles from her right glove to a point */
    static void hoseLine(FpeEntity e, Vec3 to) {
        Vec3 from = FpeUtil.ahead(e, 0.4, 1.6).add(FpeUtil.right(e).scale(0.45));
        for (int i = 1; i <= 7; i++) FpeUtil.particles(e, ParticleTypes.CRIT, from.lerp(to, i / 8.0), 1, 0, 0, 0, 0);
    }

    // ------------------------------------------------------------------ abilities
    @Override
    protected void registerAbilities(List<Ability> out) {
        // 1. Canister bash: sideways club swing t9, two-handed overhead slam t18 (stagger)
        out.add(Ability.of("canister_bash", 34, 45).range(0, 3.6).weight(4).faceUntil(16).tick((e, t, tk) -> {
            if (tk == 7 || tk == 16) e.dashForward(0.25, 0);
            if (tk == 9) {
                FpeUtil.hitCone(e, 3.3, 80, e.dmg(0.9f), 0.9, 0.2);
                arc(e, 2.6f, 140, -12, 1.4, WHITE_ARC);
                FpeUtil.sound(e, SoundEvents.ANVIL_PLACE, 0.5f, 1.6f);
                FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_SWEEP, 0.8f, 0.9f);
            }
            if (tk == 18) {
                t.invulnerableTime = 0;
                Vec3 at = FpeUtil.ahead(e, 1.7, 0.05);
                FpeUtil.hitRadius(e, at, 1.7, e.dmg(1.4f), 0.4, 0.3);
                for (LivingEntity v : FpeUtil.enemiesInRadius(e, at, 1.9, 2.5, 1))
                    v.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 30, 2));
                arc(e, 2.4f, 90, 85, 1.0, WHITE_ARC);
                puff(e, at.add(0, 0.3, 0), 10, 0.4);
                FpeUtil.particles(e, ParticleTypes.CRIT, at.add(0, 0.4, 0), 12, 0.5, 0.2, 0.5, 0.25);
                FpeUtil.sound(e, SoundEvents.ANVIL_LAND, 0.7f, 0.9f);
            }
        }));

        // 2. Nozzle jab: cocks back, rapier thrust with the nozzle t7 + acid squirt
        out.add(Ability.of("nozzle_jab", 22, 30).range(0, 4.2).weight(4).faceUntil(6).tick((e, t, tk) -> {
            if (tk == 6) e.dashForward(0.45, 0);
            if (tk == 7) {
                Vec3 from = e.position().add(0, 1.4, 0);
                if (FpeUtil.hitLine(e, from, from.add(FpeUtil.forward(e).scale(3.8)), 0.8, e.dmg(1.0f), 0.6, 0.1) > 0) {
                    if (inFront(e, t, 4.2, 40)) acid(t, 50);
                }
                puff(e, nozzle(e, 2.6), 8, 0.2);
                FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_CRIT, 1f, 1.2f);
                FpeUtil.sound(e, SoundEvents.SLIME_SQUISH_SMALL, 1f, 1.4f);
            }
        }));

        // 3. Acid spray: braces and hoses a sweeping acid cone t10-t28 (poison, hits every 3 ticks)
        out.add(Ability.of("acid_spray", 40, 90).range(0, 5.5).weight(3).faceUntil(28).tick((e, t, tk) -> {
            if (tk == 6) FpeUtil.sound(e, SoundEvents.BREWING_STAND_BREW, 1f, 1.4f);
            if (tk >= 10 && tk <= 28) {
                sprayStream(e, 4.8);
                if (tk % 2 == 0) FpeUtil.sound(e, SoundEvents.FIRE_EXTINGUISH, 0.5f, 1.6f);
                if ((tk - 10) % 3 == 0) {
                    for (LivingEntity v : FpeUtil.enemiesInRadius(e, FpeUtil.ahead(e, 2.6, 0), 2.6, 2.5, 1)) {
                        if (!inFront(e, v, 5.5, 40)) continue;
                        v.invulnerableTime = 0;
                        if (FpeUtil.hit(e, v, e.dmg(0.3f), 0.15, 0.02)) acid(v, 60);
                    }
                }
            }
        }));

        // 4. Hair lash: coils low then spins 360 at t9-t15, the spiked mane whips everything around (t12)
        out.add(Ability.of("hair_lash", 32, 70).range(0, 3.8).weight(3).faceUntil(8).tick((e, t, tk) -> {
            if (tk == 5) FpeUtil.sound(e, SoundEvents.WOOL_PLACE, 1.2f, 0.6f);
            if (tk == 12) {
                FpeUtil.hitRadius(e, e.position().add(0, 1.0, 0), 3.7, e.dmg(1.2f), 1.1, 0.3);
                arc(e, 3.4f, 360, 0, 1.6, BLACK_ARC);
                arc(e, 3.0f, 360, 6, 0.9, BLACK_ARC);
                FpeUtil.particles(e, ParticleTypes.SQUID_INK, e.position().add(0, 1.4, 0), 14, 1.5, 0.4, 1.5, 0.02);
                FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_SWEEP, 1.2f, 0.6f);
            }
        }));

        // 5. Hose whip: grabs the hose, windmills it overhead and cracks it t12 (long line), yanks victims in t18
        out.add(Ability.of("hose_whip", 30, 70).range(2.5, 6.5).weight(3).faceUntil(11).tick((e, t, tk) -> {
            if (tk == 6) FpeUtil.sound(e, SoundEvents.FISHING_BOBBER_THROW, 1f, 0.6f);
            if (tk == 12) {
                Vec3 from = e.position().add(0, 1.2, 0);
                Vec3 to = from.add(FpeUtil.forward(e).scale(6.0));
                FpeUtil.hitLine(e, from, to, 0.9, e.dmg(1.0f), 0.1, 0.1);
                for (int i = 1; i <= 8; i++) FpeUtil.particles(e, ParticleTypes.CRIT, from.add(FpeUtil.forward(e).scale(i * 0.75)), 1, 0.05, 0.05, 0.05, 0.05);
                FpeUtil.sound(e, SoundEvents.FISHING_BOBBER_RETRIEVE, 1.2f, 0.6f);
                FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_STRONG, 1f, 1.3f);
            }
            if (tk == 18) {
                Vec3 from = e.position().add(0, 1.2, 0);
                for (LivingEntity v : FpeUtil.enemiesInRadius(e, FpeUtil.ahead(e, 3.5, 0), 3.0, 2.5, 1)) {
                    if (!inFront(e, v, 6.8, 30)) continue;
                    Vec3 pull = from.subtract(v.position()).normalize().scale(0.9);
                    v.setDeltaMovement(pull.x, 0.25, pull.z);
                    v.hurtMarked = true;
                    v.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 25, 2));
                }
                FpeUtil.sound(e, SoundEvents.LEASH_KNOT_BREAK, 1f, 0.8f);
            }
        }));

        // 6. Boot kick: knee chamber, pointed-boot push kick t9 (huge knockback), hops back
        out.add(Ability.of("boot_kick", 26, 50).range(0, 3.0).weight(3).faceUntil(8).tick((e, t, tk) -> {
            if (tk == 9) {
                FpeUtil.hitCone(e, 3.0, 45, e.dmg(1.1f), 2.0, 0.35);
                FpeUtil.particles(e, ParticleTypes.CRIT, FpeUtil.ahead(e, 1.5, 0.9), 8, 0.3, 0.2, 0.3, 0.2);
                FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_KNOCKBACK, 1f, 0.8f);
            }
            if (tk == 15) e.dashForward(-0.3, 0.15);
        }));

        // 7. Lab lunge: sinks low, dashes in t9, nozzle stab t12, rising canister uppercut t20 (launch)
        out.add(Ability.of("lab_lunge", 36, 80).range(2.5, 8).weight(3).faceUntil(9).tick((e, t, tk) -> {
            if (tk == 3) FpeUtil.sound(e, SoundEvents.WITCH_CELEBRATE, 1f, 0.7f);
            if (tk == 9) e.dashToward(t.position(), Math.min(1.4, 0.4 + e.distanceTo(t) * 0.16), 0.05);
            if (tk > 9 && tk < 14) FpeUtil.particles(e, ParticleTypes.CLOUD, e.position().add(0, 0.1, 0), 2, 0.2, 0.05, 0.2, 0.01);
            if (tk == 12) {
                if (FpeUtil.hitCone(e, 2.8, 40, e.dmg(1.0f), 0.1, 0) > 0 && inFront(e, t, 3, 45)) acid(t, 40);
                FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_CRIT, 1f, 1.0f);
            }
            if (tk == 14) e.setDeltaMovement(e.getDeltaMovement().scale(0.2));
            if (tk == 20) {
                t.invulnerableTime = 0;
                FpeUtil.hitCone(e, 2.8, 60, e.dmg(1.3f), 0.3, 1.0);
                arc(e, 2.5f, 110, -80, 1.0, WHITE_ARC);
                FpeUtil.sound(e, SoundEvents.ANVIL_PLACE, 0.6f, 1.3f);
            }
        }));

        // 8. Acid puddle: sprays the ground under the target t8-t20, the corrosive pool bursts at t30 (trap) and poisons
        out.add(Ability.of("acid_puddle", 36, 110).range(2, 9).weight(2).faceUntil(14).tick((e, t, tk) -> {
            GreenCircle g = (GreenCircle) e;
            if (tk >= 8 && tk <= 20) {
                Vec3 to = t.position();
                Vec3 from = nozzle(e, 1.0);
                for (int i = 1; i <= 4; i++) FpeUtil.particles(e, ACID, from.add(to.subtract(from).scale(i / 4.0)), 2, 0.1, 0.1, 0.1, 0.01);
                if (tk % 3 == 0) FpeUtil.sound(e, SoundEvents.FIRE_EXTINGUISH, 0.6f, 1.4f);
            }
            if (tk == 14) {
                g.puddle = t.position();
                FpeUtil.fx(e, FpeFx.Kind.RING_TRAP, g.puddle, 16, 22, 2.4f, e.dmg(1.2f)).color(0xC08CFF3A);
            }
            if (g.puddle != null && tk > 14) {
                if (tk % 2 == 0) FpeUtil.particles(e, ACID, g.puddle.add(0, 0.1, 0), 4, 1.0, 0.05, 1.0, 0.01);
                if (tk == 30) {
                    for (LivingEntity v : FpeUtil.enemiesInRadius(e, g.puddle, 2.6, 2, 1)) {
                        acid(v, 100);
                        v.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 60, 1));
                    }
                    puff(e, g.puddle.add(0, 0.4, 0), 30, 1.0);
                    FpeUtil.sound(e, SoundEvents.GENERIC_EXTINGUISH_FIRE, 1f, 0.6f);
                }
            }
        }).end((e, t, tk) -> ((GreenCircle) e).puddle = null));

        // 9. Goggle charge: snaps the goggles down t4-8, lowers the spiked crown and rams t16 + t20
        out.add(Ability.of("goggle_charge", 38, 90).range(3, 10).weight(3).faceUntil(12).tick((e, t, tk) -> {
            if (tk == 6) FpeUtil.sound(e, SoundEvents.ARMOR_EQUIP_IRON, 1f, 1.3f);
            if (tk == 12) {
                e.dashToward(t.position(), Math.min(1.5, 0.5 + e.distanceTo(t) * 0.15), 0.05);
                FpeUtil.sound(e, SoundEvents.RAVAGER_ROAR, 0.5f, 1.6f);
            }
            if (tk > 12 && tk < 22) FpeUtil.particles(e, ParticleTypes.CLOUD, e.position().add(0, 0.1, 0), 2, 0.2, 0.05, 0.2, 0.01);
            if (tk == 16 || tk == 20) {
                t.invulnerableTime = 0;
                if (FpeUtil.hitCone(e, 2.4, 60, e.dmg(tk == 16 ? 0.9f : 1.2f), tk == 16 ? 0.3 : 1.5, tk == 16 ? 0.15 : 0.5) > 0)
                    FpeUtil.sound(e, SoundEvents.GOAT_RAM_IMPACT, 1.2f, 0.8f);
            }
            if (tk == 22) e.setDeltaMovement(e.getDeltaMovement().scale(0.2));
        }));

        // 10. Grin bite (CC grab): glove grab t10, holds the victim at her teeth (stunned), chomps t20 + t28 (drains), shoves t34
        out.add(Ability.of("grin_bite", 40, 130).range(0, 3.4).weight(2).faceUntil(10)
                .start((e, t, tk) -> ((GreenCircle) e).held = null).tick((e, t, tk) -> {
            GreenCircle g = (GreenCircle) e;
            if (tk == 8) e.dashForward(0.45, 0);
            if (tk == 10) {
                LivingEntity v = pickCone(e, 3.0, 55);
                if (v != null && FpeUtil.hit(e, v, e.dmg(0.3f), 0, 0)) g.held = v;
                FpeUtil.sound(e, g.held != null ? SoundEvents.ARMOR_EQUIP_LEATHER : SoundEvents.PLAYER_ATTACK_NODAMAGE, 1f, 0.7f);
            }
            if (tk > 10 && tk < 34 && g.grabbing()) {
                FpeUtil.hold(e, g.held, 0.95, 0.45, 0);
                if (tk % 5 == 1) FpeUtil.stun(g.held, 6);
                if (tk == 20 || tk == 28) {
                    g.held.invulnerableTime = 0;
                    if (FpeUtil.hit(e, g.held, e.dmg(0.9f), 0, 0)) e.heal(e.dmg(0.4f));
                    FpeUtil.particles(e, ParticleTypes.DAMAGE_INDICATOR, g.held.position().add(0, 1.4, 0), 5, 0.3, 0.3, 0.3, 0.1);
                    FpeUtil.sound(e, SoundEvents.EVOKER_FANGS_ATTACK, 1f, 1.3f);
                }
            }
            if (tk == 34) {
                if (g.grabbing()) {
                    g.held.invulnerableTime = 0;
                    FpeUtil.hit(e, g.held, e.dmg(0.6f), 1.6, 0.4);
                } else FpeUtil.hitCone(e, 2.5, 50, e.dmg(0.6f), 1.2, 0.3);
                FpeUtil.sound(e, SoundEvents.WITCH_CELEBRATE, 1f, 1.1f);
                g.held = null;
            }
        }).end((e, t, tk) -> ((GreenCircle) e).held = null));

        // 11. Acid mortar: points the sprayer skyward, pumps it and lobs 3 acid globs t12/t16/t20 that splash down on the target area
        out.add(Ability.of("acid_mortar", 40, 120).range(5, 16).weight(2).tick((e, t, tk) -> {
            if (tk == 4) FpeUtil.sound(e, SoundEvents.BREWING_STAND_BREW, 1f, 0.8f);
            if (tk == 12 || tk == 16 || tk == 20) {
                int i = (tk - 12) / 4;
                Vec3 lead = t.getDeltaMovement().scale(10);
                Vec3 at = t.position().add(lead.x, 0, lead.z).add(FpeUtil.right(e).scale((i - 1) * 1.6)).add(FpeUtil.forward(e).scale(i == 1 ? 0.8 : -0.4));
                FpeUtil.fx(e, FpeFx.Kind.RING_TRAP, at, 14, 18, 1.8f, e.dmg(1.0f)).color(0xC08CFF3A);
                puff(e, e.position().add(0, 3.0, 0), 10, 0.2);
                FpeUtil.particles(e, ParticleTypes.ITEM_SLIME, e.position().add(0, 3.0, 0), 8, 0.2, 0.3, 0.2, 0.2);
                FpeUtil.sound(e, SoundEvents.SLIME_JUMP, 1.2f, 0.7f);
            }
        }));

        // 12. Toxic overdrive (enraged): goggles down, spins twice spraying acid all around t14-t38 (hit every 4t),
        //     then crashes the canister down t46 -> toxic shockwave
        out.add(Ability.of("toxic_overdrive", 56, 200).range(0, 5).weight(3).when(FpeEntity::isEnraged).faceUntil(10).tick((e, t, tk) -> {
            if (tk == 1) FpeUtil.sound(e, SoundEvents.WITCH_CELEBRATE, 1.4f, 0.7f);
            if (tk >= 14 && tk <= 38) {
                float yaw = e.getYRot() + (tk - 14) * 30f;
                Vec3 d = Vec3.directionFromRotation(0, yaw);
                for (int i = 1; i <= 4; i++) FpeUtil.particles(e, ACID, e.position().add(0, 1.3, 0).add(d.scale(i * 0.9)), 2, 0.15, 0.15, 0.15, 0.01);
                if (tk % 2 == 0) FpeUtil.sound(e, SoundEvents.FIRE_EXTINGUISH, 0.5f, 1.5f);
                if ((tk - 14) % 4 == 0) {
                    for (LivingEntity v : FpeUtil.enemiesInRadius(e, e.position(), 4.2, 2.5, 1)) {
                        v.invulnerableTime = 0;
                        if (FpeUtil.hit(e, v, e.dmg(0.45f), 0.3, 0.05)) acid(v, 60);
                    }
                }
            }
            if (tk == 46) {
                Vec3 at = FpeUtil.ahead(e, 1.4, 0.05);
                FpeUtil.hitRadius(e, at, 2.6, e.dmg(1.6f), 0.9, 0.5);
                for (LivingEntity v : FpeUtil.enemiesInRadius(e, at, 3.0, 2.5, 1)) acid(v, 80);
                FpeUtil.fx(e, FpeFx.Kind.RING_SHOCK, at, 0, 14, 4.0f, e.dmg(0.6f)).color(0xC08CFF3A);
                puff(e, at.add(0, 0.3, 0), 30, 0.9);
                FpeUtil.particles(e, ParticleTypes.EXPLOSION, at, 1, 0, 0, 0, 0);
                FpeUtil.sound(e, SoundEvents.ANVIL_LAND, 1f, 0.6f);
                FpeUtil.sound(e, SoundEvents.GENERIC_EXPLODE, 0.6f, 1.3f);
            }
        }));

        // 13. Hair eruption (enraged signature): flips the mane over her head into the floor t12 ->
        //     black hair spikes race toward the target t14-t28, a ring of spikes when she rips it out t32
        out.add(Ability.of("hair_eruption", 44, 180).range(2, 12).weight(3).when(FpeEntity::isEnraged).faceUntil(12).tick((e, t, tk) -> {
            if (tk == 4) FpeUtil.sound(e, SoundEvents.WITCH_CELEBRATE, 1.2f, 0.6f);
            if (tk == 12) {
                FpeUtil.particles(e, ParticleTypes.SQUID_INK, FpeUtil.ahead(e, 1.2, 0.1), 14, 0.5, 0.1, 0.5, 0.05);
                FpeUtil.sound(e, SoundEvents.ROOTED_DIRT_BREAK, 1.4f, 0.6f);
            }
            if (tk >= 14 && tk <= 28 && tk % 2 == 0) {
                int i = (tk - 14) / 2;
                Vec3 at = FpeUtil.ahead(e, 1.6 + i * 1.3, 0);
                FpeUtil.fx(e, FpeFx.Kind.SPIKE, at, 2, 22, 1.0f, e.dmg(1.1f)).param(1.0f + i * 0.08f);
                if (i % 2 == 0) {
                    Vec3 side = FpeUtil.right(e).scale(1.1);
                    FpeUtil.fx(e, FpeFx.Kind.SPIKE, at.add(side), 3, 20, 0.8f, e.dmg(0.8f)).param(0.7f);
                    FpeUtil.fx(e, FpeFx.Kind.SPIKE, at.subtract(side), 3, 20, 0.8f, e.dmg(0.8f)).param(0.7f);
                }
            }
            if (tk == 32) {
                for (int i = 0; i < 8; i++) {
                    Vec3 d = Vec3.directionFromRotation(0, e.getYRot() + i * 45);
                    FpeUtil.fx(e, FpeFx.Kind.SPIKE, e.position().add(d.scale(2.2)), 2, 18, 1.0f, e.dmg(0.9f)).param(0.9f);
                }
                FpeUtil.sound(e, SoundEvents.EVOKER_FANGS_ATTACK, 1.2f, 0.8f);
            }
        }));

        // 14. Hose lasso (CC grab): windmills the hose overhead t2-t9, casts it t10 (line 9.5), reels the snared victim in
        //     hand-over-hand t11-t20 (yanks t12/t15/t18), chokes it with the hose, lifted in front of her t21-t45
        //     (stunned, squeezes t26/t33/t40, dazed t33), hoists it t46-49 and hurls it away t50
        out.add(Ability.of("hose_lasso", 64, 170).range(3.5, 9.5).weight(2).faceUntil(10)
                .start((e, t, tk) -> ((GreenCircle) e).held = null).tick((e, t, tk) -> {
            GreenCircle g = (GreenCircle) e;
            if (tk == 2 || tk == 6) FpeUtil.sound(e, SoundEvents.FISHING_BOBBER_THROW, 1f, 0.5f);
            if (tk == 10) {
                Vec3 from = e.position().add(0, 1.4, 0);
                Vec3 to = from.add(FpeUtil.forward(e).scale(9.5));
                LivingEntity v = pickLine(e, from, to, 0.6);
                if (v != null && FpeUtil.hit(e, v, e.dmg(0.5f), 0, 0)) {
                    g.held = v;
                    g.snag = v.position();
                    FpeUtil.root(v, 12);
                    FpeUtil.sound(e, SoundEvents.LEASH_KNOT_PLACE, 1.2f, 0.7f);
                    hoseLine(e, v.position().add(0, v.getBbHeight() * 0.7, 0));
                } else {
                    for (int i = 1; i <= 9; i++) FpeUtil.particles(e, ParticleTypes.CRIT, from.add(FpeUtil.forward(e).scale(i)), 1, 0.05, 0.05, 0.05, 0.02);
                    FpeUtil.sound(e, SoundEvents.FISHING_BOBBER_RETRIEVE, 1f, 0.7f);
                }
            }
            if (tk > 10 && tk <= 20 && g.grabbing()) {
                float k = Mth.clamp((tk - 10) / 10f, 0, 1);
                k = k * k * (3 - 2 * k);
                FpeUtil.holdAt(g.held, g.snag.lerp(FpeUtil.ahead(e, 1.0, 0.3), k));
                hoseLine(e, g.held.position().add(0, g.held.getBbHeight() * 0.7, 0));
                if (tk == 12 || tk == 15 || tk == 18) FpeUtil.sound(e, SoundEvents.LEASH_KNOT_BREAK, 1f, 0.7f + tk * 0.02f);
            }
            if (tk > 20 && tk <= 45 && g.grabbing()) {
                FpeUtil.hold(e, g.held, 0.95, tk >= 24 ? 0.65 : 0.5, 0);
                if (tk % 5 == 1) FpeUtil.stun(g.held, 7);
                if (tk == 26 || tk == 33 || tk == 40) {
                    g.held.invulnerableTime = 0;
                    FpeUtil.hit(e, g.held, e.dmg(0.3f), 0, 0);
                    if (tk == 33) FpeUtil.daze(g.held, 50);
                    FpeUtil.particles(e, ParticleTypes.DAMAGE_INDICATOR, g.held.position().add(0, g.held.getBbHeight(), 0), 4, 0.2, 0.2, 0.2, 0.05);
                    FpeUtil.sound(e, SoundEvents.PLAYER_HURT_SWEET_BERRY_BUSH, 1f, 0.6f);
                }
                if (tk == 30) FpeUtil.sound(e, SoundEvents.WITCH_CELEBRATE, 1f, 0.8f);
            }
            if (tk > 45 && tk < 50 && g.grabbing()) FpeUtil.hold(e, g.held, 0.7, 1.0, -0.4);
            if (tk == 50 && g.grabbing()) {
                g.held.invulnerableTime = 0;
                FpeUtil.hit(e, g.held, e.dmg(0.8f), 1.7, 0.55);
                FpeUtil.stun(g.held, 15);
                arc(e, 2.6f, 160, -20, 1.6, WHITE_ARC);
                FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_KNOCKBACK, 1.2f, 0.7f);
            }
            if (tk >= 50) g.held = null;
        }).end((e, t, tk) -> ((GreenCircle) e).held = null));

        // 15. Specimen pin (CC grab): low leg reap + glove shove t7 drops the victim, boot stomp pins it t12-t38 (stunned),
        //     sprays acid in its face t18-t34 (daze t20 + poison), punts it away t42
        out.add(Ability.of("specimen_pin", 52, 150).range(0, 3.2).weight(2).faceUntil(7)
                .start((e, t, tk) -> ((GreenCircle) e).held = null).tick((e, t, tk) -> {
            GreenCircle g = (GreenCircle) e;
            if (tk == 5) e.dashForward(0.35, 0);
            if (tk == 7) {
                LivingEntity v = pickCone(e, 3.0, 50);
                if (v != null && FpeUtil.hit(e, v, e.dmg(0.4f), 0, 0)) {
                    g.held = v;
                    FpeUtil.stun(v, 8);
                    FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_SWEEP, 1f, 0.7f);
                } else FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_NODAMAGE, 1f, 0.8f);
            }
            if (tk > 7 && tk <= 38 && g.grabbing()) {
                FpeUtil.hold(e, g.held, 1.35, 0, 0.2);
                if (tk % 5 == 2) FpeUtil.stun(g.held, 7);
                if (tk == 12) {
                    g.held.invulnerableTime = 0;
                    FpeUtil.hit(e, g.held, e.dmg(0.6f), 0, 0);
                    FpeUtil.particles(e, ParticleTypes.CRIT, g.held.position().add(0, 0.5, 0), 10, 0.3, 0.2, 0.3, 0.2);
                    FpeUtil.particles(e, ParticleTypes.CLOUD, g.held.position().add(0, 0.1, 0), 6, 0.4, 0.05, 0.4, 0.02);
                    FpeUtil.sound(e, SoundEvents.ANVIL_LAND, 0.6f, 1.2f);
                }
                if (tk >= 18 && tk <= 34) {
                    Vec3 face = g.held.position().add(0, g.held.getBbHeight() * 0.8, 0);
                    Vec3 from = nozzle(e, 0.9);
                    for (int i = 1; i <= 3; i++) FpeUtil.particles(e, ACID, from.lerp(face, i / 3.0), 2, 0.08, 0.08, 0.08, 0.01);
                    if (tk % 2 == 0) FpeUtil.sound(e, SoundEvents.FIRE_EXTINGUISH, 0.5f, 1.6f);
                    if (tk % 4 == 2) {
                        g.held.invulnerableTime = 0;
                        if (FpeUtil.hit(e, g.held, e.dmg(0.12f), 0, 0)) acid(g.held, 60);
                    }
                    if (tk == 20) FpeUtil.daze(g.held, 60);
                }
            }
            if (tk == 42) {
                if (g.grabbing()) {
                    g.held.invulnerableTime = 0;
                    FpeUtil.hit(e, g.held, e.dmg(0.7f), 1.9, 0.45);
                } else FpeUtil.hitCone(e, 2.6, 45, e.dmg(0.7f), 1.5, 0.3);
                FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_KNOCKBACK, 1f, 0.8f);
                g.held = null;
            }
        }).end((e, t, tk) -> ((GreenCircle) e).held = null));

        // 16. Glove snatch (CC disarm): nozzle feint t3, the free glove snatches the weapon out of the victim's hand t7
        //     (disarm + weakness), squirts it in the eyes t12 (daze), tosses the loot over her shoulder and backhands t17
        out.add(Ability.of("glove_snatch", 30, 140).range(0, 3.2).weight(2).faceUntil(12)
                .start((e, t, tk) -> ((GreenCircle) e).held = null).tick((e, t, tk) -> {
            GreenCircle g = (GreenCircle) e;
            if (tk == 5) e.dashForward(0.3, 0);
            if (tk == 7) {
                LivingEntity v = pickCone(e, 3.0, 50);
                if (v != null && FpeUtil.hit(e, v, e.dmg(0.4f), 0, 0)) {
                    g.held = v;
                    FpeUtil.disarm(v);
                    v.addEffect(new MobEffectInstance(MobEffects.WEAKNESS, 80, 0));
                    FpeUtil.sound(e, SoundEvents.ITEM_PICKUP, 1.2f, 0.6f);
                } else FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_NODAMAGE, 1f, 0.8f);
            }
            if (tk == 12) {
                puff(e, nozzle(e, 1.6), 10, 0.25);
                if (g.grabbing() && inFront(e, g.held, 3.6, 60)) {
                    FpeUtil.daze(g.held, 50);
                    acid(g.held, 40);
                }
                FpeUtil.sound(e, SoundEvents.SLIME_SQUISH_SMALL, 1f, 1.5f);
            }
            if (tk == 17) {
                if (FpeUtil.hitCone(e, 2.8, 60, e.dmg(0.6f), 0.9, 0.2) > 0) FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_STRONG, 1f, 1.2f);
                arc(e, 2.2f, 120, 10, 1.5, WHITE_ARC);
                g.held = null;
            }
        }).end((e, t, tk) -> ((GreenCircle) e).held = null));
    }

    // ------------------------------------------------------------------ sounds
    @Override protected SoundEvent getAmbientSound() { return SoundEvents.WITCH_AMBIENT; }
    @Override protected SoundEvent getHurtSound(DamageSource s) { return SoundEvents.WITCH_HURT; }
    @Override protected SoundEvent getDeathSound() { return SoundEvents.WITCH_DEATH; }
    @Override public int getAmbientSoundInterval() { return 220; }
}
