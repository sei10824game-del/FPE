package com.fpe.entity.characters;

import java.util.List;
import com.fpe.entity.*;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.*;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.Vec3;

/** Image-based Zombie AU roster. Combat moves are original to this mod. */
public final class ZombieAuCharacter extends FpeEntity {
    public enum Role {
        SURVIVOR_GRACE("survivor_grace", 2.4f, 180, 8, "gun"),
        SURVIVOR_DEMI("survivor_demi", 2.1f, 130, 5, "medic"),
        SURVIVOR_SASHA("survivor_sasha", 2f, 130, 5, "medic"),
        SURVIVOR_THAVEL("survivor_thavel", 2.6f, 240, 11, "claw"),
        SURVIVOR_CIRCLE("survivor_circle", 3f, 300, 13, "chainsaw"),
        SURVIVOR_BLOOMIE("survivor_bloomie", 2.25f, 190, 10, "cleaver"),
        SURVIVOR_ALICE("survivor_alice", 2.5f, 250, 12, "claw"),
        SURVIVOR_RILEY("survivor_riley", 1.75f, 120, 7, "knife"),
        SURVIVOR_BUBBLE("survivor_bubble", 1.8f, 120, 5, "medic"),
        SURVIVOR_LIZZY("survivor_lizzy", 1.9f, 130, 7, "gun"),
        SURVIVOR_KEVIN("survivor_kevin", 1.9f, 150, 6, "shield"),
        SURVIVOR_OLIVER("survivor_oliver", 2.1f, 170, 9, "knife"),
        ZOMBIE_OLIVER("zombie_oliver", 2.2f, 190, 9, "monster"),
        ZOMBIE_ZIP("zombie_zip", 2.5f, 200, 9, "monster"),
        ZOMBIE_EDWARD("zombie_edward", 2.2f, 200, 9, "monster"),
        ZOMBIE_ROBBY("zombie_robby", 2.6f, 180, 9, "monster"),
        ZOMBIE_SKELL("zombie_skell", 3.8f, 380, 14, "monster"),
        ZOMBIE_LANA("zombie_lana", 2.15f, 170, 8, "monster"),
        ZOMBIE_ABBIE("zombie_abbie", 3.4f, 270, 12, "monster"),
        ZOMBIE_PETUNIA("zombie_petunia", 2.15f, 170, 8, "monster"),
        ZOMBIE_CUBBIE("zombie_cubbie", 2.8f, 240, 10, "monster");
        public final String id, style;
        public final float height;
        public final double health, damage;
        Role(String id, float height, double health, double damage, String style) {
            this.id=id; this.height=height; this.health=health; this.damage=damage; this.style=style;
        }
        public boolean survivor() { return id.startsWith("survivor_"); }
        public boolean medic() { return style.equals("medic"); }
        public static Role byId(String id) { return valueOf(id.toUpperCase(java.util.Locale.ROOT)); }
    }
    private final Role role;
    private LivingEntity held;
    private Vec3 grabOrigin = Vec3.ZERO;
    public ZombieAuCharacter(EntityType<? extends FpeEntity> type, Level level, Role role) { super(type, level); this.role=role; }
    public Role role() { return role; }
    public static AttributeSupplier.Builder attributes(Role role) {
        return baseAttributes(role.health, role.damage, role == Role.ZOMBIE_ROBBY ? .36 : .29, role.survivor()?4:2, role.height>3?.5:.2);
    }
    @Override public Faction faction() { return role.survivor()?Faction.SURVIVOR:Faction.ZOMBIE_AU; }
    @Override public boolean protectsPlayer(Player player) { return role.survivor(); }
    @Override public double preferredDistance() { return role.style.equals("gun")?7:2; }
    @Override public boolean meleeFocus() { return !role.style.equals("gun"); }
    @Override public AABB getBoundingBoxForCulling() { return super.getBoundingBoxForCulling().inflate(role==Role.ZOMBIE_SKELL?3:1.8,1,1.8); }
    private double reach() { return role.height>3?4:3; }
    @Override protected void registerAbilities(List<Ability> out) {
        out.add(Ability.of("sweep",34,48).range(0,reach()+1).weight(4).faceUntil(10).tick((e,t,k)->{if(k==14)cut(1,75,.5,.1);}));
        out.add(Ability.of("double_strike",42,72).range(0,reach()+1).weight(3).faceUntil(9).tick((e,t,k)->{if(k==12||k==26)cut(.8f,65,.3,.1);}));
        out.add(Ability.of("lunge",36,85).range(2,9).weight(3).closer().faceUntil(10).tick((e,t,k)->{if(k==10)dashForward(Math.min(1.1,distanceTo(t)*.16),.1); if(k==16)cut(1.2f,45,.7,.1);}));
        out.add(Ability.of("grab",42,120).range(0,reach()+1).weight(2).faceUntil(10)
                .end((e,t,k)->held=null).tick((e,t,k)->grab(t,k)));
        out.add(Ability.of("slam",44,100).range(0,reach()+1).weight(3).faceUntil(15).tick((e,t,k)->{if(k==22)cut(1.5f,110,.9,.35);}));
        out.add(Ability.of("uppercut",32,65).range(0,reach()).weight(3).faceUntil(10).tick((e,t,k)->{if(k==14)cut(1.1f,50,.3,.6);}));
        out.add(Ability.of("backstep",36,85).range(0,reach()+1).weight(2).faceUntil(10).tick((e,t,k)->{if(k==12)cut(.8f,85,.7,.1);if(k==16)dashForward(-.65,.15);}));
        out.add(Ability.of("leap",46,115).range(3,11).weight(2).closer().faceUntil(12).tick((e,t,k)->{if(k==12)dashForward(Math.min(1.2,distanceTo(t)*.15),.5);if(k==26)cut(1.4f,85,.8,.2);}));
        out.add(Ability.of("volley",42,115).range(4,17).weight(role.style.equals("gun")?5:1).faceUntil(18).tick((e,t,k)->{if(k==18||k==24||k==30)shoot(t);}));
        out.add(Ability.of("signature",54,180).range(0,role.medic()?12:reach()+4).weight(4).faceUntil(18).tick((e,t,k)->{
            if(role.medic()) { if(k==24)healAllies(); }
            else if(role.style.equals("gun")) {if(k==24||k==32)shoot(t);}
            else if(role.style.equals("shield")) {if(k==24)addEffect(new MobEffectInstance(MobEffects.DAMAGE_RESISTANCE,80,1));if(k==32)cut(1.2f,100,1.4,.15);}
            else if(k==24||k==32)signature(t,k);
        }));
        out.add(Ability.of("rally",44,220).range(0,10).weight(2).faceUntil(16).tick((e,t,k)->{if(k==20)rally();}));
        out.add(Ability.of("frenzy",66,180).range(0,reach()+1).weight(4).faceUntil(9).when(FpeEntity::isEnraged).tick((e,t,k)->{if(k==14||k==30||k==46)cut(1.05f,100,.5,.2);}));
    }
    @Override public void cancelAbility() { held=null; super.cancelAbility(); }
    @Override protected void onAbilityStart(Ability ability, LivingEntity target) { held=null; }
    private void grab(LivingEntity target, int tick) {
        if(tick==12 && FpeCombat.cone(this,reach(),45).contains(target) && hasLineOfSight(target)
                && FpeUtil.hit(this,target,dmg(.4f),0,0)) {
            held=target; grabOrigin=target.position();
        }
        if(held!=target || !FpeUtil.canHurt(this,target)) { held=null; return; }
        if(tick>=13 && tick<=23) {
            double separation=(getBbWidth()+target.getBbWidth())*.5+.45;
            Vec3 next=grabOrigin.lerp(FpeUtil.ahead(this,separation,.08),(tick-12)/11.0);
            AABB path=target.getBoundingBox().expandTowards(next.subtract(target.position()));
            if(hasLineOfSight(target) && level().getWorldBorder().isWithinBounds(path) && level().noCollision(target,path))
                FpeUtil.holdAt(target,next);
            else held=null;
        }
        if(tick==26) {
            if(distanceTo(target)<reach() && hasLineOfSight(target))FpeUtil.hit(this,target,dmg(1.4f),1,.2);
            held=null;
        }
    }
    private void cut(float multiplier, float angle, double knock, double up) {
        for(LivingEntity v:FpeCombat.cone(this,reach(),angle)) {
            if(hasLineOfSight(v) && FpeUtil.hit(this,v,dmg(multiplier),knock,up) && !role.survivor())
                v.addEffect(new MobEffectInstance(MobEffects.POISON,50,0),this);
        }
        FpeCombat.slashArc(this,(float)reach(),angle*2,-20,0,getBbHeight()*.5,role.survivor()?0xFFE2E9DF:0xFF91EF42);
        FpeUtil.sound(this,SoundEvents.PLAYER_ATTACK_SWEEP,.8f,role.height>3?.6f:1);
    }
    private void signature(LivingEntity target, int tick) {
        switch(role) {
            case ZOMBIE_EDWARD -> { if(tick==24)for(int i=-1;i<=1;i++) {
                Vec3 from=FpeUtil.ahead(this,.5,getBbHeight()*.7);
                FpeUtil.projectile(this,FpeProjectile.Kind.BILE,from,FpeCombat.rotY(FpeUtil.aim(from,target,1.2,.1),i*14),dmg(.6f));
            } }
            case ZOMBIE_SKELL -> { cut(.9f,150,1.8,.45); FpeUtil.particles(this,ParticleTypes.CLOUD,getEyePosition(),25,1,1,1,.08); }
            case ZOMBIE_ROBBY -> { if(tick==24)dashForward(.9,.1); else cut(1.6f,35,.8,.1); }
            case ZOMBIE_ZIP, ZOMBIE_PETUNIA -> { if(tick==24)dashForward(.75,.45); else cut(1.6f,100,.8,.25); }
            case ZOMBIE_CUBBIE -> {
                cut(.9f,100,.4,.1);
                for(LivingEntity v:FpeCombat.cone(this,reach(),100))if(hasLineOfSight(v))
                    v.addEffect(new MobEffectInstance(MobEffects.BLINDNESS,45,0),this);
            }
            case ZOMBIE_ABBIE -> { if(tick==24) {
                for(LivingEntity v:FpeCombat.cone(this,5,45))if(hasLineOfSight(v) && FpeUtil.hit(this,v,dmg(.6f),0,0)) {
                    Vec3 pull=position().subtract(v.position()).normalize().scale(.45);
                    v.setDeltaMovement(pull.x,.1,pull.z);v.hurtMarked=true;
                }
            } else cut(1.4f,70,.8,.2); }
            case ZOMBIE_LANA -> { cut(1.1f,120,.3,.1); }
            default -> cut(role.style.equals("chainsaw")?1.2f:1.05f,90,.4,.12);
        }
    }
    private void shoot(LivingEntity target) {
        Vec3 from=FpeUtil.ahead(this,.5,getBbHeight()*.7);
        FpeUtil.projectile(this, role.style.equals("gun")?FpeProjectile.Kind.BULLET:!role.survivor()?FpeProjectile.Kind.BILE:FpeProjectile.Kind.KNIFE,from,FpeUtil.aim(from,target,role.style.equals("gun")?2.2:1.3,.1),dmg(.65f));
        FpeUtil.sound(this,SoundEvents.ARROW_SHOOT,.8f,1.3f);
    }
    private boolean supported(LivingEntity v) {
        return v instanceof Player p && !p.isSpectator() || v instanceof ZombieAuCharacter z && z.role.survivor();
    }
    private void healAllies() {
        for(LivingEntity v:level().getEntitiesOfClass(LivingEntity.class,getBoundingBox().inflate(8),this::supported)) {
            if(distanceToSqr(v)<=64 && hasLineOfSight(v)) {
                v.heal(6); v.removeEffect(MobEffects.POISON);
                FpeUtil.particles(this,ParticleTypes.HAPPY_VILLAGER,v.position().add(0,1,0),8,.3,.4,.3,.01);
            }
        }
        FpeUtil.sound(this,SoundEvents.AMETHYST_BLOCK_CHIME,1,1.2f);
    }
    private void rally() {
        if(role.survivor()) {
            for(LivingEntity v:level().getEntitiesOfClass(LivingEntity.class,getBoundingBox().inflate(6),this::supported))
                if(distanceToSqr(v)<=36 && hasLineOfSight(v))v.addEffect(new MobEffectInstance(MobEffects.DAMAGE_RESISTANCE,80,0),this);
        } else {
            for(LivingEntity v:FpeUtil.enemiesInRadius(this,position(),6,2,1))
                if(hasLineOfSight(v))v.addEffect(new MobEffectInstance(MobEffects.WEAKNESS,60,0),this);
        }
        FpeUtil.particles(this,role.survivor()?ParticleTypes.HAPPY_VILLAGER:ParticleTypes.SPORE_BLOSSOM_AIR,getEyePosition(),24,1,1,1,.03);
        FpeUtil.sound(this,role.survivor()?SoundEvents.NOTE_BLOCK_BELL.value():SoundEvents.ZOMBIE_AMBIENT,1,.75f);
    }
}
