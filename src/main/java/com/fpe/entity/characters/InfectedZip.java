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
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.Vec3;

/**
 * Infected Zip (Basics in Survival AU): feral inked quadruped, huge maw, spiky mane, one bat-blade wing and a long blade tail.
 * Ticks match client/spec/InfectedZipSpec.
 */
public class InfectedZip extends FpeEntity {
    private boolean landed;

    public InfectedZip(EntityType<? extends FpeEntity> type, Level level) { super(type, level); }

    @Override public Faction faction() { return Faction.INFECTED; }

    public static AttributeSupplier.Builder attributes() { return baseAttributes(190, 9, 0.38, 3, 0.5); }

    @Override public double preferredDistance() { return 2.2; }
    @Override protected int restTicks() { return isEnraged() ? 5 : 13; }
    @Override public boolean causeFallDamage(float d, float m, DamageSource s) { return false; }

    @Override protected SoundEvent getAmbientSound() { return SoundEvents.RAVAGER_AMBIENT; }
    @Override protected SoundEvent getHurtSound(DamageSource s) { return SoundEvents.RAVAGER_HURT; }
    @Override protected SoundEvent getDeathSound() { return SoundEvents.RAVAGER_DEATH; }
    @Override protected void playStepSound(BlockPos p, BlockState s) { playSound(SoundEvents.RAVAGER_STEP, 0.6f, 0.7f); }

    private static void infect(LivingEntity v, int ticks) {
        v.addEffect(new MobEffectInstance(MobEffects.POISON, ticks, 0));
        v.addEffect(new MobEffectInstance(MobEffects.HUNGER, ticks * 2, 1));
        v.addEffect(new MobEffectInstance(MobEffects.WEAKNESS, ticks * 2, 0));
    }

    private static void snd(FpeEntity e, SoundEvent s, float v, float p) { FpeUtil.sound(e, s, v, p); }

    @Override
    protected void registerAbilities(List<Ability> out) {
        // maul: lunge + crunching bite that infects
        out.add(Ability.of("maul", 34, 50).range(0, 3.6).weight(4).faceUntil(12).tick((e, t, tk) -> {
            if (tk == 13) e.dashForward(0.5, 0.1);
            if (tk == 15) {
                for (LivingEntity v : FpeCombat.cone(e, 3.6, 50))
                    if (FpeUtil.hit(e, v, e.dmg(1.4f), 0.4, 0.15)) { infect(v, 100); e.heal(5f); }
                snd(e, SoundEvents.FOX_BITE, 1.3f, 0.35f);
                FpeUtil.particles(e, FpeCombat.BLOOD, e.position().add(0, 1.2, 0).add(FpeUtil.forward(e).scale(2)), 16, 0.3, 0.3, 0.3, 0.05);
            }
        }));
        // rear up, two heavy claw swipes
        out.add(Ability.of("claw", 34, 45).range(0, 4.2).weight(4).faceUntil(18).tick((e, t, tk) -> {
            if (tk == 12 || tk == 20) {
                for (LivingEntity v : FpeCombat.cone(e, 4.0, 65)) { v.invulnerableTime = 0; FpeUtil.hit(e, v, e.dmg(1f), 0.8, 0.3); }
                FpeCombat.slashArc(e, 4.2f, 120, tk == 12 ? 30 : -30, 0, 1.6, 0xD0C8CCDC);
                snd(e, SoundEvents.PLAYER_ATTACK_SWEEP, 1.2f, 0.6f);
            }
        }));
        // tail whip all around
        out.add(Ability.of("tail_sweep", 40, 70).range(0, 6).weight(3).faceUntil(8).tick((e, t, tk) -> {
            if (tk >= 12 && tk <= 26 && tk % 4 == 0) {
                FpeUtil.hitRadius(e, e.position(), 6.2, e.dmg(1f), 1.3, 0.35);
                FpeUtil.arc(e, ParticleTypes.SWEEP_ATTACK, e.position().add(0, 0.9, 0), tk * 25f, 180, 5, 8);
                snd(e, SoundEvents.PLAYER_ATTACK_SWEEP, 1.2f, 0.45f);
            }
        }));
        // wing-blade chop
        out.add(Ability.of("wing_slash", 36, 60).range(0, 7).weight(3).faceUntil(15).tick((e, t, tk) -> {
            if (tk == 17) {
                FpeCombat.slashArc(e, 6f, 100, 70, 0, 1.8, 0xE8E0E4F4);
                FpeUtil.hitCone(e, 6.2, 45, e.dmg(1.7f), 1.2, 0.45);
                snd(e, SoundEvents.PLAYER_ATTACK_SWEEP, 1.4f, 0.4f);
            }
        }));
        // pounce
        out.add(Ability.of("pounce", 44, 85).range(5, 15).weight(3).moving().faceUntil(15)
                .start((e, t, tk) -> ((InfectedZip) e).landed = false)
                .tick((e, t, tk) -> {
                    InfectedZip z = (InfectedZip) e;
                    if (tk == 14) { e.dashToward(t.position(), 1.55, 0.6); snd(e, SoundEvents.RAVAGER_ROAR, 1f, 0.9f); }
                    if (tk > 17 && !z.landed && e.onGround()) {
                        z.landed = true;
                        FpeUtil.hitRadius(e, e.position(), 4, e.dmg(1.5f), 1.4, 0.5);
                        FpeUtil.fx(e, FpeFx.Kind.RING_SHOCK, e.position().add(0, 0.1, 0), 0, 14, 7f, e.dmg(0.7f));
                        snd(e, SoundEvents.GENERIC_EXPLODE, 0.8f, 1.4f);
                    }
                }));
        // scribbled spike fan
        out.add(Ability.of("scribble", 44, 80).range(3, 15).weight(3).faceUntil(15).tick((e, t, tk) -> {
            if (tk >= 16 && tk < 34 && tk % 2 == 0) {
                int i = (tk - 16) / 2;
                for (int ang = -24; ang <= 24; ang += 24) {
                    Vec3 d = FpeCombat.rotY(FpeUtil.forward(e), ang);
                    FpeUtil.fx(e, FpeFx.Kind.SPIKE, e.position().add(d.scale(2.2 + i * 1.5)), 8, 30, 1f, e.dmg(1f)).param(1.3f);
                }
            }
        }));
        // ink orbs
        out.add(Ability.of("ink_spit", 40, 70).range(4, 18).weight(3).faceUntil(26).tick((e, t, tk) -> {
            if (tk == 16 || tk == 20 || tk == 24) {
                Vec3 from = e.position().add(0, 1.3, 0).add(FpeUtil.forward(e).scale(1.8));
                Vec3 v = FpeUtil.aim(from, t, 0.55, 0.3);
                FpeUtil.projectile(e, FpeProjectile.Kind.SHADOW_ORB, from, FpeCombat.rotY(v, (tk - 20) * 2.5), e.dmg(0.9f));
                FpeUtil.particles(e, ParticleTypes.SQUID_INK, from, 8, 0.2, 0.2, 0.2, 0.05);
                snd(e, SoundEvents.LLAMA_SPIT, 1f, 0.5f);
            }
        }));
        // roar
        out.add(Ability.of("roar", 44, 110).range(0, 12).weight(2).blind().faceUntil(10).tick((e, t, tk) -> {
            if (tk == 14) {
                snd(e, SoundEvents.RAVAGER_ROAR, 1.6f, 0.5f);
                FpeUtil.fx(e, FpeFx.Kind.RING_SHOCK, e.position().add(0, 0.1, 0), 0, 18, 11f, e.dmg(0.5f));
            }
            if (tk >= 14 && tk <= 30 && tk % 5 == 4) {
                for (LivingEntity v : FpeUtil.enemiesInRadius(e, e.position(), 9, 3, 1)) {
                    FpeUtil.knock(v, e.position(), 0.8, 0.2);
                    v.addEffect(new MobEffectInstance(MobEffects.DARKNESS, 80, 0));
                    v.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 60, 1));
                }
            }
        }));
        // enraged frenzy: three maul-dashes
        out.add(Ability.of("frenzy", 56, 180).range(0, 12).weight(5).moving().when(FpeEntity::isEnraged).faceUntil(8).tick((e, t, tk) -> {
            if (tk == 10 || tk == 24 || tk == 38) { e.snapFace(t); e.dashForward(1.2, 0.1); snd(e, SoundEvents.RAVAGER_ROAR, 0.8f, 1.1f); }
            if (tk >= 10 && tk <= 46 && tk % 3 == 0) {
                for (LivingEntity v : FpeUtil.enemiesInRadius(e, e.position().add(FpeUtil.forward(e).scale(1.5)), 2.6, 2.5, 1)) {
                    v.invulnerableTime = 0;
                    if (FpeUtil.hit(e, v, e.dmg(0.8f), 0.6, 0.25)) infect(v, 60);
                }
            }
        }));
    }
}
