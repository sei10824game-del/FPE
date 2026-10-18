package com.fpe.client.spec;

import com.fpe.client.model.Anim;
import com.fpe.client.model.AnimCtx;
import com.fpe.client.model.ModelParts;
import com.fpe.client.model.ModelSpec;
import com.fpe.client.model.ModelSpec.Face;
import com.fpe.client.model.ModelSpec.Pattern;

/**
 * Infected Zip (Basics in Survival AU): hunched inked quadruped, hatched black hide, huge fanged maw, bristling mane and back spikes,
 * paper spiral flag on a stalk, one bat-blade wing and a long blade tail. Keyed to entity/characters/InfectedZip.
 */
public final class InfectedZipSpec {
    private InfectedZipSpec() {}

    static final int INK = 0x15141A, FUR = 0x26242E, FUR2 = 0x34313F, PAPER = 0xE8E6EE, PAPER_DK = 0xB9B7C6, EYE = 0xFFFFFF, OOZE = 0x0A090D;

    public static final ModelSpec SPEC = com.fpe.client.model.BbModel.load("infected_zip", 1.2f);
    static final ModelSpec PROC = build();

    private static ModelSpec build() {
        ModelSpec m = new ModelSpec("infected_zip").shadow(1.2f);
        m.group("root", null, 0, 24, 0);
        m.group("torso", "root", 0, 5, 2);

        // ---------------------------------------------------------------- body
        m.part("chest", "torso", 0, 5, 2, -5, -7, -10, 10, 12, 10, INK).pattern(Pattern.DIAG, FUR, 1).grain(0.08f);
        m.part("belly", "torso", 0, 5, 2, -3.5f, -4, 0, 7, 9, 10, INK).pattern(Pattern.DIAG, FUR, 1).grain(0.08f);
        m.part("rump", "torso", 0, 5, 2, -4, -5, 9, 8, 10, 6, INK).pattern(Pattern.DIAG, FUR2, 1).grain(0.08f);
        float[] sz = {-8, -5, -2, 1, 4, 7, 10, 13};
        for (int i = 0; i < sz.length; i++) {
            float h = 4 + (i % 3) * 1.5f;
            m.part("spine" + i, "torso", 0, sz[i] < 0 ? -1.5f : 0.5f, sz[i] + 2, -0.6f, -h, -0.6f, 1.2f, h, 1.2f, FUR2).rot(-26 - i * 2, 0, 0);
        }

        // ---------------------------------------------------------------- neck, head, maw, mane
        m.part("neck", "torso", 0, -2, -8, -2.5f, -3, -6, 5, 6, 7, INK).pattern(Pattern.DIAG, FUR, 1).rot(14, 0, 0);
        m.part("head", "neck", 0, 0, -13, -3.5f, -6, -6, 7, 8, 7, INK).pattern(Pattern.DIAG, FUR, 1)
                .decor(Face.FRONT, 0, 2, 3, 2, PAPER_DK).decor(Face.FRONT, 4, 2, 3, 2, PAPER_DK)
                .decor(Face.FRONT, 1, 2, 2, 2, OOZE).decor(Face.FRONT, 4, 2, 2, 2, OOZE)
                .decorGlow(Face.FRONT, 1, 3, 1, 1, EYE).decorGlow(Face.FRONT, 5, 3, 1, 1, EYE);
        m.part("snout", "head", 0, 0, -13, -2.6f, -1, -12, 5.2f, 3, 6, INK).pattern(Pattern.DIAG, FUR2, 1)
                .decor(Face.BOTTOM, 0, 0, 1, 6, PAPER).decor(Face.BOTTOM, 2, 0, 1, 6, PAPER).decor(Face.BOTTOM, 4, 0, 1, 6, PAPER);
        m.part("jaw", "head", 0, 2, -14, -2.4f, 0, -9, 4.8f, 2.2f, 9, OOZE)
                .decor(Face.TOP, 0, 0, 1, 8, PAPER).decor(Face.TOP, 2, 1, 1, 7, PAPER).decor(Face.TOP, 4, 0, 1, 8, PAPER);
        m.part("tongue", "jaw", 0, 2.2f, -13, -1, -0.4f, -5, 2, 0.8f, 6, 0x4A1A24);
        m.part("drip", "jaw", 0, 2, -22, -0.5f, 0, -0.5f, 1, 8, 1, OOZE);
        for (int i = 0; i < 7; i++) {
            float a = -60 + i * 20;
            m.part("mane" + i, "neck", (float) Math.sin(Math.toRadians(a)) * 3, -4 + (float) -Math.abs(Math.cos(Math.toRadians(a))) * 1, -9, -0.6f, -6, -0.6f, 1.2f, 6, 1.2f, FUR2).rot(-10, 0, a * 0.8f);
        }
        m.part("stalk", "head", -2, -6, -9, -0.4f, -7, -0.4f, 0.8f, 7, 0.8f, FUR2).rot(-12, 0, -8);
        m.part("flag", "stalk", -2, -13, -9, -3, -5, -0.3f, 6, 5, 0.6f, PAPER).rot(-12, 0, -8)
                .decor(Face.FRONT, 0, 0, 6, 1, INK).decor(Face.FRONT, 5, 0, 1, 5, INK).decor(Face.FRONT, 0, 4, 5, 1, INK).decor(Face.FRONT, 0, 1, 1, 3, INK)
                .decor(Face.FRONT, 2, 2, 3, 1, INK).decor(Face.FRONT, 2, 2, 1, 2, INK)
                .decor(Face.BACK, 0, 0, 6, 1, INK).decor(Face.BACK, 0, 0, 1, 5, INK).decor(Face.BACK, 1, 4, 5, 1, INK).decor(Face.BACK, 4, 1, 1, 3, INK);

        // ---------------------------------------------------------------- forelimbs
        for (int s = -1; s <= 1; s += 2) {
            String k = s < 0 ? "R" : "L";
            float x = s * 5.5f;
            m.part("arm" + k, "chest", x, -1, -3, -1.3f, 0, -1.3f, 2.6f, 11, 2.6f, INK).pattern(Pattern.DIAG, FUR, 1).rot(-20, 0, -s * 5);
            m.part("fore" + k, "arm" + k, x, 10, -3, -1.1f, 0, -1.1f, 2.2f, 11, 2.2f, INK).pattern(Pattern.DIAG, FUR2, 1).rot(38, 0, 0);
            m.part("hand" + k, "fore" + k, x, 21, -3, -2, -0.5f, -3.5f, 4, 2, 5, INK);
            for (int i = -1; i <= 1; i++)
                m.part("claw" + k + (i + 1), "hand" + k, x + i * 1.3f, 22, -6.5f, -0.35f, -0.4f, -3.5f, 0.7f, 0.8f, 3.5f, PAPER).rot(0, i * 8, 0);
        }

        // ---------------------------------------------------------------- hind legs
        for (int s = -1; s <= 1; s += 2) {
            String k = s < 0 ? "R" : "L";
            float x = s * 4f;
            m.part("thigh" + k, "rump", x, 4, 12, -1.8f, 0, -1.8f, 3.6f, 10, 3.6f, INK).pattern(Pattern.DIAG, FUR, 1).rot(-38, 0, -s * 4);
            m.part("shin" + k, "thigh" + k, x, 14, 12, -1.4f, 0, -1.4f, 2.8f, 10, 2.8f, INK).pattern(Pattern.DIAG, FUR2, 1).rot(62, 0, 0);
            m.part("foot" + k, "shin" + k, x, 23, 12, -2, -1, -5, 4, 2, 6, INK).rot(-24, 0, 0);
            for (int i = -1; i <= 1; i++)
                m.part("toe" + k + (i + 1), "foot" + k, x + i * 1.3f, 23.5f, 7, -0.35f, -0.4f, -3, 0.7f, 0.8f, 3f, PAPER).rot(0, i * 9, 0);
        }

        // ---------------------------------------------------------------- wing blade (left side only, like the drawing)
        m.part("wingU", "chest", 3.5f, -6, -3, -0.8f, -14, -0.8f, 1.6f, 14, 1.6f, INK).rot(-30, 0, 28);
        m.part("wingB", "wingU", 3.5f, -20, -3, -0.5f, -17, -4, 1, 17, 8, INK).pattern(Pattern.STRIPE_H, FUR2, 2).rot(105, 0, 0)
                .decor(Face.RIGHT, 0, 0, 1, 17, PAPER_DK).decor(Face.LEFT, 7, 0, 1, 17, PAPER_DK).decor(Face.FRONT, 0, 4, 1, 8, PAPER);
        m.part("wingT", "wingB", 3.5f, -37, -3, -0.5f, -6, -3, 1, 6, 6, INK).rot(40, 0, 0);

        // ---------------------------------------------------------------- tail
        String par = "rump";
        float z = 15;
        for (int i = 0; i < 6; i++) {
            float w = Math.max(1.4f, 4.2f - i * 0.5f);
            m.part("tail" + i, par, 0, 3.5f + i * 0.4f, z, -w / 2, -w / 2, 0, w, w, 6, i % 2 == 0 ? INK : FUR).rot(-6, 0, 0);
            par = "tail" + i;
            z += 6;
        }
        m.part("tailBlade", par, 0, 6, z, -0.5f, -5, 0, 1, 5, 7, INK).decor(Face.RIGHT, 0, 0, 1, 5, PAPER_DK);

        m.animator(InfectedZipSpec::animate);
        return m;
    }

    private static float sgn(String k) { return k.equals("R") ? -1f : 1f; }

    private static void animate(ModelParts m, AnimCtx c) {
        float a = c.age, t = c.t, w = c.walk(), ls = c.limbSwing;

        // ---------------- locomotion / idle (bounding quadruped gait)
        for (String k : new String[] {"R", "L"}) {
            float ph = k.equals("R") ? 0 : 3.14159f;
            float sw = Anim.sinr(ls * 0.6f + ph) * w;
            float sh = Anim.sinr(ls * 0.6f + ph + 1.6f) * w;
            m.addRot("arm" + k, sw * 34, 0, 0);
            m.addRot("fore" + k, Math.max(0, -sw) * 35, 0, 0);
            m.addRot("thigh" + k, -sh * 32, 0, 0);
            m.addRot("shin" + k, Math.max(0, sh) * 34, 0, 0);
            m.addRot("claw" + k + "0", Anim.sinr(a * 0.2f + ph) * 5, 0, 0);
        }
        for (int i = 0; i < 6; i++)
            m.addRot("tail" + i, Anim.sinr(a * 0.09f - i * 0.6f) * 3, Anim.sinr(a * 0.11f - i * 0.7f) * (7 + i) + Anim.sinr(ls * 0.6f - i * 0.5f) * 8 * w, 0);
        for (int i = 0; i < 7; i++) m.addRot("mane" + i, Anim.sinr(a * 0.12f + i) * 5, 0, 0);
        for (int i = 0; i < 8; i++) m.addRot("spine" + i, Anim.sinr(a * 0.1f + i * 0.5f) * 3 + w * 5, 0, 0);
        m.addRot("torso", Anim.sinr(a * 0.07f) * 1.5f + Anim.sinr(ls * 1.2f) * 3 * w, Anim.sinr(ls * 0.6f) * 4 * w, 0);
        m.addRot("neck", Anim.sinr(a * 0.06f + 1f) * 3, Math.max(-40, Math.min(40, c.headYaw)) * 0.7f, 0);
        m.addRot("jaw", 8 + Anim.sinr(a * 0.13f) * 6, 0, 0);
        m.addRot("drip", Anim.sinr(a * 0.17f) * 6, 0, Anim.sinr(a * 0.14f) * 7);
        m.addRot("stalk", Anim.sinr(a * 0.1f) * 6, 0, Anim.sinr(a * 0.08f) * 6);
        m.addRot("flag", Anim.sinr(a * 0.2f) * 10, 0, 0);
        m.addRot("wingU", Anim.sinr(a * 0.05f) * 5 + w * 8, 0, Anim.sinr(a * 0.06f) * 4);
        m.addRot("wingB", Anim.sinr(a * 0.07f + 1) * 8, 0, 0);
        m.addRot("wingT", Anim.sinr(a * 0.09f + 2) * 10, 0, 0);
        m.move("torso", 0, Anim.sinr(ls * 1.2f) * 0.9f * w, 0);

        // ---------------- abilities
        if (c.is("maul")) {
            float rear = Anim.curve(t, 0, 0, 12, 1, 15, 0, 34, 0);
            float lunge = Anim.curve(t, 0, 0, 12, 0, 15, 1, 24, 0.5f, 34, 0);
            m.addRot("torso", -8 * rear + 12 * lunge, 0, 0);
            m.addRot("neck", -22 * rear + 30 * lunge, 0, 0);
            m.addRot("jaw", 52 * rear + (t < 14 ? 0 : Anim.curve(t, 14, 0, 16, -26, 24, 0)) - 6 * lunge, 0, 0);
            m.addRot("armR", -30 * lunge, 0, 0);
            m.addRot("armL", -30 * lunge, 0, 0);
            m.addRot("thighR", 16 * lunge, 0, 0);
            m.addRot("thighL", 16 * lunge, 0, 0);
        } else if (c.is("claw")) {
            float up = Anim.curve(t, 0, 0, 10, 1, 24, 1, 34, 0);
            m.addRot("torso", -38 * up, Anim.curve(t, 0, 0, 12, 14, 20, -14, 34, 0), 0);
            m.addRot("neck", 16 * up, 0, 0);
            m.addRot("jaw", 20 * up, 0, 0);
            m.addRot("thighR", 24 * up, 0, 0);
            m.addRot("thighL", 24 * up, 0, 0);
            m.addRot("shinR", -14 * up, 0, 0);
            m.addRot("shinL", -14 * up, 0, 0);
            float r = Anim.curve(t, 0, 0, 5, -100, 12, 60, 16, 0, 34, 0);
            float l = Anim.curve(t, 0, 0, 13, -100, 20, 60, 24, 0, 34, 0);
            m.addRot("armR", r, 0, 0);
            m.addRot("foreR", -r * 0.3f, 0, 0);
            m.addRot("armL", l, 0, 0);
            m.addRot("foreL", -l * 0.3f, 0, 0);
        } else if (c.is("tail_sweep")) {
            float st = Anim.curve(t, 0, 0, 10, 1, 28, 1, 40, 0);
            m.addRot("root", 0, Anim.linear(t, 0, 0, 10, 0, 26, 300, 99, 300) * 0 + Anim.linear(t, 0, 0, 10, 0, 26, -330, 99, -330), 0);
            m.addRot("torso", 6 * st, 0, 0);
            m.addRot("neck", 10 * st, 0, 0);
            for (int i = 0; i < 6; i++) m.addRot("tail" + i, 0, 18 * st * (1 - i * 0.08f), 0);
            m.addRot("tailBlade", 0, 20 * st, 0);
            for (String k : new String[] {"R", "L"}) { m.addRot("arm" + k, -20 * st, 0, 0); m.addRot("wingU", 0, 0, 0); }
        } else if (c.is("wing_slash")) {
            float up = Anim.curve(t, 0, 0, 14, 1, 17, 0, 36, 0);
            float down = Anim.curve(t, 0, 0, 14, 0, 18, 1, 28, 0.8f, 36, 0);
            m.addRot("torso", -14 * up + 16 * down, Anim.curve(t, 0, 0, 14, -10, 18, 12, 36, 0), 0);
            m.addRot("neck", -8 * up + 12 * down, 0, 0);
            m.addRot("wingU", -40 * up + 100 * down, 0, 12 * up - 40 * down);
            m.addRot("wingB", -30 * up + 30 * down, 0, 0);
            m.addRot("wingT", -20 * up + 30 * down, 0, 0);
            m.addRot("jaw", 25 * up, 0, 0);
        } else if (c.is("pounce")) {
            float crouch = Anim.curve(t, 0, 0, 13, 1, 14, 0.9f, 18, 0, 44, 0);
            float air = Anim.curve(t, 0, 0, 14, 0, 18, 1, 28, 1, 34, 0, 44, 0);
            m.move("torso", 0, 6 * crouch, 0);
            m.addRot("torso", 12 * crouch - 14 * air, 0, 0);
            m.addRot("neck", -8 * crouch + 6 * air, 0, 0);
            m.addRot("jaw", 40 * air, 0, 0);
            for (String k : new String[] {"R", "L"}) {
                m.addRot("arm" + k, 24 * crouch - 95 * air, 0, 0);
                m.addRot("thigh" + k, -30 * crouch + 36 * air, 0, 0);
                m.addRot("shin" + k, 50 * crouch - 30 * air, 0, 0);
            }
            for (int i = 0; i < 6; i++) m.addRot("tail" + i, -6 * air, 0, 0);
        } else if (c.is("scribble")) {
            float up = Anim.curve(t, 0, 0, 14, 1, 16, 1, 18, 0, 44, 0);
            float slam = Anim.curve(t, 0, 0, 14, 0, 18, 1, 34, 1, 44, 0);
            m.addRot("torso", -28 * up + 14 * slam, 0, 0);
            m.addRot("neck", -10 * up + 14 * slam, 0, 0);
            for (String k : new String[] {"R", "L"}) { m.addRot("arm" + k, -70 * up + 120 * slam, 0, 0); m.addRot("thigh" + k, 18 * up, 0, 0); }
            m.addRot("wingU", -30 * up, 0, 10 * up);
        } else if (c.is("ink_spit")) {
            float rear = Anim.curve(t, 0, 0, 14, 1, 16, 0.4f, 26, 0, 40, 0);
            m.addRot("torso", -16 * rear, 0, 0);
            m.addRot("neck", -34 * rear, 0, 0);
            m.addRot("jaw", Anim.curve(t, 0, 0, 14, 20, 17, 60, 28, 60, 34, 0, 40, 0), 0, 0);
            m.addRot("drip", -20 * rear, 0, 0);
        } else if (c.is("roar")) {
            float up = Anim.curve(t, 0, 0, 12, 1, 34, 1, 44, 0);
            float sh = t > 12 && t < 36 ? 1 : 0;
            m.addRot("torso", -40 * up, Anim.sinr(a * 2.6f) * 2 * sh, 0);
            m.addRot("neck", -30 * up + Anim.sinr(a * 3f) * 3 * sh, Anim.sinr(a * 3.3f) * 5 * sh, 0);
            m.addRot("jaw", 70 * up, 0, 0);
            for (String k : new String[] {"R", "L"}) { m.addRot("arm" + k, -40 * up, 0, -sgn(k) * 20 * up); m.addRot("thigh" + k, 24 * up, 0, 0); }
            m.addRot("wingU", -30 * up, 0, 24 * up);
            for (int i = 0; i < 7; i++) m.addRot("mane" + i, -18 * up, 0, 0);
        } else if (c.is("frenzy")) {
            float run = Anim.sinr(a * 1.1f);
            m.addRot("torso", 14, Anim.sinr(a * 0.9f) * 8, 0);
            m.addRot("neck", 14, 0, 0);
            m.addRot("jaw", 40 + Anim.sinr(a * 1.4f) * 18, 0, 0);
            m.addRot("armR", -60 + run * 40, 0, 0);
            m.addRot("armL", -60 - run * 40, 0, 0);
            m.addRot("thighR", -run * 36, 0, 0);
            m.addRot("thighL", run * 36, 0, 0);
            m.addRot("wingU", 30, 0, 18);
            for (int i = 0; i < 6; i++) m.addRot("tail" + i, 0, Anim.sinr(a * 0.8f - i * 0.8f) * 18, 0);
        }

        // ---------------- death: collapses onto its side
        if (c.death > 0) {
            float d = Anim.easeOut(c.death);
            m.addRot("root", 0, 0, 86 * d);
            m.move("root", 0, -5 * d, 0);
            for (String k : new String[] {"R", "L"}) {
                m.addRot("arm" + k, -28 * d, 0, 0);
                m.addRot("thigh" + k, -26 * d, 0, 0);
            }
            m.addRot("neck", 14 * d, 0, 0);
            m.addRot("jaw", 40 * d, 0, 0);
            m.addRot("wingU", -30 * d, 0, 30 * d);
        }
    }
}
