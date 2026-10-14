package com.fpe.entity.characters;

import java.util.List;

import com.fpe.entity.Ability;
import com.fpe.entity.FpeEntity;
import com.fpe.entity.FpeFx;
import com.fpe.entity.FpeProjectile.Kind;
import com.fpe.entity.FpeUtil;

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
import net.minecraft.world.phys.Vec3;

/**
 * Danger AU Bloomie: a silent rifle gunner who keeps her distance. Many weak bullets, a grenade launcher,
 * and close-quarters answers (hip-fire blast, rifle butt, ribbon lash, back-flip). Spray/suppress/hail end in a
 * forced, vulnerable reload.
 */
public class DangerBloomie extends FpeEntity {
    public DangerBloomie(EntityType<? extends FpeEntity> type, Level level) { super(type, level); }

    @Override public Faction faction() { return Faction.DANGER; }

    public static AttributeSupplier.Builder attributes() { return baseAttributes(100, 6, 0.27, 6, 0.4); }

    @Override public double preferredDistance() { return 8.0; }

    @Override protected SoundEvent getHurtSound(DamageSource s) { return SoundEvents.IRON_GOLEM_HURT; }
    @Override protected SoundEvent getDeathSound() { return SoundEvents.IRON_GOLEM_DEATH; }

    /** reloading leaves her open: +50% damage taken */
    @Override
    public boolean hurt(DamageSource s, float amount) {
        return super.hurt(s, "reload".equals(currentAbilityId()) ? amount * 1.5f : amount);
    }

    // ------------------------------------------------------------------ gun helpers
    static Vec3 muzzle(FpeEntity e) {
        return e.position().add(0, 1.45, 0).add(FpeUtil.forward(e).scale(1.35)).add(FpeUtil.right(e).scale(0.22));
    }

    static Vec3 spread(FpeEntity e, Vec3 v, double deg) {
        double s = Math.tan(Math.toRadians(deg)) * v.length();
        return v.add(e.getRandom().nextGaussian() * s, e.getRandom().nextGaussian() * s * 0.6, e.getRandom().nextGaussian() * s);
    }

    static void shot(FpeEntity e, Vec3 from, Vec3 vel, float dmg, boolean loud) {
        FpeUtil.projectile(e, Kind.BULLET, from, vel, dmg);
        FpeUtil.particles(e, ParticleTypes.FLAME, from, 2, 0.05, 0.05, 0.05, 0.02);
        FpeUtil.particles(e, ParticleTypes.SMOKE, from, 1, 0.05, 0.05, 0.05, 0.01);
        if (loud) FpeUtil.sound(e, SoundEvents.FIREWORK_ROCKET_BLAST, 0.9f, 1.7f + e.getRandom().nextFloat() * 0.2f);
        FpeUtil.sound(e, SoundEvents.CROSSBOW_SHOOT, 0.4f, 1.9f);
    }

    /** aimed bullet at the target's chest from the muzzle */
    static void aimed(FpeEntity e, LivingEntity t, double deg, float mult) {
        Vec3 m = muzzle(e);
        shot(e, m, spread(e, FpeUtil.aim(m, t, 3.0, 0.5), deg), e.dmg(mult), true);
    }

    static Vec3 lob(Vec3 from, Vec3 to, double g, int ticks) {
        double f = ticks * 0.02 / (1 - Math.pow(0.98, ticks));
        return new Vec3((to.x - from.x) / ticks * f, ((to.y - from.y) / ticks + 0.5 * g * ticks) * f, (to.z - from.z) / ticks * f);
    }

    @Override
    protected void registerAbilities(List<Ability> out) {
        // 1. shouldered double three-round burst
        out.add(Ability.of("burst", 30, 28).range(3, 22).weight(5).tick((e, t, tk) -> {
            if (tk == 6) FpeUtil.sound(e, SoundEvents.ARMOR_EQUIP_CHAIN, 0.8f, 0.7f);
            if ((tk >= 10 && tk <= 14 || tk >= 20 && tk <= 24) && tk % 2 == 0) aimed(e, t, 2.0, 0.4f);
        }));
        // 2. full-auto strafing spray, sweeping left -> right
        out.add(Ability.of("spray", 52, 110).range(3, 16).weight(3).faceUntil(8).tick((e, t, tk) -> {
            if (tk >= 10 && tk <= 42 && tk % 2 == 0) {
                float off = -40 + 80 * smooth((tk - 10) / 32f);
                Vec3 m = muzzle(e);
                Vec3 to = t.position().add(0, t.getBbHeight() * 0.55, 0);
                double pitch = Math.atan2(to.y - m.y, Math.max(1, Math.hypot(to.x - m.x, to.z - m.z)));
                Vec3 d = Vec3.directionFromRotation(0, e.getYRot() + off);
                Vec3 v = new Vec3(d.x * Math.cos(pitch), Math.sin(pitch), d.z * Math.cos(pitch)).scale(3.0);
                Vec3 from = e.position().add(0, 1.45, 0).add(d.scale(1.35));
                shot(e, from, spread(e, v, 3.0), e.dmg(0.32f), tk % 4 == 0);
            }
        }).end((e, t, tk) -> e.forceAbility("reload")));
        // 3. kneel, underbarrel grenade launcher lob
        out.add(Ability.of("grenade_launcher", 36, 100).range(7, 22).weight(3).tick((e, t, tk) -> {
            if (tk == 11) FpeUtil.sound(e, SoundEvents.CROSSBOW_LOADING_MIDDLE, 1f, 0.6f);
            if (tk == 16) {
                Vec3 m = e.position().add(0, 1.0, 0).add(FpeUtil.forward(e).scale(1.3)).add(FpeUtil.right(e).scale(0.22));
                int fl = (int) Math.max(12, Math.min(30, e.distanceTo(t) * 1.4));
                Vec3 to = t.position().add(t.getDeltaMovement().multiply(fl, 0, fl));
                FpeUtil.projectile(e, Kind.GRENADE, m, lob(m, to, 0.06, fl), e.dmg(1.8f));
                FpeUtil.particles(e, ParticleTypes.LARGE_SMOKE, m, 6, 0.1, 0.1, 0.1, 0.03);
                FpeUtil.sound(e, SoundEvents.DISPENSER_LAUNCH, 1.4f, 0.5f);
            }
        }));
        // 4. hip-fire buckshot cone (close range), recoil slides her back
        out.add(Ability.of("shotgun", 26, 60).range(0, 6).weight(3).tick((e, t, tk) -> {
            if (tk == 10) {
                Vec3 m = e.position().add(0, 1.05, 0).add(FpeUtil.forward(e).scale(1.3)).add(FpeUtil.right(e).scale(0.22));
                Vec3 base = FpeUtil.aim(m, t, 2.6, 0.2);
                for (int i = 0; i < 8; i++) FpeUtil.projectile(e, Kind.BULLET, m, spread(e, base, 11), e.dmg(0.45f));
                FpeUtil.particles(e, ParticleTypes.FLAME, m, 12, 0.2, 0.15, 0.2, 0.08);
                FpeUtil.particles(e, ParticleTypes.LARGE_SMOKE, m, 6, 0.2, 0.1, 0.2, 0.04);
                FpeUtil.sound(e, SoundEvents.GENERIC_EXPLODE, 0.8f, 1.8f);
                FpeUtil.hitCone(e, 2.2, 40, e.dmg(0.6f), 1.0, 0.25);
                e.dashForward(-0.45, 0.05);
            }
        }));
        // 5. flip the rifle and ram the stock forward
        out.add(Ability.of("butt_bash", 26, 40).range(0, 3.2).weight(4).tick((e, t, tk) -> {
            if (tk == 9) e.dashForward(0.4, 0.05);
            if (tk == 11) {
                if (FpeUtil.hitCone(e, 3.2, 60, e.dmg(1.4f), 1.2, 0.35) > 0) FpeUtil.sound(e, SoundEvents.ZOMBIE_ATTACK_IRON_DOOR, 0.8f, 1.3f);
                else FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_SWEEP, 1f, 0.7f);
                FpeUtil.particles(e, ParticleTypes.CRIT, FpeUtil.ahead(e, 1.5, 1.3), 8, 0.2, 0.2, 0.2, 0.2);
            }
        }));
        // 6. heel spin: the two long hazard ribbons lash everything around her twice
        out.add(Ability.of("ribbon_whip", 34, 70).range(0, 4.5).weight(3).tick((e, t, tk) -> {
            if (tk == 11) FpeUtil.fx(e, FpeFx.Kind.ARC, e.position().add(0, 1.5, 0), 0, 8, 4.2f, 0).param(320).color(0xFFDCC690);
            if (tk == 15) FpeUtil.fx(e, FpeFx.Kind.ARC, e.position().add(0, 1.1, 0), 0, 8, 4.0f, 0).param(320).color(0xFF16161C);
            if (tk == 12 || tk == 16) {
                FpeUtil.hitRadius(e, e.position(), 4.0, e.dmg(tk == 12 ? 1.0f : 0.8f), 0.9, 0.3);
                FpeUtil.arc(e, ParticleTypes.SWEEP_ATTACK, e.position().add(0, 1.4, 0), e.getYRot(), 180, 3.0, 8);
                FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_SWEEP, 1f, tk == 12 ? 0.6f : 0.8f);
            }
        }));
        // 7. kneeling suppressive fire: steady stream, pins the target (slowness)
        out.add(Ability.of("suppress", 64, 160).range(6, 26).weight(2).tick((e, t, tk) -> {
            if (tk >= 14 && tk <= 56 && (tk - 14) % 3 == 0) {
                aimed(e, t, 4.5, 0.3f);
                if (tk % 12 == 2 && e.hasLineOfSight(t)) t.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 30, 1));
            }
        }).end((e, t, tk) -> e.forceAbility("reload")));
        // 8. forced reload after long strings of fire (never picked randomly) - she takes +50% damage meanwhile
        out.add(Ability.of("reload", 32, 0).range(0, 99).blind().when(e -> false).tick((e, t, tk) -> {
            if (tk == 9) FpeUtil.sound(e, SoundEvents.IRON_TRAPDOOR_OPEN, 0.8f, 1.6f);
            if (tk == 13) FpeUtil.sound(e, SoundEvents.ARMOR_EQUIP_IRON, 0.6f, 1.4f);
            if (tk == 20) FpeUtil.sound(e, SoundEvents.CROSSBOW_LOADING_END, 1f, 1.2f);
            if (tk == 25) FpeUtil.sound(e, SoundEvents.IRON_TRAPDOOR_CLOSE, 1f, 1.8f);
        }));
        // 9. back-flip away from melee range, snap shot on landing
        out.add(Ability.of("backstep", 22, 70).range(0, 3.5).weight(3).tick((e, t, tk) -> {
            if (tk == 4) {
                e.dashToward(e.position().add(e.position().subtract(t.position())), 0.85, 0.42);
                FpeUtil.sound(e, SoundEvents.ARMOR_EQUIP_LEATHER, 1f, 0.8f);
            }
            if (tk == 16) aimed(e, t, 1.0, 0.6f);
        }));
        // 10. ENRAGED: empty the drum into the sky, then the bullets hail down on the target while she keeps firing
        out.add(Ability.of("bullet_hail", 84, 240).range(0, 26).weight(4).when(FpeEntity::isEnraged).tick((e, t, tk) -> {
            if (tk >= 12 && tk <= 40 && tk % 2 == 0) {
                Vec3 m = e.position().add(0, 2.6, 0).add(FpeUtil.forward(e).scale(0.4));
                shot(e, m, spread(e, new Vec3(0, 3.0, 0), 6), 0f, tk % 4 == 0);
            }
            if (tk == 30) FpeUtil.arc(e, ParticleTypes.CRIT, t.position().add(0, 0.1, 0), 0, 180, 3.5, 30);
            if (tk >= 36 && tk <= 76) {
                for (int i = 0; i < 2; i++) {
                    Vec3 at = t.position().add((e.getRandom().nextDouble() - 0.5) * 7, 16, (e.getRandom().nextDouble() - 0.5) * 7);
                    FpeUtil.projectile(e, Kind.BULLET, at, new Vec3((e.getRandom().nextDouble() - 0.5) * 0.2, -3.0, (e.getRandom().nextDouble() - 0.5) * 0.2), e.dmg(0.3f));
                }
            }
            if (tk >= 50 && tk <= 74 && (tk - 50) % 4 == 0) aimed(e, t, 2.5, 0.35f);
        }).end((e, t, tk) -> e.forceAbility("reload")));
    }

    private static float smooth(float x) { x = Math.max(0, Math.min(1, x)); return x * x * (3 - 2 * x); }
}
