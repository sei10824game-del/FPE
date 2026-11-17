package com.fpe.entity.characters;

import java.util.List;

import com.fpe.entity.Ability;
import com.fpe.entity.FpeEntity;
import com.fpe.entity.FpeCombat;
import com.fpe.entity.FpeProjectile;
import com.fpe.entity.FpeUtil;

import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.sounds.SoundEvent;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.Vec3;

/** Crazie, retaining crazy_one as the saved entity id. Knife/body moves are mod-original,
 * not claims about canon powers. Legacy ability ids remain for compatibility; wrench_smash
 * now means an overhead knife strike. All hit ticks match crazy_one.bbmodel animations. */
public class CrazyOne extends FpeEntity {
    public CrazyOne(EntityType<? extends FpeEntity> type, Level level) { super(type, level); }
    @Override public Faction faction() { return Faction.WILD; }
    public static AttributeSupplier.Builder attributes() { return baseAttributes(130, 7, 0.37, 2, 0.2); }
    @Override public double preferredDistance() { return 1.4; }
    @Override public boolean meleeFocus() { return true; }
    @Override protected int restTicks() { return isEnraged() ? 7 : 12; }
    @Override protected SoundEvent getAmbientSound() { return SoundEvents.WITCH_CELEBRATE; }
    @Override protected SoundEvent getHurtSound(DamageSource s) { return SoundEvents.VILLAGER_HURT; }
    @Override protected SoundEvent getDeathSound() { return SoundEvents.WITCH_DEATH; }
    @Override public float getVoicePitch() { return 1.5f; }

    private static void slash(FpeEntity e, double range, double angle, float mult, double knock) {
        slash(e, range, angle, mult, knock, false);
    }

    /** Only the follow-up contacts of intentional eight-tick combos bypass hurt immunity. */
    private static void slash(FpeEntity e, double range, double angle, float mult, double knock, boolean followUp) {
        FpeCombat.cut(e, range, angle, e.dmg(mult), knock, 0.15, 0, followUp);
        FpeUtil.sound(e, SoundEvents.PLAYER_ATTACK_SWEEP, 0.8f, 1.3f);
        FpeUtil.particles(e, ParticleTypes.CRIT, FpeUtil.ahead(e, 1.6, 1.0), 5, 0.2, 0.2, 0.2, 0.05);
    }

    @Override protected void registerAbilities(List<Ability> out) {
        out.add(Ability.of("frantic_flurry", 40, 75).range(0, 3).weight(3).faceUntil(8).tick((e,t,k)->{
            if(k==10 || k==18 || k==26) slash(e,2.7,65,0.65f,0.25,k>10);
        }));
        out.add(Ability.of("wrench_smash",34,65).range(0,3.3).weight(3).faceUntil(12).tick((e,t,k)->{
            if(k==17) slash(e,3.0,45,1.5f,0.9);
        }));
        out.add(Ability.of("zigzag_dash",40,95).range(3,10).weight(2).closer().moving().faceUntil(4).tick((e,t,k)->{
            if(k==6 || k==14 || k==22) {
                e.snapFace(t);
                Vec3 side=FpeUtil.right(e).scale(k==14 ? -0.35 : 0.35);
                e.setDeltaMovement(FpeUtil.forward(e).scale(0.75).add(side).add(0,0.08,0)); e.hasImpulse=true;
            }
            if(k==10 || k==18 || k==26) slash(e,2.4,65,0.6f,0.25,k>10);
        }));
        out.add(Ability.of("cackle",44,120).range(0,3).weight(1).faceUntil(12).tick((e,t,k)->{
            if(k==14) FpeUtil.sound(e,SoundEvents.WITCH_CELEBRATE,1.2f,1.4f);
            if(k==24) slash(e,2.5,65,0.8f,0.7);
        }));
        out.add(Ability.of("junk_throw",34,90).range(4,12).weight(1).faceUntil(14).tick((e,t,k)->{
            if(k==15 || k==19 || k==23) {
                Vec3 from=FpeUtil.ahead(e,0.75,1.3);
                FpeUtil.projectile(e,FpeProjectile.Kind.KNIFE,from,FpeUtil.aim(from,t,1.1,0.2),e.dmg(0.6f));
                FpeUtil.sound(e,SoundEvents.TRIDENT_THROW,0.6f,1.5f);
            }
        }));
        out.add(Ability.of("tantrum",40,100).range(0,2.8).weight(2).faceUntil(8).tick((e,t,k)->{
            if(k==16 || k==24) {
                for (LivingEntity victim : FpeUtil.enemiesInRadius(e,e.position(),2.2,2.5,1.0)) {
                    if (k == 24) victim.invulnerableTime = 0;
                    FpeUtil.hit(e,victim,e.dmg(0.65f),0.45,0.12);
                }
                FpeUtil.sound(e,SoundEvents.PLAYER_ATTACK_KNOCKBACK,0.8f,1.2f);
            }
        }));
        out.add(Ability.of("jump_scare",36,100).range(3,9).weight(2).closer().moving().faceUntil(8).tick((e,t,k)->{
            if(k==8) e.dashToward(t.position(),0.8,0.32);
            if(k==20) slash(e,2.8,55,1.3f,0.8);
        }));
        out.add(Ability.of("meltdown",60,180).range(0,7).weight(3).closer().moving().when(FpeEntity::isEnraged).faceUntil(6).tick((e,t,k)->{
            if(k==8 || k==24 || k==40) { e.snapFace(t); e.dashForward(0.7,0.08); }
            if(k==12 || k==28 || k==44) slash(e,2.6,70,0.8f,0.4);
        }));
        out.add(Ability.of("reverse_cut",30,65).range(0,3).weight(3).faceUntil(7).tick((e,t,k)->{
            if(k==12) slash(e,2.8,70,0.95f,0.4);
        }));
        out.add(Ability.of("heel_kick",32,75).range(0,2.8).weight(2).faceUntil(8).tick((e,t,k)->{
            if(k==14) slash(e,2.5,45,0.9f,1.0);
        }));
        out.add(Ability.of("knife_lunge",36,90).range(2.5,8).weight(2).closer().moving().faceUntil(7).tick((e,t,k)->{
            if(k==10) e.dashToward(t.position(),0.85,0.1);
            if(k==16) slash(e,3.0,35,1.25f,0.7);
        }));
        out.add(Ability.of("low_sweep",38,85).range(0,3.3).weight(2).faceUntil(10).tick((e,t,k)->{
            if(k==18) slash(e,3.0,80,1.0f,0.6);
        }));
    }
}
