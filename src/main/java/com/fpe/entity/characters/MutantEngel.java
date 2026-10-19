package com.fpe.entity.characters;

import java.util.List;

import com.fpe.entity.Ability;
import com.fpe.entity.FpeEntity;
import com.fpe.entity.FpeFx;
import com.fpe.entity.FpeProjectile;
import com.fpe.entity.FpeUtil;

import net.minecraft.core.BlockPos;
import net.minecraft.core.particles.DustParticleOptions;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.util.Mth;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.Vec3;
import org.joml.Vector3f;

/**
 * Mutant Engel (FPE Green, mutant 002): tall spiky-haired boy with a cracked ear-to-ear grin and one huge ink-black clawed (left) arm.
 * Claw rakes / combos / grab-and-slam / lunge / ground rake / guard + counter / spin kick / ink quake / ink tendrils, ranged feather darts;
 * enraged = mad cackle (homing ink orbs) + claw frenzy. Every tick index matches the key poses in tools/bbgen/chars/mutant_engel.py.
 */
public class MutantEngel extends FpeEntity {
    private static final DustParticleOptions INK = new DustParticleOptions(new Vector3f(0.06f, 0.06f, 0.08f), 1.6f);
    private static final int BLACK_ARC = 0xE0101014, WHITE_ARC = 0xD0F2F2F4;
    private boolean grabbed;
    private Vec3 trapAt = Vec3.ZERO;

    public MutantEngel(EntityType<? extends FpeEntity> type, Level level) { super(type, level); }

    @Override public Faction faction() { return Faction.MUTANT; }

    public static AttributeSupplier.Builder attributes() { return baseAttributes(110, 8, 0.31, 4, 0.45); }

    @Override public double preferredDistance() { return 2.0; }
    @Override protected int restTicks() { return isEnraged() ? 6 : 14; }

    @Override protected SoundEvent getAmbientSound() { return SoundEvents.WITCH_CELEBRATE; }
    @Override protected SoundEvent getHurtSound(DamageSource s) { return SoundEvents.PLAYER_HURT; }
    @Override protected SoundEvent getDeathSound() { return SoundEvents.WITCH_DEATH; }
    @Override public float getVoicePitch() { return 0.65f; }

    // ------------------------------------------------------------------ helpers
    private void arc(float radius, float sweep, float tilt, double y, int color) {
        FpeFx f = FpeUtil.fx(this, FpeFx.Kind.ARC, position().add(0, y, 0), 0, 7, radius, 0).param(sweep).color(color);
        f.setYRot(getYRot());
        f.setXRot(tilt);
    }

    private void rake(float mult, double reach, double halfAngle, double knock, float tilt) {
        FpeUtil.hitCone(this, reach, halfAngle, dmg(mult), knock, 0.2);
        arc((float) reach - 0.4f, (float) halfAngle * 2, tilt, 1.2, BLACK_ARC);
        FpeUtil.particles(this, INK, FpeUtil.ahead(this, 1.6, 1.2), 12, 0.6, 0.3, 0.6, 0.05);
        FpeUtil.sound(this, SoundEvents.PLAYER_ATTACK_SWEEP, 1.1f, 0.6f);
    }

    private double groundY(double x, double z, double refY) {
        BlockPos.MutableBlockPos p = new BlockPos.MutableBlockPos(x, refY + 3, z);
        for (int i = 0; i < 10; i++, p.move(0, -1, 0)) {
            BlockPos b = p.below();
            if (level().getBlockState(p).getCollisionShape(level(), p).isEmpty() && !level().getBlockState(b).getCollisionShape(level(), b).isEmpty()) return p.getY();
        }
        return refY;
    }

    private Vec3 ground(Vec3 p) { return new Vec3(p.x, groundY(p.x, p.z, getY()), p.z); }

    private void fan(FpeProjectile.Kind kind, Vec3 from, LivingEntity t, int n, double spreadDeg, double speed, float dmg) {
        Vec3 dir = FpeUtil.aim(from, t, speed, 0.4);
        for (int i = 0; i < n; i++) {
            double a = Math.toRadians((i - (n - 1) / 2.0) * spreadDeg);
            double c = Math.cos(a), s = Math.sin(a);
            FpeUtil.projectile(this, kind, from, new Vec3(dir.x * c - dir.z * s, dir.y, dir.x * s + dir.z * c), dmg);
        }
    }

    private static boolean inFront(FpeEntity e, LivingEntity t, double reach, double halfAngle) {
        Vec3 to = t.position().subtract(e.position());
        double ang = Math.toDegrees(Math.acos(Mth.clamp(new Vec3(to.x, 0, to.z).normalize().dot(FpeUtil.forward(e)), -1, 1)));
        return e.distanceTo(t) < reach && ang < halfAngle && FpeUtil.canHurt(e, t);
    }

    // ------------------------------------------------------------------ abilities
    @Override
    protected void registerAbilities(List<Ability> out) {
        // 1. Claw swipe: claw cocked wide (0-9), horizontal rake t12
        out.add(Ability.of("claw_swipe", 26, 30).range(0, 3.8).weight(5).faceUntil(10).tick((e, t, k) -> {
            MutantEngel c = (MutantEngel) e;
            if (k == 10) e.dashForward(0.3, 0);
            if (k == 12) c.rake(1.3f, 3.8, 70, 0.8f, 10);
        }));

        // 2. Claw combo: backhand t9, forehand t17, overhead slam t27
        out.add(Ability.of("claw_combo", 36, 50).range(0, 3.6).weight(4).tick((e, t, k) -> {
            MutantEngel c = (MutantEngel) e;
            if (k == 7 || k == 15 || k == 25) e.dashForward(0.22, 0);
            if (k == 9 || k == 17) { t.invulnerableTime = 0; c.rake(0.75f, 3.4, 65, 0.4, k == 9 ? -15 : 15); }
            if (k == 27) {
                t.invulnerableTime = 0;
                FpeUtil.hitCone(e, 3.4, 35, e.dmg(1.3f), 0.3, 0.6);
                c.arc(3.0f, 90, 85, 1.2, BLACK_ARC);
                FpeUtil.fx(e, FpeFx.Kind.RING_SHOCK, c.ground(FpeUtil.ahead(e, 2.0, 0)).add(0, 0.05, 0), 0, 10, 2.4f, 0);
                FpeUtil.particles(e, INK, FpeUtil.ahead(e, 2.0, 0.2), 20, 0.6, 0.1, 0.6, 0.05);
                FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_STRONG, 1.2f, 0.6f);
            }
        }));

        // 3. Grab & slam (signature): reaching grab t12, hoists overhead, SLAMS into the floor t36
        out.add(Ability.of("grab_slam", 56, 120).range(0, 3.6).weight(3).faceUntil(11)
                .start((e, t, k) -> ((MutantEngel) e).grabbed = false).tick((e, t, k) -> {
            MutantEngel c = (MutantEngel) e;
            if (k == 10) e.dashForward(0.55, 0);
            if (k == 12) {
                c.grabbed = inFront(e, t, 3.8, 60);
                FpeUtil.sound(e, c.grabbed ? SoundEvents.SLIME_ATTACK : SoundEvents.PLAYER_ATTACK_NODAMAGE, 1.2f, 0.5f);
                if (c.grabbed) FpeUtil.hit(c, t, e.dmg(0.4f), 0, 0);
            }
            if (c.grabbed && k > 12 && k < 36) {
                double lift = Math.min(2.6, (k - 12) * 0.14);
                Vec3 hold = FpeUtil.ahead(e, k < 28 ? 1.4 : 0.6, 0.6 + lift).add(FpeUtil.right(e).scale(-0.5));
                t.setDeltaMovement(hold.subtract(t.position()).scale(0.5));
                t.hurtMarked = true;
                t.fallDistance = 0;
                if (k % 4 == 0) FpeUtil.particles(e, INK, t.position().add(0, 1, 0), 4, 0.3, 0.3, 0.3, 0.02);
            }
            if (k == 36) {
                Vec3 at = c.ground(FpeUtil.ahead(e, 1.8, 0));
                if (c.grabbed) {
                    t.teleportTo(at.x, at.y + 0.1, at.z);
                    t.invulnerableTime = 0;
                    FpeUtil.hit(c, t, e.dmg(2.0f), 0.3, 0.5);
                    t.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 50, 3));
                }
                FpeUtil.hitRadius(e, at, 2.4, e.dmg(0.6f), 0.8, 0.4);
                FpeUtil.fx(e, FpeFx.Kind.RING_SHOCK, at.add(0, 0.05, 0), 0, 12, 3.6f, 0);
                FpeUtil.particles(e, INK, at.add(0, 0.2, 0), 30, 1.0, 0.1, 1.0, 0.08);
                FpeUtil.sound(e, SoundEvents.GENERIC_EXPLODE, 0.8f, 0.8f);
                FpeUtil.sound(e, SoundEvents.ANVIL_LAND, 0.7f, 0.5f);
            }
        }));

        // 4. Feather darts: plucks feathers from his hair, flicks a fan t13 and a wider fan t21
        out.add(Ability.of("feather_darts", 30, 50).range(4, 16).weight(3).tick((e, t, k) -> {
            MutantEngel c = (MutantEngel) e;
            if (k == 6) FpeUtil.sound(e, SoundEvents.CHICKEN_EGG, 1.2f, 0.6f);
            if (k == 13 || k == 21) {
                Vec3 from = FpeUtil.ahead(e, 0.5, 2.3).add(FpeUtil.right(e).scale(0.4));
                c.fan(FpeProjectile.Kind.KNIFE, from, t, k == 13 ? 3 : (e.isEnraged() ? 7 : 5), 10, 1.3, e.dmg(0.5f));
                FpeUtil.particles(e, ParticleTypes.WHITE_ASH, from, 14, 0.4, 0.3, 0.4, 0.05);
                FpeUtil.sound(e, SoundEvents.ARROW_SHOOT, 1.1f, 1.4f);
                FpeUtil.sound(e, SoundEvents.PARROT_FLY, 1f, 0.8f);
            }
        }));

        // 5. Ink lunge: drops low (0-8), explodes forward t9, claw spear-thrust t13 along the path
        out.add(Ability.of("ink_lunge", 30, 60).range(3, 9).weight(3).faceUntil(9).tick((e, t, k) -> {
            if (k == 4) FpeUtil.sound(e, SoundEvents.PHANTOM_FLAP, 1f, 0.6f);
            if (k == 9) {
                e.dashToward(t.position(), Mth.clamp(e.distanceTo(t) * 0.16, 0.7, 1.5), 0.08);
                FpeUtil.particles(e, INK, e.position(), 16, 0.4, 0.1, 0.4, 0.05);
            }
            if (k >= 10 && k <= 13) {
                Vec3 a = e.position().add(0, 1.2, 0), b = FpeUtil.ahead(e, 3.4, 1.2);
                if (k == 13) FpeUtil.hitLine((FpeEntity) e, a, b, 0.9, e.dmg(1.4f), 1.0, 0.25);
                FpeUtil.particles(e, INK, e.position().add(0, 1, 0), 6, 0.3, 0.3, 0.3, 0.02);
            }
            if (k == 13) {
                ((MutantEngel) e).arc(3.2f, 30, 0, 1.2, BLACK_ARC);
                FpeUtil.sound(e, SoundEvents.TRIDENT_HIT, 1.2f, 0.6f);
            }
        }));

        // 6. Ground rake: drives the claw into the floor t14 and rakes a line of ink spikes toward the target (t14-28)
        out.add(Ability.of("ground_rake", 40, 80).range(2.5, 12).weight(3).faceUntil(12).tick((e, t, k) -> {
            MutantEngel c = (MutantEngel) e;
            if (k == 14) {
                FpeUtil.hitRadius(e, FpeUtil.ahead(e, 1.4, 0), 1.6, e.dmg(0.8f), 0.4, 0.4);
                FpeUtil.particles(e, INK, FpeUtil.ahead(e, 1.4, 0.2), 24, 0.6, 0.1, 0.6, 0.05);
                FpeUtil.sound(e, SoundEvents.GRAVEL_BREAK, 1.4f, 0.5f);
            }
            if (k >= 14 && k <= 28 && (k - 14) % 2 == 0) {
                int i = (k - 14) / 2;
                double side = (i % 2 == 0 ? 0.5 : -0.5);
                Vec3 p = FpeUtil.ahead(e, 1.8 + i * 1.3, 0).add(FpeUtil.right(e).scale(side));
                FpeUtil.fx(e, FpeFx.Kind.SPIKE, c.ground(p), 3, 14, 1.0f, e.dmg(0.8f)).param(0.8f + i * 0.1f);
                if (i % 2 == 0) FpeUtil.sound(e, SoundEvents.EVOKER_FANGS_ATTACK, 0.8f, 0.7f);
            }
        }));

        // 7. Guard & counter: claw raised as a shield (t4-24, heavily resisted), then a punishing counter rake t28
        out.add(Ability.of("guard_counter", 40, 140).range(0, 4).weight(2).tick((e, t, k) -> {
            MutantEngel c = (MutantEngel) e;
            if (k == 4) {
                e.addEffect(new MobEffectInstance(MobEffects.DAMAGE_RESISTANCE, 22, 3, false, false));
                FpeUtil.sound(e, SoundEvents.SHIELD_BLOCK, 1f, 0.6f);
            }
            if (k > 4 && k < 24 && k % 6 == 0) FpeUtil.particles(e, INK, FpeUtil.ahead(e, 0.8, 1.8), 6, 0.4, 0.4, 0.4, 0.01);
            if (k == 26) e.dashForward(0.4, 0);
            if (k == 28) {
                boolean hurtRecently = e.getLastHurtByMob() != null && e.tickCount - e.getLastHurtByMobTimestamp() < 30;
                c.rake(hurtRecently ? 1.8f : 1.2f, 4.0, 85, 1.4, 0);
                if (hurtRecently) FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_CRIT, 1.2f, 0.6f);
            }
        }));

        // 8. Spin kick: full turn on one leg, the long black leg sweeps everything around t12
        out.add(Ability.of("spin_kick", 28, 45).range(0, 3.2).weight(3).faceUntil(6).tick((e, t, k) -> {
            MutantEngel c = (MutantEngel) e;
            if (k == 12) {
                FpeUtil.hitRadius(e, e.position().add(0, 0.6, 0), 3.0, e.dmg(1.0f), 1.3, 0.4);
                c.arc(2.8f, 360, 0, 0.6, WHITE_ARC);
                FpeUtil.particles(e, ParticleTypes.SWEEP_ATTACK, e.position().add(0, 0.6, 0), 4, 1.2, 0.1, 1.2, 0);
                FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_KNOCKBACK, 1.2f, 0.8f);
            }
        }));

        // 9. Ink quake: hoists the claw (fist) high, hammers the floor t17, ring of ink spikes erupts t20
        out.add(Ability.of("ink_quake", 40, 100).range(0, 6).weight(2).tick((e, t, k) -> {
            MutantEngel c = (MutantEngel) e;
            if (k == 17) {
                Vec3 at = c.ground(FpeUtil.ahead(e, 1.6, 0));
                FpeUtil.hitRadius(e, at, 2.6, e.dmg(1.3f), 1.0, 0.6);
                FpeUtil.fx(e, FpeFx.Kind.RING_SHOCK, at.add(0, 0.05, 0), 0, 14, 5.0f, e.dmg(0.4f));
                FpeUtil.particles(e, INK, at.add(0, 0.2, 0), 30, 1.2, 0.1, 1.2, 0.08);
                FpeUtil.sound(e, SoundEvents.GENERIC_EXPLODE, 0.9f, 0.7f);
            }
            if (k == 20) {
                Vec3 at = FpeUtil.ahead(e, 1.6, 0);
                int n = e.isEnraged() ? 10 : 7;
                for (int i = 0; i < n; i++) {
                    double a = i * Math.PI * 2 / n;
                    Vec3 p = at.add(Math.cos(a) * 3.2, 0, Math.sin(a) * 3.2);
                    FpeUtil.fx(e, FpeFx.Kind.SPIKE, c.ground(p), 4, 14, 1.0f, e.dmg(0.8f)).param(1.1f);
                }
                FpeUtil.sound(e, SoundEvents.EVOKER_FANGS_ATTACK, 1.3f, 0.5f);
            }
        }));

        // 10. Ink tendrils: claw stabbed into the floor t14 -> ink tendrils grab under the target, wrenched up t24 -> spikes burst
        out.add(Ability.of("ink_tendrils", 40, 100).range(3, 14).weight(2).faceUntil(13).tick((e, t, k) -> {
            MutantEngel c = (MutantEngel) e;
            if (k == 14) {
                c.trapAt = c.ground(t.position());
                FpeUtil.fx(e, FpeFx.Kind.TENTACLE, c.trapAt, 4, 26, 1.6f, e.dmg(0.4f)).param(1.0f);
                FpeUtil.particles(e, INK, FpeUtil.ahead(e, 1.4, 0.2), 16, 0.4, 0.1, 0.4, 0.05);
                FpeUtil.sound(e, SoundEvents.SCULK_BLOCK_SPREAD, 1.4f, 0.6f);
            }
            if (k == 24) {
                FpeUtil.fx(e, FpeFx.Kind.SPIKE, c.trapAt, 2, 14, 1.3f, e.dmg(1.2f)).param(1.6f);
                for (int i = 0; i < 4; i++) {
                    double a = i * Math.PI / 2 + Math.PI / 4;
                    double x = c.trapAt.x + Math.cos(a) * 1.4, z = c.trapAt.z + Math.sin(a) * 1.4;
                    FpeUtil.fx(e, FpeFx.Kind.SPIKE, new Vec3(x, c.groundY(x, z, c.trapAt.y), z), 4, 12, 0.9f, e.dmg(0.7f)).param(1.0f);
                }
                FpeUtil.sound(e, SoundEvents.EVOKER_FANGS_ATTACK, 1.4f, 0.6f);
            }
        }));

        // 11. Mad cackle (enraged): head thrown back laughing - homing ink orbs t18 / 26 / 34, laughter weakens nearby foes
        out.add(Ability.of("mad_cackle", 44, 140).range(3, 18).weight(3).when(FpeEntity::isEnraged).blind().tick((e, t, k) -> {
            MutantEngel c = (MutantEngel) e;
            if (k == 10) FpeUtil.sound(e, SoundEvents.WITCH_CELEBRATE, 2.0f, 0.5f);
            if (k == 18 || k == 26 || k == 34) {
                Vec3 from = FpeUtil.ahead(e, 0.6, 2.5).add(FpeUtil.right(e).scale(-0.8));
                FpeUtil.projectile(c, FpeProjectile.Kind.SHADOW_ORB, from, FpeUtil.aim(from, t, 0.5, 0.2).add(0, 0.15, 0), e.dmg(0.8f));
                FpeUtil.particles(e, INK, from, 10, 0.3, 0.3, 0.3, 0.05);
                FpeUtil.sound(e, SoundEvents.WITCH_AMBIENT, 1.4f, 0.5f + k * 0.01f);
                for (LivingEntity v : FpeUtil.enemiesInRadius(e, e.position(), 5, 3, 1)) {
                    v.addEffect(new MobEffectInstance(MobEffects.WEAKNESS, 60, 0));
                    v.addEffect(new MobEffectInstance(MobEffects.CONFUSION, 80, 0));
                }
            }
        }));

        // 12. Claw frenzy (enraged): four alternating rakes t10/16/22/28, rising double-claw uppercut t36
        out.add(Ability.of("claw_frenzy", 48, 90).range(0, 4.5).weight(4).when(FpeEntity::isEnraged).tick((e, t, k) -> {
            MutantEngel c = (MutantEngel) e;
            if (k == 8 || k == 14 || k == 20 || k == 26 || k == 33) { e.snapFace(t); e.dashForward(0.35, 0); }
            if (k == 10 || k == 16 || k == 22 || k == 28) {
                t.invulnerableTime = 0;
                c.rake(0.7f, 3.4, 70, 0.3, (k / 6) % 2 == 0 ? 20 : -20);
            }
            if (k == 36) {
                t.invulnerableTime = 0;
                FpeUtil.hitCone(e, 3.4, 60, e.dmg(1.5f), 0.4, 1.1);
                c.arc(3.0f, 120, -80, 0.8, BLACK_ARC);
                FpeUtil.particles(e, INK, FpeUtil.ahead(e, 1.4, 1.0), 24, 0.5, 0.8, 0.5, 0.08);
                FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_CRIT, 1.3f, 0.5f);
            }
        }));
    }
}
