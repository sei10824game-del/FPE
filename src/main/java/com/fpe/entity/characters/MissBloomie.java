package com.fpe.entity.characters;

import java.util.List;

import com.fpe.entity.Ability;
import com.fpe.entity.FpeCombat;
import com.fpe.entity.FpeEntity;
import com.fpe.entity.FpeFx;
import com.fpe.entity.FpeUtil;

import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.Vec3;

/**
 * Miss Bloomie: the box-cutter teacher. Pure close-quarters fighter (canon: she slashes Claire's leg during the chase):
 * a long striped box-cutter blade in her left hand, big pale claws on her right. Every attack is melee or a gap-closer.
 */
public class MissBloomie extends FpeEntity {
    public MissBloomie(EntityType<? extends FpeEntity> type, Level level) { super(type, level); }

    /** victim currently held by claw_grab (server only, cleared when the grab ends) */
    private LivingEntity held;
    /** floor point the blade_pin victim is nailed to */
    private Vec3 pinAt = Vec3.ZERO;

    /** grab target: the current target if it is inside the cone, else the nearest valid enemy in it, else null */
    private static LivingEntity pick(FpeEntity e, LivingEntity t, double range, double half) {
        LivingEntity best = null;
        for (LivingEntity v : FpeCombat.cone(e, range, half)) {
            if (v == t) return t;
            if (best == null || v.distanceToSqr(e) < best.distanceToSqr(e)) best = v;
        }
        return best;
    }

    /** true while the grabbed victim is still valid; drops it otherwise */
    private boolean holding() {
        if (held != null && (held.isRemoved() || !FpeUtil.canHurt(this, held))) held = null;
        return held != null;
    }

    @Override public Faction faction() { return Faction.MISS; }

    @Override public boolean meleeFocus() { return true; }

    public static AttributeSupplier.Builder attributes() { return baseAttributes(90, 7, 0.30, 4, 0.3); }

    @Override public double preferredDistance() { return 2.5; }

    @Override protected SoundEvent getAmbientSound() { return SoundEvents.WITCH_CELEBRATE; }
    @Override protected SoundEvent getHurtSound(net.minecraft.world.damagesource.DamageSource s) { return SoundEvents.WITCH_HURT; }
    @Override protected SoundEvent getDeathSound() { return SoundEvents.WITCH_DEATH; }

    private static void swish(FpeEntity e, float pitch) { FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_SWEEP, 1.1f, pitch); }

    private static void slow(LivingEntity v, int ticks, int amp) { v.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, ticks, amp)); }

    @Override
    protected void registerAbilities(List<Ability> out) {
        // 1. claws: downward rake + backhand return rake
        out.add(Ability.of("claw_rake", 28, 40).range(0, 3.2).weight(4).faceUntil(15).tick((e, t, tk) -> {
            if (tk == 7) e.dashForward(0.3, 0.02);
            if (tk == 9 || tk == 17) {
                FpeCombat.slashArc(e, 2.6f, 120, tk == 9 ? 70 : -20, tk == 9 ? 0 : 10, 1.3, FpeCombat.SLASH);
                FpeCombat.cut(e, 3.0, 65, e.dmg(tk == 9 ? 1.0f : 1.2f), 0.5, 0.2, tk == 17 ? 40 : 0, true);
                swish(e, tk == 9 ? 1.4f : 1.1f);
            }
        }));
        // 2. the big striped box-cutter: wide horizontal sweep
        out.add(Ability.of("cleaver_slash", 34, 70).range(0, 4.2).weight(3).faceUntil(12).tick((e, t, tk) -> {
            if (tk == 8) FpeUtil.sound(e, SoundEvents.ARMOR_EQUIP_IRON, 1f, 0.6f);
            if (tk == 13) e.dashForward(0.35, 0.02);
            if (tk == 15) {
                FpeCombat.slashArc(e, 4.4f, 200, 0, 0, 1.0, FpeCombat.SLASH);
                FpeCombat.cut(e, 4.4, 100, e.dmg(1.6f), 1.1, 0.3, 0, false);
                FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_SWEEP, 1.4f, 0.6f);
            }
        }));
        // 3. canon: crouching sweep at the ankles -> hamstrung (heavy slow) + bleeding
        out.add(Ability.of("leg_slash", 26, 60).range(0, 3.6).weight(4).faceUntil(9).tick((e, t, tk) -> {
            if (tk == 8) e.dashForward(0.4, 0.0);
            if (tk == 11) {
                FpeCombat.slashArc(e, 3.2f, 150, 8, 0, 0.35, FpeCombat.SLASH_RED);
                for (LivingEntity v : FpeCombat.cone(e, 3.3, 75)) {
                    if (FpeUtil.hit(e, v, e.dmg(1.1f), 0.2, 0.05)) {
                        slow(v, 70, 2);
                        FpeCombat.bleed(e, v, 50);
                    }
                }
                swish(e, 1.6f);
                FpeUtil.particles(e, ParticleTypes.CRIT, FpeUtil.ahead(e, 1.6, 0.3), 12, 0.6, 0.1, 0.6, 0.2);
            }
        }));
        // 4. box-cutter: click the blade out three segments, then a long reaching thrust
        out.add(Ability.of("blade_extend", 34, 90).range(2.5, 6).weight(3).faceUntil(17).tick((e, t, tk) -> {
            if (tk == 6 || tk == 9 || tk == 12) FpeUtil.sound(e, SoundEvents.CROSSBOW_LOADING_MIDDLE, 1f, 1.4f + tk * 0.03f);
            if (tk == 16) e.dashForward(0.3, 0.0);
            if (tk == 18) {
                Vec3 from = e.position().add(0, 1.2, 0);
                Vec3 to = from.add(FpeUtil.forward(e).scale(5.8));
                for (LivingEntity v : FpeUtil.enemiesInRadius(e, from.lerp(to, 0.5), 3.2, 1.2, 1.2)) {
                    Vec3 p = v.position().add(0, v.getBbHeight() * 0.5, 0);
                    Vec3 seg = to.subtract(from);
                    double k = Math.max(0, Math.min(1, p.subtract(from).dot(seg) / seg.lengthSqr()));
                    if (p.distanceTo(from.add(seg.scale(k))) < 0.9 + v.getBbWidth() * 0.5 && FpeUtil.hit(e, v, e.dmg(1.6f), 0.6, 0.1))
                        FpeCombat.bleed(e, v, 50);
                }
                FpeUtil.particles(e, ParticleTypes.CRIT, from.lerp(to, 0.8), 14, 0.2, 0.2, 0.2, 0.3);
                FpeUtil.sound(e, SoundEvents.TRIDENT_THROW, 1.2f, 0.8f);
            }
            if (tk == 26) FpeUtil.sound(e, SoundEvents.CROSSBOW_LOADING_END, 1f, 1.6f);
        }));
        // 5. gap closer: low crouch, explosive lunge, point-first stab
        out.add(Ability.of("lunge_stab", 30, 70).range(3, 9).weight(4).faceUntil(12).tick((e, t, tk) -> {
            if (tk == 6) FpeUtil.sound(e, SoundEvents.WITCH_CELEBRATE, 1f, 1.5f);
            if (tk == 12) {
                e.dashToward(t.position(), Math.min(1.5, 0.4 + e.distanceTo(t) * 0.13), 0.12);
                FpeUtil.particles(e, ParticleTypes.CLOUD, e.position().add(0, 0.1, 0), 8, 0.3, 0.05, 0.3, 0.02);
            }
            if (tk == 16) {
                FpeCombat.slashArc(e, 2.4f, 40, 0, 0, 1.2, FpeCombat.SLASH);
                FpeCombat.cut(e, 2.8, 35, e.dmg(1.7f), 0.9, 0.15, 60, false);
                FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_STRONG, 1.2f, 0.9f);
            }
        }));
        // 6. heel stomp: ground shock ring around her feet
        out.add(Ability.of("stomp", 32, 70).range(0, 3.5).weight(3).tick((e, t, tk) -> {
            if (tk == 9) e.setDeltaMovement(e.getDeltaMovement().add(0, 0.25, 0));
            if (tk == 13) {
                Vec3 foot = e.position().add(FpeUtil.forward(e).scale(0.3)).add(0, 0.1, 0);
                FpeUtil.particles(e, ParticleTypes.CRIT, foot, 20, 0.8, 0.1, 0.8, 0.3);
                FpeUtil.particles(e, ParticleTypes.CLOUD, foot, 10, 0.8, 0.05, 0.8, 0.05);
                FpeUtil.sound(e, SoundEvents.ANVIL_LAND, 0.9f, 0.7f);
                FpeUtil.hitRadius(e, foot, 2.0, e.dmg(1.3f), 1.0, 0.6);
                FpeUtil.fx(e, FpeFx.Kind.RING_SHOCK, foot, 0, 10, 3.5f, e.dmg(0.8f));
            }
        }));
        // 7. hop-in high roundhouse with her stilt leg: big knockback
        out.add(Ability.of("kick_back", 38, 60).range(0, 3.2).weight(3).faceUntil(14).tick((e, t, tk) -> {
            if (tk == 12) e.dashForward(0.3, 0.05);
            if (tk == 16) {
                FpeCombat.slashArc(e, 2.6f, 110, -30, 0, 1.4, FpeCombat.SLASH);
                FpeUtil.hitCone(e, 2.8, 60, e.dmg(1.2f), 1.8, 0.55);
                FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_KNOCKBACK, 1.2f, 0.8f);
                FpeUtil.particles(e, ParticleTypes.CRIT, FpeUtil.ahead(e, 1.4, 1.4), 10, 0.3, 0.3, 0.3, 0.3);
            }
        }));
        // 8. claw grab: snatch, hoist and squeeze, then slam into the floor (stunned)
        out.add(Ability.of("claw_grab", 40, 130).range(0, 3.2).weight(2).faceUntil(10).tick((e, t, tk) -> {
            MissBloomie b = (MissBloomie) e;
            if (tk == 8) e.dashForward(0.35, 0.0);
            if (tk == 10) {
                b.held = pick(e, t, 2.8, 50);
                if (b.held != null) {
                    FpeUtil.hit(e, b.held, e.dmg(0.6f), 0, 0);
                    FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_CRIT, 1f, 0.7f);
                } else swish(e, 1.2f);
            }
            if (tk > 10 && tk < 25 && b.holding()) {
                FpeUtil.hold(e, b.held, 1.15, Math.min(1.3, (tk - 10) * 0.13), 0.3);
                if (tk == 17) {
                    b.held.invulnerableTime = 0;
                    FpeUtil.hit(e, b.held, e.dmg(0.7f), 0, 0);
                    FpeCombat.bleed(e, b.held, 40);
                }
            }
            if (tk == 25 && b.holding()) {
                LivingEntity v = b.held;
                FpeUtil.hold(e, v, 1.4, 0, 0.1);
                v.invulnerableTime = 0;
                FpeUtil.hit(e, v, e.dmg(1.5f), 0, 0);
                FpeUtil.stun(v, 30);
                FpeUtil.particles(e, ParticleTypes.CLOUD, v.position(), 14, 0.6, 0.1, 0.6, 0.05);
                FpeUtil.sound(e, SoundEvents.ANVIL_LAND, 0.8f, 1.1f);
            }
            if (tk >= 25) b.held = null;
        }).end((e, t, tk) -> ((MissBloomie) e).held = null));
        // 9. slice flurry: four fast alternating box-cutter cuts, finished by an X-cut
        out.add(Ability.of("slice_flurry", 36, 70).range(0, 3.4).weight(3).faceUntil(26).tick((e, t, tk) -> {
            if (tk == 9 || tk == 13 || tk == 17 || tk == 21) {
                int i = (tk - 9) / 4;
                e.dashForward(0.15, 0.0);
                FpeCombat.slashArc(e, 2.8f, 130, i % 2 == 0 ? 35 : -35, 0, 1.2, FpeCombat.SLASH);
                FpeCombat.cut(e, 3.0, 60, e.dmg(0.55f), 0.1, 0.05, 0, true);
                swish(e, 1.3f + i * 0.1f);
            }
            if (tk == 27) {
                e.dashForward(0.3, 0.0);
                FpeCombat.slashArc(e, 3.0f, 140, 55, 0, 1.2, FpeCombat.SLASH_RED);
                FpeCombat.slashArc(e, 3.0f, 140, -55, 0, 1.2, FpeCombat.SLASH_RED);
                FpeCombat.cut(e, 3.2, 60, e.dmg(1.3f), 0.9, 0.25, 60, true);
                FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_STRONG, 1.2f, 0.8f);
            }
        }));
        // 10. two-handed overhead chop: blade bites into the floor, cracks the ground just in front
        out.add(Ability.of("overhead_chop", 36, 70).range(0, 4).weight(3).faceUntil(16).tick((e, t, tk) -> {
            if (tk == 10) FpeUtil.sound(e, SoundEvents.TRIDENT_RETURN, 1f, 0.7f);
            if (tk == 16) e.dashForward(0.3, 0.0);
            if (tk == 18) {
                FpeCombat.slashArc(e, 3.0f, 140, 90, 0, 1.2, FpeCombat.SLASH);
                FpeCombat.cut(e, 3.4, 30, e.dmg(2.0f), 0.4, 0.2, 40, false);
                Vec3 at = FpeUtil.ahead(e, 2.0, 0.1);
                FpeUtil.hitRadius(e, at, 1.4, e.dmg(0.9f), 0.5, 0.4);
                FpeUtil.particles(e, ParticleTypes.CRIT, at, 18, 0.5, 0.1, 0.5, 0.25);
                FpeUtil.particles(e, ParticleTypes.CLOUD, at, 6, 0.4, 0.05, 0.4, 0.02);
                FpeUtil.sound(e, SoundEvents.ANVIL_LAND, 0.7f, 1.4f);
            }
            if (tk == 28) FpeUtil.sound(e, SoundEvents.ITEM_BREAK, 0.6f, 1.6f);
        }));
        // 11. pirouette cut: three spinning 360 slashes that glide her into the target
        out.add(Ability.of("pirouette_cut", 40, 100).range(0, 6).weight(3).faceUntil(8).tick((e, t, tk) -> {
            if (tk == 10 || tk == 17 || tk == 24) {
                e.dashToward(t.position(), 0.45, 0.04);
                FpeCombat.slashArc(e, 3.0f, 360, 0, 0, 1.0, FpeCombat.SLASH);
                FpeUtil.hitRadius(e, e.position().add(0, 1, 0), 2.9, e.dmg(0.8f), 0.3, 0.1);
                swish(e, 1.0f + (tk - 10) * 0.03f);
            }
            if (tk == 31) {
                FpeCombat.cut(e, 3.0, 70, e.dmg(1.1f), 0.8, 0.2, 40, true);
                FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_STRONG, 1f, 1.1f);
            }
        }));
        // 12. pounce: crouch, leap at the target, land blade-first
        out.add(Ability.of("pounce", 42, 110).range(4, 11).weight(3).faceUntil(12).tick((e, t, tk) -> {
            if (tk == 6) FpeUtil.sound(e, SoundEvents.WITCH_CELEBRATE, 1.1f, 1.3f);
            if (tk == 12) {
                e.dashToward(t.position(), Math.min(1.3, 0.3 + e.distanceTo(t) * 0.1), 0.55);
                FpeUtil.particles(e, ParticleTypes.CLOUD, e.position().add(0, 0.1, 0), 10, 0.3, 0.05, 0.3, 0.03);
                FpeUtil.sound(e, SoundEvents.GOAT_LONG_JUMP, 1f, 1.2f);
            }
            if (tk == 27) {
                Vec3 at = FpeUtil.ahead(e, 0.8, 0.1);
                FpeUtil.hitRadius(e, at, 2.6, e.dmg(1.8f), 0.8, 0.4);
                FpeCombat.cut(e, 2.6, 50, e.dmg(0.6f), 0.2, 0.1, 50, true);
                FpeUtil.fx(e, FpeFx.Kind.RING_SHOCK, at, 0, 8, 2.8f, e.dmg(0.6f));
                FpeUtil.particles(e, ParticleTypes.CRIT, at, 20, 0.6, 0.1, 0.6, 0.3);
                FpeUtil.sound(e, SoundEvents.ANVIL_LAND, 0.9f, 1.0f);
            }
        }));
        // 13. ENRAGED: three spinning cleaver slashes walking forward, then a leaping blade plunge
        out.add(Ability.of("massacre_dance", 52, 180).range(0, 5).weight(3).when(FpeEntity::isEnraged).faceUntil(10).tick((e, t, tk) -> {
            if (tk == 4) FpeUtil.sound(e, SoundEvents.WITCH_CELEBRATE, 1.4f, 1.2f);
            if (tk == 12 || tk == 20 || tk == 28) {
                e.dashToward(t.position(), 0.35, 0.05);
                FpeCombat.slashArc(e, 3.4f, 360, 0, 0, 1.0, FpeCombat.SLASH_RED);
                for (LivingEntity v : FpeUtil.enemiesInRadius(e, e.position().add(0, 1, 0), 3.3, 1.5, 1.5)) {
                    v.invulnerableTime = 0;
                    if (FpeUtil.hit(e, v, e.dmg(0.9f), 0.4, 0.15)) FpeCombat.bleed(e, v, 30);
                }
                FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_SWEEP, 1.2f, 0.8f + tk * 0.01f);
            }
            if (tk == 34) { e.dashToward(t.position(), 0.3, 0.42); FpeUtil.sound(e, SoundEvents.WITCH_CELEBRATE, 1.2f, 1.6f); }
            if (tk == 40) {
                Vec3 at = FpeUtil.ahead(e, 0.6, 0.1);
                FpeUtil.hitRadius(e, at, 3.2, e.dmg(1.9f), 1.3, 0.6);
                FpeUtil.fx(e, FpeFx.Kind.RING_SHOCK, at, 0, 10, 4.0f, e.dmg(0.8f));
                FpeUtil.particles(e, ParticleTypes.CRIT, at, 30, 1.0, 0.1, 1.0, 0.35);
                FpeUtil.particles(e, FpeCombat.BLOOD, at, 20, 1.0, 0.2, 1.0, 0.1);
                FpeUtil.sound(e, SoundEvents.ANVIL_LAND, 1.2f, 0.8f);
            }
        }));
        // 15. CC - blade pin: hop in, plunge the box-cutter through the victim's foot into the floor; it is nailed in place,
        //     she twists the blade (20) and rips it out (30); stays rooted a little longer after
        out.add(Ability.of("blade_pin", 44, 150).range(0, 3.4).weight(2).faceUntil(10).tick((e, t, tk) -> {
            MissBloomie b = (MissBloomie) e;
            if (tk == 4) FpeUtil.sound(e, SoundEvents.WITCH_CELEBRATE, 1f, 1.6f);
            if (tk == 8) e.dashForward(0.4, 0.12);
            if (tk == 12) {
                b.held = pick(e, t, 2.6, 45);
                Vec3 at = b.held != null ? b.held.position() : FpeUtil.ahead(e, 1.2, 0);
                b.pinAt = at;
                FpeUtil.particles(e, ParticleTypes.CRIT, at.add(0, 0.1, 0), 16, 0.3, 0.05, 0.3, 0.25);
                FpeUtil.sound(e, SoundEvents.TRIDENT_HIT_GROUND, 1.2f, 0.7f);
                if (b.held != null) {
                    FpeUtil.hit(e, b.held, e.dmg(1.2f), 0, 0);
                    FpeUtil.root(b.held, 46);
                    FpeCombat.bleed(e, b.held, 50);
                }
            }
            if (tk > 12 && tk < 30 && b.holding()) {
                FpeUtil.holdAt(b.held, b.pinAt);
                if (tk == 20) {
                    b.held.invulnerableTime = 0;
                    FpeUtil.hit(e, b.held, e.dmg(0.6f), 0, 0);
                    FpeUtil.particles(e, FpeCombat.BLOOD, b.pinAt.add(0, 0.3, 0), 10, 0.2, 0.2, 0.2, 0.05);
                    FpeUtil.sound(e, SoundEvents.ITEM_BREAK, 0.7f, 0.6f);
                }
            }
            if (tk == 30) {
                if (b.holding()) {
                    b.held.invulnerableTime = 0;
                    FpeUtil.hit(e, b.held, e.dmg(0.5f), 0, 0.25);
                    FpeUtil.particles(e, FpeCombat.BLOOD, b.held.position().add(0, 0.4, 0), 14, 0.2, 0.3, 0.2, 0.1);
                }
                FpeUtil.sound(e, SoundEvents.TRIDENT_RETURN, 1f, 1.3f);
                b.held = null;
            }
        }).end((e, t, tk) -> ((MissBloomie) e).held = null));
        // 16. CC - choke lift: claw seizes the throat (weapon knocked away), hoists the victim overhead, three box-cutter
        //     cuts while it dangles (22/30/38), then hurls it away dazed and stunned (44)
        out.add(Ability.of("choke_lift", 56, 200).range(0, 3.0).weight(2).faceUntil(10).tick((e, t, tk) -> {
            MissBloomie b = (MissBloomie) e;
            if (tk == 8) e.dashForward(0.4, 0.0);
            if (tk == 10) {
                b.held = pick(e, t, 2.6, 45);
                if (b.held != null) {
                    FpeUtil.disarm(b.held);
                    FpeUtil.hit(e, b.held, e.dmg(0.5f), 0, 0);
                    FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_CRIT, 1f, 0.6f);
                } else swish(e, 1.0f);
            }
            if (tk > 10 && tk < 44 && b.holding()) {
                double up = Math.min(0.6, (tk - 10) * 0.075);
                FpeUtil.hold(e, b.held, 1.0, up, 0.3);
                if (tk % 6 == 0) FpeUtil.sound(e, SoundEvents.PLAYER_HURT_DROWN, 0.6f, 1.4f);
                if (tk == 22 || tk == 30 || tk == 38) {
                    b.held.invulnerableTime = 0;
                    FpeUtil.hit(e, b.held, e.dmg(tk == 38 ? 0.9f : 0.6f), 0, 0);
                    if (tk == 38) FpeCombat.bleed(e, b.held, 50);
                    FpeCombat.slashArc(e, 2.0f, 110, tk == 30 ? -40 : 40, 0, 1.4, FpeCombat.SLASH_RED);
                    swish(e, 1.2f + (tk - 22) * 0.02f);
                }
            }
            if (tk == 44) {
                if (b.holding()) {
                    LivingEntity v = b.held;
                    v.invulnerableTime = 0;
                    FpeUtil.hit(e, v, e.dmg(0.8f), 0, 0);
                    FpeUtil.fling(v, FpeUtil.forward(e), 1.3, 0.45);
                    FpeUtil.stun(v, 30);
                    FpeUtil.daze(v, 60);
                    FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_KNOCKBACK, 1.2f, 0.7f);
                }
                b.held = null;
            }
        }).end((e, t, tk) -> ((MissBloomie) e).held = null));
        // 17. CC - terror grin: hunched creep, head cranks sideways, then she lunges her grinning face forward with claws flung wide;
        //     everyone in front is dazed (nausea/blind), frozen in fear for a moment and mobs recoil
        out.add(Ability.of("terror_grin", 34, 140).range(0, 7).weight(2).faceUntil(16).tick((e, t, tk) -> {
            if (tk == 4) FpeUtil.sound(e, SoundEvents.ITEM_BREAK, 0.6f, 0.5f);
            if (tk == 16) {
                for (LivingEntity v : FpeCombat.cone(e, 7.0, 55)) {
                    FpeUtil.daze(v, 60);
                    FpeUtil.stun(v, 14);
                    if (!(v instanceof net.minecraft.world.entity.player.Player)) FpeUtil.knock(v, e.position(), 0.6, 0.1);
                }
                FpeUtil.sound(e, SoundEvents.WITCH_CELEBRATE, 1.6f, 0.5f);
                FpeUtil.sound(e, SoundEvents.ELDER_GUARDIAN_CURSE, 0.5f, 1.6f);
                FpeUtil.particles(e, ParticleTypes.SMOKE, FpeUtil.ahead(e, 1.5, 1.6), 30, 1.2, 0.4, 1.2, 0.04);
                FpeUtil.arc(e, ParticleTypes.SQUID_INK, e.position().add(0, 1.2, 0), e.getYRot(), 55, 3.5, 24);
            }
        }));
        // 14. ENRAGED signature: the chase - three relentless dash-cuts in a row, the last one a hamstring
        out.add(Ability.of("frenzy_chase", 60, 200).range(2, 12).weight(4).when(FpeEntity::isEnraged).faceUntil(46).tick((e, t, tk) -> {
            if (tk == 4) FpeUtil.sound(e, SoundEvents.WITCH_CELEBRATE, 1.5f, 0.9f);
            if (tk == 10 || tk == 26 || tk == 42) {
                e.dashToward(t.position(), Math.min(1.4, 0.45 + e.distanceTo(t) * 0.12), 0.08);
                FpeUtil.particles(e, ParticleTypes.CLOUD, e.position().add(0, 0.1, 0), 6, 0.3, 0.05, 0.3, 0.02);
            }
            if (tk == 14 || tk == 30 || tk == 46) {
                boolean last = tk == 46;
                FpeCombat.slashArc(e, 3.0f, 160, last ? 10 : (tk == 14 ? 40 : -40), 0, last ? 0.5 : 1.2, FpeCombat.SLASH_RED);
                for (LivingEntity v : FpeCombat.cone(e, 3.1, 65)) {
                    v.invulnerableTime = 0;
                    if (FpeUtil.hit(e, v, e.dmg(last ? 1.4f : 1.0f), last ? 0.3 : 0.6, 0.15)) {
                        FpeCombat.bleed(e, v, 40);
                        if (last) slow(v, 80, 3);
                    }
                }
                swish(e, last ? 0.7f : 1.2f);
            }
        }));
    }
}
