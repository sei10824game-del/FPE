package com.fpe.entity.characters;

import java.util.ArrayList;
import java.util.List;

import org.joml.Vector3f;

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
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.Vec3;

/**
 * Danger AU Bloomie – thin, precise, eerie. White claws on the right hand, a huge serrated bandage-wrapped cleaver
 * in the left. Fast cuts that make the victim bleed (wither). Tick indices match client/spec/DangerBloomieSpec.
 */
public class DangerBloomie extends FpeEntity {
    static final DustParticleOptions BLOOD = new DustParticleOptions(new Vector3f(0.55f, 0.02f, 0.06f), 1.2f);
    static final int SLASH = 0xE8E8ECF2, SLASH_RED = 0xE0A01828;

    public DangerBloomie(EntityType<? extends FpeEntity> type, Level level) { super(type, level); }

    public static AttributeSupplier.Builder attributes() { return baseAttributes(115, 8, 0.33, 3, 0.25); }

    @Override public double preferredDistance() { return 1.8; }
    @Override protected int restTicks() { return isEnraged() ? 5 : 12; }

    // ------------------------------------------------------------------ helpers
    /** enemies inside a horizontal cone (same rule as FpeUtil.hitCone) so we can bleed exactly who got cut */
    static List<LivingEntity> cone(FpeEntity e, double range, double halfAngle) {
        Vec3 f = FpeUtil.forward(e);
        List<LivingEntity> out = new ArrayList<>();
        AABB box = e.getBoundingBox().inflate(range, 1.5, range);
        for (LivingEntity v : e.level().getEntitiesOfClass(LivingEntity.class, box, x -> FpeUtil.canHurt(e, x))) {
            Vec3 d = new Vec3(v.getX() - e.getX(), 0, v.getZ() - e.getZ());
            if (d.length() - v.getBbWidth() * 0.5 - e.getBbWidth() * 0.5 > range) continue;
            if (d.lengthSqr() > 0.01 && Math.toDegrees(Math.acos(Mth.clamp(d.normalize().dot(f), -1, 1))) > halfAngle) continue;
            out.add(v);
        }
        return out;
    }

    /** cut everything in the cone; bleedTicks > 0 applies wither (bleeding). resetIframes for fast combos. */
    static int cut(FpeEntity e, double range, double half, float dmg, double knock, double up, int bleedTicks, boolean resetIframes) {
        int n = 0;
        for (LivingEntity v : cone(e, range, half)) {
            if (resetIframes) v.invulnerableTime = 0;
            if (FpeUtil.hit(e, v, dmg, knock, up)) {
                n++;
                if (bleedTicks > 0) bleed(e, v, bleedTicks);
            }
        }
        return n;
    }

    static void bleed(FpeEntity e, LivingEntity v, int ticks) {
        v.addEffect(new MobEffectInstance(MobEffects.WITHER, ticks, e.isEnraged() ? 1 : 0));
        FpeUtil.particles(e, BLOOD, v.position().add(0, v.getBbHeight() * 0.6, 0), 12, 0.25, 0.3, 0.25, 0.05);
    }

    static void slashArc(FpeEntity e, float radius, float sweep, float tilt, float yawOff, double y, int color) {
        FpeFx f = FpeUtil.fx(e, FpeFx.Kind.ARC, e.position().add(0, y, 0), 0, 7, radius, 0).param(sweep).color(color);
        f.setYRot(e.getYRot() + yawOff);
        f.setXRot(tilt);
    }

    static Vec3 rotY(Vec3 v, double deg) {
        double a = Math.toRadians(deg), c = Math.cos(a), s = Math.sin(a);
        return new Vec3(v.x * c - v.z * s, v.y, v.x * s + v.z * c);
    }

    /** sink into shadow and re-emerge behind the target (falls back to its side / front when blocked) */
    static void shadowStep(FpeEntity e, LivingEntity t) {
        FpeUtil.particles(e, ParticleTypes.SQUID_INK, e.position().add(0, 0.8, 0), 30, 0.3, 0.6, 0.3, 0.05);
        FpeUtil.particles(e, ParticleTypes.LARGE_SMOKE, e.position().add(0, 0.5, 0), 12, 0.3, 0.4, 0.3, 0.02);
        Vec3 look = Vec3.directionFromRotation(0, t.getYRot());
        for (double ang : new double[] {180, 130, 230, 90, 270, 0}) {
            Vec3 dest = t.position().add(rotY(look, ang).scale(1.7));
            AABB bb = e.getBoundingBox().move(dest.subtract(e.position()));
            if (e.level().noCollision(e, bb) && !e.level().noCollision(e, bb.move(0, -0.6, 0).deflate(0.05, 0, 0.05).setMaxY(bb.minY))) {
                e.teleportTo(dest.x, dest.y, dest.z);
                break;
            }
        }
        e.setDeltaMovement(Vec3.ZERO);
        e.snapFace(t);
        FpeUtil.particles(e, ParticleTypes.SQUID_INK, e.position().add(0, 0.3, 0), 30, 0.4, 0.2, 0.4, 0.08);
        FpeUtil.particles(e, ParticleTypes.REVERSE_PORTAL, e.position().add(0, 1, 0), 20, 0.3, 0.6, 0.3, 0.05);
        FpeUtil.sound(e, SoundEvents.ENDERMAN_TELEPORT, 0.9f, 0.5f);
    }

    // ------------------------------------------------------------------ abilities
    @Override
    protected void registerAbilities(List<Ability> out) {
        // 1. Overhead chop: blade raised two-handed (0-11), falls at 13 – heavy cut + crack in the floor
        out.add(Ability.of("chop", 30, 50).range(0, 3.8).weight(3).faceUntil(11).tick((e, t, tk) -> {
            if (tk == 9) FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_SWEEP, 0.6f, 0.5f);
            if (tk == 13) {
                cut(e, 3.4, 35, e.dmg(1.7f), 0.4, 0.1, 60, false);
                slashArc(e, 3.0f, 70, 90, 0, 0.2, SLASH);
                Vec3 at = FpeUtil.ahead(e, 2.4, 0.05);
                FpeUtil.particles(e, ParticleTypes.CRIT, at, 18, 0.3, 0.1, 0.3, 0.3);
                FpeUtil.particles(e, ParticleTypes.LARGE_SMOKE, at, 6, 0.3, 0.05, 0.3, 0.02);
                FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_STRONG, 1f, 0.5f);
                FpeUtil.sound(e, SoundEvents.ANVIL_PLACE, 0.5f, 1.6f);
            }
        }));

        // 2. Cleaver sweep: wide horizontal cut left->right at 11
        out.add(Ability.of("sweep", 26, 45).range(0, 4.2).weight(3).faceUntil(9).tick((e, t, tk) -> {
            if (tk == 11) {
                cut(e, 4.0, 95, e.dmg(1.3f), 0.9, 0.2, 40, false);
                slashArc(e, 3.8f, 190, 0, 0, 1.0, SLASH);
                FpeUtil.arc(e, ParticleTypes.SWEEP_ATTACK, e.position().add(0, 1, 0), e.getYRot(), 80, 2.6, 5);
                FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_SWEEP, 1f, 0.75f);
            }
        }));

        // 3. Rising slash: low drag (0-10), up-cut at 12 launching the target, she hops with it
        out.add(Ability.of("rising_slash", 28, 70).range(0, 3.6).weight(2).faceUntil(11).tick((e, t, tk) -> {
            if (tk == 10) e.dashForward(0.45, 0.35);
            if (tk == 12) {
                cut(e, 3.1, 45, e.dmg(1.2f), 0.3, 0.95, 40, false);
                slashArc(e, 2.6f, 120, -80, 0, 0.3, SLASH);
                FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_SWEEP, 1f, 1.1f);
                FpeUtil.particles(e, ParticleTypes.CRIT, FpeUtil.ahead(e, 1.6, 1.0), 10, 0.2, 0.6, 0.2, 0.2);
            }
        }));

        // 4. Blade tornado: spins with the cleaver out (10-44), drifting toward the target, cutting every 4 ticks
        out.add(Ability.of("tornado", 54, 140).range(0, 7).weight(2).moving().tick((e, t, tk) -> {
            if (tk >= 10 && tk <= 44) {
                Vec3 d = t.position().subtract(e.position());
                Vec3 h = new Vec3(d.x, 0, d.z);
                if (h.length() > 1.2) { h = h.normalize().scale(0.22); e.setDeltaMovement(h.x, e.getDeltaMovement().y, h.z); }
                if (tk % 4 == 2) {
                    for (LivingEntity v : FpeUtil.enemiesInRadius(e, e.position(), 2.7, 2.5, 1)) {
                        v.invulnerableTime = 0;
                        if (FpeUtil.hit(e, v, e.dmg(0.5f), 0.35, 0.12) && tk % 12 == 2) bleed(e, v, 30);
                    }
                    FpeUtil.arc(e, ParticleTypes.SWEEP_ATTACK, e.position().add(0, 1.0, 0), tk * 40f, 180, 2.2, 6);
                    FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_SWEEP, 0.7f, 1.2f + (tk % 8) * 0.04f);
                }
                if (tk % 8 == 0) slashArc(e, 2.8f, 300, 0, tk * 47f, 1.0, 0x90E8E8F0);
            }
        }));

        // 5. Blade wave: diagonal slash at 14 throws a crescent, reverse slash at 22 throws another (fans of 3 when enraged)
        out.add(Ability.of("blade_wave", 32, 80).range(4, 18).weight(2).tick((e, t, tk) -> {
            if (tk == 14 || tk == 22) {
                Vec3 from = e.position().add(0, 1.1, 0).add(FpeUtil.forward(e).scale(0.8));
                int n = e.isEnraged() ? 3 : 1;
                for (int i = 0; i < n; i++)
                    FpeUtil.projectile(e, FpeProjectile.Kind.BLADE_WAVE, from, rotY(FpeUtil.aim(from, t, 1.15, 0.3), (i - (n - 1) / 2.0) * 16), e.dmg(1.1f));
                slashArc(e, 2.4f, 150, tk == 14 ? 40 : -40, 0, 1.2, SLASH);
                FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_SWEEP, 1f, tk == 14 ? 0.6f : 0.8f);
            }
        }));

        // 6. Cleaver throw: wound-up overhand throw at 13; the spinning cleaver comes back and she catches it (~46)
        out.add(Ability.of("cleaver_throw", 50, 120).range(5, 16).weight(2).tick((e, t, tk) -> {
            if (tk == 13) {
                Vec3 from = e.position().add(0, 1.7, 0).add(FpeUtil.forward(e).scale(0.6)).add(FpeUtil.right(e).scale(-0.4));
                FpeUtil.projectile(e, FpeProjectile.Kind.AXE, from, FpeUtil.aim(from, t, 1.15, 0.5).add(0, 0.12, 0), e.dmg(1.4f));
                FpeUtil.sound(e, SoundEvents.TRIDENT_THROW, 1f, 0.6f);
            }
            if (tk == 20 || tk == 30) FpeUtil.sound(e, SoundEvents.VEX_AMBIENT, 0.8f, 0.6f);
            if (tk == 46) FpeUtil.sound(e, SoundEvents.ARMOR_EQUIP_IRON, 1f, 0.7f);
        }));

        // 7. Claw flurry: four swipes of the white claws (8 / 13 / 18 / 24) – last one makes them bleed
        out.add(Ability.of("claw_flurry", 32, 60).range(0, 3).weight(3).tick((e, t, tk) -> {
            if (tk == 6 || tk == 16 || tk == 22) e.dashForward(0.22, 0);
            if (tk == 8 || tk == 13 || tk == 18 || tk == 24) {
                boolean last = tk == 24;
                cut(e, last ? 2.9 : 2.6, last ? 35 : 65, e.dmg(last ? 0.8f : 0.5f), last ? 0.7 : 0.15, 0.1, last ? 70 : 0, true);
                slashArc(e, 2.0f, 110, tk == 8 ? 50 : tk == 13 ? -50 : tk == 18 ? 0 : 85, 0, 1.2, SLASH_RED);
                FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_SWEEP, 0.7f, 1.4f + tk * 0.01f);
            }
        }));

        // 8. Shadow step: sinks into her shadow (0-8), rises behind the target (8-14), stab in the back at 18
        out.add(Ability.of("shadow_step", 34, 110).range(3, 16).weight(2).tick((e, t, tk) -> {
            if (tk < 8 && tk % 2 == 0) FpeUtil.particles(e, ParticleTypes.SQUID_INK, e.position().add(0, 0.2, 0), 6, 0.4, 0.1, 0.4, 0.02);
            if (tk == 8) shadowStep(e, t);
            if (tk == 16) FpeUtil.sound(e, SoundEvents.VEX_CHARGE, 1f, 0.7f);
            if (tk == 18) {
                if (cut(e, 2.9, 30, e.dmg(1.5f), 0.6, 0.15, 80, false) > 0) FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_CRIT, 1f, 0.6f);
                FpeUtil.particles(e, ParticleTypes.CRIT, FpeUtil.ahead(e, 1.8, 1.1), 10, 0.1, 0.1, 0.1, 0.3);
            }
        }));

        // 9. Cross cut: claw and cleaver crossed (0-9), both rip outward at 11 – X-shaped double cut
        out.add(Ability.of("cross_cut", 30, 70).range(0, 3.4).weight(2).tick((e, t, tk) -> {
            if (tk == 11) {
                cut(e, 3.0, 55, e.dmg(0.8f), 0, 0, 0, false);
                slashArc(e, 2.4f, 120, 45, 0, 1.1, SLASH);
                slashArc(e, 2.2f, 120, -45, 0, 1.1, SLASH_RED);
            }
            if (tk == 13) {
                cut(e, 3.0, 55, e.dmg(0.8f), 0.8, 0.2, 60, true);
                FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_STRONG, 1f, 0.9f);
            }
        }));

        // 10. ENRAGED – Execution: shadow step behind (8), cross slash (16), launcher (26), leap (30), front-flip plunge (46)
        out.add(Ability.of("execution", 80, 240).range(0, 12).weight(3).when(FpeEntity::isEnraged).tick((e, t, tk) -> {
            if (tk == 0) FpeUtil.sound(e, SoundEvents.VEX_CHARGE, 1.2f, 0.4f);
            if (tk < 8 && tk % 2 == 0) FpeUtil.particles(e, ParticleTypes.SQUID_INK, e.position().add(0, 0.2, 0), 8, 0.4, 0.1, 0.4, 0.02);
            if (tk == 8) shadowStep(e, t);
            if (tk == 16) {
                cut(e, 3.0, 70, e.dmg(0.9f), 0.1, 0, 60, true);
                slashArc(e, 3.0f, 170, 0, 0, 1.1, SLASH_RED);
                FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_SWEEP, 1f, 0.9f);
            }
            if (tk == 26) {
                cut(e, 3.0, 50, e.dmg(1.0f), 0.2, 1.1, 0, true);
                slashArc(e, 2.6f, 120, -80, 0, 0.3, SLASH);
                FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_STRONG, 1f, 1.1f);
            }
            if (tk == 30) e.dashToward(t.position(), Math.min(0.9, e.distanceTo(t) * 0.12), 0.85);
            if (tk > 30 && tk < 46 && tk % 2 == 0) FpeUtil.particles(e, ParticleTypes.SQUID_INK, e.position().add(0, 1, 0), 3, 0.3, 0.3, 0.3, 0.01);
            if (tk == 40) e.setDeltaMovement(e.getDeltaMovement().x * 0.5, -1.2, e.getDeltaMovement().z * 0.5);
            if (tk == 46) {
                Vec3 at = FpeUtil.ahead(e, 1.2, 0.05);
                for (LivingEntity v : FpeUtil.enemiesInRadius(e, at, 3.2, 3, 1.5)) {
                    v.invulnerableTime = 0;
                    if (FpeUtil.hit(e, v, e.dmg(2.0f), 1.2, 0.5)) bleed(e, v, 100);
                }
                FpeUtil.fx(e, FpeFx.Kind.RING_SHOCK, at, 0, 14, 5f, e.dmg(0.7f)).color(0xC0901828);
                for (int i = 0; i < 6; i++) FpeUtil.fx(e, FpeFx.Kind.SPIKE, at.add(rotY(new Vec3(3.0, 0, 0), i * 60 + 30)), 5 + i % 2 * 3, 30, 1.2f, e.dmg(0.8f));
                FpeUtil.particles(e, ParticleTypes.EXPLOSION, at, 2, 0.5, 0.1, 0.5, 0);
                FpeUtil.particles(e, BLOOD, at.add(0, 0.5, 0), 40, 1.2, 0.4, 1.2, 0.1);
                FpeUtil.sound(e, SoundEvents.GENERIC_EXPLODE, 1f, 0.6f);
                FpeUtil.sound(e, SoundEvents.ANVIL_LAND, 0.8f, 0.5f);
            }
            if (tk == 70) FpeUtil.particles(e, BLOOD, e.position().add(FpeUtil.forward(e).scale(0.6)).add(FpeUtil.right(e).scale(-0.9)).add(0, 0.4, 0), 14, 0.5, 0.1, 0.5, 0.05);
        }));
    }

    // ------------------------------------------------------------------ sounds
    @Override protected SoundEvent getAmbientSound() { return SoundEvents.VEX_AMBIENT; }
    @Override protected SoundEvent getHurtSound(DamageSource s) { return SoundEvents.VEX_HURT; }
    @Override protected SoundEvent getDeathSound() { return SoundEvents.VEX_DEATH; }
    @Override public float getVoicePitch() { return 0.6f; }
    @Override public int getAmbientSoundInterval() { return 260; }
}
