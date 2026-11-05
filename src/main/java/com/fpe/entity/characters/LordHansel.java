package com.fpe.entity.characters;

import java.util.List;

import org.joml.Vector3f;

import com.fpe.entity.Ability;
import com.fpe.entity.FpeEntity;
import com.fpe.entity.FpeFx;
import com.fpe.entity.FpeProjectile;
import com.fpe.entity.FpeUtil;

import net.minecraft.core.BlockPos;
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
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.Vec3;

/**
 * Lord Hansel (FPE: Advanced Class, faction OUTSIDER) - three-form boss.
 * Variant 0 MATURED (docs/ref/confirmed/hansel_matured.png): pale fur-cloaked antlered beast-man, bandaged torso, black thorny
 * pauldrons, long black claws, a bloody claw-heart in his right hand, wrapped boots, huge fluffy tail. Fast melee hunter.
 * Variant 1 PREMATURE (hansel_premature.png): red-black corrupted mass of thorns/tendrils with a white grin, red glow ("THESE PESTS
 * ARE INTERRUPTING ME"). Bigger, tendrils + red bursts.
 * Variant 2 TRUE FORM / Windeigo (hansel_true_form.png): giant black tree-man, thorn-branch arm, red flame hair, red glowing
 * face, red mark on the chest. Root / branch eruptions.
 * Forced transformations at 66 % ("transform") and 33 % ("transform2") hp; the variant is saved by FpeEntity so each happens once.
 */
public class LordHansel extends FpeEntity {
    /** transform timelines (ticks of the "transform" / "transform2" abilities) */
    public static final int T_FLIP = 60, T_ROAR = 76, T_END = 90;
    public static final int T2_FLIP = 80, T2_ROAR = 100, T2_END = 120;

    private static final ParticleOptions RED = new DustParticleOptions(new Vector3f(0.85f, 0.05f, 0.06f), 2.0f);
    private static final ParticleOptions BLOOD = new DustParticleOptions(new Vector3f(0.55f, 0.0f, 0.02f), 1.4f);
    private static final ParticleOptions FUR = new DustParticleOptions(new Vector3f(0.93f, 0.88f, 0.74f), 1.5f);

    /** 0 = not transforming, else ticks into the transformation (server only, transient on purpose) */
    private int transformT, stage;
    private boolean holding, flag;

    public LordHansel(EntityType<? extends FpeEntity> type, Level level) { super(type, level); }

    @Override public Faction faction() { return Faction.OUTSIDER; }

    public static AttributeSupplier.Builder attributes() { return baseAttributes(600, 9, 0.34, 6, 0.4); }

    // ------------------------------------------------------------------ form / boss plumbing
    private static boolean form(FpeEntity e, int v) { return e.getVariant() == v && ((LordHansel) e).transformT == 0; }
    private static Ability f0(String id, int dur, int cd) { return Ability.of(id, dur, cd).when(e -> form(e, 0)); }
    private static Ability f1(String id, int dur, int cd) { return Ability.of(id, dur, cd).when(e -> form(e, 1)); }
    private static Ability f2(String id, int dur, int cd) { return Ability.of(id, dur, cd).when(e -> form(e, 2)); }

    @Override protected boolean hasBossBar() { return true; }
    @Override protected BossEvent.BossBarColor bossColor() { return BossEvent.BossBarColor.RED; }
    /** enraged = lower half of the current form's hp band */
    @Override public boolean isEnraged() {
        float h = getHealth() / getMaxHealth();
        return switch (getVariant()) { case 0 -> h < 0.83f; case 1 -> h < 0.5f; default -> h < 0.17f; };
    }
    @Override public double preferredDistance() { return getVariant() == 2 ? 5.0 : getVariant() == 1 ? 2.0 : 1.0; }
    @Override protected int restTicks() { return getVariant() == 0 ? 10 : isEnraged() ? 10 : 16; }

    @Override
    public EntityDimensions getDimensions(Pose pose) {
        return switch (getVariant()) {
            case 1 -> EntityDimensions.scalable(1.5f, 3.8f);
            case 2 -> EntityDimensions.scalable(2.6f, 8.0f);
            default -> super.getDimensions(pose);
        };
    }

    @Override
    protected float getStandingEyeHeight(Pose pose, EntityDimensions d) { return d.height * 0.86f; }

    @Override
    public boolean causeFallDamage(float dist, float mult, DamageSource src) { return false; }

    @Override
    public boolean hurt(DamageSource s, float amount) {
        boolean bypass = s.is(DamageTypeTags.BYPASSES_INVULNERABILITY);
        if (transformT > 0 && !bypass) return false;
        float floor = getVariant() == 0 ? 0.66f : getVariant() == 1 ? 0.33f : -1f;
        if (floor > 0 && !bypass) // a form can't be skipped with one huge hit
            amount = Math.min(amount, Math.max(0.5f, getHealth() - getMaxHealth() * floor + 0.5f));
        return super.hurt(s, amount);
    }

    @Override
    public void tick() {
        super.tick();
        setMaxUpStep(getVariant() == 2 ? 2.2f : getVariant() == 1 ? 1.2f : 0.6f);
        if (level().isClientSide || !isAlive()) return;
        if (transformT == 0) {
            if (getVariant() == 0 && getHealth() <= getMaxHealth() * 0.66f) startTransform("transform");
            else if (getVariant() == 1 && getHealth() <= getMaxHealth() * 0.33f) startTransform("transform2");
        }
        if (transformT > 0) {
            if (stage == 1) transformTick(transformT++); else transform2Tick(transformT++);
        }
    }

    private void startTransform(String id) {
        transformT = 1;
        stage = id.equals("transform") ? 1 : 2;
        cancelAbility();
        forceAbility(id);
        sound(SoundEvents.WARDEN_HEARTBEAT, 2f, 0.6f);
    }

    /** matured -> premature: the claw-heart is crushed into his chest, red-black corruption bursts out */
    private void transformTick(int t) {
        Vec3 c = position();
        float k = Math.min(1f, t / (float) T_FLIP);
        setDeltaMovement(0, getDeltaMovement().y, 0);
        if (t < T_FLIP) {
            FpeUtil.particles(this, RED, c.add(0, 1.4, 0), 2 + (int) (k * 8), 0.4 + k, 0.8, 0.4 + k, 0.02);
            if (t % 3 == 0) FpeUtil.particles(this, ParticleTypes.SQUID_INK, c.add(0, 0.4, 0), 3 + (int) (k * 8), 0.8 + k, 0.2, 0.8 + k, 0.03);
            if (t % 12 == 0) sound(SoundEvents.WARDEN_HEARTBEAT, 2.5f, 0.6f + k * 0.5f);
            if (t == 22) { // heart crushed into the chest
                FpeUtil.particles(this, BLOOD, c.add(0, 1.5, 0), 40, 0.3, 0.3, 0.3, 0.2);
                sound(SoundEvents.SLIME_SQUISH, 2f, 0.5f);
            }
            if (t == 40) { FpeUtil.particles(this, FUR, c.add(0, 1.5, 0), 40, 0.6, 0.8, 0.6, 0.2); sound(SoundEvents.WOOL_BREAK, 2f, 0.5f); }
        }
        if (t == T_FLIP) {
            setVariant(1);
            setHealth(Math.max(getHealth(), getMaxHealth() * 0.7f));
            getAttribute(Attributes.KNOCKBACK_RESISTANCE).setBaseValue(0.8);
            getAttribute(Attributes.ARMOR).setBaseValue(10);
            getAttribute(Attributes.MOVEMENT_SPEED).setBaseValue(0.31);
            FpeUtil.particles(this, RED, c.add(0, 2, 0), 120, 1.4, 2, 1.4, 0.2);
            FpeUtil.particles(this, ParticleTypes.SQUID_INK, c.add(0, 2, 0), 80, 1.2, 1.6, 1.2, 0.3);
            sound(SoundEvents.WARDEN_EMERGE, 3f, 1.1f);
        }
        if (t == T_ROAR) {
            sound(SoundEvents.RAVAGER_ROAR, 3f, 0.6f);
            sound(SoundEvents.GENERIC_EXPLODE, 2f, 0.7f);
            FpeUtil.fx(this, FpeFx.Kind.RING_SHOCK, c.add(0, 0.1, 0), 0, 16, 9f, dmg(0.5f));
            FpeUtil.hitRadius(this, c, 5, dmg(0.7f), 2.0, 0.5);
            FpeUtil.particles(this, ParticleTypes.EXPLOSION, c.add(0, 1, 0), 4, 1, 1, 1, 0);
        }
        if (t >= T_END) transformT = 0;
    }

    /** premature -> true form: the corruption hardens into bark, he grows into a towering tree (Windeigo) */
    private void transform2Tick(int t) {
        Vec3 c = position();
        float k = Math.min(1f, t / (float) T2_FLIP);
        setDeltaMovement(0, getDeltaMovement().y, 0);
        if (t < T2_FLIP) {
            if (t % 2 == 0) FpeUtil.particles(this, ParticleTypes.SQUID_INK, c.add(0, 1.5, 0), 3 + (int) (k * 10), 0.6 + k, 1 + k, 0.6 + k, 0.04);
            if (t % 4 == 0) FpeUtil.particles(this, ParticleTypes.FLAME, c.add(0, 3 + k * 2, 0), 4 + (int) (k * 10), 0.5, 0.5, 0.5, 0.03);
            if (t % 16 == 0) {
                sound(SoundEvents.WARDEN_HEARTBEAT, 3f, 0.4f + k * 0.3f);
                for (int i = 0; i < 6; i++) { double a = Math.PI * 2 * i / 6 + t; spike(c.x + Math.cos(a) * (2 + k * 4), c.z + Math.sin(a) * (2 + k * 4), c.y, 3, 20, 0, 0.8f + k); }
                for (LivingEntity v : FpeUtil.enemiesInRadius(this, c, 9, 3, 1)) FpeUtil.knock(v, c, 0.3, 0.25);
            }
            if (t == 30 || t == 56) sound(SoundEvents.WOOD_BREAK, 3f, 0.4f);
        }
        if (t == T2_FLIP) {
            setVariant(2);
            setHealth(Math.max(getHealth(), getMaxHealth() * 0.4f));
            getAttribute(Attributes.KNOCKBACK_RESISTANCE).setBaseValue(1.0);
            getAttribute(Attributes.ARMOR).setBaseValue(14);
            getAttribute(Attributes.MOVEMENT_SPEED).setBaseValue(0.27);
            FpeUtil.particles(this, ParticleTypes.SQUID_INK, c.add(0, 4, 0), 160, 2, 4, 2, 0.3);
            FpeUtil.particles(this, ParticleTypes.FLAME, c.add(0, 7, 0), 60, 1.5, 1, 1.5, 0.1);
            sound(SoundEvents.WARDEN_EMERGE, 4f, 0.6f);
        }
        if (t == T2_ROAR) {
            sound(SoundEvents.WARDEN_ROAR, 4f, 0.5f);
            sound(SoundEvents.GENERIC_EXPLODE, 3f, 0.5f);
            FpeUtil.particles(this, ParticleTypes.EXPLOSION_EMITTER, c.add(0, 1, 0), 1, 0, 0, 0, 0);
            FpeUtil.fx(this, FpeFx.Kind.RING_SHOCK, c.add(0, 0.1, 0), 0, 20, 14f, dmg(0.6f));
            spikeRing(c, 5, 12, 2, 2.0f, 0);
            FpeUtil.hitRadius(this, c, 7, dmg(0.8f), 2.4, 0.6);
            for (LivingEntity v : FpeUtil.enemiesInRadius(this, c, 20, 8, 4)) v.addEffect(new MobEffectInstance(MobEffects.DARKNESS, 140, 0));
        }
        if (t >= T2_END) transformT = 0;
    }

    // ------------------------------------------------------------------ sounds
    @Override protected SoundEvent getAmbientSound() { return switch (getVariant()) { case 0 -> SoundEvents.WOLF_GROWL; case 1 -> SoundEvents.WARDEN_AMBIENT; default -> SoundEvents.WARDEN_AMBIENT; }; }
    @Override protected SoundEvent getHurtSound(DamageSource s) { return getVariant() == 0 ? SoundEvents.WOLF_HURT : SoundEvents.WARDEN_HURT; }
    @Override protected SoundEvent getDeathSound() { return getVariant() == 0 ? SoundEvents.WOLF_DEATH : SoundEvents.WARDEN_DEATH; }
    @Override protected void playStepSound(BlockPos pos, BlockState st) {
        if (getVariant() == 2) playSound(SoundEvents.WARDEN_STEP, 2f, 0.5f);
        else if (getVariant() == 1) playSound(SoundEvents.WARDEN_STEP, 1f, 0.9f);
        else super.playStepSound(pos, st);
    }
    @Override public float getVoicePitch() { return getVariant() == 2 ? 0.55f : getVariant() == 1 ? 0.8f : 0.95f; }

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

    private FpeFx tentacle(double x, double z, double refY, int warm, int life, float h, float dmg) {
        return FpeUtil.fx(this, FpeFx.Kind.TENTACLE, new Vec3(x, groundY(x, z, refY), z), warm, life, 1.6f, dmg).param(h);
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

    private void healFrac(float frac) { setHealth(Math.min(getMaxHealth(), getHealth() + getMaxHealth() * frac)); }

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
    private void fireCone(double range, double half, float dmg) {
        for (LivingEntity v : FpeUtil.enemiesInRadius(this, position(), range, 4, 2)) if (inFront(v, range, half)) {
            if (FpeUtil.hit(this, v, dmg, 0.3, 0.1)) v.setSecondsOnFire(4);
        }
    }

    // ------------------------------------------------------------------ abilities
    @Override
    protected void registerAbilities(List<Ability> out) {
        // ======================= MATURED (variant 0) =======================
        // left claw rakes down, then a rising backhand
        out.add(f0("claw_rake", 30, 34).range(0, 3.6).weight(4).faceUntil(9).tick((e, t, tk) -> {
            LordHansel a = (LordHansel) e;
            if (tk == 6) a.sound(SoundEvents.WOLF_GROWL, 1f, 1.2f);
            if (tk == 11 || tk == 19) {
                FpeUtil.hitCone(a, 3.2, 70, a.dmg(tk == 11 ? 0.9f : 1.1f), tk == 11 ? 0.3 : 1.0, tk == 11 ? 0.1 : 0.45);
                a.arcFx(1.4, 3.0f, 150, tk == 11 ? 60 : -45, 0, 0xEE141414);
                a.sound(SoundEvents.PLAYER_ATTACK_SWEEP, 1f, tk == 11 ? 1.2f : 0.9f);
            }
        }));
        // lowers the antlers and charges through the target, tossing it up
        out.add(f0("antler_charge", 34, 60).range(3, 12).weight(3).faceUntil(9).start((e, t, tk) -> ((LordHansel) e).flag = false).tick((e, t, tk) -> {
            LordHansel a = (LordHansel) e;
            if (tk == 4) a.sound(SoundEvents.RAVAGER_STEP, 1.2f, 1.3f);
            if (tk == 10) { a.dashForward(1.25, 0.05); a.sound(SoundEvents.RAVAGER_ATTACK, 1.2f, 1.2f); }
            if (tk > 10 && tk < 20) {
                FpeUtil.particles(a, FUR, a.position().add(0, 0.3, 0), 3, 0.3, 0.1, 0.3, 0.01);
                if (!a.flag && FpeUtil.hitCone(a, 1.9, 60, a.dmg(1.3f), 1.0, 0.8) > 0) { a.flag = true; a.sound(SoundEvents.PLAYER_ATTACK_KNOCKBACK, 1.2f, 0.7f); }
            }
            if (tk == 20) a.setDeltaMovement(a.getDeltaMovement().scale(0.2));
        }));
        // hurls fans of black thorn shards with the left claw
        out.add(f0("thorn_throw", 32, 50).range(4, 16).weight(3).faceUntil(20).tick((e, t, tk) -> {
            LordHansel a = (LordHansel) e;
            if (tk == 11 || tk == 20) {
                Vec3 from = a.position().add(0, 1.7, 0).add(FpeUtil.right(a).scale(-0.5));
                Vec3 v = FpeUtil.aim(from, t, 1.3, 0.3);
                for (int i = -1; i <= 1; i++) FpeUtil.projectile(a, FpeProjectile.Kind.KNIFE, from, v.yRot((float) Math.toRadians(i * 11)), a.dmg(0.6f));
                a.sound(SoundEvents.TRIDENT_THROW, 1f, 1.1f);
            }
        }));
        // raises the bloody claw-heart: it beats three times, blood pulses out and feeds him
        out.add(f0("heart_pulse", 40, 90).range(0, 5).weight(2).blind().tick((e, t, tk) -> {
            LordHansel a = (LordHansel) e;
            if (tk == 12 || tk == 22 || tk == 32) {
                Vec3 h = a.position().add(0, 2.0, 0).add(FpeUtil.forward(a).scale(0.5));
                a.sound(SoundEvents.WARDEN_HEARTBEAT, 2f, 1.0f);
                FpeUtil.particles(a, BLOOD, h, 25, 0.2, 0.2, 0.2, 0.25);
                FpeUtil.arc(a, RED, a.position().add(0, 0.4, 0), 0, 180, 1.5 + (tk - 12) / 10 * 1.2, 30);
                int n = FpeUtil.hitRadius(a, a.position(), 3.6, a.dmg(0.5f), 0.6, 0.2);
                a.healFrac(0.008f + n * 0.006f);
            }
        }));
        // spins on the spot, the huge fluffy tail sweeps everything away
        out.add(f0("tail_sweep", 28, 45).range(0, 3.8).weight(3).tick((e, t, tk) -> {
            LordHansel a = (LordHansel) e;
            if (tk == 13) {
                FpeUtil.hitRadius(a, a.position(), 3.8, a.dmg(0.9f), 1.6, 0.4);
                a.arcFx(0.8, 3.8f, 360, 0, 0, 0xCCEDE3C6);
                FpeUtil.arc(a, FUR, a.position().add(0, 0.8, 0), 0, 180, 3.2, 30);
                a.sound(SoundEvents.PLAYER_ATTACK_SWEEP, 1.2f, 0.6f);
            }
        }));
        // crouches, pounces onto the target, slams both claws down, then bites
        out.add(f0("pounce_maul", 44, 70).range(3, 10).weight(3).faceUntil(10).start((e, t, tk) -> ((LordHansel) e).flag = false).tick((e, t, tk) -> {
            LordHansel a = (LordHansel) e;
            if (tk == 10) { a.dashToward(t.position(), Math.min(1.3, a.distanceTo(t) * 0.17), 0.6); a.sound(SoundEvents.WOLF_GROWL, 1.3f, 0.8f); }
            if (!a.flag && tk >= 16 && (a.onGround() || tk == 22)) {
                a.flag = true;
                FpeUtil.hitRadius(a, FpeUtil.ahead(a, 0.8, 0), 2.6, a.dmg(1.2f), 0.4, 0.2);
                FpeUtil.particles(a, ParticleTypes.CRIT, FpeUtil.ahead(a, 0.8, 0.4), 15, 0.6, 0.2, 0.6, 0.2);
                a.sound(SoundEvents.PLAYER_ATTACK_STRONG, 1.2f, 0.7f);
            }
            if (tk == 28) {
                FpeUtil.hitCone(a, 2.6, 60, a.dmg(0.9f), 0.9, 0.3);
                FpeUtil.particles(a, BLOOD, FpeUtil.ahead(a, 1.2, 1.2), 12, 0.3, 0.3, 0.3, 0.1);
                a.sound(SoundEvents.PHANTOM_BITE, 1.2f, 0.6f);
            }
        }));
        // slams the claw-heart into the ground: a line of bloody black thorns races toward the target
        out.add(f0("blood_spikes", 36, 70).range(3, 14).weight(2).faceUntil(14).tick((e, t, tk) -> {
            LordHansel a = (LordHansel) e;
            if (tk == 15) {
                Vec3 d = a.flatDir(t), side = new Vec3(-d.z, 0, d.x);
                for (int i = 0; i < 11; i++) {
                    Vec3 p = a.position().add(d.scale(1.4 + i * 1.15)).add(side.scale(i % 2 == 0 ? 0.35 : -0.35));
                    a.spike(p.x, p.z, a.getY(), 2 + i * 2, 28 + i * 2, a.dmg(0.85f), 0.9f + i * 0.06f);
                }
                FpeUtil.particles(a, BLOOD, FpeUtil.ahead(a, 1, 0.2), 30, 0.4, 0.1, 0.4, 0.15);
                a.sound(SoundEvents.EVOKER_FANGS_ATTACK, 1.2f, 0.7f);
            }
        }));
        // throws the head back and howls: slowness + weakness, small shockwave
        out.add(f0("howl", 40, 140).range(0, 9).weight(1).blind().tick((e, t, tk) -> {
            LordHansel a = (LordHansel) e;
            if (tk == 16) {
                a.sound(SoundEvents.WOLF_HOWL, 3f, 0.6f);
                a.sound(SoundEvents.WARDEN_SONIC_CHARGE, 1f, 1.5f);
                FpeUtil.fx(a, FpeFx.Kind.RING_SHOCK, a.position().add(0, 0.1, 0), 0, 14, 7f, a.dmg(0.3f));
                FpeUtil.hitRadius(a, a.position(), 4, a.dmg(0.4f), 1.4, 0.4);
                for (LivingEntity v : FpeUtil.enemiesInRadius(a, a.position(), 10, 4, 2)) {
                    v.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 80, 1));
                    v.addEffect(new MobEffectInstance(MobEffects.WEAKNESS, 80, 0));
                }
            }
        }));
        // ENRAGED: lunges, hooks the victim on his claws, carves twice (life steal) and flings it away
        out.add(Ability.of("heart_harvest", 56, 160).when(e -> form(e, 0) && e.isEnraged()).range(0, 5).weight(3).faceUntil(10)
                .start((e, t, tk) -> ((LordHansel) e).holding = false).tick((e, t, tk) -> {
            LordHansel a = (LordHansel) e;
            if (tk == 8) a.dashToward(t.position(), 0.7, 0.1);
            if (tk == 12 && a.inFront(t, 2.6, 55) && FpeUtil.hit(a, t, a.dmg(0.5f), 0, 0)) { a.holding = true; a.sound(SoundEvents.PHANTOM_BITE, 1f, 0.6f); }
            if (!a.holding) return;
            if (tk > 12 && tk < 44) holdAt(t, FpeUtil.ahead(a, 1.3, 0.5));
            if (tk == 22 || tk == 32) {
                FpeUtil.hit(a, t, a.dmg(0.7f), 0, 0);
                a.healFrac(0.02f);
                FpeUtil.particles(a, BLOOD, chest(t), 20, 0.3, 0.3, 0.3, 0.15);
                a.sound(SoundEvents.SLIME_SQUISH, 1.2f, 0.5f);
            }
            if (tk == 44) {
                a.holding = false;
                FpeUtil.hit(a, t, a.dmg(1.0f), 2.0, 0.7);
                a.sound(SoundEvents.PLAYER_ATTACK_KNOCKBACK, 1.2f, 0.6f);
            }
        }));
        // forced by tick(): matured -> premature
        out.add(Ability.of("transform", T_END, 0).when(e -> false).blind());

        // ======================= PREMATURE (variant 1) =======================
        // two thorn tendrils lance out of his back one after the other
        out.add(f1("thorn_lash", 34, 50).range(2, 9).weight(3).faceUntil(16).tick((e, t, tk) -> {
            LordHansel a = (LordHansel) e;
            if (tk == 5) a.sound(SoundEvents.SCULK_CLICKING, 1.2f, 0.6f);
            if (tk == 12 || tk == 18) {
                Vec3 from = a.position().add(0, 3.0, 0).add(FpeUtil.right(a).scale(tk == 12 ? 0.9 : -0.9));
                Vec3 to = from.add(chest(t).subtract(from).normalize().scale(9));
                FpeUtil.hitLine(a, from, to, 0.7, a.dmg(0.9f), 0.5, 0.15);
                a.lineParticles(RED, from, to, 0.5);
                a.sound(SoundEvents.TRIDENT_THROW, 1.2f, 0.5f);
            }
        }));
        // frantic four-hit claw flurry, stepping forward with every swipe
        out.add(f1("frenzy_claws", 34, 50).range(0, 4.5).weight(4).faceUntil(20).tick((e, t, tk) -> {
            LordHansel a = (LordHansel) e;
            if (tk == 8 || tk == 12 || tk == 16 || tk == 21) {
                a.dashForward(0.25, 0);
                boolean last = tk == 21;
                FpeUtil.hitCone(a, 3.6, 70, a.dmg(last ? 1.1f : 0.55f), last ? 1.3 : 0.15, last ? 0.4 : 0.05);
                a.arcFx(1.9, 3.4f, 140, (tk / 4) % 2 == 0 ? 50 : -50, 0, 0xEEB01018);
                a.sound(SoundEvents.PLAYER_ATTACK_SWEEP, 1f, 1.0f + (tk % 8) * 0.04f);
            }
        }));
        // claws dig in: red-black tendrils burst up under and around the target
        out.add(f1("tendril_field", 42, 100).range(3, 16).weight(3).blind().tick((e, t, tk) -> {
            LordHansel a = (LordHansel) e;
            if (tk == 6) a.sound(SoundEvents.WARDEN_ANGRY, 1.5f, 1.0f);
            if (tk == 16) {
                Vec3 c = t.position();
                a.tentacle(c.x, c.z, c.y, 8, 70, 1.4f, a.dmg(0.55f));
                for (int i = 0; i < 4; i++) {
                    double ang = Math.PI * 2 * i / 4 + a.random.nextDouble() * 0.5;
                    a.tentacle(c.x + Math.cos(ang) * 2.4, c.z + Math.sin(ang) * 2.4, c.y, 12 + i * 2, 70, 1.1f, a.dmg(0.5f));
                }
                FpeUtil.particles(a, RED, FpeUtil.ahead(a, 1.5, 0.2), 30, 0.8, 0.1, 0.8, 0.1);
                a.sound(SoundEvents.SCULK_SHRIEKER_SHRIEK, 1.2f, 0.7f);
            }
        }));
        // hunches, gathers red energy, bursts it out around himself (sets on fire)
        out.add(f1("crimson_burst", 38, 80).range(0, 5).weight(2).blind().tick((e, t, tk) -> {
            LordHansel a = (LordHansel) e;
            if (tk < 18 && tk % 2 == 0) FpeUtil.particles(a, RED, a.position().add(0, 2, 0), 6, 1.2, 1.2, 1.2, -0.05);
            if (tk == 4) a.sound(SoundEvents.WARDEN_SONIC_CHARGE, 1.5f, 1.4f);
            if (tk == 18) {
                FpeUtil.particles(a, RED, a.position().add(0, 2, 0), 80, 1.5, 1.5, 1.5, 0.4);
                FpeUtil.particles(a, ParticleTypes.FLAME, a.position().add(0, 1, 0), 40, 1.5, 0.8, 1.5, 0.15);
                FpeUtil.fx(a, FpeFx.Kind.RING_SHOCK, a.position().add(0, 0.1, 0), 0, 12, 6f, 0);
                for (LivingEntity v : FpeUtil.enemiesInRadius(a, a.position(), 5, 3, 1)) if (FpeUtil.hit(a, v, a.dmg(1.2f), 1.6, 0.5)) v.setSecondsOnFire(4);
                a.sound(SoundEvents.GENERIC_EXPLODE, 1.5f, 0.9f);
            }
        }));
        // "THESE PESTS...": both fists raised overhead and hammered down, shockwave
        out.add(f1("pest_swat", 44, 70).range(0, 6).weight(3).faceUntil(16).tick((e, t, tk) -> {
            LordHansel a = (LordHansel) e;
            if (tk == 6) a.sound(SoundEvents.RAVAGER_ROAR, 1.2f, 1.3f);
            if (tk == 21) {
                Vec3 p = FpeUtil.ahead(a, 2.4, 0);
                FpeUtil.hitRadius(a, p, 2.8, a.dmg(1.7f), 1.0, 0.7);
                FpeUtil.fx(a, FpeFx.Kind.RING_SHOCK, new Vec3(p.x, a.groundY(p.x, p.z, a.getY()) + 0.1, p.z), 0, 12, 6f, a.dmg(0.5f));
                FpeUtil.particles(a, ParticleTypes.EXPLOSION, p, 2, 0.6, 0.2, 0.6, 0);
                FpeUtil.particles(a, RED, p, 30, 1.2, 0.2, 1.2, 0.2);
                a.sound(SoundEvents.GENERIC_EXPLODE, 1.6f, 0.7f);
            }
        }));
        // glitches out, reappears behind the target and rakes twice
        out.add(f1("glitch_blink", 32, 80).range(3, 16).weight(2).blind().tick((e, t, tk) -> {
            LordHansel a = (LordHansel) e;
            if (tk == 8) { FpeUtil.particles(a, RED, a.position().add(0, 1.8, 0), 40, 0.5, 1.2, 0.5, 0.1); a.sound(SoundEvents.ENDERMAN_TELEPORT, 1f, 0.5f); }
            if (tk == 10) {
                Vec3[] tries = { t.position().subtract(FpeUtil.forward(t).scale(2.2)), t.position().add(FpeUtil.right(t).scale(2.2)), t.position().subtract(FpeUtil.right(t).scale(2.2)) };
                for (Vec3 p : tries) if (a.level().noCollision(a, a.getBoundingBox().move(p.subtract(a.position())))) { a.teleportTo(p.x, p.y, p.z); break; }
                a.snapFace(t);
                FpeUtil.particles(a, RED, a.position().add(0, 1.8, 0), 40, 0.5, 1.2, 0.5, 0.1);
            }
            if (tk == 15 || tk == 21) {
                FpeUtil.hitCone(a, 3.4, 75, a.dmg(tk == 15 ? 0.8f : 1.1f), tk == 15 ? 0.3 : 1.2, 0.3);
                a.arcFx(1.8, 3.2f, 150, tk == 15 ? 40 : -40, 0, 0xEE9A0A12);
                a.sound(SoundEvents.PLAYER_ATTACK_SWEEP, 1f, 0.8f);
            }
        }));
        // tendrils on his back spit a stream of homing red-black orbs
        out.add(f1("thorn_barrage", 44, 90).range(5, 20).weight(2).tick((e, t, tk) -> {
            LordHansel a = (LordHansel) e;
            if (tk == 4) a.sound(SoundEvents.EVOKER_PREPARE_SUMMON, 1f, 0.8f);
            if (tk >= 12 && tk <= 32 && (tk - 12) % 4 == 0) {
                int i = (tk - 12) / 4;
                Vec3 from = a.position().add(0, 3.2 + (i % 2) * 0.4, 0).add(FpeUtil.right(a).scale(i % 2 == 0 ? 1.2 : -1.2));
                FpeUtil.projectile(a, FpeProjectile.Kind.SHADOW_ORB, from, FpeUtil.aim(from, t, 0.6, 0.2), a.dmg(0.6f));
                FpeUtil.particles(a, RED, from, 8, 0.2, 0.2, 0.2, 0.05);
                a.sound(SoundEvents.EVOKER_CAST_SPELL, 0.9f, 0.8f);
            }
        }));
        // grin splits wide: a screeching scream (nausea, slowness) and a push
        out.add(f1("grin_scream", 40, 130).range(0, 8).weight(1).blind().tick((e, t, tk) -> {
            LordHansel a = (LordHansel) e;
            if (tk == 16) {
                a.sound(SoundEvents.GHAST_SCREAM, 2f, 0.6f);
                a.sound(SoundEvents.WARDEN_ROAR, 1.2f, 1.6f);
                FpeUtil.particles(a, ParticleTypes.SONIC_BOOM, a.position().add(0, 3, 0).add(FpeUtil.forward(a).scale(1.5)), 1, 0, 0, 0, 0);
                for (int r = 2; r <= 8; r += 2) FpeUtil.arc(a, RED, a.position().add(0, 1.5, 0), 0, 180, r, 10 + r * 4);
                FpeUtil.hitRadius(a, a.position(), 7, a.dmg(0.5f), 2.0, 0.5);
                for (LivingEntity v : FpeUtil.enemiesInRadius(a, a.position(), 9, 4, 2)) {
                    v.addEffect(new MobEffectInstance(MobEffects.CONFUSION, 120, 0));
                    v.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 60, 1));
                }
            }
        }));
        // ENRAGED: arms flung wide, the corruption spreads in three rings of thorns, then a red detonation
        out.add(Ability.of("corruption_wave", 60, 200).when(e -> form(e, 1) && e.isEnraged()).range(0, 12).weight(3).blind().tick((e, t, tk) -> {
            LordHansel a = (LordHansel) e;
            if (tk == 4) a.sound(SoundEvents.WITHER_AMBIENT, 2f, 0.7f);
            if (tk == 18) a.spikeRing(a.position(), 2.8, 8, 2, 1.4f, 0);
            if (tk == 26) a.spikeRing(a.position(), 5.0, 14, 2, 1.7f, 0.5f);
            if (tk == 34) a.spikeRing(a.position(), 7.2, 20, 2, 2.0f, 0.25f);
            if (tk == 18 || tk == 26 || tk == 34) { a.sound(SoundEvents.EVOKER_FANGS_ATTACK, 1.5f, 0.5f); FpeUtil.particles(a, RED, a.position().add(0, 0.3, 0), 40, 3, 0.1, 3, 0.1); }
            if (tk == 46) {
                FpeUtil.hitRadius(a, a.position(), 4.5, a.dmg(1.5f), 2.0, 0.6);
                FpeUtil.fx(a, FpeFx.Kind.RING_SHOCK, a.position().add(0, 0.1, 0), 0, 16, 10f, a.dmg(0.6f));
                FpeUtil.particles(a, RED, a.position().add(0, 2, 0), 100, 2, 2, 2, 0.4);
                a.sound(SoundEvents.GENERIC_EXPLODE, 2.5f, 0.6f);
            }
        }));
        // forced by tick(): premature -> true form
        out.add(Ability.of("transform2", T2_END, 0).when(e -> false).blind());

        // ======================= TRUE FORM / WINDEIGO (variant 2) =======================
        // the thorn-branch arm sweeps a huge arc in front of him
        out.add(f2("branch_sweep", 44, 60).range(0, 9).weight(4).faceUntil(12).tick((e, t, tk) -> {
            LordHansel a = (LordHansel) e;
            if (tk == 6) a.sound(SoundEvents.WOOD_BREAK, 2f, 0.4f);
            if (tk == 20) {
                FpeUtil.hitCone(a, 9, 110, a.dmg(1.5f), 1.8, 0.5);
                a.arcFx(3.5, 9f, 220, 10, 0, 0xEE060606);
                a.sound(SoundEvents.PLAYER_ATTACK_SWEEP, 2.5f, 0.4f);
                a.sound(SoundEvents.WARDEN_ATTACK_IMPACT, 1.2f, 0.6f);
            }
        }));
        // stamps a foot: root lines erupt outward in a fan toward the target
        out.add(f2("root_eruption", 46, 90).range(3, 16).weight(3).faceUntil(16).tick((e, t, tk) -> {
            LordHansel a = (LordHansel) e;
            if (tk == 18) {
                a.sound(SoundEvents.GENERIC_EXPLODE, 2f, 0.5f);
                FpeUtil.fx(a, FpeFx.Kind.RING_SHOCK, a.position().add(0, 0.1, 0), 0, 10, 5f, 0);
                double base = Math.atan2(t.getZ() - a.getZ(), t.getX() - a.getX());
                for (int l = -2; l <= 2; l++) {
                    double ang = base + l * 0.32;
                    for (int i = 0; i < 9; i++) {
                        double r = 2.2 + i * 1.5;
                        a.spike(a.getX() + Math.cos(ang) * r, a.getZ() + Math.sin(ang) * r, a.getY(), 2 + i * 2, 30, a.dmg(0.9f), 1.4f + i * 0.12f);
                    }
                }
            }
        }));
        // roots stab up under the target three times, tracking it
        out.add(f2("impale_roots", 44, 80).range(2, 22).weight(3).blind().tick((e, t, tk) -> {
            LordHansel a = (LordHansel) e;
            if (tk == 6) a.sound(SoundEvents.ROOTED_DIRT_BREAK, 2f, 0.4f);
            if (tk == 14 || tk == 24 || tk == 34) {
                Vec3 c = t.position().add(t.getDeltaMovement().scale(4));
                a.spike(c.x, c.z, t.getY(), 8, 26, a.dmg(1.0f), 2.4f);
                for (int i = 0; i < 3; i++) { double ang = Math.PI * 2 * i / 3 + tk; a.spike(c.x + Math.cos(ang) * 1.2, c.z + Math.sin(ang) * 1.2, t.getY(), 10, 24, a.dmg(0.7f), 1.5f); }
                FpeUtil.particles(a, ParticleTypes.SQUID_INK, c, 12, 0.6, 0.1, 0.6, 0.05);
                a.sound(SoundEvents.ROOTED_DIRT_BREAK, 1.5f, 0.6f);
            }
        }));
        // snatches the target with the branch hand, crushes it twice and slams it down
        out.add(f2("branch_grab", 60, 120).range(0, 8).weight(2).faceUntil(16).start((e, t, tk) -> ((LordHansel) e).holding = false).tick((e, t, tk) -> {
            LordHansel a = (LordHansel) e;
            if (tk == 18 && a.inFront(t, 7.0, 45) && FpeUtil.hit(a, t, a.dmg(0.6f), 0, 0)) { a.holding = true; a.sound(SoundEvents.WOOD_BREAK, 2f, 0.5f); }
            if (!a.holding) return;
            if (tk > 18 && tk < 48) holdAt(t, a.position().add(FpeUtil.forward(a).scale(3.0)).add(0, 3 + 3.5 * Math.min(1, (tk - 18) / 10.0), 0));
            if (tk == 30 || tk == 38) {
                FpeUtil.hit(a, t, a.dmg(0.8f), 0, 0);
                FpeUtil.particles(a, ParticleTypes.CRIT, chest(t), 15, 0.4, 0.4, 0.4, 0.2);
                a.sound(SoundEvents.SKELETON_HURT, 1f, 0.4f);
            }
            if (tk == 48) {
                a.holding = false;
                t.setDeltaMovement(0, -1.6, 0); t.hurtMarked = true;
                FpeUtil.hit(a, t, a.dmg(1.4f), 1.4, 0.3);
                Vec3 p = FpeUtil.ahead(a, 3.5, 0);
                FpeUtil.fx(a, FpeFx.Kind.RING_SHOCK, new Vec3(p.x, a.groundY(p.x, p.z, a.getY()) + 0.1, p.z), 0, 10, 6f, a.dmg(0.4f));
                a.sound(SoundEvents.GENERIC_EXPLODE, 2f, 0.6f);
            }
        }));
        // whips his head: the red flame-hair lashes forward as a sweeping fire cone
        out.add(f2("flame_hair", 50, 100).range(0, 11).weight(3).faceUntil(36).tick((e, t, tk) -> {
            LordHansel a = (LordHansel) e;
            if (tk == 6) a.sound(SoundEvents.BLAZE_SHOOT, 2f, 0.5f);
            if (tk >= 16 && tk <= 38) {
                Vec3 head = a.position().add(0, 7.0, 0);
                for (int i = 0; i < 3; i++) {
                    Vec3 d = FpeUtil.forward(a).yRot((float) ((a.random.nextDouble() - 0.5) * 1.2)).add(0, -0.45, 0).normalize();
                    FpeUtil.particles(a, ParticleTypes.FLAME, head.add(d.scale(2 + a.random.nextDouble() * 7)), 3, 0.4, 0.4, 0.4, 0.02);
                    FpeUtil.particles(a, RED, head.add(d.scale(2 + a.random.nextDouble() * 7)), 2, 0.4, 0.4, 0.4, 0.02);
                }
                if ((tk - 16) % 4 == 0) { a.fireCone(10, 45, a.dmg(0.45f)); a.sound(SoundEvents.FIRECHARGE_USE, 1.2f, 0.6f); }
            }
        }));
        // flings both arms up: thorns rain out of the ground all around the target
        out.add(f2("thorn_rain", 64, 130).range(0, 22).weight(2).blind().tick((e, t, tk) -> {
            LordHansel a = (LordHansel) e;
            if (tk == 10) a.sound(SoundEvents.WITHER_AMBIENT, 2f, 0.4f);
            if (tk >= 20 && tk <= 56 && tk % 3 == 0) {
                double x, z;
                if (tk % 9 == 0) { x = t.getX() + t.getDeltaMovement().x * 6; z = t.getZ() + t.getDeltaMovement().z * 6; }
                else { double ang = a.random.nextDouble() * Math.PI * 2, r = a.random.nextDouble() * 6; x = t.getX() + Math.cos(ang) * r; z = t.getZ() + Math.sin(ang) * r; }
                a.spike(x, z, t.getY(), 12, 40, a.dmg(0.75f), 1.3f + a.random.nextFloat() * 1.2f);
                FpeUtil.particles(a, ParticleTypes.SQUID_INK, new Vec3(x, t.getY() + 5, z), 6, 0.2, 2.5, 0.2, 0);
            }
        }));
        // a ring of tall thorn-trees closes around the target, then a root bursts in the middle
        out.add(f2("forest_cage", 50, 140).range(3, 18).weight(2).blind().tick((e, t, tk) -> {
            LordHansel a = (LordHansel) e;
            if (tk == 6) a.sound(SoundEvents.ROOTED_DIRT_PLACE, 2f, 0.4f);
            if (tk == 16) { Vec3 c = t.position(); for (int i = 0; i < 12; i++) { double ang = Math.PI * 2 * i / 12; a.spike(c.x + Math.cos(ang) * 3.2, c.z + Math.sin(ang) * 3.2, c.y, 2, 60, a.dmg(0.6f), 2.6f); } a.flag = false; }
            if (tk == 32) { Vec3 c = t.position(); a.tentacle(c.x, c.z, c.y, 4, 40, 1.8f, a.dmg(0.7f)); a.spike(c.x, c.z, c.y, 8, 24, a.dmg(1.2f), 2.8f); a.sound(SoundEvents.EVOKER_FANGS_ATTACK, 2f, 0.4f); }
        }));
        // quick stomp for anything under his feet
        out.add(f2("stomp", 30, 40).range(0, 5).weight(3).tick((e, t, tk) -> {
            LordHansel a = (LordHansel) e;
            if (tk == 13) {
                FpeUtil.hitRadius(a, FpeUtil.ahead(a, 1.5, 0), 3.6, a.dmg(1.3f), 1.5, 0.5);
                FpeUtil.fx(a, FpeFx.Kind.RING_SHOCK, a.position().add(0, 0.1, 0), 0, 10, 6f, a.dmg(0.4f));
                a.sound(SoundEvents.WARDEN_STEP, 3f, 0.4f);
                a.sound(SoundEvents.GENERIC_EXPLODE, 1f, 0.7f);
            }
        }));
        // starving Windeigo roar: darkness + hunger, drags victims a step closer
        out.add(f2("hunger_roar", 50, 200).range(0, 16).weight(1).blind().tick((e, t, tk) -> {
            LordHansel a = (LordHansel) e;
            if (tk == 18) {
                a.sound(SoundEvents.WARDEN_ROAR, 4f, 0.6f);
                FpeUtil.particles(a, ParticleTypes.SONIC_BOOM, a.position().add(0, 6.5, 0).add(FpeUtil.forward(a).scale(2)), 3, 1, 0.5, 1, 0);
                FpeUtil.fx(a, FpeFx.Kind.RING_SHOCK, a.position().add(0, 0.1, 0), 0, 16, 12f, a.dmg(0.5f));
                for (LivingEntity v : FpeUtil.enemiesInRadius(a, a.position(), 16, 6, 4)) {
                    v.addEffect(new MobEffectInstance(MobEffects.DARKNESS, 120, 0));
                    v.addEffect(new MobEffectInstance(MobEffects.HUNGER, 200, 2));
                    v.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 60, 1));
                    FpeUtil.knock(v, v.position().add(v.position().subtract(a.position())), 0.6, 0.2); // pulled toward him
                }
            }
        }));
        // ENRAGED: the whole forest wakes - tendril cage, three root rings, then a world-shaking double slam
        out.add(Ability.of("windeigo_feast", 86, 300).when(e -> form(e, 2) && e.isEnraged()).range(0, 18).weight(4).blind().tick((e, t, tk) -> {
            LordHansel a = (LordHansel) e;
            if (tk == 4) { a.sound(SoundEvents.WARDEN_ROAR, 4f, 0.4f); a.sound(SoundEvents.WITHER_SPAWN, 1.5f, 0.5f); }
            if (tk == 20) {
                Vec3 c = t.position();
                a.tentacle(c.x, c.z, c.y, 8, 80, 1.8f, a.dmg(0.6f));
                for (int i = 0; i < 8; i++) { double ang = Math.PI * 2 * i / 8; a.tentacle(c.x + Math.cos(ang) * 3, c.z + Math.sin(ang) * 3, c.y, 10 + i, 80, 1.5f, a.dmg(0.5f)); }
            }
            if (tk == 34) a.spikeRing(a.position(), 4.0, 12, 3, 2.0f, 0);
            if (tk == 42) a.spikeRing(a.position(), 7.0, 20, 3, 2.4f, 0.5f);
            if (tk == 50) a.spikeRing(a.position(), 10.0, 28, 3, 2.8f, 0.25f);
            if (tk == 66) {
                Vec3 p = FpeUtil.ahead(a, 4.5, 0);
                FpeUtil.hitRadius(a, p, 5.5, a.dmg(2.2f), 2.0, 0.8);
                FpeUtil.fx(a, FpeFx.Kind.RING_SHOCK, a.position().add(0, 0.1, 0), 0, 20, 15f, a.dmg(0.8f));
                FpeUtil.particles(a, ParticleTypes.EXPLOSION_EMITTER, p, 1, 0, 0, 0, 0);
                FpeUtil.particles(a, ParticleTypes.FLAME, p, 60, 3, 0.5, 3, 0.2);
                a.sound(SoundEvents.GENERIC_EXPLODE, 3f, 0.4f);
            }
        }));
    }
}
