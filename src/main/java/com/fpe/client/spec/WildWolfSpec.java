package com.fpe.client.spec;

import com.fpe.client.model.Anim;
import com.fpe.client.model.AnimCtx;
import com.fpe.client.model.ModelParts;
import com.fpe.client.model.ModelSpec;
import com.fpe.client.model.ModelSpec.Face;
import com.fpe.client.model.ModelSpec.Pattern;

/**
 * Nameless Werewolf (original design): hulking hunched wolf-man, shaggy slate-grey fur, black eyes, big shoulders, long clawed arms,
 * digitigrade legs, bushy tail, heavy iron pickaxe in the right hand. About 3 blocks tall. Keyed to entity/characters/WildWolf.
 */
public final class WildWolfSpec {
    private WildWolfSpec() {}

    static final int FUR = 0x4A4C55, FUR_D = 0x34363E, FUR_L = 0x6A6D78, BELLY = 0x8A8C94, SKIN = 0x2A2528, TOOTH = 0xEDE9DC, EYE = 0x050506,
            CLAW = 0xD8D4C6, WOOD = 0x6B4A2C, WOOD_D = 0x4E3520, IRON = 0x8C9097, IRON_D = 0x5C6068, RAG = 0x5A4A3A;

    public static final ModelSpec SPEC = build();

    private static ModelSpec build() {
        ModelSpec m = new ModelSpec("wild_wolf").shadow(1.1f);
        m.group("root", null, 0, 24, 0);
        m.group("hips", "root", 0, 3, 0);

        // digitigrade legs
        for (int s = -1; s <= 1; s += 2) {
            String k = s < 0 ? "R" : "L";
            float x = 4f * s;
            m.part("thigh" + k, "hips", x, 3, 0, -2.4f, 0, -2.4f, 4.8f, 11, 4.8f, FUR).pattern(Pattern.STRIPE_V, FUR_D, 2).grain(0.07f).rot(-22, 0, -s * 3);
            m.part("shin" + k, "thigh" + k, x, 14, 0, -1.9f, 0, -1.9f, 3.8f, 11, 3.8f, FUR_D).grain(0.07f).rot(40, 0, 0);
            m.part("foot" + k, "shin" + k, x, 25, 0, -2.2f, -1, -5.5f, 4.4f, 2, 6, SKIN).rot(-20, 0, 0);
            for (int i = -1; i <= 1; i++)
                m.part("toe" + k + (i + 1), "foot" + k, x + i * 1.4f, 25, -5.5f, -0.4f, -0.6f, -3, 0.8f, 0.9f, 3, CLAW).rot(0, i * 8, 0);
        }
        m.part("loin", "hips", 0, 3, 0, -5, -3, -3.5f, 10, 5, 7, RAG).decor(Face.FRONT, 0, 3, 10, 2, 0x3E3226);

        // hunched torso
        m.part("chest", "hips", 0, 3, 0, -6.5f, -17, -4.2f, 13, 17, 8.4f, FUR).pattern(Pattern.STRIPE_V, FUR_D, 3).grain(0.08f).rot(24, 0, 0)
                .decor(Face.FRONT, 3, 9, 7, 6, BELLY).decor(Face.FRONT, 4, 3, 5, 3, FUR_L);
        for (int s = -1; s <= 1; s += 2)
            m.part("shoulder" + (s < 0 ? "R" : "L"), "chest", s * 7.2f, -14, 0, -3.4f, -3.2f, -4.2f, 6.8f, 6.4f, 8.4f, FUR_L).grain(0.09f).rot(0, 0, -s * 8);
        m.part("mane", "chest", 0, -15, 3, -6, -3, 0, 12, 10, 4, FUR_L).grain(0.1f).rot(-14, 0, 0);
        for (int i = 0; i < 6; i++)
            m.part("spine" + i, "chest", -4.5f + i * 1.8f, -15.5f, 3.4f, -0.8f, -4, 0, 1.6f, 4 + (i % 3), 1.4f, FUR_D).rot(-30, 0, (i - 2.5f) * 6);

        // head: muzzle, jaw, ears, black eyes
        m.part("neck", "chest", 0, -16.5f, -1, -2.8f, -3, -3.4f, 5.6f, 4, 6, FUR).rot(-6, 0, 0);
        m.part("head", "neck", 0, -18.5f, -1.5f, -3.6f, -7.2f, -4.8f, 7.2f, 7.2f, 7.4f, FUR).grain(0.08f)
                .decor(Face.FRONT, 0, 2, 3, 2, EYE).decor(Face.FRONT, 4, 2, 3, 2, EYE).decor(Face.FRONT, 0, 1, 3, 1, FUR_D).decor(Face.FRONT, 4, 1, 3, 1, FUR_D);
        m.part("snout", "head", 0, -19, -4.8f, -2.2f, -3.4f, -5, 4.4f, 3.4f, 5.2f, FUR_L).decor(Face.FRONT, 1, 0, 2, 1, EYE)
                .decor(Face.BOTTOM, 0, 0, 1, 5, TOOTH).decor(Face.BOTTOM, 3, 0, 1, 5, TOOTH);
        m.part("jaw", "head", 0, -17.2f, -4.4f, -2, 0, -4.8f, 4, 1.6f, 5, FUR_D).rot(14, 0, 0)
                .decor(Face.TOP, 0, 0, 1, 5, TOOTH).decor(Face.TOP, 3, 0, 1, 5, TOOTH).decor(Face.TOP, 1, 2, 2, 1, TOOTH);
        for (int s = -1; s <= 1; s += 2) {
            m.part("ear" + (s < 0 ? "R" : "L"), "head", s * 2.8f, -25.6f, 0, -1.2f, -4.4f, -1, 2.4f, 4.4f, 2, FUR_D).rot(-8, 0, s * 18);
        }

        // arms (long, clawed); right arm carries the pickaxe
        for (int s = -1; s <= 1; s += 2) {
            String k = s < 0 ? "R" : "L";
            float x = 8.4f * s;
            m.part("arm" + k, "chest", x, -13, 0, -2.4f, 0, -2.4f, 4.8f, 13, 4.8f, FUR).pattern(Pattern.STRIPE_V, FUR_D, 2).grain(0.07f).rot(-18, 0, -s * 6);
            m.part("fore" + k, "arm" + k, x, 0, 0, -2.1f, 0, -2.1f, 4.2f, 13, 4.2f, FUR_D).grain(0.07f).rot(-14, 0, 0);
            m.part("hand" + k, "fore" + k, x, 13, 0, -2.5f, 0, -2.5f, 5, 4, 5, SKIN);
            for (int i = -1; i <= 1; i++)
                m.part("claw" + k + (i + 1), "hand" + k, x + i * 1.6f, 17, -1.6f, -0.45f, 0, -0.45f, 0.9f, 5, 0.9f, CLAW).rot(-12, 0, i * 7);
        }
        m.group("pick", "handR", -8.4f, 15, -1);
        m.part("pickShaft", "pick", -8.4f, 15, -1, -0.9f, -24, -0.9f, 1.8f, 30, 1.8f, WOOD).pattern(Pattern.STRIPE_H, WOOD_D, 3).rot(-55, 0, 0);
        m.part("pickBar", "pickShaft", -8.4f, -9, -1, -1, -1.2f, -9, 2, 2.4f, 18, IRON).grain(0.06f).rot(-55, 0, 0);
        m.part("pickTipA", "pickBar", -8.4f, -9, -10, -0.8f, -0.6f, -4, 1.6f, 1.6f, 4, IRON_D).rot(-55, 0, 0);
        m.part("pickTipB", "pickBar", -8.4f, -9, 8, -0.8f, -0.6f, 0, 1.6f, 1.6f, 4, IRON_D).rot(-55, 0, 0);

        // tail
        String par = "hips";
        float z = 3.4f;
        for (int i = 0; i < 4; i++) {
            float w = 4.4f - i * 0.8f;
            m.part("tail" + i, par, 0, 1, z, -w / 2, -w / 2, 0, w, w, 5, i % 2 == 0 ? FUR : FUR_D).grain(0.08f).rot(i == 0 ? 20 : 8, 0, 0);
            par = "tail" + i;
            z += 5;
        }
        m.animator(WildWolfSpec::animate);
        return m;
    }

    private static void animate(ModelParts m, AnimCtx c) {
        float a = c.age, t = c.t, w = c.walk(), ls = c.limbSwing;
        for (String k : new String[] {"R", "L"}) {
            float ph = k.equals("R") ? 0 : 3.14159f, sw = Anim.sinr(ls * 0.55f + ph) * w;
            m.addRot("thigh" + k, sw * 40, 0, 0);
            m.addRot("shin" + k, Math.max(0, -sw) * 36, 0, 0);
            m.addRot("arm" + k, -sw * 32 + Anim.sinr(a * 0.06f + ph) * 3, 0, 0);
        }
        m.addRot("chest", Anim.sinr(a * 0.09f) * 2.5f + w * 4, Anim.sinr(ls * 0.55f) * 8 * w, 0);
        m.addRot("neck", Anim.sinr(a * 0.05f + 1) * 3, Math.max(-40, Math.min(40, c.headYaw)) * 0.7f, 0);
        m.addRot("jaw", Anim.sinr(a * 0.12f) * 4, 0, 0);
        m.addRot("mane", Anim.sinr(a * 0.1f) * 3 + w * 8, 0, 0);
        for (int i = 0; i < 6; i++) m.addRot("spine" + i, Anim.sinr(a * 0.12f + i) * 4 + w * 6, 0, 0);
        for (int i = 0; i < 4; i++) m.addRot("tail" + i, Anim.sinr(a * 0.09f - i * 0.6f) * 3, Anim.sinr(a * 0.1f - i * 0.7f) * (6 + i * 2) + Anim.sinr(ls * 0.55f - i * 0.4f) * 8 * w, 0);
        m.addRot("pick", Anim.sinr(a * 0.07f) * 3, 0, 0);
        m.move("hips", 0, Anim.sinr(ls * 1.1f) * 0.6f * w, 0);

        if (c.is("pick_smash")) {
            float up = Anim.curve(t, 0, 0, 18, 1, 20, 0, 44, 0);
            float dn = Anim.curve(t, 0, 0, 20, 0, 23, 1, 36, 1, 44, 0);
            m.addRot("chest", -26 * up + 40 * dn, Anim.curve(t, 0, 0, 18, -12, 22, 8, 44, 0), 0);
            m.addRot("armR", -150 * up + 170 * dn, 0, 12 * up);
            m.addRot("pick", -30 * up + 40 * dn, 0, 0);
            m.addRot("armL", -50 * up + 30 * dn, 0, -20 * up);
            m.addRot("neck", -12 * up + 16 * dn, 0, 0);
            m.addRot("thighR", 18 * up - 10 * dn, 0, 0); m.addRot("thighL", -20 * up + 22 * dn, 0, 0);
        } else if (c.is("pick_sweep")) {
            float wd = Anim.curve(t, 0, 0, 14, 1, 16, 0, 40, 0);
            float sw = Anim.curve(t, 0, 0, 14, 0, 18, 1, 30, 1, 40, 0);
            m.addRot("chest", 6, Anim.curve(t, 0, 0, 14, 70, 18, -80, 30, -80, 40, 0), 0);
            m.addRot("armR", -60 * wd - 20 * sw, 0, 90 * wd - 130 * sw);
            m.addRot("pick", -10, 0, 0);
            m.addRot("armL", -30, 0, -40 * sw);
            m.addRot("neck", 0, Anim.curve(t, 0, 0, 14, -24, 18, 24, 40, 0), 0);
            m.addRot("thighR", -14 * sw, 0, 0); m.addRot("thighL", 14 * sw, 0, 0);
        } else if (c.is("claw_rake")) {
            m.addRot("chest", 8, Anim.curve(t, 0, 0, 9, 26, 15, -24, 21, 26, 34, 0), 0);
            float r = Anim.curve(t, 0, 0, 5, -120, 9, 55, 12, -120, 15, 55, 18, -120, 21, 55, 28, 0, 34, 0);
            float l = Anim.curve(t, 0, 0, 8, 0, 11, -120, 15, 55, 18, 0, 34, 0);
            m.addRot("armL", l, 0, 0); m.addRot("foreL", -l * 0.2f, 0, 0);
            m.addRot("armR", r * 0.6f, 0, 0);
            m.addRot("neck", 8, 0, 0); m.addRot("jaw", 24, 0, 0);
        } else if (c.is("pounce")) {
            float cr = Anim.curve(t, 0, 0, 13, 1, 14, 0.8f, 18, 0, 44, 0);
            float air = Anim.curve(t, 0, 0, 14, 0, 18, 1, 30, 1, 36, 0, 44, 0);
            m.move("hips", 0, 7 * cr, 0);
            m.addRot("chest", 14 * cr - 18 * air, 0, 0);
            for (String k : new String[] {"R", "L"}) {
                m.addRot("arm" + k, 24 * cr - 110 * air, 0, 0);
                m.addRot("thigh" + k, -34 * cr + 30 * air, 0, 0);
                m.addRot("shin" + k, 56 * cr - 24 * air, 0, 0);
            }
            m.addRot("jaw", 40 * air, 0, 0);
            for (int i = 0; i < 4; i++) m.addRot("tail" + i, -10 * air, 0, 0);
        } else if (c.is("howl")) {
            float up = Anim.curve(t, 0, 0, 12, 1, 38, 1, 50, 0);
            m.addRot("chest", -34 * up, Anim.sinr(a * 2.6f) * 2 * (t > 12 && t < 38 ? 1 : 0), 0);
            m.addRot("neck", -50 * up, 0, 0);
            m.addRot("jaw", 60 * up, 0, 0);
            m.addRot("armR", -30 * up, 0, 60 * up); m.addRot("armL", -30 * up, 0, -60 * up);
            for (int i = 0; i < 6; i++) m.addRot("spine" + i, -16 * up, 0, 0);
        } else if (c.is("pick_throw")) {
            float wd = Anim.curve(t, 0, 0, 16, 1, 18, 0, 40, 0);
            float th = Anim.curve(t, 0, 0, 16, 0, 19, 1, 28, 0, 40, 0);
            m.addRot("chest", -16 * wd + 20 * th, Anim.curve(t, 0, 0, 16, 30, 19, -24, 40, 0), 0);
            m.addRot("armR", -140 * wd + 170 * th, 0, 0);
            m.show("pick", !(t > 18 && t < 38));
        } else if (c.is("ground_pick")) {
            float up = Anim.curve(t, 0, 0, 16, 1, 18, 0, 46, 0);
            float dn = Anim.curve(t, 0, 0, 16, 0, 20, 1, 36, 1, 46, 0);
            m.addRot("chest", -22 * up + 34 * dn, 0, 0);
            m.addRot("armR", -170 * up + 200 * dn, 0, 0);
            m.addRot("pick", -20 * up + 50 * dn, 0, 0);
            m.addRot("armL", -60 * up + 40 * dn, 0, -20 * up);
        } else if (c.is("rampage")) {
            float ph = Anim.sinr(a * 1.0f);
            m.addRot("chest", 18, Anim.sinr(a * 0.45f) * 22, 0);
            m.addRot("armR", -80 + ph * 80, 0, 0); m.addRot("armL", -50 - ph * 60, 0, 0);
            m.addRot("neck", 12, 0, 0); m.addRot("jaw", 30, 0, 0);
            m.addRot("thighR", ph * 30, 0, 0); m.addRot("thighL", -ph * 30, 0, 0);
        }
        if (!c.is("pick_throw")) m.show("pick", true);

        if (c.death > 0) {
            float d = Anim.easeOut(c.death);
            m.addRot("root", -84 * d, 0, 0);
            m.move("root", 0, -2 * d, 0);
            m.addRot("armR", 40 * d, 0, 22 * d); m.addRot("armL", 30 * d, 0, -22 * d);
        }
    }
}
