package com.fpe.entity;

import com.fpe.registry.ModEffects;

import net.minecraft.world.entity.LivingEntity;
import net.minecraftforge.event.entity.living.LivingEvent.LivingJumpEvent;
import net.minecraftforge.eventbus.api.SubscribeEvent;

/** Runs on both sides: the synced effect also suppresses local player jumps. */
public final class FpeCrowdControl {
    private FpeCrowdControl() {}

    @SubscribeEvent
    public static void onJump(LivingJumpEvent event) {
        LivingEntity victim = event.getEntity();
        if (!victim.hasEffect(ModEffects.ROOTED.get())) return;
        // Forge fires after the upward velocity and sprint impulse are applied.
        // Do not clear motion each tick: attacks may intentionally launch victims.
        victim.setDeltaMovement(0, Math.min(0, victim.getDeltaMovement().y), 0);
        victim.hasImpulse = true;
    }
}
