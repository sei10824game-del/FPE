package com.fpe.entity.characters;

import java.util.List;

import com.fpe.entity.Ability;
import com.fpe.entity.FpeCombat;
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

/** "Crazy" (original design): a jittery, cackling brawler with a rusty wrench. Fast, erratic, hard to read. Ticks match client/spec/CrazyOneSpec. */
public class CrazyOne extends FpeEntity {
    public CrazyOne(EntityType<? extends FpeEntity> type, Level level) { super(type, level); }

    @Override public Faction faction() { return Faction.WILD; }

    public static AttributeSupplier.Builder attributes() { return baseAttributes(130, 7, 0.37, 2, 0.2); }

    @Override public double preferredDistance() { return 1.8; }
    @Override protected int restTicks() { return isEnraged() ? 3 : 8; }
    @Override protected SoundEvent getAmbientSound() { return SoundEvents.WITCH_CELEBRATE; }
    @Override protected SoundEvent getHurtSound(DamageSource s) { return SoundEvents.VILLAGER_HURT; }
    @Override protected SoundEvent getDeathSound() { return SoundEvents.WITCH_DEATH; }
    @Override public float getVoicePitch() { return 1.5f; }

    private static void snd(FpeEntity e, SoundEvent s, float v, float p) { FpeUtil.sound(e, s, v, p); }

    @Override
    protected void registerAbilities(List<Ability> out) {
        out.add(Ability.of("frantic_flurry", 40, 50).range(0, 3.8).weight(4).faceUntil(30).tick((e, t, tk) -> {
            if (tk >= 8 && tk <= 32 && tk % 4 == 0) {
                for (LivingEntity v : FpeCombat.cone(e, 3.6, 70)) { v.invulnerableTime = 0; FpeUtil.hit(e, v, e.dmg(0.55f), 0.3, 0.1); }
                snd(e, SoundEvents.PLAYER_ATTACK_SWEEP, 1f, 1.3f);
            }
        }));
        out.add(Ability.of("wrench_smash", 34, 50).range(0, 4).weight(4).faceUntil(14).tick((e, t, tk) -> {
            if (tk == 17) {
                FpeUtil.hitCone(e, 4, 50, e.dmg(2f), 1.4, 0.5);
                FpeUtil.particles(e, ParticleTypes.CRIT, FpeUtil.ahead(e, 2.4, 0.8), 10, 0.4, 0.4, 0.4, 0.2);
                snd(e, SoundEvents.ANVIL_LAND, 1f, 1.1f);
            }
        }));
        out.add(Ability.of("zigzag_dash", 40, 70).range(3, 12).weight(3).moving().faceUntil(4).tick((e, t, tk) -> {
            if (tk == 6 || tk == 14 || tk == 22) {
                Vec3 side = FpeUtil.right(e).scale(tk == 14 ? -0.8 : 0.8);
                e.snapFace(t);
                e.setDeltaMovement(FpeUtil.forward(e).scale(0.9).add(side).add(0, 0.12, 0));
                e.hasImpulse = true;
            }
            if (tk >= 8 && tk <= 30 && tk % 3 == 0)
                for (LivingEntity v : FpeUtil.enemiesInRadius(e, e.position(), 2.2, 2.5, 1)) { v.invulnerableTime = 0; FpeUtil.hit(e, v, e.dmg(0.7f), 0.6, 0.2); }
        }));
        out.add(Ability.of("cackle", 44, 110).range(0, 9).weight(2).blind().faceUntil(10).tick((e, t, tk) -> {
            if (tk == 14) {
                snd(e, SoundEvents.WITCH_CELEBRATE, 1.6f, 1.2f);
                FpeUtil.fx(e, FpeFx.Kind.RING_SHOCK, e.position().add(0, 0.1, 0), 0, 14, 8f, e.dmg(0.3f));
                for (LivingEntity v : FpeUtil.enemiesInRadius(e, e.position(), 8, 3, 1)) {
                    v.addEffect(new MobEffectInstance(MobEffects.CONFUSION, 120, 0));
                    v.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 40, 1));
                    FpeUtil.knock(v, e.position(), 0.5, 0.15);
                }
            }
        }));
        out.add(Ability.of("junk_throw", 34, 55).range(4, 14).weight(3).faceUntil(16).tick((e, t, tk) -> {
            if (tk == 15 || tk == 19 || tk == 23) {
                Vec3 from = e.position().add(0, 1.4, 0).add(FpeUtil.forward(e).scale(0.8));
                Vec3 v = FpeUtil.aim(from, t, 1.1, 0.3);
                FpeUtil.projectile(e, FpeProjectile.Kind.KNIFE, from, FpeCombat.rotY(v, (tk - 19) * 5), e.dmg(0.8f));
                snd(e, SoundEvents.TRIDENT_THROW, 0.8f, 1.5f);
            }
        }));
        out.add(Ability.of("tantrum", 40, 80).range(0, 5).weight(3).faceUntil(8).tick((e, t, tk) -> {
            if (tk == 16 || tk == 24) {
                FpeUtil.hitRadius(e, e.position(), 4.4, e.dmg(1.1f), 1.2, 0.4);
                FpeUtil.fx(e, FpeFx.Kind.RING_SHOCK, e.position().add(0, 0.1, 0), 0, 10, 5.5f, 0);
                snd(e, SoundEvents.GENERIC_EXPLODE, 0.8f, 1.5f);
            }
        }));
        out.add(Ability.of("jump_scare", 36, 100).range(4, 16).weight(3).blind().faceUntil(24).tick((e, t, tk) -> {
            if (tk == 8) FpeCombat.shadowStep(e, t);
            if (tk == 20) {
                FpeUtil.hitCone(e, 3.2, 60, e.dmg(1.7f), 1.2, 0.4);
                FpeCombat.slashArc(e, 3.4f, 120, 0, 0, 1.2, 0xE0F0F0E0);
                snd(e, SoundEvents.PLAYER_ATTACK_CRIT, 1.1f, 1.2f);
            }
        }));
        out.add(Ability.of("meltdown", 60, 170).range(0, 8).weight(6).moving().when(FpeEntity::isEnraged).faceUntil(6).tick((e, t, tk) -> {
            if (tk == 8 || tk == 18 || tk == 28 || tk == 38 || tk == 48) { e.snapFace(t); e.dashForward(0.85, 0.1); }
            if (tk >= 8 && tk <= 52 && tk % 3 == 0)
                for (LivingEntity v : FpeUtil.enemiesInRadius(e, e.position(), 2.6, 2.5, 1)) { v.invulnerableTime = 0; FpeUtil.hit(e, v, e.dmg(0.6f), 0.7, 0.2); }
        }));
    }
}
