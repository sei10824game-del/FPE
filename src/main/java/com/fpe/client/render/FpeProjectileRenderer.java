package com.fpe.client.render;

import java.util.EnumMap;
import java.util.Map;

import com.fpe.client.model.ModelSpec;
import com.fpe.client.model.SpecModel;
import com.fpe.client.spec.ProjectileSpecs;
import com.fpe.entity.FpeProjectile;
import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.math.Axis;

import net.minecraft.client.renderer.MultiBufferSource;
import net.minecraft.client.renderer.RenderType;
import net.minecraft.client.renderer.entity.EntityRenderer;
import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.client.renderer.texture.OverlayTexture;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.util.Mth;

public class FpeProjectileRenderer extends EntityRenderer<FpeProjectile> {
    private final Map<FpeProjectile.Kind, SpecModel<FpeProjectile>> models = new EnumMap<>(FpeProjectile.Kind.class);

    public FpeProjectileRenderer(EntityRendererProvider.Context ctx) {
        super(ctx);
        for (FpeProjectile.Kind k : FpeProjectile.Kind.values()) {
            ModelSpec s = ProjectileSpecs.get(k);
            models.put(k, new SpecModel<>(ctx.bakeLayer(s.layer()), s));
        }
    }

    @Override
    public void render(FpeProjectile e, float yaw, float pt, PoseStack ps, MultiBufferSource buf, int light) {
        FpeProjectile.Kind k = e.kind();
        SpecModel<FpeProjectile> m = models.get(k);
        ps.pushPose();
        ps.translate(0, e.getBbHeight() / 2, 0);
        float spin = (e.ageTicks() + pt) * k.spin;
        if (k.spin == 0f) {
            ps.mulPose(Axis.YP.rotationDegrees(180f - Mth.lerp(pt, e.yRotO, e.getYRot())));
            ps.mulPose(Axis.XP.rotationDegrees(-Mth.lerp(pt, e.xRotO, e.getXRot())));
        } else {
            ps.mulPose(Axis.YP.rotationDegrees(180f - Mth.lerp(pt, e.yRotO, e.getYRot())));
            switch (k) {
                case COMPASS, DIAMOND, SHADOW_ORB -> ps.mulPose(Axis.YP.rotationDegrees(spin));
                case ABC_BLOCK -> { ps.mulPose(Axis.XP.rotationDegrees(spin)); ps.mulPose(Axis.ZP.rotationDegrees(spin * 0.6f)); }
                default -> ps.mulPose(Axis.XP.rotationDegrees(spin));
            }
        }
        ps.scale(-1f, -1f, 1f);
        ps.translate(0, -0.0, 0); // models are authored around their own pivot (0,0,0)
        m.setupAnim(e, 0, 0, e.tickCount + pt, 0, 0);
        m.renderToBuffer(ps, buf.getBuffer(RenderType.entityCutoutNoCull(m.spec.texture())), 0xF000F0, OverlayTexture.NO_OVERLAY, 1f, 1f, 1f, 1f);
        if (m.spec.hasGlow()) m.renderToBuffer(ps, buf.getBuffer(RenderType.eyes(m.spec.glowTexture())), 0xF000F0, OverlayTexture.NO_OVERLAY, 1f, 1f, 1f, 1f);
        ps.popPose();
    }

    @Override public ResourceLocation getTextureLocation(FpeProjectile e) { return ProjectileSpecs.get(e.kind()).texture(); }
}
