package com.fpe.entity;

import java.util.List;

import com.fpe.registry.ModEntities;

import net.minecraft.core.particles.ParticleOptions;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundSource;
import net.minecraft.util.Mth;
import net.minecraft.world.entity.Entity;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.Vec3;

/** Toolbox for ability authors. All methods are server-side unless noted. */
public final class FpeUtil {
    private FpeUtil() {}

    public static boolean isAlly(Entity a, Entity b) {
        if (b == a) return true;
        if (!(b instanceof FpeEntity fb)) return false;
        return !(a instanceof FpeEntity fa) || !FpeEntity.hostile(fa.faction(), fb.faction());
    }

    public static boolean canHurt(Entity attacker, Entity victim) {
        if (!(victim instanceof LivingEntity l) || !l.isAlive() || isAlly(attacker, victim)) return false;
        return !(victim instanceof Player p) || (!p.isCreative() && !p.isSpectator());
    }

    /** unit forward vector (horizontal) of the entity */
    public static Vec3 forward(Entity e) { return Vec3.directionFromRotation(0, e.getYRot()); }
    /** unit right-hand vector (horizontal) */
    public static Vec3 right(Entity e) { Vec3 f = forward(e); return new Vec3(-f.z, 0, f.x); }

    public static Vec3 ahead(Entity e, double dist, double yOff) { return e.position().add(forward(e).scale(dist)).add(0, yOff, 0); }

    /** knock victim away from `from` horizontally with extra upward component */
    public static void knock(LivingEntity v, Vec3 from, double strength, double up) {
        Vec3 d = new Vec3(v.getX() - from.x, 0, v.getZ() - from.z);
        if (d.lengthSqr() < 1.0E-4) d = new Vec3(0, 0, 1);
        d = d.normalize().scale(strength * (1.0 - v.getAttributeValue(Attributes.KNOCKBACK_RESISTANCE)));
        v.setDeltaMovement(v.getDeltaMovement().x * 0.3 + d.x, Math.max(v.getDeltaMovement().y, up), v.getDeltaMovement().z * 0.3 + d.z);
        v.hasImpulse = true;
        v.hurtMarked = true;
    }

    /** damage + knockback; returns true if hurt */
    public static boolean hit(FpeEntity src, LivingEntity v, float damage, double knock, double up) {
        if (!canHurt(src, v)) return false;
        boolean ok = v.hurt(src.damageSources().mobAttack(src), damage);
        if (ok && knock != 0) knock(v, src.position(), knock, up);
        return ok;
    }

    public static List<LivingEntity> enemiesInRadius(Entity src, Vec3 c, double r, double up, double down) {
        AABB box = new AABB(c.x - r - 1, c.y - down, c.z - r - 1, c.x + r + 1, c.y + up, c.z + r + 1);
        return src.level().getEntitiesOfClass(LivingEntity.class, box, v -> {
            if (!canHurt(src, v)) return false;
            double rr = r + v.getBbWidth() * 0.5;
            double dx = v.getX() - c.x, dz = v.getZ() - c.z;
            return dx * dx + dz * dz <= rr * rr;
        });
    }

    /** damage everything in a horizontal cone in front of the entity (range, half angle degrees). Returns number hit. */
    public static int hitCone(FpeEntity src, double range, double halfAngleDeg, float damage, double knock, double up) {
        Vec3 f = forward(src);
        int n = 0;
        AABB box = src.getBoundingBox().inflate(range, 1.5, range);
        for (LivingEntity v : src.level().getEntitiesOfClass(LivingEntity.class, box, x -> canHurt(src, x))) {
            Vec3 d = new Vec3(v.getX() - src.getX(), 0, v.getZ() - src.getZ());
            double dist = d.length() - v.getBbWidth() * 0.5 - src.getBbWidth() * 0.5;
            if (dist > range) continue;
            if (d.lengthSqr() > 0.01 && Math.toDegrees(Math.acos(Mth.clamp(d.normalize().dot(f), -1, 1))) > halfAngleDeg) continue;
            if (hit(src, v, damage, knock, up)) n++;
        }
        return n;
    }

    /** damage in a radius around a point */
    public static int hitRadius(FpeEntity src, Vec3 c, double r, float damage, double knock, double up) {
        int n = 0;
        for (LivingEntity v : enemiesInRadius(src, c, r, 2.5, 1.0)) if (hit(src, v, damage, knock, up)) n++;
        return n;
    }

    /** damage along a segment (beam / thrust / bullet). radius = beam half-width. */
    public static int hitLine(FpeEntity src, Vec3 from, Vec3 to, double radius, float damage, double knock, double up) {
        int n = 0;
        AABB box = new AABB(from, to).inflate(radius + 1);
        for (LivingEntity v : src.level().getEntitiesOfClass(LivingEntity.class, box, x -> canHurt(src, x))) {
            AABB bb = v.getBoundingBox().inflate(radius);
            if (bb.clip(from, to).isPresent() || bb.contains(from)) { if (hit(src, v, damage, knock, up)) n++; }
        }
        return n;
    }

    // ----------------------------------------------------------------- effects
    public static void particles(Entity e, ParticleOptions p, Vec3 at, int count, double dx, double dy, double dz, double speed) {
        if (e.level() instanceof ServerLevel s) s.sendParticles(p, at.x, at.y, at.z, count, dx, dy, dz, speed);
    }

    /** a ring/arc of particles on the horizontal plane. yawCenter degrees (MC yaw), halfAngle degrees (180 = full circle). */
    public static void arc(Entity e, ParticleOptions p, Vec3 c, float yawCenter, double halfAngle, double radius, int count) {
        if (!(e.level() instanceof ServerLevel s)) return;
        for (int i = 0; i < count; i++) {
            double a = Math.toRadians(yawCenter + (count == 1 ? 0 : -halfAngle + 2 * halfAngle * i / (double) (count - 1)));
            s.sendParticles(p, c.x - Math.sin(a) * radius, c.y, c.z + Math.cos(a) * radius, 1, 0, 0, 0, 0);
        }
    }

    public static void sound(Entity e, SoundEvent s, float vol, float pitch) {
        e.level().playSound(null, e.getX(), e.getY(), e.getZ(), s, SoundSource.HOSTILE, vol, pitch);
    }

    // ----------------------------------------------------------------- spawning
    public static FpeProjectile projectile(FpeEntity owner, FpeProjectile.Kind kind, Vec3 pos, Vec3 vel, float damage) {
        FpeProjectile p = new FpeProjectile(ModEntities.PROJECTILE.get(), owner.level());
        p.setOwner(owner);
        p.setKind(kind);
        p.setDamage(damage);
        p.setPos(pos);
        p.setDeltaMovement(vel);
        owner.level().addFreshEntity(p);
        return p;
    }

    /** velocity from `from` to target's chest at `speed` (lead 0..1 = how much to predict target movement) */
    public static Vec3 aim(Vec3 from, LivingEntity t, double speed, double lead) {
        Vec3 to = t.position().add(0, t.getBbHeight() * 0.6, 0).add(t.getDeltaMovement().scale(lead * 8));
        return to.subtract(from).normalize().scale(speed);
    }

    public static FpeFx fx(FpeEntity owner, FpeFx.Kind kind, Vec3 pos, int warmup, int life, float radius, float damage) {
        FpeFx f = new FpeFx(ModEntities.FX.get(), owner.level());
        f.setOwner(owner);
        f.setup(kind, warmup, life, radius, damage);
        f.setPos(pos);
        f.setYRot(owner.getYRot());
        owner.level().addFreshEntity(f);
        return f;
    }
}
