package com.fpe.entity.characters;

import java.util.List;

import com.fpe.entity.Ability;
import com.fpe.entity.FpeEntity;
import com.fpe.entity.FpeFx;
import com.fpe.entity.FpeProjectile;
import com.fpe.entity.FpeUtil;

import net.minecraft.core.particles.DustParticleOptions;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.util.Mth;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.Vec3;
import org.joml.Vector3f;

/**
 * Mutant Lana (FPE Green, mutant 004): grinning grey-haired girl whose left side is eaten by black goo.
 * Right hand = white skull-puppet maw, left hand = black toothed bag-monster.
 * Skull snaps, double chomp, bag-monster spin, tongue lash (pull), goo spit (homing ink), tooth volley, lunge bite,
 * ink puddle with fangs, grin scream, maw trap (fling + yank), puppet feint; enraged = devour (lifesteal) + mutation burst.
 * Every tick index below matches the key poses in tools/bbgen/chars/mutant_lana.py.
 */
public class MutantLana extends FpeEntity {
    private static final DustParticleOptions INK = new DustParticleOptions(new Vector3f(0.07f, 0.06f, 0.09f), 1.6f);
    private static final DustParticleOptions BONE = new DustParticleOptions(new Vector3f(0.95f, 0.95f, 0.96f), 1.1f);
    private static final int INK_ARC = 0xD0141218;
    private static final int BONE_ARC = 0xC8F2F2F6;
    private int grabbedId = -1;
    private Vec3 puddleAt = Vec3.ZERO;

    public MutantLana(EntityType<? extends FpeEntity> type, Level level) { super(type, level); }

    @Override public Faction faction() { return Faction.MUTANT; }

    public static AttributeSupplier.Builder attributes() { return baseAttributes(90, 7, 0.32, 3, 0.3); }

    @Override public double preferredDistance() { return 2.5; }
    @Override protected int restTicks() { return isEnraged() ? 6 : 12; }

    @Override protected SoundEvent getAmbientSound() { return SoundEvents.WITCH_CELEBRATE; }
    @Override protected SoundEvent getHurtSound(DamageSource s) { return SoundEvents.SLIME_HURT; }
    @Override protected SoundEvent getDeathSound() { return SoundEvents.SLIME_DEATH; }
    @Override public float getVoicePitch() { return 1.35f; }

    // ------------------------------------------------------------------ helpers
    private void ink(Vec3 at, int n, double spread) {
        FpeUtil.particles(this, INK, at, n, spread, spread * 0.6, spread, 0.04);
        FpeUtil.particles(this, ParticleTypes.SQUID_INK, at, n / 3, spread, spread * 0.5, spread, 0.03);
    }

    private void arc(float radius, float sweep, float tilt, double y, int color) {
        FpeFx f = FpeUtil.fx(this, FpeFx.Kind.ARC, position().add(0, y, 0), 0, 7, radius, 0).param(sweep).color(color);
        f.setYRot(getYRot());
        f.setXRot(tilt);
    }

    private void chompSound(float pitch) {
        FpeUtil.sound(this, SoundEvents.EVOKER_FANGS_ATTACK, 1f, pitch);
        FpeUtil.sound(this, SoundEvents.PLAYER_ATTACK_STRONG, 0.6f, pitch * 1.2f);
    }

    /** white skull maw (right hand, in front of the chest) */
    private Vec3 skull() { return FpeUtil.ahead(this, 0.55, 1.05).add(FpeUtil.right(this).scale(0.15)); }

    /** black bag-monster (left hand) */
    private Vec3 bag() { return FpeUtil.ahead(this, 0.35, 0.75).add(FpeUtil.right(this).scale(-0.3)); }

    private static void slow(LivingEntity v, int ticks, int amp) {
        v.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, ticks, amp));
    }

    private void pull(LivingEntity v, double strength) {
        Vec3 d = position().subtract(v.position());
        Vec3 flat = new Vec3(d.x, 0, d.z);
        if (flat.lengthSqr() < 1.0) return;
        Vec3 n = flat.normalize().scale(Math.min(strength, flat.length() * 0.35));
        v.setDeltaMovement(n.x, 0.25, n.z);
        v.hurtMarked = true;
    }

    private LivingEntity grabbed() {
        Entity g = grabbedId < 0 ? null : level().getEntity(grabbedId);
        return g instanceof LivingEntity l && l.isAlive() ? l : null;
    }

    private void fan(Vec3 from, LivingEntity t, FpeProjectile.Kind kind, int n, double spreadDeg, double speed, float dmg) {
        Vec3 dir = FpeUtil.aim(from, t, speed, 0.3);
        for (int i = 0; i < n; i++) {
            double a = Math.toRadians((i - (n - 1) / 2.0) * spreadDeg);
            double c = Math.cos(a), s = Math.sin(a);
            FpeUtil.projectile(this, kind, from, new Vec3(dir.x * c - dir.z * s, dir.y, dir.x * s + dir.z * c), dmg);
        }
    }

    private void spikeRing(Vec3 c, int n, double r, int warm, float dmg, float height, double phase) {
        for (int i = 0; i < n; i++) {
            double a = phase + i * Math.PI * 2 / n;
            FpeUtil.fx(this, FpeFx.Kind.SPIKE, c.add(Math.cos(a) * r, 0, Math.sin(a) * r), warm, 30, 1.2f, dmg).param(height);
        }
    }

    // ------------------------------------------------------------------ abilities
    @Override
    protected void registerAbilities(List<Ability> out) {
        // 1. Maw snap: skull pulled back, jaw gapes, thrust + SNAP t10
        out.add(Ability.of("maw_snap", 24, 30).range(0, 3.0).weight(5).faceUntil(8).tick((e, t, k) -> {
            MutantLana l = (MutantLana) e;
            if (k == 4) FpeUtil.sound(e, SoundEvents.SKELETON_AMBIENT, 0.8f, 1.6f);
            if (k == 9) e.dashForward(0.3, 0);
            if (k == 10) {
                FpeUtil.hitCone(e, 2.9, 55, e.dmg(1.1f), 0.5, 0.15);
                l.arc(1.9f, 70, -10, 1.0, BONE_ARC);
                FpeUtil.particles(e, BONE, l.skull().add(FpeUtil.forward(e).scale(0.5)), 8, 0.2, 0.2, 0.2, 0.05);
                l.chompSound(1.4f);
            }
        }));

        // 2. Double chomp: white skull bites t9, black bag-monster swings up and bites t17
        out.add(Ability.of("double_chomp", 30, 45).range(0, 3.0).weight(4).faceUntil(15).tick((e, t, k) -> {
            MutantLana l = (MutantLana) e;
            if (k == 8 || k == 16) e.dashForward(0.25, 0);
            if (k == 9) {
                FpeUtil.hitCone(e, 2.7, 60, e.dmg(0.8f), 0.3, 0.1);
                l.arc(1.8f, 80, -15, 1.0, BONE_ARC);
                l.chompSound(1.5f);
            }
            if (k == 17) {
                t.invulnerableTime = 0;
                FpeUtil.hitCone(e, 2.9, 70, e.dmg(1.1f), 0.7, 0.3);
                l.arc(2.0f, 100, 20, 0.8, INK_ARC);
                l.ink(FpeUtil.ahead(e, 1.2, 0.9), 12, 0.3);
                l.chompSound(0.8f);
            }
        }));

        // 3. Bag swing: winds the bag-monster back, full spin (hit t14, chomp again t18)
        out.add(Ability.of("bag_swing", 34, 60).range(0, 3.2).weight(4).faceUntil(10).tick((e, t, k) -> {
            MutantLana l = (MutantLana) e;
            if (k == 6) FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_SWEEP, 1f, 0.7f);
            if (k == 14) {
                FpeUtil.hitRadius(e, e.position(), 3.0, e.dmg(1.2f), 1.0, 0.35);
                FpeUtil.arc(e, INK, e.position().add(0, 0.7, 0), e.getYRot(), 180, 2.4, 40);
                l.chompSound(0.7f);
            }
            if (k == 18) {
                for (LivingEntity v : FpeUtil.enemiesInRadius(e, e.position(), 2.6, 2, 1)) { v.invulnerableTime = 0; FpeUtil.hit(e, v, e.dmg(0.5f), 0.4, 0.1); }
                l.ink(e.position().add(0, 0.6, 0), 14, 1.2);
            }
        }));

        // 4. Tongue lash: bag-monster raised level, tongue whips out t12-14 (line hit), drags the victim in t18-21
        out.add(Ability.of("tongue_lash", 32, 70).range(2.5, 7.5).weight(4).faceUntil(12).tick((e, t, k) -> {
            MutantLana l = (MutantLana) e;
            if (k == 8) FpeUtil.sound(e, SoundEvents.FROG_TONGUE, 1f, 0.6f);
            if (k == 14) {
                Vec3 from = l.bag(), to = from.add(FpeUtil.forward(e).scale(7.5));
                FpeUtil.hitLine(e, from, to, 0.8, e.dmg(0.9f), 0, 0);
                l.grabbedId = -1;
                for (LivingEntity v : FpeUtil.enemiesInRadius(e, e.position(), 7.5, 2.5, 1)) {
                    Vec3 d = v.position().subtract(e.position());
                    if (new Vec3(d.x, 0, d.z).normalize().dot(FpeUtil.forward(e)) > 0.9) { l.grabbedId = v.getId(); break; }
                }
                for (int i = 1; i <= 7; i++) FpeUtil.particles(e, INK, from.add(FpeUtil.forward(e).scale(i)), 3, 0.08, 0.08, 0.08, 0.01);
                FpeUtil.sound(e, SoundEvents.FROG_TONGUE, 1.2f, 0.9f);
            }
            LivingEntity g = l.grabbed();
            if (g != null && k >= 18 && k <= 21) l.pull(g, 0.9);
            if (g != null && k == 22) { slow(g, 40, 1); l.chompSound(0.9f); }
        }).end((e, t, k) -> ((MutantLana) e).grabbedId = -1));

        // 5. Goo spit: bag-monster on the shoulder like a cannon, three homing ink blobs t12/18/24
        out.add(Ability.of("goo_spit", 36, 70).range(4, 14).weight(4).tick((e, t, k) -> {
            MutantLana l = (MutantLana) e;
            if (k == 10 || k == 16 || k == 22) FpeUtil.sound(e, SoundEvents.GENERIC_DRINK, 0.8f, 0.6f);
            if (k == 12 || k == 18 || k == 24) {
                Vec3 from = e.position().add(0, 1.55, 0).add(FpeUtil.right(e).scale(-0.35)).add(FpeUtil.forward(e).scale(0.3));
                FpeUtil.projectile(e, FpeProjectile.Kind.SHADOW_ORB, from, FpeUtil.aim(from, t, 0.55, 0.4), e.dmg(0.7f));
                l.ink(from, 8, 0.15);
                FpeUtil.sound(e, SoundEvents.SLIME_SQUISH, 1f, 0.7f);
            }
        }));

        // 6. Tooth volley: skull inhales (lean back) then spits a fan of five fangs t14
        out.add(Ability.of("tooth_volley", 30, 60).range(3, 12).weight(4).faceUntil(13).tick((e, t, k) -> {
            MutantLana l = (MutantLana) e;
            if (k == 6) FpeUtil.sound(e, SoundEvents.SKELETON_AMBIENT, 1f, 1.8f);
            if (k == 14) {
                l.fan(l.skull(), t, FpeProjectile.Kind.KNIFE, e.isEnraged() ? 7 : 5, 9, 1.1, e.dmg(0.55f));
                FpeUtil.particles(e, BONE, l.skull(), 10, 0.15, 0.15, 0.15, 0.08);
                FpeUtil.sound(e, SoundEvents.SKELETON_SHOOT, 1f, 1.3f);
            }
        }));

        // 7. Lunge bite: deep crouch, leaps t9-10, lands + both maws bite t17
        out.add(Ability.of("lunge_bite", 34, 70).range(3.5, 9).weight(4).faceUntil(9).tick((e, t, k) -> {
            MutantLana l = (MutantLana) e;
            if (k == 4) FpeUtil.sound(e, SoundEvents.SLIME_SQUISH, 1f, 0.8f);
            if (k == 9) { e.dashToward(t.position(), Mth.clamp(e.distanceTo(t) * 0.17, 0.5, 1.3), 0.42); FpeUtil.sound(e, SoundEvents.GOAT_LONG_JUMP, 1f, 1.2f); }
            if (k == 17) {
                FpeUtil.hitRadius(e, FpeUtil.ahead(e, 1.0, 0), 1.9, e.dmg(1.4f), 0.6, 0.3);
                l.ink(FpeUtil.ahead(e, 1.0, 0.3), 16, 0.5);
                l.arc(2.0f, 160, 0, 0.8, INK_ARC);
                l.chompSound(0.75f);
            }
        }));

        // 8. Ink puddle: slams the bag-monster into the floor t14 -> goo puddle (slows), fangs erupt under the target t20
        out.add(Ability.of("ink_puddle", 36, 90).range(0, 8).weight(3).faceUntil(12).tick((e, t, k) -> {
            MutantLana l = (MutantLana) e;
            if (k == 8) FpeUtil.sound(e, SoundEvents.SLIME_JUMP, 1f, 0.6f);
            if (k == 14) {
                l.puddleAt = FpeUtil.ahead(e, 0.8, 0);
                FpeUtil.hitRadius(e, l.puddleAt, 1.4, e.dmg(1.0f), 0.3, 0.4);
                FpeUtil.fx(e, FpeFx.Kind.SPIKE, t.position(), 6, 30, 1.2f, e.dmg(1.2f)).param(1.3f);
                FpeUtil.fx(e, FpeFx.Kind.RING_SHOCK, l.puddleAt, 0, 10, 2.5f, 0).color(INK_ARC);
                l.ink(l.puddleAt.add(0, 0.1, 0), 24, 1.0);
                FpeUtil.sound(e, SoundEvents.SLIME_BLOCK_FALL, 1.2f, 0.6f);
            }
            if (k > 14 && k <= 30 && k % 4 == 0) {
                FpeUtil.particles(e, ParticleTypes.SQUID_INK, l.puddleAt.add(0, 0.1, 0), 6, 1.0, 0.05, 1.0, 0.01);
                for (LivingEntity v : FpeUtil.enemiesInRadius(e, l.puddleAt, 2.4, 1.5, 0.5)) slow(v, 30, 2);
            }
        }));

        // 9. Grin scream: head rolls back, grin splits, shrieking shockwave t12 (weakness + nausea), pulses t16/20
        out.add(Ability.of("grin_scream", 32, 120).range(0, 5).weight(2).tick((e, t, k) -> {
            MutantLana l = (MutantLana) e;
            if (k == 4) FpeUtil.sound(e, SoundEvents.WITCH_CELEBRATE, 1f, 0.7f);
            if (k == 12) {
                FpeUtil.fx(e, FpeFx.Kind.RING_SHOCK, e.position(), 0, 14, 5.5f, e.dmg(0.7f)).color(INK_ARC);
                for (LivingEntity v : FpeUtil.enemiesInRadius(e, e.position(), 5.5, 3, 1)) {
                    v.addEffect(new MobEffectInstance(MobEffects.WEAKNESS, 80, 0));
                    v.addEffect(new MobEffectInstance(MobEffects.CONFUSION, 100, 0));
                }
                FpeUtil.sound(e, SoundEvents.GHAST_SCREAM, 1.3f, 1.4f);
            }
            if (k == 16 || k == 20) {
                FpeUtil.hitRadius(e, e.position(), 3.0, e.dmg(0.3f), 0.5, 0.1);
                FpeUtil.particles(e, ParticleTypes.SONIC_BOOM, e.position().add(0, 1.6, 0), 1, 0, 0, 0, 0);
            }
        }));

        // 10. Maw trap: flings the bag-monster out on its tongue t12 (it clamps the target), yanks it all back t22
        out.add(Ability.of("maw_trap", 34, 100).range(3, 9).weight(3).faceUntil(11).tick((e, t, k) -> {
            MutantLana l = (MutantLana) e;
            if (k == 6) FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_SWEEP, 1f, 0.6f);
            if (k == 12) {
                FpeUtil.fx(e, FpeFx.Kind.TENTACLE, t.position(), 0, 12, 1.2f, e.dmg(0.6f));
                FpeUtil.hit(e, t, e.dmg(0.6f), 0, 0);
                slow(t, 20, 4);
                l.grabbedId = t.getId();
                l.ink(t.position().add(0, 0.8, 0), 14, 0.4);
                l.chompSound(0.6f);
            }
            LivingEntity g = l.grabbed();
            if (g != null && k >= 22 && k <= 24) l.pull(g, 1.1);
            if (g != null && k == 26 && g.distanceTo(e) < 3.0) { g.invulnerableTime = 0; FpeUtil.hit(e, g, e.dmg(0.9f), 0.6, 0.3); l.chompSound(1.0f); }
        }).end((e, t, k) -> ((MutantLana) e).grabbedId = -1));

        // 11. Puppet feint: the skull "talks" (clack), sudden side-hop t14, snap t18 from the flank
        out.add(Ability.of("puppet_feint", 28, 60).range(0, 3.5).weight(3).tick((e, t, k) -> {
            MutantLana l = (MutantLana) e;
            if (k == 4 || k == 6 || k == 8 || k == 10) FpeUtil.sound(e, SoundEvents.SKELETON_STEP, 0.7f, 1.8f);
            if (k == 13) {
                Vec3 side = FpeUtil.right(e).scale(-0.55);   // hops toward her right (model +X)
                e.setDeltaMovement(side.x, 0.3, side.z);
                e.hurtMarked = true;
            }
            if (k == 17) e.snapFace(t);
            if (k == 18) {
                FpeUtil.hitCone(e, 2.8, 60, e.dmg(1.0f), 0.4, 0.2);
                l.arc(1.8f, 70, -10, 1.0, BONE_ARC);
                l.chompSound(1.6f);
            }
        }));

        // 12. Devour (enraged): both maws swell, lunge t10, three crushing chomps t16/24/32 that heal her
        out.add(Ability.of("devour", 46, 140).range(0, 4).weight(4).when(FpeEntity::isEnraged).faceUntil(30).tick((e, t, k) -> {
            MutantLana l = (MutantLana) e;
            if (k == 2) FpeUtil.sound(e, SoundEvents.RAVAGER_ROAR, 0.8f, 1.6f);
            if (k == 10) e.dashToward(t.position(), Mth.clamp(e.distanceTo(t) * 0.2, 0.3, 0.8), 0.15);
            if (k == 16 || k == 24 || k == 32) {
                t.invulnerableTime = 0;
                int n = FpeUtil.hitCone(e, 3.0, 70, e.dmg(k == 32 ? 1.4f : 0.9f), k == 32 ? 1.0 : 0.15, 0.2);
                if (n > 0) e.heal(k == 32 ? 5f : 3f);
                l.ink(FpeUtil.ahead(e, 1.2, 0.9), 14, 0.4);
                l.arc(2.2f, 90, k == 24 ? 20 : -20, 0.9, k == 24 ? INK_ARC : BONE_ARC);
                l.chompSound(k == 32 ? 0.6f : 0.9f);
                if (n > 0) FpeUtil.particles(e, ParticleTypes.HEART, e.position().add(0, 2.1, 0), 2, 0.3, 0.1, 0.3, 0);
            }
        }));

        // 13. Mutation burst (enraged): hunched, goo swells, ERUPTS t18 (inner spike ring) and t26 (outer ring)
        out.add(Ability.of("mutation_burst", 44, 160).range(0, 6).weight(3).when(FpeEntity::isEnraged).tick((e, t, k) -> {
            MutantLana l = (MutantLana) e;
            if (k < 16 && k % 3 == 0) l.ink(e.position().add(0, 1.0, 0), 6, 0.4);
            if (k == 6) FpeUtil.sound(e, SoundEvents.WARDEN_HEARTBEAT, 1.2f, 1.2f);
            if (k == 18) {
                FpeUtil.hitRadius(e, e.position(), 2.6, e.dmg(1.2f), 1.1, 0.5);
                l.spikeRing(e.position(), 8, 1.8, 0, e.dmg(0.8f), 1.2f, 0);
                l.ink(e.position().add(0, 0.8, 0), 30, 1.4);
                FpeUtil.sound(e, SoundEvents.WARDEN_SONIC_BOOM, 0.6f, 1.6f);
            }
            if (k == 26) {
                l.spikeRing(e.position(), 12, 4.0, 0, e.dmg(1.0f), 1.5f, Math.PI / 12);
                FpeUtil.fx(e, FpeFx.Kind.RING_SHOCK, e.position(), 0, 12, 5.0f, 0).color(INK_ARC);
                FpeUtil.sound(e, SoundEvents.SLIME_BLOCK_BREAK, 1.4f, 0.5f);
            }
        }));
    }
}
