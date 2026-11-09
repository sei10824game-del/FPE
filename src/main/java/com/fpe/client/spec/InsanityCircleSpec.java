package com.fpe.client.spec;

import com.fpe.client.model.Anim;
import com.fpe.client.model.AnimCtx;
import com.fpe.client.model.ModelParts;
import com.fpe.client.model.ModelSpec;
import com.fpe.client.model.ModelSpec.Face;
import com.fpe.client.model.ModelSpec.Pattern;

/**
 * FPE Insanity Miss Circle: huge black spiky mane + two tall horns, a single red spider-pupil eye, dark jacket with white collar and buttons,
 * baggy white striped trousers, tall striped boots, drawing compass (with a banded pencil leg) in the left hand and a hugely swollen black
 * clawed right hand about as long as the compass. Keyed to entity/characters/InsanityCircle.
 */
public final class InsanityCircleSpec {
    private InsanityCircleSpec() {}

    static final int INK = 0x0B0A10, INK2 = 0x1A1822, INK3 = 0x2B2833, FACE = 0xE8E6EC, FACE_D = 0xB4B2BC, JACKET = 0x15141C, WHITE = 0xF2F2F6, GREY = 0xB9BAC2,
            GREY_D = 0x8B8C96, STEEL = 0xC4C7CF, STEEL_D = 0x8E919B, WOOD = 0xD8C9A0, RED = 0xFF1428;

    public static final ModelSpec SPEC = build();

    private static ModelSpec build() {
        ModelSpec m = new ModelSpec("insanity_circle").shadow(0.9f);
        m.group("root", null, 0, 24, 0);
        m.group("spin", "root", 0, 12, 0);

        // legs: baggy striped trousers, folded cuffs, tall striped boots
        for (int s = -1; s <= 1; s += 2) {
            String k = s < 0 ? "R" : "L";
            float x = 2.4f * s;
            m.part("leg" + k, "spin", x, 12, 0, -2.7f, 0, -2.7f, 5.4f, 8, 5.4f, WHITE).pattern(Pattern.STRIPE_H, GREY, 2).grain(0.03f);
            m.part("cuff" + k, "leg" + k, x, 19, 0, -3, 0, -3, 6, 2, 6, WHITE).decor(Face.FRONT, 0, 1, 6, 1, GREY_D);
            m.part("boot" + k, "leg" + k, x, 20, 0, -2.4f, 0, -2.4f, 4.8f, 4, 4.8f, INK2).decor(Face.FRONT, 0, 0, 5, 1, WHITE).decor(Face.FRONT, 0, 2, 5, 1, WHITE)
                    .decor(Face.RIGHT, 0, 0, 5, 1, WHITE).decor(Face.LEFT, 0, 0, 5, 1, WHITE).decor(Face.RIGHT, 0, 2, 5, 1, WHITE).decor(Face.LEFT, 0, 2, 5, 1, WHITE);
            m.part("toe" + k, "boot" + k, x, 23.2f, 0, -2.4f, -0.8f, -5, 4.8f, 1.8f, 2.6f, INK);
        }
        // torso: dark jacket, white shirt front + collar, white buttons
        m.part("waist", "spin", 0, 12, 0, -4.3f, -2, -2.5f, 8.6f, 3, 5, WHITE).pattern(Pattern.STRIPE_H, GREY, 2);
        m.part("torso", "spin", 0, 12, 0, -4.4f, -11, -2.5f, 8.8f, 9.5f, 5, JACKET)
                .decor(Face.FRONT, 4, 0, 1, 9, INK).decor(Face.FRONT, 3, 3, 1, 1, WHITE).decor(Face.FRONT, 5, 3, 1, 1, WHITE).decor(Face.FRONT, 3, 6, 1, 1, WHITE).decor(Face.FRONT, 5, 6, 1, 1, WHITE)
                .decor(Face.FRONT, 3, 0, 3, 2, FACE_D).decor(Face.BACK, 3, 0, 2, 9, INK);
        m.part("collarR", "torso", -1.6f, 1.2f, -2.5f, -1.7f, -0.2f, -0.2f, 2.4f, 2.4f, 0.8f, WHITE).rot(0, 0, 25);
        m.part("collarL", "torso", 1.6f, 1.2f, -2.5f, -0.7f, -0.2f, -0.2f, 2.4f, 2.4f, 0.8f, WHITE).rot(0, 0, -25);
        m.part("hem", "torso", 0, 11, 0, -4.8f, -1, -2.9f, 9.6f, 2, 5.8f, INK2);

        // head: pale face with one huge red spider-pupil eye
        m.part("head", "torso", 0, 1, 0, -3.8f, -7.5f, -3.6f, 7.6f, 7.5f, 7.2f, FACE)
                .decor(Face.FRONT, 0, 2, 4, 4, INK).decor(Face.FRONT, 1, 3, 2, 2, 0x300408)
                .decorGlow(Face.FRONT, 1, 3, 2, 2, RED).decor(Face.FRONT, 0, 1, 1, 1, INK).decor(Face.FRONT, 4, 3, 1, 1, INK).decor(Face.FRONT, 2, 6, 1, 1, INK)
                .decor(Face.FRONT, 4, 1, 3, 1, FACE_D).decor(Face.FRONT, 5, 5, 2, 2, FACE_D);
        m.part("fringe", "head", 0, -4, -3.7f, 0.3f, -3.6f, -0.4f, 3.9f, 7.4f, 0.9f, INK).pattern(Pattern.STRIPE_V, INK2, 1);
        m.part("lockR", "head", -3.9f, -6, -1, -1.2f, 0, -2.6f, 1.6f, 13, 6.4f, INK).rot(0, 0, 5);
        m.part("lockL", "head", 3.9f, -6, -1, -0.4f, 0, -2.6f, 1.6f, 13, 6.4f, INK).rot(0, 0, -5);
        m.part("hairTop", "head", 0, -7.5f, 0, -4.4f, -1.8f, -4.2f, 8.8f, 2.4f, 8.6f, INK);
        m.part("hairBack", "head", 0, -7, 3, -6.2f, 0, 0, 12.4f, 28, 3.6f, INK).pattern(Pattern.STRIPE_V, INK2, 3).grain(0.03f);
        for (int i = 0; i < 18; i++) {   // jagged mane spikes fanning behind and to the sides
            float a = -160 + i * 18.8f;
            float len = 9 + (i * 7 % 6) * 1.6f;
            double r = Math.toRadians(a);
            m.part("mane" + i, "head", (float) Math.sin(r) * 4.5f, -3 - (float) Math.abs(Math.cos(r)) * 3, 2 + (float) Math.cos(r) * 2f, -1, 0, -0.6f, 2, len, 1.4f, i % 2 == 0 ? INK : INK2)
                    .rot(18 + (i % 3) * 10, 0, a * 0.55f);
        }
        m.part("hornA", "head", -1.9f, -8, 0.2f, -1, -12, -1, 2, 12, 2, INK).rot(-14, 0, -24).grain(0.02f);
        m.part("hornB", "head", 2.1f, -8, 0.2f, -1, -14, -1, 2, 14, 2, INK).rot(-10, 0, 26).grain(0.02f);
        m.part("hornC", "head", 0.1f, -8, 1.4f, -0.8f, -10, -0.8f, 1.6f, 10, 1.6f, INK2).rot(-20, 0, 2);

        // left arm: compass
        m.part("armL", "torso", 5.7f, 1.5f, 0, -2, -1, -2, 4, 8, 4, JACKET).rot(-30, 0, -4).decor(Face.FRONT, 0, 6, 4, 2, INK2);
        m.part("foreL", "armL", 5.7f, 9.5f, 0, -1.8f, 0, -1.8f, 3.6f, 6, 3.6f, JACKET).rot(-26, 0, 0).decor(Face.FRONT, 0, 4, 4, 1, WHITE);
        m.part("handL", "foreL", 5.7f, 15.5f, 0, -1.5f, 0, -1.5f, 3, 3, 3, FACE);
        m.group("compass", "handL", 5.7f, 17, -0.5f).rot(48, 0, 0);
        m.part("handle", "compass", 5.7f, 17, -0.5f, -1.3f, -1.6f, -1, 2.6f, 3.2f, 3, INK3).decor(Face.TOP, 0, 0, 3, 1, WHITE).decor(Face.TOP, 0, 2, 3, 1, WHITE);
        m.part("legA", "compass", 5.7f, 17, -0.5f, -2.1f, -0.7f, -26, 1.5f, 1.5f, 26, STEEL).pattern(Pattern.STRIPE_H, STEEL_D, 3).rot(0, 2.5f, 0).grain(0.04f);
        m.part("legB", "compass", 5.7f, 17, -0.5f, 0.6f, -0.7f, -26, 1.5f, 1.5f, 26, WOOD).pattern(Pattern.STRIPE_H, 0xB89E68, 2).rot(0, -2.5f, 0);
        for (int i = 0; i < 3; i++) m.part("band" + i, "legB", 5.7f, 17, -0.5f, 0.45f, -0.85f, -25 + i * 2.2f, 1.8f, 1.8f, 1.2f, INK2).rot(0, -2.5f, 0);
        m.part("lead", "legB", 5.7f, 17, -0.5f, 0.8f, -0.4f, -29, 0.9f, 0.9f, 3, INK).rot(0, -2.5f, 0);
        m.part("needle", "legA", 5.7f, 17, -0.5f, -1.8f, -0.4f, -30, 0.8f, 0.8f, 4, STEEL_D).rot(0, 2.5f, 0);

        // right arm: a long black tentacle (segments taper toward a glowing tip)
        m.part("armR", "torso", -5.9f, 1.5f, 0, -2.4f, -1, -2.4f, 4.8f, 6, 4.8f, JACKET).rot(-10, 0, 10);
        m.part("foreR", "armR", -5.9f, 6.5f, 0, -3f, 0, -3f, 6, 7, 6, INK).grain(0.05f).decor(Face.FRONT, 1, 2, 4, 1, INK3).decor(Face.FRONT, 1, 5, 4, 1, INK3);
        String par = "foreR";
        for (int i = 0; i < 10; i++) {
            int wd = Math.max(2, Math.round(5.4f - i * 0.38f));
            m.part("tent" + i, par, -5.9f, 13.5f + i * 6.5f, 0, -wd / 2f, 0, -wd / 2f, wd, 6.5f, wd, i % 2 == 0 ? INK : INK2).grain(0.05f)
                    .decor(Face.FRONT, 0, 1, 1, 1, 0x4A2030).decor(Face.FRONT, Math.max(0, wd - 1), 4, 1, 1, 0x4A2030)
                    .rot(i == 0 ? 6 : i < 3 ? 4 : -22, 0, 0);
            if (i % 2 == 1) m.part("tspike" + i, "tent" + i, -5.9f, 13.5f + i * 6.5f + 3, 0, -0.4f, 0, 1.6f, 0.8f, 0.8f, 3, INK3).rot(30, 0, 0);
            par = "tent" + i;
        }
        m.part("tentTip", par, -5.9f, 13.5f + 10 * 6.5f, 0, -0.6f, 0, -0.6f, 1.2f, 4, 1.2f, RED).glow();

        m.animator(InsanityCircleSpec::animate);
        return m;
    }

    /** bend all tentacle segments: base curl on the first, rest follow */
    private static void tent(ModelParts m, float first, float rest, float up, float dn) {
        for (int i = 0; i < 10; i++) m.addRot("tent" + i, (i == 0 ? 0 : -1) * 0 + (i > 2 ? (-18 * up + 30 * dn) : (-6 * up + 8 * dn)) * rest, 0, 0);
    }

    private static void animate(ModelParts m, AnimCtx c) {
        float a = c.age, t = c.t, w = c.walk(), ls = c.limbSwing;

        // idle: heavy hunch, eye-twitch sway; walk: lumbering with the claw dragging
        for (String k : new String[] {"R", "L"}) {
            float ph = k.equals("R") ? 0 : 3.14159f, sw = Anim.sinr(ls * 0.55f + ph) * w;
            m.addRot("leg" + k, sw * 36, 0, 0);
            m.addRot("boot" + k, Math.max(0, -sw) * 22, 0, 0);
        }
        m.addRot("torso", 6 + Anim.sinr(a * 0.07f) * 1.6f + w * 5, Anim.sinr(ls * 0.55f) * 6 * w, 0);
        m.addRot("head", 8 + Anim.sinr(a * 0.05f + 1) * 3, Math.max(-40, Math.min(40, c.headYaw)) * 0.7f + Anim.sinr(a * 0.33f) * (c.idle() ? 1.5f : 0), Anim.sinr(a * 0.04f) * 2);
        m.addRot("armR", Anim.sinr(ls * 0.55f) * 18 * w + Anim.sinr(a * 0.06f) * 2, 0, 0);
        for (int i = 0; i < 10; i++) m.addRot("tent" + i, Anim.sinr(a * 0.1f - i * 0.55f) * 7 + Anim.sinr(ls * 0.55f - i * 0.4f) * 8 * w, 0, Anim.sinr(a * 0.08f - i * 0.5f) * 5);
        m.addRot("armL", Anim.sinr(ls * 0.55f + 3.14f) * 10 * w, 0, 0);
        m.addRot("compass", Anim.sinr(a * 0.09f) * 3 + w * 4, 0, 0);
        m.addRot("hairBack", 3 + Anim.sinr(a * 0.05f) * 2 + w * 8, 0, 0);
        for (int i = 0; i < 18; i++) m.addRot("mane" + i, Anim.sinr(a * 0.1f + i * 0.6f) * 6 + w * 10, 0, Anim.sinr(a * 0.07f + i) * 3);
        m.addRot("hornA", Anim.sinr(a * 0.04f) * 2, 0, 0);
        m.move("spin", 0, Anim.sinr(ls * 1.1f) * 0.5f * w, 0);
        m.scale("torso", 0.9f, 1, 0.9f);
        m.scale("root", 1.04f, 1.04f, 1.04f);   // match Miss Circle (head top 46.4px vs 44.6px above ground)

        if (c.is("compass_sweep")) {
            float wind = Anim.curve(t, 0, 0, 14, 1, 16, 0, 38, 0);
            float sw = Anim.curve(t, 0, 0, 14, 0, 18, 1, 28, 1, 38, 0);
            m.addRot("torso", -8 * wind + 10 * sw, Anim.curve(t, 0, 0, 14, 60, 18, -80, 28, -80, 38, 0), 0);
            m.addRot("armL", -40 * wind - 30 * sw, 0, 50 * wind - 90 * sw);
            m.addRot("compass", -25 * wind, 0, 0);
            m.addRot("armR", -20 * wind + 30 * sw, 0, 40 * sw);
            m.addRot("legR", -16 * sw, 0, 0); m.addRot("legL", 14 * sw, 0, 0);
        } else if (c.is("compass_lunge")) {
            float draw = Anim.curve(t, 0, 0, 14, 1, 16, 0, 34, 0);
            float th = Anim.curve(t, 0, 0, 14, 0, 17, 1, 24, 1, 34, 0);
            m.addRot("torso", -10 * draw + 28 * th, 0, 0);
            m.addRot("armL", 20 * draw - 70 * th, 0, 0);
            m.addRot("foreL", 30 * draw - 40 * th, 0, 0);
            m.addRot("compass", -20 * th, 0, 0);
            m.addRot("head", -8 * draw + 10 * th, 0, 0);
            m.addRot("legR", -26 * th, 0, 0); m.addRot("legL", 20 * th, 0, 0);
            m.addRot("armR", 25 * th, 0, 20 * th);
        } else if (c.is("split_slam")) {
            float up = Anim.curve(t, 0, 0, 12, 1, 20, 1, 22, 0, 42, 0);
            float dn = Anim.curve(t, 0, 0, 20, 0, 23, 1, 36, 1, 42, 0);
            m.move("spin", 0, -5 * Anim.curve(t, 0, 0, 12, 0, 16, 1, 22, 0, 42, 0), 0);
            m.addRot("torso", -22 * up + 40 * dn, 0, 0);
            m.addRot("armL", -150 * up + 100 * dn, 0, 0);
            m.addRot("armR", -110 * up + 90 * dn, 0, 0);
            m.addRot("head", -12 * up + 12 * dn, 0, 0);
            m.addRot("legR", 20 * up - 10 * dn, 0, 0); m.addRot("legL", -24 * up + 22 * dn, 0, 0);
        } else if (c.is("compass_throw")) {
            float wind = Anim.curve(t, 0, 0, 15, 1, 17, 0, 40, 0);
            float thr = Anim.curve(t, 0, 0, 15, 0, 18, 1, 28, 0, 40, 0);
            m.addRot("torso", -14 * wind + 18 * thr, Anim.curve(t, 0, 0, 15, 30, 18, -24, 40, 0), 0);
            m.addRot("armL", -130 * wind + 150 * thr, 0, 0);
            m.addRot("compass", 0, 0, 0);
            m.addRot("armR", 20 * wind, 0, 0);
            m.show("compass", !(t > 17 && t < 36));
        } else if (c.is("draw_circle")) {
            float st = Anim.curve(t, 0, 0, 8, 1, 46, 1, 56, 0);
            m.move("spin", 0, 6 * st, 0);
            m.addRot("torso", 22 * st, Anim.linear(t, 0, 0, 8, 0, 44, 720), 0);
            m.addRot("armL", -50 * st, 0, 60 * st);
            m.addRot("compass", 52 * st, 0, 0);
            m.addRot("armR", -30 * st, 0, -60 * st);
            m.addRot("legR", -28 * st, 0, 0); m.addRot("legL", -28 * st, 0, 0);
            m.addRot("boot" + "R", 40 * st, 0, 0); m.addRot("boot" + "L", 40 * st, 0, 0);
        } else if (c.is("tentacle_slam")) {
            float up = Anim.curve(t, 0, 0, 17, 1, 19, 0, 44, 0);
            float dn = Anim.curve(t, 0, 0, 18, 0, 21, 1, 36, 1, 44, 0);
            m.addRot("torso", -22 * up + 34 * dn, Anim.curve(t, 0, 0, 17, -18, 21, 12, 44, 0), 0);
            m.addRot("armR", -170 * up + 185 * dn, 0, 10 * up);
            tent(m, -(-30 * up) , 1, up, dn);
            m.addRot("head", -10 * up + 12 * dn, 0, 0);
            m.addRot("armL", 20 * dn, 0, 0);
        } else if (c.is("tentacle_lash")) {
            m.addRot("torso", 8, Anim.curve(t, 0, 0, 10, 30, 14, -26, 19, 30, 24, -26, 28, 20, 40, 0), 0);
            float r = Anim.curve(t, 0, 0, 6, -100, 12, 40, 14, -110, 19, 40, 21, -110, 26, 40, 32, 0, 40, 0);
            m.addRot("armR", r, 0, 0);
            for (int i = 0; i < 10; i++) m.addRot("tent" + i, (r < 0 ? -24 : 18) * (i < 4 ? 0.4f : 1), 0, 0);
            m.addRot("legR", -14, 0, 0); m.addRot("legL", 14, 0, 0);
        } else if (c.is("tentacle_spear")) {
            float dr = Anim.curve(t, 0, 0, 14, 1, 16, 0, 36, 0);
            float th = Anim.curve(t, 0, 0, 14, 0, 17, 1, 26, 1, 36, 0);
            m.addRot("torso", -10 * dr + 24 * th, 0, 0);
            m.addRot("armR", -40 * dr - 85 * th, 0, -8 * th);
            for (int i = 0; i < 10; i++) m.addRot("tent" + i, (30 + 22) * dr * (i > 2 ? 1 : 0.4f) + (-22 - 0) * 0 - 24 * th * (i > 0 ? 1 : 0) * -1 * 0 + 22 * th * (i > 0 ? 1 : 0), 0, 0);
            m.addRot("legR", -22 * th, 0, 0); m.addRot("legL", 18 * th, 0, 0);
        } else if (c.is("tentacle_grab")) {
            float re = Anim.curve(t, 0, 0, 12, 1, 14, 0, 50, 0);
            float gr = Anim.curve(t, 0, 0, 12, 0, 15, 1, 26, 1, 40, 0.8f, 42, 0, 50, 0);
            m.addRot("torso", -6 * re + 14 * gr, 0, 0);
            m.addRot("armR", -40 * re - 80 * gr, 0, -10 * gr);
            for (int i = 0; i < 10; i++) m.addRot("tent" + i, 20 * re * (i > 2 ? 1 : 0.3f) - (i > 4 ? 40 : 6) * gr, 0, 0);
            m.addRot("head", 6 * gr, 0, 0);
        } else if (c.is("tentacle_erupt")) {
            float up = Anim.curve(t, 0, 0, 14, 1, 17, 0.6f, 46, 0);
            m.addRot("torso", -12 * up + 20 * Anim.curve(t, 0, 0, 14, 0, 17, 1, 34, 1, 46, 0), 0, 0);
            m.addRot("armR", -120 * up + 170 * Anim.curve(t, 0, 0, 15, 0, 18, 1, 34, 0.8f, 46, 0), 0, 0);
            m.addRot("armL", -40 * up, 0, -40 * up);
            m.addRot("head", -18 * up, 0, 0);
        } else if (c.is("compass_frenzy")) {
            float ph = Anim.sinr(a * 1.15f);
            m.addRot("torso", 14, Anim.sinr(a * 0.55f) * 38, Anim.sinr(a * 0.5f) * 6);
            m.addRot("armL", -70 + ph * 60, 0, Anim.sinr(a * 0.55f + 1) * 70);
            m.addRot("foreL", -20, 0, 0);
            m.addRot("compass", ph * 25, 0, 0);
            m.addRot("head", 8, -Anim.sinr(a * 0.55f) * 18, 0);
            m.addRot("legR", ph * 26, 0, 0); m.addRot("legL", -ph * 26, 0, 0);
            m.addRot("armR", 25 + ph * 25, 0, 20);
        } else if (c.is("compass_cleave")) {
            float up = Anim.curve(t, 0, 0, 20, 1, 22, 0, 44, 0);
            float dn = Anim.curve(t, 0, 0, 20, 0, 24, 1, 36, 1, 44, 0);
            m.move("spin", 0, -3 * Anim.curve(t, 0, 0, 16, 0, 20, 1, 24, 0, 44, 0), 0);
            m.addRot("torso", -28 * up + 50 * dn, Anim.curve(t, 0, 0, 20, -14, 24, 10, 44, 0), 0);
            m.addRot("armL", -170 * up + 200 * dn, 0, 0);
            m.addRot("compass", -15 * up + 20 * dn, 0, 0);
            m.addRot("head", -14 * up + 16 * dn, 0, 0);
            m.addRot("legR", 20 * up - 14 * dn, 0, 0); m.addRot("legL", -22 * up + 20 * dn, 0, 0);
            m.addRot("armR", -50 * up + 70 * dn, 0, 40 * up);
        } else if (c.is("hair_lash")) {
            float st = Anim.curve(t, 0, 0, 8, 1, 26, 1, 34, 0);
            m.addRot("spin", 0, Anim.linear(t, 0, 0, 12, 0, 24, -400, 99, -400), 0);
            m.addRot("hairBack", 40 * st, 0, 0);
            for (int i = 0; i < 18; i++) m.addRot("mane" + i, 30 * st, 0, (i - 9) * 4 * st);
            m.addRot("armR", -50 * st, 0, 60 * st); m.addRot("armL", -50 * st, 0, -60 * st);
        } else if (c.is("eye_beam")) {
            float ch = Anim.curve(t, 0, 0, 10, 1, 32, 1, 40, 0.2f, 54, 0);
            m.addRot("torso", -16 * ch, 0, 0);
            m.addRot("head", -24 * ch + Anim.sinr(a * 3f) * 3 * ch, 0, 0);
            m.addRot("armR", -40 * ch, 0, 50 * ch); m.addRot("armL", -40 * ch, 0, -50 * ch);
            for (int i = 0; i < 18; i++) m.addRot("mane" + i, -25 * ch, 0, 0);
        } else if (c.is("rampage")) {
            float ph = Anim.sinr(a * 1.0f);
            m.addRot("torso", 18, Anim.sinr(a * 0.45f) * 18, 0);
            m.addRot("armR", -70 + ph * 70, 0, 0);
            m.addRot("armL", -30 - ph * 50, 0, 0);
            m.addRot("head", 12, 0, 0);
            m.addRot("legR", ph * 30, 0, 0); m.addRot("legL", -ph * 30, 0, 0);
        }
        if (!c.is("compass_throw")) m.show("compass", true);

        if (c.death > 0) {
            float d = Anim.easeOut(c.death);
            m.addRot("root", -86 * d, 0, 0);
            m.move("root", 0, -2 * d, 0);
            m.addRot("armR", 40 * d, 0, 20 * d); m.addRot("armL", 20 * d, 0, -20 * d);
        }
    }
}
