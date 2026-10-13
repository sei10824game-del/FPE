package com.fpe.client.render;

import com.fpe.client.model.ModelSpec;
import com.fpe.client.model.SpecModel;
import com.fpe.entity.FpeEntity;
import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.blaze3d.vertex.VertexConsumer;

import net.minecraft.client.renderer.MultiBufferSource;
import net.minecraft.client.renderer.RenderType;
import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.client.renderer.entity.MobRenderer;
import net.minecraft.client.renderer.entity.layers.RenderLayer;
import net.minecraft.client.renderer.entity.RenderLayerParent;
import net.minecraft.client.renderer.texture.OverlayTexture;
import net.minecraft.resources.ResourceLocation;

/** Renders an FpeEntity with one ModelSpec per variant (entity.getVariant()). */
public class FpeRenderer<T extends FpeEntity> extends MobRenderer<T, SpecModel<T>> {
    private final ModelSpec[] specs;
    private final SpecModel<T>[] models;

    @SuppressWarnings("unchecked")
    public FpeRenderer(EntityRendererProvider.Context ctx, ModelSpec... specs) {
        super(ctx, new SpecModel<T>(ctx.bakeLayer(specs[0].layer()), specs[0]), specs[0].shadow);
        this.specs = specs;
        this.models = new SpecModel[specs.length];
        for (int i = 0; i < specs.length; i++) models[i] = i == 0 ? model : new SpecModel<T>(ctx.bakeLayer(specs[i].layer()), specs[i]);
        addLayer(new Glow<>(this));
    }

    private int idx(T e) { return Math.min(specs.length - 1, Math.max(0, e.getVariant())); }

    @Override
    public void render(T e, float yaw, float pt, PoseStack ps, MultiBufferSource buf, int light) {
        int i = idx(e);
        this.model = models[i];
        this.shadowRadius = specs[i].shadow;
        super.render(e, yaw, pt, ps, buf, light);
    }

    @Override public ResourceLocation getTextureLocation(T e) { return specs[idx(e)].texture(); }
    @Override protected float getFlipDegrees(T e) { return 0f; }
    @Override protected boolean isShaking(T e) { return false; }

    static final class Glow<T extends FpeEntity> extends RenderLayer<T, SpecModel<T>> {
        Glow(RenderLayerParent<T, SpecModel<T>> p) { super(p); }

        @Override
        public void render(PoseStack ps, MultiBufferSource buf, int light, T e, float ls, float la, float pt, float age, float hy, float hp) {
            SpecModel<T> m = getParentModel();
            if (!m.spec.hasGlow()) return;
            VertexConsumer vc = buf.getBuffer(RenderType.eyes(m.spec.glowTexture()));
            m.renderToBuffer(ps, vc, 0xF000F0, OverlayTexture.NO_OVERLAY, 1f, 1f, 1f, 1f);
        }
    }
}
