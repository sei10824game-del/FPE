package com.fpe.entity.characters;

import java.util.List;

import com.fpe.entity.Ability;
import com.fpe.entity.FpeCombat;
import com.fpe.entity.FpeEntity;
import com.fpe.entity.FpeFx;
import com.fpe.entity.FpeProjectile;
import com.fpe.entity.FpeUtil;

import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.Vec3;

/**
 * Danger AU Circle ("Red Circle"): tall muscular fire teacher. NO compass. Canon: left forearm is a removable flamethrower, right paw is a clawed
 * burnt hand, yellow fleece scarf, red glasses, gold tooth, black horns, combat boots, motorcycle "Jessica Bloody Angel".
 * Ticks match client/spec/RedCircleSpec.
 */
public class RedCircle extends FpeEntity {
    public RedCircle(EntityType<? extends FpeEntity> type, Level level) { super(type, level); }

    @Override public Faction faction() { return Faction.DANGER; }

    public static AttributeSupplier.Builder attributes() { return baseAttributes(170, 8, 0.31, 5, 0.5); }

    @Override public double preferredDistance() { return 3.0; }
    @Override protected int restTicks() { return isEnraged() ? 6 : 14; }
    @Override public boolean fireImmune() { return true; }
    @Override protected SoundEvent getHurtSound(DamageSource s) { return SoundEvents.PLAYER_HURT_ON_FIRE; }
    @Override protected SoundEvent getDeathSound() { return SoundEvents.BLAZE_DEATH; }
    @Override protected SoundEvent getAmbientSound() { return SoundEvents.BLAZE_AMBIENT; }

    /** left forearm nozzle position */
    static Vec3 nozzle(FpeEntity e, double fwd) {
        return e.position().add(0, 1.55, 0).add(FpeUtil.forward(e).scale(fwd)).add(FpeUtil.right(e).scale(-0.45));
    }

    static void burnCone(FpeEntity e, double range, double half, float dmg, int secs) {
        for (LivingEntity v : FpeCombat.cone(e, range, half)) if (FpeUtil.hit(e, v, dmg, 0.2, 0.05)) v.setSecondsOnFire(secs);
    }

    static void burnRadius(FpeEntity e, Vec3 c, double r, float dmg, double kb, int secs) {
        for (LivingEntity v : FpeUtil.enemiesInRadius(e, c, r, 2.5, 1)) if (FpeUtil.hit(e, v, dmg, kb, 0.4)) v.setSecondsOnFire(secs);
    }

    @Override
    protected void registerAbilities(List<Ability> out) {
        // sustained flamethrower sweep
        out.add(Ability.of("flame_stream", 58, 70).range(1.5, 9).weight(5).faceUntil(46).tick((e, t, tk) -> {
            if (tk >= 14 && tk <= 46) {
                Vec3 d = FpeUtil.forward(e), n = nozzle(e, 1.2);
                for (int i = 1; i <= 4; i++) FpeUtil.particles(e, ParticleTypes.FLAME, n.add(d.scale(i * 1.8)), 3, 0.2 + i * 0.12, 0.2 + i * 0.1, 0.2 + i * 0.12, 0.02);
                FpeUtil.particles(e, ParticleTypes.SMOKE, n.add(d.scale(5)), 2, 0.5, 0.4, 0.5, 0.02);
                if (tk % 3 == 0) FpeUtil.sound(e, SoundEvents.BLAZE_SHOOT, 0.5f, 0.7f);
                if (tk % 4 == 0) burnCone(e, 8, 20, e.dmg(0.4f), 4);
            }
        }));
        // fireball
        out.add(Ability.of("fireball", 34, 60).range(5, 22).weight(4).faceUntil(15).tick((e, t, tk) -> {
            if (tk == 15 || (e.isEnraged() && (tk == 19 || tk == 23))) {
                Vec3 from = nozzle(e, 1.5);
                FpeUtil.projectile(e, FpeProjectile.Kind.FIREBALL, from, FpeUtil.aim(from, t, 1.0, 0.4), e.dmg(1.5f));
                FpeUtil.sound(e, SoundEvents.FIRECHARGE_USE, 1f, 0.8f);
                FpeUtil.particles(e, ParticleTypes.FLAME, from, 14, 0.2, 0.2, 0.2, 0.08);
            }
        }));
        // point-blank burst
        out.add(Ability.of("flame_burst", 40, 90).range(0, 5.5).weight(3).faceUntil(10).tick((e, t, tk) -> {
            if (tk == 17) {
                burnRadius(e, e.position(), 5.5, e.dmg(1.3f), 1.5, 5);
                FpeUtil.fx(e, FpeFx.Kind.RING_SHOCK, e.position().add(0, 0.1, 0), 0, 14, 6.5f, 0).color(0xFFFF8020);
                FpeUtil.arc(e, ParticleTypes.FLAME, e.position().add(0, 0.3, 0), 0, 180, 3, 40);
                FpeUtil.particles(e, ParticleTypes.LAVA, e.position().add(0, 1, 0), 20, 1.5, 0.6, 1.5, 0.1);
                FpeUtil.sound(e, SoundEvents.GENERIC_EXPLODE, 0.9f, 1.3f);
            }
        }));
        // burnt claw paw swipes
        out.add(Ability.of("claw", 30, 40).range(0, 4).weight(4).faceUntil(18).tick((e, t, tk) -> {
            if (tk == 9 || tk == 17) {
                for (LivingEntity v : FpeCombat.cone(e, 3.8, 60)) { v.invulnerableTime = 0; FpeUtil.hit(e, v, e.dmg(tk == 9 ? 0.9f : 1.2f), 0.7, 0.25); }
                FpeCombat.slashArc(e, 3.8f, 110, tk == 9 ? 25 : -25, 0, 1.5, 0xE0D8DCE8);
                FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_SWEEP, 1f, 0.7f);
            }
        }));
        // hair lash
        out.add(Ability.of("hair_whip", 32, 60).range(0, 6).weight(3).faceUntil(8).tick((e, t, tk) -> {
            if (tk == 14 || tk == 20) {
                FpeUtil.hitRadius(e, e.position(), 5.6, e.dmg(0.9f), 1.2, 0.3);
                FpeUtil.arc(e, ParticleTypes.SWEEP_ATTACK, e.position().add(0, 1.2, 0), tk * 15f, 180, 4.2, 8);
                FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_SWEEP, 1.2f, 0.5f);
            }
        }));
        // "Jessica Bloody Angel": rev up and ram through
        out.add(Ability.of("bike_charge", 52, 110).range(6, 18).weight(4).moving().faceUntil(18).tick((e, t, tk) -> {
            if (tk < 18 && tk % 3 == 0) {
                FpeUtil.particles(e, ParticleTypes.FLAME, e.position().add(0, 0.2, 0), 4, 0.3, 0.1, 0.3, 0.05);
                FpeUtil.sound(e, SoundEvents.BLAZE_SHOOT, 0.4f, 0.5f);
            }
            if (tk >= 20 && tk <= 36) {
                e.dashForward(1.25, 0);
                FpeUtil.particles(e, ParticleTypes.FLAME, e.position().add(0, 0.3, 0), 5, 0.3, 0.1, 0.3, 0.02);
                FpeUtil.particles(e, ParticleTypes.LARGE_SMOKE, e.position().add(0, 0.4, 0), 2, 0.3, 0.1, 0.3, 0.02);
                for (LivingEntity v : FpeUtil.enemiesInRadius(e, FpeUtil.ahead(e, 1.2, 0), 1.9, 2.5, 0.5))
                    if (FpeUtil.hit(e, v, e.dmg(0.9f), 1.4, 0.45)) v.setSecondsOnFire(3);
            }
        }));
        // molotov: burning circle at the target's feet
        out.add(Ability.of("molotov", 46, 80).range(5, 16).weight(3).faceUntil(12).tick((e, t, tk) -> {
            if (tk == 14) {
                FpeUtil.fx(e, FpeFx.Kind.RING_TRAP, t.position().add(0, 0.05, 0), 24, 34, 3.6f, e.dmg(1.2f)).color(0xFFFF6A20);
                FpeUtil.sound(e, SoundEvents.SPLASH_POTION_THROW, 1f, 0.7f);
                FpeUtil.particles(e, ParticleTypes.FLAME, t.position().add(0, 0.2, 0), 10, 1.2, 0.1, 1.2, 0.02);
            }
            if (tk == 38) burnRadius(e, t.position(), 3.8, 0, 0, 7);
        }));
        // enraged: "I am the FIRE!"
        out.add(Ability.of("inferno", 74, 200).range(0, 14).weight(6).blind().when(FpeEntity::isEnraged).faceUntil(10).tick((e, t, tk) -> {
            if (tk >= 20 && tk <= 62 && tk % 14 == 6) {
                FpeUtil.fx(e, FpeFx.Kind.RING_SHOCK, e.position().add(0, 0.1, 0), 0, 18, 12f, 0).color(0xFFFF7020);
                FpeUtil.sound(e, SoundEvents.BLAZE_SHOOT, 1.2f, 0.5f);
            }
            if (tk >= 20 && tk <= 66 && tk % 6 == 0) {
                double r = 2 + (tk - 20) * 0.22;
                FpeUtil.arc(e, ParticleTypes.FLAME, e.position().add(0, 0.2, 0), 0, 180, r, 36);
                FpeUtil.arc(e, ParticleTypes.LARGE_SMOKE, e.position().add(0, 1.2, 0), 0, 180, r, 18);
                for (LivingEntity v : FpeUtil.enemiesInRadius(e, e.position(), r + 1.5, 3, 1))
                    if (FpeUtil.hit(e, v, e.dmg(0.7f), 0.8, 0.3)) v.setSecondsOnFire(5);
            }
        }));
    }
}
