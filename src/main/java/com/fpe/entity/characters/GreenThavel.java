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
import net.minecraft.world.phys.Vec3;
import org.joml.Vector3f;

/**
 * Green Thavel - FPE Green lab teacher: white antlers, goggles, lab coat, BIG green gloves holding clipboards.
 * Pure melee: clipboard slaps/chops, glove punches and grabs, antler charge, boot stomps; enraged = toxic gloves.
 * Every tick index below matches the key poses in tools/bbgen/chars/green_thavel.py.
 */
public class GreenThavel extends FpeEntity {
    private static final DustParticleOptions TOXIC = new DustParticleOptions(new Vector3f(0.55f, 1.0f, 0.23f), 1.2f);
    private static final int GREEN_ARC = 0xD08CFF3A, WHITE_ARC = 0xD0F4F4F0;
    private boolean grabbed;

    public GreenThavel(EntityType<? extends FpeEntity> type, Level level) { super(type, level); }

    @Override public Faction faction() { return Faction.GREEN_TEACHER; }

    @Override public boolean meleeFocus() { return true; }

    public static AttributeSupplier.Builder attributes() { return baseAttributes(110, 7, 0.31, 4, 0.3); }

    @Override public double preferredDistance() { return 1.6; }
    @Override protected int restTicks() { return isEnraged() ? 8 : 16; }

    // ------------------------------------------------------------------ helpers
    static void arc(FpeEntity e, float radius, float sweep, float tilt, double y, int color) {
        FpeFx f = FpeUtil.fx(e, FpeFx.Kind.ARC, e.position().add(0, y, 0), 0, 7, radius, 0).param(sweep).color(color);
        f.setYRot(e.getYRot());
        f.setXRot(tilt);
    }

    static void poison(LivingEntity v, int ticks) {
        v.addEffect(new MobEffectInstance(MobEffects.POISON, ticks, 0));
    }

    static void toxicPuff(FpeEntity e, Vec3 at, int n) {
        FpeUtil.particles(e, TOXIC, at, n, 0.4, 0.4, 0.4, 0.02);
    }

    /** in front of the entity, within reach and angle */
    static boolean inFront(FpeEntity e, LivingEntity t, double reach, double halfAngle) {
        Vec3 to = t.position().subtract(e.position());
        Vec3 flat = new Vec3(to.x, 0, to.z);
        if (flat.lengthSqr() < 1.0E-4) return true;
        double ang = Math.toDegrees(Math.acos(Mth.clamp(flat.normalize().dot(FpeUtil.forward(e)), -1, 1)));
        return e.distanceTo(t) < reach && ang < halfAngle && FpeUtil.canHurt(e, t);
    }

    // ------------------------------------------------------------------ abilities
    @Override
    protected void registerAbilities(List<Ability> out) {
        // 1. Clipboard slap combo: forehand t8, backhand t16, double overhead whack t25
        out.add(Ability.of("clip_slap", 32, 45).range(0, 3.4).weight(4).tick((e, t, tk) -> {
            if (tk == 6 || tk == 14) e.dashForward(0.25, 0);
            if (tk == 8 || tk == 16) {
                t.invulnerableTime = 0;
                FpeUtil.hitCone(e, 3.0, 75, e.dmg(0.75f), 0.5, 0.15);
                arc(e, 2.4f, 140, tk == 8 ? 10 : -10, 1.2, WHITE_ARC);
                FpeUtil.sound(e, SoundEvents.BOOK_PAGE_TURN, 1.2f, 0.6f);
                FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_SWEEP, 0.8f, 1.1f);
            }
            if (tk == 25) {
                t.invulnerableTime = 0;
                FpeUtil.hitCone(e, 3.0, 45, e.dmg(1.2f), 0.4, 0.0);
                arc(e, 2.2f, 100, 80, 1.0, WHITE_ARC);
                for (LivingEntity v : FpeUtil.enemiesInRadius(e, FpeUtil.ahead(e, 1.6, 0), 1.6, 2.5, 1))
                    v.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 30, 2));
                FpeUtil.particles(e, ParticleTypes.CRIT, FpeUtil.ahead(e, 1.6, 1.4), 12, 0.4, 0.2, 0.4, 0.2);
                FpeUtil.sound(e, SoundEvents.WOOD_BREAK, 1f, 0.7f);
            }
        }));

        // 2. Glove haymaker: coils (0-13), giant right hook lands t16 (heavy knockback)
        out.add(Ability.of("glove_haymaker", 34, 70).range(0, 3.4).weight(3).faceUntil(14).tick((e, t, tk) -> {
            if (tk == 4) FpeUtil.sound(e, SoundEvents.WITCH_CELEBRATE, 1f, 1.3f);
            if (tk == 15) e.dashForward(0.35, 0);
            if (tk == 16) {
                FpeUtil.hitCone(e, 3.2, 60, e.dmg(1.6f), 1.6, 0.45);
                arc(e, 2.6f, 120, 0, 1.3, GREEN_ARC);
                FpeUtil.particles(e, ParticleTypes.SWEEP_ATTACK, FpeUtil.ahead(e, 1.8, 1.3), 2, 0.3, 0.2, 0.3, 0);
                FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_KNOCKBACK, 1.2f, 0.6f);
                FpeUtil.sound(e, SoundEvents.SLIME_SQUISH, 1f, 0.7f);
            }
        }));

        // 3. Clap crush: arms spread wide (0-10), clipboards slammed together on the target t13 (stun: slow + nausea)
        out.add(Ability.of("clap_crush", 30, 80).range(0, 3.0).weight(3).faceUntil(11).tick((e, t, tk) -> {
            if (tk == 11) e.dashForward(0.3, 0);
            if (tk == 13) {
                FpeUtil.hitCone(e, 2.6, 40, e.dmg(1.3f), 0.2, 0.1);
                for (LivingEntity v : FpeUtil.enemiesInRadius(e, FpeUtil.ahead(e, 1.5, 0), 1.4, 2.5, 1)) {
                    v.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 50, 3));
                    v.addEffect(new MobEffectInstance(MobEffects.CONFUSION, 70, 0));
                }
                FpeUtil.particles(e, ParticleTypes.CLOUD, FpeUtil.ahead(e, 1.5, 1.4), 10, 0.2, 0.3, 0.2, 0.08);
                FpeUtil.sound(e, SoundEvents.WOODEN_DOOR_CLOSE, 1.4f, 0.6f);
                FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_STRONG, 1f, 0.8f);
            }
        }));

        // 4. Lab grab: lunging glove grab t10, lifts the "specimen" (squeezes t18/t26), body-slams it at t36
        out.add(Ability.of("lab_grab", 50, 140).range(0, 3.2).weight(2).faceUntil(10)
                .start((e, t, tk) -> ((GreenThavel) e).grabbed = false).tick((e, t, tk) -> {
            GreenThavel g = (GreenThavel) e;
            if (tk == 7) e.dashForward(0.45, 0);
            if (tk == 10) {
                g.grabbed = inFront(e, t, 3.4, 60);
                FpeUtil.sound(e, g.grabbed ? SoundEvents.SLIME_SQUISH : SoundEvents.PLAYER_ATTACK_NODAMAGE, 1f, 0.6f);
                if (g.grabbed) FpeUtil.hit(e, t, e.dmg(0.4f), 0, 0);
            }
            if (g.grabbed && tk > 10 && tk < 36) {
                double lift = tk < 32 ? Math.min(1.6, (tk - 10) * 0.12) : 1.9;
                Vec3 hold = FpeUtil.ahead(e, 1.4, lift).add(FpeUtil.right(e).scale(0.4));
                t.setDeltaMovement(hold.subtract(t.position()).scale(0.5));
                t.hurtMarked = true;
                t.fallDistance = 0;
                if (tk == 18 || tk == 26) {
                    t.invulnerableTime = 0;
                    FpeUtil.hit(e, t, e.dmg(0.4f), 0, 0);
                    FpeUtil.particles(e, ParticleTypes.DAMAGE_INDICATOR, t.position().add(0, 1, 0), 4, 0.3, 0.3, 0.3, 0.1);
                    FpeUtil.sound(e, SoundEvents.WITCH_CELEBRATE, 0.9f, 1.4f);
                }
            }
            if (tk == 36) {
                Vec3 at = FpeUtil.ahead(e, 1.5, 0.05);
                if (g.grabbed) {
                    t.invulnerableTime = 0;
                    t.setDeltaMovement(0, -1.2, 0);
                    t.hurtMarked = true;
                    FpeUtil.hit(e, t, e.dmg(1.8f), 0.4, 0.2);
                    t.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 40, 2));
                } else FpeUtil.hitCone(e, 2.5, 50, e.dmg(0.9f), 0.6, 0.2);
                FpeUtil.fx(e, FpeFx.Kind.RING_SHOCK, at, 0, 10, 2.2f, 0).color(0xB0F4F4F0);
                FpeUtil.particles(e, ParticleTypes.LARGE_SMOKE, at, 10, 0.6, 0.1, 0.6, 0.03);
                FpeUtil.sound(e, SoundEvents.ANVIL_LAND, 0.9f, 0.7f);
                g.grabbed = false;
            }
        }).end((e, t, tk) -> ((GreenThavel) e).grabbed = false));

        // 5. Antler charge: lowers horns (0-8), bull-rush t9, gores at t12 and t15, skid
        out.add(Ability.of("antler_charge", 34, 90).range(3.5, 10).weight(3).faceUntil(9).tick((e, t, tk) -> {
            if (tk == 3) FpeUtil.sound(e, SoundEvents.GOAT_RAM_IMPACT, 0.6f, 1.4f);
            if (tk == 9) {
                e.dashToward(t.position(), Math.min(1.5, 0.45 + e.distanceTo(t) * 0.15), 0.05);
                FpeUtil.sound(e, SoundEvents.GOAT_LONG_JUMP, 1f, 1.0f);
            }
            if (tk > 9 && tk < 17) FpeUtil.particles(e, ParticleTypes.CLOUD, e.position().add(0, 0.1, 0), 2, 0.2, 0.05, 0.2, 0.01);
            if (tk == 12 || tk == 15) {
                t.invulnerableTime = 0;
                if (FpeUtil.hitCone(e, 2.2, 60, e.dmg(tk == 12 ? 0.9f : 1.2f), tk == 12 ? 0.3 : 1.3, tk == 12 ? 0.2 : 0.6) > 0)
                    FpeUtil.sound(e, SoundEvents.GOAT_RAM_IMPACT, 1.2f, 0.9f);
            }
            if (tk == 17) e.setDeltaMovement(e.getDeltaMovement().scale(0.2));
        }));

        // 6. Clipboard spin: coils (0-8), three whirling sweeps t10/t16/t22, dizzy wobble
        out.add(Ability.of("clip_spin", 36, 90).range(0, 3.4).weight(3).faceUntil(8).tick((e, t, tk) -> {
            if (tk == 9) e.dashForward(0.25, 0);
            if (tk == 10 || tk == 16 || tk == 22) {
                t.invulnerableTime = 0;
                FpeUtil.hitRadius(e, e.position().add(0, 0.9, 0), 2.9, e.dmg(0.7f), 0.5, 0.15);
                arc(e, 2.7f, 360, 0, 1.0, WHITE_ARC);
                FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_SWEEP, 1f, 0.8f + (tk - 10) * 0.03f);
            }
            if (tk == 26) FpeUtil.sound(e, SoundEvents.WITCH_CELEBRATE, 0.8f, 1.6f);
        }));

        // 7. Boot stomp: crouch, leap t8 at the target, both boots crash down t20 -> shockwave + slow
        out.add(Ability.of("boot_stomp", 40, 110).range(2.5, 8).weight(2).faceUntil(8).tick((e, t, tk) -> {
            if (tk == 8) {
                e.dashToward(t.position(), Math.min(1.1, 0.2 + e.distanceTo(t) * 0.11), 0.62);
                FpeUtil.sound(e, SoundEvents.GOAT_LONG_JUMP, 1f, 1.2f);
            }
            if (tk == 20) {
                FpeUtil.hitRadius(e, e.position(), 2.6, e.dmg(1.4f), 0.9, 0.5);
                for (LivingEntity v : FpeUtil.enemiesInRadius(e, e.position(), 3.2, 2, 1))
                    v.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 50, 1));
                FpeUtil.fx(e, FpeFx.Kind.RING_SHOCK, e.position().add(0, 0.05, 0), 0, 12, 3.2f, e.dmg(0.5f)).color(0xC08CFF3A);
                FpeUtil.particles(e, ParticleTypes.EXPLOSION, e.position(), 1, 0, 0, 0, 0);
                FpeUtil.particles(e, ParticleTypes.LARGE_SMOKE, e.position().add(0, 0.1, 0), 14, 1.2, 0.1, 1.2, 0.03);
                FpeUtil.sound(e, SoundEvents.ANVIL_LAND, 1f, 0.6f);
            }
        }));

        // 8. Front kick: knee chamber, push kick with the tall boot at t10 (big knockback)
        out.add(Ability.of("front_kick", 26, 55).range(0, 3.0).weight(3).faceUntil(9).tick((e, t, tk) -> {
            if (tk == 10) {
                FpeUtil.hitCone(e, 2.8, 45, e.dmg(1.1f), 1.9, 0.35);
                FpeUtil.particles(e, ParticleTypes.CRIT, FpeUtil.ahead(e, 1.4, 0.9), 8, 0.3, 0.2, 0.3, 0.2);
                FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_KNOCKBACK, 1f, 0.9f);
            }
            if (tk == 15) e.dashForward(-0.25, 0.15);
        }));

        // 9. Pummel: five alternating glove jabs (t6..t22), two-glove shove t28
        out.add(Ability.of("pummel", 36, 75).range(0, 3.0).weight(3).tick((e, t, tk) -> {
            if (tk == 6 || tk == 10 || tk == 14 || tk == 18 || tk == 22) {
                t.invulnerableTime = 0;
                e.dashForward(0.12, 0);
                FpeUtil.hitCone(e, 2.6, 50, e.dmg(0.4f), 0.1, 0.05);
                FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_WEAK, 1f, 0.9f + tk * 0.01f);
            }
            if (tk == 28) {
                t.invulnerableTime = 0;
                FpeUtil.hitCone(e, 2.8, 55, e.dmg(1.0f), 1.5, 0.3);
                FpeUtil.particles(e, ParticleTypes.POOF, FpeUtil.ahead(e, 1.4, 1.2), 8, 0.3, 0.3, 0.3, 0.05);
                FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_STRONG, 1f, 0.8f);
            }
        }));

        // 10. Clipboard chop: hop forward (6-12), edge-first guillotine chop t16 -> bleeding cut
        out.add(Ability.of("clip_chop", 36, 85).range(1.5, 5.5).weight(2).faceUntil(8).tick((e, t, tk) -> {
            if (tk == 7) e.dashToward(t.position(), Math.min(0.9, 0.2 + e.distanceTo(t) * 0.12), 0.35);
            if (tk == 16) {
                FpeUtil.hitCone(e, 2.6, 35, e.dmg(1.5f), 0.3, 0.0);
                for (LivingEntity v : FpeUtil.enemiesInRadius(e, FpeUtil.ahead(e, 1.3, 0), 1.3, 2.5, 1))
                    v.addEffect(new MobEffectInstance(MobEffects.WITHER, 50, 0));
                arc(e, 2.3f, 90, 88, 1.0, WHITE_ARC);
                FpeUtil.particles(e, ParticleTypes.CRIT, FpeUtil.ahead(e, 1.4, 0.2), 14, 0.3, 0.1, 0.3, 0.25);
                FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_CRIT, 1f, 0.6f);
            }
        }));

        // 11. Toxic palm (enraged): goggles down, gloves ooze toxin, lunge t13, palm to the face t15 (poison+blind),
        //     grinds (t19/t23), toxic burst shove t26
        out.add(Ability.of("toxic_palm", 40, 120).range(0, 4.5).weight(3).when(FpeEntity::isEnraged).faceUntil(13).tick((e, t, tk) -> {
            if (tk == 5) FpeUtil.sound(e, SoundEvents.BREWING_STAND_BREW, 1f, 1.2f);
            if (tk > 5 && tk < 30 && tk % 2 == 0) toxicPuff(e, FpeUtil.ahead(e, 0.6, 1.0).add(FpeUtil.right(e).scale(0.5)), 2);
            if (tk == 13) e.dashForward(0.55, 0.05);
            if (tk == 15 || tk == 19 || tk == 23) {
                t.invulnerableTime = 0;
                if (FpeUtil.hitCone(e, 2.4, 45, e.dmg(tk == 15 ? 0.9f : 0.35f), 0.05, 0) > 0 && tk == 15) {
                    poison(t, 100);
                    t.addEffect(new MobEffectInstance(MobEffects.BLINDNESS, 40, 0));
                }
                toxicPuff(e, FpeUtil.ahead(e, 1.5, 1.5), 8);
                FpeUtil.sound(e, SoundEvents.SLIME_SQUISH, 1f, 0.8f);
            }
            if (tk == 26) {
                for (LivingEntity v : FpeUtil.enemiesInRadius(e, FpeUtil.ahead(e, 1.5, 0), 2.2, 2.5, 1)) {
                    v.invulnerableTime = 0;
                    if (FpeUtil.hit(e, v, e.dmg(1.1f), 1.6, 0.4)) poison(v, 80);
                }
                toxicPuff(e, FpeUtil.ahead(e, 1.6, 1.2), 30);
                FpeUtil.sound(e, SoundEvents.GENERIC_EXTINGUISH_FIRE, 1f, 0.7f);
            }
        }));

        // 12. Experiment (enraged signature): dash t6, slap t10, backslap t16, double uppercut t24 (launch),
        //     leaps after it t28, double clipboard spike t38 + shockwave, giggles
        out.add(Ability.of("experiment", 60, 200).range(0, 6).weight(3).when(FpeEntity::isEnraged).faceUntil(28).tick((e, t, tk) -> {
            if (tk == 1) FpeUtil.sound(e, SoundEvents.WITCH_CELEBRATE, 1.4f, 0.8f);
            if (tk == 6) e.dashToward(t.position(), Math.min(1.2, 0.3 + e.distanceTo(t) * 0.15), 0.05);
            if (tk > 3 && tk < 44 && tk % 3 == 0) toxicPuff(e, e.position().add(0, 1.0, 0), 2);
            if (tk == 10 || tk == 16) {
                t.invulnerableTime = 0;
                if (FpeUtil.hitCone(e, 2.8, 70, e.dmg(0.7f), 0.15, 0.05) > 0) poison(t, 60);
                arc(e, 2.4f, 140, tk == 10 ? 10 : -10, 1.2, GREEN_ARC);
                FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_SWEEP, 1f, 1.0f);
            }
            if (tk == 24) {
                t.invulnerableTime = 0;
                FpeUtil.hitCone(e, 2.8, 55, e.dmg(1.0f), 0.2, 0.95);
                arc(e, 2.4f, 110, -80, 1.0, GREEN_ARC);
                FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_KNOCKBACK, 1f, 0.7f);
            }
            if (tk == 28) e.dashToward(t.position(), Math.min(0.6, e.distanceTo(t) * 0.15), 0.6);
            if (tk == 38) {
                Vec3 at = e.position();
                FpeUtil.hitRadius(e, at, 2.8, e.dmg(1.6f), 0.8, -0.4);
                for (LivingEntity v : FpeUtil.enemiesInRadius(e, at, 3.2, 3, 1)) poison(v, 80);
                FpeUtil.fx(e, FpeFx.Kind.RING_SHOCK, at.add(0, 0.05, 0), 0, 14, 3.6f, e.dmg(0.5f)).color(0xC08CFF3A);
                toxicPuff(e, at.add(0, 0.3, 0), 30);
                FpeUtil.particles(e, ParticleTypes.EXPLOSION, at, 2, 0.5, 0.1, 0.5, 0);
                FpeUtil.sound(e, SoundEvents.ANVIL_LAND, 1f, 0.5f);
                FpeUtil.sound(e, SoundEvents.GENERIC_EXPLODE, 0.6f, 1.2f);
            }
            if (tk == 48) FpeUtil.sound(e, SoundEvents.WITCH_CELEBRATE, 1.2f, 1.5f);
        }));
    }

    // ------------------------------------------------------------------ sounds
    @Override protected SoundEvent getAmbientSound() { return SoundEvents.WITCH_AMBIENT; }
    @Override protected SoundEvent getHurtSound(DamageSource s) { return SoundEvents.WITCH_HURT; }
    @Override protected SoundEvent getDeathSound() { return SoundEvents.WITCH_DEATH; }
    @Override public int getAmbientSoundInterval() { return 240; }
}
