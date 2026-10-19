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
 * Mutant Abbie (FPE Green, mutant 005): shy, hunched all-black mutant hugging herself, spiky mane with a leaf sprout,
 * a big clawed limb growing from her right hip and a jagged tail.
 * Claw swipe, double rake, tail whip (spin), tail spear (scorpion stab), limb crush (ground slam), shy lunge (leap),
 * thorn volley (mane quills), leaf boomerang, root snare (spike line), shriek, hug crush (grab + squeeze + throw),
 * curl guard (armoured ball that bursts into thorns); enraged = frenzy (slash flurry) + bramble bloom (thorn rings, heal).
 * Every tick index below matches the key poses in tools/bbgen/chars/mutant_abbie.py.
 */
public class MutantAbbie extends FpeEntity {
    private static final DustParticleOptions INK = new DustParticleOptions(new Vector3f(0.06f, 0.06f, 0.08f), 1.5f);
    private static final DustParticleOptions LEAF = new DustParticleOptions(new Vector3f(0.86f, 0.95f, 0.82f), 1.0f);
    private static final DustParticleOptions PINK = new DustParticleOptions(new Vector3f(0.85f, 0.42f, 0.52f), 1.1f);
    private static final int INK_ARC = 0xD0121116;
    private static final int PINK_ARC = 0xA0C4697C;
    private int grabbedId = -1;
    private Vec3 snareDir = Vec3.ZERO;

    public MutantAbbie(EntityType<? extends FpeEntity> type, Level level) { super(type, level); }

    @Override public Faction faction() { return Faction.MUTANT; }

    public static AttributeSupplier.Builder attributes() { return baseAttributes(90, 7, 0.32, 3, 0.3); }

    @Override public double preferredDistance() { return 2.0; }
    @Override protected int restTicks() { return isEnraged() ? 6 : 12; }

    @Override protected SoundEvent getAmbientSound() { return SoundEvents.FOX_SNIFF; }
    @Override protected SoundEvent getHurtSound(DamageSource s) { return SoundEvents.FOX_HURT; }
    @Override protected SoundEvent getDeathSound() { return SoundEvents.FOX_DEATH; }
    @Override public float getVoicePitch() { return 0.8f; }

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

    private void slashSound(float pitch) {
        FpeUtil.sound(this, SoundEvents.PLAYER_ATTACK_SWEEP, 1f, pitch);
        FpeUtil.sound(this, SoundEvents.FOX_BITE, 0.6f, pitch * 0.8f);
    }

    /** big mutant claw on her right hip */
    private Vec3 claw() { return FpeUtil.ahead(this, 0.5, 0.45).add(FpeUtil.right(this).scale(-0.55)); }

    private static void slow(LivingEntity v, int ticks, int amp) {
        v.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, ticks, amp));
    }

    private LivingEntity grabbed() {
        Entity g = grabbedId < 0 ? null : level().getEntity(grabbedId);
        return g instanceof LivingEntity l && l.isAlive() ? l : null;
    }

    /** keeps the grabbed victim pinned in front of her arms */
    private void hold(LivingEntity v) {
        Vec3 spot = FpeUtil.ahead(this, 0.9, 0);
        Vec3 d = spot.subtract(v.position());
        v.setDeltaMovement(d.x * 0.5, Math.max(-0.1, d.y * 0.3), d.z * 0.5);
        v.hurtMarked = true;
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
        // 1. Claw swipe: right claw unfolds out of the hug, cocks back, swipes across t9
        out.add(Ability.of("claw_swipe", 24, 30).range(0, 3.0).weight(5).faceUntil(7).tick((e, t, k) -> {
            MutantAbbie a = (MutantAbbie) e;
            if (k == 8) e.dashForward(0.3, 0);
            if (k == 9) {
                FpeUtil.hitCone(e, 2.9, 70, e.dmg(1.1f), 0.5, 0.15);
                a.arc(2.0f, 110, -15, 1.1, INK_ARC);
                a.slashSound(1.3f);
            }
        }));

        // 2. Double rake: right claw t8, left backhand t15
        out.add(Ability.of("double_rake", 30, 45).range(0, 3.0).weight(4).faceUntil(13).tick((e, t, k) -> {
            MutantAbbie a = (MutantAbbie) e;
            if (k == 7 || k == 14) e.dashForward(0.25, 0);
            if (k == 8 || k == 15) {
                t.invulnerableTime = 0;
                FpeUtil.hitCone(e, 2.8, 70, e.dmg(k == 8 ? 0.8f : 1.0f), k == 8 ? 0.2 : 0.6, 0.15);
                a.arc(2.0f, 110, k == 8 ? -20 : 20, 1.1, INK_ARC);
                a.slashSound(k == 8 ? 1.4f : 1.1f);
            }
        }));

        // 3. Tail whip: crouches, full spin t9-18 with the jagged tail straightened (hit t13)
        out.add(Ability.of("tail_whip", 32, 60).range(0, 3.6).weight(4).faceUntil(8).tick((e, t, k) -> {
            MutantAbbie a = (MutantAbbie) e;
            if (k == 8) FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_SWEEP, 1f, 0.6f);
            if (k == 13) {
                FpeUtil.hitRadius(e, e.position(), 3.5, e.dmg(1.1f), 1.1, 0.35);
                FpeUtil.arc(e, INK, e.position().add(0, 0.6, 0), e.getYRot(), 180, 3.0, 44);
                a.ink(e.position().add(0, 0.5, 0), 10, 1.5);
            }
        }));

        // 4. Tail spear: tail arches over the shoulder (scorpion), stabs forward t12 (long thin line)
        out.add(Ability.of("tail_spear", 28, 50).range(2, 5).weight(4).faceUntil(10).tick((e, t, k) -> {
            MutantAbbie a = (MutantAbbie) e;
            if (k == 6) FpeUtil.sound(e, SoundEvents.TRIDENT_RETURN, 0.8f, 1.4f);
            if (k == 12) {
                Vec3 from = e.position().add(0, 1.3, 0), to = from.add(FpeUtil.forward(e).scale(5.0));
                FpeUtil.hitLine(e, from, to, 0.7, e.dmg(1.3f), 0.4, 0.1);
                for (int i = 1; i <= 5; i++) FpeUtil.particles(e, INK, from.add(FpeUtil.forward(e).scale(i)), 3, 0.05, 0.05, 0.05, 0.01);
                FpeUtil.sound(e, SoundEvents.TRIDENT_THROW, 1f, 0.8f);
            }
        }));

        // 5. Limb crush: the mutant claw rears overhead, slams down in front t14 (shockwave)
        out.add(Ability.of("limb_crush", 32, 70).range(0, 3.5).weight(4).faceUntil(11).tick((e, t, k) -> {
            MutantAbbie a = (MutantAbbie) e;
            if (k == 6) FpeUtil.sound(e, SoundEvents.RAVAGER_ROAR, 0.6f, 1.6f);
            if (k == 14) {
                Vec3 at = FpeUtil.ahead(e, 1.4, 0);
                FpeUtil.hitRadius(e, at, 1.9, e.dmg(1.5f), 0.4, 0.5);
                FpeUtil.fx(e, FpeFx.Kind.RING_SHOCK, at, 0, 10, 2.6f, 0).color(INK_ARC);
                a.ink(at.add(0, 0.1, 0), 22, 0.9);
                FpeUtil.sound(e, SoundEvents.GENERIC_EXPLODE, 0.5f, 1.4f);
                FpeUtil.sound(e, SoundEvents.ANVIL_LAND, 0.4f, 0.6f);
            }
        }));

        // 6. Shy lunge: curls lower, leaps t9, lands raking with both claws t16
        out.add(Ability.of("shy_lunge", 34, 70).range(3.5, 9).weight(4).faceUntil(9).tick((e, t, k) -> {
            MutantAbbie a = (MutantAbbie) e;
            if (k == 4) FpeUtil.sound(e, SoundEvents.FOX_SNIFF, 1f, 0.7f);
            if (k == 9) { e.dashToward(t.position(), Mth.clamp(e.distanceTo(t) * 0.17, 0.5, 1.3), 0.42); FpeUtil.sound(e, SoundEvents.GOAT_LONG_JUMP, 1f, 1.1f); }
            if (k == 16) {
                FpeUtil.hitRadius(e, FpeUtil.ahead(e, 1.0, 0), 1.9, e.dmg(1.4f), 0.6, 0.3);
                a.arc(2.0f, 160, 0, 0.8, INK_ARC);
                a.ink(FpeUtil.ahead(e, 1.0, 0.3), 14, 0.5);
                a.slashSound(0.9f);
            }
        }));

        // 7. Thorn volley: ducks and shakes the mane, whips the head up t14 flinging a fan of black quills
        out.add(Ability.of("thorn_volley", 30, 60).range(3, 12).weight(4).faceUntil(13).tick((e, t, k) -> {
            MutantAbbie a = (MutantAbbie) e;
            if (k == 5 || k == 9) FpeUtil.sound(e, SoundEvents.ARMOR_EQUIP_LEATHER, 0.8f, 1.4f);
            if (k == 14) {
                Vec3 from = e.position().add(0, 1.8, 0);
                a.fan(from, t, FpeProjectile.Kind.KNIFE, e.isEnraged() ? 7 : 5, 10, 1.1, e.dmg(0.55f));
                a.ink(from, 10, 0.3);
                FpeUtil.sound(e, SoundEvents.ARROW_SHOOT, 1f, 0.8f);
            }
        }));

        // 8. Leaf boomerang: plucks the leaf off her sprout t6, sidearm throw t12 (returns), regrows
        out.add(Ability.of("leaf_boomerang", 36, 80).range(4, 14).weight(3).faceUntil(11).tick((e, t, k) -> {
            MutantAbbie a = (MutantAbbie) e;
            if (k == 6) { FpeUtil.sound(e, SoundEvents.CAVE_VINES_PICK_BERRIES, 1f, 1.2f); FpeUtil.particles(e, LEAF, e.position().add(0, 2.4, 0), 6, 0.1, 0.1, 0.1, 0.02); }
            if (k == 12) {
                Vec3 from = e.position().add(0, 1.2, 0).add(FpeUtil.right(e).scale(-0.4));
                FpeUtil.projectile(e, FpeProjectile.Kind.AXE, from, FpeUtil.aim(from, t, 0.9, 0.3), e.dmg(0.9f));
                FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_SWEEP, 1f, 1.6f);
            }
            if (k == 26) { FpeUtil.particles(e, LEAF, e.position().add(0, 2.4, 0), 8, 0.2, 0.2, 0.2, 0.02); FpeUtil.sound(e, SoundEvents.AZALEA_LEAVES_PLACE, 1f, 1.3f); }
        }));

        // 9. Root snare: plunges the mutant claw into the floor t12; black thorns race toward the target t14-22
        out.add(Ability.of("root_snare", 36, 90).range(3, 10).weight(3).faceUntil(11).tick((e, t, k) -> {
            MutantAbbie a = (MutantAbbie) e;
            if (k == 4) FpeUtil.sound(e, SoundEvents.ROOTED_DIRT_BREAK, 1f, 0.6f);
            if (k == 12) {
                Vec3 d = t.position().subtract(e.position());
                a.snareDir = new Vec3(d.x, 0, d.z).normalize();
                a.ink(a.claw(), 16, 0.4);
                FpeUtil.sound(e, SoundEvents.ROOTED_DIRT_PLACE, 1.4f, 0.5f);
            }
            if (k >= 14 && k <= 22 && k % 2 == 0) {
                int i = (k - 12) / 2;   // 1..5
                Vec3 at = e.position().add(a.snareDir.scale(1.2 + i * 1.5));
                FpeUtil.fx(e, FpeFx.Kind.SPIKE, at, 4, 26, 1.0f, e.dmg(0.9f)).param(1.0f + i * 0.12f);
            }
            if (k == 22) {
                FpeUtil.fx(e, FpeFx.Kind.TENTACLE, t.position(), 4, 24, 1.2f, e.dmg(0.4f));
                for (LivingEntity v : FpeUtil.enemiesInRadius(e, t.position(), 1.8, 1.5, 0.5)) slow(v, 40, 2);
            }
        }).end((e, t, k) -> ((MutantAbbie) e).snareDir = Vec3.ZERO));

        // 10. Shriek: uncurls, flings arms wide, faint pink mouth gapes - shockwave t12 (weakness + darkness), pulses t16/t20
        out.add(Ability.of("shriek", 32, 120).range(0, 5).weight(2).tick((e, t, k) -> {
            MutantAbbie a = (MutantAbbie) e;
            if (k == 4) FpeUtil.sound(e, SoundEvents.FOX_SCREECH, 1f, 0.7f);
            if (k == 12) {
                FpeUtil.fx(e, FpeFx.Kind.RING_SHOCK, e.position(), 0, 14, 5.5f, e.dmg(0.7f)).color(PINK_ARC);
                for (LivingEntity v : FpeUtil.enemiesInRadius(e, e.position(), 5.5, 3, 1)) {
                    v.addEffect(new MobEffectInstance(MobEffects.WEAKNESS, 80, 0));
                    v.addEffect(new MobEffectInstance(MobEffects.DARKNESS, 60, 0));
                }
                FpeUtil.particles(e, PINK, e.position().add(0, 1.7, 0), 16, 0.4, 0.3, 0.4, 0.1);
                FpeUtil.sound(e, SoundEvents.GHAST_SCREAM, 1.2f, 1.3f);
            }
            if (k == 16 || k == 20) {
                FpeUtil.hitRadius(e, e.position(), 3.0, e.dmg(0.3f), 0.5, 0.1);
                FpeUtil.particles(e, ParticleTypes.SONIC_BOOM, e.position().add(0, 1.6, 0), 1, 0, 0, 0, 0);
            }
        }));

        // 11. Hug crush: arms thrown open, lunges + clamps t10, squeezes t14/20/26, flings the victim aside t32
        out.add(Ability.of("hug_crush", 40, 100).range(0, 3.2).weight(3).faceUntil(9).tick((e, t, k) -> {
            MutantAbbie a = (MutantAbbie) e;
            if (k == 8) e.dashForward(0.45, 0);
            if (k == 10) {
                a.grabbedId = -1;
                if (e.distanceTo(t) < 2.6) { a.grabbedId = t.getId(); FpeUtil.hit(e, t, e.dmg(0.5f), 0, 0); }
                FpeUtil.sound(e, SoundEvents.FOX_BITE, 1f, 0.6f);
            }
            LivingEntity g = a.grabbed();
            if (g != null && k > 10 && k < 32) a.hold(g);
            if (g != null && (k == 14 || k == 20 || k == 26)) {
                g.invulnerableTime = 0;
                FpeUtil.hit(e, g, e.dmg(0.6f), 0, 0);
                a.ink(g.position().add(0, 1.0, 0), 8, 0.3);
                FpeUtil.sound(e, SoundEvents.SLIME_SQUISH, 1f, 0.6f);
            }
            if (g != null && k == 32) {
                g.invulnerableTime = 0;
                FpeUtil.hit(e, g, e.dmg(0.8f), 0, 0);
                Vec3 side = FpeUtil.right(e).scale(1.2).add(FpeUtil.forward(e).scale(0.6));
                g.setDeltaMovement(side.x, 0.55, side.z);
                g.hurtMarked = true;
                FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_KNOCKBACK, 1f, 0.7f);
            }
        }).end((e, t, k) -> ((MutantAbbie) e).grabbedId = -1));

        // 12. Curl guard: curls into a spiky armoured ball t0-24 (resistance), BURSTS t26 into a thorn ring
        out.add(Ability.of("curl_guard", 40, 140).range(0, 4.5).weight(2).tick((e, t, k) -> {
            MutantAbbie a = (MutantAbbie) e;
            if (k == 2) {
                e.addEffect(new MobEffectInstance(MobEffects.DAMAGE_RESISTANCE, 24, 2, false, false));
                FpeUtil.sound(e, SoundEvents.ARMOR_EQUIP_NETHERITE, 1f, 0.6f);
            }
            if (k > 4 && k < 24 && k % 4 == 0) a.ink(e.position().add(0, 0.5, 0), 4, 0.4);
            if (k == 26) {
                FpeUtil.hitRadius(e, e.position(), 3.0, e.dmg(1.2f), 1.2, 0.5);
                a.spikeRing(e.position(), 10, 1.9, 0, e.dmg(0.8f), 1.1f, 0);
                a.ink(e.position().add(0, 0.6, 0), 26, 1.3);
                FpeUtil.sound(e, SoundEvents.TRIDENT_RIPTIDE_1, 1f, 0.7f);
            }
        }));

        // 13. Frenzy (enraged): dash t8, slashes t12/16/20/24, limb + both claws hammer t30
        out.add(Ability.of("frenzy", 46, 120).range(0, 5).weight(4).when(FpeEntity::isEnraged).faceUntil(28).tick((e, t, k) -> {
            MutantAbbie a = (MutantAbbie) e;
            if (k == 2) FpeUtil.sound(e, SoundEvents.FOX_SCREECH, 1f, 0.6f);
            if (k == 8) e.dashToward(t.position(), Mth.clamp(e.distanceTo(t) * 0.2, 0.3, 0.9), 0.1);
            if (k == 12 || k == 16 || k == 20 || k == 24) {
                t.invulnerableTime = 0;
                FpeUtil.hitCone(e, 2.8, 70, e.dmg(0.6f), 0.1, 0.05);
                boolean right = k == 12 || k == 20;
                a.arc(2.0f, 100, right ? -20 : 20, 1.1, INK_ARC);
                a.slashSound(right ? 1.4f : 1.2f);
                if (k < 24) e.dashForward(0.15, 0);
            }
            if (k == 30) {
                t.invulnerableTime = 0;
                FpeUtil.hitRadius(e, FpeUtil.ahead(e, 1.2, 0), 2.2, e.dmg(1.5f), 1.0, 0.5);
                FpeUtil.fx(e, FpeFx.Kind.RING_SHOCK, FpeUtil.ahead(e, 1.2, 0), 0, 10, 3.0f, 0).color(INK_ARC);
                a.ink(FpeUtil.ahead(e, 1.2, 0.2), 20, 0.8);
                FpeUtil.sound(e, SoundEvents.GENERIC_EXPLODE, 0.5f, 1.3f);
            }
        }));

        // 14. Bramble bloom (enraged): the sprout swells huge, thorn ring erupts t18 (inner) and t26 (outer), she drinks it in (heal)
        out.add(Ability.of("bramble_bloom", 44, 160).range(0, 7).weight(3).when(FpeEntity::isEnraged).tick((e, t, k) -> {
            MutantAbbie a = (MutantAbbie) e;
            if (k < 16 && k % 3 == 0) FpeUtil.particles(e, LEAF, e.position().add(0, 2.4, 0), 4, 0.3, 0.2, 0.3, 0.02);
            if (k == 4) FpeUtil.sound(e, SoundEvents.WARDEN_HEARTBEAT, 1.2f, 1.3f);
            if (k == 18) {
                FpeUtil.hitRadius(e, e.position(), 2.6, e.dmg(1.2f), 1.1, 0.5);
                a.spikeRing(e.position(), 8, 1.8, 0, e.dmg(0.8f), 1.2f, 0);
                a.ink(e.position().add(0, 0.8, 0), 24, 1.4);
                FpeUtil.sound(e, SoundEvents.ROOTED_DIRT_BREAK, 1.4f, 0.5f);
            }
            if (k == 26) {
                a.spikeRing(e.position(), 12, 4.0, 0, e.dmg(1.0f), 1.5f, Math.PI / 12);
                FpeUtil.fx(e, FpeFx.Kind.RING_SHOCK, e.position(), 0, 12, 5.0f, 0).color(INK_ARC);
                e.heal(6f);
                FpeUtil.particles(e, LEAF, e.position().add(0, 1.2, 0), 20, 1.5, 0.5, 1.5, 0.05);
                FpeUtil.sound(e, SoundEvents.AZALEA_LEAVES_BREAK, 1.4f, 0.6f);
            }
        }));
    }
}
