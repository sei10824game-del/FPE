package com.fpe.client.spec;

import com.fpe.client.model.Anim;
import com.fpe.client.model.AnimCtx;
import com.fpe.client.model.ModelParts;
import com.fpe.client.model.ModelSpec;
import com.fpe.client.model.ModelSpec.Face;
import com.fpe.client.model.ModelSpec.Pattern;

/** "Crazy" (original design): wiry, hunched, wild teal hair spikes, huge white eyes with pinprick pupils, a stitched ear-to-ear grin, patched oversized coat, mismatched boots, rusty wrench. */
public final class CrazyOneSpec {
    private CrazyOneSpec() {}

    static final int SKIN = 0xD9CFC2, SKIN_D = 0xB4AAA0, HAIR = 0x2C8C86, HAIR_D = 0x1C5E5A, COAT = 0x5B4A66, COAT_D = 0x3E3248, PATCH = 0xC9A24A, PANTS = 0x2E2B33,
            BOOT_A = 0xA23A32, BOOT_B = 0x3A5A8A, EYE = 0xFAFAF4, PUPIL = 0x120808, MOUTH = 0x2A0E12, TOOTH = 0xF0ECDC, STITCH = 0x1A1416, RUST = 0x8A4E2A, RUST_D = 0x5E3418, STEEL = 0x9A9EA4;

    public static final ModelSpec SPEC = build();

    private static ModelSpec build() {
        ModelSpec m = new ModelSpec("crazy_one").shadow(0.6f);
        m.group("root", null, 0, 24, 0);
        m.group("spin", "root", 0, 12, 0);
        for (int s = -1; s <= 1; s += 2) {
            String k = s < 0 ? "R" : "L";
            float x = 2f * s;
            m.part("leg" + k, "spin", x, 12, 0, -1.6f, 0, -1.6f, 3.2f, 7, 3.2f, PANTS).decor(Face.FRONT, 0, 3, 3, 2, COAT_D);
            m.part("shin" + k, "leg" + k, x, 19, 0, -1.9f, 0, -1.9f, 3.8f, 5, 3.8f, s < 0 ? BOOT_A : BOOT_B).decor(Face.FRONT, 0, 0, 4, 1, PATCH);
            m.part("toe" + k, "shin" + k, x, 23, 0, -1.9f, -0.8f, -4.4f, 3.8f, 1.6f, 2.6f, s < 0 ? BOOT_A : BOOT_B);
        }
        m.part("coatSkirt", "spin", 0, 12, 0, -4.4f, -1, -2.8f, 8.8f, 8, 5.6f, COAT).pattern(Pattern.STRIPE_V, COAT_D, 2).decor(Face.FRONT, 5, 3, 3, 3, PATCH).decor(Face.FRONT, 1, 5, 2, 2, SKIN_D);
        m.part("torso", "spin", 0, 12, 0, -4.2f, -12, -2.3f, 8.4f, 11, 4.6f, COAT).grain(0.07f).rot(10, 0, 0)
                .decor(Face.FRONT, 0, 2, 3, 3, PATCH).decor(Face.FRONT, 5, 6, 3, 3, COAT_D).decor(Face.FRONT, 4, 0, 1, 11, STITCH);
        m.part("collar", "torso", 0, 0, 0, -4.6f, -13, -2.7f, 9.2f, 2.4f, 5.4f, COAT_D);
        m.part("head", "torso", 0, 0, 0, -3.6f, -8.2f, -3.6f, 7.2f, 7.4f, 7.2f, SKIN).grain(0.05f).rot(-6, 0, 4)
                .decor(Face.FRONT, 0, 1, 3, 3, EYE).decor(Face.FRONT, 4, 1, 3, 3, EYE).decorGlow(Face.FRONT, 1, 2, 1, 1, PUPIL).decorGlow(Face.FRONT, 5, 2, 1, 1, PUPIL)
                .decor(Face.FRONT, 0, 4, 7, 3, MOUTH).decor(Face.FRONT, 0, 4, 1, 1, TOOTH).decor(Face.FRONT, 2, 4, 1, 1, TOOTH).decor(Face.FRONT, 4, 4, 1, 1, TOOTH).decor(Face.FRONT, 6, 4, 1, 1, TOOTH)
                .decor(Face.FRONT, 1, 6, 1, 1, TOOTH).decor(Face.FRONT, 3, 6, 1, 1, TOOTH).decor(Face.FRONT, 5, 6, 1, 1, TOOTH)
                .decor(Face.FRONT, 0, 5, 1, 2, STITCH).decor(Face.FRONT, 6, 5, 1, 2, STITCH).decor(Face.FRONT, 0, 0, 7, 1, SKIN_D);
        m.part("hairTop", "head", 0, -8.2f, 0, -3.9f, -1.6f, -3.9f, 7.8f, 2.2f, 7.8f, HAIR);
        m.part("hairBack", "head", 0, -7, 3, -3.9f, 0, 0, 7.8f, 9, 1.8f, HAIR_D);
        for (int i = 0; i < 9; i++) {
            float a = -80 + i * 20;
            m.part("spike" + i, "head", (float) Math.sin(Math.toRadians(a)) * 3.2f, -8.4f, (float) Math.cos(Math.toRadians(a)) * 1.5f - 0.5f, -0.9f, -5 - (i % 3) * 1.8f, -0.9f, 1.8f, 5 + (i % 3) * 1.8f, 1.8f, i % 2 == 0 ? HAIR : HAIR_D)
                    .rot(-8 + (i % 2) * 14, 0, a * 0.7f);
        }
        for (int s = -1; s <= 1; s += 2) {
            String k = s < 0 ? "R" : "L";
            float x = 5.2f * s;
            m.part("arm" + k, "torso", x, -10, 0, -1.7f, -1, -1.7f, 3.4f, 8, 3.4f, COAT).decor(Face.FRONT, 0, 5, 4, 2, PATCH);
            m.part("fore" + k, "arm" + k, x, -3, 0, -1.5f, 0, -1.5f, 3, 7, 3, SKIN).decor(Face.FRONT, 0, 1, 3, 1, 0xE8E4D8).decor(Face.FRONT, 0, 3, 3, 1, 0xE8E4D8).decor(Face.FRONT, 0, 5, 3, 1, 0xE8E4D8);
            m.part("hand" + k, "fore" + k, x, 4, 0, -1.4f, 0, -1.4f, 2.8f, 2.8f, 2.8f, SKIN_D);
        }
        m.group("wrench", "handR", -5.2f, 6, -0.5f);
        m.part("wrenchShaft", "wrench", -5.2f, 6, -0.5f, -0.9f, -1, -13, 1.8f, 1.8f, 14, RUST).pattern(Pattern.STRIPE_H, RUST_D, 3).rot(-20, 0, 0);
        m.part("wrenchHead", "wrenchShaft", -5.2f, 6, -13.5f, -2.2f, -2.2f, -3.4f, 4.4f, 4.4f, 3.4f, STEEL).grain(0.08f).rot(-20, 0, 0).decor(Face.FRONT, 1, 1, 2, 2, RUST_D);
        m.animator(CrazyOneSpec::animate);
        return m;
    }

    private static float sgn(String k) { return k.equals("R") ? -1f : 1f; }

    private static void animate(ModelParts m, AnimCtx c) {
        float a = c.age, t = c.t, w = c.walk(), ls = c.limbSwing;
        // jittery idle: twitching head, bobbing knees; walk: skipping, uneven
        for (String k : new String[] {"R", "L"}) {
            float ph = k.equals("R") ? 0 : 3.14159f, sw = Anim.sinr(ls * 0.75f + ph) * w;
            m.addRot("leg" + k, sw * 48, 0, 0);
            m.addRot("shin" + k, Math.max(0, -sw) * 40, 0, 0);
            m.addRot("arm" + k, -sw * 36 + Anim.sinr(a * 0.4f + ph) * 4, 0, sgn(k) * -4);
        }
        m.addRot("torso", Anim.sinr(a * 0.5f) * 2.5f, Anim.sinr(a * 0.31f) * 4 + Anim.sinr(ls * 0.75f) * 8 * w, Anim.sinr(a * 0.27f) * 3);
        m.addRot("head", Anim.sinr(a * 0.9f) * 3, Math.max(-40, Math.min(40, c.headYaw)) * 0.7f + Anim.sinr(a * 0.63f) * 6, Anim.sinr(a * 0.45f) * 5);
        for (int i = 0; i < 9; i++) m.addRot("spike" + i, Anim.sinr(a * 0.5f + i) * 8, 0, 0);
        m.addRot("wrench", Anim.sinr(a * 0.35f) * 6, 0, 0);
        m.move("spin", 0, Math.abs(Anim.sinr(ls * 0.75f)) * 0.9f * w + Anim.sinr(a * 0.5f) * 0.3f, 0);

        if (c.is("frantic_flurry")) {
            float ph = Anim.sinr(a * 1.7f);
            float st = Anim.curve(t, 0, 0, 6, 1, 34, 1, 40, 0);
            m.addRot("torso", 14 * st, ph * 24 * st, 0);
            m.addRot("armR", (-70 + ph * 70) * st, 0, 10); m.addRot("armL", (-70 - ph * 70) * st, 0, -10);
            m.addRot("head", 8 * st, -ph * 14 * st, 0);
            m.addRot("legR", ph * 20 * st, 0, 0); m.addRot("legL", -ph * 20 * st, 0, 0);
        } else if (c.is("wrench_smash")) {
            float up = Anim.curve(t, 0, 0, 15, 1, 17, 0, 34, 0);
            float dn = Anim.curve(t, 0, 0, 16, 0, 19, 1, 28, 1, 34, 0);
            m.addRot("torso", -20 * up + 34 * dn, Anim.curve(t, 0, 0, 15, -16, 18, 12, 34, 0), 0);
            m.addRot("armR", -165 * up + 190 * dn, 0, 8 * up);
            m.addRot("wrench", -20 * up + 24 * dn, 0, 0);
            m.addRot("armL", -40 * up + 40 * dn, 0, -30 * up);
            m.addRot("head", -10 * up + 12 * dn, 0, 0);
        } else if (c.is("zigzag_dash")) {
            float sw = Anim.sinr(t * 0.52f);
            float run = Anim.curve(t, 0, 0, 5, 1, 32, 1, 40, 0);
            m.addRot("torso", 22 * run, sw * 28 * run, sw * 12 * run);
            m.addRot("armR", -60 * run, 0, 20 * run); m.addRot("armL", -60 * run, 0, -20 * run);
            m.addRot("legR", sw * 40 * run, 0, 0); m.addRot("legL", -sw * 40 * run, 0, 0);
            m.addRot("head", -8 * run, -sw * 16 * run, 0);
        } else if (c.is("cackle")) {
            float up = Anim.curve(t, 0, 0, 12, 1, 36, 1, 44, 0);
            float sh = Anim.sinr(a * 2.4f) * (t > 12 && t < 36 ? 1 : 0);
            m.addRot("torso", -22 * up + sh * 4, sh * 6, 0);
            m.addRot("head", -34 * up + sh * 6, sh * 8, sh * 6);
            m.addRot("armR", -40 * up, 0, 70 * up); m.addRot("armL", -40 * up, 0, -70 * up);
            m.move("spin", 0, sh * 0.8f, 0);
        } else if (c.is("junk_throw")) {
            float wd = Anim.curve(t, 0, 0, 15, 1, 17, 0, 34, 0);
            float th = Anim.curve(t, 0, 0, 14, 0, 17, 1, 26, 0.3f, 34, 0);
            m.addRot("torso", -12 * wd + 16 * th, Anim.curve(t, 0, 0, 14, 28, 18, -22, 34, 0), 0);
            m.addRot("armR", -140 * wd + 170 * th, 0, 0);
            m.addRot("armL", -60 * th, 0, -20 * th);
        } else if (c.is("tantrum")) {
            float up = Anim.curve(t, 0, 0, 10, 1, 14, 0, 40, 0);
            float st = Anim.curve(t, 0, 0, 14, 0, 16, 1, 18, 0, 24, 1, 26, 0, 40, 0);
            m.move("spin", 0, -3 * st + 2 * up, 0);
            m.addRot("torso", -10 * up + 14 * st, 0, 0);
            m.addRot("armR", -150 * up + 160 * st, 0, 20 * up); m.addRot("armL", -150 * up + 160 * st, 0, -20 * up);
            m.addRot("legR", -40 * up + 40 * st, 0, 0); m.addRot("legL", 20 * up - 30 * st, 0, 0);
            m.addRot("head", 10 * st, 0, 0);
        } else if (c.is("jump_scare")) {
            float cr = Anim.curve(t, 0, 0, 6, 1, 8, 0, 36, 0);
            float st = Anim.curve(t, 0, 0, 16, 0, 20, 1, 28, 0.5f, 36, 0);
            m.move("spin", 0, 4 * cr, 0);
            m.addRot("torso", 18 * cr + 20 * st, 0, 0);
            m.addRot("armR", -120 * st, 0, 0);
            m.addRot("head", -20 * st, 0, 0);
        } else if (c.is("meltdown")) {
            float ph = Anim.sinr(a * 1.5f);
            m.addRot("torso", 20, Anim.sinr(a * 0.9f) * 30, Anim.sinr(a * 0.7f) * 8);
            m.addRot("armR", -90 + ph * 90, 0, 20); m.addRot("armL", -90 - ph * 90, 0, -20);
            m.addRot("head", 10, Anim.sinr(a * 1.1f) * 16, 0);
            m.addRot("legR", ph * 36, 0, 0); m.addRot("legL", -ph * 36, 0, 0);
        }
        if (c.death > 0) {
            float d = Anim.easeOut(c.death);
            m.addRot("root", -86 * d, 0, 0);
            m.move("root", 0, -2 * d, 0);
            m.addRot("armR", 40 * d, 0, 25 * d); m.addRot("armL", 30 * d, 0, -25 * d);
        }
    }
}
