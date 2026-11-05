package com.fpe.entity.characters;

import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.UUID;

import com.fpe.entity.Ability;
import com.fpe.entity.FpeCombat;
import com.fpe.entity.FpeEntity;
import com.fpe.entity.FpeFx;
import com.fpe.entity.FpeProjectile;
import com.fpe.entity.FpeUtil;

import net.minecraft.core.BlockPos;
import net.minecraft.core.particles.ParticleOptions;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.tags.DamageTypeTags;
import net.minecraft.world.BossEvent;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.EntityDimensions;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.Pose;
import net.minecraft.world.entity.ai.attributes.AttributeInstance;
import net.minecraft.world.entity.ai.attributes.AttributeModifier;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.Vec3;

/**
 * Danger AU Alice (docs/ref/confirmed/danger_alice_phase1.jpg / danger_alice_phase2.jpg).
 * Variant 0: scruffy girl - messy brown hair + ahoge, spiky black crown, eyes hidden under the bangs, grey patched cape,
 * triangle pendant, ragged black patched skirt, bandaged arms/legs, black sandals with an ankle ring, six black spikes on her back.
 * At 50 % hp she is forced into "reveal" (invulnerable) and becomes variant 1 (model danger_alice_boss): a 5-block pitch-black
 * monster with red eyes, a white grin, four insect wings, two arching back horns, very long arms ending in huge claws, tentacles
 * and black spikes erupting from the ground. Phase 2 also has a QUADRUPED stance (stance 1): she drops onto her claws ("drop_down")
 * when the target is far, when enraged or every ~200-400 ticks, skitters much faster with her back tentacles streaming behind like
 * tails, uses the quad_* attacks and rears back up ("rise_up") when close or after a while. Ticks match tools/bbgen/chars/danger_alice.py.
 */
public class DangerAlice extends FpeEntity {
    /** reveal timeline: variant flips at T_FLIP (boss model plays the rest: unfurl + roar at T_ROAR) */
    public static final int T_FLIP = 50, T_ROAR = 62, T_END = 80;
    private int revealT;
    private boolean holding, flag;
    /** ticks spent in the current stance and when to switch again (server only) */
    private int stanceT, nextSwap = 300;
    private final Set<Integer> hitIds = new HashSet<>();
    private static final UUID QUAD_SPEED = UUID.fromString("5b1e7c42-9d3a-4f60-8e21-da11ce0d4a02");

    public DangerAlice(EntityType<? extends FpeEntity> type, Level level) { super(type, level); }

    @Override public Faction faction() { return Faction.DANGER_ALICE; }

    public static AttributeSupplier.Builder attributes() { return baseAttributes(300, 7, 0.33, 4, 0.4); }

    // ------------------------------------------------------------------ phase plumbing
    private static boolean phase(FpeEntity e, int v) { return e.getVariant() == v && ((DangerAlice) e).revealT == 0; }
    private static Ability p1(String id, int dur, int cd) { return Ability.of(id, dur, cd).when(e -> phase(e, 0)); }
    private static Ability p2(String id, int dur, int cd) { return Ability.of(id, dur, cd).when(e -> phase(e, 1) && e.getStance() == 0); }
    /** phase 2, on all fours */
    private static Ability q2(String id, int dur, int cd) { return Ability.of(id, dur, cd).when(e -> phase(e, 1) && e.getStance() == 1); }

    @Override protected boolean hasBossBar() { return true; }
    @Override protected BossEvent.BossBarColor bossColor() { return BossEvent.BossBarColor.RED; }
    @Override public boolean isEnraged() { return getVariant() == 1 && getHealth() < getMaxHealth() * 0.3f; }
    @Override public double preferredDistance() { return getVariant() == 1 ? (getStance() == 1 ? 2.4 : 3.6) : 1.8; }
    /** on all fours she hunts: only gap closers while far away */
    @Override public boolean meleeFocus() { return getVariant() == 1 && getStance() == 1; }
    @Override public double engageRange() { return 7.0; }
    @Override protected int restTicks() { return getVariant() == 0 ? 12 : isEnraged() ? 8 : 16; }
    @Override public boolean causeFallDamage(float d, float m, DamageSource s) { return false; }
    @Override protected SoundEvent getAmbientSound() { return getVariant() == 1 ? SoundEvents.WARDEN_AMBIENT : SoundEvents.VEX_AMBIENT; }
    @Override protected SoundEvent getHurtSound(DamageSource s) { return getVariant() == 1 ? SoundEvents.WARDEN_HURT : SoundEvents.VEX_HURT; }
    @Override protected SoundEvent getDeathSound() { return SoundEvents.WARDEN_DEATH; }
    @Override public float getVoicePitch() { return getVariant() == 1 ? 0.8f : 1.3f; }

    @Override
    public EntityDimensions getDimensions(Pose pose) {
        if (getVariant() != 1) return super.getDimensions(pose);
        return getStance() == 1 ? EntityDimensions.scalable(4.06f, 3.61f) : EntityDimensions.scalable(2.48f, 5.87f);
    }

    @Override
    protected float getStandingEyeHeight(Pose pose, EntityDimensions d) { return d.height * (d.height > 3 ? 0.84f : 0.86f); }

    @Override
    public boolean hurt(DamageSource s, float a) {
        boolean bypass = s.is(DamageTypeTags.BYPASSES_INVULNERABILITY);
        if (revealT > 0 && !bypass) return false;
        if (getVariant() == 0 && !bypass) a = Math.min(a, Math.max(0.5f, getHealth() - getMaxHealth() * 0.5f + 0.5f)); // can't skip phase 2
        return super.hurt(s, a);
    }

    @Override
    public void tick() {
        super.tick();
        setMaxUpStep(getVariant() == 1 ? 1.4f : 0.6f);
        if (level().isClientSide || !isAlive()) return;
        if (getVariant() == 0 && revealT == 0 && getHealth() <= getMaxHealth() * 0.5f) {
            revealT = 1; cancelAbility(); forceAbility("reveal");
            sound(SoundEvents.WARDEN_HEARTBEAT, 2f, 0.7f);
        }
        if (revealT > 0) revealTick(revealT++);
        stanceTick();
    }

    // ------------------------------------------------------------------ quadruped stance switching (phase 2)
    private void stanceTick() {
        stanceT++;
        boolean quad = getStance() == 1;
        AttributeInstance sp = getAttribute(Attributes.MOVEMENT_SPEED);
        if (sp != null && quad != (sp.getModifier(QUAD_SPEED) != null)) {
            if (quad) sp.addTransientModifier(new AttributeModifier(QUAD_SPEED, "danger alice skitter", 0.6, AttributeModifier.Operation.MULTIPLY_TOTAL));
            else sp.removeModifier(QUAD_SPEED);
        }
        if (getVariant() != 1) { if (quad) setStance(0); return; }
        if (revealT > 0 || isBusy()) return;
        LivingEntity t = getTarget();
        if (t == null || !t.isAlive()) { if (quad && stanceT > 200) switchStance(0); return; }
        double d = distanceTo(t);
        if (!quad) {
            if (stanceT < 50) return;
            if ((d > 9 && stanceT > 70) || stanceT > nextSwap || (isEnraged() && random.nextInt(80) == 0)) forceAbility("drop_down");
        } else {
            int stay = isEnraged() ? nextSwap * 3 / 2 : nextSwap;
            if (stanceT > stay || (d < 4 && stanceT > 120 && random.nextInt(isEnraged() ? 70 : 35) == 0)) forceAbility("rise_up");
        }
    }

    private void switchStance(int s) {
        setStance(s);
        stanceT = 0;
        nextSwap = 200 + random.nextInt(200);
    }

    private void sound(SoundEvent s, float v, float p) { FpeUtil.sound(this, s, v, p); }

    private void revealTick(int t) {
        Vec3 c = position();
        setDeltaMovement(0, getDeltaMovement().y, 0);
        getNavigation().stop();
        if (t < T_FLIP) {
            float k = t / (float) T_FLIP;
            FpeUtil.particles(this, ParticleTypes.SQUID_INK, c.add(0, 1, 0), 2 + (int) (k * 8), 0.4 + k, 0.8, 0.4 + k, 0.05);
            if (t % 10 == 0) sound(SoundEvents.WARDEN_HEARTBEAT, 2f, 0.6f + k * 0.4f);
            if (t == 20 || t == 34 || t == 44) { // bandages snap off
                FpeUtil.particles(this, ParticleTypes.WHITE_ASH, c.add(0, 1, 0), 40, 0.5, 0.8, 0.5, 0.1);
                sound(SoundEvents.WOOL_BREAK, 2f, 0.6f);
            }
        }
        if (t == T_FLIP) {
            setVariant(1);
            stanceT = 0;
            setHealth(getMaxHealth() * 0.7f);
            getAttribute(Attributes.KNOCKBACK_RESISTANCE).setBaseValue(1.0);
            getAttribute(Attributes.ARMOR).setBaseValue(10);
            getAttribute(Attributes.ATTACK_DAMAGE).setBaseValue(10);
            FpeUtil.particles(this, ParticleTypes.SQUID_INK, c.add(0, 2, 0), 120, 1.2, 2, 1.2, 0.3);
            sound(SoundEvents.WARDEN_EMERGE, 3f, 0.9f);
        }
        if (t == T_ROAR) {
            sound(SoundEvents.WARDEN_ROAR, 4f, 0.8f);
            FpeUtil.particles(this, ParticleTypes.EXPLOSION, c.add(0, 1, 0), 4, 0.8, 0.5, 0.8, 0);
            FpeUtil.fx(this, FpeFx.Kind.RING_SHOCK, c.add(0, 0.1, 0), 0, 16, 10f, dmg(0.5f));
            FpeUtil.hitRadius(this, c, 5, dmg(0.6f), 2.0, 0.5);
            for (LivingEntity v : FpeUtil.enemiesInRadius(this, c, 14, 5, 3)) v.addEffect(new MobEffectInstance(MobEffects.DARKNESS, 100, 0));
        }
        if (t >= T_END) revealT = 0;
    }

    // ------------------------------------------------------------------ helpers
    private double groundY(double x, double z, double refY) {
        BlockPos.MutableBlockPos p = new BlockPos.MutableBlockPos(x, refY + 3, z);
        for (int i = 0; i < 10; i++, p.move(0, -1, 0)) {
            BlockPos b = p.below();
            if (level().getBlockState(p).getCollisionShape(level(), p).isEmpty() && !level().getBlockState(b).getCollisionShape(level(), b).isEmpty()) return p.getY();
        }
        return refY;
    }
    private FpeFx spike(double x, double z, double refY, int warm, int life, float dmg, float h) {
        return FpeUtil.fx(this, FpeFx.Kind.SPIKE, new Vec3(x, groundY(x, z, refY), z), warm, life, 1.2f, dmg).param(h);
    }
    private FpeFx tentacle(double x, double z, double refY, int warm, int life, float h) {
        return FpeUtil.fx(this, FpeFx.Kind.TENTACLE, new Vec3(x, groundY(x, z, refY), z), warm, life, 1.6f, dmg(0.5f)).param(h);
    }
    private void spikeRing(Vec3 c, double r, int n, int warm, float h, float off) {
        for (int i = 0; i < n; i++) {
            double a = Math.PI * 2 * (i + off) / n;
            spike(c.x + Math.cos(a) * r, c.z + Math.sin(a) * r, c.y, warm, 32, dmg(0.8f), h);
        }
    }
    private void line(ParticleOptions p, Vec3 a, Vec3 b, double step) {
        Vec3 d = b.subtract(a);
        int n = (int) Math.max(1, d.length() / step);
        for (int i = 0; i <= n; i++) FpeUtil.particles(this, p, a.add(d.scale(i / (double) n)), 1, 0.05, 0.05, 0.05, 0);
    }
    private static Vec3 chest(LivingEntity t) { return t.position().add(0, t.getBbHeight() * 0.6, 0); }
    private Vec3 flatDir(LivingEntity t) {
        Vec3 d = new Vec3(t.getX() - getX(), 0, t.getZ() - getZ());
        return d.lengthSqr() < 1e-4 ? FpeUtil.forward(this) : d.normalize();
    }
    private static void holdAt(LivingEntity v, Vec3 p) {
        v.setDeltaMovement(p.subtract(v.position()).scale(0.5));
        v.hurtMarked = true;
        v.fallDistance = 0;
    }
    /** one back spike shoots out as a lance (i = 0..5: right/left, top to bottom) */
    private void spikeLance(LivingEntity t, int i, float dmg, double len) {
        Vec3 from = position().add(0, 1.45 - (i / 2) * 0.2, 0).add(FpeUtil.right(this).scale(i % 2 == 0 ? 0.45 : -0.45));
        Vec3 to = from.add(chest(t).subtract(from).normalize().scale(len));
        FpeUtil.hitLine(this, from, to, 0.6, dmg, 0.7, 0.2);
        line(ParticleTypes.SQUID_INK, from, to, 0.5);
    }

    // ------------------------------------------------------------------ abilities
    @Override
    protected void registerAbilities(List<Ability> out) {
        // forced by tick(); logic lives in revealTick so it survives a lost target
        out.add(Ability.of("reveal", T_END, 0).range(0, 99).blind().when(e -> false));

        // ======================= PHASE 1 (human, back spikes) =======================
        // right spikes sweep, left spikes sweep, then all six stab forward with a lunge
        out.add(p1("spike_lash", 38, 40).range(0, 4.2).weight(4).faceUntil(16).tick((e, t, tk) -> {
            DangerAlice a = (DangerAlice) e;
            if (tk == 11 || tk == 18) {
                FpeCombat.cut(a, 3.8, 70, a.dmg(0.8f), 0.5, 0.15, 0, true);
                FpeCombat.slashArc(a, 3.6f, 130, tk == 11 ? 18 : -18, 0, 1.3, 0xE0101016);
                a.sound(SoundEvents.PLAYER_ATTACK_SWEEP, 1f, 0.8f);
            }
            if (tk == 25) a.dashForward(0.55, 0.05);
            if (tk == 27) {
                FpeCombat.cut(a, 4.2, 35, a.dmg(1.4f), 1.0, 0.3, 60, true);
                FpeUtil.particles(a, ParticleTypes.SQUID_INK, FpeUtil.ahead(a, 2.5, 1.2), 14, 0.5, 0.3, 0.5, 0.05);
                a.sound(SoundEvents.TRIDENT_HIT, 1f, 0.7f);
            }
        }));
        // the six spikes fire one after another as long lances
        out.add(p1("spike_barrage", 46, 70).range(3, 16).weight(4).faceUntil(26).tick((e, t, tk) -> {
            DangerAlice a = (DangerAlice) e;
            if (tk == 6) a.sound(SoundEvents.SCULK_CLICKING, 1f, 1.2f);
            if (tk >= 16 && tk <= 26 && (tk - 16) % 2 == 0) { a.spikeLance(t, (tk - 16) / 2, a.dmg(0.75f), 9); a.sound(SoundEvents.TRIDENT_THROW, 0.8f, 1.2f); }
        }));
        // all spikes braid into one giant lance and drive straight ahead
        out.add(p1("spike_impale", 42, 80).range(2, 10).weight(3).faceUntil(16).tick((e, t, tk) -> {
            DangerAlice a = (DangerAlice) e;
            if (tk == 19) {
                Vec3 s = a.position().add(0, 1.3, 0), b = s.add(FpeUtil.forward(a).scale(9));
                FpeUtil.hitLine(a, s, b, 1.2, a.dmg(1.9f), 1.4, 0.4);
                for (int k = 1; k <= 9; k++) FpeUtil.particles(a, ParticleTypes.SQUID_INK, s.add(FpeUtil.forward(a).scale(k)), 6, 0.5, 0.4, 0.2, 0.05);
                a.sound(SoundEvents.TRIDENT_HIT, 1.2f, 0.5f);
            }
        }));
        // melts into her shadow, rises behind the target and stabs with both lower spikes
        out.add(p1("blink_stab", 34, 70).range(3, 15).weight(3).blind().faceUntil(24).tick((e, t, tk) -> {
            DangerAlice a = (DangerAlice) e;
            if (tk == 9) FpeCombat.shadowStep(a, t);
            if (tk == 20) {
                FpeCombat.cut(a, 3.4, 45, a.dmg(1.6f), 0.8, 0.3, 70, false);
                FpeCombat.slashArc(a, 3.4f, 90, 80, 0, 1.0, 0xE0101016);
                a.sound(SoundEvents.PLAYER_ATTACK_CRIT, 1f, 0.8f);
            }
        }));
        // raises the warning-triangle pendant: a ringing pulse of darkness and slowness
        out.add(p1("pendant_pulse", 40, 100).range(0, 8).weight(2).blind().faceUntil(10).tick((e, t, tk) -> {
            DangerAlice a = (DangerAlice) e;
            if (tk == 6) a.sound(SoundEvents.AMETHYST_BLOCK_CHIME, 1.5f, 0.5f);
            if (tk == 18) {
                FpeUtil.fx(a, FpeFx.Kind.RING_SHOCK, a.position().add(0, 0.1, 0), 0, 14, 8f, a.dmg(0.4f)).color(0xFFE09040);
                for (LivingEntity v : FpeUtil.enemiesInRadius(a, a.position(), 8, 3, 1)) {
                    v.addEffect(new MobEffectInstance(MobEffects.DARKNESS, 100, 0));
                    v.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 60, 1));
                }
                a.sound(SoundEvents.BELL_BLOCK, 1.5f, 0.5f);
            }
        }));
        // flings her arm bandage like a whip, reels the target in and skewers it on her spikes
        out.add(p1("bandage_snare", 44, 90).range(3, 9).weight(3).faceUntil(12).start((e, t, tk) -> ((DangerAlice) e).holding = false).tick((e, t, tk) -> {
            DangerAlice a = (DangerAlice) e;
            if (tk == 12) {
                Vec3 s = a.position().add(0, 1.3, 0), b = s.add(chest(t).subtract(s).normalize().scale(9));
                a.line(ParticleTypes.WHITE_ASH, s, b, 0.3);
                a.sound(SoundEvents.FISHING_BOBBER_THROW, 1.2f, 0.6f);
                if (FpeUtil.hitLine(a, s, b, 0.7, a.dmg(0.4f), 0, 0) > 0 && t.distanceTo(a) < 10) a.holding = true;
            }
            if (a.holding && tk > 12 && tk < 24) holdAt(t, FpeUtil.ahead(a, 1.4, 0.1));
            if (tk == 25) {
                a.holding = false;
                if (FpeCombat.cut(a, 3.0, 50, a.dmg(1.4f), 1.2, 0.35, 60, true) > 0) a.sound(SoundEvents.TRIDENT_HIT, 1f, 0.6f);
                FpeUtil.particles(a, ParticleTypes.SQUID_INK, FpeUtil.ahead(a, 1.5, 1.2), 16, 0.4, 0.4, 0.4, 0.05);
            }
        }));
        // snaps the tips off her spikes and throws them like knives (two volleys)
        out.add(p1("shard_throw", 34, 50).range(4, 15).weight(3).faceUntil(22).tick((e, t, tk) -> {
            DangerAlice a = (DangerAlice) e;
            if (tk == 13 || tk == 22) {
                Vec3 from = a.position().add(0, 1.4, 0).add(FpeUtil.forward(a).scale(0.6));
                Vec3 v = FpeUtil.aim(from, t, 1.4, 0.3);
                int n = tk == 13 ? 1 : 2;
                for (int i = -n; i <= n; i++) FpeUtil.projectile(a, FpeProjectile.Kind.KNIFE, from, FpeCombat.rotY(v, i * (tk == 13 ? 8 : 5)), a.dmg(0.8f));
                a.sound(SoundEvents.TRIDENT_THROW, 1f, 1.4f);
            }
        }));
        // spins with the spikes fanned out like blades: two full revolutions
        out.add(p1("spike_whirl", 34, 70).range(0, 4.8).weight(3).faceUntil(8).tick((e, t, tk) -> {
            DangerAlice a = (DangerAlice) e;
            if (tk == 14 || tk == 20) {
                for (LivingEntity v : FpeUtil.enemiesInRadius(a, a.position(), 4.4, 2, 1)) { v.invulnerableTime = 0; FpeUtil.hit(a, v, a.dmg(0.9f), 1.0, 0.3); }
                FpeCombat.slashArc(a, 4.2f, 360, 0, 0, 1.2, 0xE0101016);
                a.sound(SoundEvents.PLAYER_ATTACK_SWEEP, 1.2f, 0.6f);
            }
        }));
        // stamps her sandal: a row of black spikes runs along the floor toward the target
        out.add(p1("shadow_spikes", 40, 90).range(3, 13).weight(2).faceUntil(13).tick((e, t, tk) -> {
            DangerAlice a = (DangerAlice) e;
            if (tk == 14) {
                a.sound(SoundEvents.EVOKER_FANGS_ATTACK, 1.2f, 0.7f);
                Vec3 d = a.flatDir(t);
                for (int i = 0; i < 8; i++) {
                    Vec3 p = a.position().add(d.scale(1.6 + i * 1.4));
                    a.spike(p.x, p.z, a.getY(), 2 + i * 2, 26, a.dmg(0.9f), 0.9f + i * 0.06f);
                }
            }
        }));

        // ======================= PHASE 2 (pitch-black monster) =======================
        // three huge claw rakes: right, left, both crashing down
        out.add(p2("claw_rake", 40, 45).range(0, 6.5).weight(4).faceUntil(20).tick((e, t, tk) -> {
            DangerAlice a = (DangerAlice) e;
            if (tk == 12 || tk == 19) {
                FpeCombat.cut(a, 6.0, 70, a.dmg(1.0f), 0.9, 0.25, 0, true);
                FpeCombat.slashArc(a, 5.8f, 140, tk == 12 ? 35 : -35, 0, 2.2, 0xE0080808);
                a.sound(SoundEvents.PLAYER_ATTACK_SWEEP, 1.6f, 0.5f);
            }
            if (tk == 28) {
                FpeCombat.cut(a, 5.5, 45, a.dmg(1.4f), 1.2, 0.5, 60, true);
                FpeUtil.particles(a, ParticleTypes.SQUID_INK, FpeUtil.ahead(a, 3.5, 0.2), 30, 1, 0.2, 1, 0.1);
                a.sound(SoundEvents.WARDEN_ATTACK_IMPACT, 1.4f, 0.6f);
            }
        }));
        // both claws raised overhead and slammed down: shockwave + spike ring
        out.add(p2("claw_slam", 46, 70).range(0, 7.5).weight(3).faceUntil(16).tick((e, t, tk) -> {
            DangerAlice a = (DangerAlice) e;
            if (tk == 6) a.sound(SoundEvents.WARDEN_ANGRY, 1.5f, 0.8f);
            if (tk == 22) {
                Vec3 p = FpeUtil.ahead(a, 3.8, 0);
                FpeUtil.hitRadius(a, p, 3.2, a.dmg(1.8f), 1.2, 0.7);
                FpeUtil.fx(a, FpeFx.Kind.RING_SHOCK, new Vec3(p.x, a.groundY(p.x, p.z, a.getY()) + 0.1, p.z), 0, 14, 7f, a.dmg(0.6f));
                a.spikeRing(p, 2.6, 8, 3, 1.3f, 0);
                FpeUtil.particles(a, ParticleTypes.EXPLOSION, p, 3, 1, 0.2, 1, 0);
                a.sound(SoundEvents.GENERIC_EXPLODE, 2f, 0.55f);
            }
        }));
        // claws plunge into the floor: three lanes of black spikes erupt toward the target
        out.add(p2("eruption", 50, 90).range(3, 16).weight(3).faceUntil(15).tick((e, t, tk) -> {
            DangerAlice a = (DangerAlice) e;
            if (tk == 16) { a.sound(SoundEvents.GENERIC_EXPLODE, 1.6f, 0.5f); FpeUtil.particles(a, ParticleTypes.SQUID_INK, FpeUtil.ahead(a, 2.5, 0.2), 40, 1.2, 0.2, 1.2, 0.15); }
            if (tk >= 18 && tk < 36 && tk % 2 == 0) {
                int i = (tk - 18) / 2;
                Vec3 f = FpeUtil.forward(a), side = new Vec3(-f.z, 0, f.x);
                for (int l = -1; l <= 1; l++) {
                    Vec3 p = a.position().add(f.scale(2.5 + i * 1.5)).add(side.scale(l * (1.2 + i * 0.25)));
                    a.spike(p.x, p.z, a.getY(), 6, 30, a.dmg(1.0f), 1.3f + i * 0.08f);
                }
            }
        }));
        // sinks a claw into the ground: tentacles burst up under and around the target
        out.add(p2("tentacle_grasp", 46, 110).range(3, 16).weight(3).blind().tick((e, t, tk) -> {
            DangerAlice a = (DangerAlice) e;
            if (tk == 6) a.sound(SoundEvents.SCULK_SHRIEKER_SHRIEK, 1.5f, 0.6f);
            if (tk == 16) {
                a.sound(SoundEvents.GENERIC_EXPLODE, 1.4f, 0.6f);
                Vec3 c = t.position();
                a.tentacle(c.x, c.z, c.y, 8, 80, 1.6f);
                for (int i = 0; i < 5; i++) {
                    double ang = Math.PI * 2 * i / 5 + a.random.nextDouble() * 0.4;
                    a.tentacle(c.x + Math.cos(ang) * 2.4, c.z + Math.sin(ang) * 2.4, c.y, 12 + i * 2, 80, 1.2f + a.random.nextFloat() * 0.4f);
                }
            }
        }));
        // two hard beats of the insect wings: a gale that hurls everything away
        out.add(p2("wing_gust", 44, 100).range(0, 12).weight(2).tick((e, t, tk) -> {
            DangerAlice a = (DangerAlice) e;
            if (tk == 16 || tk == 27) {
                FpeUtil.hitCone(a, 12, 55, a.dmg(0.3f), 1.9, 0.4);
                for (int i = 0; i < 6; i++) {
                    Vec3 o = a.position().add(0, 1 + i * 0.7, 0).add(FpeUtil.right(a).scale((a.random.nextDouble() - 0.5) * 4));
                    a.line(ParticleTypes.CLOUD, o, o.add(FpeUtil.forward(a).scale(9)), 1.0);
                }
                a.sound(SoundEvents.ENDER_DRAGON_FLAP, 2f, 1.1f);
            }
        }));
        // the grin splits open and spits a stream of homing shadow orbs
        out.add(p2("grin_volley", 48, 100).range(6, 20).weight(2).tick((e, t, tk) -> {
            DangerAlice a = (DangerAlice) e;
            if (tk == 6) a.sound(SoundEvents.WARDEN_SONIC_CHARGE, 2f, 1.3f);
            if (tk >= 14 && tk <= 32 && (tk - 14) % 3 == 0) {
                Vec3 from = a.position().add(0, 4.2, 0).add(FpeUtil.forward(a).scale(1.0));
                Vec3 v = FpeUtil.aim(from, t, 0.55, 0.2).add((a.random.nextDouble() - 0.5) * 0.3, a.random.nextDouble() * 0.15, (a.random.nextDouble() - 0.5) * 0.3);
                FpeUtil.projectile(a, FpeProjectile.Kind.SHADOW_ORB, from, v, a.dmg(0.5f));
                a.sound(SoundEvents.EVOKER_CAST_SPELL, 1f, 0.7f);
            }
        }));
        // crouches on all fours, leaps onto the target and lands claws-first in a spike ring
        out.add(p2("pounce", 50, 100).range(6, 16).weight(2).faceUntil(14).start((e, t, tk) -> ((DangerAlice) e).flag = false).tick((e, t, tk) -> {
            DangerAlice a = (DangerAlice) e;
            if (tk == 14) {
                a.dashToward(t.position(), Math.max(0.4, Math.min(1.4, a.distanceTo(t) / 11.0)), 0.85);
                a.sound(SoundEvents.RAVAGER_ROAR, 2f, 0.8f);
            }
            if (!a.flag && tk >= 22 && (a.onGround() || tk == 34)) {
                a.flag = true;
                FpeUtil.hitRadius(a, a.position(), 4.5, a.dmg(1.6f), 1.6, 0.7);
                FpeUtil.fx(a, FpeFx.Kind.RING_SHOCK, a.position().add(0, 0.1, 0), 0, 14, 8f, a.dmg(0.5f));
                a.spikeRing(a.position(), 3.2, 9, 3, 1.4f, 0);
                a.sound(SoundEvents.GENERIC_EXPLODE, 2f, 0.6f);
            }
        }));
        // snatches the target with the right claw, squeezes twice and smashes it down
        out.add(p2("grab_crush", 56, 120).range(0, 6).weight(2).faceUntil(14).start((e, t, tk) -> ((DangerAlice) e).holding = false).tick((e, t, tk) -> {
            DangerAlice a = (DangerAlice) e;
            if (tk == 14 && FpeCombat.cone(a, 5.5, 45).contains(t) && FpeUtil.hit(a, t, a.dmg(0.6f), 0, 0)) { a.holding = true; a.sound(SoundEvents.WARDEN_ATTACK_IMPACT, 1.5f, 0.7f); }
            if (!a.holding) return;
            if (tk > 14 && tk < 44) holdAt(t, a.position().add(FpeUtil.forward(a).scale(2.6)).add(0, 1.5 + 2.0 * Math.min(1, (tk - 14) / 10.0), 0));
            if (tk == 24 || tk == 34) {
                FpeUtil.hit(a, t, a.dmg(0.7f), 0, 0);
                FpeUtil.particles(a, ParticleTypes.CRIT, chest(t), 15, 0.4, 0.4, 0.4, 0.2);
                a.sound(SoundEvents.SKELETON_HURT, 1f, 0.4f);
            }
            if (tk == 44) {
                a.holding = false;
                t.setDeltaMovement(0, -1.4, 0); t.hurtMarked = true;
                FpeUtil.hit(a, t, a.dmg(1.3f), 1.2, 0.3);
                Vec3 p = FpeUtil.ahead(a, 2.6, 0);
                FpeUtil.fx(a, FpeFx.Kind.RING_SHOCK, new Vec3(p.x, a.groundY(p.x, p.z, a.getY()) + 0.1, p.z), 0, 10, 5f, a.dmg(0.4f));
                a.sound(SoundEvents.GENERIC_EXPLODE, 1.5f, 0.7f);
            }
        }));
        // spins on the spot with both claws out: two full mowing circles
        out.add(p2("spin_rend", 40, 70).range(0, 7).weight(3).faceUntil(8).tick((e, t, tk) -> {
            DangerAlice a = (DangerAlice) e;
            if (tk == 6) a.sound(SoundEvents.WARDEN_ATTACK_IMPACT, 1.2f, 0.5f);
            if (tk == 15 || tk == 22) {
                for (LivingEntity v : FpeUtil.enemiesInRadius(a, a.position(), 6.5, 3, 1)) { v.invulnerableTime = 0; FpeUtil.hit(a, v, a.dmg(1.0f), 1.6, 0.4); }
                FpeCombat.slashArc(a, 6.4f, 360, 0, 0, 1.8, 0xE0080808);
                FpeUtil.arc(a, ParticleTypes.SQUID_INK, a.position().add(0, 0.8, 0), 0, 180, 6, 36);
                a.sound(SoundEvents.PLAYER_ATTACK_SWEEP, 2f, 0.45f);
            }
        }));
        // ENRAGED signature "Welcome home": roar, tentacle cage, three spike rings, wings fire spike lances
        out.add(Ability.of("welcome_home", 72, 220).when(e -> phase(e, 1) && e.isEnraged()).range(0, 14).weight(5).blind().faceUntil(48).tick((e, t, tk) -> {
            DangerAlice a = (DangerAlice) e;
            if (tk == 12) {
                a.sound(SoundEvents.WARDEN_ROAR, 4f, 0.6f);
                FpeUtil.fx(a, FpeFx.Kind.RING_SHOCK, a.position().add(0, 0.1, 0), 0, 16, 11f, a.dmg(0.7f)).color(0xFF101018);
                for (LivingEntity v : FpeUtil.enemiesInRadius(a, a.position(), 14, 5, 3)) {
                    FpeUtil.knock(v, a.position(), 0.8, 0.3);
                    v.addEffect(new MobEffectInstance(MobEffects.DARKNESS, 120, 0));
                    v.addEffect(new MobEffectInstance(MobEffects.BLINDNESS, 40, 0));
                }
            }
            if (tk == 24) {
                Vec3 c = t.position();
                for (int i = 0; i < 7; i++) { double ang = Math.PI * 2 * i / 7; a.tentacle(c.x + Math.cos(ang) * 2.8, c.z + Math.sin(ang) * 2.8, c.y, 6 + i, 70, 1.5f); }
            }
            if (tk == 32) a.spikeRing(a.position(), 3.5, 10, 3, 1.5f, 0);
            if (tk == 38) a.spikeRing(a.position(), 6.0, 16, 3, 1.8f, 0.5f);
            if (tk == 44) a.spikeRing(a.position(), 8.5, 22, 3, 2.1f, 0.25f);
            if (tk >= 50 && tk <= 60 && tk % 2 == 0) {
                Vec3 from = a.position().add(0, 4.4, 0).add(FpeUtil.right(a).scale(((tk / 2) % 2 == 0 ? 1.4 : -1.4)));
                Vec3 to = from.add(chest(t).subtract(from).normalize().scale(14));
                FpeUtil.hitLine(a, from, to, 0.7, a.dmg(0.6f), 0.5, 0.1);
                a.line(ParticleTypes.SQUID_INK, from, to, 0.5);
                a.sound(SoundEvents.TRIDENT_THROW, 1.2f, 0.5f);
            }
        }));

        // ======================= PHASE 2 - QUADRUPED STANCE =======================
        // forced by stanceTick(): topples forward onto her claws (stance flips on the claw slam), tentacles burst out of her back
        out.add(Ability.of("drop_down", 26, 0).when(e -> false).blind().tick((e, t, tk) -> {
            DangerAlice a = (DangerAlice) e;
            if (tk == 2) a.sound(SoundEvents.WARDEN_ANGRY, 2f, 0.7f);
            if (tk == 14) {
                a.switchStance(1);
                Vec3 p = FpeUtil.ahead(a, 2.4, 0);
                FpeUtil.fx(a, FpeFx.Kind.RING_SHOCK, new Vec3(p.x, a.groundY(p.x, p.z, a.getY()) + 0.1, p.z), 0, 10, 4.5f, a.dmg(0.4f));
                FpeUtil.hitRadius(a, p, 2.6, a.dmg(0.6f), 0.9, 0.4);
                FpeUtil.particles(a, ParticleTypes.SQUID_INK, p, 30, 1.4, 0.2, 1.4, 0.15);
                a.sound(SoundEvents.WARDEN_STEP, 3f, 0.6f);
                a.sound(SoundEvents.SLIME_SQUISH, 2f, 0.5f);
            }
        }));
        // forced by stanceTick(): shoves off the floor and rears up with a shriek that pushes enemies off her
        out.add(Ability.of("rise_up", 26, 0).when(e -> false).blind().tick((e, t, tk) -> {
            DangerAlice a = (DangerAlice) e;
            if (tk == 10) {
                a.switchStance(0);
                a.sound(SoundEvents.WARDEN_ROAR, 2f, 0.9f);
                FpeUtil.hitRadius(a, a.position(), 3.8, a.dmg(0.4f), 1.6, 0.4);
                FpeUtil.particles(a, ParticleTypes.LARGE_SMOKE, a.position(), 20, 1.6, 0.2, 1.6, 0.05);
            }
        }));
        // screeches, paws the floor and skitters straight through everything, then tosses whatever is in front with a claw uppercut
        out.add(q2("quad_charge", 52, 90).range(6, 22).weight(3).closer().faceUntil(13).start((e, t, tk) -> { ((DangerAlice) e).hitIds.clear(); ((DangerAlice) e).flag = false; }).tick((e, t, tk) -> {
            DangerAlice a = (DangerAlice) e;
            if (tk == 3) a.sound(SoundEvents.WARDEN_ROAR, 2f, 1.2f);
            if (tk == 6 || tk == 9) { FpeUtil.particles(a, ParticleTypes.SQUID_INK, FpeUtil.ahead(a, 2.2, 0.1), 8, 0.5, 0.1, 0.5, 0.05); a.sound(SoundEvents.WARDEN_STEP, 1.5f, 0.8f); }
            if (tk >= 13 && tk <= 33 && !a.flag) {
                Vec3 f = FpeUtil.forward(a);
                a.setDeltaMovement(f.x * 1.05, a.getDeltaMovement().y, f.z * 1.05);
                a.hasImpulse = true;
                FpeUtil.particles(a, ParticleTypes.SQUID_INK, a.position().add(0, 0.4, 0), 4, 1.2, 0.2, 1.2, 0.02);
                if (tk % 3 == 0) a.sound(SoundEvents.SPIDER_STEP, 2f, 0.5f);
                for (LivingEntity v : FpeUtil.enemiesInRadius(a, FpeUtil.ahead(a, 2.0, 0), 2.4, 3, 1)) {
                    if (a.hitIds.add(v.getId())) { FpeUtil.hit(a, v, a.dmg(1.1f), 1.8, 0.55); a.sound(SoundEvents.PLAYER_ATTACK_KNOCKBACK, 1.5f, 0.5f); }
                }
                if (a.horizontalCollision && tk > 15) { a.flag = true; a.sound(SoundEvents.GENERIC_EXPLODE, 1.5f, 0.7f); FpeUtil.particles(a, ParticleTypes.EXPLOSION, FpeUtil.ahead(a, 2.2, 1.2), 3, 0.6, 0.6, 0.6, 0); }
            }
            if (tk == 34) a.setDeltaMovement(a.getDeltaMovement().scale(0.2));
            if (tk == 37) {
                FpeUtil.hitCone(a, 4.6, 70, a.dmg(1.3f), 0.8, 1.1);
                FpeCombat.slashArc(a, 4.4f, 120, -70, 0, 1.6, 0xEE080808);
                a.sound(SoundEvents.WARDEN_ATTACK_IMPACT, 2f, 0.7f);
            }
        }));
        // butt-wiggle and buzzing wings, then a huge leap onto the target: claws crash down (pinning shockwave + spike ring), then a bite
        out.add(q2("quad_pounce", 46, 80).range(4, 15).weight(3).closer().faceUntil(13).start((e, t, tk) -> ((DangerAlice) e).flag = false).tick((e, t, tk) -> {
            DangerAlice a = (DangerAlice) e;
            if (tk == 4) a.sound(SoundEvents.BEE_LOOP_AGGRESSIVE, 2.5f, 0.5f);
            if (tk == 13) { a.dashToward(t.position(), Math.max(0.5, Math.min(1.5, a.distanceTo(t) / 8.0)), 0.55); a.sound(SoundEvents.ENDER_DRAGON_FLAP, 2f, 1.2f); }
            if (!a.flag && tk >= 21 && (a.onGround() || tk == 27)) {
                a.flag = true;
                Vec3 p = FpeUtil.ahead(a, 1.8, 0);
                for (LivingEntity v : FpeUtil.enemiesInRadius(a, p, 3.4, 3, 1)) {
                    FpeUtil.hit(a, v, a.dmg(1.6f), 0.5, 0.2);
                    v.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 50, 3));
                }
                FpeUtil.fx(a, FpeFx.Kind.RING_SHOCK, a.position().add(0, 0.1, 0), 0, 12, 7f, a.dmg(0.5f));
                a.spikeRing(p, 3.0, 7, 3, 1.3f, 0);
                FpeUtil.particles(a, ParticleTypes.EXPLOSION, p, 3, 1.2, 0.2, 1.2, 0);
                a.sound(SoundEvents.GENERIC_EXPLODE, 2f, 0.6f);
            }
            if (tk == 28 && a.flag) {
                for (LivingEntity v : FpeUtil.enemiesInRadius(a, FpeUtil.ahead(a, 2.0, 1.0), 2.4, 3, 2)) { v.invulnerableTime = 0; FpeUtil.hit(a, v, a.dmg(0.6f), 0, 0); }
                a.sound(SoundEvents.PHANTOM_BITE, 1.6f, 0.5f);
            }
        }));
        // rears half up: right rake, left rake, then both claws hammer the floor
        out.add(q2("quad_rake", 40, 50).range(0, 6.5).weight(4).faceUntil(18).tick((e, t, tk) -> {
            DangerAlice a = (DangerAlice) e;
            if (tk == 4) a.sound(SoundEvents.WARDEN_ANGRY, 1.5f, 0.9f);
            if (tk == 12 || tk == 20) {
                FpeCombat.cut(a, 5.5, 80, a.dmg(1.05f), 0.5, 0.25, 0, true);
                FpeCombat.slashArc(a, 5.2f, 150, tk == 12 ? 50 : -50, 0, 1.6, 0xEE080808);
                a.sound(SoundEvents.PLAYER_ATTACK_SWEEP, 2f, 0.5f);
            }
            if (tk == 28) {
                Vec3 p = FpeUtil.ahead(a, 3.0, 0);
                FpeUtil.hitRadius(a, p, 3.0, a.dmg(1.3f), 1.3, 0.5);
                FpeUtil.fx(a, FpeFx.Kind.RING_SHOCK, new Vec3(p.x, a.groundY(p.x, p.z, a.getY()) + 0.1, p.z), 0, 10, 5f, a.dmg(0.4f));
                FpeUtil.particles(a, ParticleTypes.SQUID_INK, p, 25, 1.2, 0.2, 1.2, 0.15);
                a.sound(SoundEvents.WARDEN_ATTACK_IMPACT, 2f, 0.5f);
            }
        }));
        // pivots on her front claws: the tentacle-tails lengthen and mow a full circle
        out.add(q2("quad_tail_sweep", 40, 70).range(0, 7.5).weight(3).tick((e, t, tk) -> {
            DangerAlice a = (DangerAlice) e;
            if (tk == 6) a.sound(SoundEvents.WARDEN_ATTACK_IMPACT, 1.2f, 0.5f);
            if (tk == 16) {
                for (LivingEntity v : FpeUtil.enemiesInRadius(a, a.position(), 7.2, 3, 1)) {
                    FpeUtil.hit(a, v, a.dmg(1.2f), 2.4, 0.5);
                    v.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 40, 1));
                }
                FpeCombat.slashArc(a, 7.2f, 360, 0, 0, 0.7, 0xEE08080B);
                FpeUtil.arc(a, ParticleTypes.SQUID_INK, a.position().add(0, 0.4, 0), 0, 180, 6.5, 44);
                a.sound(SoundEvents.PLAYER_ATTACK_SWEEP, 2f, 0.4f);
            }
        }));
        // rears up shrieking, buries both claws and the tentacles: a fan of spikes and tentacles erupts toward the target, then a burst under it
        out.add(q2("quad_eruption", 54, 120).range(3, 16).weight(3).blind().faceUntil(16).tick((e, t, tk) -> {
            DangerAlice a = (DangerAlice) e;
            if (tk == 6) a.sound(SoundEvents.SCULK_SHRIEKER_SHRIEK, 2.5f, 0.6f);
            if (tk == 18) {
                Vec3 p0 = FpeUtil.ahead(a, 2.6, 0);
                FpeUtil.fx(a, FpeFx.Kind.RING_SHOCK, new Vec3(p0.x, a.groundY(p0.x, p0.z, a.getY()) + 0.1, p0.z), 0, 12, 6f, a.dmg(0.5f));
                FpeUtil.particles(a, ParticleTypes.SQUID_INK, p0, 50, 1.6, 0.3, 1.6, 0.25);
                a.sound(SoundEvents.GENERIC_EXPLODE, 2.5f, 0.5f);
                Vec3 d = a.flatDir(t), side = new Vec3(-d.z, 0, d.x);
                for (int r = 0; r < 9; r++) {
                    int w = 1 + r / 2;
                    for (int s = -w; s <= w; s++) {
                        Vec3 p = a.position().add(d.scale(3 + r * 1.5)).add(side.scale(s * 1.1 + (r % 2) * 0.5));
                        if ((r == 5 || r == 8) && s % 2 == 0) a.tentacle(p.x, p.z, a.getY(), 4 + r * 2, 50, 1.3f);
                        else a.spike(p.x, p.z, a.getY(), 2 + r * 2, 28, a.dmg(0.8f), 1.2f + r * 0.12f + a.random.nextFloat() * 0.3f);
                    }
                }
            }
            if (tk == 30) {
                Vec3 c = t.position();
                a.tentacle(c.x, c.z, c.y, 6, 60, 1.6f);
                for (int i = 0; i < 4; i++) { double ang = Math.PI * 0.5 * i + 0.4; a.spike(c.x + Math.cos(ang) * 2, c.z + Math.sin(ang) * 2, c.y, 8, 26, a.dmg(0.7f), 1.5f); }
                a.sound(SoundEvents.EVOKER_FANGS_ATTACK, 2f, 0.5f);
            }
            if (tk == 40) { FpeUtil.hitRadius(a, FpeUtil.ahead(a, 2.4, 0), 4.0, a.dmg(0.9f), 1.5, 0.6); a.sound(SoundEvents.ROOTED_DIRT_BREAK, 2f, 0.5f); }
        }));
        // the grin splits wide: lunging bite that withers, shakes the victim and flings it aside
        out.add(q2("quad_bite", 32, 45).range(0, 5.5).weight(4).faceUntil(10).tick((e, t, tk) -> {
            DangerAlice a = (DangerAlice) e;
            if (tk == 3) a.sound(SoundEvents.WARDEN_SNIFF, 2f, 0.8f);
            if (tk == 9) a.dashForward(0.7, 0.05);
            if (tk == 11) {
                for (LivingEntity v : FpeUtil.enemiesInRadius(a, FpeUtil.ahead(a, 2.2, 1.6), 2.6, 3, 2)) {
                    FpeUtil.hit(a, v, a.dmg(1.6f), 0.2, 0.1);
                    v.addEffect(new MobEffectInstance(MobEffects.WITHER, 60, 1));
                }
                a.sound(SoundEvents.EVOKER_FANGS_ATTACK, 2f, 0.6f);
                a.sound(SoundEvents.PHANTOM_BITE, 2f, 0.6f);
            }
            if (tk == 18) {
                FpeUtil.hitCone(a, 4.4, 60, a.dmg(0.7f), 1.7, 0.6);
                FpeUtil.particles(a, ParticleTypes.SQUID_INK, FpeUtil.ahead(a, 2.4, 1.6), 20, 0.6, 0.6, 0.6, 0.2);
                a.sound(SoundEvents.PLAYER_ATTACK_KNOCKBACK, 2f, 0.5f);
            }
        }));
        // arches her back like a cat, horns bristle: three volleys of black horn shards whip forward
        out.add(q2("quad_horn_volley", 44, 90).range(5, 20).weight(2).faceUntil(30).tick((e, t, tk) -> {
            DangerAlice a = (DangerAlice) e;
            if (tk == 6) a.sound(SoundEvents.CAT_HISS, 2.5f, 0.5f);
            if (tk == 18 || tk == 24 || tk == 30) {
                Vec3 from = a.position().add(0, 2.6, 0).add(FpeUtil.forward(a).scale(0.4));
                Vec3 aim = FpeUtil.aim(from, t, 1.2, 0.4);
                for (int i = -2; i <= 2; i++)
                    FpeUtil.projectile(a, FpeProjectile.Kind.KNIFE, from.add(FpeUtil.right(a).scale(i * 0.5)), FpeCombat.rotY(aim, i * 12 + (tk == 24 ? 6 : 0)), a.dmg(0.55f));
                FpeUtil.particles(a, ParticleTypes.SQUID_INK, from, 20, 1.2, 0.3, 1.2, 0.2);
                a.sound(SoundEvents.TRIDENT_THROW, 1.6f, 0.5f);
            }
        }));
        // ENRAGED: three bounding claw-slams that chase the target (spike lanes ahead), then a rearing double-claw crater
        out.add(Ability.of("quad_stampede", 64, 200).when(e -> phase(e, 1) && e.getStance() == 1 && e.isEnraged()).range(3, 20).weight(5).closer().faceUntil(40).blind().tick((e, t, tk) -> {
            DangerAlice a = (DangerAlice) e;
            if (tk == 3) { a.sound(SoundEvents.WARDEN_ROAR, 3f, 0.7f); a.sound(SoundEvents.SCULK_SHRIEKER_SHRIEK, 2f, 0.5f); }
            if (tk == 10 || tk == 22 || tk == 34) a.dashToward(t.position(), Math.max(0.5, Math.min(1.2, a.distanceTo(t) / 6.0)), 0.3);
            if (tk == 16 || tk == 28 || tk == 40) {
                Vec3 p = FpeUtil.ahead(a, 2.0, 0);
                FpeUtil.hitRadius(a, p, 3.6, a.dmg(1.0f), 1.0, 0.45);
                FpeUtil.fx(a, FpeFx.Kind.RING_SHOCK, a.position().add(0, 0.1, 0), 0, 10, 5.5f, a.dmg(0.4f));
                Vec3 d = FpeUtil.forward(a);
                for (int i = 0; i < 3; i++) { Vec3 s = a.position().add(d.scale(3.5 + i * 1.4)); a.spike(s.x, s.z, a.getY(), 2 + i * 2, 24, a.dmg(0.7f), 1.3f + i * 0.2f); }
                a.sound(SoundEvents.WARDEN_STEP, 3f, 0.5f);
                a.sound(SoundEvents.GENERIC_EXPLODE, 1.2f, 0.8f);
            }
            if (tk == 52) {
                Vec3 p = FpeUtil.ahead(a, 3.2, 0);
                FpeUtil.hitRadius(a, p, 4.8, a.dmg(2.0f), 1.8, 0.7);
                FpeUtil.fx(a, FpeFx.Kind.RING_SHOCK, new Vec3(p.x, a.groundY(p.x, p.z, a.getY()) + 0.1, p.z), 0, 16, 11f, a.dmg(0.7f));
                a.spikeRing(p, 4.0, 12, 3, 1.8f, 0);
                FpeUtil.particles(a, ParticleTypes.EXPLOSION_EMITTER, p, 1, 0, 0, 0, 0);
                FpeUtil.particles(a, ParticleTypes.SQUID_INK, p, 60, 2.5, 0.4, 2.5, 0.3);
                a.sound(SoundEvents.GENERIC_EXPLODE, 3f, 0.45f);
            }
        }));
    }
}
