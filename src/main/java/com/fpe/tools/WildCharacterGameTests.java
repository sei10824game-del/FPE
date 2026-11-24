package com.fpe.tools;

import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.HashSet;
import java.util.Set;

import com.fpe.entity.Ability;
import com.fpe.entity.FpeEntity;
import com.fpe.entity.FpeFx;
import com.fpe.entity.characters.CrazyOne;
import com.fpe.entity.characters.WildWolf;
import com.fpe.registry.ModEntities;
import com.fpe.registry.ModItems;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;

import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.entity.monster.Zombie;
import net.minecraftforge.common.ForgeSpawnEggItem;
import net.minecraftforge.gametest.GameTestHolder;
import net.minecraftforge.gametest.PrefixGameTestTemplate;

@GameTestHolder("fpe")
@PrefixGameTestTemplate(false)
public final class WildCharacterGameTests {
    @GameTest(template = "combat_empty")
    public static void savedCharactersAndEggsStayCompatible(GameTestHelper h) {
        var crazie = stationary(h, ModEntities.CRAZY_ONE.get(), 2, 2);
        var wolf = stationary(h, ModEntities.WILD_WOLF.get(), 8, 8);
        CompoundTag crazieTag = new CompoundTag(), wolfTag = new CompoundTag();
        crazie.save(crazieTag);
        wolf.save(wolfTag);
        h.assertTrue(crazieTag.getString("id").equals("fpe:crazy_one"), "Crazie must retain existing saved ID");
        h.assertTrue(wolfTag.getString("id").equals("fpe:wild_wolf"), "Werewolf must retain existing saved ID");
        h.assertTrue(EntityType.loadEntityRecursive(crazieTag, h.getLevel(), e -> e) instanceof CrazyOne,
                "Saved Crazie must reload as the registered character");
        h.assertTrue(EntityType.loadEntityRecursive(wolfTag, h.getLevel(), e -> e) instanceof WildWolf,
                "Saved werewolf must reload as the registered character");
        h.assertTrue(((ForgeSpawnEggItem) ModItems.CRAZY_ONE.get()).getType(null) == crazie.getType(),
                "Existing Crazie egg must create the updated character");
        h.assertTrue(((ForgeSpawnEggItem) ModItems.WILD_WOLF.get()).getType(null) == wolf.getType(),
                "Existing werewolf egg must create the updated character");
        h.assertTrue(!wolf.canFreeze(), "Werewolf must retain cold resistance");
        verifyModel(h, crazie, "crazy_one");
        verifyModel(h, wolf, "wild_wolf");
        h.succeed();
    }

    @GameTest(template = "combat_empty")
    public static void crazieKnifeWindowProtectsAlly(GameTestHelper h) {
        var crazie = stationary(h, ModEntities.CRAZY_ONE.get(), 5, 2);
        var ally = stationary(h, ModEntities.WILD_WOLF.get(), 6, 4);
        Zombie target = stationary(h, EntityType.ZOMBIE, 5, 4);
        float before = target.getHealth(), allyBefore = ally.getHealth();
        crazie.setTarget(target);
        h.assertTrue(crazie.forceAbility("frantic_flurry"), "Knife flurry must be registered");
        crazie.animTime = 9;
        crazie.tick();
        h.assertTrue(target.getHealth() == before, "Knife flurry must respect anticipation");
        crazie.tick();
        h.assertTrue(target.getHealth() < before, "Knife flurry must strike at tick 10");
        float afterFirst = target.getHealth();
        h.assertTrue(target.invulnerableTime > 0, "First contact must establish hurt immunity");
        crazie.animTime = 18;
        crazie.tick();
        h.assertTrue(target.getHealth() < afterFirst, "Eight-tick combo follow-up must connect through hurt immunity");
        h.assertTrue(ally.getHealth() == allyBefore, "Knife flurry must protect allied werewolf");
        h.succeed();
    }

    @GameTest(template = "combat_empty")
    public static void werewolfPickWindowProtectsAlly(GameTestHelper h) {
        var wolf = stationary(h, ModEntities.WILD_WOLF.get(), 5, 2);
        var ally = stationary(h, ModEntities.CRAZY_ONE.get(), 6, 5);
        Zombie target = stationary(h, EntityType.ZOMBIE, 5, 5);
        float before = target.getHealth(), allyBefore = ally.getHealth();
        wolf.setTarget(target);
        h.assertTrue(wolf.forceAbility("pick_smash"), "Pick smash must be registered");
        wolf.animTime = 20;
        wolf.tick();
        h.assertTrue(target.getHealth() == before, "Pick smash must respect wind-up");
        wolf.tick();
        h.assertTrue(target.getHealth() < before, "Pick smash must strike at tick 21");
        h.assertTrue(ally.getHealth() == allyBefore, "Pick smash must protect allied Crazie");
        h.succeed();
    }

    @GameTest(template = "combat_empty")
    public static void werewolfPhysicalAttacks(GameTestHelper h) {
        var wolf = stationary(h, ModEntities.WILD_WOLF.get(), 5, 2);
        var ally = stationary(h, ModEntities.CRAZY_ONE.get(), 5, 4);
        var target = stationary(h, EntityType.ZOMBIE, 5, 5);
        target.getAttribute(net.minecraft.world.entity.ai.attributes.Attributes.MAX_HEALTH).setBaseValue(100);
        target.setHealth(100);
        wolf.setTarget(target);
        float allyBefore = ally.getHealth();
        h.assertTrue(!wolf.forceAbility("ground_pick"), "Removed ground spikes must not be selectable");
        h.assertTrue(wolf.forceAbility("pick_thrust"), "Physical pick thrust must replace ground spikes");
        float before = target.getHealth();
        wolf.animTime = 17;
        wolf.tick();
        h.assertTrue(target.getHealth() == before, "Thrust must not hit during anticipation");
        wolf.tick();
        h.assertTrue(target.getHealth() < before, "Thrust must connect at tick 18");
        wolf.cancelAbility();
        target.invulnerableTime = 0;
        before = target.getHealth();
        h.assertTrue(wolf.forceAbility("claw_retreat"), "Retreating claw must be selectable");
        wolf.animTime = 12;
        wolf.tick();
        h.assertTrue(target.getHealth() == before, "Retreating claw must telegraph its strike");
        wolf.tick();
        h.assertTrue(target.getHealth() < before, "Retreating claw must connect at tick 13");
        wolf.animTime = 15;
        wolf.tick();
        h.assertTrue(wolf.getDeltaMovement().dot(com.fpe.entity.FpeUtil.forward(wolf)) < 0,
                "Retreat must move away after contact");
        h.assertTrue(ally.getHealth() == allyBefore, "New physical attacks must protect Crazie");
        h.succeed();
    }

    @GameTest(template = "combat_empty")
    public static void werewolfNeverSummonsGroundLimbs(GameTestHelper h) {
        var wolf = stationary(h, ModEntities.WILD_WOLF.get(), 5, 2);
        var target = stationary(h, EntityType.ZOMBIE, 5, 6);
        target.getAttribute(net.minecraft.world.entity.ai.attributes.Attributes.MAX_HEALTH).setBaseValue(2000);
        target.setHealth(2000);
        wolf.setTarget(target);
        var start = wolf.position();
        for (Ability ability : wolf.abilities()) {
            wolf.cancelAbility();
            h.assertTrue(wolf.forceAbility(ability.id), "Ability must be available: " + ability.id);
            for (int tick = 0; tick < ability.duration; tick++) {
                wolf.setPos(start);
                wolf.setDeltaMovement(net.minecraft.world.phys.Vec3.ZERO);
                wolf.tick();
            }
        }
        h.assertTrue(h.getLevel().getEntitiesOfClass(FpeFx.class, wolf.getBoundingBox().inflate(64),
                fx -> fx.getOwner() == wolf && (fx.kind() == FpeFx.Kind.SPIKE || fx.kind() == FpeFx.Kind.TENTACLE)).isEmpty(),
                "No werewolf ability may summon ground spikes or tentacles");
        h.succeed();
    }

    private static void verifyModel(GameTestHelper h, FpeEntity actor, String id) {
        try (InputStream stream = WildCharacterGameTests.class.getResourceAsStream("/assets/fpe/bbmodels/" + id + ".bbmodel")) {
            h.assertTrue(stream != null, id + " model must be packaged");
            JsonObject model = JsonParser.parseReader(new InputStreamReader(stream, StandardCharsets.UTF_8)).getAsJsonObject();
            Set<String> names = new HashSet<>();
            for (var element : model.getAsJsonArray("animations")) {
                JsonObject animation = element.getAsJsonObject();
                names.add(animation.get("name").getAsString());
            }
            h.assertTrue(names.containsAll(Set.of("idle", "walk", "death")), id + " needs lifecycle animations");
            for (Ability ability : actor.abilities()) {
                h.assertTrue(names.contains(ability.id), id + " missing attack animation " + ability.id);
                JsonObject animation = model.getAsJsonArray("animations").asList().stream()
                        .map(e -> e.getAsJsonObject()).filter(a -> a.get("name").getAsString().equals(ability.id)).findFirst().orElseThrow();
                h.assertTrue(animation.get("length").getAsDouble() * 20 + 0.01 >= ability.duration,
                        id + " animation too short: " + ability.id);
                h.assertTrue(!animation.getAsJsonObject("animators").entrySet().isEmpty(), id + " attack must have authored motion: " + ability.id);
            }
        } catch (java.io.IOException e) {
            throw new IllegalStateException("Cannot load " + id, e);
        }
    }

    private static <T extends Mob> T stationary(GameTestHelper h, EntityType<T> type, int x, int z) {
        T actor = h.spawn(type, x, 2, z);
        actor.setNoAi(true);
        actor.setNoGravity(true);
        return actor;
    }
}
