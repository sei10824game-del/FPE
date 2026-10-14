package com.fpe.entity.characters;

import java.util.ArrayList;
import java.util.List;

import com.fpe.entity.Ability;
import com.fpe.entity.FpeEntity;
import com.fpe.entity.FpeFx;
import com.fpe.entity.FpeProjectile;
import com.fpe.entity.FpeUtil;

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

/**
 * Miss Bloomie – the alphabet teacher. Giant shard claw on her right arm, ABC blocks in her crown.
 * Every tick index below matches the key poses in client/spec/MissBloomieSpec.
 */
public class MissBloomie extends FpeEntity {
    /** letter-rain: points still to drop and blocks currently falling */
    private final List<Vec3> rainPoints = new ArrayList<>();
    private final List<FpeProjectile> falling = new ArrayList<>();
    private boolean grabbed;

    public MissBloomie(EntityType<? extends FpeEntity> type, Level level) { super(type, level); }

    @Override public Faction faction() { return Faction.MISS; }

    public static AttributeSupplier.Builder attributes() { return baseAttributes(130, 7, 0.29, 5, 0.35); }

    @Override public double preferredDistance() { return 1.6; }
    @Override protected int restTicks() { return isEnraged() ? 7 : 16; }

    // ------------------------------------------------------------------ positions
    /** world position of the giant claw (right hand) */
    static Vec3 claw(FpeEntity e, double fwd, double up) { return e.position().add(FpeUtil.forward(e).scale(fwd)).add(FpeUtil.right(e).scale(0.55)).add(0, up, 0); }
    /** world position of the small left hand */
    static Vec3 leftHand(FpeEntity e, double fwd, double up) { return e.position().add(FpeUtil.forward(e).scale(fwd)).add(FpeUtil.right(e).scale(-0.45)).add(0, up, 0); }

    static void slashArc(FpeEntity e, float radius, float sweep, float tilt, float yawOff, double y, int color) {
        FpeFx f = FpeUtil.fx(e, FpeFx.Kind.ARC, e.position().add(0, y, 0), 0, 7, radius, 0).param(sweep).color(color);
        f.setYRot(e.getYRot() + yawOff);
        f.setXRot(tilt);
    }

    static Vec3 rotY(Vec3 v, double deg) {
        double a = Math.toRadians(deg), c = Math.cos(a), s = Math.sin(a);
        return new Vec3(v.x * c - v.z * s, v.y, v.x * s + v.z * c);
    }

    static void throwBlock(FpeEntity e, Vec3 from, LivingEntity t, double speed, double yawSpread, double lift, float dmg) {
        Vec3 v = rotY(FpeUtil.aim(from, t, speed, 0.5), yawSpread).add(0, lift, 0);
        FpeUtil.projectile(e, FpeProjectile.Kind.ABC_BLOCK, from, v, dmg);
    }

    private void squeak(SoundEvent s, float vol, float pitch) { FpeUtil.sound(this, s, vol, pitch); }

    // ------------------------------------------------------------------ abilities
    @Override
    protected void registerAbilities(List<Ability> out) {
        // 1. ABC throw: plucks blocks from her crown, three with the left hand (t12), one hard hurl with the claw (t22)
        out.add(Ability.of("abc_throw", 32, 60).range(3, 16).weight(3).tick((e, t, tk) -> {
            if (tk == 5) FpeUtil.sound(e, SoundEvents.WOOD_HIT, 0.7f, 1.6f);
            if (tk == 12) {
                Vec3 from = leftHand(e, 0.5, 1.7);
                for (int i = -1; i <= 1; i++) throwBlock(e, from, t, 0.85, i * 14, 0.18, e.dmg(0.7f));
                FpeUtil.sound(e, SoundEvents.SNOWBALL_THROW, 1f, 0.7f);
            }
            if (tk == 22) {
                Vec3 from = claw(e, 0.8, 1.8);
                int n = e.isEnraged() ? 3 : 1;
                for (int i = 0; i < n; i++) throwBlock(e, from, t, 1.25, (i - (n - 1) / 2.0) * 10, 0.08, e.dmg(1.0f));
                FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_STRONG, 1f, 0.8f);
            }
        }));

        // 2. Letter rain: marks a pattern of glyphs around the target, then blocks crash down onto it
        out.add(Ability.of("letter_rain", 56, 170).range(3, 20).weight(2).blind().start((e, t, tk) -> {
            MissBloomie b = (MissBloomie) e;
            b.rainPoints.clear(); b.falling.clear();
            Vec3 c = t.position();
            b.rainPoints.add(c);
            double rot = e.getRandom().nextDouble() * 60;
            for (int i = 0; i < 6; i++) {
                b.rainPoints.add(c.add(rotY(new Vec3(2.4, 0, 0), rot + i * 60)));
                if (e.isEnraged()) b.rainPoints.add(c.add(rotY(new Vec3(4.4, 0, 0), rot + i * 60 + 30)));
            }
            FpeUtil.sound(e, SoundEvents.WITCH_CELEBRATE, 1.2f, 1.3f);
        }).tick((e, t, tk) -> {
            MissBloomie b = (MissBloomie) e;
            if (tk < 22 && tk % 3 == 0) for (Vec3 p : b.rainPoints) {
                FpeUtil.particles(e, ParticleTypes.ENCHANT, p.add(0, 0.2, 0), 6, 0.4, 0.1, 0.4, 0.4);
                FpeUtil.arc(e, ParticleTypes.WITCH, p.add(0, 0.1, 0), 0, 180, 0.9, 8);
            }
            // drops: centre at 22, ring points every 3 ticks (two per drop when enraged), last one on the target's CURRENT position
            if (tk >= 22 && tk <= 43 && (tk - 22) % 3 == 0 && !b.rainPoints.isEmpty()) {
                int n = e.isEnraged() && tk > 22 ? 2 : 1;
                for (int i = 0; i < n && !b.rainPoints.isEmpty(); i++) b.dropBlock(b.rainPoints.remove(0));
                FpeUtil.sound(e, SoundEvents.ITEM_FRAME_REMOVE_ITEM, 1f, 0.6f);
            }
            if (tk == 44) b.dropBlock(t.position());
            b.tickFalling();
        }).end((e, t, tk) -> ((MissBloomie) e).tickFalling()));

        // 3. Rake: three-hit claw combo (t9 forehand, t18 backhand, t30 overhead rake)
        out.add(Ability.of("rake", 40, 50).range(0, 3.6).weight(4).tick((e, t, tk) -> {
            if (tk == 7 || tk == 16) e.dashForward(0.32, 0);
            if (tk == 27) e.dashForward(0.45, 0.05);
            if (tk == 9 || tk == 18) {
                FpeUtil.hitCone(e, 3.2, 75, e.dmg(0.8f), 0.45, 0.15);
                slashArc(e, 2.6f, 150, tk == 9 ? 15 : -15, 0, 1.2, 0xE0302A3A);
                FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_SWEEP, 1f, tk == 9 ? 0.7f : 0.85f);
            }
            if (tk == 30) {
                FpeUtil.hitCone(e, 3.4, 50, e.dmg(1.25f), 0.9, 0.25);
                slashArc(e, 2.4f, 120, 75, 0, 1.0, 0xF0201C28);
                FpeUtil.particles(e, ParticleTypes.CRIT, FpeUtil.ahead(e, 1.8, 0.3), 14, 0.5, 0.2, 0.5, 0.25);
                FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_STRONG, 1f, 0.6f);
            }
        }));

        // 4. Claw smash: rears up (0-20), slams at t22 -> cone hit + shockwave (+ erupting shards when enraged)
        out.add(Ability.of("claw_smash", 44, 100).range(0, 5).weight(2).faceUntil(20).tick((e, t, tk) -> {
            if (tk == 6) FpeUtil.sound(e, SoundEvents.RAVAGER_ROAR, 0.7f, 1.6f);
            if (tk == 22) {
                Vec3 at = FpeUtil.ahead(e, 1.9, 0.05);
                FpeUtil.hitCone(e, 3.5, 60, e.dmg(1.6f), 1.0, 0.5);
                FpeUtil.fx(e, FpeFx.Kind.RING_SHOCK, at, 0, 14, 5.5f, e.dmg(0.7f)).color(0xC0302838);
                FpeUtil.particles(e, ParticleTypes.EXPLOSION, at, 2, 0.4, 0.1, 0.4, 0);
                FpeUtil.particles(e, ParticleTypes.LARGE_SMOKE, at, 16, 1.0, 0.2, 1.0, 0.04);
                FpeUtil.sound(e, SoundEvents.ANVIL_LAND, 1f, 0.5f);
                FpeUtil.sound(e, SoundEvents.GENERIC_EXPLODE, 0.8f, 0.8f);
                if (e.isEnraged()) for (int i = 0; i < 5; i++) {
                    Vec3 p = e.position().add(rotY(FpeUtil.forward(e), -40 + i * 20).scale(3.6 + (i % 2) * 0.8));
                    FpeUtil.fx(e, FpeFx.Kind.SPIKE, p, 6 + i, 34, 1.2f, e.dmg(0.9f)).param(1.2f);
                }
            }
        }));

        // 5. Scratch lunge: low crouch, explosive dash at t10, rising claw at t14
        out.add(Ability.of("scratch_lunge", 30, 80).range(3.5, 10).weight(2).faceUntil(10).tick((e, t, tk) -> {
            if (tk == 10) {
                e.dashToward(t.position(), Math.min(1.5, 0.35 + e.distanceTo(t) * 0.17), 0.22);
                FpeUtil.sound(e, SoundEvents.PHANTOM_SWOOP, 1f, 1.2f);
            }
            if (tk > 10 && tk < 17) FpeUtil.particles(e, ParticleTypes.SQUID_INK, e.position().add(0, 0.6, 0), 2, 0.2, 0.3, 0.2, 0.01);
            if (tk == 14) {
                FpeUtil.hitCone(e, 2.6, 60, e.dmg(1.2f), 0.7, 0.35);
                slashArc(e, 2.2f, 130, -45, 0, 1.1, 0xE0302A3A);
                FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_CRIT, 1f, 0.8f);
            }
        }));

        // 6. Shard throw: claw across body (0-12), backhand flick at t14 sheds a fan of black shards
        out.add(Ability.of("shard_throw", 34, 90).range(5, 16).weight(2).tick((e, t, tk) -> {
            if (tk == 14) {
                Vec3 from = claw(e, 0.6, 1.4);
                int n = e.isEnraged() ? 7 : 5;
                for (int i = 0; i < n; i++) {
                    Vec3 v = rotY(FpeUtil.aim(from, t, 1.35, 0.4), (i - (n - 1) / 2.0) * 9).add(0, 0.03, 0);
                    FpeUtil.projectile(e, FpeProjectile.Kind.KNIFE, from, v, e.dmg(0.6f));
                }
                FpeUtil.particles(e, ParticleTypes.SQUID_INK, from, 10, 0.3, 0.3, 0.3, 0.1);
                FpeUtil.sound(e, SoundEvents.TRIDENT_THROW, 1f, 0.7f);
            }
        }));

        // 7. Spelling test: writes in the air; rings spell out a word through the target, then burst letter by letter (t32..t44)
        out.add(Ability.of("spelling_test", 50, 200).range(2, 14).weight(2).blind().tick((e, t, tk) -> {
            if (tk == 8) {
                Vec3 c = t.position();
                Vec3 side = FpeUtil.right(e);
                float d = e.dmg(1.0f);
                FpeUtil.fx(e, FpeFx.Kind.RING_TRAP, c, 30, 36, 2.4f, d).color(0xFF8A70C8);
                int[] off = {-2, -1, 1, 2};
                for (int i = 0; i < off.length; i++)
                    FpeUtil.fx(e, FpeFx.Kind.RING_TRAP, c.add(side.scale(off[i] * 2.6)), 24 + i * 4, 30 + i * 4, 1.5f, d).color(0xFFE8E4F0);
                FpeUtil.sound(e, SoundEvents.BOOK_PAGE_TURN, 1.5f, 0.8f);
            }
            if (tk > 8 && tk < 32 && tk % 4 == 0) {
                FpeUtil.particles(e, ParticleTypes.ENCHANT, t.position().add(0, 0.3, 0), 12, 2.5, 0.2, 2.5, 0.6);
                FpeUtil.sound(e, SoundEvents.VILLAGER_WORK_CARTOGRAPHER, 0.8f, 1.4f);
            }
            if (tk == 38) FpeUtil.sound(e, SoundEvents.WITCH_CELEBRATE, 1.2f, 1.1f);
        }));

        // 8. Grab & rip: lunging grab (t10), lifts & squeezes the victim (t16/22/28), rips and flings at t36
        out.add(Ability.of("grab_rip", 52, 140).range(0, 3.2).weight(2).faceUntil(10).start((e, t, tk) -> ((MissBloomie) e).grabbed = false).tick((e, t, tk) -> {
            MissBloomie b = (MissBloomie) e;
            if (tk == 6) e.dashForward(0.4, 0);
            if (tk == 10) {
                Vec3 to = t.position().subtract(e.position());
                double ang = Math.toDegrees(Math.acos(Mth.clamp(new Vec3(to.x, 0, to.z).normalize().dot(FpeUtil.forward(e)), -1, 1)));
                b.grabbed = e.distanceTo(t) < 3.6 && ang < 60 && FpeUtil.canHurt(e, t);
                FpeUtil.sound(e, b.grabbed ? SoundEvents.PLAYER_ATTACK_KNOCKBACK : SoundEvents.PLAYER_ATTACK_NODAMAGE, 1f, 0.6f);
                if (b.grabbed) FpeUtil.hit(e, t, e.dmg(0.4f), 0, 0);
            }
            if (b.grabbed && tk > 10 && tk < 36) {
                Vec3 hold = claw(e, 1.5, 0.6 + Math.min(1.2, (tk - 10) * 0.08)).subtract(0, t.getBbHeight() * 0.4, 0);
                t.setDeltaMovement(hold.subtract(t.position()).scale(0.5));
                t.hurtMarked = true;
                t.fallDistance = 0;
                if (tk == 16 || tk == 22 || tk == 28) {
                    t.invulnerableTime = 0;
                    FpeUtil.hit(e, t, e.dmg(0.35f), 0, 0);
                    FpeUtil.particles(e, ParticleTypes.DAMAGE_INDICATOR, t.position().add(0, 1, 0), 4, 0.3, 0.3, 0.3, 0.1);
                    FpeUtil.sound(e, SoundEvents.PLAYER_HURT_SWEET_BERRY_BUSH, 1f, 0.7f);
                }
            }
            if (tk == 36) {
                if (b.grabbed) {
                    t.invulnerableTime = 0;
                    FpeUtil.hit(e, t, e.dmg(1.7f), 1.7, 0.6);
                    FpeUtil.particles(e, ParticleTypes.SWEEP_ATTACK, t.position().add(0, 1, 0), 3, 0.4, 0.4, 0.4, 0);
                } else FpeUtil.hitCone(e, 2.6, 60, e.dmg(0.9f), 0.8, 0.3);
                slashArc(e, 2.0f, 140, 30, 0, 1.2, 0xF0201C28);
                FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_STRONG, 1f, 0.5f);
                b.grabbed = false;
            }
        }).end((e, t, tk) -> ((MissBloomie) e).grabbed = false));

        // 9. Screech: inhales (0-10), shrieking cone t12 (knockback + slow), sound rings travel outward
        out.add(Ability.of("screech", 36, 120).range(0, 7).weight(2).tick((e, t, tk) -> {
            if (tk == 12) {
                FpeUtil.sound(e, SoundEvents.GHAST_SCREAM, 1.4f, 0.7f);
                FpeUtil.sound(e, SoundEvents.RAVAGER_ROAR, 1f, 1.5f);
                FpeUtil.hitCone(e, 7, 45, e.dmg(0.6f), 1.9, 0.45);
                for (LivingEntity v : FpeUtil.enemiesInRadius(e, e.position(), 7, 3, 1)) {
                    Vec3 d = v.position().subtract(e.position());
                    if (new Vec3(d.x, 0, d.z).normalize().dot(FpeUtil.forward(e)) > 0.7) {
                        v.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 70, 1));
                        v.addEffect(new MobEffectInstance(MobEffects.CONFUSION, 80, 0));
                    }
                }
            }
            if (tk >= 12 && tk <= 20 && tk % 2 == 0) {
                double dist = 1.3 + (tk - 12) * 0.75;
                FpeUtil.particles(e, ParticleTypes.SONIC_BOOM, FpeUtil.ahead(e, dist, 1.5), 1, 0, 0, 0, 0);
                FpeUtil.particles(e, ParticleTypes.NOTE, FpeUtil.ahead(e, dist, 1.6), 3, 0.8, 0.5, 0.8, 1);
            }
        }));

        // 10. ENRAGED – Alphabet barrage: rears up (0-14), then A..Z: one block every 2 ticks, alternating hands (t16..t66)
        out.add(Ability.of("alphabet_barrage", 80, 260).range(3, 20).weight(3).when(FpeEntity::isEnraged).tick((e, t, tk) -> {
            if (tk == 4) FpeUtil.sound(e, SoundEvents.WITCH_CELEBRATE, 1.5f, 0.8f);
            if (tk < 14 && tk % 2 == 0) FpeUtil.particles(e, ParticleTypes.ENCHANT, e.position().add(0, 2.4, 0), 10, 0.5, 0.3, 0.5, 1.0);
            if (tk >= 16 && tk <= 66 && tk % 2 == 0) {
                int letter = (tk - 16) / 2;
                boolean left = letter % 2 == 0;
                Vec3 from = left ? leftHand(e, 0.6, 1.7) : claw(e, 0.7, 1.7);
                double spread = (e.getRandom().nextDouble() - 0.5) * 26;
                throwBlock(e, from, t, 0.95 + e.getRandom().nextDouble() * 0.25, spread, 0.12 + e.getRandom().nextDouble() * 0.1, e.dmg(0.45f));
                FpeUtil.sound(e, SoundEvents.NOTE_BLOCK_XYLOPHONE.value(), 1f, 0.55f + letter * 0.055f);
            }
        }));
    }

    private void dropBlock(Vec3 p) {
        FpeProjectile b = FpeUtil.projectile(this, FpeProjectile.Kind.ABC_BLOCK, p.add(0, 9, 0), new Vec3(0, -0.85, 0), dmg(0.9f));
        falling.add(b);
        FpeUtil.particles(this, ParticleTypes.ENCHANT, p.add(0, 0.3, 0), 10, 0.5, 0.1, 0.5, 0.5);
    }

    /** rain blocks shatter on landing instead of bouncing */
    private void tickFalling() {
        falling.removeIf(b -> {
            if (b.isRemoved()) return true;
            if (b.getDeltaMovement().y > -0.05 || b.onGround() || b.ageTicks() > 40) {
                Vec3 p = b.position();
                FpeUtil.hitRadius(this, p, 1.7, dmg(0.9f), 0.6, 0.35);
                FpeUtil.particles(this, ParticleTypes.EXPLOSION, p, 1, 0, 0, 0, 0);
                FpeUtil.particles(this, ParticleTypes.ENCHANT, p, 16, 0.6, 0.4, 0.6, 0.8);
                squeak(SoundEvents.WOOD_BREAK, 1f, 0.8f);
                b.discard();
                return true;
            }
            return false;
        });
    }

    // ------------------------------------------------------------------ sounds
    @Override protected SoundEvent getAmbientSound() { return SoundEvents.WITCH_CELEBRATE; }
    @Override protected SoundEvent getHurtSound(DamageSource s) { return SoundEvents.WITCH_HURT; }
    @Override protected SoundEvent getDeathSound() { return SoundEvents.WITCH_DEATH; }
    @Override public int getAmbientSoundInterval() { return 220; }
}
