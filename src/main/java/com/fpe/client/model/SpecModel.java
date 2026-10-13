package com.fpe.client.model;

import com.fpe.entity.FpeEntity;
import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.blaze3d.vertex.VertexConsumer;

import net.minecraft.client.model.EntityModel;
import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.world.entity.Entity;

public class SpecModel<T extends Entity> extends EntityModel<T> {
    public final ModelPart root;
    public final ModelSpec spec;
    public final ModelParts parts;
    private float partial;

    public SpecModel(ModelPart root, ModelSpec spec) {
        this.root = root;
        this.spec = spec;
        this.parts = new ModelParts(root, spec);
    }

    @Override
    public void prepareMobModel(T e, float limbSwing, float limbAmt, float partial) { this.partial = partial; }

    @Override
    public void setupAnim(T e, float limbSwing, float limbAmt, float age, float headYaw, float headPitch) {
        parts.resetAll();
        if (spec.animator == null) return;
        AnimCtx c = new AnimCtx();
        c.entity = e; c.age = age; c.limbSwing = limbSwing; c.limbAmt = limbAmt; c.headYaw = headYaw; c.headPitch = headPitch; c.partial = partial;
        if (e instanceof FpeEntity f) {
            c.fpe = f;
            c.ability = f.currentAbilityId();
            c.dur = Math.max(1, f.currentAbilityDuration());
            c.t = f.animTime + partial;
            c.variant = f.getVariant();
            c.death = f.deathTime > 0 ? Math.min(1f, (f.deathTime + partial) / FpeEntity.DEATH_TICKS) : 0f;
        }
        spec.animator.animate(parts, c);
    }

    @Override
    public void renderToBuffer(PoseStack ps, VertexConsumer vc, int light, int overlay, float r, float g, float b, float a) {
        root.render(ps, vc, light, overlay, r, g, b, a);
    }
}
