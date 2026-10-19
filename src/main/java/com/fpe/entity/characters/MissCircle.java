package com.fpe.entity.characters;

import java.util.List;

import com.fpe.entity.Ability;
import com.fpe.entity.FpeCombat;
import com.fpe.entity.FpeEntity;
import com.fpe.entity.FpeFx;
import com.fpe.entity.FpeUtil;

import net.minecraft.core.BlockPos;
import net.minecraft.core.particles.BlockParticleOption;
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
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.Vec3;

/**
 * Miss Circle (normal teacher, confirmed art docs/ref/confirmed/miss_circle.jpg). Giant steel drawing compass (needle + pencil leg),
 * black claw hand. Model + animations: assets/fpe/bbmodels/miss_circle.bbmodel (tools/bbgen/chars/miss_circle.py).
 * MELEE ONLY (she is never seen fighting at range): sweep, lunge, splitSlam, drawCircle, charge, hairWhip, scissorSnip, arcSlash,
 * impale (canon skewer + slam), devour (canon: grabs and bites failing students), pencilStab (bleeding stab flurry),
 * pounce (leaping needle plunge gap-closer), combo (rage), perfectCircle (rage signature).
 */
public class MissCircle extends FpeEntity {
    /** direction locked at the start of directional moves (slam crack lines) */
    private Vec3 lockDir = new Vec3(0, 0, 1);
    private Vec3 lockPos = Vec3.ZERO;
    /** victim held during "impale" / "devour" */
    private LivingEntity held;

    public MissCircle(EntityType<? extends FpeEntity> type, Level level) { super(type, level); }

    @Override public Faction faction() { return Faction.MISS; }

    @Override public boolean meleeFocus() { return true; }

    public static AttributeSupplier.Builder attributes() { return baseAttributes(90, 7, 0.3, 5, 0.4); }

    @Override public double preferredDistance() { return 2.5; }
    @Override protected SoundEvent getAmbientSound() { return SoundEvents.WITCH_AMBIENT; }
    @Override protected SoundEvent getHurtSound(DamageSource s) { return SoundEvents.WITCH_HURT; }
    @Override protected SoundEvent getDeathSound() { return SoundEvents.WITCH_DEATH; }
    @Override public float getVoicePitch() { return 0.8f; }

    // ------------------------------------------------------------------ helpers
    private static Vec3 rotY(Vec3 f, double deg) {
        double r = Math.toRadians(deg), c = Math.cos(r), s = Math.sin(r);
        return new Vec3(f.x * c - f.z * s, 0, f.x * s + f.z * c);
    }

    /** direction "deg" degrees toward her right of her facing (matches positive model yaw) */
    private static Vec3 dirRight(FpeEntity e, double deg) {
        double r = Math.toRadians(deg);
        return FpeUtil.forward(e).scale(Math.cos(r)).add(FpeUtil.right(e).scale(Math.sin(r)));
    }

    private static void debris(FpeEntity e, Vec3 at) {
        BlockState st = e.level().getBlockState(BlockPos.containing(at.x, at.y - 0.5, at.z));
        if (!st.isAir()) FpeUtil.particles(e, new BlockParticleOption(ParticleTypes.BLOCK, st), at.add(0, 0.2, 0), 14, 0.35, 0.15, 0.35, 0.15);
    }

    private void lockDir(FpeEntity e) { lockDir = FpeUtil.forward(e); lockPos = e.position(); }

    /** drag the held victim toward a point (server-side velocity, works on players too) */
    private void hold(Vec3 at) {
        if (held == null || !held.isAlive()) return;
        held.setDeltaMovement(at.subtract(held.position()).scale(0.6));
        held.hurtMarked = true;
        held.fallDistance = 0;
    }

    // ------------------------------------------------------------------ abilities
    @Override
    protected void registerAbilities(List<Ability> out) {
        // 1. 360° compass sweep
        out.add(Ability.of("sweep", 34, 70).range(0, 4.5).weight(4)
                .tick((e, t, k) -> {
                    if (k == 2) FpeUtil.sound(e, SoundEvents.ARMOR_EQUIP_IRON, 1f, 0.6f);
                    if (k == 13) FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_SWEEP, 1.4f, 0.7f);
                    if (k == 14) FpeUtil.fx(e, FpeFx.Kind.ARC, e.position().add(0, 1.0, 0), 0, 9, 4.6f, 0).param(360).color(0xFFE6E8F4);
                    if (k == 15) {
                        FpeUtil.hitRadius(e, e.position(), 4.6, e.dmg(1.5f), 1.1, 0.35);
                        FpeUtil.arc(e, ParticleTypes.SWEEP_ATTACK, e.position().add(0, 1, 0), e.getYRot(), 180, 3.6, 10);
                    }
                }));

        // 2. long lunging stab (gap closer)
        out.add(Ability.of("lunge", 30, 60).range(2.5, 8).weight(3).faceUntil(9)
                .tick((e, t, k) -> {
                    if (k == 3) FpeUtil.sound(e, SoundEvents.ARMOR_EQUIP_CHAIN, 1f, 0.6f);
                    if (k == 10) { e.dashForward(1.45, 0.08); FpeUtil.sound(e, SoundEvents.TRIDENT_THROW, 1.2f, 0.8f); }
                    if (k >= 11 && k <= 14) {
                        Vec3 from = e.position().add(0, 1.2, 0), to = from.add(FpeUtil.forward(e).scale(4.2));
                        if (FpeUtil.hitLine(e, from, to, 0.6, e.dmg(1.8f), 1.2, 0.25) > 0) FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_CRIT, 1f, 0.8f);
                        FpeUtil.particles(e, ParticleTypes.CRIT, to, 4, 0.2, 0.2, 0.2, 0.1);
                    }
                }));

        // 3. hop + overhead split-legs slam: two short diverging ground cracks
        out.add(Ability.of("splitSlam", 40, 110).range(0, 5).weight(3).faceUntil(17)
                .tick((e, t, k) -> {
                    if (k == 8) { e.dashForward(0.35, 0.5); FpeUtil.sound(e, SoundEvents.GOAT_LONG_JUMP, 1f, 0.7f); }
                    if (k == 17) lockDir(e);
                    if (k == 20) {
                        FpeUtil.hitCone(e, 3.6, 55, e.dmg(2.0f), 0.6, 0.8);
                        FpeUtil.sound(e, SoundEvents.GENERIC_EXPLODE, 1f, 0.7f);
                        FpeUtil.sound(e, SoundEvents.ANVIL_LAND, 0.8f, 0.5f);
                        debris(e, e.position().add(lockDir.scale(2)));
                    }
                    if (k > 20 && k <= 24) {
                        int i = k - 20;
                        for (int s = -1; s <= 1; s += 2) {
                            Vec3 at = lockPos.add(rotY(lockDir, s * 16).scale(1.4 + i * 0.8));
                            FpeUtil.hitRadius(e, at, 1.0, e.dmg(1.0f), 0.3, 0.7);
                            debris(e, at);
                            FpeUtil.particles(e, ParticleTypes.CRIT, at.add(0, 0.2, 0), 5, 0.3, 0.1, 0.3, 0.2);
                        }
                        if (i % 2 == 0) FpeUtil.sound(e, SoundEvents.STONE_BREAK, 1f, 0.6f);
                    }
                }));

        // 4. crouching spin: the pencil leg scores a circle around her, then it bursts (point-blank zone)
        out.add(Ability.of("drawCircle", 46, 160).range(0, 4.5).weight(2)
                .tick((e, t, k) -> {
                    if (k == 4) {
                        FpeUtil.fx(e, FpeFx.Kind.RING_TRAP, e.position(), 30, 40, 4.5f, e.dmg(2.0f));
                        lockPos = e.position();
                    }
                    if (k >= 6 && k <= 30) {
                        double spin = 360.0 * (k - 6) / 24.0;
                        Vec3 d = dirRight(e, spin);
                        FpeUtil.particles(e, ParticleTypes.ELECTRIC_SPARK, lockPos.add(d.scale(2.2)).add(0, 0.1, 0), 3, 0.1, 0.05, 0.1, 0.05);
                        if (k % 4 == 0) FpeUtil.sound(e, SoundEvents.GRINDSTONE_USE, 0.5f, 1.4f);
                        // anyone standing on the pencil's path is cut as it passes
                        if (k % 3 == 0) FpeUtil.hitRadius(e, lockPos.add(d.scale(2.2)), 1.0, e.dmg(0.6f), 0.4, 0.1);
                    }
                    if (k == 31) FpeUtil.sound(e, SoundEvents.WITCH_CELEBRATE, 1.2f, 0.8f);
                }));

        // 5. sprinting chase with the compass scraping behind, rising slash
        out.add(Ability.of("charge", 34, 100).range(5, 18).weight(3)
                .tick((e, t, k) -> {
                    if (k == 4) FpeUtil.sound(e, SoundEvents.WITCH_CELEBRATE, 1f, 1.2f);
                    if (k >= 6 && k < 24) {
                        e.dashToward(t.position(), e.isEnraged() ? 0.72 : 0.62, e.getDeltaMovement().y);
                        Vec3 tip = e.position().add(FpeUtil.forward(e).scale(-1.4)).add(FpeUtil.right(e).scale(0.6));
                        FpeUtil.particles(e, ParticleTypes.ELECTRIC_SPARK, tip.add(0, 0.1, 0), 3, 0.1, 0.05, 0.1, 0.1);
                        if (k % 3 == 0) FpeUtil.sound(e, SoundEvents.GRINDSTONE_USE, 0.4f, 1.6f);
                        if (e.distanceTo(t) < 2.0) FpeUtil.hitCone(e, 2.0, 80, e.dmg(0.8f), 0.5, 0.2);
                    }
                    if (k == 24) e.setDeltaMovement(e.getDeltaMovement().scale(0.2));
                    if (k == 27) {
                        FpeUtil.hitCone(e, 3.4, 70, e.dmg(1.4f), 0.4, 0.95);
                        FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_SWEEP, 1.2f, 0.8f);
                        FpeUtil.fx(e, FpeFx.Kind.ARC, e.position().add(0, 1.1, 0), 0, 8, 3.2f, 0).param(150).color(0xFFE6E8F4).setXRot(80);
                    }
                }));

        // 6. hair whip
        out.add(Ability.of("hairWhip", 28, 70).range(0, 4).weight(3)
                .tick((e, t, k) -> {
                    if (k == 11) FpeUtil.sound(e, SoundEvents.PHANTOM_FLAP, 1.2f, 0.6f);
                    if (k == 13) {
                        if (FpeUtil.hitCone(e, 4.2, 110, e.dmg(1.0f), 1.5, 0.3) > 0)
                            for (LivingEntity v : FpeUtil.enemiesInRadius(e, e.position(), 4.4, 3, 1)) v.addEffect(new MobEffectInstance(MobEffects.BLINDNESS, 40, 0));
                        FpeUtil.arc(e, ParticleTypes.SQUID_INK, e.position().add(0, 1.2, 0), e.getYRot(), 80, 3.2, 14);
                    }
                }));

        // 7. enraged three-hit combo
        out.add(Ability.of("combo", 44, 90).range(0, 5).weight(4).when(FpeEntity::isEnraged)
                .tick((e, t, k) -> {
                    if (k == 6 || k == 15) e.dashForward(0.45, 0);
                    if (k == 22) e.dashForward(0.4, 0.45);
                    if (k == 8) {
                        FpeUtil.hitCone(e, 3.6, 80, e.dmg(1.1f), 0.5, 0.2);
                        FpeUtil.fx(e, FpeFx.Kind.ARC, e.position().add(0, 1.1, 0), 0, 7, 3.6f, 0).param(170).color(0xFFE6E8F4);
                        FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_SWEEP, 1f, 0.9f);
                    }
                    if (k == 17) {
                        FpeUtil.hitCone(e, 3.6, 80, e.dmg(1.1f), 0.5, 0.4);
                        FpeUtil.fx(e, FpeFx.Kind.ARC, e.position().add(0, 1.3, 0), 0, 7, 3.6f, 0).param(170).color(0xFFE6E8F4).setXRot(-35);
                        FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_SWEEP, 1f, 1.1f);
                    }
                    if (k == 30) {
                        FpeUtil.hitCone(e, 3.2, 60, e.dmg(1.6f), 0.7, 0.7);
                        FpeUtil.fx(e, FpeFx.Kind.RING_SHOCK, e.position().add(FpeUtil.forward(e).scale(2)), 0, 12, 3f, e.dmg(0.8f));
                        FpeUtil.sound(e, SoundEvents.GENERIC_EXPLODE, 0.9f, 0.8f);
                        debris(e, e.position().add(FpeUtil.forward(e).scale(2)));
                    }
                }));

        // 8. scissor snip: compass legs flung open, step in, snap shut on 14 (heavy hit + slowness)
        out.add(Ability.of("scissorSnip", 30, 80).range(0, 4.2).weight(3).faceUntil(12)
                .tick((e, t, k) -> {
                    if (k == 4) FpeUtil.sound(e, SoundEvents.ARMOR_EQUIP_IRON, 1f, 1.3f);
                    if (k == 10) e.dashForward(0.45, 0);
                    if (k == 14) {
                        Vec3 from = e.position().add(0, 1.2, 0), to = from.add(FpeUtil.forward(e).scale(3.6));
                        if (FpeUtil.hitLine(e, from, to, 0.9, e.dmg(2.1f), 0.3, 0.1) > 0)
                            for (LivingEntity v : FpeUtil.enemiesInRadius(e, from.add(FpeUtil.forward(e).scale(2.4)), 1.8, 3, 1))
                                v.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 50, 2));
                        FpeUtil.sound(e, SoundEvents.SHEEP_SHEAR, 1.4f, 0.5f);
                        FpeUtil.sound(e, SoundEvents.ANVIL_PLACE, 0.5f, 1.8f);
                        FpeUtil.particles(e, ParticleTypes.CRIT, to, 12, 0.3, 0.3, 0.3, 0.2);
                    }
                }));

        // 9. arc slash: huge diagonal compass slash (14, bleeds) + backhand return slash (24)
        out.add(Ability.of("arcSlash", 36, 100).range(0, 4.5).weight(3).faceUntil(12)
                .tick((e, t, k) -> {
                    if (k == 6) FpeUtil.sound(e, SoundEvents.ARMOR_EQUIP_CHAIN, 1f, 0.7f);
                    if (k == 11) e.dashForward(0.5, 0);
                    if (k == 14 || k == 24) {
                        boolean first = k == 14;
                        FpeCombat.cut(e, 3.8, 75, e.dmg(first ? 1.5f : 1.1f), 0.6, 0.2, first ? 60 : 0, !first);
                        FpeUtil.fx(e, FpeFx.Kind.ARC, e.position().add(0, 1.2, 0), 0, 8, 3.6f, 0).param(160).color(0xFFE6E8F4).setXRot(first ? 40 : -10);
                        FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_SWEEP, 1.2f, first ? 0.7f : 0.9f);
                    }
                }));

        // 10. enraged signature "perfect circle": leap, plant the compass (20), draw two turns, every pass scores the ring,
        //     rip the compass out (48) -> the circle bursts + shockwave
        out.add(Ability.of("perfectCircle", 64, 260).range(0, 6).weight(3).when(FpeEntity::isEnraged).faceUntil(14)
                .tick((e, t, k) -> {
                    if (k == 2) FpeUtil.sound(e, SoundEvents.WITCH_CELEBRATE, 1.4f, 0.6f);
                    if (k == 14) e.dashToward(t.position(), 0.45, 0.45);
                    if (k == 20) {
                        lockPos = e.position();
                        FpeUtil.hitRadius(e, e.position().add(FpeUtil.forward(e).scale(1.5)), 2.0, e.dmg(1.4f), 0.5, 0.5);
                        FpeUtil.fx(e, FpeFx.Kind.RING_TRAP, lockPos, 28, 30, 5.0f, e.dmg(1.8f));
                        FpeUtil.sound(e, SoundEvents.ANVIL_LAND, 0.9f, 0.6f);
                        debris(e, e.position().add(FpeUtil.forward(e).scale(1.5)));
                    }
                    if (k > 22 && k <= 46) {
                        // pencil tip on the ground, two right-hand turns (model ry 0 -> -720 over 22..46)
                        Vec3 d = dirRight(e, (k - 22) * 30.0);
                        Vec3 tip = lockPos.add(d.scale(2.6));
                        FpeUtil.particles(e, ParticleTypes.ELECTRIC_SPARK, tip.add(0, 0.1, 0), 3, 0.1, 0.02, 0.1, 0.02);
                        if (k % 2 == 0) for (LivingEntity v : FpeUtil.enemiesInRadius(e, tip, 1.2, 2, 1)) {
                            v.invulnerableTime = 0;
                            if (FpeUtil.hit(e, v, e.dmg(0.5f), 0.2, 0.1)) FpeCombat.bleed(e, v, 40);
                        }
                        if (k % 4 == 0) FpeUtil.sound(e, SoundEvents.GRINDSTONE_USE, 0.6f, 1.2f);
                    }
                    if (k == 48) {
                        FpeUtil.fx(e, FpeFx.Kind.RING_SHOCK, e.position(), 0, 14, 5.0f, e.dmg(1.0f));
                        FpeUtil.hitRadius(e, e.position(), 2.6, e.dmg(1.2f), 1.2, 0.6);
                        FpeUtil.sound(e, SoundEvents.GENERIC_EXPLODE, 1.1f, 0.8f);
                    }
                    if (k == 52) FpeUtil.sound(e, SoundEvents.WITCH_CELEBRATE, 1.4f, 0.7f);
                }));

        // 11. canon: needle thrust (11) -> the victim is hoisted overhead on the compass (12..24) -> slammed down in front (26)
        out.add(Ability.of("impale", 40, 120).range(0, 3.6).weight(3).faceUntil(10)
                .start((e, t, k) -> held = null)
                .end((e, t, k) -> held = null)
                .tick((e, t, k) -> {
                    if (k == 4) FpeUtil.sound(e, SoundEvents.ARMOR_EQUIP_CHAIN, 1f, 0.5f);
                    if (k == 10) e.dashForward(0.4, 0);
                    if (k == 11) {
                        Vec3 from = e.position().add(0, 1.3, 0), to = from.add(FpeUtil.forward(e).scale(3.2));
                        FpeUtil.sound(e, SoundEvents.TRIDENT_HIT, 1.2f, 0.7f);
                        for (LivingEntity v : FpeUtil.enemiesInRadius(e, from.add(FpeUtil.forward(e).scale(1.8)), 1.6, 1.5, 1.5)) {
                            if (FpeUtil.hit(e, v, e.dmg(1.2f), 0, 0)) { held = v; break; }
                        }
                        FpeUtil.particles(e, ParticleTypes.CRIT, to, 10, 0.2, 0.2, 0.2, 0.2);
                    }
                    if (k > 11 && k <= 25 && held != null && held.isAlive()) {
                        double lift = Math.min(1.0, (k - 11) / 11.0);
                        hold(e.position().add(FpeUtil.forward(e).scale(2.2 - 1.6 * lift)).add(0, 1.2 + 2.0 * lift, 0));
                        if (k % 4 == 0) FpeUtil.particles(e, FpeCombat.BLOOD, held.position().add(0, 1, 0), 4, 0.2, 0.2, 0.2, 0.05);
                    }
                    if (k == 26) {
                        Vec3 at = e.position().add(FpeUtil.forward(e).scale(2.0));
                        if (held != null && held.isAlive()) {
                            held.setDeltaMovement(at.subtract(held.position()).scale(0.5).add(0, -1.4, 0));
                            held.hurtMarked = true;
                            FpeUtil.hit(e, held, e.dmg(1.7f), 0.2, 0.1);
                        }
                        FpeUtil.hitRadius(e, at, 1.8, e.dmg(0.9f), 0.8, 0.4);
                        FpeUtil.sound(e, SoundEvents.ANVIL_LAND, 0.9f, 0.6f);
                        FpeUtil.sound(e, SoundEvents.GENERIC_EXPLODE, 0.6f, 1.2f);
                        debris(e, at);
                        held = null;
                    }
                    if (k == 30) FpeUtil.sound(e, SoundEvents.TRIDENT_RETURN, 1f, 0.7f);
                }));

        // 12. canon "devour": claw grab (10), victim hauled up to her shark grin, two bites (18, 25) that heal her, tossed aside (33)
        out.add(Ability.of("devour", 44, 140).range(0, 3.2).weight(3).faceUntil(9)
                .start((e, t, k) -> held = null)
                .end((e, t, k) -> held = null)
                .tick((e, t, k) -> {
                    if (k == 3) FpeUtil.sound(e, SoundEvents.WITCH_CELEBRATE, 1f, 0.6f);
                    if (k == 8) e.dashForward(0.5, 0);
                    if (k == 10) {
                        FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_STRONG, 1f, 0.6f);
                        for (LivingEntity v : FpeUtil.enemiesInRadius(e, FpeUtil.ahead(e, 1.6, 0), 1.5, 2, 1)) {
                            if (FpeUtil.hit(e, v, e.dmg(0.6f), 0, 0)) { held = v; break; }
                        }
                    }
                    if (k > 10 && k < 33 && held != null && held.isAlive()) {
                        hold(FpeUtil.ahead(e, 1.2, Math.min(1.0, (k - 10) / 6.0) * 0.9));
                        if (k == 18 || k == 25) {
                            held.invulnerableTime = 0;
                            if (FpeUtil.hit(e, held, e.dmg(1.1f), 0, 0)) {
                                e.heal(e.isEnraged() ? 5 : 3);
                                FpeCombat.bleed(e, held, 50);
                            }
                            FpeUtil.sound(e, SoundEvents.GENERIC_EAT, 1.4f, 0.6f);
                            FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_CRIT, 1f, 0.6f);
                        }
                    }
                    if (k == 33 && held != null && held.isAlive()) {
                        held.invulnerableTime = 0;
                        FpeUtil.hit(e, held, e.dmg(0.6f), 1.4, 0.45);
                        FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_KNOCKBACK, 1f, 0.7f);
                        held = null;
                    }
                }));

        // 13. pencil stab: a fistful of pencils clenched in the claw, three quick bleeding stabs (9, 13, 17) + compass needle finisher (23)
        out.add(Ability.of("pencilStab", 32, 80).range(0, 3.4).weight(3).faceUntil(20)
                .tick((e, t, k) -> {
                    if (k == 4) FpeUtil.sound(e, SoundEvents.ARMOR_EQUIP_LEATHER, 1f, 1.4f);
                    if (k == 8 || k == 16) e.dashForward(0.3, 0);
                    if (k == 9 || k == 13 || k == 17) {
                        FpeCombat.cut(e, 3.0, 45, e.dmg(0.55f), 0.1, 0.05, 40, true);
                        FpeUtil.particles(e, ParticleTypes.CRIT, FpeUtil.ahead(e, 2.0, 1.3), 5, 0.2, 0.2, 0.2, 0.1);
                        FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_WEAK, 1f, 1.4f);
                    }
                    if (k == 22) e.dashForward(0.5, 0);
                    if (k == 23) {
                        Vec3 from = e.position().add(0, 1.2, 0), to = from.add(FpeUtil.forward(e).scale(3.8));
                        for (LivingEntity v : FpeUtil.enemiesInRadius(e, from.add(FpeUtil.forward(e).scale(2)), 2.0, 2, 1)) v.invulnerableTime = 0;
                        FpeUtil.hitLine(e, from, to, 0.7, e.dmg(1.3f), 1.0, 0.2);
                        FpeUtil.sound(e, SoundEvents.TRIDENT_HIT, 1.1f, 0.8f);
                        FpeUtil.particles(e, ParticleTypes.CRIT, to, 10, 0.2, 0.2, 0.2, 0.2);
                    }
                }));

        // 14. pounce: crouch, leap at the target (8), needle-first plunge on landing (20), wrench free (27)
        out.add(Ability.of("pounce", 40, 120).range(4, 11).weight(3).faceUntil(8)
                .tick((e, t, k) -> {
                    if (k == 3) FpeUtil.sound(e, SoundEvents.WITCH_CELEBRATE, 1.2f, 0.9f);
                    if (k == 8) {
                        double d = Math.sqrt(e.distanceToSqr(t.getX(), e.getY(), t.getZ())) - 1.2;
                        e.dashToward(t.position(), Math.max(0.3, Math.min(1.5, d * 0.13)), 0.6);
                        FpeUtil.sound(e, SoundEvents.GOAT_LONG_JUMP, 1.1f, 0.6f);
                    }
                    if (k > 8 && k < 20) FpeUtil.particles(e, ParticleTypes.CLOUD, e.position().add(0, 0.6, 0), 1, 0.1, 0.1, 0.1, 0.0);
                    if (k == 20) {
                        e.setDeltaMovement(e.getDeltaMovement().multiply(0.1, 1, 0.1));
                        Vec3 at = FpeUtil.ahead(e, 1.4, 0);
                        FpeUtil.hitRadius(e, at, 1.4, e.dmg(1.9f), 0.3, 0.2);
                        FpeUtil.hitRadius(e, e.position(), 3.0, e.dmg(0.7f), 0.9, 0.45);
                        FpeUtil.fx(e, FpeFx.Kind.RING_SHOCK, at, 0, 10, 3.0f, 0);
                        FpeUtil.sound(e, SoundEvents.ANVIL_LAND, 1f, 0.5f);
                        FpeUtil.sound(e, SoundEvents.TRIDENT_HIT, 1.1f, 0.6f);
                        debris(e, at);
                    }
                    if (k == 27) { FpeUtil.sound(e, SoundEvents.TRIDENT_RETURN, 1f, 0.7f); debris(e, FpeUtil.ahead(e, 1.4, 0)); }
                }));
    }
}
