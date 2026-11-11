package com.fpe.entity.characters;

import java.util.List;

import javax.annotation.Nullable;

import com.fpe.entity.Ability;
import com.fpe.entity.FpeCombat;
import com.fpe.entity.FpeEntity;
import com.fpe.entity.FpeFx;
import com.fpe.entity.FpeProjectile;
import com.fpe.entity.FpeUtil;

import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.BossEvent;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.Vec3;

/**
 * FPE: Insanity Miss Circle. Black spiky mane with two tall horns, one huge red spider-pupil eye, drawing compass in the LEFT hand
 * and a hugely swollen black clawed RIGHT hand as big as the compass. Ticks match client/spec/InsanityCircleSpec.
 */
public class InsanityCircle extends FpeEntity {
    @Nullable private LivingEntity grabbed;

    public InsanityCircle(EntityType<? extends FpeEntity> type, Level level) { super(type, level); }

    @Override public Faction faction() { return Faction.MISS; }

    public static AttributeSupplier.Builder attributes() { return baseAttributes(240, 10, 0.32, 6, 0.7); }

    @Override public double preferredDistance() { return 2.6; }
    @Override protected int restTicks() { return isEnraged() ? 6 : 14; }
    @Override protected boolean hasBossBar() { return true; }
    @Override protected BossEvent.BossBarColor bossColor() { return BossEvent.BossBarColor.RED; }
    @Override protected SoundEvent getAmbientSound() { return SoundEvents.WARDEN_AMBIENT; }
    @Override protected SoundEvent getHurtSound(DamageSource s) { return SoundEvents.WARDEN_HURT; }
    @Override protected SoundEvent getDeathSound() { return SoundEvents.WARDEN_DEATH; }
    @Override public float getVoicePitch() { return 0.7f; }

    private static void snd(FpeEntity e, SoundEvent s, float v, float p) { FpeUtil.sound(e, s, v, p); }

    private Vec3 hand() { return position().add(0, 1.3, 0).add(FpeUtil.forward(this).scale(1.9)).add(FpeUtil.right(this).scale(-0.6)); }

    @Override
    protected void registerAbilities(List<Ability> out) {
        out.add(Ability.of("compass_sweep", 38, 55).range(0, 6).weight(4).faceUntil(14).tick((e, t, tk) -> {
            if (tk == 16) {
                FpeCombat.slashArc(e, 6f, 170, 0, 0, 1.3, 0xE8F0F0F4);
                FpeCombat.slashArc(e, 6f, 170, 10, 0, 1.6, 0xB0A01018);
                FpeUtil.hitCone(e, 6, 85, e.dmg(1.5f), 1.3, 0.4);
                snd(e, SoundEvents.PLAYER_ATTACK_SWEEP, 1.5f, 0.45f);
            }
        }));
        out.add(Ability.of("compass_lunge", 34, 50).range(3, 10).weight(3).faceUntil(14).tick((e, t, tk) -> {
            if (tk == 15) { e.dashForward(1.1, 0.1); snd(e, SoundEvents.TRIDENT_THROW, 1f, 0.5f); }
            if (tk >= 15 && tk <= 21) {
                Vec3 a = e.position().add(0, 1.3, 0);
                FpeUtil.hitLine(e, a, a.add(FpeUtil.forward(e).scale(3.6)), 0.8, e.dmg(1.6f), 1.2, 0.3);
                FpeUtil.particles(e, ParticleTypes.CRIT, a.add(FpeUtil.forward(e).scale(3)), 3, 0.2, 0.2, 0.2, 0.1);
            }
        }));
        out.add(Ability.of("split_slam", 42, 80).range(0, 7).weight(3).faceUntil(12).tick((e, t, tk) -> {
            if (tk == 12) e.dashToward(t.position(), 0.5, 0.55);
            if (tk == 22) {
                FpeUtil.hitRadius(e, FpeUtil.ahead(e, 2.2, 0), 4, e.dmg(1.8f), 1.5, 0.5);
                FpeUtil.fx(e, FpeFx.Kind.RING_SHOCK, e.position().add(0, 0.1, 0), 0, 12, 6f, e.dmg(0.6f));
                for (int i = 0; i < 6; i++) FpeUtil.fx(e, FpeFx.Kind.SPIKE, e.position().add(FpeUtil.forward(e).scale(2 + i * 1.5)), 4 + i, 24, 1f, e.dmg(0.9f));
                snd(e, SoundEvents.GENERIC_EXPLODE, 1f, 0.8f);
            }
        }));
        out.add(Ability.of("compass_throw", 40, 70).range(5, 18).weight(3).faceUntil(16).tick((e, t, tk) -> {
            if (tk == 17) {
                Vec3 from = e.position().add(0, 1.5, 0).add(FpeUtil.forward(e).scale(1.2));
                FpeUtil.projectile(e, FpeProjectile.Kind.COMPASS, from, FpeUtil.aim(from, t, 1.2, 0.2), e.dmg(1.5f));
                snd(e, SoundEvents.TRIDENT_THROW, 1.2f, 0.6f);
            }
        }));
        out.add(Ability.of("draw_circle", 56, 110).range(0, 12).weight(3).blind().faceUntil(8).tick((e, t, tk) -> {
            if (tk == 8) FpeUtil.fx(e, FpeFx.Kind.RING_TRAP, t.position().add(0, 0.05, 0), 36, 46, 6f, e.dmg(2.2f)).color(0xFFE02030);
            if (tk < 40 && tk % 4 == 0) FpeUtil.particles(e, ParticleTypes.CRIT, e.position().add(0, 0.3, 0), 4, 1, 0.1, 1, 0.1);
        }));
        // right arm is a tentacle
        out.add(Ability.of("tentacle_slam", 44, 70).range(0, 9).weight(4).faceUntil(16).tick((e, t, tk) -> {
            if (tk == 21) {
                Vec3 p = FpeUtil.ahead(e, 6, 0);
                FpeUtil.hitRadius(e, p, 4, e.dmg(2f), 1.8, 0.6);
                FpeUtil.fx(e, FpeFx.Kind.RING_SHOCK, p.add(0, 0.1, 0), 0, 14, 8f, e.dmg(0.7f));
                FpeUtil.particles(e, ParticleTypes.EXPLOSION, p, 2, 1, 0.2, 1, 0);
                snd(e, SoundEvents.GENERIC_EXPLODE, 1.2f, 0.6f);
            }
        }));
        out.add(Ability.of("tentacle_lash", 40, 50).range(0, 10).weight(4).faceUntil(16).tick((e, t, tk) -> {
            if (tk == 12 || tk == 19 || tk == 26) {
                Vec3 a = e.position().add(0, 1.3, 0), b = a.add(FpeUtil.forward(e).scale(9));
                for (LivingEntity v : FpeUtil.enemiesInRadius(e, FpeUtil.ahead(e, 4.5, 0), 4.6, 2.5, 1)) {
                    v.invulnerableTime = 0;
                    FpeUtil.hit(e, v, e.dmg(1f), 1.0, 0.3);
                }
                FpeCombat.slashArc(e, 9f, 140, tk == 19 ? -20 : 20, 0, 1.2, 0xE0140810);
                snd(e, SoundEvents.PLAYER_ATTACK_SWEEP, 1.4f, 0.4f);
            }
        }));
        out.add(Ability.of("tentacle_spear", 36, 60).range(3, 12).weight(3).faceUntil(15).tick((e, t, tk) -> {
            if (tk == 16) {
                Vec3 a = e.position().add(0, 1.5, 0), b = a.add(FpeUtil.forward(e).scale(11));
                FpeUtil.hitLine(e, a, b, 1.0, e.dmg(1.9f), 1.4, 0.3);
                for (int i = 1; i <= 11; i++) FpeUtil.particles(e, ParticleTypes.SQUID_INK, a.add(FpeUtil.forward(e).scale(i)), 3, 0.2, 0.2, 0.2, 0.02);
                snd(e, SoundEvents.TRIDENT_HIT, 1.2f, 0.5f);
            }
        }));
        out.add(Ability.of("tentacle_grab", 50, 100).range(2, 10).weight(3).faceUntil(14)
                .start((e, t, tk) -> ((InsanityCircle) e).grabbed = null)
                .tick((e, t, tk) -> {
                    InsanityCircle c = (InsanityCircle) e;
                    if (tk == 14) for (LivingEntity v : FpeUtil.enemiesInRadius(e, FpeUtil.ahead(e, 5, 0), 5.5, 2.5, 1)) { c.grabbed = v; break; }
                    if (c.grabbed != null && c.grabbed.isAlive() && tk >= 14 && tk < 40) {
                        Vec3 h = c.hand();
                        Vec3 cur = c.grabbed.position();
                        Vec3 to = tk < 26 ? h.subtract(cur).scale(0.35) : Vec3.ZERO;
                        c.grabbed.setDeltaMovement(to);
                        c.grabbed.hurtMarked = true;
                        if (tk >= 26) { c.grabbed.teleportTo(h.x, h.y - c.grabbed.getBbHeight() * 0.5, h.z); c.grabbed.setDeltaMovement(Vec3.ZERO); }
                        if (tk == 28 || tk == 34) { c.grabbed.invulnerableTime = 0; FpeUtil.hit(e, c.grabbed, e.dmg(1.2f), 0, 0); FpeCombat.bleed(e, c.grabbed, 40); snd(e, SoundEvents.PLAYER_ATTACK_CRIT, 1f, 0.5f); }
                    }
                    if (tk == 40 && c.grabbed != null) {
                        FpeUtil.hit(e, c.grabbed, e.dmg(1.6f), 0, 0);
                        FpeUtil.knock(c.grabbed, e.position().subtract(FpeUtil.forward(e)), 2.2, 0.55);
                        c.grabbed = null;
                    }
                }));
        out.add(Ability.of("tentacle_erupt", 46, 90).range(3, 16).weight(3).faceUntil(14).tick((e, t, tk) -> {
            if (tk == 16) {
                for (int i = 0; i < 5; i++) {
                    Vec3 d = FpeCombat.rotY(new Vec3(1, 0, 0), i * 72 + e.getRandom().nextInt(40));
                    FpeUtil.fx(e, FpeFx.Kind.TENTACLE, t.position().add(d.scale(i == 0 ? 0 : 2.4)), 12 + i * 2, 50, 1.5f, e.dmg(0.9f)).param(1.2f);
                }
                snd(e, SoundEvents.SLIME_SQUISH, 1.2f, 0.4f);
            }
        }));
        // rough compass work (left hand)
        out.add(Ability.of("compass_frenzy", 48, 80).range(0, 6).weight(4).moving().faceUntil(40).tick((e, t, tk) -> {
            if (tk == 8 || tk == 17 || tk == 25 || tk == 33 || tk == 40) {
                e.snapFace(t);
                e.dashForward(0.7, 0.05);
                for (LivingEntity v : FpeCombat.cone(e, 5, 75)) { v.invulnerableTime = 0; FpeUtil.hit(e, v, e.dmg(0.9f), 0.8, 0.2); }
                FpeCombat.slashArc(e, 5.5f, 140, (tk * 37) % 80 - 40, 0, 1.3, 0xE8F0F0F4);
                snd(e, SoundEvents.PLAYER_ATTACK_SWEEP, 1.3f, 0.4f + (tk % 3) * 0.1f);
            }
        }));
        out.add(Ability.of("compass_cleave", 44, 75).range(0, 7).weight(3).faceUntil(18).tick((e, t, tk) -> {
            if (tk == 22) {
                Vec3 p = FpeUtil.ahead(e, 3.4, 0);
                FpeUtil.hitRadius(e, p, 3.6, e.dmg(2.2f), 1.6, 0.55);
                FpeCombat.slashArc(e, 6f, 100, 80, 0, 1.8, 0xF0FFFFFF);
                FpeUtil.fx(e, FpeFx.Kind.SPIKE, p, 2, 24, 1f, e.dmg(0.6f)).param(1.4f);
                snd(e, SoundEvents.PLAYER_ATTACK_STRONG, 1.5f, 0.4f);
            }
        }));
        out.add(Ability.of("hair_lash", 34, 60).range(0, 7).weight(3).faceUntil(8).tick((e, t, tk) -> {
            if (tk == 15 || tk == 21) {
                FpeUtil.hitRadius(e, e.position(), 6.5, e.dmg(1f), 1.3, 0.35);
                FpeUtil.arc(e, ParticleTypes.SQUID_INK, e.position().add(0, 1.2, 0), tk * 20f, 180, 5, 24);
            }
        }));
        out.add(Ability.of("eye_beam", 54, 90).range(6, 22).weight(3).faceUntil(32).tick((e, t, tk) -> {
            Vec3 eye = e.position().add(0, 1.9, 0).add(FpeUtil.forward(e).scale(0.5));
            if (tk >= 10 && tk < 30) FpeUtil.particles(e, ParticleTypes.CRIT, eye, 3, 0.1, 0.1, 0.1, 0.3);
            if (tk == 32) {
                Vec3 end = eye.add(FpeUtil.forward(e).scale(22));
                FpeUtil.hitLine(e, eye, end, 0.9, e.dmg(2.2f), 1.0, 0.3);
                for (int i = 1; i <= 22; i++) FpeUtil.particles(e, net.minecraft.core.particles.ParticleTypes.CRIT, eye.add(FpeUtil.forward(e).scale(i)), 2, 0.05, 0.05, 0.05, 0);
                for (LivingEntity v : FpeUtil.enemiesInRadius(e, FpeUtil.ahead(e, 8, 0), 9, 3, 1)) v.addEffect(new MobEffectInstance(MobEffects.DARKNESS, 80, 0));
                snd(e, SoundEvents.WARDEN_SONIC_BOOM, 1.5f, 0.7f);
            }
        }));
        out.add(Ability.of("rampage", 72, 200).range(0, 12).weight(6).moving().when(FpeEntity::isEnraged).faceUntil(6).tick((e, t, tk) -> {
            if (tk == 8 || tk == 22 || tk == 36 || tk == 50) { e.snapFace(t); e.dashForward(1.1, 0.1); }
            if (tk == 14 || tk == 28 || tk == 42 || tk == 56) {
                FpeUtil.hitRadius(e, FpeUtil.ahead(e, 2, 0), 3.8, e.dmg(1.3f), 1.4, 0.4);
                FpeCombat.slashArc(e, 5f, 150, (tk / 14) % 2 == 0 ? 25 : -25, 0, 1.4, 0xE0F0F0F4);
                snd(e, SoundEvents.PLAYER_ATTACK_SWEEP, 1.3f, 0.5f);
            }
            if (tk == 64) FpeUtil.fx(e, FpeFx.Kind.RING_SHOCK, e.position().add(0, 0.1, 0), 0, 16, 10f, e.dmg(1f));
        }));
    
        // ---- extra melee
        out.add(com.fpe.entity.Ability.of("boot_stomp", 32, 40).range(0, 3.6).weight(3).faceUntil(12).tick((e, t, tk) -> { if (tk == 15) { com.fpe.entity.FpeUtil.hitRadius(e, com.fpe.entity.FpeUtil.ahead(e, 1.5, 0), 3.6, e.dmg(1.5f), 1.5, 0.45); com.fpe.entity.FpeUtil.fx(e, com.fpe.entity.FpeFx.Kind.RING_SHOCK, e.position().add(0, 0.1, 0), 0, 10, 3.6f + 1.5f, 0); com.fpe.entity.FpeUtil.sound(e, net.minecraft.sounds.SoundEvents.GENERIC_EXPLODE, 1.2f, 1.4f); } }));
        out.add(com.fpe.entity.Ability.of("pommel_strike", 28, 40).range(0, 3.2).weight(3).faceUntil(8).tick((e, t, tk) -> { if (tk == 11) { com.fpe.entity.FpeUtil.hitCone(e, 3.2, 35, e.dmg(1.2f), 1.0, 0.2); com.fpe.entity.FpeUtil.sound(e, net.minecraft.sounds.SoundEvents.PLAYER_ATTACK_CRIT, 1.2f, 1.1f); } }));
        out.add(com.fpe.entity.Ability.of("tentacle_backhand", 28, 35).range(0, 6).weight(3).faceUntil(9).tick((e, t, tk) -> { if (tk == 12) { com.fpe.entity.FpeUtil.hitCone(e, 6, 80, e.dmg(1.1f), 1.4, 0.3); com.fpe.entity.FpeCombat.slashArc(e, 6f, 130, -15, 0, 1.4, 0xE0140810); com.fpe.entity.FpeUtil.sound(e, net.minecraft.sounds.SoundEvents.PLAYER_ATTACK_SWEEP, 1.2f, 0.6f); } }));
}
}
