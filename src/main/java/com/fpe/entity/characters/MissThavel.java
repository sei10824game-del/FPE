package com.fpe.entity.characters;

import java.util.List;

import com.fpe.entity.Ability;
import com.fpe.entity.FpeEntity;
import com.fpe.entity.FpeFx;
import com.fpe.entity.FpeUtil;

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

/**
 * Miss Thavel – the alphabet teacher. Giant shard claw on her right arm, ABC blocks in her crown.
 * Pure melee brawler: every attack is a claw / block / body strike at close range (gap-closers included).
 * Every tick index below matches the key poses in tools/bbgen/chars/miss_thavel.py.
 */
public class MissThavel extends FpeEntity {
    private boolean grabbed;

    public MissThavel(EntityType<? extends FpeEntity> type, Level level) { super(type, level); }

    @Override public Faction faction() { return Faction.MISS; }

    public static AttributeSupplier.Builder attributes() { return baseAttributes(130, 7, 0.29, 5, 0.35); }

    @Override public double preferredDistance() { return 1.6; }
    @Override protected int restTicks() { return isEnraged() ? 7 : 16; }

    // ------------------------------------------------------------------ positions
    /** world position of the giant claw (right hand) */
    static Vec3 claw(FpeEntity e, double fwd, double up) { return e.position().add(FpeUtil.forward(e).scale(fwd)).add(FpeUtil.right(e).scale(0.55)).add(0, up, 0); }

    static void slashArc(FpeEntity e, float radius, float sweep, float tilt, float yawOff, double y, int color) {
        FpeFx f = FpeUtil.fx(e, FpeFx.Kind.ARC, e.position().add(0, y, 0), 0, 7, radius, 0).param(sweep).color(color);
        f.setYRot(e.getYRot() + yawOff);
        f.setXRot(tilt);
    }

    static Vec3 rotY(Vec3 v, double deg) {
        double a = Math.toRadians(deg), c = Math.cos(a), s = Math.sin(a);
        return new Vec3(v.x * c - v.z * s, v.y, v.x * s + v.z * c);
    }

    // ------------------------------------------------------------------ abilities
    @Override
    protected void registerAbilities(List<Ability> out) {
        // 1. Rake: three-hit claw combo (t9 forehand, t18 backhand, t30 overhead rake)
        out.add(Ability.of("rake", 40, 50).range(0, 3.6).weight(4).tick((e, t, tk) -> {
            if (tk == 7 || tk == 16) e.dashForward(0.32, 0);
            if (tk == 27) e.dashForward(0.45, 0.05);
            if (tk == 9 || tk == 18) {
                t.invulnerableTime = 0;
                FpeUtil.hitCone(e, 3.2, 75, e.dmg(0.8f), 0.45, 0.15);
                slashArc(e, 2.6f, 150, tk == 9 ? 15 : -15, 0, 1.2, 0xE0302A3A);
                FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_SWEEP, 1f, tk == 9 ? 0.7f : 0.85f);
            }
            if (tk == 30) {
                t.invulnerableTime = 0;
                FpeUtil.hitCone(e, 3.4, 50, e.dmg(1.25f), 0.9, 0.25);
                slashArc(e, 2.4f, 120, 75, 0, 1.0, 0xF0201C28);
                FpeUtil.particles(e, ParticleTypes.CRIT, FpeUtil.ahead(e, 1.8, 0.3), 14, 0.5, 0.2, 0.5, 0.25);
                FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_STRONG, 1f, 0.6f);
            }
        }));

        // 2. Claw smash: rears up (0-20), slams at t22 -> cone hit + shockwave (+ ring of shards around the impact when enraged)
        out.add(Ability.of("claw_smash", 44, 100).range(0, 4).weight(2).faceUntil(20).tick((e, t, tk) -> {
            if (tk == 6) FpeUtil.sound(e, SoundEvents.RAVAGER_ROAR, 0.7f, 1.6f);
            if (tk == 22) {
                Vec3 at = FpeUtil.ahead(e, 1.9, 0.05);
                FpeUtil.hitCone(e, 3.5, 60, e.dmg(1.6f), 1.0, 0.5);
                FpeUtil.fx(e, FpeFx.Kind.RING_SHOCK, at, 0, 12, 3.5f, e.dmg(0.6f)).color(0xC0302838);
                FpeUtil.particles(e, ParticleTypes.EXPLOSION, at, 2, 0.4, 0.1, 0.4, 0);
                FpeUtil.particles(e, ParticleTypes.LARGE_SMOKE, at, 16, 1.0, 0.2, 1.0, 0.04);
                FpeUtil.sound(e, SoundEvents.ANVIL_LAND, 1f, 0.5f);
                FpeUtil.sound(e, SoundEvents.GENERIC_EXPLODE, 0.8f, 0.8f);
                if (e.isEnraged()) for (int i = 0; i < 5; i++)
                    FpeUtil.fx(e, FpeFx.Kind.SPIKE, at.add(rotY(new Vec3(1.4, 0, 0), i * 72 + 15)), 4 + i, 30, 1.0f, e.dmg(0.8f)).param(1.1f);
            }
        }));

        // 3. Scratch lunge: low crouch, explosive gap-closing dash at t10, rising claw at t14
        out.add(Ability.of("scratch_lunge", 30, 80).range(3.5, 9).weight(2).faceUntil(10).tick((e, t, tk) -> {
            if (tk == 10) {
                e.dashToward(t.position(), Math.min(1.5, 0.35 + e.distanceTo(t) * 0.17), 0.22);
                FpeUtil.sound(e, SoundEvents.PHANTOM_SWOOP, 1f, 1.2f);
            }
            if (tk > 10 && tk < 17) FpeUtil.particles(e, ParticleTypes.SQUID_INK, e.position().add(0, 0.6, 0), 2, 0.2, 0.3, 0.2, 0.01);
            if (tk == 14) {
                FpeUtil.hitCone(e, 2.6, 60, e.dmg(1.2f), 0.7, 0.35);
                slashArc(e, 2.2f, 130, -45, 0, 1.1, 0xE0302A3A);
                FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_CRIT, 1f, 0.8f);
            }
        }));

        // 4. Grab & rip: lunging grab (t10), lifts & squeezes the victim (t16/22/28), rips and flings at t36 (bleeds)
        out.add(Ability.of("grab_rip", 52, 140).range(0, 3.2).weight(2).faceUntil(10).start((e, t, tk) -> ((MissThavel) e).grabbed = false).tick((e, t, tk) -> {
            MissThavel b = (MissThavel) e;
            if (tk == 6) e.dashForward(0.4, 0);
            if (tk == 10) {
                Vec3 to = t.position().subtract(e.position());
                double ang = Math.toDegrees(Math.acos(Mth.clamp(new Vec3(to.x, 0, to.z).normalize().dot(FpeUtil.forward(e)), -1, 1)));
                b.grabbed = e.distanceTo(t) < 3.6 && ang < 60 && FpeUtil.canHurt(e, t);
                FpeUtil.sound(e, b.grabbed ? SoundEvents.PLAYER_ATTACK_KNOCKBACK : SoundEvents.PLAYER_ATTACK_NODAMAGE, 1f, 0.6f);
                if (b.grabbed) FpeUtil.hit(e, t, e.dmg(0.4f), 0, 0);
            }
            if (b.grabbed && tk > 10 && tk < 36) {
                Vec3 hold = claw(e, 1.5, 0.6 + Math.min(1.2, (tk - 10) * 0.08)).subtract(0, t.getBbHeight() * 0.4, 0);
                t.setDeltaMovement(hold.subtract(t.position()).scale(0.5));
                t.hurtMarked = true;
                t.fallDistance = 0;
                if (tk == 16 || tk == 22 || tk == 28) {
                    t.invulnerableTime = 0;
                    FpeUtil.hit(e, t, e.dmg(0.35f), 0, 0);
                    FpeUtil.particles(e, ParticleTypes.DAMAGE_INDICATOR, t.position().add(0, 1, 0), 4, 0.3, 0.3, 0.3, 0.1);
                    FpeUtil.sound(e, SoundEvents.PLAYER_HURT_SWEET_BERRY_BUSH, 1f, 0.7f);
                }
            }
            if (tk == 36) {
                if (b.grabbed) {
                    t.invulnerableTime = 0;
                    FpeUtil.hit(e, t, e.dmg(1.7f), 1.7, 0.6);
                    bleed(t, 60);
                    FpeUtil.particles(e, ParticleTypes.SWEEP_ATTACK, t.position().add(0, 1, 0), 3, 0.4, 0.4, 0.4, 0);
                } else FpeUtil.hitCone(e, 2.6, 60, e.dmg(0.9f), 0.8, 0.3);
                slashArc(e, 2.0f, 140, 30, 0, 1.2, 0xF0201C28);
                FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_STRONG, 1f, 0.5f);
                b.grabbed = false;
            }
        }).end((e, t, tk) -> ((MissThavel) e).grabbed = false));

        // 5. Screech: inhales (0-10), point-blank shriek t12 (knockback + slow + nausea in a short cone)
        out.add(Ability.of("screech", 36, 120).range(0, 4.5).weight(2).tick((e, t, tk) -> {
            if (tk == 12) {
                FpeUtil.sound(e, SoundEvents.GHAST_SCREAM, 1.4f, 0.7f);
                FpeUtil.sound(e, SoundEvents.RAVAGER_ROAR, 1f, 1.5f);
                FpeUtil.hitCone(e, 4.5, 50, e.dmg(0.6f), 1.6, 0.4);
                for (LivingEntity v : FpeUtil.enemiesInRadius(e, e.position(), 4.5, 3, 1)) {
                    Vec3 d = v.position().subtract(e.position());
                    if (new Vec3(d.x, 0, d.z).normalize().dot(FpeUtil.forward(e)) > 0.6) {
                        v.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 70, 1));
                        v.addEffect(new MobEffectInstance(MobEffects.CONFUSION, 80, 0));
                    }
                }
            }
            if (tk >= 12 && tk <= 20 && tk % 2 == 0) {
                double dist = 1.0 + (tk - 12) * 0.4;
                FpeUtil.particles(e, ParticleTypes.SONIC_BOOM, FpeUtil.ahead(e, dist, 1.5), 1, 0, 0, 0, 0);
                FpeUtil.particles(e, ParticleTypes.NOTE, FpeUtil.ahead(e, dist, 1.6), 3, 0.6, 0.4, 0.6, 1);
            }
        }));

        // 6. Shard quake: both hands raised (0-12), double slam t14 -> ring of claw-shards bursts up around her,
        //    claw rips upward at t24 -> a fan of shards tears out of the floor right in front of her
        out.add(Ability.of("shard_quake", 40, 130).range(0, 4).weight(2).faceUntil(13).tick((e, t, tk) -> {
            if (tk == 4) FpeUtil.sound(e, SoundEvents.WITCH_CELEBRATE, 1f, 0.7f);
            if (tk == 14) {
                FpeUtil.hitRadius(e, e.position(), 2.6, e.dmg(1.0f), 0.8, 0.45);
                int n = e.isEnraged() ? 10 : 8;
                for (int i = 0; i < n; i++)
                    FpeUtil.fx(e, FpeFx.Kind.SPIKE, e.position().add(rotY(FpeUtil.forward(e), i * 360.0 / n).scale(1.7)), 1 + i % 3, 24, 0.8f, e.dmg(0.6f)).param(0.9f);
                FpeUtil.particles(e, ParticleTypes.LARGE_SMOKE, e.position().add(0, 0.1, 0), 14, 1.2, 0.1, 1.2, 0.03);
                FpeUtil.sound(e, SoundEvents.ANVIL_LAND, 1f, 0.6f);
            }
            if (tk == 24) {
                t.invulnerableTime = 0;
                FpeUtil.hitCone(e, 3.2, 55, e.dmg(1.1f), 0.5, 0.8);
                for (int i = -1; i <= 1; i++)
                    FpeUtil.fx(e, FpeFx.Kind.SPIKE, e.position().add(rotY(FpeUtil.forward(e), i * 25).scale(2.0 + (i == 0 ? 0.6 : 0))), 0, 22, 0.9f, e.dmg(0.8f)).param(1.4f);
                FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_SWEEP, 1f, 0.5f);
            }
        }));

        // 7. Spin shred: coils (0-8), whirls three times with the claw flung out - ring hits at t10/16/22 (enraged: bleeding cuts)
        out.add(Ability.of("spin_shred", 36, 90).range(0, 3.4).weight(3).faceUntil(8).tick((e, t, tk) -> {
            if (tk == 9) e.dashForward(0.25, 0);
            if (tk == 10 || tk == 16 || tk == 22) {
                t.invulnerableTime = 0;
                FpeUtil.hitRadius(e, e.position().add(0, 0.9, 0), 3.0, e.dmg(0.75f), 0.5, 0.2);
                if (e.isEnraged()) for (LivingEntity v : FpeUtil.enemiesInRadius(e, e.position(), 3.0, 2, 1)) bleed(v, 40);
                slashArc(e, 2.8f, 360, 0, 0, 1.0, 0xD0302A3A);
                FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_SWEEP, 1f, 0.6f + (tk - 10) * 0.03f);
            }
            if (tk == 26) FpeUtil.sound(e, SoundEvents.WITCH_CELEBRATE, 0.8f, 1.5f);
        }));

        // 8. Block bash: plucks the C block off her crown (t5), steps in and smashes it on the victim's head (t12, dazes),
        //    then a backhand claw tear (t22)
        out.add(Ability.of("block_bash", 36, 70).range(0, 3.2).weight(3).faceUntil(11).tick((e, t, tk) -> {
            if (tk == 5) FpeUtil.sound(e, SoundEvents.WOOD_HIT, 0.8f, 1.6f);
            if (tk == 10) e.dashForward(0.3, 0);
            if (tk == 12) {
                FpeUtil.hitCone(e, 2.8, 55, e.dmg(1.0f), 0.4, 0.1);
                for (LivingEntity v : FpeUtil.enemiesInRadius(e, FpeUtil.ahead(e, 1.4, 0), 1.6, 2, 1))
                    v.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 40, 2));
                Vec3 at = FpeUtil.ahead(e, 1.4, 1.4);
                FpeUtil.particles(e, ParticleTypes.CRIT, at, 12, 0.3, 0.3, 0.3, 0.3);
                FpeUtil.particles(e, ParticleTypes.POOF, at, 6, 0.2, 0.2, 0.2, 0.05);
                FpeUtil.sound(e, SoundEvents.WOOD_BREAK, 1.2f, 0.7f);
                FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_KNOCKBACK, 1f, 0.6f);
            }
            if (tk == 22) {
                t.invulnerableTime = 0;
                FpeUtil.hitCone(e, 3.2, 70, e.dmg(0.9f), 0.9, 0.25);
                slashArc(e, 2.6f, 150, -20, 0, 1.1, 0xE0302A3A);
                FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_SWEEP, 1f, 0.7f);
            }
        }));

        // 9. Skewer: claw fingers bunched into a spear, cocked back (0-10), lunging thrust t12 pierces a line and makes the
        //    victim bleed, twist, then rips the claw out at t20 (drags the victim in)
        out.add(Ability.of("skewer", 32, 80).range(0, 4.2).weight(3).faceUntil(10).tick((e, t, tk) -> {
            if (tk == 4) FpeUtil.sound(e, SoundEvents.CROSSBOW_LOADING_MIDDLE, 1f, 0.6f);
            if (tk == 11) e.dashForward(0.5, 0);
            if (tk == 12) {
                Vec3 from = FpeUtil.ahead(e, 0.4, 1.1), to = FpeUtil.ahead(e, 4.0, 1.1);
                FpeUtil.hitLine(e, from, to, 0.8, e.dmg(1.3f), 0.2, 0.05);
                for (LivingEntity v : FpeUtil.enemiesInRadius(e, FpeUtil.ahead(e, 2.2, 0), 1.9, 2, 1)) bleed(v, 70);
                FpeUtil.particles(e, ParticleTypes.CRIT, FpeUtil.ahead(e, 2.4, 1.1), 10, 0.6, 0.1, 0.6, 0.3);
                FpeUtil.sound(e, SoundEvents.TRIDENT_HIT, 1f, 0.7f);
            }
            if (tk == 20) {
                t.invulnerableTime = 0;
                FpeUtil.hitCone(e, 2.8, 45, e.dmg(0.5f), -0.5, 0.1);
                FpeUtil.particles(e, ParticleTypes.DAMAGE_INDICATOR, FpeUtil.ahead(e, 1.8, 1.1), 5, 0.3, 0.3, 0.3, 0.1);
                FpeUtil.sound(e, SoundEvents.PLAYER_HURT_SWEET_BERRY_BUSH, 1f, 0.6f);
            }
        }));

        // 10. Pounce: crouches (0-8), leaps at the target (t8), crashes down claws-first (t18), pins and rakes twice (t24/t29)
        out.add(Ability.of("pounce", 40, 110).range(4, 10).weight(2).faceUntil(8).tick((e, t, tk) -> {
            if (tk == 3) FpeUtil.sound(e, SoundEvents.CAT_HISS, 1f, 0.6f);
            if (tk == 8) {
                e.dashToward(t.position(), Mth.clamp(e.distanceTo(t) / 6.4, 0.5, 1.5), 0.42);
                FpeUtil.sound(e, SoundEvents.PHANTOM_FLAP, 1f, 0.8f);
            }
            if (tk > 8 && tk < 18) FpeUtil.particles(e, ParticleTypes.SQUID_INK, e.position().add(0, 0.8, 0), 2, 0.2, 0.3, 0.2, 0.01);
            if (tk == 18) {
                FpeUtil.hitRadius(e, FpeUtil.ahead(e, 0.6, 0), 2.3, e.dmg(1.3f), 0.3, 0.1);
                for (LivingEntity v : FpeUtil.enemiesInRadius(e, FpeUtil.ahead(e, 0.6, 0), 2.3, 2, 1))
                    v.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 30, 4));
                FpeUtil.particles(e, ParticleTypes.LARGE_SMOKE, e.position(), 10, 0.8, 0.1, 0.8, 0.03);
                FpeUtil.sound(e, SoundEvents.ANVIL_LAND, 0.8f, 0.8f);
            }
            if (tk == 24 || tk == 29) {
                t.invulnerableTime = 0;
                FpeUtil.hitCone(e, 2.4, 70, e.dmg(0.55f), tk == 29 ? 0.8 : 0.1, 0.1);
                slashArc(e, 1.8f, 120, tk == 24 ? 80 : 60, tk == 24 ? 15 : -15, 0.4, 0xE0302A3A);
                FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_SWEEP, 1f, tk == 24 ? 0.8f : 0.65f);
            }
        }));

        // 11. ABC combo: writes A-B-C with her claw on the victim: A = inverted-V double chop (t10),
        //     B = two quick hooks (t20/t23), C = huge crescent sweep (t34)
        out.add(Ability.of("abc_combo", 46, 80).range(0, 3.6).weight(3).tick((e, t, tk) -> {
            if (tk == 8 || tk == 18) e.dashForward(0.28, 0);
            if (tk == 31) e.dashForward(0.4, 0);
            if (tk == 10) {
                t.invulnerableTime = 0;
                FpeUtil.hitCone(e, 3.0, 50, e.dmg(0.9f), 0.3, 0.1);
                slashArc(e, 2.2f, 90, 70, 20, 1.3, 0xE0302A3A);
                slashArc(e, 2.2f, 90, 70, -20, 1.3, 0xE0302A3A);
                FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_STRONG, 1f, 0.8f);
            }
            if (tk == 20 || tk == 23) {
                t.invulnerableTime = 0;
                FpeUtil.hitCone(e, 2.8, 60, e.dmg(0.5f), 0.2, 0.1);
                slashArc(e, 1.8f, 160, tk == 20 ? 30 : -30, 0, tk == 20 ? 1.5 : 0.8, 0xE0302A3A);
                FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_SWEEP, 1f, tk == 20 ? 0.9f : 1.0f);
            }
            if (tk == 34) {
                t.invulnerableTime = 0;
                FpeUtil.hitCone(e, 3.6, 95, e.dmg(1.2f), 1.1, 0.3);
                slashArc(e, 3.2f, 200, 0, 0, 1.0, 0xF0201C28);
                FpeUtil.particles(e, ParticleTypes.CRIT, FpeUtil.ahead(e, 1.8, 1.0), 14, 1.2, 0.2, 1.2, 0.25);
                FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_STRONG, 1f, 0.55f);
            }
        }));

        // 12. Crown headbutt: rears back (0-9), dashes and rams her ABC crown into the victim (t11): heavy knockback + daze
        out.add(Ability.of("crown_headbutt", 30, 90).range(0, 3.4).weight(2).faceUntil(9).tick((e, t, tk) -> {
            if (tk == 3) FpeUtil.sound(e, SoundEvents.WITCH_CELEBRATE, 1f, 1.2f);
            if (tk == 9) e.dashForward(0.55, 0.05);
            if (tk == 11) {
                FpeUtil.hitCone(e, 2.4, 50, e.dmg(1.0f), 1.5, 0.35);
                for (LivingEntity v : FpeUtil.enemiesInRadius(e, FpeUtil.ahead(e, 1.2, 0), 1.6, 2, 1)) {
                    v.addEffect(new MobEffectInstance(MobEffects.CONFUSION, 70, 0));
                    v.addEffect(new MobEffectInstance(MobEffects.WEAKNESS, 60, 0));
                }
                FpeUtil.particles(e, ParticleTypes.CRIT, FpeUtil.ahead(e, 1.0, 1.7), 14, 0.3, 0.3, 0.3, 0.3);
                FpeUtil.sound(e, SoundEvents.WOOD_HIT, 1.4f, 0.6f);
                FpeUtil.sound(e, SoundEvents.ZOMBIE_ATTACK_WOODEN_DOOR, 0.9f, 0.9f);
            }
        }));

        // 13. ENRAGED - Alphabet frenzy: cackles with both hands up (0-12), then ten alternating talon/claw slashes
        //     while stalking forward (t14..t50, every 4 ticks), final two-handed "Z" slam (t60) with a shockwave + bleed
        out.add(Ability.of("alphabet_frenzy", 76, 220).range(0, 4.5).weight(3).when(FpeEntity::isEnraged).tick((e, t, tk) -> {
            if (tk == 4) FpeUtil.sound(e, SoundEvents.WITCH_CELEBRATE, 1.5f, 0.8f);
            if (tk >= 14 && tk <= 50 && (tk - 14) % 4 == 0) {
                int letter = (tk - 14) / 4;
                boolean claw = letter % 2 == 1;
                e.snapFace(t);
                e.dashForward(0.18, 0);
                t.invulnerableTime = 0;
                FpeUtil.hitCone(e, claw ? 3.0 : 2.6, 70, e.dmg(claw ? 0.5f : 0.35f), 0.15, 0.05);
                slashArc(e, claw ? 2.4f : 1.8f, 130, claw ? -25 : 25, 0, 1.1, 0xE0302A3A);
                FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_SWEEP, 0.8f, 0.7f + letter * 0.06f);
            }
            if (tk == 58) e.dashForward(0.35, 0.05);
            if (tk == 60) {
                t.invulnerableTime = 0;
                Vec3 at = FpeUtil.ahead(e, 1.8, 0.05);
                FpeUtil.hitCone(e, 3.6, 70, e.dmg(1.6f), 1.4, 0.5);
                for (LivingEntity v : FpeUtil.enemiesInRadius(e, at, 2.5, 2, 1)) bleed(v, 80);
                slashArc(e, 3.0f, 160, 60, 0, 1.4, 0xF0201C28);
                FpeUtil.fx(e, FpeFx.Kind.RING_SHOCK, at, 0, 12, 3.2f, e.dmg(0.6f)).color(0xC0302838);
                FpeUtil.particles(e, ParticleTypes.EXPLOSION, at, 2, 0.4, 0.1, 0.4, 0);
                FpeUtil.sound(e, SoundEvents.ANVIL_LAND, 1f, 0.5f);
                FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_STRONG, 1f, 0.5f);
            }
        }));
    }

    /** ink bleed: black hearts (wither) for a short while */
    static void bleed(LivingEntity v, int ticks) { v.addEffect(new MobEffectInstance(MobEffects.WITHER, ticks, 0)); }

    // ------------------------------------------------------------------ sounds
    @Override protected SoundEvent getAmbientSound() { return SoundEvents.WITCH_CELEBRATE; }
    @Override protected SoundEvent getHurtSound(DamageSource s) { return SoundEvents.WITCH_HURT; }
    @Override protected SoundEvent getDeathSound() { return SoundEvents.WITCH_DEATH; }
    @Override public int getAmbientSoundInterval() { return 220; }
}
