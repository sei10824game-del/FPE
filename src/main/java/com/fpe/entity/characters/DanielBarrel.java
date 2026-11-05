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
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.level.ClipContext;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.Vec3;

/**
 * Daniel F. Barrel (FPE: Advanced Class) - two-form boss, faction OUTSIDER.
 * Form 1 "Matured" (variant 0, docs/ref/confirmed/daniel_barrel_matured.png): lanky suited bat-demon, rifle arm, whip tail, fangs, small bat wings.
 *   rifle_burst, rifle_bash, tail_whip, fang_bite (lifesteal), wing_dash, tail_snare, mag_dump, bat_swarm, hazard_zone, screech, piercing_round.
 * At <=50 % hp he is forced into an invulnerable "transform" (sparking rifle arm, kneels, rebuilt) and becomes
 * Form 2 "Cyborg Armed" (variant 1, daniel_barrel_cyborg.png): faster, armoured, huge tech-arm cannon, goggles, glowing chest plates.
 *   cannon_shot, gatling, rocket_salvo, tail_pierce, tail_spin, tech_smash, jet_dash, goggle_laser, emp_pulse, grenade_lob, hazard_strike,
 *   overdrive (enraged <25 % only).
 * Hit ticks match the animations in tools/bbgen/chars/daniel_barrel.py. Transformation state == variant (saved by FpeEntity), happens once.
 */
public class DanielBarrel extends FpeEntity {
    /** transform timeline (ticks of the "transform" ability): matured model plays 0-90, cyborg model 90-130 */
    public static final int T_FLIP = 90, T_ROAR = 112, T_END = 130;

    private static final ParticleOptions RED = new DustParticleOptions(new Vector3f(1f, 0.15f, 0.2f), 1.6f);
    private static final ParticleOptions PINK = new DustParticleOptions(new Vector3f(1f, 0.45f, 0.55f), 1.4f);
    private static final ParticleOptions WARN = new DustParticleOptions(new Vector3f(1f, 0.85f, 0.1f), 1.3f);

    private int transformT;
    private boolean holding, flag;
    private Vec3 beamDir = Vec3.ZERO;

    public DanielBarrel(EntityType<? extends FpeEntity> type, Level level) { super(type, level); }

    @Override public Faction faction() { return Faction.OUTSIDER; }

    public static AttributeSupplier.Builder attributes() { return baseAttributes(460, 8, 0.33, 6, 0.4); }

    // ------------------------------------------------------------------ form / boss plumbing
    private static boolean phase(FpeEntity e, int v) { return e.getVariant() == v && ((DanielBarrel) e).transformT == 0; }
    private static Ability p1(String id, int dur, int cd) { return Ability.of(id, dur, cd).when(e -> phase(e, 0)); }
    private static Ability p2(String id, int dur, int cd) { return Ability.of(id, dur, cd).when(e -> phase(e, 1)); }

    @Override protected boolean hasBossBar() { return true; }
    @Override protected BossEvent.BossBarColor bossColor() { return getVariant() == 1 ? BossEvent.BossBarColor.PINK : BossEvent.BossBarColor.WHITE; }
    @Override public boolean isEnraged() { return getVariant() == 1 && getHealth() < getMaxHealth() * 0.25f; }
    @Override public double preferredDistance() { return getVariant() == 1 ? 6.0 : 3.0; }
    @Override protected int restTicks() { return getVariant() == 0 ? 14 : isEnraged() ? 6 : 10; }

    @Override
    public boolean causeFallDamage(float dist, float mult, DamageSource src) { return false; }

    @Override
    public boolean hurt(DamageSource s, float amount) {
        boolean bypass = s.is(DamageTypeTags.BYPASSES_INVULNERABILITY);
        if (transformT > 0 && !bypass) return false;
        if (getVariant() == 0 && !bypass) // form 1 can't skip the transformation with one huge hit
            amount = Math.min(amount, Math.max(0.5f, getHealth() - getMaxHealth() * 0.5f + 0.5f));
        return super.hurt(s, amount);
    }

    @Override
    public void tick() {
        super.tick();
        if (level().isClientSide || !isAlive()) return;
        if (getVariant() == 1 && transformT == 0 && getAttribute(Attributes.MOVEMENT_SPEED).getBaseValue() < 0.38) cyborgStats(); // after a reload
        if (transformT == 0 && getVariant() == 0 && getHealth() <= getMaxHealth() * 0.5f) {
            transformT = 1;
            forceAbility("transform");
            sound(SoundEvents.IRON_GOLEM_DAMAGE, 1.5f, 0.6f);
        }
        if (transformT > 0) transformTick(transformT++);
    }

    private void transformTick(int t) {
        Vec3 c = position();
        setDeltaMovement(0, getDeltaMovement().y, 0);
        if (t < T_FLIP) {
            Vec3 arm = c.add(0, 1.3, 0).subtract(FpeUtil.right(this).scale(0.3));
            if (t % 2 == 0) FpeUtil.particles(this, ParticleTypes.ELECTRIC_SPARK, arm, 4 + t / 10, 0.3, 0.5, 0.3, 0.2);
            if (t % 5 == 0) FpeUtil.particles(this, ParticleTypes.SMOKE, c.add(0, 1, 0), 6, 0.4, 0.6, 0.4, 0.02);
            if (t % 20 == 0) sound(SoundEvents.BEACON_AMBIENT, 2f, 0.6f + t / 120f);
            if (t == 10 || t == 24 || t == 62) { sound(SoundEvents.ANVIL_LAND, 1f, 1.4f); FpeUtil.particles(this, ParticleTypes.LAVA, arm, 6, 0.2, 0.2, 0.2, 0); }
            if (t == 40) { sound(SoundEvents.IRON_GOLEM_HURT, 2f, 0.5f); FpeUtil.arc(this, ParticleTypes.LARGE_SMOKE, c.add(0, 0.1, 0), 0, 180, 3, 24); }
            if (t == 80) { sound(SoundEvents.BEACON_POWER_SELECT, 3f, 0.8f); FpeUtil.particles(this, PINK, c.add(0, 1.4, 0), 60, 0.6, 1, 0.6, 0.1); }
        }
        if (t == T_FLIP) {
            setVariant(1);
            setHealth(getMaxHealth() * 0.65f);
            cyborgStats();
            FpeUtil.particles(this, ParticleTypes.FLASH, c.add(0, 1.4, 0), 1, 0, 0, 0, 0);
            FpeUtil.particles(this, ParticleTypes.ELECTRIC_SPARK, c.add(0, 1.4, 0), 80, 0.8, 1.2, 0.8, 0.5);
            sound(SoundEvents.ANVIL_USE, 2f, 0.5f);
        }
        if (t > T_FLIP && t < T_ROAR && t % 3 == 0) FpeUtil.particles(this, PINK, c.add(0, 1.4, 0), 6, 0.4, 0.4, 0.4, 0.02);
        if (t == T_ROAR) {
            sound(SoundEvents.WARDEN_SONIC_BOOM, 2f, 1.2f);
            sound(SoundEvents.GENERIC_EXPLODE, 2f, 0.8f);
            FpeUtil.particles(this, ParticleTypes.EXPLOSION_EMITTER, c.add(0, 1, 0), 1, 0, 0, 0, 0);
            FpeUtil.fx(this, FpeFx.Kind.RING_SHOCK, c.add(0, 0.1, 0), 0, 18, 10f, dmg(0.6f));
            FpeUtil.hitRadius(this, c, 5, dmg(0.7f), 2.0, 0.5);
            for (LivingEntity v : FpeUtil.enemiesInRadius(this, c, 12, 4, 3)) v.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 60, 1));
        }
        if (t >= T_END) transformT = 0;
    }

    /** Cyborg Armed: faster, armoured */
    private void cyborgStats() {
        getAttribute(Attributes.MOVEMENT_SPEED).setBaseValue(0.38);
        getAttribute(Attributes.ARMOR).setBaseValue(12);
        getAttribute(Attributes.KNOCKBACK_RESISTANCE).setBaseValue(0.8);
    }

    // ------------------------------------------------------------------ sounds
    @Override protected SoundEvent getAmbientSound() { return getVariant() == 1 ? SoundEvents.BEACON_AMBIENT : SoundEvents.BAT_AMBIENT; }
    @Override protected SoundEvent getHurtSound(DamageSource s) { return getVariant() == 1 ? SoundEvents.IRON_GOLEM_HURT : SoundEvents.BAT_HURT; }
    @Override protected SoundEvent getDeathSound() { return getVariant() == 1 ? SoundEvents.IRON_GOLEM_DEATH : SoundEvents.BAT_DEATH; }
    @Override protected void playStepSound(BlockPos pos, BlockState st) {
        if (getVariant() == 1) playSound(SoundEvents.NETHERITE_BLOCK_STEP, 0.8f, 0.8f); else super.playStepSound(pos, st);
    }
    @Override public float getVoicePitch() { return getVariant() == 1 ? 0.8f : 0.7f; }

    private void sound(SoundEvent s, float vol, float pitch) { FpeUtil.sound(this, s, vol, pitch); }

    // ------------------------------------------------------------------ helpers
    private double groundY(double x, double z, double refY) {
        BlockPos.MutableBlockPos p = new BlockPos.MutableBlockPos(x, refY + 3, z);
        for (int i = 0; i < 10; i++, p.move(0, -1, 0)) {
            BlockPos b = p.below();
            if (level().getBlockState(p).getCollisionShape(level(), p).isEmpty() && !level().getBlockState(b).getCollisionShape(level(), b).isEmpty()) return p.getY();
        }
        return refY;
    }

    /** muzzle of the weapon arm (LEFT arm) when it is levelled at the target */
    private Vec3 muzzle() {
        double reach = getVariant() == 1 ? 1.4 : 1.75;
        return position().add(0, 1.85, 0).subtract(FpeUtil.right(this).scale(0.28)).add(FpeUtil.forward(this).scale(reach));
    }

    private void arcFx(double up, float radius, float sweep, float tilt, int color) {
        FpeFx f = FpeUtil.fx(this, FpeFx.Kind.ARC, position().add(0, up, 0), 0, 8, radius, 0).param(sweep).color(color);
        f.setYRot(getYRot()); f.yRotO = f.getYRot();
        f.setXRot(tilt); f.xRotO = tilt;
    }

    private void lineParticles(ParticleOptions p, Vec3 a, Vec3 b, double step) {
        Vec3 d = b.subtract(a);
        int n = (int) Math.max(1, d.length() / step);
        for (int i = 0; i <= n; i++) FpeUtil.particles(this, p, a.add(d.scale(i / (double) n)), 1, 0.05, 0.05, 0.05, 0);
    }

    private void shoot(LivingEntity t, FpeProjectile.Kind k, double speed, double spread, float dmg) {
        Vec3 from = muzzle();
        Vec3 v = FpeUtil.aim(from, t, speed, 0.25).add((random.nextDouble() - 0.5) * spread, (random.nextDouble() - 0.5) * spread * 0.5, (random.nextDouble() - 0.5) * spread);
        FpeUtil.projectile(this, k, from, v, dmg);
        FpeUtil.particles(this, ParticleTypes.SMOKE, from, 3, 0.05, 0.05, 0.05, 0.02);
    }

    /** a hazard sigil: warning-sign trap that bursts after warmup */
    private void sigil(double x, double z, double refY, int warm, float r, float dmg) {
        Vec3 p = new Vec3(x, groundY(x, z, refY) + 0.05, z);
        FpeUtil.fx(this, FpeFx.Kind.RING_TRAP, p, warm, 14, r, dmg);
        FpeUtil.particles(this, WARN, p.add(0, 0.2, 0), 12, r * 0.4, 0.05, r * 0.4, 0);
    }

    private static Vec3 chest(LivingEntity t) { return t.position().add(0, t.getBbHeight() * 0.6, 0); }
    private boolean inFront(LivingEntity t, double range, double halfDeg) {
        Vec3 d = new Vec3(t.getX() - getX(), 0, t.getZ() - getZ());
        if (d.length() - getBbWidth() * 0.5 - t.getBbWidth() * 0.5 > range) return false;
        return d.lengthSqr() < 0.01 || Math.toDegrees(Math.acos(Math.max(-1, Math.min(1, d.normalize().dot(FpeUtil.forward(this)))))) <= halfDeg;
    }
    private static void holdAt(LivingEntity v, Vec3 p) {
        v.setDeltaMovement(p.subtract(v.position()).scale(0.6));
        v.hurtMarked = true;
        v.fallDistance = 0;
    }
    /** tail strike: a lash from the hips toward the target */
    private boolean tailLine(LivingEntity t, double len, double radius, float dmg, double knock, double up) {
        Vec3 from = position().add(0, 2.1, 0).add(FpeUtil.right(this).scale(0.4)); // tail comes over the right shoulder
        Vec3 to = from.add(chest(t).subtract(from).normalize().scale(len));
        lineParticles(ParticleTypes.SQUID_INK, from, to, 0.45);
        sound(SoundEvents.PLAYER_ATTACK_SWEEP, 1f, 1.6f);
        return FpeUtil.hitLine(this, from, to, radius, dmg, knock, up) > 0;
    }

    // ------------------------------------------------------------------ abilities
    @Override
    protected void registerAbilities(List<Ability> out) {
        // ======================= FORM 1: MATURED =======================
        // 1. levels the rifle arm and fires a three-round burst
        out.add(p1("rifle_burst", 34, 45).range(3, 18).weight(3).faceUntil(20).tick((e, t, tk) -> {
            DanielBarrel a = (DanielBarrel) e;
            if (tk == 6) a.sound(SoundEvents.CROSSBOW_LOADING_END, 1f, 0.7f);
            if (tk == 14 || tk == 17 || tk == 20) {
                a.shoot(t, FpeProjectile.Kind.BULLET, 2.2, 0.06, a.dmg(0.7f));
                a.sound(SoundEvents.GENERIC_EXPLODE, 0.5f, 1.9f);
                FpeUtil.particles(a, ParticleTypes.FLAME, a.muzzle(), 3, 0.05, 0.05, 0.05, 0.02);
            }
        }));
        // 2. horizontal rifle-butt swing
        out.add(p1("rifle_bash", 28, 35).range(0, 3.6).weight(3).faceUntil(9).tick((e, t, tk) -> {
            DanielBarrel a = (DanielBarrel) e;
            if (tk == 6) a.sound(SoundEvents.ARMOR_EQUIP_IRON, 1f, 0.6f);
            if (tk == 11) {
                if (FpeUtil.hitCone(a, 3.4, 80, a.dmg(1.25f), 1.2, 0.35) > 0) a.sound(SoundEvents.ANVIL_LAND, 0.6f, 1.6f);
                a.arcFx(1.3, 3.2f, 150, 10, 0xCC3A3A44);
                a.sound(SoundEvents.PLAYER_ATTACK_SWEEP, 1f, 0.8f);
            }
        }));
        // 3. tail rears over the shoulder and cracks down like a whip
        out.add(p1("tail_whip", 30, 40).range(1.5, 5.5).weight(3).faceUntil(11).tick((e, t, tk) -> {
            DanielBarrel a = (DanielBarrel) e;
            if (tk == 6) a.sound(SoundEvents.PHANTOM_FLAP, 0.8f, 1.4f);
            if (tk == 13) {
                a.tailLine(t, 5.5, 0.6, a.dmg(1.05f), 0.6, 0.2);
                a.sound(SoundEvents.FISHING_BOBBER_RETRIEVE, 1.2f, 1.8f);
                FpeUtil.particles(a, ParticleTypes.CRIT, chest(t), 8, 0.3, 0.3, 0.3, 0.2);
            }
        }));
        // 4. vampire lunge: fangs sink in, drains health, shoves the victim off
        out.add(p1("fang_bite", 32, 80).range(0, 4.5).weight(2).faceUntil(8).start((e, t, tk) -> ((DanielBarrel) e).holding = false).tick((e, t, tk) -> {
            DanielBarrel a = (DanielBarrel) e;
            if (tk == 7) a.dashToward(t.position(), 0.75, 0.1);
            if (tk == 12 && a.inFront(t, 2.2, 55) && FpeUtil.hit(a, t, a.dmg(0.8f), 0, 0)) {
                a.holding = true; a.heal(a.dmg(0.6f));
                a.sound(SoundEvents.PHANTOM_BITE, 1.2f, 0.8f);
                FpeUtil.particles(a, ParticleTypes.DAMAGE_INDICATOR, chest(t), 6, 0.3, 0.3, 0.3, 0.1);
            }
            if (!a.holding) return;
            if (tk > 12 && tk < 24) holdAt(t, FpeUtil.ahead(a, 1.0, 0.1));
            if (tk == 18) {
                FpeUtil.hit(a, t, a.dmg(0.4f), 0, 0); a.heal(a.dmg(0.5f));
                FpeUtil.particles(a, RED, chest(t), 12, 0.3, 0.3, 0.3, 0.05);
                a.sound(SoundEvents.HONEY_DRINK, 1f, 0.6f);
            }
            if (tk == 24) { a.holding = false; FpeUtil.knock(t, a.position(), 1.2, 0.35); }
        }));
        // 5. wings snap back, flat dash past the target with a claw rake
        out.add(p1("wing_dash", 30, 60).range(3.5, 12).weight(2).faceUntil(7).tick((e, t, tk) -> {
            DanielBarrel a = (DanielBarrel) e;
            if (tk == 7) { a.dashToward(t.position(), 1.4, 0.12); a.sound(SoundEvents.PHANTOM_SWOOP, 1.2f, 1.2f); }
            if (tk > 7 && tk < 13) FpeUtil.particles(a, ParticleTypes.SQUID_INK, a.position().add(0, 1, 0), 2, 0.2, 0.4, 0.2, 0.01);
            if (tk == 11) {
                FpeUtil.hitCone(a, 2.8, 70, a.dmg(1.1f), 0.8, 0.25);
                a.arcFx(1.4, 2.6f, 130, -30, 0xDD1A1720);
                a.sound(SoundEvents.PLAYER_ATTACK_SWEEP, 1f, 1.3f);
            }
            if (tk == 14) a.setDeltaMovement(a.getDeltaMovement().scale(0.2));
        }));
        // 6. long tail lash that snares the target and yanks it in
        out.add(p1("tail_snare", 36, 70).range(3, 9).weight(2).faceUntil(11).start((e, t, tk) -> ((DanielBarrel) e).flag = false).tick((e, t, tk) -> {
            DanielBarrel a = (DanielBarrel) e;
            if (tk == 12 && a.tailLine(t, 9, 0.6, a.dmg(0.6f), 0, 0)) a.flag = true;
            if (tk == 20 && a.flag) {
                Vec3 d = a.position().subtract(t.position());
                Vec3 v = new Vec3(d.x, 0, d.z).normalize().scale(Math.min(1.7, d.length() * 0.25));
                t.setDeltaMovement(v.x, 0.35, v.z); t.hurtMarked = true;
                t.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 40, 1));
                a.sound(SoundEvents.FISHING_BOBBER_RETRIEVE, 1.2f, 0.6f);
            }
        }));
        // 7. braced full-auto sweep, then a reload slap
        out.add(p1("mag_dump", 50, 110).range(4, 16).weight(2).faceUntil(12).tick((e, t, tk) -> {
            DanielBarrel a = (DanielBarrel) e;
            if (tk >= 14 && tk <= 38 && tk % 2 == 0) {
                float yaw = a.getYRot() + (30f - (tk - 14) * 2.5f);
                Vec3 dir = Vec3.directionFromRotation(0, yaw);
                Vec3 from = a.muzzle();
                Vec3 aim = FpeUtil.aim(from, t, 2.0, 0.1);
                Vec3 v = new Vec3(dir.x * 2.0, aim.y, dir.z * 2.0).add(aim.scale(0.35)).normalize().scale(2.0);
                FpeUtil.projectile(a, FpeProjectile.Kind.BULLET, from, v, a.dmg(0.4f));
                a.sound(SoundEvents.GENERIC_EXPLODE, 0.35f, 2f);
            }
            if (tk == 41) a.sound(SoundEvents.CROSSBOW_LOADING_START, 1f, 0.8f);
            if (tk == 44) a.sound(SoundEvents.CROSSBOW_LOADING_END, 1.2f, 0.6f);
        }));
        // 8. wing beats release a swarm of homing bats
        out.add(p1("bat_swarm", 38, 90).range(5, 20).weight(2).tick((e, t, tk) -> {
            DanielBarrel a = (DanielBarrel) e;
            if (tk == 10) a.sound(SoundEvents.BAT_TAKEOFF, 2f, 0.7f);
            if (tk == 14 || tk == 17 || tk == 20 || tk == 23) {
                int i = (tk - 14) / 3;
                Vec3 from = a.position().add(0, 2.0, 0).add(FpeUtil.right(a).scale(i % 2 == 0 ? 1.1 : -1.1)).subtract(FpeUtil.forward(a).scale(0.3));
                FpeUtil.projectile(a, FpeProjectile.Kind.SHADOW_ORB, from, FpeUtil.aim(from, t, 0.6, 0.2).add(0, 0.12, 0), a.dmg(0.55f));
                FpeUtil.particles(a, ParticleTypes.SQUID_INK, from, 8, 0.3, 0.3, 0.3, 0.05);
                a.sound(SoundEvents.BAT_AMBIENT, 1.4f, 0.8f + i * 0.1f);
            }
        }));
        // 9. rams the rifle into the ground: warning sigils arm under and around the target
        out.add(p1("hazard_zone", 34, 100).range(2, 14).weight(2).blind().tick((e, t, tk) -> {
            DanielBarrel a = (DanielBarrel) e;
            if (tk == 14) {
                a.sound(SoundEvents.ANVIL_LAND, 1.2f, 0.7f);
                FpeUtil.fx(a, FpeFx.Kind.RING_SHOCK, a.position().add(0, 0.1, 0), 0, 8, 3f, a.dmg(0.4f));
                Vec3 c = t.position();
                a.sigil(c.x, c.z, c.y, 18, 2.2f, a.dmg(1.1f));
                for (int i = 0; i < 3; i++) {
                    double ang = Math.PI * 2 * i / 3 + a.random.nextDouble();
                    a.sigil(c.x + Math.cos(ang) * 3, c.z + Math.sin(ang) * 3, c.y, 24 + i * 3, 1.8f, a.dmg(0.9f));
                }
                a.sound(SoundEvents.NOTE_BLOCK_BIT.value(), 1.5f, 1.8f);
            }
        }));
        // 10. bat screech: knockback, nausea, slowness
        out.add(p1("screech", 34, 110).range(0, 6).weight(1).tick((e, t, tk) -> {
            DanielBarrel a = (DanielBarrel) e;
            if (tk == 14) {
                a.sound(SoundEvents.BAT_HURT, 3f, 0.4f);
                a.sound(SoundEvents.VEX_CHARGE, 2f, 0.6f);
                FpeUtil.particles(a, ParticleTypes.SONIC_BOOM, a.position().add(0, 1.8, 0), 1, 0, 0, 0, 0);
                for (int r = 2; r <= 6; r += 2) FpeUtil.arc(a, ParticleTypes.NOTE, a.position().add(0, 1.4, 0), 0, 180, r, 8 + r * 3);
                FpeUtil.hitRadius(a, a.position(), 6, a.dmg(0.5f), 1.8, 0.5);
                for (LivingEntity v : FpeUtil.enemiesInRadius(a, a.position(), 7, 3, 1)) {
                    v.addEffect(new MobEffectInstance(MobEffects.CONFUSION, 100, 0));
                    v.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 60, 1));
                }
            }
        }));
        // 11. signature: kneels, long laser-sighted aim, one piercing high-calibre round
        out.add(p1("piercing_round", 44, 140).range(6, 26).weight(2).faceUntil(25).tick((e, t, tk) -> {
            DanielBarrel a = (DanielBarrel) e;
            Vec3 from = a.muzzle();
            if (tk >= 8 && tk < 28 && tk % 2 == 0) a.lineParticles(RED, from, from.add(chest(t).subtract(from).normalize().scale(Math.min(20, a.distanceTo(t)))), 1.2);
            if (tk == 8) a.sound(SoundEvents.CROSSBOW_QUICK_CHARGE_3, 1.2f, 0.5f);
            if (tk == 28) {
                Vec3 dir = chest(t).subtract(from).normalize();
                Vec3 end = a.level().clip(new ClipContext(from, from.add(dir.scale(28)), ClipContext.Block.COLLIDER, ClipContext.Fluid.NONE, a)).getLocation();
                FpeUtil.hitLine(a, from, end, 0.7, a.dmg(2.2f), 1.6, 0.3);
                a.lineParticles(ParticleTypes.CRIT, from, end, 0.4);
                a.lineParticles(ParticleTypes.SMOKE, from, end, 1.0);
                FpeUtil.particles(a, ParticleTypes.EXPLOSION, end, 1, 0, 0, 0, 0);
                a.sound(SoundEvents.GENERIC_EXPLODE, 1.5f, 1.3f);
                a.sound(SoundEvents.TRIDENT_THUNDER, 0.6f, 2f);
                FpeUtil.knock(a, end, 0.6, 0.1); // recoil skid
            }
        }));
        // forced by tick(): the transformation (logic in transformTick so it survives a lost target)
        out.add(Ability.of("transform", T_END, 0).when(e -> false).blind());

        // ======================= FORM 2: CYBORG ARMED =======================
        // 1. charged cannon blast (explosive)
        out.add(p2("cannon_shot", 34, 50).range(4, 22).weight(3).faceUntil(15).tick((e, t, tk) -> {
            DanielBarrel a = (DanielBarrel) e;
            if (tk == 9) a.sound(SoundEvents.BEACON_ACTIVATE, 1.2f, 1.6f);
            if (tk > 9 && tk < 16) FpeUtil.particles(a, PINK, a.muzzle(), 3, 0.15, 0.15, 0.15, 0.01);
            if (tk == 16) {
                a.shoot(t, FpeProjectile.Kind.ROCKET, 1.3, 0, a.dmg(1.3f));
                FpeUtil.particles(a, ParticleTypes.EXPLOSION, a.muzzle(), 1, 0, 0, 0, 0);
                a.sound(SoundEvents.GENERIC_EXPLODE, 1.5f, 1.1f);
            }
        }));
        // 2. gatling stream
        out.add(p2("gatling", 54, 90).range(4, 18).weight(3).faceUntil(42).tick((e, t, tk) -> {
            DanielBarrel a = (DanielBarrel) e;
            if (tk == 8) a.sound(SoundEvents.MINECART_RIDING, 1.5f, 2f);
            if (tk >= 12 && tk <= 42 && tk % 2 == 0) {
                a.shoot(t, FpeProjectile.Kind.BULLET, 2.3, 0.18, a.dmg(0.32f));
                a.sound(SoundEvents.GENERIC_EXPLODE, 0.3f, 2f);
            }
            if (tk == 46) { a.sound(SoundEvents.FIRE_EXTINGUISH, 1f, 1f); FpeUtil.particles(a, ParticleTypes.CLOUD, a.muzzle(), 8, 0.2, 0.2, 0.2, 0.05); }
        }));
        // 3. kneeling rocket salvo
        out.add(p2("rocket_salvo", 46, 120).range(7, 24).weight(2).faceUntil(28).tick((e, t, tk) -> {
            DanielBarrel a = (DanielBarrel) e;
            if (tk >= 14 && tk <= 29 && (tk - 14) % 3 == 0) {
                Vec3 from = a.position().add(0, 2.4, 0).subtract(FpeUtil.right(a).scale(0.4));
                Vec3 to = t.position().add((a.random.nextDouble() - 0.5) * 4, 0.5, (a.random.nextDouble() - 0.5) * 4);
                Vec3 v = to.subtract(from).normalize().scale(0.9).add(0, 0.12, 0);
                FpeUtil.projectile(a, FpeProjectile.Kind.ROCKET, from, v, a.dmg(0.8f));
                FpeUtil.particles(a, ParticleTypes.CAMPFIRE_COSY_SMOKE, from, 2, 0.1, 0.1, 0.1, 0.02);
                a.sound(SoundEvents.FIREWORK_ROCKET_LAUNCH, 1.5f, 0.7f);
            }
        }));
        // 4. tail spears forward twice over the shoulder
        out.add(p2("tail_pierce", 32, 40).range(1.5, 6.5).weight(3).faceUntil(19).tick((e, t, tk) -> {
            DanielBarrel a = (DanielBarrel) e;
            if (tk == 12 || tk == 20) {
                Vec3 from = a.position().add(0, 2.1, 0).add(FpeUtil.right(a).scale(0.4));
                Vec3 to = from.add(chest(t).subtract(from).normalize().scale(6.5));
                FpeUtil.hitLine(a, from, to, 0.55, a.dmg(0.95f), 0.5, 0.1);
                a.lineParticles(ParticleTypes.SQUID_INK, from, to, 0.5);
                a.sound(SoundEvents.TRIDENT_THROW, 1.2f, 0.8f);
            }
        }));
        // 5. spinning tail sweep around him
        out.add(p2("tail_spin", 32, 60).range(0, 4.5).weight(3).tick((e, t, tk) -> {
            DanielBarrel a = (DanielBarrel) e;
            if (tk == 11) a.sound(SoundEvents.PLAYER_ATTACK_SWEEP, 1.5f, 0.6f);
            if (tk == 14) {
                FpeUtil.hitRadius(a, a.position(), 4.6, a.dmg(1.15f), 1.6, 0.4);
                a.arcFx(0.9, 4.6f, 360, 0, 0xEE141218);
                FpeUtil.arc(a, ParticleTypes.SQUID_INK, a.position().add(0, 0.9, 0), 0, 180, 4.2, 30);
            }
        }));
        // 6. overhead tech-arm slam with shockwave
        out.add(p2("tech_smash", 38, 60).range(0, 5).weight(3).faceUntil(15).tick((e, t, tk) -> {
            DanielBarrel a = (DanielBarrel) e;
            if (tk == 8) a.sound(SoundEvents.PISTON_EXTEND, 1.2f, 0.5f);
            if (tk == 18) {
                Vec3 p = FpeUtil.ahead(a, 2.0, 0);
                FpeUtil.hitRadius(a, p, 2.8, a.dmg(1.7f), 1.2, 0.6);
                FpeUtil.fx(a, FpeFx.Kind.RING_SHOCK, new Vec3(p.x, a.groundY(p.x, p.z, a.getY()) + 0.1, p.z), 0, 12, 6f, a.dmg(0.6f));
                FpeUtil.particles(a, ParticleTypes.EXPLOSION, p, 2, 0.6, 0.1, 0.6, 0);
                FpeUtil.particles(a, ParticleTypes.ELECTRIC_SPARK, p, 30, 1, 0.2, 1, 0.3);
                a.sound(SoundEvents.ANVIL_LAND, 1.5f, 0.5f);
                a.sound(SoundEvents.GENERIC_EXPLODE, 1.2f, 0.8f);
            }
        }));
        // 7. jet dash: wing thrusters, tech-arm jab, launching uppercut
        out.add(p2("jet_dash", 34, 60).range(3.5, 14).weight(2).faceUntil(8).tick((e, t, tk) -> {
            DanielBarrel a = (DanielBarrel) e;
            if (tk == 8) { a.dashToward(t.position(), 1.5, 0.1); a.sound(SoundEvents.FIRECHARGE_USE, 1.2f, 0.6f); }
            if (tk > 8 && tk < 14) FpeUtil.particles(a, ParticleTypes.FLAME, a.position().add(0, 1.6, 0).subtract(FpeUtil.forward(a).scale(0.6)), 3, 0.3, 0.2, 0.3, 0.02);
            if (tk == 12) { FpeUtil.hitCone(a, 2.8, 60, a.dmg(0.9f), 0.2, 0.1); a.sound(SoundEvents.PLAYER_ATTACK_STRONG, 1f, 0.7f); }
            if (tk == 14) a.setDeltaMovement(a.getDeltaMovement().scale(0.2));
            if (tk == 20) {
                if (FpeUtil.hitCone(a, 3.0, 60, a.dmg(1.2f), 0.4, 1.1) > 0) a.sound(SoundEvents.PLAYER_ATTACK_KNOCKBACK, 1.2f, 0.6f);
                a.arcFx(1.2, 2.8f, 120, -80, 0xEEFF6070);
            }
        }));
        // 8. goggle laser: charges, then a tracking beam sweeps the target
        out.add(p2("goggle_laser", 62, 120).range(6, 24).weight(2).faceUntil(30).tick((e, t, tk) -> {
            DanielBarrel a = (DanielBarrel) e;
            Vec3 eye = a.getEyePosition().add(FpeUtil.forward(a).scale(0.4));
            if (tk < 30) {
                if (tk % 2 == 0) FpeUtil.particles(a, RED, eye, 3, 0.4, 0.4, 0.4, 0.02);
                if (tk == 4) a.sound(SoundEvents.BEACON_POWER_SELECT, 2f, 1.4f);
                return;
            }
            if (tk > 52) return;
            Vec3 want = chest(t).subtract(eye).normalize();
            a.beamDir = tk == 30 ? want : a.beamDir.add(want.subtract(a.beamDir).scale(0.1)).normalize();
            Vec3 end = a.level().clip(new ClipContext(eye, eye.add(a.beamDir.scale(24)), ClipContext.Block.COLLIDER, ClipContext.Fluid.NONE, a)).getLocation();
            float yaw = (float) Math.toDegrees(Math.atan2(a.beamDir.z, a.beamDir.x)) - 90f;
            a.setYRot(yaw); a.yBodyRot = yaw; a.yHeadRot = yaw;
            a.lineParticles(RED, eye, end, 0.6);
            FpeUtil.particles(a, ParticleTypes.LAVA, end, 1, 0.2, 0.1, 0.2, 0);
            if ((tk - 30) % 4 == 0) {
                FpeUtil.hitLine(a, eye, end, 0.6, a.dmg(0.4f), 0.2, 0.05);
                a.sound(SoundEvents.BEACON_AMBIENT, 1.5f, 2f);
            }
        }));
        // 9. EMP burst from the chest plates: shockwave, slowness + weakness
        out.add(p2("emp_pulse", 36, 110).range(0, 7).weight(2).blind().tick((e, t, tk) -> {
            DanielBarrel a = (DanielBarrel) e;
            if (tk == 4) a.sound(SoundEvents.BEACON_ACTIVATE, 2f, 0.6f);
            if (tk > 4 && tk < 16 && tk % 2 == 0) FpeUtil.particles(a, PINK, a.position().add(0, 1.6, 0), 6, 0.3, 0.3, 0.3, 0.05);
            if (tk == 16) {
                FpeUtil.fx(a, FpeFx.Kind.RING_SHOCK, a.position().add(0, 0.1, 0), 0, 14, 8f, a.dmg(0.5f));
                FpeUtil.hitRadius(a, a.position(), 6, a.dmg(0.8f), 1.8, 0.5);
                FpeUtil.particles(a, ParticleTypes.ELECTRIC_SPARK, a.position().add(0, 1.4, 0), 60, 2, 1, 2, 0.4);
                for (LivingEntity v : FpeUtil.enemiesInRadius(a, a.position(), 8, 3, 1)) {
                    v.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 80, 2));
                    v.addEffect(new MobEffectInstance(MobEffects.WEAKNESS, 80, 0));
                }
                a.sound(SoundEvents.BEACON_DEACTIVATE, 2f, 0.7f);
                a.sound(SoundEvents.LIGHTNING_BOLT_IMPACT, 0.8f, 1.6f);
            }
        }));
        // 10. mortar: three lobbed grenades
        out.add(p2("grenade_lob", 36, 80).range(5, 16).weight(2).faceUntil(20).tick((e, t, tk) -> {
            DanielBarrel a = (DanielBarrel) e;
            if (tk == 12 || tk == 16 || tk == 20) {
                Vec3 from = a.position().add(0, 2.6, 0).subtract(FpeUtil.right(a).scale(0.4));
                Vec3 to = t.position().add((a.random.nextDouble() - 0.5) * 3, 0, (a.random.nextDouble() - 0.5) * 3);
                Vec3 d = to.subtract(from);
                double h = Math.sqrt(d.x * d.x + d.z * d.z);
                Vec3 v = new Vec3(d.x, 0, d.z).normalize().scale(Math.min(1.2, h * 0.06 + 0.2)).add(0, 0.55, 0);
                FpeUtil.projectile(a, FpeProjectile.Kind.GRENADE, from, v, a.dmg(0.9f));
                a.sound(SoundEvents.DISPENSER_LAUNCH, 1.5f, 0.6f);
            }
        }));
        // 11. punches the ground: warning sigils ripple out around the target
        out.add(p2("hazard_strike", 44, 110).range(2, 16).weight(2).blind().tick((e, t, tk) -> {
            DanielBarrel a = (DanielBarrel) e;
            if (tk == 10) {
                a.sound(SoundEvents.ANVIL_LAND, 1.5f, 0.6f);
                FpeUtil.fx(a, FpeFx.Kind.RING_SHOCK, a.position().add(0, 0.1, 0), 0, 8, 3.5f, a.dmg(0.5f));
                Vec3 c = t.position();
                a.sigil(c.x, c.z, c.y, 14, 2.4f, a.dmg(1.2f));
                for (int i = 0; i < 5; i++) {
                    double ang = Math.PI * 2 * i / 5 + a.random.nextDouble() * 0.5;
                    a.sigil(c.x + Math.cos(ang) * 3.4, c.z + Math.sin(ang) * 3.4, c.y, 18 + i * 2, 2.0f, a.dmg(1.0f));
                }
            }
        }));
        // 12. ENRAGED: overdrive - rocket ring, spinning gatling, double slam
        out.add(Ability.of("overdrive", 80, 260).when(e -> phase(e, 1) && e.isEnraged()).range(0, 16).weight(4).blind().tick((e, t, tk) -> {
            DanielBarrel a = (DanielBarrel) e;
            if (tk == 2) { a.sound(SoundEvents.BEACON_ACTIVATE, 3f, 0.5f); a.sound(SoundEvents.WARDEN_SONIC_CHARGE, 2f, 1.4f); }
            if (tk < 30 && tk % 3 == 0) FpeUtil.particles(a, ParticleTypes.ELECTRIC_SPARK, a.position().add(0, 1.4, 0), 10, 0.6, 0.8, 0.6, 0.3);
            if (tk == 34) {
                for (int i = 0; i < 8; i++) {
                    double ang = Math.PI * 2 * i / 8;
                    Vec3 from = a.position().add(0, 2.2, 0);
                    FpeUtil.projectile(a, FpeProjectile.Kind.ROCKET, from, new Vec3(Math.cos(ang) * 0.8, 0.05, Math.sin(ang) * 0.8), a.dmg(0.8f));
                }
                FpeUtil.fx(a, FpeFx.Kind.RING_SHOCK, a.position().add(0, 0.1, 0), 0, 12, 6f, a.dmg(0.5f));
                a.sound(SoundEvents.FIREWORK_ROCKET_LARGE_BLAST, 2f, 0.6f);
            }
            if (tk >= 41 && tk <= 59 && tk % 2 == 1) {
                float yaw = a.getYRot() - (tk - 40) * 18f;
                Vec3 dir = Vec3.directionFromRotation(0, yaw);
                Vec3 from = a.position().add(0, 1.8, 0).add(dir.scale(1.3));
                FpeUtil.projectile(a, FpeProjectile.Kind.BULLET, from, dir.scale(2.0), a.dmg(0.4f));
                a.sound(SoundEvents.GENERIC_EXPLODE, 0.3f, 2f);
            }
            if (tk == 66) {
                Vec3 p = FpeUtil.ahead(a, 1.8, 0);
                FpeUtil.hitRadius(a, p, 5, a.dmg(2.0f), 2.0, 0.8);
                FpeUtil.fx(a, FpeFx.Kind.RING_SHOCK, a.position().add(0, 0.1, 0), 0, 18, 12f, a.dmg(0.8f));
                FpeUtil.particles(a, ParticleTypes.EXPLOSION_EMITTER, p, 1, 0, 0, 0, 0);
                a.sound(SoundEvents.GENERIC_EXPLODE, 3f, 0.5f);
            }
        }));
    }
}
