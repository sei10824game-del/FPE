package com.fpe.client.spec;

import com.fpe.client.model.Anim;
import com.fpe.client.model.AnimCtx;
import com.fpe.client.model.ModelParts;
import com.fpe.client.model.ModelSpec;
import com.fpe.client.model.ModelSpec.Face;
import com.fpe.client.model.ModelSpec.Pattern;

/**
 * Infected Bloomie (Basics in Survival AU): hunched spindly pale body, huge round glowing eyes, black drooling jaw with a long ooze strand,
 * long clawed forelimbs, two mantis-scythe blades over the back, long sprawling legs. Animation keyed to entity/characters/InfectedBloomie.
 */
public final class InfectedBloomieSpec {
    private InfectedBloomieSpec() {}

    static final int BONE = 0xC4C9D8, BONE_DK = 0x8E96AE, BONE_LT = 0xE6E9F2, INK = 0x14111C, INK2 = 0x2B2638, EYE = 0xF2F8FF, EDGE = 0xD8DCEA,
            TOOTH = 0xE8E6DC, OOZE = 0x0B0910, VEIN = 0x5E6AA0;

    public static final ModelSpec SPEC = com.fpe.client.model.BbModel.load("infected_bloomie", 1.0f);
    static final ModelSpec PROC = build();

    private static ModelSpec build() {
        ModelSpec m = new ModelSpec("infected_bloomie").shadow(1.0f);
        m.group("root", null, 0, 24, 0);
        m.group("hips", "root", 0, -1, 0);

        // ---------------------------------------------------------------- legs
        for (int s = -1; s <= 1; s += 2) {
            String k = s < 0 ? "R" : "L";
            float x = s * 2.8f;
            m.part("thigh" + k, "hips", x, -1, 0, -1.3f, 0, -1.3f, 2.6f, 12.5f, 2.6f, BONE).rot(-16, 0, -s * 9).grain(0.05f)
                    .decor(Face.FRONT, 0, 2, 2, 1, BONE_DK).decor(Face.FRONT, 0, 6, 2, 1, BONE_DK);
            m.part("shin" + k, "thigh" + k, x, 11.5f, 0, -1, 0, -1, 2, 12.5f, 2, BONE_DK).rot(32, 0, s * 9)
                    .decor(Face.FRONT, 0, 3, 1, 5, VEIN);
            m.part("foot" + k, "shin" + k, x, 23.2f, 0, -1.5f, -0.8f, -2.5f, 3, 1.6f, 4, INK2).rot(-18, 0, 0);
            for (int i = -1; i <= 1; i++)
                m.part("toe" + k + (i + 1), "foot" + k, x + i * 1.1f, 23.8f, -2.5f, -0.3f, -0.4f, -3f, 0.6f, 0.6f, 3.2f, BONE_LT).rot(8, i * 14, 0);
        }

        // ---------------------------------------------------------------- hunched chest (tilted forward in animator default)
        m.part("chest", "hips", 0, -1, 0, -3.5f, -15, -2.5f, 7, 15, 5, BONE).rot(50, 0, 0).grain(0.05f)
                .decor(Face.FRONT, 1, 2, 5, 1, BONE_DK).decor(Face.FRONT, 1, 4, 5, 1, BONE_DK).decor(Face.FRONT, 1, 6, 5, 1, BONE_DK)
                .decor(Face.FRONT, 1, 8, 5, 1, BONE_DK).decor(Face.FRONT, 2, 11, 3, 1, BONE_DK)
                .decor(Face.BACK, 3, 0, 1, 15, BONE_DK).decor(Face.RIGHT, 1, 3, 3, 2, OOZE).decor(Face.LEFT, 1, 8, 2, 3, OOZE)
                .decor(Face.FRONT, 0, 12, 2, 3, VEIN).decor(Face.FRONT, 5, 9, 1, 4, VEIN);
        for (int i = 0; i < 4; i++)
            m.part("spine" + i, "chest", 0, -14 + i * 3.6f, 2.5f, -0.6f, -3, 0, 1.2f, 3, 2.6f, INK2).rot(-32, 0, 0);

        // ---------------------------------------------------------------- head, horns, jaw, ooze strand
        m.part("head", "chest", 0, -16.5f, -0.5f, -3.5f, -8, -3.5f, 7, 8, 7, BONE_LT).rot(-14, 0, 0).grain(0.04f)
                .decor(Face.FRONT, 0, 1, 3, 4, INK).decor(Face.FRONT, 4, 1, 3, 4, INK)
                .decorGlow(Face.FRONT, 1, 2, 1, 2, EYE).decorGlow(Face.FRONT, 5, 2, 1, 2, EYE)
                .decor(Face.FRONT, 3, 5, 1, 3, INK2).decor(Face.TOP, 2, 2, 3, 3, BONE_DK)
                .decor(Face.FRONT, 0, 6, 7, 2, OOZE);
        m.part("hornC", "head", 0, -8, -1, -1, -6, -1, 2, 6, 2, BONE_LT).rot(-26, 0, 0);
        for (int s = -1; s <= 1; s += 2) {
            String k = s < 0 ? "R" : "L";
            m.part("horn" + k, "head", s * 2.6f, -8, 0, -0.7f, -5, -0.7f, 1.4f, 5, 1.4f, BONE).rot(-18, 0, s * 26);
            m.part("brow" + k, "head", s * 2, -5, -3.5f, -1.6f, -0.5f, -0.5f, 3.2f, 1, 1, INK2).rot(0, 0, -s * 14);
        }
        m.part("jaw", "head", 0, -2.2f, -3f, -2.6f, 0, -0.5f, 5.2f, 10, 4.2f, OOZE).grain(0.03f)
                .decor(Face.FRONT, 0, 0, 1, 2, TOOTH).decor(Face.FRONT, 2, 0, 1, 3, TOOTH).decor(Face.FRONT, 4, 0, 1, 2, TOOTH)
                .decor(Face.FRONT, 1, 3, 1, 1, TOOTH).decor(Face.FRONT, 3, 3, 1, 1, TOOTH)
                .decor(Face.RIGHT, 1, 2, 2, 1, TOOTH).decor(Face.LEFT, 1, 4, 2, 1, TOOTH);
        m.part("drip", "jaw", 0, 8, -0.5f, -0.6f, 0, -0.6f, 1.2f, 14, 1.2f, OOZE);
        m.part("drip2", "jaw", 1.4f, 7, -1.5f, -0.4f, 0, -0.4f, 0.8f, 7, 0.8f, OOZE);

        // ---------------------------------------------------------------- long clawed forelimbs
        for (int s = -1; s <= 1; s += 2) {
            String k = s < 0 ? "R" : "L";
            float x = s * 5f;
            m.part("arm" + k, "chest", x, -14.5f, 0, -1, 0, -1, 2, 13, 2, BONE).rot(-48, 0, -s * 6).decor(Face.FRONT, 0, 4, 1, 3, VEIN);
            m.part("fore" + k, "arm" + k, x, -1.5f, 0, -0.8f, 0, -0.8f, 1.6f, 13, 1.6f, BONE_DK).rot(-12, 0, 0);
            m.part("hand" + k, "fore" + k, x, 11.5f, 0, -1.2f, 0, -1, 2.4f, 2.5f, 2, INK2);
            for (int i = -1; i <= 1; i++)
                m.part("claw" + k + (i + 1), "hand" + k, x + i * 0.8f, 14f, -0.5f, -0.3f, 0, -0.3f, 0.6f, 5, 0.6f, BONE_LT).rot(-14, 0, i * 8);
        }

        // ---------------------------------------------------------------- scythe blades over the back
        for (int s = -1; s <= 1; s += 2) {
            String k = s < 0 ? "R" : "L";
            float x = s * 3f;
            m.part("scy" + k, "chest", x, -14, 2.5f, -0.9f, -17, -0.9f, 1.8f, 17, 1.8f, INK).rot(-62, 0, s * 22).grain(0.03f)
                    .decor(Face.FRONT, 0, 3, 1, 5, INK2).decor(Face.FRONT, 0, 11, 1, 3, INK2);
            m.part("blade" + k, "scy" + k, x, -31, 2.5f, -0.6f, -20, -3, 1.2f, 20, 6, INK).rot(115, 0, 0).grain(0.03f)
                    .decor(Face.RIGHT, 0, 0, 1, 20, EDGE).decor(Face.LEFT, 5, 0, 1, 20, EDGE).decor(Face.FRONT, 0, 14, 1, 5, OOZE);
            for (int i = 0; i < 4; i++)
                m.part("tooth" + k + i, "blade" + k, x, -33 - i * 4, 0.5f, -0.4f, -1.6f, 0, 0.8f, 1.6f, 2.4f, EDGE).rot(40, 0, 0);
            m.part("tip" + k, "blade" + k, x, -51, 0, -0.4f, -2.5f, -1, 0.8f, 2.5f, 2, EYE).glow();
        }

        m.animator(InfectedBloomieSpec::animate);
        return m;
    }

    private static float sgn(String k) { return k.equals("R") ? -1f : 1f; }

    private static void animate(ModelParts m, AnimCtx c) {
        float a = c.age, t = c.t, w = c.walk(), ls = c.limbSwing;
        boolean idle = c.idle();

        // ---------------- locomotion / idle
        for (String k : new String[] {"R", "L"}) {
            float s = sgn(k), ph = k.equals("R") ? 0 : 3.14159f;
            float sw = Anim.sinr(ls * 0.55f + ph) * w;
            m.addRot("thigh" + k, sw * 38, 0, 0);
            m.addRot("shin" + k, Math.max(0, -sw) * 40 + Math.abs(sw) * 8, 0, 0);
            m.addRot("arm" + k, -sw * 30 + Anim.sinr(a * 0.07f + ph) * 3, 0, 0);
            m.addRot("fore" + k, Anim.sinr(a * 0.09f + ph) * 4, 0, 0);
            m.addRot("claw" + k + "0", Anim.sinr(a * 0.2f + ph) * 6, 0, 0);
            m.addRot("claw" + k + "2", Anim.sinr(a * 0.2f + ph + 1) * 6, 0, 0);
            m.addRot("scy" + k, Anim.sinr(a * 0.05f + ph) * 5 + sw * 6, 0, s * Anim.sinr(a * 0.06f) * 4);
            m.addRot("blade" + k, Anim.sinr(a * 0.07f + ph + 1f) * 8, 0, 0);
        }
        m.addRot("chest", Anim.sinr(a * 0.08f) * 2.5f + w * 4, Anim.sinr(ls * 0.55f) * 6 * w, 0);
        m.addRot("head", Anim.sinr(a * 0.06f + 1f) * 3 - w * 4, Math.max(-35, Math.min(35, c.headYaw)) * 0.6f, 0);
        m.addRot("jaw", Anim.sinr(a * 0.11f) * 4, 0, 0);
        m.addRot("drip", Anim.sinr(a * 0.17f) * 5, 0, Anim.sinr(a * 0.13f) * 6);
        m.addRot("drip2", Anim.sinr(a * 0.2f + 2f) * 6, 0, 0);
        m.move("hips", 0, Anim.sinr(ls * 1.1f) * 0.7f * w + Anim.sinr(a * 0.08f) * 0.3f, 0);

        // ---------------- abilities
        if (c.is("cross")) {
            float lean = Anim.curve(t, 0, 0, 14, -16, 18, 28, 34, 0);
            m.addRot("chest", lean, Anim.curve(t, 0, 0, 14, 10, 18, -12, 34, 0), 0);
            m.addRot("head", Anim.curve(t, 0, 0, 14, -20, 18, 14, 34, 0), 0, 0);
            for (String k : new String[] {"R", "L"}) {
                float s = sgn(k);
                m.addRot("scy" + k, Anim.curve(t, 0, 0, 14, -42, 16, 88, 22, 76, 34, 0), 0, s * Anim.curve(t, 0, 0, 14, 8, 18, -62, 22, -50, 34, 0));
                m.addRot("blade" + k, Anim.curve(t, 0, 0, 14, -34, 18, 20, 34, 0), 0, 0);
                m.addRot("arm" + k, Anim.curve(t, 0, 0, 14, -20, 18, 25, 34, 0), 0, 0);
            }
        } else if (c.is("whirl") || c.is("blade_storm")) {
            boolean big = c.is("blade_storm");
            float end = big ? 46 : 30, st = 10;
            float ext = Anim.curve(t, 0, 0, st, 1, end, 1, end + 12, 0);
            m.move("hips", 0, 5 * Anim.curve(t, 0, 0, st, 1, end, 0.4f, end + 12, 0), 0);
            m.addRot("chest", 20 * ext, 0, 0);
            m.addRot("root", 0, Anim.linear(t, 0, 0, st, 0, end, big ? -1080 : -720, 99, big ? -1080 : -720), 0);
            for (String k : new String[] {"R", "L"}) {
                float s = sgn(k);
                m.addRot("scy" + k, 62 * ext, 0, s * 72 * ext);
                m.addRot("blade" + k, -40 * ext, 0, 0);
                m.addRot("arm" + k, 0, 0, s * -70 * ext);
                m.addRot("fore" + k, -20 * ext, 0, 0);
            }
            m.addRot("head", -20 * ext, 0, 0);
        } else if (c.is("impale")) {
            float draw = Anim.curve(t, 0, 0, 16, 1, 18, 0.2f, 22, -1, 30, 0, 38, 0);
            float thrust = Anim.curve(t, 0, 0, 14, 0, 17, 1, 24, 1, 34, 0);
            m.addRot("chest", Anim.curve(t, 0, 0, 14, -14, 17, 24, 26, 20, 38, 0), Anim.curve(t, 0, 0, 14, 22, 17, -10, 38, 0), 0);
            m.addRot("head", Anim.curve(t, 0, 0, 14, -22, 17, 12, 38, 0), 0, 0);
            m.addRot("scyR", -40 * draw + 112 * thrust, 0, 12 * thrust);
            m.addRot("bladeR", -34 * draw - 100 * thrust, 0, 0);
            m.addRot("scyL", -16 * draw, 0, 0);
            m.addRot("thighR", -18 * thrust, 0, 0);
            m.addRot("thighL", 14 * thrust, 0, 0);
        } else if (c.is("pounce")) {
            float crouch = Anim.curve(t, 0, 0, 14, 1, 16, 0.8f, 20, 0, 40, 0, 46, 0);
            float air = Anim.curve(t, 0, 0, 16, 0, 20, 1, 30, 1, 36, 0, 46, 0);
            m.move("hips", 0, 7 * crouch, 0);
            m.addRot("chest", 14 * crouch - 12 * air, 0, 0);
            m.addRot("head", -10 * crouch, 0, 0);
            for (String k : new String[] {"R", "L"}) {
                float s = sgn(k);
                m.addRot("thigh" + k, -42 * crouch + 25 * air, 0, 0);
                m.addRot("shin" + k, 55 * crouch - 25 * air, 0, 0);
                m.addRot("arm" + k, 25 * crouch - 120 * air, 0, 0);
                m.addRot("fore" + k, -18 * air, 0, 0);
                m.addRot("scy" + k, -24 * crouch + 78 * air, 0, s * -12 * air);
                m.addRot("blade" + k, -50 * air, 0, 0);
            }
        } else if (c.is("rake")) {
            m.addRot("chest", 12, Anim.curve(t, 0, 0, 8, 14, 14, -14, 20, 14, 30, 0), 0);
            m.addRot("head", 10, 0, 0);
            float r = Anim.curve(t, 0, 0, 3, -85, 8, 40, 11, 0, 15, -85, 20, 40, 24, 0, 30, 0);
            float l = Anim.curve(t, 0, 0, 9, -85, 14, 40, 18, 0, 30, 0);
            m.addRot("armR", r, 0, 0);
            m.addRot("foreR", r * 0.35f, 0, 0);
            m.addRot("armL", l, 0, 0);
            m.addRot("foreL", l * 0.35f, 0, 0);
            m.addRot("scyR", 20, 0, 0);
            m.addRot("scyL", 20, 0, 0);
        } else if (c.is("spit")) {
            float rear = Anim.curve(t, 0, 0, 14, 1, 16, 0.5f, 18, -0.4f, 26, 0, 40, 0);
            m.addRot("chest", -30 * rear + (t > 16 && t < 30 ? 8 : 0), 0, 0);
            m.addRot("head", -32 * rear, 0, 0);
            m.addRot("jaw", -(Anim.curve(t, 0, 0, 14, 40, 17, 62, 26, 62, 32, 0, 40, 0)), 0, 0);
            m.addRot("drip", -20 * rear, 0, 0);
            for (String k : new String[] {"R", "L"}) { m.addRot("scy" + k, -22 * rear, 0, 0); m.addRot("arm" + k, -16 * rear, 0, 0); }
        } else if (c.is("screech")) {
            float up = Anim.curve(t, 0, 0, 12, 1, 36, 1, 46, 0);
            float sh = t > 12 && t < 38 ? 1 : 0;
            m.addRot("chest", -28 * up, Anim.sinr(a * 2.5f) * 3 * sh, Anim.sinr(a * 2.8f) * 2 * sh);
            m.addRot("head", -48 * up + Anim.sinr(a * 3f) * 4 * sh, Anim.sinr(a * 3.3f) * 6 * sh, 0);
            m.addRot("jaw", -80 * up, 0, 0);
            m.move("hips", 0, Anim.sinr(a * 3f) * 0.5f * sh, 0);
            for (String k : new String[] {"R", "L"}) {
                float s = sgn(k);
                m.addRot("scy" + k, -30 * up, 0, s * 38 * up);
                m.addRot("blade" + k, -55 * up, 0, 0);
                m.addRot("arm" + k, -50 * up, 0, -s * 30 * up);
            }
        } else if (c.is("spikes")) {
            float up = Anim.curve(t, 0, 0, 14, 1, 16, 1, 18, 0, 32, 0, 44, 0);
            float slam = Anim.curve(t, 0, 0, 14, 0, 18, 1, 32, 1, 44, 0);
            m.addRot("chest", -18 * up + 38 * slam, 0, 0);
            m.addRot("head", -16 * up + 14 * slam, 0, 0);
            for (String k : new String[] {"R", "L"}) {
                float s = sgn(k);
                m.addRot("arm" + k, -110 * up + 150 * slam, 0, 0);
                m.addRot("fore" + k, -15 * up, 0, 0);
                m.addRot("scy" + k, -34 * up + 50 * slam, 0, s * 10 * up);
                m.addRot("blade" + k, -40 * up, 0, 0);
            }
        } else if (c.is("bite")) {
            float rear = Anim.curve(t, 0, 0, 12, 1, 14, 0, 32, 0);
            float lunge = Anim.curve(t, 0, 0, 12, 0, 15, 1, 22, 0.6f, 32, 0);
            m.addRot("chest", -18 * rear + 34 * lunge, 0, 0);
            m.addRot("head", -22 * rear + 30 * lunge, 0, 0);
            m.addRot("jaw", -58 * rear + 40 * lunge * (t > 14 ? Anim.curve(t, 14, 1, 17, -0.5f, 32, 0) : 0), 0, 0);
            m.addRot("armR", -40 * lunge, 0, 0);
            m.addRot("armL", -40 * lunge, 0, 0);
            m.addRot("thighR", -20 * lunge, 0, 0);
            m.addRot("thighL", 16 * lunge, 0, 0);
        }

        // ---------------- death: collapses sideways, limbs curl
        if (c.death > 0) {
            float d = Anim.easeOut(c.death);
            m.addRot("root", 0, 0, 88 * d);
            m.move("root", 0, -6 * d, 0);
            for (String k : new String[] {"R", "L"}) {
                m.addRot("thigh" + k, -38 * d, 0, 0);
                m.addRot("shin" + k, 60 * d, 0, 0);
                m.addRot("arm" + k, 30 * d, 0, 0);
                m.addRot("scy" + k, -30 * d, 0, 0);
            }
            m.addRot("head", 20 * d, 0, 0);
            m.addRot("jaw", -40 * d, 0, 0);
        }
    }
}
