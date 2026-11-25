package com.fpe.tools;

import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.HashMap;
import java.util.UUID;
import com.fpe.entity.*;
import com.fpe.entity.characters.ZombieAuCharacter;
import com.fpe.entity.characters.ZombieAuCharacter.Role;
import com.fpe.registry.ModEntities;
import com.fpe.registry.ModItems;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import com.mojang.authlib.GameProfile;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.level.GameType;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.phys.Vec3;
import net.minecraftforge.common.ForgeSpawnEggItem;
import net.minecraftforge.common.util.FakePlayerFactory;
import net.minecraftforge.gametest.GameTestHolder;
import net.minecraftforge.gametest.PrefixGameTestTemplate;

@GameTestHolder("fpe")
@PrefixGameTestTemplate(false)
public final class ZombieAuGameTests {
    @GameTest(template="combat_empty")
    public static void approvedRosterSavesAndEggsRestoreIdentity(GameTestHelper h) {
        h.assertTrue(Role.values().length==21,"Approved roster has 21 characters");
        int survivors=0;
        for(Role role:Role.values()) {
            if(role.survivor())survivors++;
            var actor=actor(h,role,5,5);
            CompoundTag tag=new CompoundTag(); actor.save(tag);
            h.assertTrue(tag.getString("id").equals("fpe:"+role.id),"Each character needs its own saved entity ID");
            var restored=EntityType.loadEntityRecursive(tag,h.getLevel(),e->e);
            h.assertTrue(restored instanceof ZombieAuCharacter z && z.role()==role,"Reload must preserve role");
            var egg=(ForgeSpawnEggItem)ModItems.ZOMBIE_AU.get(role).get();
            h.assertTrue(egg.getType(null)==actor.getType(),"Egg must spawn matching character");
            h.assertTrue(!java.util.List.of("survivor_zip","survivor_engel","survivor_claire","survivor_chip","survivor_emily","survivor_edward").contains(role.id),"Excluded survivors must not be added");
            actor.discard();
        }
        h.assertTrue(survivors==12,"Roster must contain twelve survivors and nine zombies");h.succeed();
    }

    @GameTest(template="combat_empty")
    public static void everyModelCoversTwelveRuntimeAttacks(GameTestHelper h) {
        for(Role role:Role.values()) {
            var actor=actor(h,role,5,5);
            h.assertTrue(actor.abilities().size()==12,"Each role needs twelve attacks");
            try(var stream=ZombieAuGameTests.class.getResourceAsStream("/assets/fpe/bbmodels/"+role.id+".bbmodel")) {
                h.assertTrue(stream!=null,"Missing packaged model: "+role.id);
                var model=JsonParser.parseReader(new InputStreamReader(stream,StandardCharsets.UTF_8)).getAsJsonObject();
                var animations=new HashMap<String,JsonObject>();
                for(var entry:model.getAsJsonArray("animations")){var a=entry.getAsJsonObject();animations.put(a.get("name").getAsString(),a);}
                h.assertTrue(animations.keySet().containsAll(java.util.List.of("idle","walk","death")),"Lifecycle animations required");
                for(var ability:actor.abilities()) {
                    h.assertTrue(animations.containsKey(ability.id),role.id+" missing "+ability.id);
                    var a=animations.get(ability.id);
                    h.assertTrue(a.get("length").getAsDouble()*20+.01>=ability.duration,"Animation must cover attack duration");
                    h.assertTrue(!a.getAsJsonObject("animators").entrySet().isEmpty(),"Every attack must animate");
                }
            }catch(java.io.IOException e){throw new IllegalStateException(e);}
            actor.discard();
        }
        h.succeed();
    }

    @GameTest(template="combat_empty")
    public static void survivorAndZombieRelationshipsAreSymmetric(GameTestHelper h) {
        var survivor=actor(h,Role.SURVIVOR_OLIVER,3,3);var zombie=actor(h,Role.ZOMBIE_OLIVER,3,5);
        var fellow=actor(h,Role.SURVIVOR_GRACE,6,3);var infected=actor(h,Role.ZOMBIE_LANA,6,5);
        h.assertTrue(survivor.canAttack(zombie)&&zombie.canAttack(survivor),"Survivors and zombies must fight both ways");
        h.assertTrue(!survivor.canAttack(fellow)&&!zombie.canAttack(infected),"Each AU group must protect its own members");
        for(var faction:FpeEntity.Faction.values())for(var added:java.util.List.of(FpeEntity.Faction.SURVIVOR,FpeEntity.Faction.ZOMBIE_AU))
            h.assertTrue(FpeEntity.hostile(added,faction)==FpeEntity.hostile(faction,added),"New faction relationships must be symmetric");
        h.succeed();
    }

    @GameTest(template="combat_empty")
    public static void survivorAttacksProtectSurvivalPlayers(GameTestHelper h) {
        var survivor=actor(h,Role.SURVIVOR_GRACE,3,3);
        var player=FakePlayerFactory.get(h.getLevel(),new GameProfile(UUID.randomUUID(),"ZombieAuFriend"));
        player.setGameMode(GameType.SURVIVAL);player.setHealth(20);
        player.setPos(survivor.getX(),survivor.getY(),survivor.getZ()+1);
        var shot=new FpeProjectile(ModEntities.PROJECTILE.get(),h.getLevel());shot.setOwner(survivor);
        var fx=new FpeFx(ModEntities.FX.get(),h.getLevel());fx.setOwner(survivor);
        h.assertTrue(!player.isCreative()&&!player.isSpectator(),"Friendliness must be tested against vulnerable players");
        h.assertTrue(!survivor.canAttack(player)&&!FpeUtil.canHurt(survivor,player),"Survivors must not select or hurt players");
        h.assertTrue(!FpeUtil.canHurt(shot,player)&&!FpeUtil.canHurt(fx,player),"Projectile and area effect owners must preserve player protection");
        h.assertTrue(!FpeUtil.hit(survivor,player,10,0,0)&&player.getHealth()==20,"Direct attacks must also preserve health");
        var zombie=actor(h,Role.ZOMBIE_OLIVER,6,6);
        h.assertTrue(FpeUtil.canHurt(zombie,player),"Zombie attacks must still threaten survival players");
        h.succeed();
    }

    @GameTest(template="combat_empty")
    public static void medicsHealSurvivorsAndPlayersButNotZombies(GameTestHelper h) {
        var medic=actor(h,Role.SURVIVOR_BUBBLE,5,2);var friend=actor(h,Role.SURVIVOR_RILEY,4,4);var zombie=actor(h,Role.ZOMBIE_LANA,6,4);
        friend.setHealth(20);friend.addEffect(new MobEffectInstance(MobEffects.POISON,100));zombie.setHealth(20);
        var player=FakePlayerFactory.get(h.getLevel(),new GameProfile(UUID.randomUUID(),"ZombieAuPatient"));
        player.setGameMode(GameType.SURVIVAL);player.setPos(h.absoluteVec(new Vec3(5,2,4)));player.setHealth(8);
        h.getLevel().addNewPlayer(player);
        medic.setTarget(zombie);medic.forceAbility("signature");medic.animTime=23;medic.tick();
        h.assertTrue(friend.getHealth()==20&&player.getHealth()==8,"Healing needs a visible windup");
        medic.tick();
        h.assertTrue(friend.getHealth()==26&&!friend.hasEffect(MobEffects.POISON),"Medic must heal and cleanse an allied survivor");
        h.assertTrue(player.getHealth()==14,"Medic must heal a nearby survival player");
        h.assertTrue(zombie.getHealth()==20,"Medical support must not heal the opposing zombies");
        player.discard();h.succeed();
    }

    @GameTest(template="combat_empty")
    public static void medicHealingCannotPassThroughWalls(GameTestHelper h) {
        var medic=actor(h,Role.SURVIVOR_DEMI,5,2);var friend=actor(h,Role.SURVIVOR_RILEY,5,7);var zombie=actor(h,Role.ZOMBIE_LANA,2,3);
        friend.setHealth(20);friend.addEffect(new MobEffectInstance(MobEffects.POISON,100));
        wall(h,4);medic.setTarget(zombie);medic.forceAbility("signature");medic.animTime=24;medic.tick();
        h.assertTrue(friend.getHealth()==20&&friend.hasEffect(MobEffects.POISON),"Cover must block both healing and cleansing");
        h.assertBlockPresent(Blocks.STONE,5,3,4);h.succeed();
    }

    @GameTest(template="combat_empty")
    public static void zombieContactPoisonsEnemyAndProtectsOtherZombies(GameTestHelper h) {
        var zombie=actor(h,Role.ZOMBIE_OLIVER,5,2);var friend=actor(h,Role.ZOMBIE_LANA,4,4);var target=actor(h,Role.SURVIVOR_OLIVER,5,4);
        zombie.setTarget(target);zombie.forceAbility("sweep");zombie.animTime=13;zombie.tick();
        h.assertTrue(target.getHealth()==target.getMaxHealth()&&!target.hasEffect(MobEffects.POISON),"Poison must wait for attack contact");
        zombie.tick();
        h.assertTrue(target.getHealth()<target.getMaxHealth()&&target.hasEffect(MobEffects.POISON),"Landed zombie melee must damage and poison");
        h.assertTrue(friend.getHealth()==friend.getMaxHealth()&&!friend.hasEffect(MobEffects.POISON),"Zombie allies must resist friendly strikes");
        h.succeed();
    }

    @GameTest(template="combat_empty")
    public static void survivorVolleyStopsAtSolidCover(GameTestHelper h) {
        var shooter=actor(h,Role.SURVIVOR_GRACE,5,2);var zombie=actor(h,Role.ZOMBIE_OLIVER,5,8);wall(h,4);
        shooter.setTarget(zombie);shooter.forceAbility("volley");shooter.animTime=18;shooter.tick();
        var shots=h.getLevel().getEntitiesOfClass(FpeProjectile.class,shooter.getBoundingBox().inflate(3),p->p.getOwner()==shooter);
        h.assertTrue(!shots.isEmpty(),"Volley contact must spawn a projectile");
        for(var shot:shots){for(int i=0;i<8&&!shot.isRemoved();i++)shot.tick();h.assertTrue(shot.isRemoved(),"Bullet must terminate at cover");}
        h.assertTrue(zombie.getHealth()==zombie.getMaxHealth(),"Volley must not shoot through solid walls");
        h.assertBlockPresent(Blocks.STONE,5,3,4);h.succeed();
    }

    @GameTest(template="combat_empty")
    public static void bilePassesAlliesAndPoisonsEnemyOnContact(GameTestHelper h) {
        var owner=actor(h,Role.ZOMBIE_LANA,1,5);
        var ally=actor(h,Role.ZOMBIE_OLIVER,5,5);
        var target=actor(h,Role.SURVIVOR_OLIVER,7,5);
        ally.setPos(h.absoluteVec(new Vec3(5.5,2,5.5)));
        target.setPos(h.absoluteVec(new Vec3(7.5,2,5.5)));
        var shot=FpeUtil.projectile(owner,FpeProjectile.Kind.BILE,
                h.absoluteVec(new Vec3(4.5,3.2,5.5)),new Vec3(3,0,0),10);
        h.assertTrue(!target.hasEffect(MobEffects.POISON),"Bile must wait for a real projectile collision");
        shot.tick();
        h.assertTrue(shot.isRemoved(),"Bile must terminate at the enemy contact");
        h.assertTrue(target.getHealth()<target.getMaxHealth()&&target.hasEffect(MobEffects.POISON),
                "Bile projectile must damage and poison the survivor on contact");
        h.assertTrue(ally.getHealth()==ally.getMaxHealth()&&!ally.hasEffect(MobEffects.POISON),
                "Bile must pass through allied zombies without damage or poison");
        h.succeed();
    }

    private static ZombieAuCharacter actor(GameTestHelper h,Role role,int x,int z) {
        var actor=h.spawn(ModEntities.ZOMBIE_AU.get(role).get(),x,2,z);actor.setNoAi(true);actor.setNoGravity(true);return actor;
    }
    private static void wall(GameTestHelper h,int z) {
        for(int x=3;x<=7;x++)for(int y=2;y<=7;y++)h.setBlock(x,y,z,Blocks.STONE);
    }
}
