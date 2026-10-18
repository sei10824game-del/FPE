package com.fpe.entity.characters;

import java.util.List;

import com.fpe.entity.Ability;
import com.fpe.entity.FpeCombat;
import com.fpe.entity.FpeEntity;
import com.fpe.entity.FpeFx;
import com.fpe.entity.FpeProjectile.Kind;
import com.fpe.entity.FpeUtil;

import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.Vec3;

/**
 * Miss Thavel "the bomb": cheerful explosives teacher. Every attack is a different way of delivering a bang.
 * All explosions are entity-only (FpeProjectile detonate / hitRadius): blocks are never broken.
 */
public class MissBloomie extends FpeEntity {
    public MissBloomie(EntityType<? extends FpeEntity> type, Level level) { super(type, level); }

    @Override public Faction faction() { return Faction.MISS; }

    public static AttributeSupplier.Builder attributes() { return baseAttributes(90, 7, 0.29, 4, 0.3); }

    @Override public double preferredDistance() { return 5.0; }

    @Override protected SoundEvent getAmbientSound() { return SoundEvents.WITCH_CELEBRATE; }
    @Override protected SoundEvent getHurtSound(net.minecraft.world.damagesource.DamageSource s) { return SoundEvents.WITCH_HURT; }
    @Override protected SoundEvent getDeathSound() { return SoundEvents.GENERIC_EXPLODE; }

    // ------------------------------------------------------------------ helpers
    /** approx world position of a hand (side: +1 left, -1 right) */
    static Vec3 hand(FpeEntity e, int side, double up, double fwd) {
        return e.position().add(0, up, 0).add(FpeUtil.forward(e).scale(fwd)).add(FpeUtil.right(e).scale(-0.35 * side));
    }

    /** ballistic lob (gravity g, drag 0.98) landing at `to` after `ticks` */
    static Vec3 lob(Vec3 from, Vec3 to, double g, int ticks) {
        double f = ticks * 0.02 / (1 - Math.pow(0.98, ticks));
        double vx = (to.x - from.x) / ticks, vz = (to.z - from.z) / ticks;
        double vy = (to.y - from.y) / ticks + 0.5 * g * ticks;
        return new Vec3(vx * f, vy * f, vz * f);
    }

    static Vec3 lead(LivingEntity t, double ticks) { return t.position().add(t.getDeltaMovement().multiply(ticks, 0, ticks)); }

    static void boom(FpeEntity e, Vec3 at, double r, float dmg, double knock) {
        FpeUtil.particles(e, ParticleTypes.EXPLOSION_EMITTER, at, 1, 0, 0, 0, 0);
        FpeUtil.particles(e, ParticleTypes.EXPLOSION, at, (int) (r * 3), r * 0.5, 0.4, r * 0.5, 0);
        FpeUtil.particles(e, ParticleTypes.FLAME, at, (int) (r * 10), r * 0.4, 0.3, r * 0.4, 0.08);
        FpeUtil.particles(e, ParticleTypes.LARGE_SMOKE, at, (int) (r * 6), r * 0.4, 0.4, r * 0.4, 0.03);
        e.level().playSound(null, at.x, at.y, at.z, SoundEvents.GENERIC_EXPLODE, net.minecraft.sounds.SoundSource.HOSTILE, (float) Math.min(3, r * 0.6), 1.0f);
        FpeUtil.hitRadius(e, at, r, dmg, knock, 0.6);
    }

    private static Vec3 rand(FpeEntity e, double r) {
        return new Vec3((e.getRandom().nextDouble() - 0.5) * 2 * r, 0, (e.getRandom().nextDouble() - 0.5) * 2 * r);
    }

    @Override
    protected void registerAbilities(List<Ability> out) {
        // 1. pull the pin with her teeth, big overhand lob
        out.add(Ability.of("grenade_lob", 30, 45).range(3.5, 16).weight(4).tick((e, t, tk) -> {
            if (tk == 6) FpeUtil.sound(e, SoundEvents.TRIPWIRE_CLICK_OFF, 1f, 1.6f);
            if (tk == 16) {
                Vec3 from = hand(e, 1, 2.1, 0.3);
                int fl = (int) Math.max(12, Math.min(28, e.distanceTo(t) * 1.7));
                FpeUtil.projectile(e, Kind.GRENADE, from, lob(from, lead(t, fl).add(0, 0.2, 0), 0.06, fl), e.dmg(1.8f));
                FpeUtil.sound(e, SoundEvents.SNOWBALL_THROW, 1f, 0.6f);
            }
        }));
        // 2. rip the bandolier open: a fan of seven bomblets
        out.add(Ability.of("bandolier_burst", 36, 90).range(2, 10).weight(3).tick((e, t, tk) -> {
            if (tk == 6) FpeUtil.sound(e, SoundEvents.TNT_PRIMED, 1f, 1.4f);
            if (tk == 14) {
                Vec3 c = e.position().add(0, 1.4, 0);
                for (int i = 0; i < 7; i++) {
                    float yaw = e.getYRot() - 66 + i * 22;
                    Vec3 d = Vec3.directionFromRotation(0, yaw);
                    double sp = 0.45 + Math.min(0.5, e.distanceTo(t) * 0.04) + (i % 2) * 0.12;
                    FpeUtil.projectile(e, Kind.BOMBLET, c.add(d.scale(0.5)), new Vec3(d.x * sp, 0.42 + (i % 3) * 0.06, d.z * sp), e.dmg(0.9f));
                }
                FpeUtil.particles(e, ParticleTypes.CRIT, c, 20, 0.6, 0.3, 0.6, 0.3);
                FpeUtil.sound(e, SoundEvents.CROSSBOW_SHOOT, 1f, 0.7f);
                FpeUtil.sound(e, SoundEvents.WITCH_CELEBRATE, 1f, 1.3f);
            }
        }));
        // 3. kneeling pirouette sowing timed mines around herself + a few tossed around the target, then hop away
        out.add(Ability.of("mine_field", 44, 140).range(0, 8).weight(2).faceUntil(10).tick((e, t, tk) -> {
            if (tk >= 12 && tk <= 28 && (tk - 12) % 4 == 0) {
                float yaw = e.getYRot() + (tk - 12) / 16f * 360f;
                Vec3 d = Vec3.directionFromRotation(0, yaw);
                for (double r : new double[] {1.8, 3.3}) {
                    Vec3 at = e.position().add(d.scale(r)).add(0, 0.3, 0);
                    FpeUtil.projectile(e, Kind.BOMBLET, at, new Vec3(d.x * 0.02, 0.05, d.z * 0.02), e.dmg(1.0f));
                }
                FpeUtil.sound(e, SoundEvents.STONE_BUTTON_CLICK_ON, 0.8f, 1.5f);
                FpeUtil.particles(e, ParticleTypes.SMOKE, e.position().add(d.scale(1.8)), 4, 0.2, 0.1, 0.2, 0.01);
            }
            if (tk == 20) for (int i = 0; i < 3; i++) {
                Vec3 from = hand(e, -1, 1.2, 0.5);
                Vec3 to = t.position().add(Vec3.directionFromRotation(0, i * 120 + e.getRandom().nextInt(60)).scale(2.2));
                FpeUtil.projectile(e, Kind.BOMBLET, from, lob(from, to, 0.06, 14), e.dmg(0.9f));
            }
            if (tk == 32) {
                Vec3 away = e.position().add(e.position().subtract(t.position()));
                e.dashToward(away, 0.75, 0.45);
                FpeUtil.sound(e, SoundEvents.WITCH_CELEBRATE, 1f, 1.5f);
            }
        }));
        // 4. pull a rocket launcher out of her hair, kneel, fire
        out.add(Ability.of("rocket", 44, 110).range(6, 24).weight(3).faceUntil(24).tick((e, t, tk) -> {
            if (tk == 8) FpeUtil.sound(e, SoundEvents.ARMOR_EQUIP_IRON, 1f, 0.8f);
            if (tk == 20) FpeUtil.sound(e, SoundEvents.CROSSBOW_LOADING_END, 1f, 0.7f);
            if (tk == 24) {
                Vec3 from = e.position().add(0, 1.35, 0).add(FpeUtil.forward(e).scale(1.1)).add(FpeUtil.right(e).scale(0.35));
                FpeUtil.projectile(e, Kind.ROCKET, from, FpeUtil.aim(from, t, 1.25, 0.6), e.dmg(2.0f));
                Vec3 back = from.subtract(FpeUtil.forward(e).scale(1.6));
                FpeUtil.particles(e, ParticleTypes.LARGE_SMOKE, back, 14, 0.3, 0.2, 0.3, 0.05);
                FpeUtil.particles(e, ParticleTypes.FLAME, back, 10, 0.2, 0.2, 0.2, 0.06);
                FpeUtil.sound(e, SoundEvents.FIREWORK_ROCKET_LAUNCH, 2f, 0.5f);
                e.dashForward(-0.35, 0.05);
            }
        }));
        // 5. hurl bombs into the sky, they rain down around the target
        out.add(Ability.of("bomb_rain", 56, 160).range(4, 20).weight(2).tick((e, t, tk) -> {
            if (tk == 4) FpeUtil.sound(e, SoundEvents.WITCH_CELEBRATE, 1.2f, 1.1f);
            if (tk == 15) {
                FpeUtil.particles(e, ParticleTypes.FIREWORK, e.position().add(0, 2.4, 0), 20, 0.2, 0.6, 0.2, 0.25);
                FpeUtil.sound(e, SoundEvents.FIREWORK_ROCKET_LAUNCH, 1.5f, 0.8f);
            }
            if (tk == 18) FpeUtil.arc(e, ParticleTypes.SMOKE, t.position().add(0, 0.1, 0), 0, 180, 3.5, 24);
            if (tk >= 22 && tk <= 46 && tk % 3 == 1) {
                Vec3 at = lead(t, 6).add(rand(e, 3.5)).add(0, 9, 0);
                FpeUtil.projectile(e, Kind.BOMBLET, at, new Vec3(0, -0.75, 0), e.dmg(1.0f));
            }
        }));
        // 6. kamikaze: light her own antenna, dive-hug the target and explode (she survives, blown back)
        out.add(Ability.of("kamikaze", 50, 220).range(3, 12).weight(2).faceUntil(20).tick((e, t, tk) -> {
            Vec3 head = e.position().add(0, 2.6, 0);
            if (tk == 6) FpeUtil.sound(e, SoundEvents.FLINTANDSTEEL_USE, 1f, 1f);
            if (tk == 9) FpeUtil.sound(e, SoundEvents.TNT_PRIMED, 1.5f, 0.9f);
            if (tk > 6 && tk < 28) {
                FpeUtil.particles(e, ParticleTypes.FLAME, head, 2, 0.05, 0.05, 0.05, 0.02);
                FpeUtil.particles(e, ParticleTypes.SMOKE, head, 1, 0.05, 0.1, 0.05, 0.02);
            }
            if (tk == 16) {
                double d = e.distanceTo(t);
                e.dashToward(t.position(), Math.min(1.7, 0.35 + d * 0.12), 0.32);
                FpeUtil.sound(e, SoundEvents.WITCH_CELEBRATE, 1.5f, 1.6f);
            }
            if (tk == 28) {
                boom(e, e.position().add(0, 1, 0), 4.5, e.dmg(2.3f), 1.7);
                e.dashToward(e.position().add(e.position().subtract(t.position())), 0.8, 0.65);
            }
        }));
        // 7. explosive stomp -> shockwave ring
        out.add(Ability.of("stomp", 32, 70).range(0, 4.5).weight(3).tick((e, t, tk) -> {
            if (tk == 9) e.setDeltaMovement(e.getDeltaMovement().add(0, 0.25, 0));
            if (tk == 13) {
                Vec3 foot = e.position().add(FpeUtil.forward(e).scale(0.3)).add(0, 0.1, 0);
                FpeUtil.particles(e, ParticleTypes.EXPLOSION, foot, 3, 0.4, 0.1, 0.4, 0);
                FpeUtil.particles(e, ParticleTypes.LAVA, foot, 8, 0.6, 0.1, 0.6, 0);
                FpeUtil.sound(e, SoundEvents.GENERIC_EXPLODE, 1.2f, 1.3f);
                FpeUtil.hitRadius(e, foot, 1.9, e.dmg(1.3f), 1.0, 0.6);
                FpeUtil.fx(e, FpeFx.Kind.RING_SHOCK, foot, 0, 14, 5.5f, e.dmg(1.0f));
            }
        }));
        // 8. flick the grenade up and volley-kick it at the target (plus the kick itself hurts up close)
        out.add(Ability.of("kick_back", 38, 90).range(1.5, 9).weight(3).tick((e, t, tk) -> {
            if (tk == 4) FpeUtil.sound(e, SoundEvents.TRIPWIRE_CLICK_OFF, 1f, 1.6f);
            if (tk == 16) {
                Vec3 from = e.position().add(0, 0.5, 0).add(FpeUtil.forward(e).scale(0.7));
                Vec3 v = FpeUtil.aim(from, t, 1.45, 0.4).add(0, 0.06 + e.distanceTo(t) * 0.012, 0);
                FpeUtil.projectile(e, Kind.BOMBLET, from, v, e.dmg(1.6f));
                FpeUtil.hitCone(e, 2.4, 50, e.dmg(0.9f), 0.9, 0.4);
                FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_STRONG, 1f, 0.8f);
                FpeUtil.particles(e, ParticleTypes.CRIT, from, 10, 0.2, 0.2, 0.2, 0.3);
            }
        }));
        // 9. point-blank grenade punch
        out.add(Ability.of("boom_punch", 24, 35).range(0, 3).weight(4).tick((e, t, tk) -> {
            if (tk == 8) e.dashForward(0.45, 0.05);
            if (tk == 11) {
                Vec3 fist = FpeUtil.ahead(e, 1.4, 1.3);
                FpeUtil.particles(e, ParticleTypes.EXPLOSION, fist, 2, 0.2, 0.2, 0.2, 0);
                FpeUtil.particles(e, ParticleTypes.FLAME, fist, 12, 0.3, 0.3, 0.3, 0.06);
                FpeUtil.sound(e, SoundEvents.GENERIC_EXPLODE, 0.9f, 1.5f);
                FpeUtil.hitCone(e, 2.9, 55, e.dmg(1.5f), 1.2, 0.45);
            }
        }));
        // 11. canon claws: downward rake + backhand return rake
        out.add(Ability.of("claw_rake", 28, 40).range(0, 3.2).weight(4).faceUntil(15).tick((e, t, tk) -> {
            if (tk == 7) e.dashForward(0.3, 0.02);
            if (tk == 9 || tk == 17) {
                FpeCombat.slashArc(e, 2.6f, 120, tk == 9 ? 70 : -20, tk == 9 ? 0 : 10, 1.3, FpeCombat.SLASH);
                FpeCombat.cut(e, 3.0, 65, e.dmg(tk == 9 ? 1.0f : 1.2f), 0.5, 0.2, tk == 17 ? 40 : 0, true);
                FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_SWEEP, 1f, tk == 9 ? 1.4f : 1.1f);
            }
        }));
        // 12. the big striped cleaver: wide horizontal sweep
        out.add(Ability.of("cleaver_slash", 34, 70).range(0, 4.2).weight(3).faceUntil(12).tick((e, t, tk) -> {
            if (tk == 8) FpeUtil.sound(e, SoundEvents.ARMOR_EQUIP_IRON, 1f, 0.6f);
            if (tk == 13) e.dashForward(0.35, 0.02);
            if (tk == 15) {
                FpeCombat.slashArc(e, 4.4f, 200, 0, 0, 1.0, FpeCombat.SLASH);
                FpeCombat.cut(e, 4.4, 100, e.dmg(1.6f), 1.1, 0.3, 0, false);
                FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_SWEEP, 1.4f, 0.6f);
            }
        }));
        // 13. overhead chop that launches a cleaver wave along the ground
        out.add(Ability.of("blade_wave", 36, 90).range(4, 14).weight(3).faceUntil(16).tick((e, t, tk) -> {
            if (tk == 10) FpeUtil.sound(e, SoundEvents.TRIDENT_RETURN, 1f, 0.7f);
            if (tk == 18) {
                Vec3 from = FpeUtil.ahead(e, 1.2, 0.8);
                Vec3 d = FpeUtil.aim(from, t, 1.1, 0.3);
                FpeUtil.projectile(e, Kind.BLADE_WAVE, from, new Vec3(d.x, 0, d.z), e.dmg(1.4f));
                FpeCombat.slashArc(e, 2.8f, 140, 90, 0, 1.2, FpeCombat.SLASH);
                FpeCombat.cut(e, 2.6, 40, e.dmg(1.2f), 0.6, 0.3, 0, false);
                FpeUtil.particles(e, ParticleTypes.CRIT, FpeUtil.ahead(e, 1.6, 0.1), 16, 0.5, 0.1, 0.5, 0.2);
                FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_STRONG, 1.2f, 0.6f);
            }
        }));
        // 14. ENRAGED signature: three spinning cleaver slashes, each leaves a bomblet; then she lights her fuse and blows the whole ring
        out.add(Ability.of("detonation_dance", 52, 200).range(0, 5).weight(3).when(FpeEntity::isEnraged).faceUntil(10).tick((e, t, tk) -> {
            if (tk == 4) FpeUtil.sound(e, SoundEvents.WITCH_CELEBRATE, 1.4f, 1.2f);
            if (tk == 12 || tk == 20 || tk == 28) {
                e.dashToward(t.position(), 0.35, 0.05);
                FpeCombat.slashArc(e, 3.4f, 360, 0, 0, 1.0, FpeCombat.SLASH);
                FpeUtil.hitRadius(e, e.position().add(0, 1, 0), 3.3, e.dmg(0.9f), 0.5, 0.2);
                FpeUtil.projectile(e, Kind.BOMBLET, e.position().add(0, 0.6, 0), rand(e, 0.15).add(0, 0.25, 0), e.dmg(0.8f));
                FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_SWEEP, 1.2f, 0.8f + tk * 0.01f);
            }
            if (tk == 34) FpeUtil.sound(e, SoundEvents.TNT_PRIMED, 1.5f, 1.2f);
            if (tk > 34 && tk < 40) FpeUtil.particles(e, ParticleTypes.FLAME, e.position().add(0, 2.5, 0), 2, 0.05, 0.05, 0.05, 0.02);
            if (tk == 40) {
                boom(e, e.position().add(0, 0.8, 0), 4.0, e.dmg(1.8f), 1.4);
                FpeUtil.fx(e, FpeFx.Kind.RING_SHOCK, e.position().add(0, 0.1, 0), 0, 12, 6f, e.dmg(0.8f));
            }
        }));
        // 10. ENRAGED: detonator click -> two lines of falling rockets carpet the ground toward and past the target
        out.add(Ability.of("carpet_bomb", 72, 260).range(0, 26).weight(4).blind().when(FpeEntity::isEnraged).tick((e, t, tk) -> {
            if (tk == 4) FpeUtil.sound(e, SoundEvents.WITCH_CELEBRATE, 1.5f, 0.9f);
            if (tk == 15) FpeUtil.sound(e, SoundEvents.LEVER_CLICK, 1f, 1.8f);
            if (tk == 16) FpeUtil.sound(e, SoundEvents.NOTE_BLOCK_PLING.value(), 2f, 0.5f);
            if (tk >= 18 && tk <= 57 && (tk - 18) % 3 == 0) {
                int k = (tk - 18) / 3; // 0..13
                Vec3 start = e.position().add(FpeUtil.forward(e).scale(2.5));
                Vec3 dir = t.position().subtract(start);
                Vec3 end = t.position().add(new Vec3(dir.x, 0, dir.z).normalize().scale(4));
                Vec3 at = start.lerp(end, k / 13.0).add(FpeUtil.right(e).scale(k % 2 == 0 ? 1.6 : -1.6));
                at = new Vec3(at.x, Math.max(e.getY(), t.getY()) + 14, at.z);
                FpeUtil.projectile(e, Kind.ROCKET, at, new Vec3(0, -1.6, 0), e.dmg(1.3f));
            }
        }));
    }
}
