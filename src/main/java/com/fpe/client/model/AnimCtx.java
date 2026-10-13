package com.fpe.client.model;

import com.fpe.entity.FpeEntity;

import net.minecraft.world.entity.Entity;

/** Per-frame animation context. Angles in DEGREES unless noted. */
public final class AnimCtx {
    public Entity entity;
    /** null for non-FpeEntity (projectiles / fx) */
    public FpeEntity fpe;
    /** ageInTicks incl. partial tick */
    public float age;
    public float limbSwing, limbAmt;
    public float headYaw, headPitch;
    public float partial;
    /** id of the running ability ("" when idle) */
    public String ability = "";
    /** ticks since the ability started (incl. partial) and its duration */
    public float t, dur = 1;
    /** 0..1 death progress (0 while alive) */
    public float death;
    /** entity-specific variant (e.g. Alice phase) */
    public int variant;

    public boolean is(String id) { return ability.equals(id); }
    public boolean idle() { return ability.isEmpty(); }
    /** 0..1 progress through the whole ability */
    public float p() { return Anim.clamp(t / Math.max(1f, dur), 0, 1); }
    /** 0..1 progress between tick a and tick b of the ability */
    public float seg(float a, float b) { return Anim.clamp((t - a) / Math.max(0.0001f, b - a), 0, 1); }
    /** walking intensity 0..1 */
    public float walk() { return Math.min(1f, limbAmt * 1.6f); }
}
