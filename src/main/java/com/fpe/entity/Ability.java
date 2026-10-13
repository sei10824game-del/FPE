package com.fpe.entity;

import java.util.function.Predicate;

import javax.annotation.Nullable;

import net.minecraft.world.entity.LivingEntity;

/**
 * One attack/skill. The animation system looks the ability up by {@link #id} (see AnimCtx.is(id)),
 * so the model animator and the server logic share one timeline measured in ticks since start.
 * The target passed to callbacks is never null/dead (the ability is aborted otherwise).
 */
public final class Ability {
    @FunctionalInterface
    public interface Fn { void run(FpeEntity e, LivingEntity target, int t); }

    public final String id;
    public final int duration, cooldown;
    public double min = 0, max = 4;
    public int weight = 1;
    /** stop pathfinding while active */
    public boolean rooted = true;
    public boolean needsSight = true;
    /** keep facing the target until this tick (default: whole duration) */
    public int faceUntil;
    @Nullable public Fn onStart, onTick, onEnd;
    public Predicate<FpeEntity> cond = e -> true;

    private Ability(String id, int duration, int cooldown) { this.id = id; this.duration = duration; this.cooldown = cooldown; this.faceUntil = duration; }

    public static Ability of(String id, int duration, int cooldown) { return new Ability(id, duration, cooldown); }

    public Ability range(double min, double max) { this.min = min; this.max = max; return this; }
    public Ability weight(int w) { this.weight = w; return this; }
    public Ability moving() { this.rooted = false; return this; }
    public Ability blind() { this.needsSight = false; return this; }
    public Ability faceUntil(int t) { this.faceUntil = t; return this; }
    public Ability when(Predicate<FpeEntity> c) { this.cond = c; return this; }
    public Ability start(Fn f) { this.onStart = f; return this; }
    public Ability tick(Fn f) { this.onTick = f; return this; }
    public Ability end(Fn f) { this.onEnd = f; return this; }
}
