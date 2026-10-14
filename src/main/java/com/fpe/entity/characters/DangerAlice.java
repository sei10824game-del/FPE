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
 * Danger AU Alice (Δlice): looks like a normal girl in a black trench coat with a yellow danger-sign pendant and a dagger under her skirt;
 * below 50 % health she is "partially transformed": six huge black spikes with claws, a long tail, a giant black claw hand, yellow slit eyes.
 * Variant 0 = human, 1 = partially transformed. Ticks match client/spec/DangerAliceSpec.
 */
public class DangerAlice extends FpeEntity {
    static final int REVEAL = 44;
    private int revealT;

    public DangerAlice(EntityType<? extends FpeEntity> type, Level level) { super(type, level); }

    @Override public Faction faction() { return Faction.DANGER_ALICE; }

    public static AttributeSupplier.Builder attributes() { return baseAttributes(260, 7, 0.33, 4, 0.4); }

    @Override public double preferredDistance() { return getVariant() == 1 ? 2.6 : 1.8; }
    @Override protected int restTicks() { return getVariant() == 0 ? 12 : isEnraged() ? 6 : 14; }
    @Override public boolean causeFallDamage(float d, float m, DamageSource s) { return false; }
    @Override protected SoundEvent getAmbientSound() { return getVariant() == 1 ? SoundEvents.WARDEN_AMBIENT : SoundEvents.VEX_AMBIENT; }
    @Override protected SoundEvent getHurtSound(DamageSource s) { return getVariant() == 1 ? SoundEvents.WARDEN_HURT : SoundEvents.VEX_HURT; }
    @Override protected SoundEvent getDeathSound() { return SoundEvents.WARDEN_DEATH; }
    @Override public float getVoicePitch() { return getVariant() == 1 ? 0.8f : 1.3f; }

    @Override
    public boolean hurt(DamageSource s, float a) { return revealT > 0 ? false : super.hurt(s, a); }

    @Override
    public void tick() {
        super.tick();
        if (level().isClientSide) return;
        if (getVariant() == 0 && revealT == 0 && isAlive() && getHealth() < getMaxHealth() * 0.5f) { revealT = 1; cancelAbility(); forceAbility("reveal"); }
        if (revealT > 0) {
            revealT++;
            getNavigation().stop();
            FpeUtil.particles(this, ParticleTypes.SQUID_INK, position().add(0, 1, 0), 3, 0.4, 0.8, 0.4, 0.04);
            if (revealT >= REVEAL) {
                revealT = 0; setVariant(1); heal(40f);
                FpeUtil.particles(this, ParticleTypes.EXPLOSION, position().add(0, 1, 0), 3, 0.5, 0.5, 0.5, 0);
                FpeUtil.fx(this, FpeFx.Kind.RING_SHOCK, position().add(0, 0.1, 0), 0, 16, 9f, dmg(0.5f));
                FpeUtil.sound(this, SoundEvents.WARDEN_ROAR, 1.5f, 1f);
            }
        }
    }

    private static boolean p(FpeEntity e, int v) { return e.getVariant() == v && ((DangerAlice) e).revealT == 0; }
    private static void snd(FpeEntity e, SoundEvent s, float v, float p) { FpeUtil.sound(e, s, v, p); }

    private static void spikeHit(FpeEntity e, LivingEntity t, int i, float dmg) {
        Vec3 from = e.position().add(0, 1.6, 0).add(FpeUtil.right(e).scale((i % 2 == 0 ? -0.3 : 0.3) * (1 + i / 2)));
        Vec3 to = from.add(t.position().add(0, t.getBbHeight() * 0.5, 0).subtract(from).normalize().scale(8));
        FpeUtil.hitLine(e, from, to, 0.7, dmg, 0.8, 0.25);
        for (int k = 1; k <= 8; k++) FpeUtil.particles(e, ParticleTypes.SQUID_INK, from.add(to.subtract(from).normalize().scale(k)), 2, 0.05, 0.05, 0.05, 0.02);
    }

    @Override
    protected void registerAbilities(List<Ability> out) {
        out.add(Ability.of("reveal", REVEAL, 99999).range(0, 99).blind().when(e -> false));
        // ---------------------------------------------------------------- human form
        out.add(Ability.of("dagger_combo", 38, 40).range(0, 3.6).weight(4).when(e -> p(e, 0)).faceUntil(16).tick((e, t, tk) -> {
            if (tk == 12 || tk == 19) {
                for (LivingEntity v : FpeCombat.cone(e, 3.2, 60)) { v.invulnerableTime = 0; FpeUtil.hit(e, v, e.dmg(0.8f), 0.5, 0.15); }
                FpeCombat.slashArc(e, 3.2f, 120, tk == 12 ? 20 : -20, 0, 1.2, 0xE0E4E8F0);
                snd(e, SoundEvents.PLAYER_ATTACK_SWEEP, 1f, 1.1f);
            }
            if (tk == 26) {
                e.dashForward(0.5, 0.05);
                for (LivingEntity v : FpeCombat.cone(e, 3.6, 35)) if (FpeUtil.hit(e, v, e.dmg(1.4f), 1.0, 0.3)) FpeCombat.bleed(e, v, 60);
                snd(e, SoundEvents.PLAYER_ATTACK_STRONG, 1f, 0.9f);
            }
        }));
        out.add(Ability.of("dagger_throw", 32, 50).range(4, 15).weight(3).when(e -> p(e, 0)).faceUntil(15).tick((e, t, tk) -> {
            if (tk == 15) {
                Vec3 from = e.position().add(0, 1.4, 0).add(FpeUtil.forward(e).scale(0.8));
                Vec3 v = FpeUtil.aim(from, t, 1.4, 0.3);
                for (int i = -1; i <= 1; i++) FpeUtil.projectile(e, FpeProjectile.Kind.KNIFE, from, FpeCombat.rotY(v, i * 7), e.dmg(0.9f));
                snd(e, SoundEvents.TRIDENT_THROW, 1f, 1.4f);
            }
        }));
        out.add(Ability.of("blink_stab", 32, 70).range(3, 15).weight(3).blind().when(e -> p(e, 0)).faceUntil(25).tick((e, t, tk) -> {
            if (tk == 8) FpeCombat.shadowStep(e, t);
            if (tk == 20) {
                for (LivingEntity v : FpeCombat.cone(e, 3.4, 40)) if (FpeUtil.hit(e, v, e.dmg(1.6f), 0.8, 0.3)) FpeCombat.bleed(e, v, 70);
                FpeCombat.slashArc(e, 3.4f, 90, 0, 0, 1.3, 0xE0F0F0F8);
                snd(e, SoundEvents.PLAYER_ATTACK_CRIT, 1f, 1f);
            }
        }));
        out.add(Ability.of("pendant_pulse", 40, 100).range(0, 8).weight(2).blind().when(e -> p(e, 0)).faceUntil(10).tick((e, t, tk) -> {
            if (tk == 16) {
                FpeUtil.fx(e, FpeFx.Kind.RING_SHOCK, e.position().add(0, 0.1, 0), 0, 14, 8f, e.dmg(0.4f)).color(0xFFFFC040);
                for (LivingEntity v : FpeUtil.enemiesInRadius(e, e.position(), 8, 3, 1)) {
                    v.addEffect(new MobEffectInstance(MobEffects.DARKNESS, 100, 0));
                    v.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 60, 0));
                }
                snd(e, SoundEvents.BELL_BLOCK, 1.5f, 0.5f);
            }
        }));
        // ---------------------------------------------------------------- partially transformed
        out.add(Ability.of("spike_barrage", 46, 70).range(3, 16).weight(4).when(e -> p(e, 1)).faceUntil(24).tick((e, t, tk) -> {
            if (tk >= 16 && tk <= 26 && (tk - 16) % 2 == 0) spikeHit(e, t, (tk - 16) / 2, e.dmg(0.8f));
        }));
        out.add(Ability.of("spike_impale", 42, 80).range(2, 10).weight(3).when(e -> p(e, 1)).faceUntil(16).tick((e, t, tk) -> {
            if (tk == 19) {
                Vec3 a = e.position().add(0, 1.5, 0), b = a.add(FpeUtil.forward(e).scale(9));
                FpeUtil.hitLine(e, a, b, 1.3, e.dmg(2f), 1.4, 0.4);
                for (int k = 1; k <= 9; k++) FpeUtil.particles(e, ParticleTypes.SQUID_INK, a.add(FpeUtil.forward(e).scale(k)), 6, 0.6, 0.5, 0.2, 0.05);
                snd(e, SoundEvents.TRIDENT_HIT, 1.2f, 0.5f);
            }
        }));
        out.add(Ability.of("claw_rake", 36, 45).range(0, 4.6).weight(4).when(e -> p(e, 1)).faceUntil(18).tick((e, t, tk) -> {
            if (tk == 10 || tk == 16 || tk == 22) {
                for (LivingEntity v : FpeCombat.cone(e, 4.4, 65)) { v.invulnerableTime = 0; FpeUtil.hit(e, v, e.dmg(0.9f), 0.7, 0.25); }
                FpeCombat.slashArc(e, 4.4f, 130, tk == 16 ? -30 : 30, 0, 1.5, 0xE0101018);
                snd(e, SoundEvents.PLAYER_ATTACK_SWEEP, 1.2f, 0.6f);
            }
        }));
        out.add(Ability.of("tail_whip", 38, 60).range(0, 6.5).weight(3).when(e -> p(e, 1)).faceUntil(8).tick((e, t, tk) -> {
            if (tk == 15 || tk == 21) {
                FpeUtil.hitRadius(e, e.position(), 6, e.dmg(1f), 1.3, 0.35);
                FpeUtil.arc(e, ParticleTypes.SWEEP_ATTACK, e.position().add(0, 0.9, 0), tk * 20f, 180, 5, 8);
                snd(e, SoundEvents.PLAYER_ATTACK_SWEEP, 1.2f, 0.45f);
            }
        }));
        out.add(Ability.of("eruption", 46, 90).range(3, 14).weight(3).when(e -> p(e, 1)).faceUntil(15).tick((e, t, tk) -> {
            if (tk >= 18 && tk < 34 && tk % 2 == 0) {
                int i = (tk - 18) / 2;
                FpeUtil.fx(e, FpeFx.Kind.SPIKE, e.position().add(FpeUtil.forward(e).scale(2.2 + i * 1.6)), 8, 30, 1f, e.dmg(1.1f)).param(1.3f);
            }
        }));
        out.add(Ability.of("welcome_home", 58, 160).range(0, 12).weight(5).blind().when(e -> p(e, 1) && e.isEnraged()).faceUntil(10).tick((e, t, tk) -> {
            if (tk == 18 || tk == 30) {
                FpeUtil.fx(e, FpeFx.Kind.RING_SHOCK, e.position().add(0, 0.1, 0), 0, 16, 11f, e.dmg(0.8f)).color(0xFF101018);
                snd(e, SoundEvents.WARDEN_SONIC_BOOM, 1.3f, 0.6f);
                for (LivingEntity v : FpeUtil.enemiesInRadius(e, e.position(), 10, 3, 1)) {
                    FpeUtil.knock(v, e.position(), 0.9, 0.3);
                    v.addEffect(new MobEffectInstance(MobEffects.DARKNESS, 120, 0));
                    v.addEffect(new MobEffectInstance(MobEffects.BLINDNESS, 50, 0));
                }
            }
            if (tk >= 36 && tk <= 52 && tk % 4 == 0) for (int i = 0; i < 6; i++) spikeHit(e, t, i, e.dmg(0.6f));
        }));
    }
}
