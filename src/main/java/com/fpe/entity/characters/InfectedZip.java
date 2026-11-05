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
 * Infected Zip: feral ink-sketch quadruped, gaping maw, spiky mane + back, spiral hat, two bat wings and a long bristly blade tail.
 * Ticks match the animations in assets/fpe/bbmodels/infected_zip.bbmodel (tools/bbgen/chars/infected_zip.py).
 */
public class InfectedZip extends FpeEntity {
    private boolean landed;
    /** victim currently snatched / pinned / lassoed (null = nobody) */
    private LivingEntity held;
    private Vec3 snag;

    public InfectedZip(EntityType<? extends FpeEntity> type, Level level) { super(type, level); }

    @Override public Faction faction() { return Faction.INFECTED; }

    @Override public boolean meleeFocus() { return true; }

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

    /** nearest valid enemy inside a horizontal cone, or null */
    private static LivingEntity pick(FpeEntity e, double range, double half) {
        LivingEntity best = null;
        for (LivingEntity v : FpeCombat.cone(e, range, half))
            if (FpeUtil.canHurt(e, v) && (best == null || v.distanceToSqr(e) < best.distanceToSqr(e))) best = v;
        return best;
    }

    /** grab still valid? drops the victim when it died / turned invalid (creative, spectator, ally) or got torn away */
    private boolean grabbing() {
        if (held != null && (!FpeUtil.canHurt(this, held) || held.distanceTo(this) > 12)) held = null;
        return held != null;
    }

    private static InfectedZip z(FpeEntity e) { return (InfectedZip) e; }

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
        // scorpion tail: the blade tail arcs over the back and stabs far forward
        out.add(Ability.of("tail_stab", 34, 55).range(2, 6.5).weight(3).faceUntil(13).tick((e, t, tk) -> {
            if (tk == 16) {
                Vec3 from = e.position().add(0, 1.2, 0);
                FpeUtil.hitLine(e, from, from.add(FpeUtil.forward(e).scale(6.2)), 1.1, e.dmg(1.6f), 0.7, 0.2);
                for (LivingEntity v : FpeUtil.enemiesInRadius(e, from.add(FpeUtil.forward(e).scale(5)), 1.6, 2, 1)) infect(v, 80);
                FpeUtil.particles(e, ParticleTypes.SQUID_INK, from.add(FpeUtil.forward(e).scale(5)), 14, 0.2, 0.2, 0.2, 0.08);
                snd(e, SoundEvents.TRIDENT_HIT, 1.2f, 0.6f);
            }
        }));
        // wing gust: both wings beat twice, blasting enemies back and loosing ink quills
        out.add(Ability.of("wing_gust", 42, 90).range(3, 11).weight(2).faceUntil(22).tick((e, t, tk) -> {
            if (tk == 16 || tk == 26) {
                for (LivingEntity v : FpeCombat.cone(e, 9, 55)) {
                    FpeUtil.knock(v, e.position(), tk == 16 ? 1.4 : 1.0, 0.35);
                    v.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 50, 1));
                }
                FpeUtil.arc(e, ParticleTypes.CLOUD, e.position().add(0, 1.2, 0), e.getYRot(), 55, 4, 14);
                snd(e, SoundEvents.ENDER_DRAGON_FLAP, 1.4f, 0.7f);
            }
            if (tk == 17 || tk == 27) {
                Vec3 from = e.position().add(0, 2.2, 0);
                Vec3 v = FpeUtil.aim(from, t, 0.9, 0.2);
                for (int a = -20; a <= 20; a += 10) FpeUtil.projectile(e, FpeProjectile.Kind.KNIFE, from, FpeCombat.rotY(v, a), e.dmg(0.6f));
            }
        }));
        // ink tendrils: claws plunge into the floor, ink tentacles burst up under and around the target
        out.add(Ability.of("ink_tendrils", 46, 100).range(3, 14).weight(2).faceUntil(14).tick((e, t, tk) -> {
            if (tk == 14) {
                snd(e, SoundEvents.SLIME_SQUISH, 1.5f, 0.4f);
                FpeUtil.particles(e, ParticleTypes.SQUID_INK, FpeUtil.ahead(e, 1.6, 0.2), 30, 0.8, 0.1, 0.8, 0.05);
            }
            if (tk == 18) FpeUtil.fx(e, FpeFx.Kind.TENTACLE, t.position(), 6, 40, 1.4f, e.dmg(1.1f));
            if (tk == 22 || tk == 26) {
                for (int i = 0; i < 3; i++) {
                    Vec3 off = FpeCombat.rotY(new Vec3(2.4, 0, 0), i * 120 + tk * 17);
                    FpeUtil.fx(e, FpeFx.Kind.TENTACLE, t.position().add(off), 6, 34, 1.2f, e.dmg(0.8f));
                }
            }
        }));
        // enraged signature: beats its wings, rockets skyward and crashes down on the target in a spike crater
        out.add(Ability.of("dive_bomb", 60, 200).range(4, 18).weight(4).moving().when(FpeEntity::isEnraged).faceUntil(20)
                .start((e, t, tk) -> ((InfectedZip) e).landed = false)
                .tick((e, t, tk) -> {
                    InfectedZip z = (InfectedZip) e;
                    if (tk == 12) { e.setDeltaMovement(0, 1.25, 0); snd(e, SoundEvents.ENDER_DRAGON_FLAP, 1.6f, 0.6f); }
                    if (tk == 20) { e.dashToward(t.position(), 1.9, -0.9); snd(e, SoundEvents.RAVAGER_ROAR, 1.4f, 0.7f); }
                    if (tk > 21 && !z.landed && e.onGround()) {
                        z.landed = true;
                        FpeUtil.hitRadius(e, e.position(), 4.5, e.dmg(2.0f), 1.6, 0.6);
                        FpeUtil.fx(e, FpeFx.Kind.RING_SHOCK, e.position().add(0, 0.1, 0), 0, 16, 8f, e.dmg(0.8f));
                        for (int a = 0; a < 360; a += 45)
                            FpeUtil.fx(e, FpeFx.Kind.SPIKE, e.position().add(FpeCombat.rotY(new Vec3(3, 0, 0), a)), 4, 30, 1f, e.dmg(0.9f)).param(1.6f);
                        snd(e, SoundEvents.GENERIC_EXPLODE, 1.2f, 0.8f);
                    }
                }));

        // CC grab - sky snatch: lunge t9, jaws+claws snatch t10, beats into the air t14 carrying the victim (stunned, bitten t22/t30),
        // folds the wings and nose-dives t36, smashes the victim into the floor on landing and lets go
        out.add(Ability.of("sky_snatch", 64, 240).range(0, 3.8).weight(2).moving().faceUntil(10)
                .start((e, t, tk) -> { z(e).held = null; z(e).landed = false; })
                .tick((e, t, tk) -> {
                    InfectedZip z = z(e);
                    if (tk == 9) e.dashForward(0.6, 0.05);
                    if (tk == 10) {
                        LivingEntity v = pick(e, 3.6, 50);
                        if (v != null && FpeUtil.hit(e, v, e.dmg(0.5f), 0, 0)) { z.held = v; FpeUtil.stun(v, 10); }
                        snd(e, z.held != null ? SoundEvents.FOX_BITE : SoundEvents.PLAYER_ATTACK_NODAMAGE, 1.3f, 0.4f);
                    }
                    if (tk == 16 && z.held == null) { e.cancelAbility(); return; }
                    boolean g = z.grabbing();
                    if (tk == 14 && g) { e.setDeltaMovement(0, 1.05, 0); snd(e, SoundEvents.ENDER_DRAGON_FLAP, 1.6f, 0.7f); }
                    if ((tk == 21 || tk == 28) && g) {
                        Vec3 m = e.getDeltaMovement();
                        e.setDeltaMovement(m.x * 0.5, Math.max(m.y, 0.42), m.z * 0.5);
                        snd(e, SoundEvents.ENDER_DRAGON_FLAP, 1.3f, 0.8f);
                    }
                    if (g && tk > 10 && !z.landed && tk < 52) {
                        FpeUtil.hold(e, z.held, 1.45, tk < 14 ? 0.15 : -0.35, 0);
                        if (tk % 5 == 0) FpeUtil.stun(z.held, 8);
                        if (tk == 22 || tk == 30) {
                            z.held.invulnerableTime = 0;
                            if (FpeUtil.hit(e, z.held, e.dmg(0.6f), 0, 0)) { infect(z.held, 60); e.heal(3f); }
                            FpeUtil.particles(e, FpeCombat.BLOOD, z.held.position().add(0, 1.2, 0), 10, 0.3, 0.3, 0.3, 0.05);
                            snd(e, SoundEvents.FOX_BITE, 1.2f, 0.5f);
                        }
                    }
                    if (tk == 36 && g) {
                        Vec3 f = FpeUtil.forward(e);
                        e.setDeltaMovement(f.x * 0.45, -1.7, f.z * 0.45);
                        snd(e, SoundEvents.RAVAGER_ROAR, 1.4f, 0.8f);
                    }
                    if (tk > 36 && !z.landed && (e.onGround() || tk == 52)) {
                        z.landed = true;
                        if (z.grabbing()) {
                            FpeUtil.hold(e, z.held, 1.45, 0.1, 0);
                            z.held.invulnerableTime = 0;
                            FpeUtil.hit(e, z.held, e.dmg(1.5f), 0, 0);
                            FpeUtil.daze(z.held, 60);
                            FpeUtil.fling(z.held, FpeUtil.forward(e), 0.6, 0.35);
                        }
                        z.held = null;
                        FpeUtil.hitRadius(e, e.position(), 3.5, e.dmg(0.8f), 1.2, 0.4);
                        FpeUtil.fx(e, FpeFx.Kind.RING_SHOCK, e.position().add(0, 0.1, 0), 0, 14, 6f, e.dmg(0.5f));
                        snd(e, SoundEvents.GENERIC_EXPLODE, 1f, 1.1f);
                    }
                }).end((e, t, tk) -> z(e).held = null));

        // CC pin - wing pin: hop t8, slams the victim to the floor under both claws t11 (stunned), wraps it in its wings t14 (dazed),
        // gnaws t20/t28/t36 (infects), rakes it away t44
        out.add(Ability.of("wing_pin", 52, 170).range(0, 3.8).weight(2).faceUntil(9)
                .start((e, t, tk) -> z(e).held = null)
                .tick((e, t, tk) -> {
                    InfectedZip z = z(e);
                    if (tk == 8) e.dashForward(0.7, 0.3);
                    if (tk == 11) {
                        LivingEntity v = pick(e, 3.8, 55);
                        if (v != null && FpeUtil.hit(e, v, e.dmg(0.6f), 0, 0)) { z.held = v; FpeUtil.stun(v, 10); }
                        else FpeUtil.hitCone(e, 3.2, 50, e.dmg(0.8f), 0.6, 0.2);
                        snd(e, SoundEvents.RAVAGER_ATTACK, 1.2f, 0.7f);
                        FpeUtil.particles(e, ParticleTypes.SQUID_INK, FpeUtil.ahead(e, 1.5, 0.2), 16, 0.5, 0.1, 0.5, 0.05);
                    }
                    if (tk == 17 && z.held == null) { e.cancelAbility(); return; }
                    if (tk > 11 && tk < 44 && z.grabbing()) {
                        FpeUtil.hold(e, z.held, 1.5, 0, 0);
                        if (tk % 5 == 1) FpeUtil.stun(z.held, 8);
                        if (tk == 14) { FpeUtil.daze(z.held, 40); snd(e, SoundEvents.ENDER_DRAGON_FLAP, 1f, 1.2f); }
                        if (tk == 20 || tk == 28 || tk == 36) {
                            z.held.invulnerableTime = 0;
                            if (FpeUtil.hit(e, z.held, e.dmg(0.55f), 0, 0)) { infect(z.held, 50); e.heal(2f); }
                            FpeUtil.particles(e, FpeCombat.BLOOD, z.held.position().add(0, 0.5, 0), 8, 0.3, 0.2, 0.3, 0.05);
                            snd(e, SoundEvents.FOX_BITE, 1.2f, 0.45f);
                        }
                    }
                    if (tk == 44) {
                        if (z.grabbing()) { z.held.invulnerableTime = 0; FpeUtil.hit(e, z.held, e.dmg(0.8f), 1.5, 0.45); }
                        z.held = null;
                        FpeCombat.slashArc(e, 3f, 110, 20, 0, 0.5, 0xD0C8CCDC);
                        snd(e, SoundEvents.PLAYER_ATTACK_SWEEP, 1.2f, 0.6f);
                    }
                }).end((e, t, tk) -> z(e).held = null));

        // CC pull + disarm - tail lasso: tail coils over the back, lashes out t13 (line 8), wrenches the weapon away, reels the victim in
        // t14-24, hoists it overhead and squeezes t28, slams it down in front t36 (dazed) and lets go
        out.add(Ability.of("tail_lasso", 48, 150).range(2.5, 8).weight(2).faceUntil(13)
                .start((e, t, tk) -> z(e).held = null)
                .tick((e, t, tk) -> {
                    InfectedZip z = z(e);
                    if (tk == 13) {
                        LivingEntity v = pick(e, 8.2, 14);
                        if (v != null && FpeUtil.hit(e, v, e.dmg(0.5f), 0, 0)) { z.held = v; z.snag = v.position(); FpeUtil.disarm(v); FpeUtil.stun(v, 10); }
                        Vec3 from = e.position().add(0, 1.4, 0);
                        for (int i = 1; i <= 8; i++) FpeUtil.particles(e, ParticleTypes.SQUID_INK, from.add(FpeUtil.forward(e).scale(i)), 2, 0.1, 0.1, 0.1, 0.01);
                        snd(e, SoundEvents.TRIDENT_THROW, 1.2f, 0.5f);
                    }
                    if (tk == 18 && z.held == null) { e.cancelAbility(); return; }
                    if (tk > 13 && tk < 36 && z.grabbing()) {
                        if (tk <= 24) {
                            double k = (tk - 13) / 11.0;
                            FpeUtil.holdAt(z.held, z.snag.lerp(FpeUtil.ahead(e, 1.2, 2.2), k * k));
                        } else FpeUtil.hold(e, z.held, 0.6, 2.6, 0);
                        if (tk % 5 == 0) FpeUtil.stun(z.held, 8);
                        if (tk == 28) {
                            z.held.invulnerableTime = 0;
                            FpeUtil.hit(e, z.held, e.dmg(0.6f), 0, 0);
                            snd(e, SoundEvents.SLIME_SQUISH, 1.4f, 0.5f);
                        }
                    }
                    if (tk == 36) {
                        if (z.grabbing()) {
                            FpeUtil.hold(e, z.held, 1.9, 0.05, 0);
                            z.held.invulnerableTime = 0;
                            FpeUtil.hit(e, z.held, e.dmg(1.3f), 0.5, 0.25);
                            FpeUtil.daze(z.held, 60);
                            FpeUtil.particles(e, ParticleTypes.SQUID_INK, z.held.position(), 20, 0.6, 0.1, 0.6, 0.05);
                        }
                        z.held = null;
                        snd(e, SoundEvents.ANVIL_LAND, 0.8f, 0.6f);
                    }
                }).end((e, t, tk) -> z(e).held = null));
    }
}
