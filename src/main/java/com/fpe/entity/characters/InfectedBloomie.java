package com.fpe.entity.characters;

import com.fpe.entity.FpeCombat;

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
 * over the back, long clawed forelimbs. Animations: assets/fpe/bbmodels/infected_bloomie.bbmodel (tools/bbgen/chars/infected_bloomie.py),
 * hit ticks below = strike peaks there.
 */
public class InfectedBloomie extends FpeEntity {
    private boolean landed;
    private Vec3 puddle = Vec3.ZERO;
    private int side = 1;

    public InfectedBloomie(EntityType<? extends FpeEntity> type, Level level) { super(type, level); }

    @Override public Faction faction() { return Faction.INFECTED; }

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
                FpeCombat.slashArc(e, 5.5f, 150, 40, 0, 1.4, 0xE8D8DCF2);
                FpeCombat.slashArc(e, 5.5f, 150, -40, 0, 1.4, 0xE8D8DCF2);
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
                for (LivingEntity v : FpeCombat.cone(e, 3.8, 60)) { v.invulnerableTime = 0; FpeUtil.hit(e, v, e.dmg(0.8f), 0.4, 0.15); }
                snd(e, SoundEvents.PLAYER_ATTACK_SWEEP, 1f, 0.8f);
            }
        }));
        // black spit orbs
        out.add(Ability.of("spit", 40, 70).range(4, 18).weight(3).faceUntil(26).tick((e, t, tk) -> {
            if (tk == 16 || tk == 20 || tk == 24) {
                Vec3 from = e.position().add(0, 1.5, 0).add(FpeUtil.forward(e).scale(1.2));
                Vec3 v = FpeUtil.aim(from, t, 0.55, 0.3);
                double off = (tk - 20) * 0.04;
                FpeUtil.projectile(e, FpeProjectile.Kind.SHADOW_ORB, from, FpeCombat.rotY(v, off * 57), e.dmg(0.9f));
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
                for (LivingEntity v : FpeCombat.cone(e, 3.2, 45))
                    if (FpeUtil.hit(e, v, e.dmg(1.3f), 0.2, 0.1)) { infect(v, 100); e.heal(4f); }
                snd(e, SoundEvents.FOX_BITE, 1.2f, 0.4f);
                FpeUtil.particles(e, FpeCombat.BLOOD, e.position().add(0, 1.4, 0).add(FpeUtil.forward(e).scale(1.6)), 15, 0.3, 0.3, 0.3, 0.05);
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
                    Vec3 d = FpeCombat.rotY(new Vec3(1, 0, 0), i * 30 + tk * 3).scale(tk == 30 ? 3 : 6);
                    FpeUtil.fx(e, FpeFx.Kind.SPIKE, e.position().add(d), 8, 28, 1f, e.dmg(1f)).param(1.3f);
                }
            }
        }));
        // hook: the serrated back-blade lashes out, snags and reels the victim in, then the knife-blade jabs
        out.add(Ability.of("hook", 38, 80).range(4, 11).weight(3).faceUntil(12).tick((e, t, tk) -> {
            if (tk == 14) {
                Vec3 a = e.position().add(0, 2.4, 0), b = a.add(FpeUtil.forward(e).scale(10)).add(0, -1.4, 0);
                for (int i = 1; i <= 10; i++) FpeUtil.particles(e, ParticleTypes.SQUID_INK, a.add(b.subtract(a).scale(i / 10.0)), 2, 0.05, 0.05, 0.05, 0.01);
                for (LivingEntity v : FpeUtil.enemiesInRadius(e, e.position(), 11, 3, 1)) {
                    Vec3 rel = v.position().subtract(e.position());
                    if (rel.horizontalDistance() < 0.1 || rel.normalize().dot(FpeUtil.forward(e)) < 0.85) continue;
                    if (FpeUtil.hit(e, v, e.dmg(1.0f), 0, 0)) {
                        Vec3 d = rel.scale(-1).normalize().scale(Math.min(1.8, rel.length() * 0.22));
                        v.setDeltaMovement(d.x, 0.45, d.z); v.hurtMarked = true;
                        FpeCombat.bleed(e, v, 60);
                    }
                }
                snd(e, SoundEvents.CHAIN_HIT, 1.4f, 0.6f);
            }
            if (tk == 24) {
                FpeUtil.hitCone(e, 4.2, 35, e.dmg(1.3f), 1.0, 0.3);
                snd(e, SoundEvents.TRIDENT_HIT, 1f, 0.7f);
            }
        }));
        // stomp: rears up on the hind legs and slams both clawed forelimbs down -> shockwave + a ring of spikes
        out.add(Ability.of("stomp", 42, 90).range(0, 6).weight(3).faceUntil(16).tick((e, t, tk) -> {
            if (tk == 20) {
                Vec3 c = FpeUtil.ahead(e, 1.8, 0);
                FpeUtil.hitRadius(e, c, 4.0, e.dmg(1.6f), 0.8, 0.7);
                FpeUtil.fx(e, FpeFx.Kind.RING_SHOCK, c.add(0, 0.1, 0), 0, 14, 6f, e.dmg(0.6f));
                for (int i = 0; i < 8; i++)
                    FpeUtil.fx(e, FpeFx.Kind.SPIKE, c.add(FpeCombat.rotY(new Vec3(3, 0, 0), i * 45)), 6, 26, 1f, e.dmg(1f)).param(1.2f);
                FpeUtil.particles(e, ParticleTypes.CAMPFIRE_COSY_SMOKE, c, 12, 1.5, 0.1, 1.5, 0.02);
                snd(e, SoundEvents.GENERIC_EXPLODE, 0.8f, 1.4f);
            }
        }));
        // ooze: retches up a stream of infected ink that leaves a lingering poison puddle on the ground
        out.add(Ability.of("ooze", 60, 110).range(3, 12).weight(2).faceUntil(14)
                .start((e, t, tk) -> ((InfectedBloomie) e).puddle = t.position())
                .tick((e, t, tk) -> {
                    InfectedBloomie b = (InfectedBloomie) e;
                    Vec3 mouth = e.position().add(0, 2.0, 0).add(FpeUtil.forward(e).scale(1.6));
                    if (tk == 14) b.puddle = t.position();
                    if (tk >= 16 && tk <= 26) {
                        Vec3 to = b.puddle.add(0, 0.1, 0);
                        for (int i = 1; i <= 6; i++) FpeUtil.particles(e, ParticleTypes.SQUID_INK, mouth.add(to.subtract(mouth).scale(i / 6.0)), 2, 0.1, 0.1, 0.1, 0.02);
                        if (tk % 3 == 1) snd(e, SoundEvents.HONEY_BLOCK_SLIDE, 1.2f, 0.4f);
                    }
                    if (tk >= 18 && tk % 4 == 2) {
                        FpeUtil.particles(e, ParticleTypes.SQUID_INK, b.puddle.add(0, 0.15, 0), 14, 1.4, 0.05, 1.4, 0.01);
                        for (LivingEntity v : FpeUtil.enemiesInRadius(e, b.puddle, 2.6, 1.5, 1)) {
                            v.invulnerableTime = 0;
                            if (FpeUtil.hit(e, v, e.dmg(0.35f), 0, 0)) {
                                infect(v, 60);
                                v.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 40, 2));
                            }
                        }
                    }
                }));
        // skitter: insect-fast sidestep, then a lunging crossed rake from the flank
        out.add(Ability.of("skitter", 32, 50).range(2, 9).weight(3).moving().faceUntil(16)
                .start((e, t, tk) -> ((InfectedBloomie) e).side = e.getRandom().nextBoolean() ? 1 : -1)
                .tick((e, t, tk) -> {
                    InfectedBloomie b = (InfectedBloomie) e;
                    if (tk == 4) {
                        Vec3 r = FpeUtil.right(e).scale(1.3 * b.side);
                        e.setDeltaMovement(r.x, 0.25, r.z); e.hurtMarked = true;
                        snd(e, SoundEvents.SPIDER_STEP, 1.2f, 1.3f);
                    }
                    if (tk == 12) e.dashToward(t.position(), 1.2, 0.2);
                    if (tk == 17) {
                        FpeCombat.slashArc(e, 4f, 140, 30 * b.side, 0, 1.2, FpeCombat.SLASH);
                        FpeCombat.cut(e, 4.0, 60, e.dmg(1.3f), 0.7, 0.25, 40, true);
                        snd(e, SoundEvents.PLAYER_ATTACK_SWEEP, 1.2f, 0.7f);
                    }
                }));
        // enraged: drives both blades into the floor; infected tendrils + spike rows burst up under the target
        out.add(Ability.of("infest", 60, 220).range(3, 16).weight(5).when(FpeEntity::isEnraged).blind().faceUntil(16).tick((e, t, tk) -> {
            if (tk == 18) {
                FpeUtil.hitRadius(e, FpeUtil.ahead(e, 1.5, 0), 2.5, e.dmg(1.2f), 0.6, 0.4);
                FpeUtil.particles(e, ParticleTypes.SQUID_INK, FpeUtil.ahead(e, 1.5, 0), 30, 1, 0.2, 1, 0.1);
                snd(e, SoundEvents.WARDEN_DIG, 1.4f, 0.8f);
            }
            if (tk == 22 || tk == 30 || tk == 38) {
                FpeUtil.fx(e, FpeFx.Kind.TENTACLE, t.position(), 8, 34, 1.4f, e.dmg(1.0f));
                for (int i = 0; i < 5; i++) {
                    Vec3 d = FpeCombat.rotY(new Vec3(2.2, 0, 0), i * 72 + tk * 7);
                    FpeUtil.fx(e, FpeFx.Kind.SPIKE, t.position().add(d), 10, 26, 1f, e.dmg(0.9f)).param(1.3f);
                }
                snd(e, SoundEvents.WARDEN_EMERGE, 0.8f, 1.4f);
            }
        }));
    }
}
