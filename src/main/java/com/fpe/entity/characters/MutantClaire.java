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
 * Mutant Claire (FPE Green, mutant 001): hunched white-hooded wolf-thing whose whole face is a jagged maw.
 * Bites, sleeve flails, satchel swings, pounces, a howl, ranged spat fangs / failed tests, ground jaws; enraged = devour + frenzy.
 * Every tick index below matches the key poses in tools/bbgen/chars/mutant_claire.py.
 */
public class MutantClaire extends FpeEntity {
    private static final DustParticleOptions INK = new DustParticleOptions(new Vector3f(0.08f, 0.08f, 0.1f), 1.4f);
    private static final int WHITE_ARC = 0xD0F2F2F4, BLACK_ARC = 0xD0141418;
    private boolean grabbed;
    private Vec3 trapAt = Vec3.ZERO;

    public MutantClaire(EntityType<? extends FpeEntity> type, Level level) { super(type, level); }

    @Override public Faction faction() { return Faction.MUTANT; }

    @Override public boolean meleeFocus() { return true; }

    public static AttributeSupplier.Builder attributes() { return baseAttributes(100, 7, 0.32, 3, 0.35); }

    @Override public double preferredDistance() { return 1.4; }
    @Override protected int restTicks() { return isEnraged() ? 6 : 14; }

    @Override protected SoundEvent getAmbientSound() { return SoundEvents.WOLF_GROWL; }
    @Override protected SoundEvent getHurtSound(DamageSource s) { return SoundEvents.WOLF_HURT; }
    @Override protected SoundEvent getDeathSound() { return SoundEvents.WOLF_DEATH; }
    @Override public float getVoicePitch() { return 0.7f; }

    // ------------------------------------------------------------------ helpers
    private void arc(float radius, float sweep, float tilt, double y, int color) {
        FpeFx f = FpeUtil.fx(this, FpeFx.Kind.ARC, position().add(0, y, 0), 0, 7, radius, 0).param(sweep).color(color);
        f.setYRot(getYRot());
        f.setXRot(tilt);
    }

    private void bite(float mult, double reach, double halfAngle) {
        FpeUtil.hitCone(this, reach, halfAngle, dmg(mult), 0.4, 0.15);
        FpeUtil.particles(this, ParticleTypes.CRIT, FpeUtil.ahead(this, 1.4, 1.3), 10, 0.3, 0.3, 0.3, 0.2);
        FpeUtil.sound(this, SoundEvents.EVOKER_FANGS_ATTACK, 1.1f, 1.3f);
        FpeUtil.sound(this, SoundEvents.WOLF_GROWL, 0.8f, 0.6f);
    }

    private void bleed(LivingEntity v, int ticks) {
        v.addEffect(new MobEffectInstance(MobEffects.WITHER, ticks, 0));
    }

    private double groundY(double x, double z, double refY) {
        BlockPos.MutableBlockPos p = new BlockPos.MutableBlockPos(x, refY + 3, z);
        for (int i = 0; i < 10; i++, p.move(0, -1, 0)) {
            BlockPos b = p.below();
            if (level().getBlockState(p).getCollisionShape(level(), p).isEmpty() && !level().getBlockState(b).getCollisionShape(level(), b).isEmpty()) return p.getY();
        }
        return refY;
    }

    private Vec3 mouth() { return FpeUtil.ahead(this, 0.7, 1.35); }

    private Vec3 hand(boolean right) { return FpeUtil.ahead(this, 0.5, 1.4).add(FpeUtil.right(this).scale(right ? 0.45 : -0.45)); }

    private void fan(FpeProjectile.Kind kind, Vec3 from, LivingEntity t, int n, double spreadDeg, double speed, float dmg) {
        Vec3 dir = FpeUtil.aim(from, t, speed, 0.4);
        for (int i = 0; i < n; i++) {
            double a = Math.toRadians((i - (n - 1) / 2.0) * spreadDeg);
            double c = Math.cos(a), s = Math.sin(a);
            FpeUtil.projectile(this, kind, from, new Vec3(dir.x * c - dir.z * s, dir.y, dir.x * s + dir.z * c), dmg);
        }
    }

    // ------------------------------------------------------------------ abilities
    @Override
    protected void registerAbilities(List<Ability> out) {
        // 1. Maw chomp: rears + gapes (0-9), lunging snap t11, shakes the prey
        out.add(Ability.of("maw_chomp", 24, 30).range(0, 3.2).weight(5).faceUntil(9).tick((e, t, k) -> {
            MutantClaire c = (MutantClaire) e;
            if (k == 3) FpeUtil.sound(e, SoundEvents.WOLF_GROWL, 1f, 0.5f);
            if (k == 9) e.dashForward(0.55, 0.05);
            if (k == 11) {
                c.bite(1.3f, 2.8, 50);
                for (LivingEntity v : FpeUtil.enemiesInRadius(e, FpeUtil.ahead(e, 1.4, 0), 1.4, 2.5, 1)) c.bleed(v, 40);
            }
        }));

        // 2. Sleeve flail: right sleeve whips across t8, left t15, both slammed overhead t23
        out.add(Ability.of("sleeve_flail", 32, 45).range(0, 3.4).weight(4).tick((e, t, k) -> {
            MutantClaire c = (MutantClaire) e;
            if (k == 6 || k == 13 || k == 21) e.dashForward(0.22, 0);
            if (k == 8 || k == 15) {
                t.invulnerableTime = 0;
                FpeUtil.hitCone(e, 3.0, 80, e.dmg(0.75f), 0.6, 0.15);
                c.arc(2.4f, 150, k == 8 ? 12 : -12, 1.1, WHITE_ARC);
                FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_SWEEP, 1f, 0.8f);
                FpeUtil.sound(e, SoundEvents.WOOL_BREAK, 1f, 0.6f);
            }
            if (k == 23) {
                t.invulnerableTime = 0;
                FpeUtil.hitCone(e, 3.0, 45, e.dmg(1.2f), 0.3, 0.0);
                c.arc(2.2f, 100, 80, 1.0, WHITE_ARC);
                for (LivingEntity v : FpeUtil.enemiesInRadius(e, FpeUtil.ahead(e, 1.6, 0), 1.6, 2.5, 1))
                    v.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 30, 2));
                FpeUtil.particles(e, ParticleTypes.POOF, FpeUtil.ahead(e, 1.6, 0.2), 8, 0.4, 0.1, 0.4, 0.04);
                FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_STRONG, 1.1f, 0.7f);
            }
        }));

        // 3. Bag swing: hauls the satchel back (0-14), whirls it round t17 - huge knockback
        out.add(Ability.of("bag_swing", 34, 70).range(0, 3.8).weight(3).faceUntil(15).tick((e, t, k) -> {
            MutantClaire c = (MutantClaire) e;
            if (k == 8) FpeUtil.sound(e, SoundEvents.ARMOR_EQUIP_LEATHER, 1f, 0.6f);
            if (k == 16) e.dashForward(0.25, 0);
            if (k == 17) {
                FpeUtil.hitCone(e, 3.6, 100, e.dmg(1.5f), 1.8, 0.5);
                c.arc(3.0f, 200, 0, 1.0, WHITE_ARC);
                FpeUtil.particles(e, ParticleTypes.SWEEP_ATTACK, FpeUtil.ahead(e, 1.8, 1.0), 3, 0.6, 0.2, 0.6, 0);
                FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_KNOCKBACK, 1.3f, 0.6f);
                FpeUtil.sound(e, SoundEvents.BOOK_PUT, 1.2f, 0.5f);
            }
        }));

        // 4. Pounce: crouch (0-9), launches t10 at the target, crash-bite landing t20
        out.add(Ability.of("pounce", 36, 80).range(3.5, 11).weight(3).faceUntil(10).tick((e, t, k) -> {
            MutantClaire c = (MutantClaire) e;
            if (k == 4) FpeUtil.sound(e, SoundEvents.WOLF_GROWL, 1.2f, 0.7f);
            if (k == 10) {
                double d = e.distanceTo(t);
                e.dashToward(t.position(), Mth.clamp(d * 0.11, 0.5, 1.25), 0.55);
                FpeUtil.particles(e, ParticleTypes.CLOUD, e.position(), 10, 0.4, 0.05, 0.4, 0.05);
                FpeUtil.sound(e, SoundEvents.RAVAGER_STEP, 1f, 1.4f);
            }
            if (k > 10 && k < 20) e.fallDistance = 0;
            if (k == 20) {
                FpeUtil.hitRadius(e, FpeUtil.ahead(e, 0.8, 0), 2.2, e.dmg(1.5f), 0.7, 0.3);
                c.bite(0.6f, 2.4, 60);
                FpeUtil.fx(e, FpeFx.Kind.RING_SHOCK, e.position().add(0, 0.05, 0), 0, 10, 3.0f, 0);
                FpeUtil.particles(e, ParticleTypes.POOF, e.position(), 14, 0.8, 0.1, 0.8, 0.05);
                FpeUtil.sound(e, SoundEvents.GENERIC_SMALL_FALL, 1.3f, 0.6f);
            }
        }));

        // 5. Talon stomp: right clawed foot raised (0-12), STOMP t14 - shockwave ring
        out.add(Ability.of("talon_stomp", 30, 60).range(0, 3.5).weight(3).tick((e, t, k) -> {
            if (k == 14) {
                Vec3 at = FpeUtil.ahead(e, 0.6, 0);
                FpeUtil.hitRadius(e, at, 2.6, e.dmg(1.1f), 0.8, 0.5);
                FpeUtil.fx(e, FpeFx.Kind.RING_SHOCK, new Vec3(at.x, e.getY() + 0.05, at.z), 0, 12, 4.0f, e.dmg(0.4f));
                FpeUtil.particles(e, INK, at.add(0, 0.2, 0), 20, 0.9, 0.1, 0.9, 0.05);
                FpeUtil.sound(e, SoundEvents.GENERIC_EXPLODE, 0.6f, 1.4f);
                FpeUtil.sound(e, SoundEvents.RAVAGER_STEP, 1.2f, 0.6f);
            }
        }));

        // 6. Howl: coils (0-11), rears up and howls 14-34 - shockwaves t14/22/30 push back, slow + weaken
        out.add(Ability.of("howl", 44, 160).range(0, 8).weight(2).blind().tick((e, t, k) -> {
            if (k == 12) FpeUtil.sound(e, SoundEvents.WOLF_HOWL, 2.0f, 0.55f);
            if (k == 14 || k == 22 || k == 30) {
                float r = 3.5f + (k - 14) * 0.15f;
                FpeUtil.fx(e, FpeFx.Kind.RING_SHOCK, e.position().add(0, 0.1, 0), 0, 12, r + 2, 0);
                for (LivingEntity v : FpeUtil.enemiesInRadius(e, e.position(), r, 3, 1)) {
                    v.invulnerableTime = 0;
                    FpeUtil.hit((FpeEntity) e, v, e.dmg(0.45f), 1.0, 0.25);
                    v.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 60, 1));
                    v.addEffect(new MobEffectInstance(MobEffects.WEAKNESS, 80, 0));
                    if (e.isEnraged()) v.addEffect(new MobEffectInstance(MobEffects.DARKNESS, 60, 0));
                }
                FpeUtil.particles(e, ParticleTypes.SONIC_BOOM, e.position().add(0, 2.2, 0), 1, 0, 0, 0, 0);
                FpeUtil.sound(e, SoundEvents.WOLF_HOWL, 1.4f, 0.4f + k * 0.01f);
            }
        }));

        // 7. Paper storm: digs failed tests + pencils out of the satchel, hurls them t12 (r), t20 (l), t27 (both)
        out.add(Ability.of("paper_storm", 34, 70).range(4, 16).weight(3).tick((e, t, k) -> {
            MutantClaire c = (MutantClaire) e;
            if (k == 5) FpeUtil.sound(e, SoundEvents.BOOK_PAGE_TURN, 1.2f, 0.7f);
            if (k == 12) c.fan(FpeProjectile.Kind.PENCIL, c.hand(true), t, 3, 9, 1.1, e.dmg(0.5f));
            if (k == 20) c.fan(FpeProjectile.Kind.PENCIL, c.hand(false), t, 3, 9, 1.1, e.dmg(0.5f));
            if (k == 27) c.fan(FpeProjectile.Kind.PENCIL, FpeUtil.ahead(e, 0.6, 1.8), t, e.isEnraged() ? 7 : 5, 8, 1.2, e.dmg(0.5f));
            if (k == 12 || k == 20 || k == 27) {
                FpeUtil.particles(e, ParticleTypes.WHITE_ASH, FpeUtil.ahead(e, 1.0, 1.6), 20, 0.6, 0.4, 0.6, 0.05);
                FpeUtil.sound(e, SoundEvents.BOOK_PAGE_TURN, 1.2f, 1.3f);
                FpeUtil.sound(e, SoundEvents.SNOWBALL_THROW, 1f, 0.6f);
            }
        }));

        // 8. Tooth spit: rears back gulping (0-10), spits a fan of fangs t13 and t19
        out.add(Ability.of("tooth_spit", 30, 55).range(3, 14).weight(3).tick((e, t, k) -> {
            MutantClaire c = (MutantClaire) e;
            if (k == 6) FpeUtil.sound(e, SoundEvents.GENERIC_DRINK, 1f, 0.5f);
            if (k == 13 || k == 19) {
                c.fan(FpeProjectile.Kind.DIAMOND, c.mouth(), t, k == 13 ? 3 : 4, 12, 1.2, e.dmg(0.55f));
                FpeUtil.particles(e, INK, c.mouth(), 8, 0.2, 0.2, 0.2, 0.05);
                FpeUtil.sound(e, SoundEvents.LLAMA_SPIT, 1.3f, 0.6f);
            }
        }));

        // 9. Jaw spikes: slams the maw into the floor t14, a line of black fangs erupts toward the target (t14-30)
        out.add(Ability.of("jaw_spikes", 40, 90).range(2.5, 12).weight(3).faceUntil(12).tick((e, t, k) -> {
            MutantClaire c = (MutantClaire) e;
            if (k == 14) {
                FpeUtil.hitRadius(e, FpeUtil.ahead(e, 1.2, 0), 1.6, e.dmg(0.8f), 0.4, 0.4);
                FpeUtil.particles(e, INK, FpeUtil.ahead(e, 1.2, 0.2), 24, 0.6, 0.1, 0.6, 0.05);
                FpeUtil.sound(e, SoundEvents.EVOKER_FANGS_ATTACK, 1.4f, 0.6f);
                FpeUtil.sound(e, SoundEvents.GENERIC_EXPLODE, 0.5f, 1.6f);
            }
            if (k >= 14 && k <= 30 && (k - 14) % 2 == 0) {
                int i = (k - 14) / 2;
                Vec3 f = FpeUtil.forward(e);
                double d = 1.6 + i * 1.3;
                Vec3 p = e.position().add(f.scale(d));
                FpeUtil.fx(e, FpeFx.Kind.SPIKE, new Vec3(p.x, c.groundY(p.x, p.z, e.getY()), p.z), 3, 14, 1.1f, e.dmg(0.8f)).param(0.8f + i * 0.08f);
            }
        }));

        // 10. Maw trap: sleeves raised (0-13), slammed down t16 -> ground jaws open under the target and snap shut t26
        out.add(Ability.of("maw_trap", 36, 100).range(2, 13).weight(2).faceUntil(15).tick((e, t, k) -> {
            MutantClaire c = (MutantClaire) e;
            if (k == 16) {
                c.trapAt = new Vec3(t.getX(), c.groundY(t.getX(), t.getZ(), t.getY()), t.getZ());
                FpeUtil.fx(e, FpeFx.Kind.TENTACLE, c.trapAt, 4, 30, 1.4f, e.dmg(0.4f)).param(0.9f);
                FpeUtil.particles(e, INK, c.trapAt.add(0, 0.1, 0), 20, 0.8, 0.05, 0.8, 0.02);
                FpeUtil.sound(e, SoundEvents.RAVAGER_STEP, 1.2f, 0.5f);
            }
            if (k == 20) {
                for (int i = 0; i < 8; i++) {
                    double a = i * Math.PI / 4;
                    double x = c.trapAt.x + Math.cos(a) * 1.5, z = c.trapAt.z + Math.sin(a) * 1.5;
                    FpeUtil.fx(e, FpeFx.Kind.SPIKE, new Vec3(x, c.groundY(x, z, c.trapAt.y), z), 6, 12, 0.9f, e.dmg(0.9f)).param(1.0f);
                }
            }
            if (k == 26) {
                for (LivingEntity v : FpeUtil.enemiesInRadius(e, c.trapAt, 1.8, 2.5, 1)) {
                    v.invulnerableTime = 0;
                    FpeUtil.hit((FpeEntity) e, v, e.dmg(1.1f), 0, 0.3);
                    c.bleed(v, 60);
                }
                FpeUtil.sound(e, SoundEvents.EVOKER_FANGS_ATTACK, 1.5f, 0.5f);
            }
        }));

        // 11. Devour (enraged signature): sleeve grab t12, hoists prey to the maw, chomps t24/32/40, flings t50
        out.add(Ability.of("devour", 60, 160).range(0, 3.2).weight(4).when(FpeEntity::isEnraged).faceUntil(11)
                .start((e, t, k) -> ((MutantClaire) e).grabbed = false).tick((e, t, k) -> {
            MutantClaire c = (MutantClaire) e;
            if (k == 10) e.dashForward(0.5, 0);
            if (k == 12) {
                Vec3 to = t.position().subtract(e.position());
                double ang = Math.toDegrees(Math.acos(Mth.clamp(new Vec3(to.x, 0, to.z).normalize().dot(FpeUtil.forward(e)), -1, 1)));
                c.grabbed = e.distanceTo(t) < 3.4 && ang < 60 && FpeUtil.canHurt(e, t);
                FpeUtil.sound(e, c.grabbed ? SoundEvents.WOOL_PLACE : SoundEvents.PLAYER_ATTACK_NODAMAGE, 1f, 0.6f);
                if (c.grabbed) FpeUtil.hit(c, t, e.dmg(0.4f), 0, 0);
            }
            if (c.grabbed && k > 12 && k < 50) {
                double lift = Math.min(1.3, (k - 12) * 0.12);
                Vec3 hold = FpeUtil.ahead(e, 1.2, lift);
                t.setDeltaMovement(hold.subtract(t.position()).scale(0.5));
                t.hurtMarked = true;
                t.fallDistance = 0;
                if (k == 24 || k == 32 || k == 40) {
                    t.invulnerableTime = 0;
                    FpeUtil.hit(c, t, e.dmg(0.7f), 0, 0);
                    c.heal(2.0f);
                    c.bleed(t, 40);
                    FpeUtil.particles(e, ParticleTypes.DAMAGE_INDICATOR, t.position().add(0, 1, 0), 5, 0.3, 0.3, 0.3, 0.1);
                    FpeUtil.sound(e, SoundEvents.GENERIC_EAT, 1.3f, 0.6f);
                    FpeUtil.sound(e, SoundEvents.EVOKER_FANGS_ATTACK, 1f, 1.2f);
                }
            }
            if (k == 50 && c.grabbed) {
                t.invulnerableTime = 0;
                FpeUtil.hit(c, t, e.dmg(0.8f), 2.0, 0.6);
                FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_KNOCKBACK, 1.3f, 0.5f);
            }
        }));

        // 12. Frenzy (enraged): four lunging bite + claw rakes t10/18/26/34
        out.add(Ability.of("frenzy", 46, 90).range(0, 4.5).weight(4).when(FpeEntity::isEnraged).tick((e, t, k) -> {
            MutantClaire c = (MutantClaire) e;
            if (k == 8 || k == 16 || k == 24 || k == 32) { e.snapFace(t); e.dashForward(0.45, 0); }
            if (k == 10 || k == 18 || k == 26 || k == 34) {
                t.invulnerableTime = 0;
                c.bite(k == 34 ? 1.1f : 0.7f, 2.8, 70);
                c.arc(2.2f, 120, k == 34 ? 80 : (k % 16 == 10 ? 30 : -30), 1.1, BLACK_ARC);
            }
        }));
    }
}
