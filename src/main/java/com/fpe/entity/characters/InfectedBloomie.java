package com.fpe.entity.characters;

import java.util.List;

import com.fpe.entity.Ability;
import com.fpe.entity.FpeEntity;
import com.fpe.entity.FpeFx;
import com.fpe.entity.FpeProjectile;
import com.fpe.entity.FpeUtil;

import net.minecraft.core.BlockPos;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.EntityDimensions;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.Pose;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.Vec3;

/**
 * Infected Bloomie (Basics in Survival AU): a hunched, spindly 3-block creature, drooling black jaw, two long mantis-scythe blades
 * over the back, long clawed forelimbs. Ticks match client/spec/InfectedBloomieSpec.
 */
public class InfectedBloomie extends FpeEntity {
    private boolean landed;

    public InfectedBloomie(EntityType<? extends FpeEntity> type, Level level) { super(type, level); }

    public static AttributeSupplier.Builder attributes() { return baseAttributes(160, 8, 0.36, 4, 0.5); }

    @Override public double preferredDistance() { return 2.6; }
    @Override protected int restTicks() { return isEnraged() ? 6 : 14; }
    @Override public boolean causeFallDamage(float d, float m, DamageSource s) { return false; }
    @Override protected float getStandingEyeHeight(Pose p, EntityDimensions d) { return d.height * 0.62f; }

    @Override protected SoundEvent getAmbientSound() { return SoundEvents.ZOGLIN_ANGRY; }
    @Override protected SoundEvent getHurtSound(DamageSource s) { return SoundEvents.RAVAGER_HURT; }
    @Override protected SoundEvent getDeathSound() { return SoundEvents.RAVAGER_DEATH; }
    @Override protected void playStepSound(BlockPos p, BlockState s) { playSound(SoundEvents.SPIDER_STEP, 0.5f, 0.6f); }
    @Override public float getVoicePitch() { return 0.6f; }

    /** infect: poison + hunger + weakness */
    private static void infect(LivingEntity v, int ticks) {
        v.addEffect(new MobEffectInstance(MobEffects.POISON, ticks, 0));
        v.addEffect(new MobEffectInstance(MobEffects.HUNGER, ticks * 2, 1));
        v.addEffect(new MobEffectInstance(MobEffects.WEAKNESS, ticks * 2, 0));
    }

    private static void snd(FpeEntity e, SoundEvent s, float v, float p) { FpeUtil.sound(e, s, v, p); }

    @Override
    protected void registerAbilities(List<Ability> out) {
        // X-slash with both scythes
        out.add(Ability.of("cross", 34, 55).range(0, 6).weight(4).faceUntil(14).tick((e, t, tk) -> {
            if (tk == 14) {
                DangerBloomie.slashArc(e, 5.5f, 150, 40, 0, 1.4, 0xE8D8DCF2);
                DangerBloomie.slashArc(e, 5.5f, 150, -40, 0, 1.4, 0xE8D8DCF2);
                FpeUtil.hitCone(e, 5.5, 75, e.dmg(1.5f), 1.0, 0.4);
                snd(e, SoundEvents.PLAYER_ATTACK_SWEEP, 1.4f, 0.5f);
            }
        }));
        // 360 whirl
        out.add(Ability.of("whirl", 42, 80).range(0, 5).weight(2).faceUntil(8).tick((e, t, tk) -> {
            if (tk >= 12 && tk <= 30 && tk % 6 == 0) {
                FpeUtil.hitRadius(e, e.position(), 5.4, e.dmg(0.9f), 1.0, 0.35);
                FpeUtil.arc(e, ParticleTypes.SWEEP_ATTACK, e.position().add(0, 1.3, 0), tk * 20f, 180, 4.5, 6);
                snd(e, SoundEvents.PLAYER_ATTACK_SWEEP, 1.2f, 0.5f);
            }
        }));
        // impale: long thrust with one blade
        out.add(Ability.of("impale", 38, 70).range(3, 10).weight(3).faceUntil(15).tick((e, t, tk) -> {
            if (tk == 17) {
                Vec3 a = e.position().add(0, 1.7, 0), b = a.add(FpeUtil.forward(e).scale(9));
                if (FpeUtil.hitLine(e, a, b, 0.9, e.dmg(1.8f), 1.2, 0.3) > 0) snd(e, SoundEvents.TRIDENT_HIT, 1f, 0.6f);
                for (int i = 1; i <= 9; i++) FpeUtil.particles(e, ParticleTypes.CRIT, a.add(FpeUtil.forward(e).scale(i)), 3, 0.1, 0.1, 0.1, 0.05);
            }
        }));
        // pounce
        out.add(Ability.of("pounce", 46, 90).range(5, 15).weight(3).moving().faceUntil(15)
                .start((e, t, tk) -> ((InfectedBloomie) e).landed = false)
                .tick((e, t, tk) -> {
                    InfectedBloomie b = (InfectedBloomie) e;
                    if (tk == 16) { e.dashToward(t.position(), 1.5, 0.65); snd(e, SoundEvents.RAVAGER_ROAR, 1f, 0.8f); }
                    if (tk > 18 && !b.landed && e.onGround()) {
                        b.landed = true;
                        FpeUtil.hitRadius(e, e.position(), 4, e.dmg(1.6f), 1.4, 0.5);
                        FpeUtil.fx(e, FpeFx.Kind.RING_SHOCK, e.position().add(0, 0.1, 0), 0, 14, 7f, e.dmg(0.8f));
                        FpeUtil.particles(e, ParticleTypes.CAMPFIRE_COSY_SMOKE, e.position(), 10, 1.5, 0.1, 1.5, 0.02);
                        snd(e, SoundEvents.GENERIC_EXPLODE, 0.9f, 1.3f);
                    }
                }));
        // forelimb rake combo
        out.add(Ability.of("rake", 30, 40).range(0, 4).weight(4).faceUntil(20).tick((e, t, tk) -> {
            if (tk == 8 || tk == 14 || tk == 20) {
                for (LivingEntity v : DangerBloomie.cone(e, 3.8, 60)) { v.invulnerableTime = 0; FpeUtil.hit(e, v, e.dmg(0.8f), 0.4, 0.15); }
                snd(e, SoundEvents.PLAYER_ATTACK_SWEEP, 1f, 0.8f);
            }
        }));
        // black spit orbs
        out.add(Ability.of("spit", 40, 70).range(4, 18).weight(3).faceUntil(26).tick((e, t, tk) -> {
            if (tk == 16 || tk == 20 || tk == 24) {
                Vec3 from = e.position().add(0, 1.5, 0).add(FpeUtil.forward(e).scale(1.2));
                Vec3 v = FpeUtil.aim(from, t, 0.55, 0.3);
                double off = (tk - 20) * 0.04;
                FpeUtil.projectile(e, FpeProjectile.Kind.SHADOW_ORB, from, DangerBloomie.rotY(v, off * 57), e.dmg(0.9f));
                FpeUtil.particles(e, ParticleTypes.SQUID_INK, from, 8, 0.2, 0.2, 0.2, 0.05);
                snd(e, SoundEvents.LLAMA_SPIT, 1f, 0.5f);
            }
        }));
        // screech
        out.add(Ability.of("screech", 46, 110).range(0, 12).weight(2).blind().faceUntil(10).tick((e, t, tk) -> {
            if (tk == 14) {
                snd(e, SoundEvents.WARDEN_SONIC_BOOM, 1.4f, 0.7f);
                FpeUtil.fx(e, FpeFx.Kind.RING_SHOCK, e.position().add(0, 0.1, 0), 0, 18, 11f, e.dmg(0.5f));
            }
            if (tk >= 14 && tk <= 32 && tk % 6 == 2) {
                FpeUtil.particles(e, ParticleTypes.SONIC_BOOM, e.position().add(0, 1.8, 0).add(FpeUtil.forward(e).scale(2 + (tk - 14) * 0.3)), 1, 0, 0, 0, 0);
                for (LivingEntity v : FpeUtil.enemiesInRadius(e, e.position(), 9, 3, 1)) {
                    FpeUtil.knock(v, e.position(), 0.9, 0.25);
                    v.addEffect(new MobEffectInstance(MobEffects.BLINDNESS, 60, 0));
                }
            }
        }));
        // infected ground spikes
        out.add(Ability.of("spikes", 44, 80).range(3, 15).weight(3).faceUntil(15).tick((e, t, tk) -> {
            if (tk >= 16 && tk < 32 && tk % 2 == 0) {
                int i = (tk - 16) / 2;
                Vec3 p = e.position().add(FpeUtil.forward(e).scale(2.2 + i * 1.6));
                FpeUtil.fx(e, FpeFx.Kind.SPIKE, p, 8, 30, 1f, e.dmg(1.2f)).param(1.4f);
            }
        }));
        // bite + infect
        out.add(Ability.of("bite", 32, 50).range(0, 3.4).weight(3).faceUntil(12).tick((e, t, tk) -> {
            if (tk == 14) {
                for (LivingEntity v : DangerBloomie.cone(e, 3.2, 45))
                    if (FpeUtil.hit(e, v, e.dmg(1.3f), 0.2, 0.1)) { infect(v, 100); e.heal(4f); }
                snd(e, SoundEvents.FOX_BITE, 1.2f, 0.4f);
                FpeUtil.particles(e, DangerBloomie.BLOOD, e.position().add(0, 1.4, 0).add(FpeUtil.forward(e).scale(1.6)), 15, 0.3, 0.3, 0.3, 0.05);
            }
        }));
        // enraged blade storm
        out.add(Ability.of("blade_storm", 62, 200).range(0, 9).weight(5).when(FpeEntity::isEnraged).faceUntil(10).moving().tick((e, t, tk) -> {
            if (tk >= 10 && tk <= 46 && tk % 5 == 0) {
                FpeUtil.hitRadius(e, e.position(), 6, e.dmg(0.8f), 1.1, 0.4);
                FpeUtil.arc(e, ParticleTypes.SWEEP_ATTACK, e.position().add(0, 1.3, 0), tk * 30f, 180, 5, 8);
            }
            if (tk == 30 || tk == 40) {
                for (int i = 0; i < 12; i++) {
                    Vec3 d = DangerBloomie.rotY(new Vec3(1, 0, 0), i * 30 + tk * 3).scale(tk == 30 ? 3 : 6);
                    FpeUtil.fx(e, FpeFx.Kind.SPIKE, e.position().add(d), 8, 28, 1f, e.dmg(1f)).param(1.3f);
                }
            }
        }));
    }
}
