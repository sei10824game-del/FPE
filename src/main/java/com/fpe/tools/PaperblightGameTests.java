package com.fpe.tools;

import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.HashMap;
import java.util.Map;

import com.fpe.entity.FpeEntity;
import com.fpe.entity.characters.Paperblight;
import com.fpe.registry.ModEntities;
import com.fpe.registry.ModItems;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.monster.Zombie;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.phys.Vec3;
import net.minecraftforge.common.ForgeSpawnEggItem;
import net.minecraftforge.gametest.GameTestHolder;
import net.minecraftforge.gametest.PrefixGameTestTemplate;

@GameTestHolder("fpe")
@PrefixGameTestTemplate(false)
public final class PaperblightGameTests {
    @GameTest(template = "combat_empty")
    public static void formsAndEggSurviveReload(GameTestHelper h) {
        Paperblight boss = boss(h);
        h.assertTrue(((ForgeSpawnEggItem) ModItems.PAPERBLIGHT.get()).getType(null) == boss.getType(), "Egg must spawn Paperblight");
        for (int phase = 0; phase < 3; phase++) {
            boss.setVariant(phase);
            CompoundTag saved = new CompoundTag();
            boss.save(saved);
            h.assertTrue(saved.getString("id").equals("fpe:paperblight"), "Paperblight needs a stable saved ID");
            var restored = EntityType.loadEntityRecursive(saved, h.getLevel(), e -> e);
            h.assertTrue(restored instanceof Paperblight, "Saved boss must reload");
            Paperblight loaded = (Paperblight) restored;
            h.assertTrue(loaded.getVariant() == phase && !loaded.isEcho(), "Saved form must remain intact");
            h.assertTrue(Math.abs(loaded.getBbHeight() - new float[] {2.2f, 3.6f, 4.8f}[phase]) < .01,
                    "Each form needs its matching dimensions");
        }
        h.succeed();
    }

    @GameTest(template = "combat_empty")
    public static void transformsCannotSkipForms(GameTestHelper h) {
        Paperblight boss = boss(h);
        Zombie victim = victim(h, 5, 7);
        boss.setTarget(victim);
        h.assertTrue(boss.hurt(boss.damageSources().mobAttack(victim), 10000), "Initial attack must damage boss");
        h.assertTrue(boss.isAlive() && boss.getVariant() == 0, "Huge hit must not skip first transformation");
        h.assertTrue(boss.currentAbilityId().equals("transform_second"), "First transition must telegraph");
        float protectedHealth = boss.getHealth();
        boss.invulnerableTime = 0;
        boss.hurt(boss.damageSources().mobAttack(victim), 10000);
        h.assertTrue(boss.getHealth() == protectedHealth, "Transition must protect its animation");
        for (int i = 0; i < 70; i++) boss.tick();
        h.assertTrue(boss.getVariant() == 1 && boss.isAlive(), "First transition must end in second form");
        boss.invulnerableTime = 0;
        boss.hurt(boss.damageSources().mobAttack(victim), 10000);
        h.assertTrue(boss.currentAbilityId().equals("transform_third") && boss.isAlive(), "Second transition must also prevent one-shot skipping");
        for (int i = 0; i < 80; i++) boss.tick();
        h.assertTrue(boss.getVariant() == 2 && boss.isAlive(), "Second transition must end in winged third form");
        boss.invulnerableTime = 0;
        boss.hurt(boss.damageSources().mobAttack(victim), 10000);
        h.assertTrue(boss.isDeadOrDying(), "Final form must be defeatable");
        h.succeed();
    }

    @GameTest(template = "combat_empty")
    public static void paperblightFightsOtherFactions(GameTestHelper h) {
        for (var faction : FpeEntity.Faction.values()) {
            boolean expected = faction != FpeEntity.Faction.PAPERBLIGHT;
            h.assertTrue(FpeEntity.hostile(FpeEntity.Faction.PAPERBLIGHT, faction) == expected
                    && FpeEntity.hostile(faction, FpeEntity.Faction.PAPERBLIGHT) == expected,
                    "All other factions must fight Paperblight symmetrically");
        }
        h.succeed();
    }

    @GameTest(template = "combat_empty")
    public static void modelsCoverEveryAbility(GameTestHelper h) {
        Paperblight boss = boss(h);
        for (String id : new String[] {"paperblight", "paperblight_phase2", "paperblight_phase3"}) {
            try (var stream = PaperblightGameTests.class.getResourceAsStream("/assets/fpe/bbmodels/" + id + ".bbmodel")) {
                h.assertTrue(stream != null, "All three forms must be packaged");
                JsonObject model = JsonParser.parseReader(new InputStreamReader(stream, StandardCharsets.UTF_8)).getAsJsonObject();
                Map<String, JsonObject> animations = new HashMap<>();
                for (var element : model.getAsJsonArray("animations")) {
                    JsonObject animation = element.getAsJsonObject();
                    animations.put(animation.get("name").getAsString(), animation);
                }
                h.assertTrue(animations.keySet().containsAll(java.util.List.of("idle", "walk", "death")), "Forms need lifecycle animations");
                for (var ability : boss.abilities()) {
                    h.assertTrue(animations.containsKey(ability.id), id + " missing " + ability.id);
                    JsonObject animation = animations.get(ability.id);
                    h.assertTrue(animation.get("length").getAsDouble() * 20 + .01 >= ability.duration,
                            id + " animation too short: " + ability.id);
                    h.assertTrue(!animation.getAsJsonObject("animators").entrySet().isEmpty(), "Attack needs authored motion");
                }
            } catch (java.io.IOException e) { throw new IllegalStateException(e); }
        }
        h.succeed();
    }

    @GameTest(template = "combat_empty")
    public static void sweepTelegraphsAndProtectsCopies(GameTestHelper h) {
        Paperblight boss = boss(h);
        var ally = h.spawn(ModEntities.PAPERBLIGHT.get(), 6, 2, 5);
        ally.setNoAi(true);
        ally.setNoGravity(true);
        Zombie victim = victim(h, 5, 5);
        boss.setTarget(victim);
        boss.forceAbility("long_sweep");
        float before = victim.getHealth(), allied = ally.getHealth();
        boss.animTime = 15;
        boss.tick();
        h.assertTrue(victim.getHealth() == before, "Sweep anticipation must be harmless");
        boss.tick();
        h.assertTrue(victim.getHealth() < before, "Sweep must hit at tick 16");
        h.assertTrue(ally.getHealth() == allied, "Paperblight must protect its own copies");
        h.succeed();
    }

    @GameTest(template = "combat_empty", timeoutTicks = 300)
    public static void echoesAreBoundedAndTemporary(GameTestHelper h) {
        for (int x = 0; x < 11; x++) for (int z = 0; z < 9; z++)
            h.setBlock(x, 1, z, net.minecraft.world.level.block.Blocks.STONE);
        Paperblight boss = boss(h);
        boss.setVariant(2);
        boss.setTarget(victim(h, 5, 7));
        boss.forceAbility("host_echo");
        boss.animTime = 32;
        boss.tick();
        var echoes = h.getLevel().getEntitiesOfClass(Paperblight.class, boss.getBoundingBox().inflate(8), Paperblight::isEcho);
        h.assertTrue(!echoes.isEmpty() && echoes.size() <= 2, "Duplication must have a small bounded number of copies");
        for (Paperblight echo : echoes) {
            echo.setNoAi(true);
            echo.setNoGravity(true);
            h.assertTrue(echo.getVariant() == 2 && echo.getMaxHealth() <= 40, "Echo must copy form with limited health");
            echo.forceAbility("host_echo");
            echo.animTime = 32;
            echo.tick();
        }
        h.assertTrue(h.getLevel().getEntitiesOfClass(Paperblight.class, boss.getBoundingBox().inflate(8), Paperblight::isEcho).size() == echoes.size(),
                "Copies must never duplicate recursively");
        for (Paperblight echo : echoes) {
            echo.cancelAbility();
            echo.setTarget(null);
        }
        h.runAtTickTime(250, () -> {
            for (Paperblight echo : echoes) h.assertTrue(echo.isRemoved(), "Echo must expire without leaving permanent mobs");
            h.succeed();
        });
    }

    private static Paperblight boss(GameTestHelper h) {
        Paperblight boss = h.spawn(ModEntities.PAPERBLIGHT.get(), 5, 2, 2);
        boss.setNoAi(true);
        boss.setNoGravity(true);
        return boss;
    }

    private static Zombie victim(GameTestHelper h, int x, int z) {
        Zombie victim = h.spawn(EntityType.ZOMBIE, x, 2, z);
        victim.setNoAi(true);
        victim.setNoGravity(true);
        victim.getAttribute(Attributes.MAX_HEALTH).setBaseValue(2000);
        victim.setHealth(2000);
        victim.setDeltaMovement(Vec3.ZERO);
        return victim;
    }
}
