package com.fpe.entity.characters;

import java.util.List;

import javax.annotation.Nullable;

import com.fpe.entity.Ability;
import com.fpe.entity.FpeEntity;
import com.fpe.entity.FpeFx;
import com.fpe.entity.FpeProjectile;
import com.fpe.entity.FpeUtil;

import net.minecraft.core.BlockPos;
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
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.Vec3;

/**
 * Fen - a towering (3.9 block) feral girl whose ink-black arms reshape at will into monstrous weapons:
 * scythes, whip + sickle, needle fans, wings, shields, a mace, a fanged maw, hooked chains, spider / barrage arms, a drill,
 * crushing pincers, razor wire, blade wings, root tendrils, a claw-star boomerang, a spiral lance and an ahoge blade.
 * ONE form (no transformation): the feral m_* attacks are normal attacks; m_frenzy / m_tendrils only while enraged.
 */
public class Fen extends FpeEntity {
    private static final int DARK = 0xE0141018, RED = 0xE08A1020, BLOOD = 0xE0D02030, HAIRC = 0xE0F39232;

    private boolean struck, guarding;
    @Nullable private Vec3 anchor;
    @Nullable private LivingEntity grabbed;

    public Fen(EntityType<? extends FpeEntity> type, Level level) { super(type, level); }

    @Override public Faction faction() { return Faction.STUDENT; }
    @Override public boolean meleeFocus() { return true; }
    @Override protected boolean hasBossBar() { return true; }

    public static AttributeSupplier.Builder attributes() { return baseAttributes(260, 11, 0.33, 8, 0.6); }

    @Override public double preferredDistance() { return 1.8; }
    @Override protected int restTicks() { return isEnraged() ? 7 : 13; }

    @Override
    public void tick() {
        super.tick();
        setMaxUpStep(1.1f);
        if (level().isClientSide || !isAlive()) return;
        if (getStance() != 0) setStance(0); // old saves from the removed monster form
        if (guarding && !"guard".equals(currentAbilityId())) guarding = false;
        if (isEnraged() && tickCount % 5 == 0) FpeUtil.particles(this, ParticleTypes.SQUID_INK, position().add(0, 1.8, 0), 1, 0.3, 0.8, 0.3, 0.01);
    }

    @Override
    public boolean hurt(DamageSource s, float amount) {
        if (guarding && s.getEntity() != null) {
            Vec3 to = s.getEntity().position().subtract(position());
            if (to.horizontalDistanceSqr() > 1e-4 && to.normalize().dot(FpeUtil.forward(this)) > 0.1) {
                FpeUtil.sound(this, SoundEvents.SHIELD_BLOCK, 1f, 0.6f);
                FpeUtil.particles(this, ParticleTypes.CRIT, FpeUtil.ahead(this, 0.8, 1.8), 8, 0.3, 0.4, 0.3, 0.2);
                amount *= 0.15f;
            }
        }
        return super.hurt(s, amount);
    }

    // ------------------------------------------------------------------ helpers
    private void slashArc(double dist, double y, float radius, float sweep, int color, float tilt) {
        FpeFx f = FpeUtil.fx(this, FpeFx.Kind.ARC, FpeUtil.ahead(this, dist, y), 0, 7, radius, 0).param(sweep).color(color);
        f.setXRot(tilt);
    }

    private void fan(FpeProjectile.Kind kind, Vec3 from, LivingEntity t, int n, double stepDeg, double speed, float dmg) {
        Vec3 base = FpeUtil.aim(from, t, speed, 0.3);
        for (int i = 0; i < n; i++)
            FpeUtil.projectile(this, kind, from, base.yRot((float) Math.toRadians((i - (n - 1) / 2.0) * stepDeg)), dmg);
    }

    private Vec3 hand(boolean right, double fwd, double y) {
        return FpeUtil.ahead(this, fwd, y).add(FpeUtil.right(this).scale(right ? 0.6 : -0.6));
    }

    private void pull(LivingEntity v, double fwd, double k) {
        Vec3 d = FpeUtil.ahead(this, fwd, 0).subtract(v.position()).scale(k);
        v.setDeltaMovement(d.x, Math.max(v.getDeltaMovement().y, 0.12), d.z);
        v.hurtMarked = true;
    }

    /** cone hit that ignores hurt-invulnerability, for rapid multi-hit attacks */
    private int rake(double range, double halfDeg, float dmg, double knock, double up) {
        Vec3 f = FpeUtil.forward(this);
        double cos = Math.cos(Math.toRadians(halfDeg));
        int n = 0;
        for (LivingEntity v : FpeUtil.enemiesInRadius(this, position(), range + getBbWidth() * 0.5, 3, 1)) {
            Vec3 d = v.position().subtract(position()).multiply(1, 0, 1);
            if (d.lengthSqr() > 0.01 && d.normalize().dot(f) < cos) continue;
            v.invulnerableTime = 0;
            if (FpeUtil.hit(this, v, dmg, knock, up)) n++;
        }
        return n;
    }

    private void spikeLine(int i, float h, float dmg) {
        Vec3 p = FpeUtil.ahead(this, 2.0 + i * 1.6, 0);
        FpeUtil.fx(this, FpeFx.Kind.SPIKE, p, 3, 22, 1.1f, dmg).param(h);
        FpeUtil.sound(this, SoundEvents.POINTED_DRIPSTONE_LAND, 1f, 0.6f + i * 0.08f);
    }

    @Override
    protected void registerAbilities(List<Ability> out) {
        // scythe - both arms become mantis scythes: X-cross sweep 14, double overhead chop 24
        out.add(Ability.of("scythe", 40, 60).range(0, 5.5).weight(4)
                .tick((e, t, k) -> {
                    if (k == 2) FpeUtil.sound(this, SoundEvents.ARMOR_EQUIP_NETHERITE, 1.2f, 0.5f);
                    if (k == 13) dashForward(0.35, getDeltaMovement().y);
                    if (k == 14) {
                        FpeUtil.hitCone(this, 5.2, 100, dmg(1.3f), 0.7, 0.2);
                        slashArc(0.8, 1.8, 4.4f, 200, RED, 20);
                        slashArc(0.8, 1.6, 4.2f, 200, DARK, -20);
                        FpeUtil.sound(this, SoundEvents.PLAYER_ATTACK_SWEEP, 1.4f, 0.5f);
                    }
                    if (k == 24) {
                        FpeUtil.hitCone(this, 5.0, 50, dmg(1.6f), 0.3, 0.8);
                        slashArc(1.0, 1.2, 3.8f, 160, RED, 88);
                        FpeUtil.sound(this, SoundEvents.PLAYER_ATTACK_STRONG, 1.3f, 0.5f);
                        FpeUtil.particles(this, ParticleTypes.CRIT, FpeUtil.ahead(this, 2.5, 0.3), 18, 0.6, 0.2, 0.6, 0.3);
                    }
                }));
        // lash - right arm becomes a long whip: crack at 13 (line 9 blocks, yanks the target), sweeping lash 22
        out.add(Ability.of("lash", 36, 70).range(3, 10).weight(3).closer()
                .tick((e, t, k) -> {
                    if (k == 3) FpeUtil.sound(this, SoundEvents.SLIME_SQUISH, 1f, 0.5f);
                    if (k == 13) {
                        Vec3 from = position().add(0, 2.2, 0);
                        Vec3 to = from.add(t.getEyePosition().subtract(from).normalize().scale(9));
                        FpeUtil.hitLine(this, from, to, 0.9, dmg(1.1f), 0, 0);
                        if (distanceTo(t) < 9.5 && hasLineOfSight(t)) pull(t, 2.2, 0.35);
                        FpeUtil.sound(this, SoundEvents.FISHING_BOBBER_RETRIEVE, 1.5f, 0.5f);
                        FpeUtil.sound(this, SoundEvents.PLAYER_ATTACK_CRIT, 1.2f, 0.6f);
                        for (int i = 1; i <= 9; i++) FpeUtil.particles(this, ParticleTypes.SQUID_INK, from.lerp(to, i / 9.0), 2, 0.1, 0.1, 0.1, 0.01);
                    }
                    if (k == 22) {
                        FpeUtil.hitCone(this, 7.5, 70, dmg(0.9f), 1.0, 0.3);
                        FpeUtil.arc(this, ParticleTypes.SQUID_INK, position().add(0, 1.5, 0), getYRot(), 70, 6.0, 26);
                        FpeUtil.sound(this, SoundEvents.PLAYER_ATTACK_SWEEP, 1.3f, 0.8f);
                    }
                }));
        // needles - forearms split into needle fans: volleys at 12 and 18, enraged double volley 24
        out.add(Ability.of("needles", 34, 80).range(4, 14).weight(2)
                .tick((e, t, k) -> {
                    if (k == 2) FpeUtil.sound(this, SoundEvents.TRIDENT_RETURN, 1f, 0.6f);
                    if (k == 12) { fan(FpeProjectile.Kind.KNIFE, hand(true, 1.0, 2.0), t, 5, 9, 1.4, dmg(0.6f)); FpeUtil.sound(this, SoundEvents.TRIDENT_THROW, 1.2f, 1.3f); }
                    if (k == 18) { fan(FpeProjectile.Kind.KNIFE, hand(false, 1.0, 2.0), t, 5, 9, 1.4, dmg(0.6f)); FpeUtil.sound(this, SoundEvents.TRIDENT_THROW, 1.2f, 1.5f); }
                    if (k == 24) {
                        int n = isEnraged() ? 9 : 5;
                        fan(FpeProjectile.Kind.KNIFE, FpeUtil.ahead(this, 1.0, 2.0), t, n, 7, 1.5, dmg(0.55f));
                        FpeUtil.sound(this, SoundEvents.TRIDENT_RIPTIDE_1, 1.2f, 1.2f);
                    }
                }));
        // wingglide - arms become ink wings: leap 12, glide homing 13-26, dive slash 28
        out.add(Ability.of("wingglide", 44, 110).range(6, 22).weight(3).closer().moving().faceUntil(26)
                .start((e, t, k) -> struck = false)
                .tick((e, t, k) -> {
                    if (k == 4) FpeUtil.sound(this, SoundEvents.PHANTOM_FLAP, 1.4f, 0.5f);
                    if (k == 12) {
                        dashToward(t.position(), Math.min(1.4, distanceTo(t) * 0.09), 0.85);
                        FpeUtil.particles(this, ParticleTypes.CLOUD, position(), 12, 0.5, 0.05, 0.5, 0.06);
                    }
                    if (k > 12 && k < 27) {
                        Vec3 d = t.position().subtract(position()).multiply(1, 0, 1);
                        Vec3 v = getDeltaMovement();
                        Vec3 h = d.lengthSqr() > 1 ? d.normalize().scale(Math.min(0.9, d.length() * 0.12)) : Vec3.ZERO;
                        setDeltaMovement(v.x * 0.6 + h.x * 0.4, Math.max(v.y, -0.08), v.z * 0.6 + h.z * 0.4);
                        if (k % 3 == 0) FpeUtil.sound(this, SoundEvents.PHANTOM_FLAP, 1f, 0.6f);
                        fallDistance = 0;
                    }
                    if (k == 27) setDeltaMovement(getDeltaMovement().x, -1.0, getDeltaMovement().z);
                    if (k == 28) {
                        FpeUtil.hitRadius(this, position().add(0, 0.6, 0), 2.8, dmg(1.5f), 1.0, 0.5);
                        FpeUtil.fx(this, FpeFx.Kind.RING_SHOCK, position().add(0, 0.1, 0), 0, 10, 3.2f, 0);
                        slashArc(0.6, 0.6, 3.0f, 180, DARK, 0);
                        FpeUtil.sound(this, SoundEvents.PLAYER_ATTACK_STRONG, 1.3f, 0.5f);
                        FpeUtil.particles(this, ParticleTypes.POOF, position(), 16, 0.8, 0.05, 0.8, 0.06);
                    }
                }));
        // guard - wing-shields wrap in front (frontal damage -85 %) 6-26, then burst open 28 (knock back)
        out.add(Ability.of("guard", 40, 140).range(0, 6).weight(2)
                .start((e, t, k) -> guarding = false)
                .tick((e, t, k) -> {
                    if (k == 5) { guarding = true; FpeUtil.sound(this, SoundEvents.ARMOR_EQUIP_NETHERITE, 1.2f, 0.4f); }
                    if (k == 27) guarding = false;
                    if (k == 28) {
                        FpeUtil.hitRadius(this, position().add(0, 1.4, 0), 4.0, dmg(1.2f), 1.6, 0.5);
                        FpeUtil.arc(this, ParticleTypes.SQUID_INK, position().add(0, 1.6, 0), getYRot(), 180, 3.2, 30);
                        FpeUtil.sound(this, SoundEvents.PHANTOM_FLAP, 1.6f, 0.4f);
                        FpeUtil.sound(this, SoundEvents.PLAYER_ATTACK_KNOCKBACK, 1.2f, 0.5f);
                    }
                })
                .end((e, t, k) -> guarding = false));
        // hammer - right arm swells into a spiked mace: overhead SLAM 20 (shockwave + spike line)
        out.add(Ability.of("hammer", 42, 90).range(0, 5.5).weight(3)
                .tick((e, t, k) -> {
                    if (k == 3) FpeUtil.sound(this, SoundEvents.ANVIL_PLACE, 0.8f, 0.5f);
                    if (k == 19) dashForward(0.3, getDeltaMovement().y);
                    if (k == 20) {
                        FpeUtil.hitCone(this, 4.8, 60, dmg(1.9f), 0.6, 0.9);
                        FpeUtil.fx(this, FpeFx.Kind.RING_SHOCK, FpeUtil.ahead(this, 2.6, 0.1), 0, 12, 4.5f, dmg(0.6f));
                        FpeUtil.sound(this, SoundEvents.GENERIC_EXPLODE, 1f, 0.6f);
                        FpeUtil.particles(this, ParticleTypes.EXPLOSION, FpeUtil.ahead(this, 2.6, 0.2), 2, 0.3, 0.1, 0.3, 0);
                    }
                    if (k >= 22 && k <= 28 && (k - 22) % 3 == 0) spikeLine(1 + (k - 22) / 3, 0.9f, dmg(0.8f));
                }));
        // spider - six spider arms burst from the back: flurry 12-28, all-arm pin 34 (slows)
        out.add(Ability.of("spider", 46, 120).range(0, 5).weight(2)
                .tick((e, t, k) -> {
                    if (k == 3) FpeUtil.sound(this, SoundEvents.SPIDER_AMBIENT, 1.4f, 0.5f);
                    if (k >= 12 && k <= 28 && k % 4 == 0) {
                        FpeUtil.hitCone(this, 4.0, 90, dmg(0.45f), 0.1, 0.05);
                        FpeUtil.sound(this, SoundEvents.SPIDER_STEP, 1.2f, 0.6f + k * 0.02f);
                        FpeUtil.particles(this, ParticleTypes.CRIT, FpeUtil.ahead(this, 2, 1.6), 6, 0.6, 0.6, 0.6, 0.2);
                    }
                    if (k == 34) {
                        for (LivingEntity v : FpeUtil.enemiesInRadius(this, FpeUtil.ahead(this, 2.2, 0), 2.6, 2, 1)) {
                            FpeUtil.hit(this, v, dmg(1.2f), 0.1, 0);
                            v.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 60, 3));
                        }
                        FpeUtil.sound(this, SoundEvents.PLAYER_ATTACK_STRONG, 1.2f, 0.6f);
                        FpeUtil.particles(this, ParticleTypes.POOF, FpeUtil.ahead(this, 2.2, 0.1), 12, 0.8, 0.05, 0.8, 0.05);
                    }
                }));
        // hook - hooked chain arm thrown 10 (reach 12), yanks the victim in 14-20, right claw slash 22
        out.add(Ability.of("hook", 40, 100).range(4, 13).weight(3).closer().faceUntil(11)
                .start((e, t, k) -> grabbed = null)
                .tick((e, t, k) -> {
                    if (k == 6) FpeUtil.sound(this, SoundEvents.CHAIN_PLACE, 1.2f, 0.6f);
                    if (k == 10) FpeUtil.sound(this, SoundEvents.FISHING_BOBBER_THROW, 1.4f, 0.5f);
                    if (k == 12) {
                        Vec3 from = position().add(0, 2.2, 0);
                        Vec3 to = from.add(FpeUtil.forward(this).scale(12));
                        if (t.getBoundingBox().inflate(0.9).clip(from, to).isPresent() && FpeUtil.hit(this, t, dmg(0.6f), 0, 0)) {
                            grabbed = t;
                            FpeUtil.sound(this, SoundEvents.CHAIN_HIT, 1.4f, 0.6f);
                        }
                        for (int i = 1; i <= 12; i++) FpeUtil.particles(this, ParticleTypes.SMOKE, from.lerp(to, i / 12.0), 1, 0.05, 0.05, 0.05, 0);
                    }
                    LivingEntity g = grabbed;
                    if (g != null && g.isAlive() && k >= 14 && k <= 20) pull(g, 1.8, 0.45);
                    if (k == 22) {
                        FpeUtil.hitCone(this, 3.8, 80, dmg(1.3f), 0.9, 0.3);
                        slashArc(1.0, 1.8, 3.2f, 150, DARK, 15);
                        FpeUtil.sound(this, SoundEvents.PLAYER_ATTACK_SWEEP, 1.2f, 0.7f);
                        grabbed = null;
                    }
                })
                .end((e, t, k) -> grabbed = null));
        // maw - right arm opens into a fanged jaw: lunge bite 10 grabs, chomps 18 / 26 / 34, flings 39
        out.add(Ability.of("maw", 44, 120).range(0, 3.8).weight(2)
                .start((e, t, k) -> grabbed = null)
                .tick((e, t, k) -> {
                    if (k == 4) FpeUtil.sound(this, SoundEvents.RAVAGER_ROAR, 0.8f, 1.5f);
                    if (k == 9) dashForward(0.4, getDeltaMovement().y);
                    if (k == 10) {
                        FpeUtil.sound(this, SoundEvents.EVOKER_FANGS_ATTACK, 1.4f, 0.6f);
                        if (distanceTo(t) < 4 && FpeUtil.hit(this, t, dmg(0.9f), 0, 0)) {
                            grabbed = t;
                            t.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 40, 4));
                        }
                    }
                    LivingEntity g = grabbed;
                    if (g == null || !g.isAlive()) return;
                    if (k > 10 && k < 39) pull(g, 2.0, 0.5);
                    if (k == 18 || k == 26 || k == 34) {
                        if (FpeUtil.canHurt(this, g)) { g.invulnerableTime = 0; g.hurt(damageSources().mobAttack(this), dmg(0.75f)); }
                        FpeUtil.sound(this, SoundEvents.EVOKER_FANGS_ATTACK, 1.2f, 0.5f + k * 0.01f);
                        FpeUtil.particles(this, ParticleTypes.DAMAGE_INDICATOR, g.position().add(0, 1, 0), 6, 0.3, 0.3, 0.3, 0.1);
                    }
                    if (k == 39) { FpeUtil.knock(g, position(), 2.0, 0.7); grabbed = null; FpeUtil.sound(this, SoundEvents.PLAYER_ATTACK_KNOCKBACK, 1.2f, 0.5f); }
                })
                .end((e, t, k) -> grabbed = null));
        // pounce - crouch, leap 8, claws-first landing rake 12-18
        out.add(Ability.of("pounce", 30, 70).range(3.5, 12).weight(3).closer().faceUntil(8)
                .start((e, t, k) -> struck = false)
                .tick((e, t, k) -> {
                    if (k == 2) FpeUtil.sound(this, SoundEvents.CAT_HISS, 1.2f, 0.5f);
                    if (k == 8) {
                        dashToward(t.position(), Math.min(1.6, Math.max(0.6, distanceTo(t) * 0.15)), 0.55);
                        FpeUtil.particles(this, ParticleTypes.CLOUD, position(), 8, 0.3, 0.05, 0.3, 0.05);
                    }
                    if (k >= 11 && k <= 18 && !struck && FpeUtil.hitCone(this, 2.8, 75, dmg(1.5f), 0.9, 0.35) > 0) {
                        struck = true;
                        FpeUtil.sound(this, SoundEvents.PHANTOM_BITE, 1f, 0.7f);
                    }
                    if (k == 15) {
                        slashArc(0.8, 0.6, 3.0f, 150, DARK, 70);
                        FpeUtil.particles(this, ParticleTypes.POOF, position(), 10, 0.6, 0.05, 0.6, 0.05);
                    }
                }));
        // ================================================================== feral attacks (formerly the monster form)
        // m_frenzy - six savage alternating slashes 10..35, crossing finisher 42
        out.add(Ability.of("m_frenzy", 48, 90).range(0, 5).weight(4).when(FpeEntity::isEnraged)
                .tick((e, t, k) -> {
                    if (k == 1) FpeUtil.sound(this, SoundEvents.RAVAGER_ROAR, 1f, 1.4f);
                    for (int i = 0; i < 6; i++) {
                        int pk = 10 + 5 * i;
                        if (k == pk - 1) dashForward(0.32, getDeltaMovement().y);
                        if (k == pk) {
                            FpeUtil.hitCone(this, 4.0, 75, dmg(0.5f), 0.15, 0.05);
                            slashArc(1.0, 1.4 + (i % 3) * 0.2, 3.2f, 140, i % 2 == 0 ? BLOOD : DARK, i % 2 == 0 ? 25 : -25);
                            FpeUtil.sound(this, SoundEvents.PLAYER_ATTACK_SWEEP, 0.9f, 0.8f + i * 0.08f);
                        }
                    }
                    if (k == 42) {
                        FpeUtil.hitCone(this, 4.6, 70, dmg(1.7f), 1.4, 0.5);
                        slashArc(1.0, 1.4, 4.0f, 160, BLOOD, 50);
                        slashArc(1.0, 1.4, 4.0f, 160, BLOOD, -50);
                        FpeUtil.sound(this, SoundEvents.PLAYER_ATTACK_STRONG, 1.4f, 0.4f);
                    }
                }));
        // m_impale - claws plunge into the ground 14, black spikes rip toward the target 16-31 (3 lanes)
        out.add(Ability.of("m_impale", 40, 90).range(2, 14).weight(3).faceUntil(13)
                .tick((e, t, k) -> {
                    if (k == 6) FpeUtil.sound(this, SoundEvents.WARDEN_ROAR, 0.8f, 1.4f);
                    if (k == 14) {
                        FpeUtil.hitCone(this, 2.8, 80, dmg(1.0f), 0.4, 0.5);
                        FpeUtil.sound(this, SoundEvents.ZOMBIE_ATTACK_WOODEN_DOOR, 1.2f, 0.5f);
                        FpeUtil.particles(this, ParticleTypes.POOF, FpeUtil.ahead(this, 1.4, 0.1), 14, 0.6, 0.05, 0.6, 0.06);
                    }
                    if (k >= 16 && k <= 31 && (k - 16) % 3 == 0) {
                        int i = (k - 16) / 3;
                        spikeLine(i, 1.1f + i * 0.15f, dmg(1.1f));
                        Vec3 p = FpeUtil.ahead(this, 2.0 + i * 1.6, 0), s = FpeUtil.right(this).scale(1.0 + i * 0.35);
                        FpeUtil.fx(this, FpeFx.Kind.SPIKE, p.add(s), 5, 18, 0.9f, dmg(0.8f)).param(0.8f);
                        FpeUtil.fx(this, FpeFx.Kind.SPIKE, p.subtract(s), 5, 18, 0.9f, dmg(0.8f)).param(0.8f);
                    }
                }));
        // m_lunge - coils, launches 9, mauls everything in the path 10-20, skids 22
        out.add(Ability.of("m_lunge", 32, 60).range(3.5, 16).weight(3).closer().faceUntil(9)
                .start((e, t, k) -> struck = false)
                .tick((e, t, k) -> {
                    if (k == 3) FpeUtil.sound(this, SoundEvents.FOX_SCREECH, 1.4f, 0.5f);
                    if (k == 9) dashToward(t.position(), Math.min(1.9, Math.max(0.8, distanceTo(t) * 0.16)), 0.35);
                    if (k >= 10 && k <= 20) {
                        if (k % 2 == 0) FpeUtil.particles(this, ParticleTypes.SQUID_INK, position().add(0, 0.8, 0), 3, 0.3, 0.3, 0.3, 0.02);
                        if (!struck && FpeUtil.hitCone(this, 2.6, 80, dmg(1.6f), 1.3, 0.4) > 0) {
                            struck = true;
                            FpeUtil.sound(this, SoundEvents.PHANTOM_BITE, 1.3f, 0.5f);
                            FpeUtil.particles(this, ParticleTypes.CRIT, FpeUtil.ahead(this, 1.2, 1.2), 16, 0.4, 0.4, 0.4, 0.3);
                        }
                    }
                    if (k == 22) setDeltaMovement(getDeltaMovement().scale(0.2));
                }));
        // m_tendrils - signature: ERUPTION 14 - extra arms burst out and tendrils/spikes erupt in a ring, thrash 18-30
        out.add(Ability.of("m_tendrils", 50, 160).range(0, 9).weight(3).blind().when(FpeEntity::isEnraged)
                .tick((e, t, k) -> {
                    if (k == 2) FpeUtil.sound(this, SoundEvents.WARDEN_HEARTBEAT, 2f, 0.7f);
                    if (k == 14) {
                        FpeUtil.sound(this, SoundEvents.WARDEN_SONIC_BOOM, 1.2f, 0.8f);
                        FpeUtil.hitRadius(this, position().add(0, 1, 0), 3.5, dmg(1.0f), 1.2, 0.5);
                        int n = isEnraged() ? 10 : 7;
                        for (int i = 0; i < n; i++) {
                            double a = Math.PI * 2 * i / n;
                            Vec3 p = position().add(Math.cos(a) * 4.5, 0, Math.sin(a) * 4.5);
                            FpeUtil.fx(this, FpeFx.Kind.SPIKE, p, 4, 24, 1.0f, dmg(0.9f)).param(1.4f);
                        }
                        FpeUtil.fx(this, FpeFx.Kind.TENTACLE, t.position(), 6, 40, 1.3f, dmg(0.6f));
                    }
                    if (k >= 18 && k <= 30 && k % 4 == 2) {
                        FpeUtil.hitRadius(this, position().add(0, 1.5, 0), 4.5, dmg(0.45f), 0.6, 0.2);
                        FpeUtil.arc(this, ParticleTypes.SQUID_INK, position().add(0, 2, 0), getYRot() + k * 30, 180, 4.0, 24);
                        FpeUtil.sound(this, SoundEvents.PLAYER_ATTACK_SWEEP, 1f, 0.5f);
                    }
                }));
        // m_reap - black scythes, two full spins: hits 12 and 20 all around
        out.add(Ability.of("m_reap", 36, 80).range(0, 5.5).weight(3)
                .tick((e, t, k) -> {
                    if (k == 2) FpeUtil.sound(this, SoundEvents.ARMOR_EQUIP_NETHERITE, 1.2f, 0.4f);
                    if (k == 11 || k == 19) dashForward(0.4, getDeltaMovement().y);
                    if (k == 12 || k == 20) {
                        FpeUtil.hitRadius(this, position().add(0, 1.2, 0), 4.8, dmg(1.25f), 1.0, 0.3);
                        FpeUtil.arc(this, ParticleTypes.SWEEP_ATTACK, position().add(0, 1.4, 0), getYRot(), 180, 3.8, 14);
                        slashArc(0, 1.4, 4.6f, 359, BLOOD, 0);
                        FpeUtil.sound(this, SoundEvents.PLAYER_ATTACK_SWEEP, 1.4f, 0.5f + (k - 12) * 0.03f);
                    }
                }));

        // ================================================================== shape-shift arsenal
        // drill - right arm twists into a drill: dash THRUST 10, grinding multi-hits 12-22, burst 24 (launch)
        out.add(Ability.of("drill", 36, 80).range(0, 6).weight(3).closer().faceUntil(10)
                .tick((e, t, k) -> {
                    if (k == 2) FpeUtil.sound(this, SoundEvents.GRINDSTONE_USE, 1.2f, 0.6f);
                    if (k == 9) dashForward(0.9, getDeltaMovement().y);
                    if (k == 10) {
                        rake(4.2, 35, dmg(0.7f), 0.1, 0);
                        FpeUtil.sound(this, SoundEvents.PLAYER_ATTACK_STRONG, 1.2f, 0.7f);
                    }
                    if (k >= 12 && k <= 22 && k % 2 == 0) {
                        rake(4.0, 35, dmg(0.32f), 0.05, 0);
                        FpeUtil.particles(this, ParticleTypes.CRIT, hand(true, 2.6, 2.0), 6, 0.2, 0.2, 0.2, 0.3);
                        FpeUtil.sound(this, SoundEvents.GRINDSTONE_USE, 0.9f, 0.8f + k * 0.02f);
                    }
                    if (k == 24) {
                        rake(4.4, 40, dmg(1.1f), 1.6, 0.4);
                        FpeUtil.particles(this, ParticleTypes.SQUID_INK, hand(true, 3.0, 2.0), 14, 0.3, 0.3, 0.3, 0.2);
                        FpeUtil.sound(this, SoundEvents.GENERIC_EXPLODE, 0.6f, 1.4f);
                    }
                }));
        // crusher - both arms become crushing pincers: CLAMP 12 grabs, lift, CRUSH 20, overhead SLAM 28
        out.add(Ability.of("crusher", 40, 110).range(0, 4.8).weight(2)
                .start((e, t, k) -> grabbed = null)
                .tick((e, t, k) -> {
                    if (k == 2) FpeUtil.sound(this, SoundEvents.ARMOR_EQUIP_NETHERITE, 1.2f, 0.5f);
                    if (k == 11) dashForward(0.3, getDeltaMovement().y);
                    if (k == 12) {
                        FpeUtil.sound(this, SoundEvents.IRON_TRAPDOOR_CLOSE, 1.4f, 0.5f);
                        Vec3 d = t.position().subtract(position());
                        if (d.horizontalDistance() < 4.8 && d.multiply(1, 0, 1).normalize().dot(FpeUtil.forward(this)) > 0.5 && FpeUtil.hit(this, t, dmg(0.7f), 0, 0)) grabbed = t;
                    }
                    LivingEntity g = grabbed;
                    if (g != null && g.isAlive() && k > 12 && k < 28) FpeUtil.hold(this, g, 2.2, 0.4 + Math.min(1.0, (k - 12) / 5.0) * 2.4, 0);
                    if (k == 20 && g != null && g.isAlive()) {
                        g.invulnerableTime = 0;
                        FpeUtil.hit(this, g, dmg(0.9f), 0, 0);
                        FpeUtil.particles(this, ParticleTypes.DAMAGE_INDICATOR, g.position().add(0, 1, 0), 8, 0.3, 0.3, 0.3, 0.1);
                        FpeUtil.sound(this, SoundEvents.ZOMBIE_ATTACK_IRON_DOOR, 1f, 0.6f);
                    }
                    if (k == 28) {
                        Vec3 p = FpeUtil.ahead(this, 2.2, 0.1);
                        if (g != null && g.isAlive()) {
                            FpeUtil.holdAt(g, p);
                            g.invulnerableTime = 0;
                            FpeUtil.hit(this, g, dmg(1.5f), 0.6, 0.2);
                            FpeUtil.stun(g, 20);
                        }
                        grabbed = null;
                        FpeUtil.hitRadius(this, p, 2.6, dmg(0.9f), 1.0, 0.4);
                        FpeUtil.fx(this, FpeFx.Kind.RING_SHOCK, p, 0, 12, 3.8f, 0);
                        FpeUtil.particles(this, ParticleTypes.EXPLOSION, p, 2, 0.3, 0.1, 0.3, 0);
                        FpeUtil.sound(this, SoundEvents.GENERIC_EXPLODE, 1f, 0.7f);
                    }
                })
                .end((e, t, k) -> grabbed = null));
        // lattice - fingers spin out razor wire: horizontal lattice 13 (5 wires), down-cut 22, cinch 28 pulls everything in
        out.add(Ability.of("lattice", 38, 90).range(2, 9).weight(3)
                .tick((e, t, k) -> {
                    if (k == 3) FpeUtil.sound(this, SoundEvents.CHAIN_PLACE, 1.2f, 1.6f);
                    Vec3 from = position().add(0, 2.2, 0);
                    if (k == 13) {
                        for (int i = -2; i <= 2; i++) {
                            Vec3 dir = FpeUtil.forward(this).yRot((float) Math.toRadians(i * 18));
                            FpeUtil.hitLine(this, from, from.add(dir.scale(8.5)), 0.45, dmg(0.8f), 0.2, 0.1);
                            for (int j = 2; j <= 8; j += 2) FpeUtil.particles(this, ParticleTypes.CRIT, from.add(dir.scale(j)), 1, 0, 0, 0, 0);
                        }
                        FpeUtil.sound(this, SoundEvents.PLAYER_ATTACK_SWEEP, 1.3f, 1.4f);
                    }
                    if (k == 22) {
                        for (int i = -1; i <= 1; i++) {
                            Vec3 s = FpeUtil.right(this).scale(i * 0.9);
                            FpeUtil.hitLine(this, from.add(0, 1.4, 0).add(s), FpeUtil.ahead(this, 8, 0.2).add(s), 0.5, dmg(0.9f), 0.3, 0.2);
                        }
                        slashArc(1.2, 1.6, 4.5f, 120, RED, 88);
                        FpeUtil.sound(this, SoundEvents.PLAYER_ATTACK_CRIT, 1.3f, 1.3f);
                    }
                    if (k == 28) {
                        for (LivingEntity v : FpeUtil.enemiesInRadius(this, position(), 9, 3, 1)) {
                            if (v.position().subtract(position()).multiply(1, 0, 1).normalize().dot(FpeUtil.forward(this)) < 0.3) continue;
                            v.invulnerableTime = 0;
                            FpeUtil.hit(this, v, dmg(0.6f), 0, 0);
                            FpeUtil.pull(v, FpeUtil.ahead(this, 1.6, 0), 1.3);
                            v.addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SLOWDOWN, 40, 2));
                        }
                        FpeUtil.sound(this, SoundEvents.FISHING_BOBBER_RETRIEVE, 1.5f, 1.2f);
                    }
                }));
        // kusari - whip arm + sickle (kusarigama): stepping sweeps 14 / 22, overhead chop 30, yank 34
        out.add(Ability.of("kusari", 44, 90).range(2.5, 9).weight(3).closer()
                .tick((e, t, k) -> {
                    if (k == 4) FpeUtil.sound(this, SoundEvents.CHAIN_PLACE, 1.2f, 0.6f);
                    if (k >= 6 && k <= 12 && k % 2 == 0) FpeUtil.sound(this, SoundEvents.PLAYER_ATTACK_NODAMAGE, 1f, 0.6f + k * 0.04f);
                    if (k == 13 || k == 21) dashForward(0.45, getDeltaMovement().y);
                    if (k == 14 || k == 22) {
                        FpeUtil.hitCone(this, 8.0, 80, dmg(1.0f), 0.6, 0.2);
                        FpeUtil.arc(this, ParticleTypes.SWEEP_ATTACK, position().add(0, 1.6, 0), getYRot(), 80, 6.0, 12);
                        slashArc(1.0, 1.6, 6.5f, 160, k == 14 ? RED : DARK, k == 14 ? 10 : -10);
                        FpeUtil.sound(this, SoundEvents.PLAYER_ATTACK_SWEEP, 1.3f, k == 14 ? 0.7f : 0.9f);
                    }
                    if (k == 30) {
                        Vec3 from = position().add(0, 3.0, 0);
                        FpeUtil.hitLine(this, from, FpeUtil.ahead(this, 8.5, 0.3), 1.0, dmg(1.4f), 0.3, 0.5);
                        slashArc(2.0, 1.2, 4.8f, 140, RED, 88);
                        FpeUtil.particles(this, ParticleTypes.CRIT, FpeUtil.ahead(this, 7.5, 0.3), 14, 0.5, 0.2, 0.5, 0.3);
                        FpeUtil.sound(this, SoundEvents.PLAYER_ATTACK_STRONG, 1.3f, 0.6f);
                    }
                    if (k == 34 && distanceTo(t) < 9.5 && hasLineOfSight(t)) {
                        FpeUtil.pull(t, FpeUtil.ahead(this, 2.0, 0), 1.4);
                        FpeUtil.sound(this, SoundEvents.FISHING_BOBBER_RETRIEVE, 1.4f, 0.6f);
                    }
                }));
        // grapple - grappling hook thrown 9, anchors 10, she REELS HERSELF in 11-18, left-claw rake on arrival 20
        out.add(Ability.of("grapple", 40, 90).range(5, 18).weight(3).closer().faceUntil(18)
                .start((e, t, k) -> anchor = null)
                .tick((e, t, k) -> {
                    if (k == 3) FpeUtil.sound(this, SoundEvents.CHAIN_PLACE, 1.2f, 0.8f);
                    if (k == 9) FpeUtil.sound(this, SoundEvents.FISHING_BOBBER_THROW, 1.5f, 0.5f);
                    if (k == 10) {
                        if (distanceTo(t) <= 18.5 && hasLineOfSight(t)) {
                            anchor = t.position();
                            FpeUtil.hit(this, t, dmg(0.5f), 0, 0);
                            FpeUtil.sound(this, SoundEvents.CHAIN_HIT, 1.4f, 0.6f);
                        } else anchor = FpeUtil.ahead(this, Math.min(10, distanceTo(t)), 0);
                        Vec3 from = position().add(0, 2.4, 0);
                        for (int i = 1; i <= 12; i++) FpeUtil.particles(this, ParticleTypes.SMOKE, from.lerp(anchor.add(0, 1, 0), i / 12.0), 1, 0.05, 0.05, 0.05, 0);
                    }
                    Vec3 a = anchor;
                    if (a != null && k >= 11 && k <= 18) {
                        if (t.isAlive() && distanceTo(t) < 20) a = anchor = t.position();
                        Vec3 d = a.subtract(position());
                        if (d.horizontalDistance() > 2.4) {
                            Vec3 v = d.multiply(1, 0, 1).normalize().scale(Math.min(1.5, d.horizontalDistance() * 0.4));
                            setDeltaMovement(v.x, 0.12 + Mth.clamp(d.y * 0.1, -0.1, 0.3), v.z);
                        } else setDeltaMovement(getDeltaMovement().scale(0.4));
                        fallDistance = 0;
                        if (k % 2 == 0) FpeUtil.sound(this, SoundEvents.CHAIN_STEP, 1f, 1.2f);
                    }
                    if (k == 20) {
                        rake(3.4, 80, dmg(1.5f), 1.2, 0.4);
                        slashArc(0.8, 1.4, 3.4f, 150, DARK, 60);
                        FpeUtil.sound(this, SoundEvents.PLAYER_ATTACK_SWEEP, 1.3f, 0.6f);
                    }
                    if (k == 21) setDeltaMovement(getDeltaMovement().scale(0.3));
                })
                .end((e, t, k) -> anchor = null));
        // wingrake - mirrored blade-wings: leap 12, low glide slicing 14-23, buzzsaw spin 28, land 32
        out.add(Ability.of("wingrake", 46, 120).range(5, 20).weight(3).closer().moving().faceUntil(25)
                .tick((e, t, k) -> {
                    if (k == 6) FpeUtil.sound(this, SoundEvents.PHANTOM_SWOOP, 1.4f, 0.6f);
                    if (k == 12) dashToward(t.position(), Math.min(1.5, distanceTo(t) * 0.11), 0.42);
                    if (k > 12 && k < 30) {
                        Vec3 d = t.position().subtract(position()).multiply(1, 0, 1);
                        Vec3 v = getDeltaMovement();
                        Vec3 h = d.lengthSqr() > 1 ? d.normalize().scale(Math.min(1.0, d.length() * 0.14)) : Vec3.ZERO;
                        setDeltaMovement(v.x * 0.55 + h.x * 0.45, Math.max(v.y, -0.04), v.z * 0.55 + h.z * 0.45);
                        fallDistance = 0;
                    }
                    if (k >= 14 && k <= 23 && (k - 14) % 3 == 0) {
                        rake(2.8, 180, dmg(0.5f), 0.3, 0.1);
                        slashArc(0, 1.2, 3.0f, 120, DARK, 0);
                        FpeUtil.sound(this, SoundEvents.PHANTOM_FLAP, 1.1f, 1.2f);
                    }
                    if (k == 28) {
                        FpeUtil.hitRadius(this, position().add(0, 1.0, 0), 3.6, dmg(1.3f), 1.2, 0.4);
                        slashArc(0, 1.1, 4.0f, 359, RED, 0);
                        FpeUtil.sound(this, SoundEvents.PLAYER_ATTACK_SWEEP, 1.5f, 0.5f);
                    }
                    if (k == 30) setDeltaMovement(getDeltaMovement().x * 0.4, -0.6, getDeltaMovement().z * 0.4);
                    if (k == 32) {
                        FpeUtil.fx(this, FpeFx.Kind.RING_SHOCK, position().add(0, 0.1, 0), 0, 8, 2.5f, 0);
                        FpeUtil.particles(this, ParticleTypes.POOF, position(), 12, 0.8, 0.05, 0.8, 0.05);
                    }
                }));
        // rootspikes - arms grow roots and PLUNGE into the ground 12: spikes erupt under the target ~20, ring around her 26
        out.add(Ability.of("rootspikes", 44, 130).range(2.5, 14).weight(2).faceUntil(14)
                .tick((e, t, k) -> {
                    if (k == 4) FpeUtil.sound(this, SoundEvents.WARDEN_ROAR, 0.7f, 1.6f);
                    if (k == 12) {
                        rake(3.0, 70, dmg(0.9f), 0.3, 0.6);
                        FpeUtil.particles(this, ParticleTypes.POOF, FpeUtil.ahead(this, 1.4, 0.1), 14, 0.6, 0.05, 0.6, 0.06);
                        FpeUtil.sound(this, SoundEvents.ROOTED_DIRT_BREAK, 1.5f, 0.5f);
                    }
                    if (k == 14) {
                        Vec3 c = t.position();
                        FpeUtil.fx(this, FpeFx.Kind.SPIKE, c, 6, 20, 1.4f, dmg(1.4f)).param(1.8f);
                        int n = isEnraged() ? 8 : 5;
                        for (int i = 0; i < n; i++) {
                            double a = Math.PI * 2 * i / n;
                            FpeUtil.fx(this, FpeFx.Kind.SPIKE, c.add(Math.cos(a) * 2.2, 0, Math.sin(a) * 2.2), 9, 18, 0.9f, dmg(0.9f)).param(1.1f);
                        }
                        if (isEnraged()) FpeUtil.fx(this, FpeFx.Kind.TENTACLE, c, 4, 36, 1.2f, dmg(0.5f));
                    }
                    if (k >= 14 && k <= 24 && k % 4 == 2) FpeUtil.sound(this, SoundEvents.ROOTED_DIRT_STEP, 1.4f, 0.5f);
                    if (k == 26) {
                        for (int i = 0; i < 8; i++) {
                            double a = Math.PI * 2 * i / 8 + 0.4;
                            FpeUtil.fx(this, FpeFx.Kind.SPIKE, position().add(Math.cos(a) * 3.0, 0, Math.sin(a) * 3.0), 1, 18, 1.0f, dmg(1.0f)).param(1.3f);
                        }
                        FpeUtil.hitRadius(this, position().add(0, 0.5, 0), 2.5, dmg(0.8f), 1.2, 0.5);
                        FpeUtil.sound(this, SoundEvents.ZOMBIE_BREAK_WOODEN_DOOR, 1.2f, 0.6f);
                    }
                }));
        // barrage - eight ink arms burst from her back: rapid punches 10-30 (every 2 ticks), all-arm finisher 34
        out.add(Ability.of("barrage", 44, 100).range(0, 5).weight(3)
                .tick((e, t, k) -> {
                    if (k == 2) FpeUtil.sound(this, SoundEvents.SPIDER_AMBIENT, 1.4f, 0.4f);
                    if (k == 10 || k == 20) dashForward(0.25, getDeltaMovement().y);
                    if (k >= 10 && k <= 30 && k % 2 == 0) {
                        rake(4.4, 60, dmg(0.28f), 0.08, 0);
                        FpeUtil.particles(this, ParticleTypes.CRIT, FpeUtil.ahead(this, 2.6, 2.4 + (k % 4) * 0.3), 3, 0.5, 0.4, 0.5, 0.2);
                        FpeUtil.sound(this, SoundEvents.PLAYER_ATTACK_WEAK, 1f, 0.6f + (k % 6) * 0.1f);
                    }
                    if (k == 34) {
                        rake(4.8, 70, dmg(1.4f), 1.8, 0.5);
                        slashArc(1.0, 2.2, 3.6f, 120, DARK, 0);
                        FpeUtil.sound(this, SoundEvents.PLAYER_ATTACK_KNOCKBACK, 1.4f, 0.5f);
                    }
                }));
        // boomerang - throws a three-bladed claw star 13 (returns), sprints after it 16, left-claw slash 24, catch 32
        out.add(Ability.of("boomerang", 44, 90).range(4, 16).weight(3).closer().faceUntil(16)
                .tick((e, t, k) -> {
                    if (k == 3) FpeUtil.sound(this, SoundEvents.ARMOR_EQUIP_NETHERITE, 1.2f, 1.2f);
                    if (k == 13) {
                        Vec3 from = hand(true, 0.8, 2.4);
                        FpeUtil.projectile(this, FpeProjectile.Kind.AXE, from, FpeUtil.aim(from, t, 1.25, 0.3), dmg(1.0f));
                        FpeUtil.sound(this, SoundEvents.TRIDENT_THROW, 1.4f, 0.6f);
                    }
                    if (k == 16) dashToward(t.position(), Math.min(1.3, distanceTo(t) * 0.13), 0.2);
                    if (k == 24) {
                        rake(3.8, 80, dmg(1.3f), 0.9, 0.3);
                        slashArc(0.9, 1.8, 3.4f, 160, DARK, -15);
                        FpeUtil.sound(this, SoundEvents.PLAYER_ATTACK_SWEEP, 1.3f, 0.8f);
                    }
                    if (k == 32) FpeUtil.sound(this, SoundEvents.ITEM_PICKUP, 1.2f, 0.5f);
                }));
        // spiral - both arms twist into a spiral lance: corkscrew LAUNCH 10, drilling hits 11-21, burst 22
        out.add(Ability.of("spiral", 40, 110).range(4, 14).weight(3).closer().faceUntil(10)
                .tick((e, t, k) -> {
                    if (k == 2) FpeUtil.sound(this, SoundEvents.WARDEN_HEARTBEAT, 1.6f, 1.2f);
                    if (k == 10) {
                        dashToward(t.position(), Math.min(1.7, Math.max(0.9, distanceTo(t) * 0.15)), 0.18);
                        FpeUtil.sound(this, SoundEvents.TRIDENT_RIPTIDE_3, 1.4f, 0.7f);
                    }
                    if (k > 10 && k <= 21) {
                        Vec3 v = getDeltaMovement();
                        setDeltaMovement(v.x, Math.max(v.y, -0.02), v.z);
                        fallDistance = 0;
                        FpeUtil.particles(this, ParticleTypes.SQUID_INK, FpeUtil.ahead(this, 2.0, 1.6), 2, 0.3, 0.3, 0.3, 0.05);
                        if (k % 2 == 1) rake(3.0, 50, dmg(0.3f), 0.15, 0.05);
                    }
                    if (k == 22) {
                        rake(3.6, 70, dmg(1.3f), 1.8, 0.5);
                        FpeUtil.fx(this, FpeFx.Kind.RING_SHOCK, FpeUtil.ahead(this, 1.5, 0.3), 0, 10, 3.0f, 0);
                        FpeUtil.sound(this, SoundEvents.PLAYER_ATTACK_KNOCKBACK, 1.4f, 0.5f);
                        setDeltaMovement(getDeltaMovement().scale(0.2));
                    }
                }));
        // hairwhip - spinning mane lash 13 (all around), the ahoge hardens into a blade: head-stab 24
        out.add(Ability.of("hairwhip", 40, 80).range(0, 6).weight(3)
                .tick((e, t, k) -> {
                    if (k == 2) FpeUtil.sound(this, SoundEvents.CAT_HISS, 1.3f, 0.6f);
                    if (k == 13) {
                        FpeUtil.hitRadius(this, position().add(0, 1.5, 0), 4.6, dmg(1.0f), 1.0, 0.3);
                        FpeUtil.arc(this, ParticleTypes.FLAME, position().add(0, 1.8, 0), getYRot(), 180, 3.6, 30);
                        slashArc(0, 1.8, 4.6f, 359, HAIRC, 0);
                        FpeUtil.sound(this, SoundEvents.PLAYER_ATTACK_SWEEP, 1.4f, 1.2f);
                    }
                    if (k == 17) FpeUtil.sound(this, SoundEvents.TRIDENT_RETURN, 1.2f, 1.4f);
                    if (k == 23) dashForward(0.55, getDeltaMovement().y);
                    if (k == 24) {
                        FpeUtil.hitLine(this, position().add(0, 3.2, 0), FpeUtil.ahead(this, 5.2, 1.4), 0.9, dmg(1.4f), 1.2, 0.3);
                        FpeUtil.particles(this, ParticleTypes.CRIT, FpeUtil.ahead(this, 3.5, 1.8), 12, 0.3, 0.3, 0.3, 0.3);
                        FpeUtil.sound(this, SoundEvents.TRIDENT_HIT, 1.4f, 0.7f);
                    }
                }));
    }

    // ------------------------------------------------------------------ sounds
    @Override protected SoundEvent getAmbientSound() { return isEnraged() ? SoundEvents.WARDEN_AMBIENT : SoundEvents.FOX_SNIFF; }
    @Override protected SoundEvent getHurtSound(DamageSource s) { return isEnraged() ? SoundEvents.WARDEN_HURT : SoundEvents.FOX_HURT; }
    @Override protected SoundEvent getDeathSound() { return SoundEvents.FOX_DEATH; }
    @Override protected void playStepSound(BlockPos p, BlockState b) { playSound(SoundEvents.SPIDER_STEP, 0.35f, isEnraged() ? 0.9f : 1.3f); }
}
