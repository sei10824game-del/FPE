package com.fpe.entity.characters;

import java.util.List;
import java.util.UUID;

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
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.ai.attributes.AttributeInstance;
import net.minecraft.world.entity.ai.attributes.AttributeModifier;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.state.BlockState;
import net.minecraft.world.phys.Vec3;

/**
 * Fen - a towering (3.6 block) feral girl whose ink-black arms reshape at will into monstrous weapons:
 * scythes, a whip, needle fans, wings, shields, a mace, a fanged maw, a hooked chain and six extra spider arms.
 * Below 50 % health (or with stance 1) she becomes the black, red-eyed MONSTER (stance 1, m_* abilities).
 */
public class Fen extends FpeEntity {
    private static final UUID MONSTER_SPEED = UUID.fromString("5e1f7a62-3c0b-4f1e-9a7d-6f0c2b8e4a11");
    private static final int DARK = 0xE0141018, RED = 0xE08A1020, BLOOD = 0xE0D02030;

    private boolean struck, guarding;
    private int monsterT;
    @Nullable private LivingEntity grabbed;

    public Fen(EntityType<? extends FpeEntity> type, Level level) { super(type, level); }

    @Override public Faction faction() { return Faction.STUDENT; }
    @Override public boolean meleeFocus() { return true; }
    @Override protected boolean hasBossBar() { return true; }

    public static AttributeSupplier.Builder attributes() { return baseAttributes(260, 11, 0.33, 8, 0.6); }

    @Override public double preferredDistance() { return 1.8; }
    @Override protected int restTicks() { return monster() ? 5 : isEnraged() ? 8 : 14; }

    private boolean monster() { return getStance() == 1; }
    private static Ability human(String id, int dur, int cd) { return Ability.of(id, dur, cd).when(e -> e.getStance() == 0); }
    private static Ability beast(String id, int dur, int cd) { return Ability.of(id, dur, cd).when(e -> e.getStance() == 1); }

    // ------------------------------------------------------------------ monster mode
    @Override
    public void tick() {
        super.tick();
        setMaxUpStep(1.1f);
        if (level().isClientSide || !isAlive()) return;
        if (!monster() && monsterT == 0 && getHealth() <= getMaxHealth() * 0.5f && !"transform".equals(currentAbilityId())) {
            cancelAbility();
            forceAbility("transform");
        }
        String cur = currentAbilityId();
        if (monsterT > 0 && !monster() && !"transform".equals(cur)) setStance(1); // transform interrupted (target lost)
        if (guarding && !"guard".equals(cur)) guarding = false;
        AttributeInstance sp = getAttribute(Attributes.MOVEMENT_SPEED);
        if (sp != null && monster() != (sp.getModifier(MONSTER_SPEED) != null)) {
            if (monster()) sp.addTransientModifier(new AttributeModifier(MONSTER_SPEED, "fen monster", 0.3, AttributeModifier.Operation.MULTIPLY_TOTAL));
            else sp.removeModifier(MONSTER_SPEED);
        }
        if (monster() && tickCount % 4 == 0) FpeUtil.particles(this, ParticleTypes.SQUID_INK, position().add(0, 1.6, 0), 1, 0.3, 0.8, 0.3, 0.01);
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

    private void spikeLine(int i, float h, float dmg) {
        Vec3 p = FpeUtil.ahead(this, 2.0 + i * 1.6, 0);
        FpeUtil.fx(this, FpeFx.Kind.SPIKE, p, 3, 22, 1.1f, dmg).param(h);
        FpeUtil.sound(this, SoundEvents.POINTED_DRIPSTONE_LAND, 1f, 0.6f + i * 0.08f);
    }

    @Override
    protected void registerAbilities(List<Ability> out) {
        // ================================================================== HUMAN FORM (stance 0)
        // scythe - both arms become mantis scythes: X-cross sweep 14, double overhead chop 24
        out.add(human("scythe", 40, 60).range(0, 5.5).weight(4)
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
        out.add(human("lash", 36, 70).range(3, 10).weight(3).closer()
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
        out.add(human("needles", 34, 80).range(4, 14).weight(2)
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
        out.add(human("wingglide", 44, 110).range(6, 22).weight(3).closer().moving().faceUntil(26)
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
        out.add(human("guard", 40, 140).range(0, 6).weight(2)
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
        out.add(human("hammer", 42, 90).range(0, 5.5).weight(3)
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
        out.add(human("spider", 46, 120).range(0, 5).weight(2)
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
        out.add(human("hook", 40, 100).range(4, 13).weight(3).closer().faceUntil(11)
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
        out.add(human("maw", 44, 120).range(0, 3.8).weight(2)
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
        out.add(human("pounce", 30, 70).range(3.5, 12).weight(3).closer().faceUntil(8)
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
        // transform - forced at <50 % hp: ink swallows her, becomes the black monster (stance 1) at tick 34, roar 46
        out.add(Ability.of("transform", 60, 9999).when(e -> false).blind()
                .tick((e, t, k) -> {
                    monsterT = 1;
                    if (k == 1) FpeUtil.sound(this, SoundEvents.WARDEN_HEARTBEAT, 2f, 0.6f);
                    if (k < 34 && k % 3 == 0) FpeUtil.particles(this, ParticleTypes.SQUID_INK, position().add(0, 1.8, 0), 6 + k / 3, 0.5, 1.0, 0.5, 0.04);
                    if (k == 20) FpeUtil.sound(this, SoundEvents.WARDEN_EMERGE, 1.4f, 1.2f);
                    if (k == 34) {
                        setStance(1);
                        addEffect(new MobEffectInstance(MobEffects.REGENERATION, 100, 1));
                        addEffect(new MobEffectInstance(MobEffects.DAMAGE_RESISTANCE, 100, 1));
                        FpeUtil.particles(this, ParticleTypes.LARGE_SMOKE, position().add(0, 1.4, 0), 40, 0.8, 1.2, 0.8, 0.05);
                    }
                    if (k == 46) {
                        FpeUtil.sound(this, SoundEvents.RAVAGER_ROAR, 2f, 0.6f);
                        FpeUtil.fx(this, FpeFx.Kind.RING_SHOCK, position().add(0, 0.1, 0), 0, 14, 7f, 0);
                        for (LivingEntity v : FpeUtil.enemiesInRadius(this, position(), 7, 2, 1)) {
                            FpeUtil.hit(this, v, dmg(0.5f), 1.4, 0.4);
                            v.addEffect(new MobEffectInstance(MobEffects.DARKNESS, 80, 0));
                        }
                    }
                }));

        // ================================================================== MONSTER FORM (stance 1)
        // m_frenzy - six savage alternating slashes 10..35, crossing finisher 42
        out.add(beast("m_frenzy", 48, 70).range(0, 5).weight(4)
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
        out.add(beast("m_impale", 40, 90).range(2, 14).weight(3).faceUntil(13)
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
        out.add(beast("m_lunge", 32, 60).range(3.5, 16).weight(3).closer().faceUntil(9)
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
        out.add(beast("m_tendrils", 50, 160).range(0, 9).weight(2).blind()
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
        out.add(beast("m_reap", 36, 80).range(0, 5.5).weight(3)
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
    }

    // ------------------------------------------------------------------ sounds
    @Override protected SoundEvent getAmbientSound() { return monster() ? SoundEvents.WARDEN_AMBIENT : SoundEvents.FOX_SNIFF; }
    @Override protected SoundEvent getHurtSound(DamageSource s) { return monster() ? SoundEvents.WARDEN_HURT : SoundEvents.FOX_HURT; }
    @Override protected SoundEvent getDeathSound() { return SoundEvents.FOX_DEATH; }
    @Override protected void playStepSound(BlockPos p, BlockState b) { playSound(SoundEvents.SPIDER_STEP, 0.35f, monster() ? 0.9f : 1.3f); }
}
