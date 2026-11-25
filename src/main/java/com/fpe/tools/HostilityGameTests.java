package com.fpe.tools;

import com.fpe.entity.FpeHostility;
import com.fpe.entity.FpeEntity;
import com.fpe.entity.FpeFx;
import com.fpe.entity.FpeProjectile;
import com.fpe.entity.FpeUtil;
import com.fpe.registry.ModEntities;

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
    public static void insanityFightsAllTeacherGroups(GameTestHelper h) {
        var insanity = h.spawn(ModEntities.INSANITY_CIRCLE.get(), 2, 2, 2);
        insanity.setNoAi(true);
        var shot = new FpeProjectile(ModEntities.PROJECTILE.get(), h.getLevel());
        shot.setOwner(insanity);
        var effect = new FpeFx(ModEntities.FX.get(), h.getLevel());
        effect.setOwner(insanity);
        for (var type : java.util.List.of(ModEntities.MISS_CIRCLE.get(), ModEntities.MISS_THAVEL.get(),
                ModEntities.MISS_BLOOMIE.get(), ModEntities.RED_CIRCLE.get(), ModEntities.DANGER_THAVEL.get(),
                ModEntities.DANGER_BLOOMIE.get(), ModEntities.GREEN_CIRCLE.get(), ModEntities.GREEN_THAVEL.get(),
                ModEntities.GREEN_BLOOMIE.get())) {
            FpeEntity teacher = h.spawn(type, 5, 2, 5);
            teacher.setNoAi(true);
            h.assertTrue(insanity.canAttack(teacher) && teacher.canAttack(insanity), "Teachers and Insanity must target each other");
            h.assertTrue(FpeUtil.canHurt(shot, teacher) && FpeUtil.canHurt(effect, teacher), "Owned attacks must honor Insanity's feud");
            h.assertTrue(FpeUtil.hit(insanity, teacher, 1, 0, 0), "Insanity must damage teachers");
            insanity.invulnerableTime = 0;
            h.assertTrue(FpeUtil.hit(teacher, insanity, 1, 0, 0), "Teachers must damage Insanity");
        }
        for (var faction : FpeEntity.Faction.values()) {
            h.assertTrue(FpeEntity.hostile(FpeEntity.Faction.INSANITY, faction)
                    == FpeEntity.hostile(faction, FpeEntity.Faction.INSANITY), "Insanity feud must be symmetric");
            if (faction != FpeEntity.Faction.MISS && faction != FpeEntity.Faction.GREEN_TEACHER && faction != FpeEntity.Faction.INSANITY && faction != FpeEntity.Faction.SURVIVOR)
                h.assertTrue(FpeEntity.hostile(FpeEntity.Faction.INSANITY, faction)
                        == FpeEntity.hostile(FpeEntity.Faction.MISS, faction), "Existing non-teacher relationships must remain stable");
        }
        h.assertTrue(!FpeUtil.canHurt(shot, insanity), "Insanity's projectile must protect its caster");
        h.succeed();
    }

    @GameTest(template = "combat_empty")
    public static void insanityAndCircleAcquireEachOther(GameTestHelper h) {
        var insanity = h.spawn(ModEntities.INSANITY_CIRCLE.get(), 3, 2, 3);
        var circle = h.spawn(ModEntities.MISS_CIRCLE.get(), 3, 2, 7);
        for (var actor : java.util.List.of(insanity, circle)) {
            actor.setNoGravity(true);
            actor.getAttribute(net.minecraft.world.entity.ai.attributes.Attributes.MOVEMENT_SPEED).setBaseValue(0);
        }
        h.succeedWhen(() -> {
            h.assertTrue(insanity.getTarget() == circle, "Insanity AI must select Circle without provocation");
            h.assertTrue(circle.getTarget() == insanity, "Circle AI must select Insanity without provocation");
        });
    }

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
