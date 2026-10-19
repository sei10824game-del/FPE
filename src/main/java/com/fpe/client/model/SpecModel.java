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
            c.variant = f.getVariant(); c.stance = f.getStance();
            c.death = f.deathTime > 0 ? Math.min(1f, (f.deathTime + partial) / FpeEntity.DEATH_TICKS) : 0f;
        }
        spec.animator.animate(parts, c);
    }

    @Override
    public void renderToBuffer(PoseStack ps, VertexConsumer vc, int light, int overlay, float r, float g, float b, float a) {
        // Models with per-face UV are drawn here (not via ModelPart.render): optimisation mods such as Embeddium/Sodium replace the
        // vanilla cube drawing with their own box-UV copy made at construction time, which would ignore our polygons.
        if (!parts.customRender) { root.render(ps, vc, light, overlay, r, g, b, a); return; }
        for (ModelSpec.Part p : parts.children.getOrDefault("", java.util.List.of())) drawNode(p, ps, vc, light, overlay, r, g, b, a);
    }

    private void drawNode(ModelSpec.Part p, PoseStack ps, VertexConsumer vc, int light, int overlay, float r, float g, float b, float a) {
        net.minecraft.client.model.geom.ModelPart mp = parts.get(p.name);
        if (!mp.visible) return;
        ps.pushPose();
        mp.translateAndRotate(ps);
        net.minecraft.client.model.geom.ModelPart.Polygon[] pg = parts.polys.get(p.name);
        if (pg != null) {
            PoseStack.Pose pose = ps.last();
            org.joml.Matrix4f m4 = pose.pose();
            org.joml.Matrix3f m3 = pose.normal();
            for (net.minecraft.client.model.geom.ModelPart.Polygon poly : pg) {
                org.joml.Vector3f n = m3.transform(new org.joml.Vector3f(poly.normal));
                for (net.minecraft.client.model.geom.ModelPart.Vertex v : poly.vertices) {
                    org.joml.Vector4f p4 = m4.transform(new org.joml.Vector4f(v.pos.x() / 16f, v.pos.y() / 16f, v.pos.z() / 16f, 1f));
                    vc.vertex(p4.x(), p4.y(), p4.z(), r, g, b, a, v.u, v.v, overlay, light, n.x(), n.y(), n.z());
                }
            }
        }
        for (ModelSpec.Part c : parts.children.getOrDefault(p.name, java.util.List.of())) drawNode(c, ps, vc, light, overlay, r, g, b, a);
        ps.popPose();
    }
}
