package com.fpe.tools;

import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.HashMap;

import com.fpe.entity.FpeFx;
import com.fpe.entity.characters.PaperblightHost;
import com.fpe.entity.characters.PaperblightHost.Role;
import com.fpe.registry.ModEntities;
import com.fpe.registry.ModItems;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.level.block.Blocks;
import net.minecraftforge.common.ForgeSpawnEggItem;
import net.minecraftforge.gametest.GameTestHolder;
import net.minecraftforge.gametest.PrefixGameTestTemplate;

@GameTestHolder("fpe")
@PrefixGameTestTemplate(false)
public final class PaperblightHostGameTests {
    private static EntityType<PaperblightHost> type(Role role) {
        return switch (role) {
            case LANA -> ModEntities.HOST_LANA.get();
            case EDWARD -> ModEntities.HOST_EDWARD.get();
            case OLIVER -> ModEntities.HOST_OLIVER.get();
            case THAVEL -> ModEntities.HOST_THAVEL.get();
            case CLAIRE -> ModEntities.PAPERBLIGHT_CLAIRE.get();
            case ZIP -> ModEntities.HOST_ZIP.get();
        };
    }

    private static String id(Role role) {
        return role == Role.CLAIRE ? "paperblight_claire" : "host_" + role.name().toLowerCase(java.util.Locale.ROOT);
    }

    @GameTest(template = "combat_empty")
    public static void sixRolesSaveAndHaveEggs(GameTestHelper h) {
        var eggs = java.util.List.of(ModItems.HOST_LANA.get(), ModItems.HOST_EDWARD.get(), ModItems.HOST_OLIVER.get(),
                ModItems.HOST_THAVEL.get(), ModItems.PAPERBLIGHT_CLAIRE.get(), ModItems.HOST_ZIP.get());
        for (Role role : Role.values()) {
            var character = host(h, role, 5, 5);
            CompoundTag saved = new CompoundTag();
            character.save(saved);
            h.assertTrue(saved.getString("id").equals("fpe:" + id(role)), "Each character needs its own saved ID");
            var restored = EntityType.loadEntityRecursive(saved, h.getLevel(), e -> e);
            h.assertTrue(restored instanceof PaperblightHost && ((PaperblightHost) restored).role() == role,
                    "Loading must preserve the correct character, attributes and behavior");
            h.assertTrue(((ForgeSpawnEggItem) eggs.get(role.ordinal())).getType(null) == type(role), "Egg must spawn the matching role");
        }
        h.succeed();
    }

    @GameTest(template = "combat_empty")
    public static void sixModelsCoverEveryAttack(GameTestHelper h) {
        for (Role role : Role.values()) {
            var actor = host(h, role, 5, 5);
            h.assertTrue(actor.abilities().size() == 12, "Every added character needs 12 attacks");
            try (var stream = PaperblightHostGameTests.class.getResourceAsStream("/assets/fpe/bbmodels/" + id(role) + ".bbmodel")) {
                h.assertTrue(stream != null, "All six models must be packaged");
                var model = JsonParser.parseReader(new InputStreamReader(stream, StandardCharsets.UTF_8)).getAsJsonObject();
                var animations = new HashMap<String, JsonObject>();
                for (var entry : model.getAsJsonArray("animations")) {
                    var animation = entry.getAsJsonObject();
                    animations.put(animation.get("name").getAsString(), animation);
                }
                h.assertTrue(animations.keySet().containsAll(java.util.List.of("idle", "walk", "death")), "Every model needs lifecycle animation");
                for (var ability : actor.abilities()) {
                    h.assertTrue(animations.containsKey(ability.id), id(role) + " missing " + ability.id);
                    var animation = animations.get(ability.id);
                    h.assertTrue(animation.get("length").getAsDouble() * 20 + .01 >= ability.duration,
                            "Animation must cover the server attack duration");
                    h.assertTrue(!animation.getAsJsonObject("animators").entrySet().isEmpty(), "Attack needs authored motion");
                }
            } catch (java.io.IOException e) { throw new IllegalStateException(e); }
        }
        h.succeed();
    }

    @GameTest(template = "combat_empty")
    public static void claireDefeatsTheThreeNamedHosts(GameTestHelper h) {
        var claire = host(h, Role.CLAIRE, 5, 2);
        var lana = host(h, Role.LANA, 4, 4);
        var edward = host(h, Role.EDWARD, 5, 4);
        var oliver = host(h, Role.OLIVER, 6, 4);
        var thavel = host(h, Role.THAVEL, 5, 5);
        float thavelBefore = thavel.getHealth();
        claire.setTarget(edward);
        claire.forceAbility("sweep");
        claire.animTime = 13;
        claire.tick();
        h.assertTrue(lana.isAlive() && edward.isAlive() && oliver.isAlive(), "Claire must still telegraph a lethal strike");
        claire.tick();
        h.assertTrue(lana.isDeadOrDying() && edward.isDeadOrDying() && oliver.isDeadOrDying(),
                "Claire's contact must defeat Lana, Edward and Oliver in one strike");
        h.assertTrue(thavel.isAlive() && thavel.getHealth() < thavelBefore,
                "Selective lethal rule must not become global instant-death damage");
        h.succeed();
    }

    @GameTest(template = "combat_empty")
    public static void claireLaserChargesThenHits(GameTestHelper h) {
        var claire = host(h, Role.CLAIRE, 5, 2);
        var oliver = host(h, Role.OLIVER, 5, 7);
        claire.setTarget(oliver);
        claire.forceAbility("eye_ray");
        claire.animTime = 23;
        claire.tick();
        h.assertTrue(oliver.isAlive() && oliver.getHealth() == oliver.getMaxHealth(), "Laser charge must allow time to dodge");
        claire.tick();
        h.assertTrue(oliver.isDeadOrDying(), "Eye laser must defeat the named host on contact");
        var beams = h.getLevel().getEntitiesOfClass(FpeFx.class, claire.getBoundingBox().inflate(2),
                fx -> fx.kind() == FpeFx.Kind.BEAM && fx.getOwner() == claire);
        h.assertTrue(!beams.isEmpty() && beams.get(0).param() > 5, "Laser damage must have a visible beam");
        h.succeed();
    }

    @GameTest(template = "combat_empty")
    public static void claireLaserStopsAtCover(GameTestHelper h) {
        var claire = host(h, Role.CLAIRE, 5, 2);
        var lana = host(h, Role.LANA, 5, 7);
        for (int x = 4; x <= 6; x++) for (int y = 2; y <= 6; y++) h.setBlock(x, y, 4, Blocks.STONE);
        claire.setTarget(lana);
        claire.forceAbility("eye_ray");
        claire.animTime = 23;
        claire.tick(); claire.tick();
        h.assertTrue(lana.getHealth() == lana.getMaxHealth(), "Solid cover must stop the lethal ray");
        var beams = h.getLevel().getEntitiesOfClass(FpeFx.class, claire.getBoundingBox().inflate(2),
                fx -> fx.kind() == FpeFx.Kind.BEAM && fx.getOwner() == claire);
        h.assertTrue(!beams.isEmpty() && beams.get(0).param() < 3, "Visible beam must stop at the wall too");
        h.assertBlockPresent(Blocks.STONE, 5, 3, 4);
        h.succeed();
    }

    @GameTest(template = "combat_empty")
    public static void hostsAllyAndClaireOpposesThem(GameTestHelper h) {
        var lana = host(h, Role.LANA, 5, 2);
        var oliver = host(h, Role.OLIVER, 5, 4);
        var claire = host(h, Role.CLAIRE, 5, 5);
        h.assertTrue(!lana.canAttack(oliver) && !oliver.canAttack(lana), "Hosts must remain allied");
        h.assertTrue(lana.canAttack(claire) && claire.canAttack(lana), "Claire and hosts must fight each other");
        float before = oliver.getHealth();
        lana.setTarget(claire);
        lana.forceAbility("sweep"); lana.animTime = 14; lana.tick();
        h.assertTrue(oliver.getHealth() == before && claire.getHealth() < claire.getMaxHealth(), "Host attacks must hit Claire while protecting other hosts");
        h.succeed();
    }

    private static PaperblightHost host(GameTestHelper h, Role role, int x, int z) {
        var host = h.spawn(type(role), x, 2, z);
        host.setNoAi(true); host.setNoGravity(true);
        return host;
    }
}
