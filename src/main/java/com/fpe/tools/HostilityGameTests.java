package com.fpe.tools;

import com.fpe.entity.FpeHostility;

import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.entity.monster.Zombie;
import net.minecraftforge.event.entity.EntityJoinLevelEvent;
import net.minecraftforge.gametest.GameTestHolder;
import net.minecraftforge.gametest.PrefixGameTestTemplate;

/** Real server regression tests for runtime AI installation across NBT reloads. */
@GameTestHolder("fpe")
@PrefixGameTestTemplate(false)
public final class HostilityGameTests {
    @GameTest(template = "combat_empty")
    public static void hostilitySurvivesReload(GameTestHelper h) {
        Zombie original = h.spawn(EntityType.ZOMBIE, 2, 2, 2);
        h.assertTrue(targetGoals(original) == 1, "Fresh mob must receive an FPE targeting goal");
        int initialGoals = original.goalSelector.getAvailableGoals().size();
        rejoin(h, original);
        rejoin(h, original);
        h.assertTrue(targetGoals(original) == 1, "Repeated join must not duplicate FPE targeting");
        h.assertTrue(original.goalSelector.getAvailableGoals().size() == initialGoals,
                "Repeated join must not duplicate attack goals");

        // Simulate a world saved by the old implementation: tags survive, goals do not.
        original.addTag("fpe_hostile");
        CompoundTag saved = original.saveWithoutId(new CompoundTag());
        original.discard();
        Zombie restored = EntityType.ZOMBIE.create(h.getLevel());
        h.assertTrue(restored != null, "Reloaded zombie must be created");
        restored.load(saved);
        h.assertTrue(restored.getTags().contains("fpe_hostile"), "Legacy tag must survive NBT roundtrip");
        h.assertTrue(targetGoals(restored) == 0, "Runtime FPE goals must not be serialized");
        h.getLevel().addFreshEntity(restored);
        h.assertTrue(targetGoals(restored) == 1, "Reload must reinstall targeting despite legacy tag");
        h.assertTrue(!restored.getTags().contains("fpe_hostile"), "Legacy installation tag must be removed");
        rejoin(h, restored);
        h.assertTrue(targetGoals(restored) == 1, "Reloaded mob must remain idempotent");
        h.assertTrue(restored.goalSelector.getAvailableGoals().size() == initialGoals,
                "Reload must preserve exactly one set of attack goals");
        h.succeed();
    }

    private static void rejoin(GameTestHelper h, Mob mob) {
        FpeHostility.onJoin(new EntityJoinLevelEvent(mob, h.getLevel()));
    }

    private static long targetGoals(Mob mob) {
        return mob.targetSelector.getAvailableGoals().stream()
                .filter(g -> g.getGoal().getClass().getEnclosingClass() == FpeHostility.class).count();
    }
}
