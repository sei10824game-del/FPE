package com.fpe.client;

import com.fpe.FpeMod;
import com.fpe.client.model.ModelSpec;
import com.fpe.client.render.FpeFxRenderer;
import com.fpe.client.render.FpeProjectileRenderer;
import com.fpe.client.render.FpeRenderer;
import com.fpe.client.spec.*;
import com.fpe.registry.ModEntities;
import com.mojang.blaze3d.platform.NativeImage;

import net.minecraft.client.Minecraft;
import net.minecraft.client.renderer.texture.DynamicTexture;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.packs.resources.ResourceManagerReloadListener;
import net.minecraftforge.api.distmarker.Dist;
import net.minecraftforge.client.event.EntityRenderersEvent;
import net.minecraftforge.client.event.RegisterClientReloadListenersEvent;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.fml.common.Mod;

@Mod.EventBusSubscriber(modid = FpeMod.MODID, bus = Mod.EventBusSubscriber.Bus.MOD, value = Dist.CLIENT)
public final class ClientSetup {
    private ClientSetup() {}

    @SubscribeEvent
    public static void layers(EntityRenderersEvent.RegisterLayerDefinitions e) {
        for (ModelSpec s : Specs.all()) e.registerLayerDefinition(s.layer(), s::layerDefinition);
    }

    @SubscribeEvent
    public static void renderers(EntityRenderersEvent.RegisterRenderers e) {
        e.registerEntityRenderer(ModEntities.MISS_CIRCLE.get(), c -> new FpeRenderer<>(c, MissCircleSpec.SPEC));
        e.registerEntityRenderer(ModEntities.MISS_THAVEL.get(), c -> new FpeRenderer<>(c, MissThavelSpec.SPEC));
        e.registerEntityRenderer(ModEntities.MISS_BLOOMIE.get(), c -> new FpeRenderer<>(c, MissBloomieSpec.SPEC));
        e.registerEntityRenderer(ModEntities.ALICE.get(), c -> new FpeRenderer<>(c, AliceSpec.PHASE1, AliceSpec.PHASE2));
        e.registerEntityRenderer(ModEntities.RED_CIRCLE.get(), c -> new FpeRenderer<>(c, RedCircleSpec.SPEC));
        e.registerEntityRenderer(ModEntities.DANGER_THAVEL.get(), c -> new FpeRenderer<>(c, DangerThavelSpec.SPEC));
        e.registerEntityRenderer(ModEntities.DANGER_BLOOMIE.get(), c -> new FpeRenderer<>(c, DangerBloomieSpec.SPEC));
        e.registerEntityRenderer(ModEntities.INFECTED_BLOOMIE.get(), c -> new FpeRenderer<>(c, InfectedBloomieSpec.SPEC));
        e.registerEntityRenderer(ModEntities.INFECTED_ZIP.get(), c -> new FpeRenderer<>(c, InfectedZipSpec.SPEC));
        e.registerEntityRenderer(ModEntities.DANGER_ALICE.get(), c -> new FpeRenderer<>(c, DangerAliceSpec.SPEC, DangerAliceSpec.PHASE2));
        e.registerEntityRenderer(ModEntities.FEN.get(), c -> new FpeRenderer<>(c, FenSpec.SPEC));
        e.registerEntityRenderer(ModEntities.AIDEN.get(), c -> new FpeRenderer<>(c, AidenSpec.SPEC));
        e.registerEntityRenderer(ModEntities.MUTANT_CLAIRE.get(), c -> new FpeRenderer<>(c, MutantClaireSpec.SPEC));
        e.registerEntityRenderer(ModEntities.MUTANT_ENGEL.get(), c -> new FpeRenderer<>(c, MutantEngelSpec.SPEC));
        e.registerEntityRenderer(ModEntities.MUTANT_BUBBLE.get(), c -> new FpeRenderer<>(c, MutantBubbleSpec.SPEC));
        e.registerEntityRenderer(ModEntities.MUTANT_LANA.get(), c -> new FpeRenderer<>(c, MutantLanaSpec.SPEC));
        e.registerEntityRenderer(ModEntities.MUTANT_ABBIE.get(), c -> new FpeRenderer<>(c, MutantAbbieSpec.SPEC));
        e.registerEntityRenderer(ModEntities.GREEN_THAVEL.get(), c -> new FpeRenderer<>(c, GreenThavelSpec.SPEC));
        e.registerEntityRenderer(ModEntities.GREEN_BLOOMIE.get(), c -> new FpeRenderer<>(c, GreenBloomieSpec.SPEC));
        e.registerEntityRenderer(ModEntities.GREEN_ALICE.get(), c -> new FpeRenderer<>(c, GreenAliceSpec.PHASE1, GreenAliceSpec.PHASE2));
        e.registerEntityRenderer(ModEntities.GREEN_CIRCLE.get(), c -> new FpeRenderer<>(c, GreenCircleSpec.SPEC));
        e.registerEntityRenderer(ModEntities.HANSEL_JUVENILE.get(), c -> new FpeRenderer<>(c, HanselJuvenileSpec.SPEC));
        e.registerEntityRenderer(ModEntities.LORD_HANSEL.get(), c -> new FpeRenderer<>(c, LordHanselSpec.MATURED, LordHanselSpec.PREMATURE, LordHanselSpec.TRUE_FORM));
        e.registerEntityRenderer(ModEntities.PROJECTILE.get(), FpeProjectileRenderer::new);
        e.registerEntityRenderer(ModEntities.FX.get(), FpeFxRenderer::new);
    }

    /** (re)creates all procedural textures on every resource reload */
    @SubscribeEvent
    public static void reload(RegisterClientReloadListenersEvent e) {
        e.registerReloadListener((ResourceManagerReloadListener) rm -> registerTextures());
    }

    static void registerTextures() {
        Minecraft mc = Minecraft.getInstance();
        for (ModelSpec s : Specs.all()) {
            s.bake();
            mc.getTextureManager().register(s.texture(), new DynamicTexture(image(s.pixels(), s.texW, s.texH)));
            if (s.hasGlow()) mc.getTextureManager().register(s.glowTexture(), new DynamicTexture(image(s.glowPixels(), s.texW, s.texH)));
            int glErr = com.mojang.blaze3d.platform.GlStateManager._getError();
            org.slf4j.LoggerFactory.getLogger("fpe").info("FPE texture {} {}x{} glow={} glError={}", s.name, s.texW, s.texH, s.hasGlow(), glErr);
        }
        int[] white = new int[16 * 16];
        java.util.Arrays.fill(white, 0xFFFFFFFF);
        mc.getTextureManager().register(FxSpecs.WHITE, new DynamicTexture(image(white, 16, 16)));
    }

    private static NativeImage image(int[] argb, int w, int h) {
        NativeImage img = new NativeImage(NativeImage.Format.RGBA, w, h, true);
        for (int y = 0; y < h; y++) for (int x = 0; x < w; x++) {
            int c = argb[y * w + x];
            int a = c >>> 24, r = c >> 16 & 255, g = c >> 8 & 255, b = c & 255;
            img.setPixelRGBA(x, y, a << 24 | b << 16 | g << 8 | r);
        }
        return img;
    }
}
