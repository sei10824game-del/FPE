package com.fpe.entity;

import java.util.ArrayList;
import java.util.List;

import org.joml.Vector3f;

import net.minecraft.core.particles.DustParticleOptions;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.util.Mth;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.Vec3;

/** Shared melee helpers (cone selection, bleeding cuts, slash arcs, shadow step) used by several characters. */
public final class FpeCombat {
    private FpeCombat() {}

    public static final DustParticleOptions BLOOD = new DustParticleOptions(new Vector3f(0.55f, 0.02f, 0.06f), 1.2f);
    public static final int SLASH = 0xE8E8ECF2, SLASH_RED = 0xE0A01828;




    // ------------------------------------------------------------------ helpers
    /** enemies inside a horizontal cone (same rule as FpeUtil.hitCone) so we can bleed exactly who got cut */
    public static List<LivingEntity> cone(FpeEntity e, double range, double halfAngle) {
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
    public static int cut(FpeEntity e, double range, double half, float dmg, double knock, double up, int bleedTicks, boolean resetIframes) {
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

    public static void bleed(FpeEntity e, LivingEntity v, int ticks) {
        v.addEffect(new MobEffectInstance(MobEffects.WITHER, ticks, e.isEnraged() ? 1 : 0));
        FpeUtil.particles(e, BLOOD, v.position().add(0, v.getBbHeight() * 0.6, 0), 12, 0.25, 0.3, 0.25, 0.05);
    }

    public static void slashArc(FpeEntity e, float radius, float sweep, float tilt, float yawOff, double y, int color) {
        FpeFx f = FpeUtil.fx(e, FpeFx.Kind.ARC, e.position().add(0, y, 0), 0, 7, radius, 0).param(sweep).color(color);
        f.setYRot(e.getYRot() + yawOff);
        f.setXRot(tilt);
    }

    public static Vec3 rotY(Vec3 v, double deg) {
        double a = Math.toRadians(deg), c = Math.cos(a), s = Math.sin(a);
        return new Vec3(v.x * c - v.z * s, v.y, v.x * s + v.z * c);
    }

    /** sink into shadow and re-emerge behind the target (falls back to its side / front when blocked) */
    public static void shadowStep(FpeEntity e, LivingEntity t) {
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

}
