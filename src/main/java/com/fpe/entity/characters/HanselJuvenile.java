package com.fpe.entity.characters;

import java.util.HashSet;
import java.util.List;
import java.util.Set;

import com.fpe.entity.Ability;
import com.fpe.entity.FpeEntity;
import com.fpe.entity.FpeFx;
import com.fpe.entity.FpeProjectile;
import com.fpe.entity.FpeUtil;

import net.minecraft.core.particles.DustParticleOptions;
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
import org.joml.Vector3f;

/**
 * Lord Hansel, juvenile form (FPE Advanced Class, OUTSIDER): antlered forest boy with a flower crown and a leaf cloak.
 * Melee: antler_gore, thorn_claw. Mid: vine_lash (pull), pollen_cloud, leap_stomp, root_snare. Ranged: petal_storm, seed_volley.
 * Zone: thorn_spikes (thorn line), bramble_ring. Gap closer: antler_charge. Sustain: bloom_heal.
 * Enraged: verdant_wrath (three expanding thorn rings), thorn_cage (bursting ring trap + root tentacles).
 * Crowd control: vine_bind (vine grab, disarm, squeeze, slam -> stun + daze), stag_pin (antler pin, stomp, toss), dream_pollen (daze + drowsy stun).
 * Every tick index below matches the key poses in tools/bbgen/chars/hansel_juvenile.py.
 */
public class HanselJuvenile extends FpeEntity {
    private static final DustParticleOptions LEAF = new DustParticleOptions(new Vector3f(0.30f, 0.55f, 0.22f), 1.4f);
    private static final DustParticleOptions PETAL = new DustParticleOptions(new Vector3f(0.98f, 0.97f, 0.92f), 1.2f);
    private static final DustParticleOptions PINK = new DustParticleOptions(new Vector3f(0.92f, 0.56f, 0.64f), 1.1f);
    private static final DustParticleOptions POLLEN = new DustParticleOptions(new Vector3f(0.95f, 0.82f, 0.30f), 1.3f);
    private static final int LEAF_ARC = 0xC84E8A3A;
    private final Set<Integer> charged = new HashSet<>();
    /** victim of the current grab (vine_bind / stag_pin); null when nothing is held */
    private LivingEntity held;
    private Vec3 grabFrom = Vec3.ZERO;

    public HanselJuvenile(EntityType<? extends FpeEntity> type, Level level) { super(type, level); }

    @Override public Faction faction() { return Faction.OUTSIDER; }

    public static AttributeSupplier.Builder attributes() { return baseAttributes(90, 7, 0.32, 3, 0.3); }

    @Override public double preferredDistance() { return 3.0; }

    @Override protected SoundEvent getAmbientSound() { return SoundEvents.AZALEA_LEAVES_BREAK; }
    @Override protected SoundEvent getHurtSound(DamageSource s) { return SoundEvents.GOAT_HURT; }
    @Override protected SoundEvent getDeathSound() { return SoundEvents.GOAT_DEATH; }

    // ------------------------------------------------------------------ helpers
    private void bloom(Vec3 at, int n, double spread) {
        FpeUtil.particles(this, PETAL, at, n, spread, spread * 0.6, spread, 0.02);
        FpeUtil.particles(this, PINK, at, n / 3, spread, spread * 0.6, spread, 0.02);
        FpeUtil.particles(this, LEAF, at, n / 2, spread, spread * 0.6, spread, 0.02);
    }

    private Vec3 hand() { return FpeUtil.ahead(this, 0.6, 1.3).add(FpeUtil.right(this).scale(0.35)); }

    private void fan(Vec3 from, LivingEntity t, FpeProjectile.Kind kind, int n, double spreadDeg, double speed, float dmg) {
        Vec3 dir = FpeUtil.aim(from, t, speed, 0.3);
        for (int i = 0; i < n; i++) {
            double a = Math.toRadians((i - (n - 1) / 2.0) * spreadDeg);
            double c = Math.cos(a), s = Math.sin(a);
            FpeUtil.projectile(this, kind, from, new Vec3(dir.x * c - dir.z * s, dir.y, dir.x * s + dir.z * c), dmg);
        }
    }

    private void thornRing(Vec3 c, int n, double r, int warm, float dmg, float height, double phase) {
        for (int i = 0; i < n; i++) {
            double a = phase + i * Math.PI * 2 / n;
            FpeUtil.fx(this, FpeFx.Kind.SPIKE, c.add(Math.cos(a) * r, 0, Math.sin(a) * r), warm, 30, 1.2f, dmg).param(height);
        }
    }

    private void slash(float yawOff, float tilt, double radius) {
        FpeFx f = FpeUtil.fx(this, FpeFx.Kind.ARC, position().add(0, 1.1, 0), 0, 8, (float) radius, 0).param(150).color(LEAF_ARC);
        f.setYRot(getYRot() + yawOff);
        f.setXRot(tilt);
    }

    private void pull(LivingEntity v, double strength) {
        Vec3 d = position().subtract(v.position());
        Vec3 flat = new Vec3(d.x, 0, d.z);
        if (flat.lengthSqr() < 1.0) return;
        Vec3 n = flat.normalize().scale(Math.min(strength, flat.length() * 0.35));
        v.setDeltaMovement(n.x, 0.3, n.z);
        v.hurtMarked = true;
    }

    private boolean holding() {
        if (held != null && (!held.isAlive() || !FpeUtil.canHurt(this, held) || held.level() != level())) held = null;
        return held != null;
    }

    private static void release(FpeEntity e, LivingEntity t, int k) { ((HanselJuvenile) e).held = null; }

    /** nearest valid enemy within `range` whose direction is inside a forward cone of `halfDeg` */
    private LivingEntity nearestInCone(double range, double halfDeg) {
        Vec3 f = FpeUtil.forward(this);
        LivingEntity best = null;
        double bd = Double.MAX_VALUE;
        for (LivingEntity v : FpeUtil.enemiesInRadius(this, position(), range, 2, 1)) {
            Vec3 d = v.position().subtract(position()).multiply(1, 0, 1);
            double len = d.length();
            if (len > 0.3 && d.scale(1 / len).dot(f) < Math.cos(Math.toRadians(halfDeg))) continue;
            if (len < bd) { bd = len; best = v; }
        }
        return best;
    }

    /** nearest valid enemy whose body touches the segment from..to (vine reach) */
    private LivingEntity nearestOnLine(Vec3 from, Vec3 to, double width) {
        Vec3 d = to.subtract(from);
        LivingEntity best = null;
        double bu = 2;
        for (LivingEntity v : FpeUtil.enemiesInRadius(this, from.lerp(to, 0.5), d.length() * 0.5 + 1, 3, 3)) {
            Vec3 p = v.position().add(0, v.getBbHeight() * 0.5, 0);
            double u = Math.max(0, Math.min(1, p.subtract(from).dot(d) / d.lengthSqr()));
            if (from.add(d.scale(u)).distanceTo(p) < width + v.getBbWidth() * 0.5 + v.getBbHeight() * 0.25 && u < bu) { bu = u; best = v; }
        }
        return best;
    }

    // ------------------------------------------------------------------ abilities
    @Override
    protected void registerAbilities(List<Ability> out) {
        // 1. antler_gore: rears up, head drops, lunge t10, antlers gore t12 (launches up)
        out.add(Ability.of("antler_gore", 28, 30).range(0, 3.2).weight(5).faceUntil(9).tick((e, t, k) -> {
            if (k == 6) FpeUtil.sound(e, SoundEvents.GOAT_SCREAMING_PREPARE_RAM, 0.9f, 1.3f);
            if (k == 10) e.dashForward(0.5, 0);
            if (k == 12) {
                FpeUtil.hitCone(e, 3.2, 55, e.dmg(1.3f), 1.0, 0.45);
                FpeUtil.sound(e, SoundEvents.GOAT_RAM_IMPACT, 1f, 1.2f);
                FpeUtil.particles(e, LEAF, FpeUtil.ahead(e, 1.6, 1.4), 10, 0.4, 0.3, 0.4, 0.05);
            }
        }));
        // 2. thorn_claw: two thorny claw rakes t9 (right) and t18 (left)
        out.add(Ability.of("thorn_claw", 30, 30).range(0, 3.0).weight(5).faceUntil(16).tick((e, t, k) -> {
            HanselJuvenile h = (HanselJuvenile) e;
            if (k == 8 || k == 17) FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_SWEEP, 0.8f, 1.4f);
            if (k == 9) { e.dashForward(0.25, 0); FpeUtil.hitCone(e, 3.0, 100, e.dmg(1.0f), 0.4, 0.15); h.slash(0, -25, 2.6); }
            if (k == 18) {
                e.dashForward(0.25, 0);
                for (LivingEntity v : FpeUtil.enemiesInRadius(e, FpeUtil.ahead(e, 1.4, 0), 2.0, 2, 1)) {
                    if (FpeUtil.hit(h, v, e.dmg(1.1f), 0.6, 0.2)) v.addEffect(new MobEffectInstance(MobEffects.POISON, 40, 0));
                }
                h.slash(0, 25, 2.8);
            }
        }));
        // 3. vine_lash: thorn vine grows from the hand, whips forward t14 along a line, drags the victim in + slows
        out.add(Ability.of("vine_lash", 32, 50).range(2.5, 8).weight(4).faceUntil(12).tick((e, t, k) -> {
            HanselJuvenile h = (HanselJuvenile) e;
            if (k == 4) FpeUtil.sound(e, SoundEvents.CAVE_VINES_PLACE, 1f, 0.8f);
            if (k == 13) FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_SWEEP, 1f, 0.7f);
            if (k == 14) {
                Vec3 from = h.hand(), to = from.add(FpeUtil.forward(e).scale(7.5));
                for (int i = 0; i <= 12; i++) FpeUtil.particles(e, LEAF, from.lerp(to, i / 12.0), 2, 0.1, 0.1, 0.1, 0);
                for (LivingEntity v : FpeUtil.enemiesInRadius(e, from.lerp(to, 0.5), 4.2, 2, 2)) {
                    Vec3 p = v.position().add(0, v.getBbHeight() * 0.5, 0);
                    Vec3 d = to.subtract(from);
                    double u = Math.max(0, Math.min(1, p.subtract(from).dot(d) / d.lengthSqr()));
                    if (from.add(d.scale(u)).distanceTo(p) < 1.0 + v.getBbWidth() * 0.5 && FpeUtil.hit(h, v, e.dmg(1.2f), 0, 0)) {
                        v.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 50, 1));
                        h.pull(v, 1.2);
                    }
                }
            }
        }));
        // 4. petal_storm: cloak opens, three twirling volleys of razor petals t14 / t20 / t26
        out.add(Ability.of("petal_storm", 36, 70).range(5, 16).weight(3).tick((e, t, k) -> {
            HanselJuvenile h = (HanselJuvenile) e;
            if (k == 8) FpeUtil.sound(e, SoundEvents.CHERRY_LEAVES_BREAK, 1f, 0.9f);
            if (k == 14 || k == 20 || k == 26) {
                Vec3 from = e.position().add(0, 1.3, 0).add(FpeUtil.forward(e).scale(0.6));
                h.fan(from, t, FpeProjectile.Kind.DIAMOND, k == 20 ? 4 : 3, 12, 1.0, e.dmg(0.55f));
                h.bloom(from, 12, 0.6);
                FpeUtil.sound(e, SoundEvents.CHERRY_LEAVES_PLACE, 1f, 1.3f);
            }
        }));
        // 5. thorn_spikes: bare-foot stomp t14 -> a line of thorns races toward the target
        out.add(Ability.of("thorn_spikes", 34, 70).range(3, 12).weight(3).faceUntil(12).tick((e, t, k) -> {
            if (k == 14) {
                FpeUtil.sound(e, SoundEvents.ROOTED_DIRT_BREAK, 1.2f, 0.7f);
                Vec3 dir = t.position().subtract(e.position()).multiply(1, 0, 1).normalize();
                for (int i = 0; i < 7; i++)
                    FpeUtil.fx(e, FpeFx.Kind.SPIKE, e.position().add(dir.scale(1.6 + i * 1.5)), 2 + i * 2, 26, 1.2f, e.dmg(1.1f)).param(0.8f + i * 0.08f);
                FpeUtil.particles(e, ParticleTypes.COMPOSTER, e.position().add(0, 0.1, 0), 14, 0.8, 0.1, 0.8, 0.02);
            }
        }));
        // 6. root_snare: kneels, palm into the soil t14 -> grasping roots erupt under the target (warns, then holds)
        out.add(Ability.of("root_snare", 40, 90).range(4, 12).weight(2).blind().tick((e, t, k) -> {
            HanselJuvenile h = (HanselJuvenile) e;
            if (k == 14) {
                FpeUtil.sound(e, SoundEvents.HANGING_ROOTS_BREAK, 1.2f, 0.6f);
                FpeUtil.particles(e, ParticleTypes.COMPOSTER, h.hand().add(0, -1.1, 0), 10, 0.3, 0.1, 0.3, 0.02);
                FpeUtil.fx(e, FpeFx.Kind.TENTACLE, t.position(), 8, 40, 1.4f, e.dmg(0.9f));
                for (int i = 0; i < 3; i++) {
                    double a = i * Math.PI * 2 / 3;
                    FpeUtil.fx(e, FpeFx.Kind.SPIKE, t.position().add(Math.cos(a) * 1.8, 0, Math.sin(a) * 1.8), 12, 28, 1.0f, e.dmg(0.7f)).param(0.7f);
                }
            }
        }));
        // 7. antler_charge: head-down stag charge t10-24, gores everything in the path once, skids
        out.add(Ability.of("antler_charge", 40, 100).range(5, 14).weight(3).faceUntil(10).start((e, t, k) -> ((HanselJuvenile) e).charged.clear()).tick((e, t, k) -> {
            HanselJuvenile h = (HanselJuvenile) e;
            if (k == 2 || k == 6) FpeUtil.particles(e, ParticleTypes.COMPOSTER, e.position(), 6, 0.3, 0.05, 0.3, 0.02);
            if (k == 8) FpeUtil.sound(e, SoundEvents.GOAT_LONG_JUMP, 1f, 1.2f);
            if (k >= 10 && k <= 24) {
                e.dashForward(0.75, 0);
                FpeUtil.particles(e, LEAF, e.position().add(0, 0.3, 0), 3, 0.3, 0.1, 0.3, 0.02);
                for (LivingEntity v : FpeUtil.enemiesInRadius(e, FpeUtil.ahead(e, 0.9, 0), 1.5, 2, 1)) {
                    if (h.charged.add(v.getId()) && FpeUtil.hit(h, v, e.dmg(1.5f), 1.4, 0.5)) FpeUtil.sound(e, SoundEvents.GOAT_RAM_IMPACT, 1f, 1f);
                }
            }
            if (k == 25) e.setDeltaMovement(e.getDeltaMovement().scale(0.2));
        }));
        // 8. bramble_ring: crouch, explosive spin t12-18 -> ring of thorns + shockwave at t16
        out.add(Ability.of("bramble_ring", 38, 80).range(0, 5).weight(3).tick((e, t, k) -> {
            HanselJuvenile h = (HanselJuvenile) e;
            if (k == 12) FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_SWEEP, 1f, 0.6f);
            if (k == 16) {
                h.thornRing(e.position(), 8, 2.2, 0, e.dmg(1.1f), 0.9f, 0);
                FpeUtil.fx(e, FpeFx.Kind.RING_SHOCK, e.position().add(0, 0.1, 0), 0, 12, 5f, e.dmg(0.6f));
                FpeUtil.hitRadius(e, e.position(), 2.6, e.dmg(0.8f), 1.0, 0.4);
                FpeUtil.arc(e, LEAF, e.position().add(0, 0.9, 0), e.getYRot(), 180, 2.2, 24);
                FpeUtil.sound(e, SoundEvents.SWEET_BERRY_BUSH_BREAK, 1.2f, 0.8f);
            }
        }));
        // 9. seed_volley: underhand lob of three exploding seed pods t12
        out.add(Ability.of("seed_volley", 32, 70).range(6, 18).weight(3).tick((e, t, k) -> {
            if (k == 12) {
                Vec3 from = e.position().add(0, 1.4, 0).add(FpeUtil.forward(e).scale(0.5));
                double dist = Math.min(16, e.distanceTo(t));
                for (int i = -1; i <= 1; i++) {
                    Vec3 aim = t.position().add(FpeUtil.right(e).scale(i * 1.6)).subtract(from);
                    Vec3 flat = new Vec3(aim.x, 0, aim.z).normalize().scale(0.35 + dist * 0.045);
                    FpeUtil.projectile((FpeEntity) e, FpeProjectile.Kind.BOMBLET, from, new Vec3(flat.x, 0.45 + dist * 0.012, flat.z), e.dmg(0.9f));
                }
                FpeUtil.sound(e, SoundEvents.BIG_DRIPLEAF_TILT_DOWN, 1f, 1.2f);
            }
        }));
        // 10. pollen_cloud: deep breath, blows a choking pollen cone t14-22 (hit t16: poison + slow)
        out.add(Ability.of("pollen_cloud", 34, 80).range(0, 6).weight(2).faceUntil(16).tick((e, t, k) -> {
            if (k == 8) FpeUtil.sound(e, SoundEvents.SPORE_BLOSSOM_BREAK, 1f, 0.6f);
            if (k >= 14 && k <= 22) {
                Vec3 f = FpeUtil.forward(e);
                for (int i = 1; i <= 5; i++) FpeUtil.particles(e, POLLEN, e.position().add(0, 1.4 - i * 0.12, 0).add(f.scale(i)), 3 + i, 0.2 * i, 0.15 * i, 0.2 * i, 0.01);
                if (k % 3 == 0) FpeUtil.particles(e, ParticleTypes.SPORE_BLOSSOM_AIR, FpeUtil.ahead(e, 3, 1), 10, 1.2, 0.6, 1.2, 0);
            }
            if (k == 16) {
                for (LivingEntity v : FpeUtil.enemiesInRadius(e, e.position(), 5.5, 2, 1)) {
                    Vec3 d = v.position().subtract(e.position()).multiply(1, 0, 1).normalize();
                    if (d.dot(FpeUtil.forward(e)) > Math.cos(Math.toRadians(40)) && FpeUtil.hit((FpeEntity) e, v, e.dmg(0.6f), 0.2, 0)) {
                        v.addEffect(new MobEffectInstance(MobEffects.POISON, 80, 1));
                        v.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 60, 0));
                    }
                }
            }
        }));
        // 11. bloom_heal: kneels, the flower crown blooms t20 (heal + regen, petal burst knocks enemies back)
        out.add(Ability.of("bloom_heal", 44, 240).range(0, 16).weight(2).blind().when(e -> e.getHealth() < e.getMaxHealth() * 0.7f).tick((e, t, k) -> {
            HanselJuvenile h = (HanselJuvenile) e;
            if (k == 10) FpeUtil.sound(e, SoundEvents.AMETHYST_BLOCK_CHIME, 1f, 0.8f);
            if (k > 10 && k < 20 && k % 3 == 0) FpeUtil.particles(e, ParticleTypes.HAPPY_VILLAGER, e.position().add(0, 1.4, 0), 4, 0.6, 0.4, 0.6, 0);
            if (k == 20) {
                e.heal(e.getMaxHealth() * 0.12f);
                e.addEffect(new MobEffectInstance(MobEffects.REGENERATION, 80, 0));
                h.bloom(e.position().add(0, 1.8, 0), 40, 1.6);
                FpeUtil.hitRadius(e, e.position(), 3.0, e.dmg(0.4f), 1.2, 0.3);
                FpeUtil.sound(e, SoundEvents.CHERRY_LEAVES_PLACE, 1.2f, 0.7f);
            }
        }));
        // 12. leap_stomp: deer leap t8, crashes down t20 with a shockwave
        out.add(Ability.of("leap_stomp", 40, 80).range(3, 9).weight(3).faceUntil(8).tick((e, t, k) -> {
            if (k == 8) {
                Vec3 to = t.position().subtract(e.position());
                e.dashToward(e.position().add(to.scale(Math.max(0, (to.length() - 1.2) / Math.max(0.1, to.length())))), 0.11 * Math.min(9, to.length()) / 1.1, 0.65);
                FpeUtil.sound(e, SoundEvents.GOAT_LONG_JUMP, 1f, 1f);
            }
            if (k == 20) {
                FpeUtil.hitRadius(e, e.position(), 3.0, e.dmg(1.4f), 0.9, 0.5);
                FpeUtil.fx(e, FpeFx.Kind.RING_SHOCK, e.position().add(0, 0.1, 0), 0, 12, 4.5f, e.dmg(0.5f));
                FpeUtil.particles(e, ParticleTypes.COMPOSTER, e.position(), 20, 1.2, 0.1, 1.2, 0.05);
                FpeUtil.sound(e, SoundEvents.GOAT_RAM_IMPACT, 1.2f, 0.7f);
            }
        }));
        // 13. verdant_wrath (enraged): arms to the sky, three palm slams t18 / t28 / t38 -> expanding thorn rings, petal storm at the end
        out.add(Ability.of("verdant_wrath", 52, 160).range(0, 9).weight(4).when(FpeEntity::isEnraged).tick((e, t, k) -> {
            HanselJuvenile h = (HanselJuvenile) e;
            if (k == 6) FpeUtil.sound(e, SoundEvents.AMETHYST_BLOCK_RESONATE, 1.4f, 0.5f);
            if (k < 16 && k % 2 == 0) h.bloom(e.position().add(0, 2.2, 0), 4, 0.8);
            if (k == 18) h.thornRing(e.position(), 8, 2.5, 0, e.dmg(1.0f), 0.9f, 0);
            if (k == 28) h.thornRing(e.position(), 12, 5.0, 0, e.dmg(1.0f), 1.1f, 0.26);
            if (k == 38) {
                h.thornRing(e.position(), 16, 7.5, 0, e.dmg(1.0f), 1.3f, 0.1);
                for (int i = 0; i < 8; i++) {
                    double a = i * Math.PI / 4;
                    FpeUtil.projectile(h, FpeProjectile.Kind.DIAMOND, e.position().add(0, 1.4, 0), new Vec3(Math.cos(a) * 0.8, 0.05, Math.sin(a) * 0.8), e.dmg(0.5f));
                }
                h.bloom(e.position().add(0, 1.4, 0), 30, 2.0);
            }
            if (k == 18 || k == 28 || k == 38) {
                FpeUtil.fx(e, FpeFx.Kind.RING_SHOCK, e.position().add(0, 0.1, 0), 0, 10, 2.5f + (k - 18) * 0.25f, 0);
                FpeUtil.sound(e, SoundEvents.ROOTED_DIRT_BREAK, 1.4f, 0.6f);
            }
        }));
        // 14. thorn_cage (enraged): points t10-12 -> thorn circle drawn round the target + root tentacles, fist clench t30 bursts it
        out.add(Ability.of("thorn_cage", 46, 140).range(3, 14).weight(3).when(FpeEntity::isEnraged).faceUntil(12).tick((e, t, k) -> {
            HanselJuvenile h = (HanselJuvenile) e;
            if (k == 12) {
                Vec3 c = t.position();
                FpeUtil.fx(h, FpeFx.Kind.RING_TRAP, c, 18, 22, 3.0f, e.dmg(1.6f));
                for (int i = 0; i < 4; i++) {
                    double a = i * Math.PI / 2 + Math.PI / 4;
                    FpeUtil.fx(h, FpeFx.Kind.TENTACLE, c.add(Math.cos(a) * 2.6, 0, Math.sin(a) * 2.6), 6, 34, 1.2f, e.dmg(0.6f));
                }
                FpeUtil.sound(e, SoundEvents.CAVE_VINES_PLACE, 1.4f, 0.6f);
            }
            if (k == 30) FpeUtil.sound(e, SoundEvents.SWEET_BERRY_BUSH_BREAK, 1.4f, 0.6f);
        }));
        // 15. vine_bind (GRAB): vine cast t10 snags the first enemy on the line (disarms it), reels it in t11-19,
        //     holds it dangling in front t20-37 with squeezes t24 / t30 (root), overhead SLAM t38 (stun + daze)
        out.add(Ability.of("vine_bind", 48, 170).range(2.5, 8).weight(2).faceUntil(10)
                .start(HanselJuvenile::release).end(HanselJuvenile::release).tick((e, t, k) -> {
            HanselJuvenile h = (HanselJuvenile) e;
            if (k == 4) FpeUtil.sound(e, SoundEvents.CAVE_VINES_PLACE, 1.2f, 0.7f);
            if (k == 9) FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_SWEEP, 1f, 0.6f);
            if (k == 10) {
                Vec3 from = h.hand(), to = from.add(FpeUtil.forward(e).scale(8));
                LivingEntity v = h.nearestOnLine(from, to, 0.9);
                Vec3 end = v == null ? to : v.position().add(0, v.getBbHeight() * 0.5, 0);
                for (int i = 0; i <= 12; i++) FpeUtil.particles(e, LEAF, from.lerp(end, i / 12.0), 2, 0.08, 0.08, 0.08, 0);
                if (v != null && FpeUtil.hit(h, v, e.dmg(0.5f), 0, 0)) {
                    h.held = v;
                    h.grabFrom = v.position();
                    FpeUtil.disarm(v);
                    FpeUtil.sound(e, SoundEvents.CAVE_VINES_PICK_BERRIES, 1.2f, 0.6f);
                }
            }
            if (k > 10 && k < 38 && h.holding()) {
                Vec3 hold = e.position().add(FpeUtil.forward(e).scale(1.7)).add(FpeUtil.right(e).scale(0.35)).add(0, 1.2 + 0.08 * Math.sin(k * 0.8), 0);
                FpeUtil.holdAt(h.held, k < 20 ? h.grabFrom.lerp(hold, (k - 10) / 10.0) : hold);
                if (k % 3 == 0) FpeUtil.particles(e, LEAF, h.held.position().add(0, h.held.getBbHeight() * 0.5, 0), 3, 0.3, 0.4, 0.3, 0);
                if (k == 24 || k == 30) {
                    h.held.invulnerableTime = 0;
                    FpeUtil.hit(h, h.held, e.dmg(0.5f), 0, 0);
                    FpeUtil.root(h.held, 40);
                    FpeUtil.particles(e, ParticleTypes.CRIT, h.held.position().add(0, h.held.getBbHeight() * 0.5, 0), 8, 0.3, 0.4, 0.3, 0.1);
                    FpeUtil.sound(e, SoundEvents.SWEET_BERRY_BUSH_BREAK, 1f, 0.8f + k * 0.01f);
                }
            }
            if (k == 38 && h.holding()) {
                LivingEntity v = h.held;
                FpeUtil.hold(e, v, 1.9, 0, 0.3);
                v.invulnerableTime = 0;
                FpeUtil.hit(h, v, e.dmg(1.2f), 0, 0);
                FpeUtil.stun(v, 30);
                FpeUtil.daze(v, 60);
                FpeUtil.fx(h, FpeFx.Kind.RING_SHOCK, v.position().add(0, 0.1, 0), 0, 10, 2.0f, 0);
                FpeUtil.particles(e, ParticleTypes.COMPOSTER, v.position(), 16, 0.7, 0.1, 0.7, 0.05);
                FpeUtil.sound(e, SoundEvents.ROOTED_DIRT_BREAK, 1.4f, 0.6f);
                h.held = null;
            }
        }));
        // 16. stag_pin (GRAB): lunge t10 catches the nearest enemy on the antlers, drives it back t11-22,
        //     rams it into the ground t24 (pin + stun), bare-foot stomp t30, antler toss t36 (fling up)
        out.add(Ability.of("stag_pin", 44, 150).range(0, 3.4).weight(2).faceUntil(10)
                .start(HanselJuvenile::release).end(HanselJuvenile::release).tick((e, t, k) -> {
            HanselJuvenile h = (HanselJuvenile) e;
            if (k == 5) FpeUtil.sound(e, SoundEvents.GOAT_SCREAMING_PREPARE_RAM, 1f, 1.2f);
            if (k == 10) {
                e.dashForward(0.45, 0);
                LivingEntity v = h.nearestInCone(3.2, 50);
                if (v != null && FpeUtil.hit(h, v, e.dmg(0.8f), 0, 0)) {
                    h.held = v;
                    FpeUtil.sound(e, SoundEvents.GOAT_RAM_IMPACT, 1f, 1.1f);
                }
            }
            if (k > 10 && k < 36 && h.holding()) {
                if (k <= 22) {
                    e.dashForward(0.32, 0);
                    FpeUtil.hold(e, h.held, 1.25, 0.45, 0);
                    if (k % 2 == 0) FpeUtil.particles(e, ParticleTypes.COMPOSTER, e.position(), 3, 0.3, 0.05, 0.3, 0.02);
                } else FpeUtil.hold(e, h.held, 1.45, 0, 0);
                if (k == 24) {
                    h.held.invulnerableTime = 0;
                    FpeUtil.hit(h, h.held, e.dmg(0.6f), 0, 0);
                    FpeUtil.stun(h.held, 30);
                    FpeUtil.particles(e, ParticleTypes.COMPOSTER, h.held.position(), 14, 0.6, 0.1, 0.6, 0.05);
                    FpeUtil.sound(e, SoundEvents.ROOTED_DIRT_BREAK, 1.2f, 0.8f);
                }
                if (k == 30) {
                    h.held.invulnerableTime = 0;
                    FpeUtil.hit(h, h.held, e.dmg(1.0f), 0, 0);
                    FpeUtil.particles(e, LEAF, h.held.position().add(0, 0.3, 0), 10, 0.4, 0.2, 0.4, 0.05);
                    FpeUtil.sound(e, SoundEvents.GOAT_RAM_IMPACT, 1.1f, 0.7f);
                }
            }
            if (k == 36 && h.holding()) {
                LivingEntity v = h.held;
                v.invulnerableTime = 0;
                FpeUtil.hit(h, v, e.dmg(0.5f), 0, 0);
                FpeUtil.fling(v, FpeUtil.forward(e), 0.7, 0.85);
                FpeUtil.sound(e, SoundEvents.GOAT_LONG_JUMP, 1f, 1.3f);
                h.held = null;
            }
        }));
        // 17. dream_pollen (DAZE): crown blooms 4-12, golden pollen gathered on the left palm, BLOWN t16 across a cone
        //     -> daze (nausea + blindness) and a drowsy stun; drifting pollen t16-26
        out.add(Ability.of("dream_pollen", 40, 160).range(0, 6.5).weight(2).faceUntil(16).tick((e, t, k) -> {
            HanselJuvenile h = (HanselJuvenile) e;
            if (k == 4) FpeUtil.sound(e, SoundEvents.AMETHYST_BLOCK_CHIME, 1f, 1.4f);
            if (k > 4 && k < 15 && k % 2 == 0) {
                FpeUtil.particles(e, POLLEN, e.position().add(0, 2.3, 0), 3, 0.4, 0.1, 0.4, 0.01);
                FpeUtil.particles(e, POLLEN, FpeUtil.ahead(e, 0.6, 1.5).add(FpeUtil.right(e).scale(-0.3)), 2, 0.08, 0.08, 0.08, 0);
            }
            if (k == 15) FpeUtil.sound(e, SoundEvents.SPORE_BLOSSOM_BREAK, 1.2f, 1.5f);
            if (k >= 16 && k <= 26) {
                Vec3 f = FpeUtil.forward(e);
                for (int i = 1; i <= 6; i++) FpeUtil.particles(e, POLLEN, e.position().add(0, 1.5 - i * 0.08, 0).add(f.scale(i)), 2 + i / 2, 0.15 * i, 0.12 * i, 0.15 * i, 0.01);
                if (k % 4 == 0) FpeUtil.particles(e, ParticleTypes.END_ROD, FpeUtil.ahead(e, 3.5, 1.2), 4, 1.2, 0.5, 1.2, 0.01);
            }
            if (k == 16) {
                for (LivingEntity v : FpeUtil.enemiesInRadius(e, e.position(), 6.5, 2, 1)) {
                    Vec3 d = v.position().subtract(e.position()).multiply(1, 0, 1);
                    if (d.lengthSqr() > 0.01 && d.normalize().dot(FpeUtil.forward(e)) < Math.cos(Math.toRadians(45))) continue;
                    if (FpeUtil.hit(h, v, e.dmg(0.3f), 0, 0)) {
                        FpeUtil.daze(v, 90);
                        FpeUtil.stun(v, 25);
                        FpeUtil.particles(e, ParticleTypes.NOTE, v.position().add(0, v.getBbHeight() + 0.3, 0), 3, 0.3, 0.1, 0.3, 0);
                    }
                }
            }
        }));
    }
}
