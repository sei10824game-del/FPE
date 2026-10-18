package com.fpe.entity.characters;

import java.util.List;

import org.joml.Vector3f;

import com.fpe.entity.Ability;
import com.fpe.entity.FpeEntity;
import com.fpe.entity.FpeFx;
import com.fpe.entity.FpeProjectile;
import com.fpe.entity.FpeUtil;

import net.minecraft.core.BlockPos;
import net.minecraft.core.particles.BlockParticleOption;
import net.minecraft.core.particles.DustParticleOptions;
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
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.Vec3;

/**
 * Green Alice - two-phase GREEN_TEACHER boss (docs/ref/confirmed/green_alice_phase1.png / green_alice_phase2.png).
 * Phase 1 (variant 0, model green_alice): messy-haired girl in a white lab coat with glowing green eyes; thin black spider legs
 * burst from her back, she shoots web lines and lobs toxic flasks.
 * At <=50 % hp she is forced into an invulnerable "transform" and becomes (variant 1, model green_alice_boss) a giant pitch-black
 * spider-woman: eight huge jointed legs, a red-hourglass abdomen; leg impales, web nets/cocoons and black eruptions from the ground.
 * Transformation state == variant (saved by FpeEntity), so it happens exactly once.
 */
public class GreenAlice extends FpeEntity {
    /** transform timeline (ticks of the "transform" ability) */
    public static final int T_FLIP = 90, T_ROAR = 112, T_END = 130;

    private static final ParticleOptions TOXIC = new DustParticleOptions(new Vector3f(0.45f, 1f, 0.2f), 1.6f);
    private static final ParticleOptions BLOOD = new DustParticleOptions(new Vector3f(0.85f, 0.08f, 0.08f), 2.0f);
    private static final ParticleOptions WEB = new BlockParticleOption(ParticleTypes.BLOCK, Blocks.COBWEB.defaultBlockState());

    /** 0 = not transforming, else ticks into the transformation (server only, transient on purpose) */
    private int transformT;
    private boolean holding, flag;
    private Vec3 mark = Vec3.ZERO;

    public GreenAlice(EntityType<? extends FpeEntity> type, Level level) { super(type, level); }

    @Override public Faction faction() { return Faction.GREEN_TEACHER; }

    public static AttributeSupplier.Builder attributes() { return baseAttributes(500, 9, 0.34, 6, 0.4); }

    // ------------------------------------------------------------------ phase / boss plumbing
    private static boolean phase(FpeEntity e, int v) { return e.getVariant() == v && ((GreenAlice) e).transformT == 0; }
    private static Ability p1(String id, int dur, int cd) { return Ability.of(id, dur, cd).when(e -> phase(e, 0)); }
    private static Ability p2(String id, int dur, int cd) { return Ability.of(id, dur, cd).when(e -> phase(e, 1)); }

    @Override protected boolean hasBossBar() { return true; }
    @Override protected BossEvent.BossBarColor bossColor() { return BossEvent.BossBarColor.GREEN; }
    @Override public boolean isEnraged() { return getVariant() == 1 && getHealth() < getMaxHealth() * 0.25f; }
    @Override public double preferredDistance() { return getVariant() == 1 ? 4.5 : 2.0; }
    @Override protected int restTicks() { return getVariant() == 0 ? 12 : isEnraged() ? 10 : 18; }

    @Override
    public EntityDimensions getDimensions(Pose pose) {
        return getVariant() == 1 ? EntityDimensions.scalable(4.0f, 6.0f) : super.getDimensions(pose);
    }

    @Override
    protected float getStandingEyeHeight(Pose pose, EntityDimensions d) { return d.height * (d.height > 3 ? 0.84f : 0.86f); }

    @Override
    public boolean causeFallDamage(float dist, float mult, DamageSource src) { return false; }

    @Override
    public boolean hurt(DamageSource s, float amount) {
        boolean bypass = s.is(DamageTypeTags.BYPASSES_INVULNERABILITY);
        if (transformT > 0 && !bypass) return false;
        if (getVariant() == 0 && !bypass) // phase 1 can't skip the transformation with one huge hit
            amount = Math.min(amount, Math.max(0.5f, getHealth() - getMaxHealth() * 0.5f + 0.5f));
        return super.hurt(s, amount);
    }

    @Override
    public void tick() {
        super.tick();
        setMaxUpStep(getVariant() == 1 ? 1.6f : 0.6f);
        if (level().isClientSide || !isAlive()) return;
        if (transformT == 0 && getVariant() == 0 && getHealth() <= getMaxHealth() * 0.5f) {
            transformT = 1;
            forceAbility("transform");
            sound(SoundEvents.SPIDER_AMBIENT, 2f, 0.5f);
        }
        if (transformT > 0) transformTick(transformT++);
    }

    private void transformTick(int t) {
        Vec3 c = position();
        float k = Math.min(1f, t / (float) T_FLIP);
        setDeltaMovement(0, getDeltaMovement().y, 0);
        if (t < T_FLIP) {
            FpeUtil.particles(this, ParticleTypes.SQUID_INK, c.add(0, 1, 0), 2 + (int) (k * 8), 0.4 + k, 0.8, 0.4 + k, 0.05);
            if (t % 3 == 0) FpeUtil.particles(this, ParticleTypes.LARGE_SMOKE, c.add(0, 0.2, 0), 3 + (int) (k * 10), 1 + k * 2, 0.1, 1 + k * 2, 0.02);
            if (t % 20 == 0) {
                sound(SoundEvents.WARDEN_HEARTBEAT, 2.5f, 0.5f + k * 0.4f);
                FpeUtil.arc(this, WEB, c.add(0, 0.1, 0), 0, 180, 2 + k * 5, 30);
                for (LivingEntity v : FpeUtil.enemiesInRadius(this, c, 8, 3, 1)) FpeUtil.knock(v, c, 0.25, 0.25); // tremor
            }
            if (t == 40 || t == 62 || t == 80) { // spider legs tearing out of her back
                FpeUtil.particles(this, BLOOD, c.add(0, 1.4, 0), 30, 0.4, 0.6, 0.4, 0.2);
                FpeUtil.particles(this, ParticleTypes.SQUID_INK, c.add(0, 1.4, 0), 20, 0.4, 0.6, 0.4, 0.2);
                sound(SoundEvents.SPIDER_HURT, 2f, 0.5f);
                sound(SoundEvents.ZOMBIE_BREAK_WOODEN_DOOR, 0.8f, 1.4f);
            }
        }
        if (t == T_FLIP) {
            setVariant(1);
            setHealth(getMaxHealth() * 0.6f);
            getAttribute(Attributes.KNOCKBACK_RESISTANCE).setBaseValue(1.0);
            getAttribute(Attributes.ARMOR).setBaseValue(12);
            FpeUtil.particles(this, ParticleTypes.SQUID_INK, c.add(0, 2, 0), 120, 1.5, 2, 1.5, 0.3);
            FpeUtil.particles(this, WEB, c.add(0, 1.5, 0), 50, 1, 1.5, 1, 0.4);
            sound(SoundEvents.WARDEN_EMERGE, 3f, 0.8f);
        }
        if (t > T_FLIP && t < T_ROAR && t % 4 == 0) FpeUtil.particles(this, ParticleTypes.LARGE_SMOKE, c, 10, 1.5, 0.2, 1.5, 0.05);
        if (t == T_ROAR) {
            sound(SoundEvents.WARDEN_ROAR, 4f, 0.9f);
            sound(SoundEvents.SPIDER_AMBIENT, 4f, 0.4f);
            sound(SoundEvents.GENERIC_EXPLODE, 3f, 0.5f);
            FpeUtil.particles(this, ParticleTypes.EXPLOSION_EMITTER, c.add(0, 1, 0), 1, 0, 0, 0, 0);
            FpeUtil.fx(this, FpeFx.Kind.RING_SHOCK, c.add(0, 0.1, 0), 0, 18, 13f, dmg(0.6f));
            FpeUtil.hitRadius(this, c, 7, dmg(0.8f), 2.4, 0.6);
            for (LivingEntity v : FpeUtil.enemiesInRadius(this, c, 18, 6, 4)) {
                v.addEffect(new MobEffectInstance(MobEffects.DARKNESS, 120, 0));
                v.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 40, 1));
            }
        }
        if (t >= T_END) transformT = 0;
    }

    // ------------------------------------------------------------------ sounds
    @Override protected SoundEvent getAmbientSound() { return getVariant() == 1 ? SoundEvents.SPIDER_AMBIENT : SoundEvents.VEX_AMBIENT; }
    @Override protected SoundEvent getHurtSound(DamageSource s) { return getVariant() == 1 ? SoundEvents.SPIDER_HURT : SoundEvents.VEX_HURT; }
    @Override protected SoundEvent getDeathSound() { return getVariant() == 1 ? SoundEvents.SPIDER_DEATH : SoundEvents.VEX_DEATH; }
    @Override protected void playStepSound(BlockPos pos, BlockState st) {
        if (getVariant() == 1) playSound(SoundEvents.SPIDER_STEP, 1.6f, 0.5f); else super.playStepSound(pos, st);
    }
    @Override public float getVoicePitch() { return getVariant() == 1 ? 0.6f : 1.2f; }

    private void sound(SoundEvent s, float vol, float pitch) { FpeUtil.sound(this, s, vol, pitch); }

    // ------------------------------------------------------------------ helpers
    /** top of the first solid block near (x,z) around refY, falls back to refY */
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
        return FpeUtil.fx(this, FpeFx.Kind.TENTACLE, new Vec3(x, groundY(x, z, refY), z), warm, life, 1.6f, dmg(0.55f)).param(h);
    }

    private void spikeRing(Vec3 c, double r, int n, int warm, float h, float off) {
        for (int i = 0; i < n; i++) {
            double a = Math.PI * 2 * (i + off) / n;
            spike(c.x + Math.cos(a) * r, c.z + Math.sin(a) * r, c.y, warm, 34, dmg(0.8f), h);
        }
    }

    private void arcFx(double up, float radius, float sweep, float tilt, float yawOff, int color) {
        FpeFx f = FpeUtil.fx(this, FpeFx.Kind.ARC, position().add(0, up, 0), 0, 8, radius, 0).param(sweep).color(color);
        f.setYRot(getYRot() + yawOff); f.yRotO = f.getYRot();
        f.setXRot(tilt); f.xRotO = tilt;
    }

    private void lineParticles(ParticleOptions p, Vec3 a, Vec3 b, double step) {
        Vec3 d = b.subtract(a);
        int n = (int) Math.max(1, d.length() / step);
        for (int i = 0; i <= n; i++) FpeUtil.particles(this, p, a.add(d.scale(i / (double) n)), 1, 0.05, 0.05, 0.05, 0);
    }

    private static Vec3 chest(LivingEntity t) { return t.position().add(0, t.getBbHeight() * 0.6, 0); }
    private Vec3 flatDir(LivingEntity t) {
        Vec3 d = new Vec3(t.getX() - getX(), 0, t.getZ() - getZ());
        return d.lengthSqr() < 1e-4 ? FpeUtil.forward(this) : d.normalize();
    }
    private boolean inFront(LivingEntity t, double range, double halfDeg) {
        Vec3 d = new Vec3(t.getX() - getX(), 0, t.getZ() - getZ());
        if (d.length() - getBbWidth() * 0.5 - t.getBbWidth() * 0.5 > range) return false;
        return d.lengthSqr() < 0.01 || Math.toDegrees(Math.acos(Math.max(-1, Math.min(1, d.normalize().dot(FpeUtil.forward(this)))))) <= halfDeg;
    }
    /** drag a held victim toward a point (smooth, works for players since hurtMarked syncs velocity) */
    private static void holdAt(LivingEntity v, Vec3 p) {
        v.setDeltaMovement(p.subtract(v.position()).scale(0.6));
        v.hurtMarked = true;
        v.fallDistance = 0;
    }
    private static void webbed(LivingEntity v, int ticks, int amp) {
        v.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, ticks, amp));
        v.addEffect(new MobEffectInstance(MobEffects.DIG_SLOWDOWN, ticks, 0));
    }
    /** web line from `from` toward the target; true if it hit */
    private boolean webLine(LivingEntity t, Vec3 from, double len, float dmg) {
        Vec3 to = from.add(chest(t).subtract(from).normalize().scale(len));
        lineParticles(WEB, from, to, 0.5);
        if (t.getBoundingBox().inflate(0.6).clip(from, to).isPresent() && FpeUtil.hit(this, t, dmg, 0, 0)) {
            webbed(t, 60, 2);
            FpeUtil.particles(this, WEB, chest(t), 20, 0.4, 0.5, 0.4, 0.05);
            return true;
        }
        return false;
    }
    /** world position of a phase-2 front leg tip (approximate: high, out to the side, ahead) */
    private Vec3 legTip(int side, double up, double out) {
        return position().add(0, up, 0).add(FpeUtil.right(this).scale(side * out)).add(FpeUtil.forward(this).scale(1.5));
    }

    // ------------------------------------------------------------------ abilities
    @Override
    protected void registerAbilities(List<Ability> out) {
        // ======================= PHASE 1 =======================
        // two pairs of spider legs burst from her back and lance forward, right pair then left pair
        out.add(p1("leg_lance", 36, 50).range(0, 6.5).weight(3).faceUntil(20).tick((e, t, tk) -> {
            GreenAlice a = (GreenAlice) e;
            if (tk == 4) a.sound(SoundEvents.SPIDER_AMBIENT, 1f, 1.6f);
            if (tk == 12 || tk == 22) {
                Vec3 from = a.position().add(0, 1.4, 0).add(FpeUtil.right(a).scale(tk == 12 ? 0.5 : -0.5));
                Vec3 to = from.add(chest(t).subtract(from).normalize().scale(6.0));
                FpeUtil.hitLine(a, from, to, 0.6, a.dmg(0.9f), 0.5, 0.15);
                a.lineParticles(ParticleTypes.SQUID_INK, from, to, 0.5);
                a.sound(SoundEvents.TRIDENT_THROW, 1f, 0.7f);
            }
        }));
        // spins with the legs held out flat: lab-coat cyclone
        out.add(p1("coat_whirl", 32, 70).range(0, 4.5).weight(2).faceUntil(10).tick((e, t, tk) -> {
            GreenAlice a = (GreenAlice) e;
            if (tk == 10) a.sound(SoundEvents.PLAYER_ATTACK_SWEEP, 1.2f, 0.6f);
            if (tk == 15) {
                FpeUtil.hitRadius(a, a.position(), 4.3, a.dmg(1.3f), 1.2, 0.4);
                a.arcFx(1.1, 4.3f, 360, 0, 0, 0xEE101016);
                FpeUtil.arc(a, TOXIC, a.position().add(0, 1.1, 0), 0, 180, 3.6, 28);
            }
        }));
        // web line shot out of her palm: damage + heavy slow
        out.add(p1("web_shot", 30, 60).range(3.5, 16).weight(2).faceUntil(12).tick((e, t, tk) -> {
            GreenAlice a = (GreenAlice) e;
            if (tk == 6) a.sound(SoundEvents.SPIDER_AMBIENT, 0.8f, 1.8f);
            if (tk == 13) {
                a.webLine(t, a.position().add(0, 1.45, 0).add(FpeUtil.right(a).scale(-0.4)), 16, a.dmg(0.6f));
                a.sound(SoundEvents.FISHING_BOBBER_THROW, 1.2f, 0.8f);
            }
        }));
        // lobs a toxic flask: it shatters where the target stood and leaves a poison cloud
        out.add(p1("toxic_flask", 60, 90).range(4, 16).weight(2).faceUntil(13).tick((e, t, tk) -> {
            GreenAlice a = (GreenAlice) e;
            if (tk == 5) a.sound(SoundEvents.BOTTLE_FILL, 1f, 0.8f);
            if (tk == 14) {
                Vec3 from = a.position().add(0, 2.0, 0).add(FpeUtil.right(a).scale(0.4));
                a.mark = t.position().add(t.getDeltaMovement().scale(8));
                FpeUtil.projectile(a, FpeProjectile.Kind.BOMBLET, from, FpeUtil.aim(from, t, 0.7, 0.3).add(0, 0.18, 0), a.dmg(0.6f));
                a.sound(SoundEvents.SPLASH_POTION_THROW, 1.2f, 0.7f);
            }
            if (tk == 24) {
                a.sound(SoundEvents.SPLASH_POTION_BREAK, 1.5f, 0.6f);
                FpeUtil.particles(a, ParticleTypes.ITEM_SLIME, a.mark.add(0, 0.3, 0), 30, 1, 0.3, 1, 0.2);
            }
            if (tk >= 24 && tk <= 58 && tk % 3 == 0) {
                FpeUtil.particles(a, TOXIC, a.mark.add(0, 0.4, 0), 18, 1.6, 0.4, 1.6, 0.01);
                FpeUtil.particles(a, ParticleTypes.ENTITY_EFFECT, a.mark.add(0, 0.4, 0), 6, 1.4, 0.3, 1.4, 0);
                if (tk % 6 == 0) for (LivingEntity v : FpeUtil.enemiesInRadius(a, a.mark, 2.8, 2, 1)) {
                    v.addEffect(new MobEffectInstance(MobEffects.POISON, 60, 1));
                    v.addEffect(new MobEffectInstance(MobEffects.WEAKNESS, 60, 0));
                }
            }
        }));
        // slaps both palms and her legs into the floor: a web-snare (black tendril grab) springs up under the target
        out.add(p1("web_snare", 40, 90).range(3, 14).weight(2).blind().tick((e, t, tk) -> {
            GreenAlice a = (GreenAlice) e;
            if (tk == 6) a.sound(SoundEvents.SCULK_CLICKING, 1.2f, 0.8f);
            if (tk == 16) {
                a.sound(SoundEvents.WARDEN_STEP, 1.5f, 1.3f);
                FpeUtil.fx(a, FpeFx.Kind.RING_SHOCK, a.position().add(0, 0.1, 0), 0, 8, 3f, 0);
                Vec3 c = t.position();
                FpeUtil.fx(a, FpeFx.Kind.TENTACLE, new Vec3(c.x, a.groundY(c.x, c.z, c.y), c.z), 6, 40, 1.4f, a.dmg(0.6f)).param(0.9f);
                FpeUtil.arc(a, WEB, c.add(0, 0.2, 0), 0, 180, 1.8, 24);
            }
            if (tk == 24) for (LivingEntity v : FpeUtil.enemiesInRadius(a, t.position(), 2.6, 2, 1)) {
                FpeUtil.hit(a, v, a.dmg(0.6f), 0, 0.1);
                webbed(v, 70, 3);
            }
        }));
        // skitters forward on all fours and strikes with claws + legs
        out.add(p1("skitter_pounce", 28, 50).range(4, 12).weight(2).faceUntil(7).tick((e, t, tk) -> {
            GreenAlice a = (GreenAlice) e;
            if (tk == 7) { a.dashToward(t.position(), 1.3, 0.15); a.sound(SoundEvents.SPIDER_STEP, 1.2f, 1.4f); }
            if (tk > 7 && tk < 15) FpeUtil.particles(a, ParticleTypes.SQUID_INK, a.position().add(0, 0.4, 0), 2, 0.2, 0.2, 0.2, 0.01);
            if (tk == 15) { FpeUtil.hitCone(a, 3.0, 55, a.dmg(1.1f), 0.8, 0.25); a.sound(SoundEvents.SPIDER_HURT, 1f, 1.4f); }
        }));
        // low sweeping arc with all four legs: trips (knock up) everything in front
        out.add(p1("leg_sweep", 34, 60).range(0, 5).weight(2).faceUntil(10).tick((e, t, tk) -> {
            GreenAlice a = (GreenAlice) e;
            if (tk == 8) a.sound(SoundEvents.SPIDER_AMBIENT, 1f, 1.2f);
            if (tk == 14) {
                FpeUtil.hitCone(a, 4.8, 100, a.dmg(1.0f), 0.6, 0.6);
                a.arcFx(0.5, 4.6f, 200, 0, 0, 0xEE0E120C);
                a.sound(SoundEvents.PLAYER_ATTACK_SWEEP, 1.2f, 0.8f);
            }
        }));
        // legs rise like antennae and spit four homing venom orbs from their tips
        out.add(p1("venom_volley", 40, 80).range(5, 18).weight(2).tick((e, t, tk) -> {
            GreenAlice a = (GreenAlice) e;
            if (tk == 4) a.sound(SoundEvents.EVOKER_PREPARE_SUMMON, 1f, 1.4f);
            if (tk == 12 || tk == 16 || tk == 20 || tk == 24) {
                int i = (tk - 12) / 4;
                Vec3 from = a.position().add(0, 2.4 + (i / 2) * 0.3, 0).add(FpeUtil.right(a).scale(i % 2 == 0 ? 1.0 : -1.0)).subtract(FpeUtil.forward(a).scale(0.3));
                FpeUtil.projectile(a, FpeProjectile.Kind.SHADOW_ORB, from, FpeUtil.aim(from, t, 0.55, 0.2), a.dmg(0.6f));
                FpeUtil.particles(a, TOXIC, from, 8, 0.1, 0.1, 0.1, 0.05);
                a.sound(SoundEvents.LLAMA_SPIT, 1f, 0.8f);
            }
        }));
        // pounces, clamps the victim with arms + legs, bites twice and hurls it
        out.add(p1("grab_bite", 48, 90).range(0, 3.2).weight(2).faceUntil(12).start((e, t, tk) -> ((GreenAlice) e).holding = false).tick((e, t, tk) -> {
            GreenAlice a = (GreenAlice) e;
            if (tk == 8) a.dashToward(t.position(), 0.6, 0.1);
            if (tk == 11 && a.inFront(t, 2.4, 50) && FpeUtil.hit(a, t, a.dmg(0.5f), 0, 0)) { a.holding = true; a.sound(SoundEvents.SPIDER_AMBIENT, 1f, 0.8f); }
            if (!a.holding) return;
            if (tk > 11 && tk < 38) holdAt(t, FpeUtil.ahead(a, 1.2, 0.1));
            if (tk == 18 || tk == 28) {
                FpeUtil.hit(a, t, a.dmg(0.55f), 0, 0);
                t.addEffect(new MobEffectInstance(MobEffects.POISON, 60, 0));
                FpeUtil.particles(a, TOXIC, chest(t), 8, 0.3, 0.3, 0.3, 0.1);
                a.sound(SoundEvents.PHANTOM_BITE, 1f, 0.8f);
            }
            if (tk == 38) {
                a.holding = false;
                if (FpeUtil.hit(a, t, a.dmg(0.9f), 1.9, 0.7)) a.sound(SoundEvents.PLAYER_ATTACK_KNOCKBACK, 1f, 0.6f);
            }
        }));
        // web line sticks to the target, then she yanks it in
        out.add(p1("web_pull", 34, 60).range(3, 11).weight(2).faceUntil(12).start((e, t, tk) -> ((GreenAlice) e).flag = false).tick((e, t, tk) -> {
            GreenAlice a = (GreenAlice) e;
            if (tk == 12) {
                a.flag = a.webLine(t, a.position().add(0, 1.5, 0).add(FpeUtil.right(a).scale(-0.4)), 11, a.dmg(0.5f));
                a.sound(SoundEvents.FISHING_BOBBER_THROW, 1.2f, 0.6f);
            }
            if (tk > 12 && tk < 23 && a.flag && tk % 2 == 0) a.lineParticles(WEB, a.position().add(0, 1.5, 0), chest(t), 0.8);
            if (tk == 23 && a.flag) {
                Vec3 d = a.position().subtract(t.position());
                Vec3 v = new Vec3(d.x, 0, d.z).normalize().scale(Math.min(1.7, d.length() * 0.24));
                t.setDeltaMovement(v.x, 0.4, v.z);
                t.hurtMarked = true;
                a.sound(SoundEvents.FISHING_BOBBER_RETRIEVE, 1.2f, 0.5f);
            }
        }));
        // shrieking blast: knockback, nausea, weakness
        out.add(p1("shriek", 36, 110).range(0, 6).weight(1).tick((e, t, tk) -> {
            GreenAlice a = (GreenAlice) e;
            if (tk == 14) {
                a.sound(SoundEvents.GHAST_SCREAM, 2f, 1.6f);
                a.sound(SoundEvents.SPIDER_AMBIENT, 2f, 0.6f);
                FpeUtil.particles(a, ParticleTypes.SONIC_BOOM, a.position().add(0, 1.5, 0), 1, 0, 0, 0, 0);
                for (int r = 2; r <= 6; r += 2) FpeUtil.arc(a, TOXIC, a.position().add(0, 1, 0), 0, 180, r, 10 + r * 4);
                FpeUtil.hitRadius(a, a.position(), 6, a.dmg(0.5f), 1.7, 0.5);
                for (LivingEntity v : FpeUtil.enemiesInRadius(a, a.position(), 7, 3, 1)) {
                    v.addEffect(new MobEffectInstance(MobEffects.CONFUSION, 100, 0));
                    v.addEffect(new MobEffectInstance(MobEffects.WEAKNESS, 80, 0));
                }
            }
        }));
        // forced by tick(): the transformation (logic lives in transformTick so it survives a lost target)
        out.add(Ability.of("transform", T_END, 0).when(e -> false).blind());

        // ======================= PHASE 2 =======================
        // top legs cocked high, then each IMPALES the ground at the target; black spikes burst from the wounds
        out.add(p2("leg_impale", 40, 60).range(0, 9).weight(3).faceUntil(14).tick((e, t, tk) -> {
            GreenAlice a = (GreenAlice) e;
            if (tk == 6) a.sound(SoundEvents.SPIDER_AMBIENT, 2f, 0.5f);
            if (tk == 14 || tk == 22) a.mark = t.position();
            if (tk == 16 || tk == 24) {
                Vec3 p = a.mark.add(FpeUtil.right(a).scale(tk == 16 ? 0.6 : -0.6));
                FpeUtil.hitRadius(a, p, 2.0, a.dmg(1.5f), 0.6, 0.5);
                a.spike(p.x, p.z, p.y, 0, 22, a.dmg(0.5f), 1.5f);
                FpeUtil.particles(a, ParticleTypes.SQUID_INK, p, 20, 0.6, 0.2, 0.6, 0.15);
                a.lineParticles(ParticleTypes.SQUID_INK, a.legTip(tk == 16 ? 1 : -1, 6.5, 2.5), p, 0.7);
                a.sound(SoundEvents.TRIDENT_HIT, 2f, 0.5f);
                a.sound(SoundEvents.WARDEN_ATTACK_IMPACT, 1f, 0.7f);
            }
        }));
        // machine-gun jabs of the front legs
        out.add(p2("leg_barrage", 48, 80).range(0, 8.5).weight(3).faceUntil(30).tick((e, t, tk) -> {
            GreenAlice a = (GreenAlice) e;
            if (tk == 4) a.sound(SoundEvents.SPIDER_AMBIENT, 2f, 0.7f);
            if (tk == 12 || tk == 17 || tk == 22 || tk == 27 || tk == 32) {
                int side = (tk == 17 || tk == 27) ? -1 : 1;
                Vec3 from = a.legTip(side, 5.5, 2.0);
                Vec3 to = from.add(chest(t).subtract(from).normalize().scale(9));
                FpeUtil.hitLine(a, from, to, 0.9, a.dmg(0.7f), 0.5, 0.15);
                a.lineParticles(ParticleTypes.SQUID_INK, from, to, 0.6);
                a.sound(SoundEvents.TRIDENT_THROW, 1.5f, 0.5f);
            }
        }));
        // spinneret swings forward: a huge web net bursts over the target zone (heavy slow + mining fatigue)
        out.add(p2("web_net", 44, 110).range(5, 18).weight(2).faceUntil(16).tick((e, t, tk) -> {
            GreenAlice a = (GreenAlice) e;
            if (tk == 6) a.sound(SoundEvents.SPIDER_AMBIENT, 2f, 0.9f);
            if (tk == 18) {
                Vec3 from = a.position().add(0, 2.2, 0).add(FpeUtil.forward(a).scale(2.5));
                Vec3 c = t.position();
                a.lineParticles(WEB, from, c.add(0, 1, 0), 0.6);
                FpeUtil.particles(a, WEB, c.add(0, 1, 0), 60, 2, 1, 2, 0.1);
                for (int r = 1; r <= 3; r++) FpeUtil.arc(a, WEB, c.add(0, 0.2, 0), 0, 180, r * 1.2, 14 + r * 6);
                for (LivingEntity v : FpeUtil.enemiesInRadius(a, c, 3.8, 3, 1)) { FpeUtil.hit(a, v, a.dmg(0.5f), 0, 0); webbed(v, 100, 4); }
                a.sound(SoundEvents.SLIME_SQUISH, 2f, 0.5f);
                a.sound(SoundEvents.WOOL_PLACE, 2f, 0.5f);
            }
        }));
        // all eight legs plunge into the floor: black tentacles burst under and around the target
        out.add(p2("tentacle_field", 46, 110).range(3, 16).weight(3).blind().tick((e, t, tk) -> {
            GreenAlice a = (GreenAlice) e;
            if (tk == 6) a.sound(SoundEvents.WARDEN_ANGRY, 2f, 0.8f);
            if (tk == 18) {
                FpeUtil.particles(a, ParticleTypes.SQUID_INK, a.position(), 40, 2.5, 0.2, 2.5, 0.15);
                a.sound(SoundEvents.GENERIC_EXPLODE, 1.5f, 0.6f);
                Vec3 c = t.position();
                a.tentacle(c.x, c.z, c.y, 10, 90, 1.7f);
                for (int i = 0; i < 6; i++) {
                    double ang = Math.PI * 2 * i / 6 + a.random.nextDouble() * 0.4;
                    a.tentacle(c.x + Math.cos(ang) * 2.7, c.z + Math.sin(ang) * 2.7, c.y, 14 + i * 2, 90, 1.2f + a.random.nextFloat() * 0.5f);
                }
            }
        }));
        // front legs rake the floor: a widening carpet of black spikes rolls toward the target
        out.add(p2("spike_carpet", 48, 100).range(3, 14).weight(3).faceUntil(14).tick((e, t, tk) -> {
            GreenAlice a = (GreenAlice) e;
            if (tk == 16) {
                a.sound(SoundEvents.EVOKER_FANGS_ATTACK, 2f, 0.4f);
                Vec3 d = a.flatDir(t), side = new Vec3(-d.z, 0, d.x);
                for (int r = 0; r < 10; r++) {
                    int w = 1 + r / 3;
                    for (int s = -w; s <= w; s++) {
                        Vec3 p = a.position().add(d.scale(2.8 + r * 1.3)).add(side.scale(s * 1.3 + (r % 2) * 0.6));
                        a.spike(p.x, p.z, a.getY(), 4 + r * 2, 30 + r * 2, a.dmg(0.85f), 1.3f + r * 0.08f + a.random.nextFloat() * 0.3f);
                    }
                }
            }
        }));
        // mid legs used as scythes: two huge crescent sweeps
        out.add(p2("scythe_sweep", 46, 70).range(0, 9).weight(3).tick((e, t, tk) -> {
            GreenAlice a = (GreenAlice) e;
            if (tk == 15 || tk == 27) {
                FpeUtil.hitCone(a, 8.5, 100, a.dmg(1.3f), 1.4, 0.4);
                a.arcFx(2.4, 8.5f, 200, tk == 15 ? 12 : -12, 0, 0xEE0A0A0E);
                a.sound(SoundEvents.PLAYER_ATTACK_SWEEP, 2f, 0.5f);
                a.sound(SoundEvents.SPIDER_HURT, 1f, 0.6f);
            }
        }));
        // rears up on the hind legs and crashes the whole body down
        out.add(p2("body_slam", 44, 70).range(0, 7.5).weight(3).faceUntil(16).tick((e, t, tk) -> {
            GreenAlice a = (GreenAlice) e;
            if (tk == 6) a.sound(SoundEvents.SPIDER_AMBIENT, 2.5f, 0.4f);
            if (tk == 21) {
                Vec3 p = FpeUtil.ahead(a, 3.5, 0);
                FpeUtil.hitRadius(a, p, 3.6, a.dmg(1.9f), 1.2, 0.7);
                FpeUtil.fx(a, FpeFx.Kind.RING_SHOCK, new Vec3(p.x, a.groundY(p.x, p.z, a.getY()) + 0.1, p.z), 0, 14, 8f, a.dmg(0.7f));
                FpeUtil.particles(a, ParticleTypes.EXPLOSION, p, 4, 1, 0.2, 1, 0);
                FpeUtil.particles(a, ParticleTypes.SQUID_INK, p, 30, 1.5, 0.3, 1.5, 0.2);
                a.sound(SoundEvents.GENERIC_EXPLODE, 2f, 0.55f);
            }
        }));
        // front legs snap shut on the target, she hoists it and wraps it in silk, squeezes twice, then slams it down
        out.add(p2("web_cocoon", 56, 120).range(0, 6.5).weight(2).faceUntil(16).start((e, t, tk) -> ((GreenAlice) e).holding = false).tick((e, t, tk) -> {
            GreenAlice a = (GreenAlice) e;
            if (tk == 16 && a.inFront(t, 6.0, 45) && FpeUtil.hit(a, t, a.dmg(0.6f), 0, 0)) { a.holding = true; a.sound(SoundEvents.SPIDER_AMBIENT, 2f, 0.6f); }
            if (!a.holding) return;
            if (tk > 16 && tk < 46) {
                holdAt(t, a.position().add(FpeUtil.forward(a).scale(3.0)).add(0, 2.5 + 2.2 * Math.min(1, (tk - 16) / 10.0), 0));
                if (tk % 3 == 0) FpeUtil.particles(a, WEB, chest(t), 8, 0.4, 0.6, 0.4, 0.02);
            }
            if (tk == 26 || tk == 36) {
                FpeUtil.hit(a, t, a.dmg(0.7f), 0, 0);
                webbed(t, 80, 3);
                FpeUtil.particles(a, ParticleTypes.CRIT, chest(t), 15, 0.4, 0.4, 0.4, 0.2);
                a.sound(SoundEvents.WOOL_BREAK, 1.5f, 0.5f);
            }
            if (tk == 46) {
                a.holding = false;
                t.setDeltaMovement(0, -1.5, 0); t.hurtMarked = true;
                FpeUtil.hit(a, t, a.dmg(1.3f), 1.4, 0.3);
                Vec3 p = FpeUtil.ahead(a, 3.0, 0);
                FpeUtil.fx(a, FpeFx.Kind.RING_SHOCK, new Vec3(p.x, a.groundY(p.x, p.z, a.getY()) + 0.1, p.z), 0, 10, 5f, a.dmg(0.4f));
                a.sound(SoundEvents.GENERIC_EXPLODE, 1.5f, 0.7f);
            }
        }));
        // rears up and spits a barrage of homing venom orbs
        out.add(p2("venom_barrage", 52, 110).range(6, 20).weight(2).tick((e, t, tk) -> {
            GreenAlice a = (GreenAlice) e;
            if (tk == 6) a.sound(SoundEvents.WARDEN_SONIC_CHARGE, 2f, 1.3f);
            if (tk >= 14 && tk <= 38 && (tk - 14) % 3 == 0) {
                Vec3 from = a.position().add(0, 5.4, 0).add(FpeUtil.forward(a).scale(0.8));
                Vec3 v = FpeUtil.aim(from, t, 0.5, 0.2).add((a.random.nextDouble() - 0.5) * 0.3, a.random.nextDouble() * 0.15, (a.random.nextDouble() - 0.5) * 0.3);
                FpeUtil.projectile(a, FpeProjectile.Kind.SHADOW_ORB, from, v, a.dmg(0.5f));
                FpeUtil.particles(a, BLOOD, from, 4, 0.2, 0.2, 0.2, 0.05);
                a.sound(SoundEvents.LLAMA_SPIT, 1.5f, 0.5f);
            }
        }));
        // deafening shriek-roar: darkness + slow, shockwave
        out.add(p2("roar", 50, 220).range(0, 14).weight(1).blind().tick((e, t, tk) -> {
            GreenAlice a = (GreenAlice) e;
            if (tk == 18) {
                a.sound(SoundEvents.WARDEN_ROAR, 4f, 0.9f);
                a.sound(SoundEvents.SPIDER_AMBIENT, 4f, 0.4f);
                FpeUtil.particles(a, ParticleTypes.SONIC_BOOM, a.position().add(0, 5, 0).add(FpeUtil.forward(a).scale(2)), 3, 1, 0.5, 1, 0);
                FpeUtil.fx(a, FpeFx.Kind.RING_SHOCK, a.position().add(0, 0.1, 0), 0, 16, 12f, a.dmg(0.6f));
                FpeUtil.hitRadius(a, a.position(), 6, a.dmg(0.6f), 2.3, 0.6);
                for (LivingEntity v : FpeUtil.enemiesInRadius(a, a.position(), 16, 6, 4)) {
                    v.addEffect(new MobEffectInstance(MobEffects.DARKNESS, 120, 0));
                    v.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 60, 1));
                }
            }
        }));
        // crouches, leaps onto the target and lands with a spike-ringed shockwave
        out.add(p2("leap_slam", 52, 100).range(6, 16).weight(2).faceUntil(14).start((e, t, tk) -> ((GreenAlice) e).flag = false).tick((e, t, tk) -> {
            GreenAlice a = (GreenAlice) e;
            if (tk == 14) {
                a.dashToward(t.position(), Math.max(0.4, Math.min(1.5, a.distanceTo(t) / 11.0)), 0.95);
                a.sound(SoundEvents.SPIDER_AMBIENT, 2.5f, 0.5f);
            }
            if (!a.flag && tk >= 22 && (a.onGround() || tk == 40)) {
                a.flag = true;
                FpeUtil.hitRadius(a, a.position(), 5, a.dmg(1.7f), 1.6, 0.7);
                FpeUtil.fx(a, FpeFx.Kind.RING_SHOCK, a.position().add(0, 0.1, 0), 0, 16, 10f, a.dmg(0.6f));
                a.spikeRing(a.position(), 3.8, 10, 3, 1.6f, 0);
                FpeUtil.particles(a, ParticleTypes.EXPLOSION, a.position(), 6, 2, 0.2, 2, 0);
                a.sound(SoundEvents.GENERIC_EXPLODE, 2.5f, 0.5f);
            }
        }));
        // front legs driven into the ground: six lines of black spikes + tentacles erupt like a starburst, second pulse at 40
        out.add(p2("eruption", 60, 140).range(0, 14).weight(2).blind().tick((e, t, tk) -> {
            GreenAlice a = (GreenAlice) e;
            if (tk == 6) a.sound(SoundEvents.WARDEN_ROAR, 2.5f, 1.1f);
            if (tk == 16) {
                a.sound(SoundEvents.GENERIC_EXPLODE, 2.5f, 0.5f);
                FpeUtil.fx(a, FpeFx.Kind.RING_SHOCK, a.position().add(0, 0.1, 0), 0, 14, 7f, a.dmg(0.6f));
                FpeUtil.particles(a, ParticleTypes.SQUID_INK, a.position(), 60, 2, 0.3, 2, 0.3);
                double base = Math.atan2(t.getZ() - a.getZ(), t.getX() - a.getX());
                for (int l = 0; l < 6; l++) {
                    double ang = base + Math.PI * 2 * l / 6;
                    for (int i = 0; i < 7; i++) {
                        double r = 3.0 + i * 1.6;
                        a.spike(a.getX() + Math.cos(ang) * r, a.getZ() + Math.sin(ang) * r, a.getY(), 2 + i * 3, 30, a.dmg(0.85f), 1.4f + i * 0.15f);
                    }
                    double r = 3.0 + 7 * 1.6;
                    a.tentacle(a.getX() + Math.cos(ang) * r, a.getZ() + Math.sin(ang) * r, a.getY(), 24, 60, 1.6f);
                }
            }
            if (tk == 40) {
                FpeUtil.hitRadius(a, a.position(), 4.5, a.dmg(0.9f), 1.6, 0.6);
                FpeUtil.fx(a, FpeFx.Kind.RING_SHOCK, a.position().add(0, 0.1, 0), 0, 10, 5f, 0);
                a.sound(SoundEvents.WARDEN_ATTACK_IMPACT, 2f, 0.6f);
            }
        }));
        // quick double front-leg stomp for targets under her
        out.add(p2("stomp", 30, 40).range(0, 5).weight(3).tick((e, t, tk) -> {
            GreenAlice a = (GreenAlice) e;
            if (tk == 12) {
                FpeUtil.hitRadius(a, FpeUtil.ahead(a, 1.5, 0), 3.4, a.dmg(1.2f), 1.3, 0.5);
                FpeUtil.fx(a, FpeFx.Kind.RING_SHOCK, a.position().add(0, 0.1, 0), 0, 10, 5f, a.dmg(0.4f));
                a.sound(SoundEvents.SPIDER_STEP, 3f, 0.4f);
                a.sound(SoundEvents.GENERIC_EXPLODE, 1f, 0.8f);
            }
        }));
        // ENRAGED finisher: legs spear the floor, three throbbing spike rings, then a cataclysmic body slam
        out.add(Ability.of("abyss", 86, 300).when(e -> phase(e, 1) && e.isEnraged()).range(0, 16).weight(4).blind().tick((e, t, tk) -> {
            GreenAlice a = (GreenAlice) e;
            if (tk == 4) { a.sound(SoundEvents.WARDEN_ROAR, 4f, 0.6f); a.sound(SoundEvents.SPIDER_AMBIENT, 4f, 0.3f); }
            if (tk == 20) {
                Vec3 c = t.position();
                a.tentacle(c.x, c.z, c.y, 8, 80, 1.8f);
                for (int i = 0; i < 8; i++) { double ang = Math.PI * 2 * i / 8; a.tentacle(c.x + Math.cos(ang) * 3, c.z + Math.sin(ang) * 3, c.y, 10 + i, 80, 1.5f); }
                for (LivingEntity v : FpeUtil.enemiesInRadius(a, c, 4, 3, 1)) webbed(v, 60, 2);
            }
            if (tk == 34) a.spikeRing(a.position(), 3.8, 10, 3, 1.6f, 0);
            if (tk == 42) a.spikeRing(a.position(), 6.8, 18, 3, 1.9f, 0.5f);
            if (tk == 50) a.spikeRing(a.position(), 9.8, 26, 3, 2.2f, 0.25f);
            if (tk == 66) {
                Vec3 p = FpeUtil.ahead(a, 3.5, 0);
                FpeUtil.hitRadius(a, p, 5.5, a.dmg(2.2f), 2.0, 0.8);
                FpeUtil.fx(a, FpeFx.Kind.RING_SHOCK, a.position().add(0, 0.1, 0), 0, 20, 14f, a.dmg(0.9f));
                FpeUtil.particles(a, ParticleTypes.EXPLOSION_EMITTER, p, 1, 0, 0, 0, 0);
                FpeUtil.particles(a, BLOOD, p, 60, 3, 0.5, 3, 0.3);
                a.sound(SoundEvents.GENERIC_EXPLODE, 3f, 0.4f);
            }
        }));
    }
}
