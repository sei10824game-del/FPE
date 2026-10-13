package com.fpe.client.model;

@FunctionalInterface
public interface Animator {
    /** Called every frame AFTER all parts were reset to their default pose. Only set rotations/offsets you need. */
    void animate(ModelParts m, AnimCtx c);
}
