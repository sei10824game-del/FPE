package com.fpe.entity.characters;

import java.util.List;

import javax.annotation.Nullable;

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
 * Fen – feral long-armed predator with a curved dark blade, diamond sparkles and a little black cat.
 * Fast, aggressive melee pressure with gap closers and a few ranged punishes.
 */
public class Fen extends FpeEntity {
    private boolean struck;
    @Nullable private LivingEntity grabbed;
    private Vec3 swarm = Vec3.ZERO;

    public Fen(EntityType<? extends FpeEntity> type, Level level) { super(type, level); }

    @Override public Faction faction() { return Faction.STUDENT; }

    @Override public boolean meleeFocus() { return true; }

    public static AttributeSupplier.Builder attributes() { return baseAttributes(90, 7, 0.34, 4, 0.3); }

    @Override public double preferredDistance() { return 1.5; }
    @Override protected int restTicks() { return isEnraged() ? 6 : 14; }

    private static final int DARK = 0xE0141018, RED = 0xE08A1020;

    private void slashArc(double dist, double y, float radius, float sweep, int color, float tilt) {
        FpeFx f = FpeUtil.fx(this, FpeFx.Kind.ARC, FpeUtil.ahead(this, dist, y), 0, 7, radius, 0).param(sweep).color(color);
        f.setXRot(tilt);
    }

    private void fan(FpeProjectile.Kind kind, Vec3 from, LivingEntity t, int n, double stepDeg, double speed, float dmg) {
        Vec3 base = FpeUtil.aim(from, t, speed, 0.3);
        for (int i = 0; i < n; i++) {
            double a = Math.toRadians((i - (n - 1) / 2.0) * stepDeg);
            FpeUtil.projectile(this, kind, from, base.yRot((float) a), dmg);
        }
    }

    private Vec3 hand(boolean right, double fwd, double y) {
        return FpeUtil.ahead(this, fwd, y).add(FpeUtil.right(this).scale(right ? 0.5 : -0.5));
    }

    @Override
    protected void registerAbilities(List<Ability> out) {
        // 1 pounce – crouch, leap, claws-first landing
        out.add(Ability.of("pounce", 28, 70).range(3.5, 12).weight(3).faceUntil(9)
                .start((e, t, k) -> struck = false)
                .tick((e, t, k) -> {
                    if (k == 2) FpeUtil.sound(this, SoundEvents.CAT_HISS, 1f, 0.6f);
                    if (k == 8) {
                        double sp = Math.min(1.5, Math.max(0.6, distanceTo(t) * 0.16));
                        dashToward(t.position(), sp, 0.52);
                        FpeUtil.particles(this, ParticleTypes.CLOUD, position(), 8, 0.3, 0.05, 0.3, 0.05);
                    }
                    if (k >= 11 && k <= 19 && !struck && FpeUtil.hitCone(this, 2.3, 75, dmg(1.6f), 0.9, 0.35) > 0) {
                        struck = true;
                        FpeUtil.sound(this, SoundEvents.PHANTOM_BITE, 1f, 0.8f);
                        FpeUtil.particles(this, ParticleTypes.CRIT, FpeUtil.ahead(this, 1.2, 1), 14, 0.4, 0.4, 0.4, 0.3);
                    }
                    if (k == 16) {
                        slashArc(0.8, 0.4, 2.4f, 150, DARK, 70);
                        FpeUtil.particles(this, ParticleTypes.POOF, position(), 10, 0.6, 0.05, 0.6, 0.05);
                    }
                }));
        // 2 claw rake combo
        out.add(Ability.of("rake", 30, 40).range(0, 3.6).weight(4)
                .tick((e, t, k) -> {
                    if (k == 5 || k == 12) dashForward(0.28, getDeltaMovement().y);
                    if (k == 7 || k == 14) {
                        FpeUtil.hitCone(this, 3.2, 75, dmg(0.8f), 0.3, 0.1);
                        slashArc(1.0, 1.2, 2.8f, 140, DARK, k == 7 ? 18 : -18);
                        FpeUtil.sound(this, SoundEvents.PLAYER_ATTACK_SWEEP, 1f, 0.7f + k * 0.02f);
                    }
                    if (k == 23) {
                        FpeUtil.hitCone(this, 3.4, 60, dmg(1.2f), 0.8, 0.3);
                        slashArc(1.0, 1.0, 2.6f, 120, DARK, 85);
                        FpeUtil.sound(this, SoundEvents.PLAYER_ATTACK_STRONG, 1f, 0.6f);
                        FpeUtil.particles(this, ParticleTypes.CRIT, FpeUtil.ahead(this, 1.6, 0.6), 12, 0.5, 0.3, 0.5, 0.2);
                    }
                }));
        // 3 all-fours sprint charge
        out.add(Ability.of("sprint", 36, 90).range(5, 16).weight(2).faceUntil(26)
                .start((e, t, k) -> struck = false)
                .tick((e, t, k) -> {
                    if (k == 4) FpeUtil.sound(this, SoundEvents.FOX_SCREECH, 1f, 0.7f);
                    if (k >= 7 && k <= 27) {
                        dashForward(0.62, getDeltaMovement().y);
                        if (k % 2 == 0) FpeUtil.particles(this, ParticleTypes.CLOUD, position(), 2, 0.2, 0.02, 0.2, 0.01);
                        if (!struck && FpeUtil.hitCone(this, 1.5, 70, dmg(1.4f), 1.3, 0.45) > 0) {
                            struck = true;
                            FpeUtil.sound(this, SoundEvents.PLAYER_ATTACK_KNOCKBACK, 1f, 0.6f);
                            FpeUtil.particles(this, ParticleTypes.CRIT, FpeUtil.ahead(this, 1, 1), 12, 0.4, 0.4, 0.4, 0.3);
                        }
                    }
                    if (k == 28) setDeltaMovement(getDeltaMovement().scale(0.2));
                }));
        // 4 dark curved blade combo
        out.add(Ability.of("blade", 38, 60).range(0, 5).weight(3)
                .tick((e, t, k) -> {
                    if (k == 3) FpeUtil.sound(this, SoundEvents.ARMOR_EQUIP_IRON, 1f, 0.6f);
                    if (k == 9) dashForward(0.3, getDeltaMovement().y);
                    if (k == 10) {
                        FpeUtil.hitCone(this, 3.9, 85, dmg(1.3f), 0.6, 0.2);
                        slashArc(0.6, 1.2, 3.6f, 170, RED, 10);
                        FpeUtil.sound(this, SoundEvents.PLAYER_ATTACK_SWEEP, 1.2f, 0.5f);
                    }
                    if (k == 19) {
                        FpeUtil.hitCone(this, 3.6, 80, dmg(1.0f), 0.4, 0.1);
                        slashArc(0.6, 1.0, 3.4f, 160, RED, -12);
                        FpeUtil.projectile(this, FpeProjectile.Kind.BLADE_WAVE, hand(true, 0.8, 1.0), FpeUtil.aim(hand(true, 0.8, 1.0), t, 1.1, 0.2), dmg(0.9f));
                        FpeUtil.sound(this, SoundEvents.PLAYER_ATTACK_SWEEP, 1.2f, 0.7f);
                    }
                    if (k == 29) {
                        FpeUtil.hitCone(this, 3.3, 55, dmg(1.4f), 0.3, 0.9);
                        slashArc(0.8, 0.8, 3.0f, 150, RED, 88);
                        FpeUtil.sound(this, SoundEvents.PLAYER_ATTACK_STRONG, 1.2f, 0.5f);
                    }
                }));
        // 5 crescent – blade waves at range
        out.add(Ability.of("crescent", 34, 70).range(4.5, 15).weight(2)
                .tick((e, t, k) -> {
                    if (k < 11 && k % 3 == 0) FpeUtil.sound(this, SoundEvents.PLAYER_ATTACK_NODAMAGE, 0.8f, 1.4f);
                    if (k == 12 || k == 19) {
                        Vec3 from = hand(true, 0.8, 1.2);
                        FpeUtil.projectile(this, FpeProjectile.Kind.BLADE_WAVE, from, FpeUtil.aim(from, t, 1.15, 0.4), dmg(1.0f));
                        slashArc(0.8, 1.2, 2.8f, 150, RED, k == 12 ? 45 : -45);
                        FpeUtil.sound(this, SoundEvents.PLAYER_ATTACK_SWEEP, 1.2f, 0.6f);
                    }
                    if (k == 26 && isEnraged()) {
                        fan(FpeProjectile.Kind.BLADE_WAVE, hand(true, 0.8, 1.0), t, 3, 16, 1.1, dmg(0.8f));
                        slashArc(0.8, 1.0, 3.2f, 170, RED, 0);
                    }
                }));
        // 6 hair whip spin
        out.add(Ability.of("hairwhip", 30, 60).range(0, 4.5).weight(2)
                .tick((e, t, k) -> {
                    if (k == 9) FpeUtil.sound(this, SoundEvents.PLAYER_ATTACK_SWEEP, 1f, 1.3f);
                    if (k == 13) {
                        FpeUtil.hitRadius(this, position().add(0, 0.8, 0), 4.0, dmg(1.1f), 1.1, 0.35);
                        FpeUtil.arc(this, ParticleTypes.SWEEP_ATTACK, position().add(0, 1.0, 0), getYRot(), 180, 3.0, 10);
                        FpeUtil.arc(this, ParticleTypes.FLAME, position().add(0, 1.2, 0), getYRot(), 180, 2.4, 16);
                    }
                }));
        // 7 diamond shard volleys
        out.add(Ability.of("diamonds", 32, 70).range(4, 18).weight(3)
                .tick((e, t, k) -> {
                    if (k == 3) FpeUtil.sound(this, SoundEvents.AMETHYST_BLOCK_RESONATE, 1f, 1.2f);
                    if (k < 9) FpeUtil.particles(this, ParticleTypes.END_ROD, position().add(0, 1.8, 0), 2, 0.6, 0.5, 0.6, 0.01);
                    if (k == 9) { fan(FpeProjectile.Kind.DIAMOND, hand(true, 0.6, 1.4), t, 5, 11, 1.0, dmg(0.6f)); FpeUtil.sound(this, SoundEvents.AMETHYST_BLOCK_CHIME, 1.2f, 1.4f); }
                    if (k == 17) { fan(FpeProjectile.Kind.DIAMOND, hand(false, 0.6, 1.4), t, 5, 11, 1.0, dmg(0.6f)); FpeUtil.sound(this, SoundEvents.AMETHYST_BLOCK_CHIME, 1.2f, 1.6f); }
                    if (k == 24 && isEnraged()) { fan(FpeProjectile.Kind.DIAMOND, FpeUtil.ahead(this, 0.6, 2.0), t, 7, 9, 1.1, dmg(0.6f)); FpeUtil.sound(this, SoundEvents.AMETHYST_CLUSTER_BREAK, 1.2f, 1.2f); }
                }));
        // 8 backflip slash
        out.add(Ability.of("backflip", 32, 70).range(0, 3.2).weight(2).faceUntil(14)
                .tick((e, t, k) -> {
                    if (k == 5) { FpeUtil.hitCone(this, 2.8, 50, dmg(0.8f), 0.6, 0.2); FpeUtil.sound(this, SoundEvents.PLAYER_ATTACK_WEAK, 1f, 0.8f); }
                    if (k == 7) dashForward(-0.75, 0.55);
                    if (k == 13) {
                        Vec3 from = position().add(0, 1.4, 0);
                        FpeUtil.projectile(this, FpeProjectile.Kind.BLADE_WAVE, from, FpeUtil.aim(from, t, 1.1, 0.2), dmg(1.1f));
                        slashArc(0.3, 1.4, 2.6f, 200, DARK, 80);
                        FpeUtil.sound(this, SoundEvents.PLAYER_ATTACK_SWEEP, 1f, 0.9f);
                    }
                    if (k == 20) FpeUtil.particles(this, ParticleTypes.POOF, position(), 8, 0.4, 0.05, 0.4, 0.04);
                }));
        // 9 ground scuttle -> upward rake
        out.add(Ability.of("scuttle", 34, 80).range(3, 10).weight(2)
                .start((e, t, k) -> struck = false)
                .tick((e, t, k) -> {
                    if (k == 4) FpeUtil.sound(this, SoundEvents.SPIDER_AMBIENT, 1f, 1.3f);
                    if (k >= 6 && k <= 21 && distanceTo(t) > 1.6) {
                        dashToward(t.position(), 0.42, getDeltaMovement().y);
                        if (k % 3 == 0) FpeUtil.sound(this, SoundEvents.SPIDER_STEP, 0.6f, 1.6f);
                    }
                    if (k == 23) setDeltaMovement(0, 0.45, 0);
                    if (k == 24) {
                        FpeUtil.hitCone(this, 2.9, 80, dmg(1.5f), 0.3, 0.9);
                        slashArc(0.6, 0.6, 2.6f, 160, DARK, -85);
                        FpeUtil.sound(this, SoundEvents.PLAYER_ATTACK_STRONG, 1f, 0.7f);
                        FpeUtil.particles(this, ParticleTypes.CRIT, FpeUtil.ahead(this, 1, 1.4), 16, 0.4, 0.6, 0.4, 0.3);
                    }
                }));
        // 10 shadow-cat swarm (signature)
        out.add(Ability.of("catswarm", 42, 140).range(3, 14).weight(2)
                .tick((e, t, k) -> {
                    if (k == 9) { swarm = position(); FpeUtil.sound(this, SoundEvents.CAT_HISS, 1.4f, 0.5f); }
                    if (k >= 10 && k <= 30) {
                        swarm = swarm.lerp(t.position(), 0.18);
                        if (k % 2 == 0) {
                            Vec3 side = FpeUtil.right(this).scale(Math.sin(k * 1.3) * 0.9);
                            Vec3 p = swarm.add(side).add(0, 0.35, 0);
                            FpeUtil.particles(this, ParticleTypes.SQUID_INK, p, 5, 0.25, 0.15, 0.25, 0.02);
                            FpeUtil.particles(this, ParticleTypes.SMOKE, p, 3, 0.25, 0.1, 0.25, 0.01);
                            FpeUtil.particles(this, ParticleTypes.SMALL_FLAME, p.add(0, 0.35, 0), 2, 0.12, 0.02, 0.12, 0);
                        }
                    }
                    if (k == 16 || k == 22 || k == 28) {
                        FpeUtil.hitRadius(this, swarm, 1.9, dmg(0.7f), 0.4, 0.3);
                        FpeUtil.particles(this, ParticleTypes.SQUID_INK, swarm.add(0, 0.6, 0), 14, 0.6, 0.4, 0.6, 0.05);
                        FpeUtil.sound(this, k == 22 ? SoundEvents.CAT_HISS : SoundEvents.CAT_PURREOW, 1f, 0.6f + k * 0.01f);
                    }
                    if (k == 30 && isEnraged()) {
                        Vec3 from = position().add(0, 0.6, 0);
                        FpeUtil.projectile(this, FpeProjectile.Kind.SHADOW_ORB, from, FpeUtil.aim(from, t, 0.5, 0).yRot(0.5f), dmg(0.8f));
                        FpeUtil.projectile(this, FpeProjectile.Kind.SHADOW_ORB, from, FpeUtil.aim(from, t, 0.5, 0).yRot(-0.5f), dmg(0.8f));
                    }
                }));
        // 11 maul – canon bite / grab / slam
        out.add(Ability.of("maul", 44, 120).range(0, 2.8).weight(2)
                .start((e, t, k) -> grabbed = null)
                .tick((e, t, k) -> {
                    if (k == 5) dashForward(0.35, getDeltaMovement().y);
                    if (k == 7) {
                        FpeUtil.sound(this, SoundEvents.PHANTOM_BITE, 1.2f, 0.6f);
                        if (distanceTo(t) < 3 && FpeUtil.hit(this, t, dmg(0.8f), 0, 0)) {
                            grabbed = t;
                            t.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 40, 4));
                        }
                    }
                    LivingEntity g = grabbed;
                    if (g == null || !g.isAlive()) return;
                    if (k > 7 && k < 37) {
                        Vec3 hold = FpeUtil.ahead(this, 1.3, 0);
                        Vec3 v = hold.subtract(g.position()).scale(0.5);
                        g.setDeltaMovement(v.x, g.getDeltaMovement().y, v.z);
                        g.hurtMarked = true;
                    }
                    if (k == 14 || k == 23 || k == 32) {
                        if (FpeUtil.canHurt(this, g)) {
                            g.invulnerableTime = 0;
                            g.hurt(damageSources().mobAttack(this), dmg(0.7f));
                            g.setDeltaMovement(0, -0.9, 0);
                            g.hurtMarked = true;
                        }
                        FpeUtil.particles(this, ParticleTypes.CRIT, g.position(), 12, 0.4, 0.1, 0.4, 0.2);
                        FpeUtil.particles(this, ParticleTypes.POOF, g.position(), 6, 0.4, 0.05, 0.4, 0.04);
                        FpeUtil.sound(this, SoundEvents.PLAYER_ATTACK_CRIT, 1f, 0.6f);
                    }
                    if (k == 37) { FpeUtil.knock(g, position(), 1.6, 0.6); grabbed = null; FpeUtil.sound(this, SoundEvents.PLAYER_ATTACK_KNOCKBACK, 1f, 0.5f); }
                })
                .end((e, t, k) -> grabbed = null));
        // 12 frenzy (enraged signature)
        out.add(Ability.of("frenzy", 48, 160).range(0, 5).weight(4).when(FpeEntity::isEnraged)
                .tick((e, t, k) -> {
                    if (k == 1) { FpeUtil.sound(this, SoundEvents.RAVAGER_ROAR, 1f, 1.6f); FpeUtil.particles(this, ParticleTypes.LARGE_SMOKE, position().add(0, 1, 0), 12, 0.4, 0.6, 0.4, 0.03); }
                    for (int i = 0; i < 6; i++) {
                        int pk = 10 + 5 * i;
                        if (k == pk - 1) dashForward(0.3, getDeltaMovement().y);
                        if (k == pk) {
                            FpeUtil.hitCone(this, 3.0, 70, dmg(0.45f), 0.15, 0.05);
                            slashArc(0.9, 1.1 + (i % 3) * 0.2, 2.5f, 130, DARK, i % 2 == 0 ? 25 : -25);
                            FpeUtil.sound(this, SoundEvents.PLAYER_ATTACK_SWEEP, 0.8f, 0.9f + i * 0.08f);
                        }
                    }
                    if (k == 42) {
                        FpeUtil.hitCone(this, 3.6, 70, dmg(1.6f), 1.2, 0.45);
                        slashArc(0.8, 1.2, 3.2f, 160, RED, 50);
                        slashArc(0.8, 1.2, 3.2f, 160, RED, -50);
                        FpeUtil.sound(this, SoundEvents.PLAYER_ATTACK_STRONG, 1.3f, 0.5f);
                        FpeUtil.particles(this, ParticleTypes.CRIT, FpeUtil.ahead(this, 1.5, 1), 20, 0.6, 0.6, 0.6, 0.3);
                    }
                }));
        // 13 howl – rears up and howls: shockwave ring + fear (slow / weakness), enraged: second wave
        out.add(Ability.of("howl", 36, 150).range(0, 7).weight(2)
                .tick((e, t, k) -> {
                    if (k == 4) FpeUtil.sound(this, SoundEvents.WOLF_GROWL, 1.2f, 0.7f);
                    if (k == 13) FpeUtil.sound(this, SoundEvents.WOLF_HOWL, 1.6f, 0.8f);
                    if (k == 14 || (k == 24 && isEnraged())) {
                        FpeUtil.fx(this, FpeFx.Kind.RING_SHOCK, position().add(0, 0.1, 0), 0, 12, k == 14 ? 5.5f : 7f, 0);
                        for (LivingEntity v : FpeUtil.enemiesInRadius(this, position(), k == 14 ? 5.5 : 7, 2, 1)) {
                            FpeUtil.hit(this, v, dmg(0.6f), 0.9, 0.25);
                            v.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 60, 1));
                            v.addEffect(new MobEffectInstance(MobEffects.WEAKNESS, 80, 0));
                        }
                        FpeUtil.particles(this, ParticleTypes.SONIC_BOOM, position().add(0, 1.6, 0), 1, 0, 0, 0, 0);
                    }
                    if (k > 14 && k < 26 && k % 3 == 0) FpeUtil.particles(this, ParticleTypes.LARGE_SMOKE, position().add(0, 1.7, 0), 4, 0.3, 0.2, 0.3, 0.02);
                }));
        // 14 clawspikes – both claws plunge into the ground, a line of black claw-spikes rips toward the target
        out.add(Ability.of("clawspikes", 40, 110).range(3, 12).weight(2).faceUntil(13)
                .tick((e, t, k) -> {
                    if (k == 6) FpeUtil.sound(this, SoundEvents.FOX_SCREECH, 1f, 0.6f);
                    if (k == 14) {
                        FpeUtil.hitCone(this, 2.2, 80, dmg(1.0f), 0.4, 0.5);
                        FpeUtil.sound(this, SoundEvents.ZOMBIE_ATTACK_WOODEN_DOOR, 1f, 0.6f);
                        FpeUtil.particles(this, ParticleTypes.POOF, FpeUtil.ahead(this, 1.0, 0.1), 14, 0.6, 0.05, 0.6, 0.06);
                    }
                    if (k >= 16 && k <= 31 && (k - 16) % 3 == 0) {
                        int i = (k - 16) / 3;
                        Vec3 p = FpeUtil.ahead(this, 1.8 + i * 1.6, 0);
                        FpeUtil.fx(this, FpeFx.Kind.SPIKE, p, 3, 22, 1.1f, dmg(1.1f)).param(0.9f + i * 0.15f);
                        if (isEnraged()) {
                            Vec3 s = FpeUtil.right(this).scale(1.4);
                            FpeUtil.fx(this, FpeFx.Kind.SPIKE, p.add(s), 5, 18, 0.9f, dmg(0.8f)).param(0.7f);
                            FpeUtil.fx(this, FpeFx.Kind.SPIKE, p.subtract(s), 5, 18, 0.9f, dmg(0.8f)).param(0.7f);
                        }
                        FpeUtil.sound(this, SoundEvents.POINTED_DRIPSTONE_LAND, 1f, 0.6f + i * 0.08f);
                    }
                }));
    }

    // ------------------------------------------------------------------ sounds
    @Override protected SoundEvent getAmbientSound() { return SoundEvents.FOX_SNIFF; }
    @Override protected SoundEvent getHurtSound(DamageSource s) { return SoundEvents.FOX_HURT; }
    @Override protected SoundEvent getDeathSound() { return SoundEvents.FOX_DEATH; }
    @Override protected void playStepSound(BlockPos p, BlockState b) { playSound(SoundEvents.SPIDER_STEP, 0.25f, 1.5f); }
}
