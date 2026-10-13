package com.fpe.client.render;

import com.fpe.client.model.Anim;
import com.fpe.client.model.SpecModel;
import com.fpe.client.spec.FxSpecs;
import com.fpe.entity.FpeFx;
import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.blaze3d.vertex.VertexConsumer;
import com.mojang.math.Axis;

import net.minecraft.client.renderer.MultiBufferSource;
import net.minecraft.client.renderer.RenderType;
import net.minecraft.client.renderer.entity.EntityRenderer;
import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.client.renderer.texture.OverlayTexture;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.util.Mth;
import org.joml.Matrix3f;
import org.joml.Matrix4f;

public class FpeFxRenderer extends EntityRenderer<FpeFx> {
    private final SpecModel<FpeFx> spike, tentacle;

    public FpeFxRenderer(EntityRendererProvider.Context ctx) {
        super(ctx);
        spike = new SpecModel<>(ctx.bakeLayer(FxSpecs.SPIKE.layer()), FxSpecs.SPIKE);
        tentacle = new SpecModel<>(ctx.bakeLayer(FxSpecs.TENTACLE.layer()), FxSpecs.TENTACLE);
    }

    @Override
    public void render(FpeFx e, float yaw, float pt, PoseStack ps, MultiBufferSource buf, int light) {
        float age = e.tickCount + pt;
        int warm = e.warmup();
        switch (e.kind()) {
            case SPIKE -> {
                telegraph(e, ps, buf, age, warm, 1.2f);
                float up = Anim.easeOut((age - warm) / 3f);
                float down = 1f - Anim.easeIn((age - (e.life() - 8)) / 8f);
                float h = e.param() > 0 ? e.param() : 1f;
                if (age >= warm) model(spike, e, ps, buf, 1f + (h - 1f) * 0.4f, up * down * h, light, age);
            }
            case TENTACLE -> {
                telegraph(e, ps, buf, age, warm, 1.5f);
                float up = Anim.easeOut((age - warm) / 6f);
                float down = 1f - Anim.easeIn((age - (e.life() - 10)) / 10f);
                float h = e.param() > 0 ? e.param() : 1f;
                if (age >= warm) model(tentacle, e, ps, buf, h, up * down * h, light, age);
            }
            case RING_TRAP -> ring(e, ps, buf, age);
            case RING_SHOCK -> shock(e, ps, buf, age);
            case ARC -> arc(e, ps, buf, age, pt);
        }
    }

    private void model(SpecModel<FpeFx> m, FpeFx e, PoseStack ps, MultiBufferSource buf, float sxz, float sy, int light, float age) {
        ps.pushPose();
        ps.mulPose(Axis.YP.rotationDegrees(180f - e.getYRot()));
        ps.scale(-sxz, -Math.max(0.001f, sy), sxz);
        ps.translate(0, -1.501, 0);
        m.setupAnim(e, 0, 0, age, 0, 0);
        m.renderToBuffer(ps, buf.getBuffer(RenderType.entityCutoutNoCull(m.spec.texture())), light, OverlayTexture.NO_OVERLAY, 1f, 1f, 1f, 1f);
        if (m.spec.hasGlow()) m.renderToBuffer(ps, buf.getBuffer(RenderType.eyes(m.spec.glowTexture())), 0xF000F0, OverlayTexture.NO_OVERLAY, 1f, 1f, 1f, 1f);
        ps.popPose();
    }

    // ---------------------------------------------------------------- flat geometry helpers
    private static VertexConsumer vc(MultiBufferSource buf) { return buf.getBuffer(RenderType.entityTranslucentEmissive(FxSpecs.WHITE)); }

    private static void quad(PoseStack ps, VertexConsumer c, float x1, float z1, float x2, float z2, float x3, float z3, float x4, float z4, float y, int argb) {
        Matrix4f m = ps.last().pose(); Matrix3f n = ps.last().normal();
        int a = argb >>> 24, r = argb >> 16 & 255, g = argb >> 8 & 255, b = argb & 255;
        float[][] p = {{x1, z1}, {x2, z2}, {x3, z3}, {x4, z4}};
        for (float[] v : p) c.vertex(m, v[0], y, v[1]).color(r, g, b, a).uv(0.5f, 0.5f).overlayCoords(OverlayTexture.NO_OVERLAY).uv2(0xF000F0).normal(n, 0, 1, 0).endVertex();
        for (int i = 3; i >= 0; i--) { float[] v = p[i]; c.vertex(m, v[0], y, v[1]).color(r, g, b, a).uv(0.5f, 0.5f).overlayCoords(OverlayTexture.NO_OVERLAY).uv2(0xF000F0).normal(n, 0, -1, 0).endVertex(); }
    }

    /** annular sector between radii r0..r1 from angle a0..a1 (radians, math angles in XZ plane) */
    private static void sector(PoseStack ps, VertexConsumer c, float r0, float r1, float a0, float a1, float y, int argb, int segs) {
        for (int i = 0; i < segs; i++) {
            float s = Mth.lerp(i / (float) segs, a0, a1), t = Mth.lerp((i + 1) / (float) segs, a0, a1);
            quad(ps, c, r0 * Mth.cos(s), r0 * Mth.sin(s), r1 * Mth.cos(s), r1 * Mth.sin(s), r1 * Mth.cos(t), r1 * Mth.sin(t), r0 * Mth.cos(t), r0 * Mth.sin(t), y, argb);
        }
    }

    private static int alpha(int argb, float a) { return ((int) Mth.clamp((argb >>> 24) * a, 0, 255) << 24) | (argb & 0xFFFFFF); }

    private void telegraph(FpeFx e, PoseStack ps, MultiBufferSource buf, float age, int warm, float r) {
        if (age >= warm) return;
        float k = Mth.clamp(age / Math.max(1, warm), 0, 1);
        ps.pushPose();
        VertexConsumer c = vc(buf);
        sector(ps, c, 0f, r * (0.4f + 0.6f * k), 0, Mth.TWO_PI, 0.03f, 0x60000000 | 0x300010, 20);
        sector(ps, c, r * 0.9f, r, 0, Mth.TWO_PI, 0.04f, alpha(0xFFC01830, 0.5f + 0.5f * Mth.sin(age * 0.8f)), 20);
        ps.popPose();
    }

    private void ring(FpeFx e, PoseStack ps, MultiBufferSource buf, float age) {
        float R = e.radius();
        int warm = e.warmup();
        int col = e.color();
        ps.pushPose();
        VertexConsumer c = vc(buf);
        float draw = Mth.clamp(age / Math.max(1f, warm * 0.6f), 0, 1); // compass draws the circle
        float end = Mth.TWO_PI * draw;
        float fade = age > warm ? 1f - Mth.clamp((age - warm) / Math.max(1f, e.life() - warm), 0, 1) : 1f;
        float pulse = age < warm ? 0.55f + 0.45f * Mth.sin(age * 0.9f) : 1f;
        sector(ps, c, R - 0.28f, R, -Mth.HALF_PI, -Mth.HALF_PI + end, 0.05f, alpha(col, fade * pulse), Math.max(2, (int) (draw * 64)));
        if (age < warm) {
            sector(ps, c, 0, R - 0.28f, 0, Mth.TWO_PI, 0.03f, alpha(col, 0.12f + 0.1f * pulse), 24);
            // spokes forming the inner pattern after drawing
            if (draw >= 1f) for (int i = 0; i < 4; i++) { float a = i * Mth.HALF_PI + age * 0.05f; sector(ps, c, 0.2f, R - 0.3f, a - 0.02f, a + 0.02f, 0.045f, alpha(col, 0.4f * pulse), 1); }
        } else {
            float f = 1f - (age - warm) / 6f;
            if (f > 0) sector(ps, c, 0, R, 0, Mth.TWO_PI, 0.06f, alpha(0xFFFFFFFF, f * 0.6f), 28);
        }
        ps.popPose();
    }

    private void shock(FpeFx e, PoseStack ps, MultiBufferSource buf, float age) {
        float R = e.radius();
        float cur = R * Mth.clamp(age / Math.max(1, e.life() - 4), 0, 1);
        float fade = 1f - Mth.clamp(age / (float) e.life(), 0, 1) * 0.8f;
        ps.pushPose();
        VertexConsumer c = vc(buf);
        sector(ps, c, Math.max(0, cur - 0.8f), cur, 0, Mth.TWO_PI, 0.06f, alpha(e.color(), fade), 40);
        sector(ps, c, Math.max(0, cur - 1.6f), Math.max(0, cur - 0.8f), 0, Mth.TWO_PI, 0.05f, alpha(e.color(), fade * 0.3f), 40);
        ps.popPose();
    }

    /** slash crescent: entity yaw = centre direction, radius = outer radius, param = sweep in degrees */
    private void arc(FpeFx e, PoseStack ps, MultiBufferSource buf, float age, float pt) {
        float life = Math.max(1, e.life());
        float k = Mth.clamp(age / life, 0, 1);
        float sweep = Mth.DEG_TO_RAD * (e.param() <= 0 ? 160f : e.param());
        float R = e.radius();
        ps.pushPose();
        ps.mulPose(Axis.YP.rotationDegrees(-Mth.lerp(pt, e.yRotO, e.getYRot())));
        ps.mulPose(Axis.XP.rotationDegrees(Mth.lerp(pt, e.xRotO, e.getXRot()))); // tilt
        VertexConsumer c = vc(buf);
        float head = Anim.easeOut(k * 2.2f);             // the leading edge sweeps fast
        float tail = Anim.easeIn(Mth.clamp((k - 0.15f) * 1.4f, 0, 1));
        float a0 = Mth.HALF_PI - sweep / 2 + sweep * tail, a1 = Mth.HALF_PI - sweep / 2 + sweep * head;
        float fade = 1f - Anim.easeIn(k);
        if (a1 > a0) {
            sector(ps, c, R * 0.55f, R, a0, a1, 0f, alpha(e.color(), fade), 18);
            sector(ps, c, R * 0.85f, R * 1.05f, a0, a1, 0.01f, alpha(0xFFFFFFFF, fade * 0.8f), 18);
        }
        ps.popPose();
    }

    @Override public ResourceLocation getTextureLocation(FpeFx e) { return FxSpecs.WHITE; }
}
