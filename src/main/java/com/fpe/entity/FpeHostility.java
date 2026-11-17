package com.fpe.entity;

import net.minecraft.world.entity.Mob;
import net.minecraft.world.entity.PathfinderMob;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.ai.goal.MeleeAttackGoal;
import net.minecraft.world.entity.ai.goal.RangedAttackGoal;
import net.minecraft.world.entity.ai.goal.target.NearestAttackableTargetGoal;
import net.minecraftforge.event.entity.EntityJoinLevelEvent;
import net.minecraftforge.eventbus.api.SubscribeEvent;

/** Makes every non-FPE mob hostile toward FPE characters (and vice versa, see FpeEntity target goals). */
public final class FpeHostility {
    private static final String LEGACY_TAG = "fpe_hostile";

    /** Runtime marker: goals are rebuilt on load, unlike persistent entity tags. */
    private static final class FpeTargetGoal extends NearestAttackableTargetGoal<FpeEntity> {
        FpeTargetGoal(Mob mob) { super(mob, FpeEntity.class, 10, false, false, null); }
    }

    @SubscribeEvent
    public static void onJoin(EntityJoinLevelEvent e) {
        if (e.getLevel().isClientSide || !(e.getEntity() instanceof Mob m) || m instanceof FpeEntity) return;
        m.removeTag(LEGACY_TAG);
        boolean hasTarget = m.targetSelector.getAvailableGoals().stream().anyMatch(g -> g.getGoal() instanceof FpeTargetGoal);
        if (!hasTarget) m.targetSelector.addGoal(2, new FpeTargetGoal(m));
        if (m instanceof PathfinderMob pm && pm.getAttributes().hasAttribute(Attributes.ATTACK_DAMAGE)) {
            boolean hasAttack = pm.goalSelector.getAvailableGoals().stream().anyMatch(g -> g.getGoal() instanceof MeleeAttackGoal || g.getGoal() instanceof RangedAttackGoal || g.getGoal().getClass().getSimpleName().contains("Attack"));
            if (!hasAttack) pm.goalSelector.addGoal(3, new MeleeAttackGoal(pm, 1.25, true));
        }
    }
}
