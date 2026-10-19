package com.fpe.entity.characters;

import java.util.List;

import com.fpe.entity.Ability;
import com.fpe.entity.FpeEntity;
import com.fpe.entity.FpeFx;
import com.fpe.entity.FpeProjectile;
import com.fpe.entity.FpeUtil;

import net.minecraft.core.particles.DustParticleOptions;
import net.minecraft.core.particles.ParticleOptions;
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
 * Mutant Bubble (FPE Green, mutant 003): tiny foam-cloud kid in a white straitjacket with a rubber duck on its head.
 * Sleeve slaps, head bonk, soap spray, wand bubble volley, bubble prison, foam wave, lather belly-slide, exploding duck,
 * hypnotic swirl-eye gaze, bubble shield; enraged = pop storm + foam geysers.
 * Every tick index below matches the key poses in tools/bbgen/chars/mutant_bubble.py.
 */
public class MutantBubble extends FpeEntity {
    private static final DustParticleOptions FOAM = new DustParticleOptions(new Vector3f(0.97f, 0.97f, 1f), 1.6f);
    private static final DustParticleOptions PINK = new DustParticleOptions(new Vector3f(0.94f, 0.54f, 0.69f), 1.2f);
    private static final int FOAM_ARC = 0xC8F4F8FF;
    private boolean trapped, shielded;
    private Vec3 slideDir = Vec3.ZERO;
    private Vec3[] geysers = new Vec3[0];

    public MutantBubble(EntityType<? extends FpeEntity> type, Level level) { super(type, level); }

    @Override public Faction faction() { return Faction.MUTANT; }

    public static AttributeSupplier.Builder attributes() { return baseAttributes(80, 6, 0.33, 2, 0.2); }

    @Override public double preferredDistance() { return 3.0; }
    @Override protected int restTicks() { return isEnraged() ? 6 : 12; }

    @Override protected SoundEvent getAmbientSound() { return SoundEvents.BUBBLE_COLUMN_UPWARDS_AMBIENT; }
    @Override protected SoundEvent getHurtSound(DamageSource s) { return SoundEvents.SLIME_HURT_SMALL; }
    @Override protected SoundEvent getDeathSound() { return SoundEvents.BUBBLE_COLUMN_WHIRLPOOL_INSIDE; }
    @Override public float getVoicePitch() { return 1.5f; }

    /** bubble shield: incoming damage cut to 25 % while the shell is up */
    @Override
    public boolean hurt(DamageSource s, float amount) {
        if (shielded && !s.is(net.minecraft.tags.DamageTypeTags.BYPASSES_INVULNERABILITY)) {
            FpeUtil.particles(this, ParticleTypes.BUBBLE_POP, position().add(0, 0.7, 0), 8, 0.5, 0.5, 0.5, 0.05);
            FpeUtil.sound(this, SoundEvents.BUBBLE_COLUMN_BUBBLE_POP, 1f, 1.4f);
            amount *= 0.25f;
        }
        return super.hurt(s, amount);
    }

    // ------------------------------------------------------------------ helpers
    private void puff(ParticleOptions p, Vec3 at, int n, double spread) {
        FpeUtil.particles(this, p, at, n, spread, spread * 0.6, spread, 0.03);
    }

    private void foamBurst(Vec3 at, int n, double spread) {
        puff(FOAM, at, n, spread);
        puff(ParticleTypes.BUBBLE_POP, at, n / 2, spread);
        FpeUtil.particles(this, ParticleTypes.CLOUD, at, n / 3, spread, 0.1, spread, 0.02);
    }

    private void pop(float vol, float pitch) {
        FpeUtil.sound(this, SoundEvents.BUBBLE_COLUMN_BUBBLE_POP, vol, pitch);
    }

    private void arc(float radius, float sweep, float tilt, double y) {
        FpeFx f = FpeUtil.fx(this, FpeFx.Kind.ARC, position().add(0, y, 0), 0, 7, radius, 0).param(sweep).color(FOAM_ARC);
        f.setYRot(getYRot());
        f.setXRot(tilt);
    }

    private static void soak(LivingEntity v, int ticks, int amp) {
        v.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, ticks, amp));
    }

    private Vec3 mouth() { return FpeUtil.ahead(this, 0.45, 0.85); }

    private Vec3 hand() { return FpeUtil.ahead(this, 0.5, 0.75).add(FpeUtil.right(this).scale(-0.3)); }

    private void fan(Vec3 from, LivingEntity t, int n, double spreadDeg, double speed, float dmg) {
        Vec3 dir = FpeUtil.aim(from, t, speed, 0.3);
        for (int i = 0; i < n; i++) {
            double a = Math.toRadians((i - (n - 1) / 2.0) * spreadDeg);
            double c = Math.cos(a), s = Math.sin(a);
            FpeUtil.projectile(this, FpeProjectile.Kind.DIAMOND, from, new Vec3(dir.x * c - dir.z * s, dir.y + 0.03 * (i % 2), dir.x * s + dir.z * c), dmg);
        }
    }

    // ------------------------------------------------------------------ abilities
    @Override
    protected void registerAbilities(List<Ability> out) {
        // 1. Foam slap: right sleeve cocks back, slaps t8; left sleeve slaps t15 (soapy sleeves slow)
        out.add(Ability.of("foam_slap", 26, 30).range(0, 2.8).weight(5).tick((e, t, k) -> {
            MutantBubble b = (MutantBubble) e;
            if (k == 7 || k == 14) e.dashForward(0.2, 0);
            if (k == 8 || k == 15) {
                t.invulnerableTime = 0;
                FpeUtil.hitCone(e, 2.6, 75, e.dmg(0.8f), 0.5, 0.15);
                for (LivingEntity v : FpeUtil.enemiesInRadius(e, FpeUtil.ahead(e, 1.2, 0), 1.3, 2, 1)) soak(v, 30, 0);
                b.arc(1.8f, 140, k == 8 ? -15 : 15, 0.7);
                b.foamBurst(FpeUtil.ahead(e, 1.1, 0.8), 10, 0.3);
                FpeUtil.sound(e, SoundEvents.SLIME_ATTACK, 1f, 1.5f);
            }
        }));

        // 2. Bubble bonk: squashes down, hops t9-10, slams its big foam head down t12
        out.add(Ability.of("bubble_bonk", 28, 50).range(0, 3.6).weight(4).faceUntil(9).tick((e, t, k) -> {
            MutantBubble b = (MutantBubble) e;
            if (k == 4) FpeUtil.sound(e, SoundEvents.SLIME_SQUISH_SMALL, 1f, 1.2f);
            if (k == 9) e.dashToward(t.position(), Mth.clamp(e.distanceTo(t) * 0.18, 0.25, 0.6), 0.35);
            if (k == 12) {
                FpeUtil.hitRadius(e, FpeUtil.ahead(e, 0.9, 0), 1.6, e.dmg(1.3f), 0.6, 0.45);
                for (LivingEntity v : FpeUtil.enemiesInRadius(e, FpeUtil.ahead(e, 0.9, 0), 1.6, 2, 1))
                    v.addEffect(new MobEffectInstance(MobEffects.CONFUSION, 60, 0));
                b.foamBurst(FpeUtil.ahead(e, 0.9, 0.2), 18, 0.5);
                FpeUtil.sound(e, SoundEvents.SLIME_JUMP, 1.2f, 0.8f);
                FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_STRONG, 0.8f, 1.4f);
            }
        }));

        // 3. Soap spray: inhales (0-8), sprays a sweeping jet of soapy foam t10-26 (stinging eyes, slippery)
        out.add(Ability.of("soap_spray", 36, 60).range(0, 5.5).weight(4).faceUntil(10).tick((e, t, k) -> {
            MutantBubble b = (MutantBubble) e;
            if (k == 3) FpeUtil.sound(e, SoundEvents.GENERIC_DRINK, 1f, 1.6f);
            if (k >= 10 && k <= 26) {
                float sweep = (float) Math.sin((k - 10) * Math.PI / 8) * 28f;
                Vec3 dir = Vec3.directionFromRotation(0, e.getYRot() + sweep);
                for (int i = 1; i <= 4; i++) b.puff(FOAM, e.position().add(dir.scale(i * 1.1)).add(0, 0.8 - i * 0.08, 0), 3, 0.15);
                if (k % 2 == 0) b.puff(ParticleTypes.SPLASH, b.mouth().add(dir.scale(0.6)), 6, 0.1);
                if (k % 4 == 2) {
                    for (LivingEntity v : FpeUtil.enemiesInRadius(e, e.position(), 5, 2.5, 1)) {
                        Vec3 to = v.position().subtract(e.position());
                        Vec3 flat = new Vec3(to.x, 0, to.z).normalize();
                        if (flat.dot(dir) < 0.85) continue;
                        v.invulnerableTime = 0;
                        FpeUtil.hit(b, v, e.dmg(0.35f), 0.25, 0.05);
                        soak(v, 40, 1);
                        v.addEffect(new MobEffectInstance(MobEffects.BLINDNESS, 30, 0));
                    }
                    FpeUtil.sound(e, SoundEvents.BUBBLE_COLUMN_UPWARDS_INSIDE, 1f, 1.3f);
                }
            }
        }));

        // 4. Bubble volley: wand slides out of the sleeve, sweeping wave t14 blows a fan of hard bubbles
        out.add(Ability.of("bubble_volley", 30, 50).range(3, 14).weight(4).faceUntil(13).tick((e, t, k) -> {
            MutantBubble b = (MutantBubble) e;
            if (k == 4) FpeUtil.sound(e, SoundEvents.ARMOR_EQUIP_LEATHER, 1f, 1.5f);
            if (k == 14) {
                b.fan(b.hand(), t, e.isEnraged() ? 7 : 5, 11, 0.7, e.dmg(0.55f));
                b.puff(ParticleTypes.BUBBLE_POP, b.hand(), 14, 0.4);
                FpeUtil.sound(e, SoundEvents.BUBBLE_COLUMN_UPWARDS_AMBIENT, 1.5f, 1.6f);
            }
        }));

        // 5. Bubble trap: conjures (0-12), thrusts t14 -> target sealed in a bubble and floated 16-36, CLAP t38 pops it
        out.add(Ability.of("bubble_trap", 44, 110).range(2, 10).weight(3).faceUntil(14)
                .start((e, t, k) -> ((MutantBubble) e).trapped = false).tick((e, t, k) -> {
            MutantBubble b = (MutantBubble) e;
            if (k == 6) FpeUtil.sound(e, SoundEvents.AMETHYST_BLOCK_CHIME, 1f, 1.6f);
            if (k == 14) {
                b.trapped = e.distanceTo(t) < 10.5 && e.hasLineOfSight(t) && FpeUtil.canHurt(e, t);
                b.puff(ParticleTypes.BUBBLE_POP, t.position().add(0, t.getBbHeight() * 0.5, 0), 20, 0.6);
                FpeUtil.sound(e, SoundEvents.BUBBLE_COLUMN_WHIRLPOOL_INSIDE, 1.2f, 1.4f);
            }
            if (b.trapped && k > 14 && k < 38) {
                t.setDeltaMovement(t.getDeltaMovement().x * 0.4, Math.min(0.12, (k - 14) * 0.02), t.getDeltaMovement().z * 0.4);
                t.hurtMarked = true;
                t.fallDistance = 0;
                if (k % 3 == 0) FpeUtil.arc(e, ParticleTypes.BUBBLE_POP, t.position().add(0, t.getBbHeight() * 0.5, 0), 0, 180, 0.9, 12);
            }
            if (k == 38) {
                if (b.trapped) {
                    t.invulnerableTime = 0;
                    FpeUtil.hit(b, t, e.dmg(1.4f), 0, 0.2);
                    soak(t, 50, 1);
                    b.foamBurst(t.position().add(0, t.getBbHeight() * 0.5, 0), 24, 0.7);
                }
                b.pop(1.5f, 0.8f);
                FpeUtil.sound(e, SoundEvents.FIREWORK_ROCKET_BLAST, 0.6f, 1.6f);
            }
        }));

        // 6. Foam wave: sinks into its foam (0-10), heaves both sleeves t14 -> a rolling wall of suds surges forward 14-24
        out.add(Ability.of("foam_wave", 32, 70).range(0, 7).weight(3).faceUntil(13).tick((e, t, k) -> {
            MutantBubble b = (MutantBubble) e;
            if (k == 5) FpeUtil.sound(e, SoundEvents.BUBBLE_COLUMN_UPWARDS_INSIDE, 1.2f, 0.7f);
            if (k >= 14 && k <= 24 && k % 2 == 0) {
                double d = 1.0 + (k - 14) * 0.6;
                Vec3 c = FpeUtil.ahead(e, d, 0);
                Vec3 side = FpeUtil.right(e).scale(1.6);
                for (LivingEntity v : FpeUtil.enemiesInRadius(e, c, 1.5, 2, 1)) {
                    if (FpeUtil.hit(b, v, e.dmg(0.9f), 1.1, 0.35)) soak(v, 40, 1);
                }
                for (int i = -2; i <= 2; i++) b.foamBurst(c.add(side.scale(i * 0.5)).add(0, 0.4, 0), 4, 0.25);
                FpeUtil.sound(e, SoundEvents.GENERIC_SPLASH, 0.8f, 1.2f);
            }
        }));

        // 7. Lather slide: belly-flops t8 and toboggans forward on foam 8-18, bowling over anything in the way
        out.add(Ability.of("lather_slide", 30, 70).range(2.5, 9).weight(3).faceUntil(7).tick((e, t, k) -> {
            MutantBubble b = (MutantBubble) e;
            if (k == 8) {
                b.slideDir = FpeUtil.forward(e);
                FpeUtil.sound(e, SoundEvents.SLIME_SQUISH, 1.2f, 1.3f);
            }
            if (k >= 8 && k <= 18) {
                double sp = 0.75 - (k - 8) * 0.04;
                e.setDeltaMovement(b.slideDir.x * sp, e.getDeltaMovement().y, b.slideDir.z * sp);
                e.hurtMarked = true;
                b.puff(FOAM, e.position().add(0, 0.15, 0), 6, 0.3);
                if (k % 2 == 0) {
                    for (LivingEntity v : FpeUtil.enemiesInRadius(e, FpeUtil.ahead(e, 0.6, 0), 1.1, 1.5, 1)) {
                        if (FpeUtil.hit(b, v, e.dmg(1.0f), 0.9, 0.5)) soak(v, 40, 1);
                    }
                }
            }
            if (k == 20) e.setDeltaMovement(Vec3.ZERO);
        }));

        // 8. Duck toss: grabs the rubber duck off its head t6, winds up, throws t16 - it bounces and bursts into suds
        out.add(Ability.of("duck_toss", 30, 80).range(4, 13).weight(3).faceUntil(15).tick((e, t, k) -> {
            MutantBubble b = (MutantBubble) e;
            if (k == 6) FpeUtil.sound(e, SoundEvents.ITEM_PICKUP, 1f, 1.8f);
            if (k == 16) {
                Vec3 from = FpeUtil.ahead(e, 0.4, 1.3);
                Vec3 dir = FpeUtil.aim(from, t, 0.7, 0.3);
                FpeUtil.projectile(b, FpeProjectile.Kind.BOMBLET, from, dir.add(0, 0.25, 0), e.dmg(1.2f));
                FpeUtil.sound(e, SoundEvents.SNOWBALL_THROW, 1f, 1.5f);
                FpeUtil.sound(e, SoundEvents.CHICKEN_AMBIENT, 1f, 1.8f);
            }
            if (k == 26) b.puff(ParticleTypes.BUBBLE_POP, e.position().add(0, 1.3, 0), 6, 0.2);
        }));

        // 9. Swirl gaze: the pink swirl eye spins up (0-12), hypnotic stare t14-24 - nausea, slowness, drags the victim in
        out.add(Ability.of("swirl_gaze", 34, 90).range(2, 11).weight(2).tick((e, t, k) -> {
            MutantBubble b = (MutantBubble) e;
            if (k == 6) FpeUtil.sound(e, SoundEvents.AMETHYST_BLOCK_RESONATE, 1.2f, 1.6f);
            if (k >= 14 && k <= 24) {
                Vec3 eye = FpeUtil.ahead(e, 0.3, 0.95);
                Vec3 to = t.position().add(0, t.getBbHeight() * 0.6, 0);
                for (int i = 1; i <= 6; i++) b.puff(PINK, eye.lerp(to, i / 7.0), 1, 0.05);
                if (k % 5 == 4 && e.hasLineOfSight(t) && e.distanceTo(t) < 12) {
                    t.invulnerableTime = 0;
                    FpeUtil.hit(b, t, e.dmg(0.3f), 0, 0);
                    t.addEffect(new MobEffectInstance(MobEffects.CONFUSION, 120, 0));
                    soak(t, 50, 2);
                    Vec3 pull = e.position().subtract(t.position()).normalize().scale(0.25);
                    t.setDeltaMovement(t.getDeltaMovement().add(pull.x, 0.02, pull.z));
                    t.hurtMarked = true;
                    FpeUtil.sound(e, SoundEvents.AMETHYST_CLUSTER_HIT, 1f, 0.6f + (k - 14) * 0.05f);
                }
            }
        }));

        // 10. Bubble shield: curls up, shell blooms t8 (damage -75 % until t32), BURST t32 shoves everything away
        out.add(Ability.of("bubble_shield", 40, 160).range(0, 6).weight(2).blind()
                .start((e, t, k) -> ((MutantBubble) e).shielded = false)
                .end((e, t, k) -> ((MutantBubble) e).shielded = false).tick((e, t, k) -> {
            MutantBubble b = (MutantBubble) e;
            if (k == 8) {
                b.shielded = true;
                FpeUtil.sound(e, SoundEvents.BUBBLE_COLUMN_WHIRLPOOL_INSIDE, 1.2f, 1.2f);
            }
            if (b.shielded && k % 4 == 0) FpeUtil.arc(e, ParticleTypes.BUBBLE_POP, e.position().add(0, 0.6, 0), e.getYRot(), 180, 0.75, 10);
            if (k == 32) {
                b.shielded = false;
                FpeUtil.hitRadius(e, e.position(), 2.6, e.dmg(0.9f), 1.6, 0.4);
                FpeUtil.fx(e, FpeFx.Kind.RING_SHOCK, e.position().add(0, 0.1, 0), 0, 10, 3.5f, 0);
                b.foamBurst(e.position().add(0, 0.6, 0), 30, 0.9);
                b.pop(1.6f, 0.6f);
            }
        }));

        // 11. Pop storm (enraged): bubbles swell while it spins, three ever-wider bursts t16 / t24 / t32
        out.add(Ability.of("pop_storm", 44, 100).range(0, 6).weight(4).when(FpeEntity::isEnraged).blind().tick((e, t, k) -> {
            MutantBubble b = (MutantBubble) e;
            if (k == 4) FpeUtil.sound(e, SoundEvents.BUBBLE_COLUMN_WHIRLPOOL_AMBIENT, 1.5f, 1.2f);
            if (k < 16 && k % 3 == 0) FpeUtil.arc(e, ParticleTypes.BUBBLE, e.position().add(0, 1.0, 0), 0, 180, 1.2, 14);
            if (k == 16 || k == 24 || k == 32) {
                float r = 2.0f + (k - 16) * 0.12f;
                for (LivingEntity v : FpeUtil.enemiesInRadius(e, e.position(), r, 2.5, 1)) {
                    v.invulnerableTime = 0;
                    if (FpeUtil.hit(b, v, e.dmg(k == 32 ? 1.0f : 0.7f), 0.9, 0.3)) soak(v, 40, 1);
                }
                FpeUtil.fx(e, FpeFx.Kind.RING_SHOCK, e.position().add(0, 0.1, 0), 0, 8, r + 1, 0);
                for (int i = 0; i < 8; i++) {
                    double a = i * Math.PI / 4 + k;
                    b.foamBurst(e.position().add(Math.cos(a) * r * 0.7, 0.8, Math.sin(a) * r * 0.7), 5, 0.3);
                }
                b.pop(1.6f, 0.7f + (k - 16) * 0.03f);
            }
        }));

        // 12. Geyser burst (enraged): hops t10 marking foam rings under the foe, squats + heaves t22 -> soap geysers launch them
        out.add(Ability.of("geyser_burst", 40, 120).range(0, 12).weight(3).when(FpeEntity::isEnraged).faceUntil(10).tick((e, t, k) -> {
            MutantBubble b = (MutantBubble) e;
            if (k == 10) {
                Vec3 c = t.position();
                Vec3 f = FpeUtil.forward(e), r = FpeUtil.right(e);
                b.geysers = new Vec3[] { c, c.add(r.scale(2.2)), c.subtract(r.scale(2.2)), c.add(f.scale(2.2)) };
                for (Vec3 g : b.geysers) {
                    FpeUtil.fx(b, FpeFx.Kind.RING_TRAP, g.add(0, 0.05, 0), 12, 4, 1.3f, 0);
                    b.puff(FOAM, g.add(0, 0.1, 0), 10, 0.6);
                }
                FpeUtil.sound(e, SoundEvents.SLIME_JUMP, 1.2f, 1.2f);
            }
            if (k > 10 && k < 22 && k % 3 == 1) for (Vec3 g : b.geysers) b.puff(ParticleTypes.BUBBLE_POP, g.add(0, 0.1, 0), 4, 0.5);
            if (k == 22) {
                for (Vec3 g : b.geysers) {
                    for (LivingEntity v : FpeUtil.enemiesInRadius(e, g, 1.4, 3, 1)) {
                        v.invulnerableTime = 0;
                        if (FpeUtil.hit(b, v, e.dmg(1.3f), 0.2, 1.1)) soak(v, 60, 1);
                    }
                    for (int i = 0; i < 6; i++) b.foamBurst(g.add(0, i * 0.5, 0), 4, 0.3);
                    FpeUtil.particles(e, ParticleTypes.SPLASH, g.add(0, 1, 0), 30, 0.4, 1.2, 0.4, 0.2);
                }
                FpeUtil.sound(e, SoundEvents.GENERIC_SPLASH, 1.5f, 0.6f);
                b.pop(1.6f, 0.5f);
            }
        }));
    }
}
