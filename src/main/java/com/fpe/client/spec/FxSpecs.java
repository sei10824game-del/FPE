package com.fpe.client.spec;

import com.fpe.FpeMod;
import com.fpe.client.model.Anim;
import com.fpe.client.model.ModelSpec;

import net.minecraft.resources.ResourceLocation;

/** Models for FpeFx: ground spike + tentacle. WHITE is a plain texture used for flat quads. */
public final class FxSpecs {
    private FxSpecs() {}

    public static final ResourceLocation WHITE = new ResourceLocation(FpeMod.MODID, "dyn/white");

    public static final ModelSpec SPIKE = new ModelSpec("fx_spike");
    public static final ModelSpec TENTACLE = new ModelSpec("fx_tentacle");

    static {
        ModelSpec s = SPIKE;
        s.group("root", null, 0, 24, 0);
        int[] ws = {10, 7, 5, 3, 1};
        float y = 24;
        for (int i = 0; i < ws.length; i++) {
            y -= 7;
            s.part("s" + i, "root", 0, y + 7, 0, -ws[i] / 2f, 0, -ws[i] / 2f, ws[i], 7, ws[i], i == ws.length - 1 ? 0x701020 : 0x1A1022 + i * 0x040204).grain(0.12f);
        }
        s.part("tip", "root", 0, y, 0, -0.5f, -2, -0.5f, 1, 2, 1, 0xFF3050).glow();
        s.group("dummy", "root", 0, 24, 0);

        ModelSpec t = TENTACLE;
        t.group("t_root", null, 0, 24, 0);
        String par = "t_root";
        float py = 24;
        for (int i = 0; i < 8; i++) {
            float w = Math.max(2f, 6f - i * 0.55f);
            int wi = Math.round(w);
            t.part("t" + i, par, 0, py, 0, -wi / 2f, -7, -wi / 2f, wi, 7, wi, 0x14101C + i * 0x020102).grain(0.1f)
                    .decor(ModelSpec.Face.FRONT, 0, 2, 1, 1, 0x6A5A7A).decor(ModelSpec.Face.FRONT, Math.max(0, wi - 1), 5, 1, 1, 0x6A5A7A);
            par = "t" + i;
            py -= 7;
        }
        t.part("t_tip", par, 0, py, 0, -1, -4, -1, 2, 4, 2, 0xA01830).glow();
        t.animator((m, c) -> {
            float amp = 1f;
            for (int i = 0; i < 8; i++) {
                float ph = c.age * 0.22f - i * 0.65f;
                m.rot("t" + i, Anim.sinr(ph * 0.8f + 1f) * (4 + i * 1.5f) * amp, 0, Anim.sinr(ph) * (7 + i * 2.2f) * amp);
            }
        });
    }
}
