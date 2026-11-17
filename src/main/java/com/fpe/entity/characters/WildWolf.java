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

/**
 * Nameless Werewolf: the horned, black-haired humanoid woman from Kaaatie's works.
 * Claws, heavy pickaxe and close-range strength drive her combat. Fear pulses,
 * howl shockwaves and ground-pick spikes are retained mod-original interpretations.
 * Animation strike ticks are authored in tools/bbgen/chars/wild_wolf.py.
 */
public class WildWolf extends FpeEntity {
    public WildWolf(EntityType<? extends FpeEntity> type, Level level) { super(type, level); }

    @Override public Faction faction() { return Faction.WILD; }

    public static AttributeSupplier.Builder attributes() { return baseAttributes(230, 10, 0.31, 5, 0.6); }

    @Override public double preferredDistance() { return 2.8; }
    @Override protected int restTicks() { return isEnraged() ? 6 : 15; }
    @Override public boolean canFreeze() { return false; }
    @Override protected SoundEvent getAmbientSound() { return SoundEvents.WOLF_GROWL; }
    @Override protected SoundEvent getHurtSound(DamageSource s) { return SoundEvents.WOLF_HURT; }
    @Override protected SoundEvent getDeathSound() { return SoundEvents.WOLF_DEATH; }
    @Override public float getVoicePitch() { return 0.55f; }

    @Override
    public void tick() {
        super.tick();
        // fear aura: players who stay close feel dread
        if (!level().isClientSide && tickCount % 40 == 0 && isAlive())
            for (LivingEntity v : FpeUtil.enemiesInRadius(this, position(), 14, 4, 2))
                if (v instanceof net.minecraft.world.entity.player.Player) v.addEffect(new MobEffectInstance(MobEffects.DARKNESS, 60, 0, true, false));
    }

    private static void snd(FpeEntity e, SoundEvent s, float v, float p) { FpeUtil.sound(e, s, v, p); }

    @Override
    protected void registerAbilities(List<Ability> out) {
        out.add(Ability.of("pick_smash", 44, 60).range(0, 6.5).weight(4).faceUntil(18).tick((e, t, tk) -> {
            if (tk == 21) {
                Vec3 p = FpeUtil.ahead(e, 3.6, 0);
                FpeUtil.hitRadius(e, p, 3.4, e.dmg(2.2f), 1.8, 0.6);
                FpeUtil.fx(e, FpeFx.Kind.RING_SHOCK, p.add(0, 0.1, 0), 0, 12, 7f, e.dmg(0.6f));
                FpeUtil.particles(e, ParticleTypes.CAMPFIRE_COSY_SMOKE, p, 6, 1.2, 0.1, 1.2, 0.02);
                snd(e, SoundEvents.GENERIC_EXPLODE, 1.2f, 0.7f);
            }
        }));
        out.add(Ability.of("pick_sweep", 40, 55).range(0, 6).weight(4).faceUntil(14).tick((e, t, tk) -> {
            if (tk == 17) {
                FpeCombat.slashArc(e, 6f, 160, 0, 0, 1.4, 0xE0D8D4CC);
                FpeUtil.hitCone(e, 6, 85, e.dmg(1.5f), 1.4, 0.4);
                snd(e, SoundEvents.PLAYER_ATTACK_SWEEP, 1.5f, 0.45f);
            }
        }));
        out.add(Ability.of("claw_rake", 34, 40).range(0, 4.5).weight(4).faceUntil(18).tick((e, t, tk) -> {
            if (tk == 9 || tk == 15 || tk == 21) {
                for (LivingEntity v : FpeCombat.cone(e, 4.2, 65)) { v.invulnerableTime = 0; FpeUtil.hit(e, v, e.dmg(0.8f), 0.8, 0.25); }
                FpeCombat.slashArc(e, 4.4f, 130, tk == 15 ? -30 : 30, 0, 1.5, 0xE0100C08);
                snd(e, SoundEvents.PLAYER_ATTACK_SWEEP, 1.2f, 0.6f);
            }
        }));
        out.add(Ability.of("pounce", 44, 90).range(5, 15).weight(3).moving().faceUntil(14).tick((e, t, tk) -> {
            if (tk == 14) { e.dashToward(t.position(), 1.5, 0.6); snd(e, SoundEvents.WOLF_HOWL, 1f, 0.7f); }
            if (tk > 18 && tk < 34 && e.onGround()) {
                FpeUtil.hitRadius(e, e.position(), 3.6, e.dmg(1.6f), 1.4, 0.5);
                FpeUtil.fx(e, FpeFx.Kind.RING_SHOCK, e.position().add(0, 0.1, 0), 0, 12, 6f, 0);
                e.cancelAbility();
            }
        }));
        out.add(Ability.of("howl", 50, 120).range(0, 14).weight(2).blind().faceUntil(10).tick((e, t, tk) -> {
            if (tk == 14) {
                snd(e, SoundEvents.WOLF_HOWL, 2f, 0.4f);
                FpeUtil.fx(e, FpeFx.Kind.RING_SHOCK, e.position().add(0, 0.1, 0), 0, 16, 11f, e.dmg(0.4f));
            }
            if (tk >= 14 && tk <= 34 && tk % 5 == 4)
                for (LivingEntity v : FpeUtil.enemiesInRadius(e, e.position(), 10, 3, 1)) {
                    FpeUtil.knock(v, e.position(), 0.7, 0.2);
                    v.addEffect(new MobEffectInstance(MobEffects.DARKNESS, 100, 0));
                    v.addEffect(new MobEffectInstance(MobEffects.WEAKNESS, 100, 0));
                    v.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 60, 1));
                }
        }));
        out.add(Ability.of("pick_throw", 40, 70).range(5, 18).weight(3).faceUntil(16).tick((e, t, tk) -> {
            if (tk == 17) {
                Vec3 from = e.position().add(0, 2.1, 0).add(FpeUtil.forward(e).scale(1.2));
                FpeUtil.projectile(e, FpeProjectile.Kind.AXE, from, FpeUtil.aim(from, t, 1.2, 0.2), e.dmg(1.6f));
                snd(e, SoundEvents.TRIDENT_THROW, 1.2f, 0.5f);
            }
        }));
        out.add(Ability.of("ground_pick", 46, 85).range(3, 14).weight(3).faceUntil(16).tick((e, t, tk) -> {
            if (tk >= 19 && tk < 35 && tk % 2 == 1) {
                int i = (tk - 19) / 2;
                FpeUtil.fx(e, FpeFx.Kind.SPIKE, e.position().add(FpeUtil.forward(e).scale(2.4 + i * 1.5)), 6, 28, 1f, e.dmg(1.1f)).param(1.3f);
            }
        }));
        out.add(Ability.of("rampage", 66, 190).range(0, 12).weight(6).moving().when(FpeEntity::isEnraged).faceUntil(6).tick((e, t, tk) -> {
            if (tk == 8 || tk == 22 || tk == 36 || tk == 50) { e.snapFace(t); e.dashForward(1.1, 0.1); }
            if (tk == 14 || tk == 28 || tk == 42 || tk == 56) {
                FpeUtil.hitRadius(e, FpeUtil.ahead(e, 2.2, 0), 3.8, e.dmg(1.4f), 1.4, 0.4);
                FpeCombat.slashArc(e, 5.5f, 150, (tk / 14) % 2 == 0 ? 25 : -25, 0, 1.6, 0xE0E8E4DC);
                snd(e, SoundEvents.PLAYER_ATTACK_STRONG, 1.3f, 0.5f);
            }
        }));
        out.add(Ability.of("shoulder_bash", 30, 55).range(1.5, 6).weight(3).faceUntil(9).tick((e, t, tk) -> {
            if (tk == 10) e.dashToward(t.position(), 0.9, 0.05);
            if (tk == 13) {
                FpeUtil.hitCone(e, 3.8, 50, e.dmg(1.2f), 1.7, 0.25);
                snd(e, SoundEvents.PLAYER_ATTACK_KNOCKBACK, 1.2f, 0.6f);
            }
        }));
        out.add(Ability.of("claw_uppercut", 34, 60).range(0, 4).weight(3).faceUntil(11).tick((e, t, tk) -> {
            if (tk == 14) {
                FpeUtil.hitCone(e, 3.8, 65, e.dmg(1.3f), 0.6, 0.8);
                FpeCombat.slashArc(e, 3.8f, 110, 80, 0, 1.6, 0xC0464C58);
                snd(e, SoundEvents.PLAYER_ATTACK_SWEEP, 1.1f, 0.5f);
            }
        }));
        out.add(Ability.of("pick_hook", 40, 80).range(1.5, 5.5).weight(3).faceUntil(12).tick((e, t, tk) -> {
            if (tk == 17) {
                for (LivingEntity v : FpeCombat.cone(e, 5.0, 40)) {
                    if (FpeUtil.hit(e, v, e.dmg(1.1f), 0, 0)) {
                        FpeUtil.pull(v, FpeUtil.ahead(e, 1.3, 0), 0.75);
                        FpeUtil.root(v, 12);
                    }
                }
                snd(e, SoundEvents.TRIDENT_HIT, 1f, 0.6f);
            }
        }));
        out.add(Ability.of("paw_stomp", 36, 65).range(0, 3.6).weight(2).faceUntil(12).tick((e, t, tk) -> {
            if (tk == 17) {
                FpeUtil.hitRadius(e, FpeUtil.ahead(e, 1.4, 0), 2.5, e.dmg(1.35f), 0.7, 0.2);
                FpeUtil.particles(e, ParticleTypes.CAMPFIRE_COSY_SMOKE, FpeUtil.ahead(e, 1.4, 0.1), 8, 0.6, 0.1, 0.6, 0.01);
                snd(e, SoundEvents.IRON_GOLEM_STEP, 1.6f, 0.6f);
            }
        }));
    }
}
