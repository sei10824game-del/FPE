package com.fpe.client.spec;

import com.fpe.client.model.Anim;
import com.fpe.client.model.AnimCtx;
import com.fpe.client.model.ModelParts;
import com.fpe.client.model.ModelSpec;
import com.fpe.client.model.ModelSpec.Face;
import com.fpe.client.model.ModelSpec.Part;
import com.fpe.client.model.ModelSpec.Pattern;

/**
 * Alice. PHASE1 = bandaged girl with a floating ring of black spike wings (docs/ref/07_alice.png).
 * PHASE2 = 6.5-block glossy black monster: bug wings, giant claws, red slit eyes, white grin (docs/ref/08_alice_monster.png).
 */
public final class AliceSpec {
    private AliceSpec() {}

    // ------------------------------------------------------------------ shared helpers
    private static float cv(float t, float... tv) { return Anim.curve(t, tv); }
    /** 0 -> 1 over `up` ticks before `at`, back to 0 over `down` ticks after */
    private static float pulse(float t, float at, float up, float down) {
        if (t < at - up || t > at + down) return 0;
        return t < at ? Anim.smooth((t - (at - up)) / up) : 1 - Anim.smooth((t - at) / down);
    }
    private static float win(float t, float a, float b, float fade) {
        return Anim.smooth((t - a) / fade) * (1 - Anim.smooth((t - b) / fade));
    }

    // =================================================================== PHASE 1
    private static final int BAND = 0xDAD3C6, BAND2 = 0xB3AA9B, BLOOD = 0x8E1C1C, SKIN = 0xE9D2C3, SKIN2 = 0xD8B6A6,
            HAIR = 0x5B3B31, HAIR2 = 0x45302A, PONCHO = 0x6C6C72, PONCHO2 = 0x56565C, BLACK = 0x17171B, SKIRT = 0x1F1F24, PATCH = 0x86705E;
    private static final float[] WZ = { -58, -90, -121, 57, 88, 119 }, WX = { 8, 16, 26, 8, 16, 26 }, WL = { 0.95f, 1.12f, 0.85f, 0.9f, 1.05f, 0.8f };

    private static Part band(ModelSpec m, String n, String par, float px, float py, float pz, float ox, float oy, float oz, float w, float h, float d) {
        return m.part(n, par, px, py, pz, ox, oy, oz, w, h, d, BAND).pattern(Pattern.DIAG, BAND2, 1).grain(0.05f);
    }

    private static ModelSpec buildP1() {
        ModelSpec m = new ModelSpec("alice");
        m.group("root", null, 0, 24, 0);
        m.group("hips", "root", 0, 13, 0);
        // legs (bandaged, scratched) + sandals, ankle cuff on the left
        for (int s = -1; s <= 1; s += 2) {
            String k = s < 0 ? "R" : "L";
            float x = 1.3f * s;
            band(m, "thigh" + k, "hips", x, 13, 0, -1, 0, -1, 2, 6, 2).decor(Face.FRONT, s < 0 ? 0 : 1, 2, 1, 2, BLOOD).decor(Face.LEFT, 1, 3, 1, 1, BLOOD);
            band(m, "shin" + k, "thigh" + k, x, 19, 0, -1, 0, -1, 2, 4.6f, 2).decor(Face.FRONT, 0, 1, 1, 1, BLOOD).decor(Face.FRONT, 1, 2, 1, 1, BLOOD)
                    .decor(Face.FRONT, 0, 4, 2, 1, SKIN2).decor(Face.FRONT, 0, 3, 2, 1, BLACK).decor(Face.RIGHT, 0, 3, 2, 1, BLACK).decor(Face.LEFT, 0, 3, 2, 1, BLACK);
            m.part("foot" + k, "shin" + k, x, 23.6f, 0, -1.25f, 0, -2.3f, 2.5f, 0.45f, 3.4f, BLACK).decor(Face.TOP, 0, 0, 3, 1, SKIN2);
        }
        m.part("cuffL", "shinL", 1.3f, 19, 0, -1.3f, 2.4f, -1.3f, 2.6f, 1f, 2.6f, 0x101012).decor(Face.FRONT, 1, 0, 1, 1, 0x707078);
        m.part("cuffRing", "cuffL", 1.3f, 21.9f, -1.3f, -0.5f, 0, -0.9f, 1f, 1.2f, 0.4f, 0x707078);
        // ragged black skirt with patches
        m.part("skirt", "hips", 0, 12.4f, 0, -3, 0, -2.3f, 6, 4, 4.6f, SKIRT)
                .decor(Face.FRONT, 1, 1, 2, 2, PATCH).decor(Face.FRONT, 1, 1, 1, 1, 0x5E4A3E).decor(Face.FRONT, 4, 2, 2, 1, 0x34343A)
                .decor(Face.LEFT, 1, 1, 2, 2, PATCH).decor(Face.BACK, 3, 1, 2, 2, PATCH);
        float[][] rags = { // x, z, w, h, rotX, rotZ, (front/back/side)
                { -1.8f, -2.05f, 2.2f, 2.8f, -8, 7 }, { 1.5f, -2.05f, 2.2f, 3.6f, -10, -9 }, { -1.5f, 2.05f, 2.4f, 3.3f, 10, 5 }, { 1.6f, 2.05f, 2f, 2.5f, 8, -7 } };
        for (int i = 0; i < rags.length; i++) {
            float[] r = rags[i];
            m.part("sk" + i, "skirt", r[0], 16.3f, r[1], -r[2] / 2, -0.2f, -0.25f, r[2], r[3], 0.5f, i % 2 == 0 ? 0x232328 : 0x1A1A1E).rot(r[4], 0, r[5])
                    .decor(Face.FRONT, 0, (int) r[3] - 1, 1, 1, 0x0E0E10);
        }
        m.part("sk4", "skirt", -2.85f, 16.3f, 0, -0.25f, -0.2f, -1.6f, 0.5f, 3.2f, 3.2f, 0x202025).rot(0, 0, 11);
        m.part("sk5", "skirt", 2.85f, 16.3f, 0, -0.25f, -0.2f, -1.3f, 0.5f, 3.8f, 2.6f, 0x1B1B1F).rot(0, 0, -13);
        // torso + poncho
        m.group("body", "hips", 0, 13, 0);
        m.part("torso", "body", 0, 13, 0, -2.3f, -9, -1.4f, 4.6f, 9, 2.8f, 0x2C2C32);
        m.part("poncho", "body", 0, 4, 0, -3.4f, -0.3f, -2.05f, 6.8f, 5.6f, 4.1f, PONCHO).pattern(Pattern.GRADIENT_V, PONCHO2, 1)
                .decor(Face.FRONT, 0, 5, 7, 1, PONCHO2).decor(Face.BACK, 2, 1, 2, 2, PATCH).decor(Face.TOP, 2, 1, 3, 2, 0x7A7A80);
        m.part("patch1", "poncho", -2.1f, 5.3f, -2.15f, -0.8f, -0.8f, -0.1f, 1.6f, 1.6f, 0.2f, PATCH).rot(0, 0, 45).decor(Face.FRONT, 0, 0, 1, 1, 0x4A3A32);
        m.part("patch2", "poncho", 2.4f, 7.6f, -2.15f, -0.6f, -0.6f, -0.1f, 1.2f, 1.2f, 0.2f, 0x9A8676).rot(0, 0, 45);
        float[][] prag = { { -2.5f, -1.95f, 1.8f, 1.9f, -6, 8 }, { 0.2f, -1.95f, 2.4f, 1.3f, -4, -3 }, { 2.6f, -1.75f, 1.6f, 2.4f, -6, -11 }, { -1.5f, 1.95f, 2.4f, 2.5f, 8, 4 }, { 1.8f, 1.95f, 2f, 1.7f, 6, -7 } };
        for (int i = 0; i < prag.length; i++) {
            float[] r = prag[i];
            m.part("pr" + i, "poncho", r[0], 9.2f, r[1], -r[2] / 2, -0.2f, -0.2f, r[2], r[3], 0.4f, i % 2 == 0 ? PONCHO2 : 0x626268).rot(r[4], 0, r[5]);
        }
        m.part("collar", "body", 0, 4, 0, -1.6f, -0.9f, -1.6f, 3.2f, 1f, 3.2f, 0x1E1E22);
        m.part("cordR", "body", -1.1f, 4.2f, -2.12f, -0.12f, 0, -0.12f, 0.24f, 2.6f, 0.24f, 0x2A2420).rot(0, 0, -20);
        m.part("cordL", "body", 1.1f, 4.2f, -2.12f, -0.12f, 0, -0.12f, 0.24f, 2.6f, 0.24f, 0x2A2420).rot(0, 0, 20);
        m.part("pendant", "body", 0, 6.6f, -2.2f, -1.25f, 0, -0.25f, 2.5f, 2f, 0.4f, 0x2A1E1A)
                .decor(Face.FRONT, 1, 0, 1, 1, 0xB0563E).decor(Face.FRONT, 0, 1, 3, 1, 0xB0563E);
        // arms: bandaged, poncho sleeves, bare scratched hands; right hand carries a hidden bandage tendril
        for (int s = -1; s <= 1; s += 2) {
            String k = s < 0 ? "R" : "L";
            float x = 3.05f * s;
            band(m, "arm" + k, "body", x, 4.7f, 0, -1, -0.2f, -1, 2, 5.2f, 2).rot(0, 0, -5 * s).decor(Face.FRONT, 0, 3, 1, 2, BLOOD);
            m.part("sleeve" + k, "arm" + k, x, 4.7f, 0, -1.75f, -0.9f, -1.75f, 3.5f, 3.3f, 3.5f, PONCHO).pattern(Pattern.GRADIENT_V, PONCHO2, 1)
                    .decor(Face.FRONT, 0, 3, 1, 1, PONCHO2).decor(Face.FRONT, 2, 3, 1, 1, PONCHO2).decor(Face.BACK, 1, 3, 2, 1, PONCHO2);
            band(m, "fore" + k, "arm" + k, x, 9.7f, 0, -0.95f, 0, -0.95f, 1.9f, 4.8f, 1.9f).rot(-8, 0, 0).decor(Face.FRONT, 1, 1, 1, 2, BLOOD);
            m.part("hand" + k, "fore" + k, x, 14.5f, 0, -1.05f, 0, -1.05f, 2.1f, 2.6f, 2.1f, SKIN)
                    .decor(Face.FRONT, 0, 2, 3, 1, SKIN2).decor(Face.FRONT, 1, 0, 1, 2, BLOOD).decor(Face.LEFT, 0, 1, 2, 1, BLOOD);
        }
        m.group("tendril", "handR", -3.05f, 17f, 0);
        String prev = "tendril";
        for (int i = 0; i < 4; i++) {
            band(m, "tnd" + i, prev, -3.05f, 17f + i * 5, 0, -0.45f, 0, -0.45f, 0.9f, 5.2f, 0.9f).decor(Face.FRONT, 0, 2, 1, 1, BLOOD);
            prev = "tnd" + i;
        }
        // head: blindfold, closed smile, messy brown hair, black spiked crown
        m.part("head", "body", 0, 4, 0, -3.4f, -6.8f, -3.4f, 6.8f, 6.8f, 6.8f, SKIN)
                .decor(Face.FRONT, 1, 4, 1, 1, 0x5A2626).decor(Face.FRONT, 2, 5, 3, 1, 0x5A2626).decor(Face.FRONT, 5, 4, 1, 1, 0x5A2626)
                .decor(Face.FRONT, 0, 6, 7, 1, SKIN2);
        m.part("mouthOpen", "head", 0, 4, 0, -1.2f, -2.4f, -3.55f, 2.4f, 1.6f, 0.3f, 0x2A0808).decor(Face.FRONT, 0, 0, 3, 1, 0xEEEEEE);
        m.part("blind", "head", 0, 4, 0, -3.6f, -4.7f, -3.6f, 7.2f, 1.5f, 7.2f, 0x141416).decor(Face.FRONT, 0, 0, 8, 1, 0x26262C);
        m.part("hairTop", "head", 0, 4, 0, -3.8f, -7.7f, -3.8f, 7.6f, 2.3f, 7.6f, HAIR).pattern(Pattern.STRIPE_V, HAIR2, 2);
        m.part("hairBack", "head", 0, 4, 0, -3.8f, -6f, 1.3f, 7.6f, 6f, 2.6f, HAIR).pattern(Pattern.STRIPE_V, HAIR2, 2).decor(Face.BACK, 0, 5, 2, 1, HAIR2);
        m.part("hairR", "head", -3.5f, -2.6f, 0, -0.65f, 0, -3.3f, 1.3f, 5.6f, 5.4f, HAIR).rot(0, 0, 7).pattern(Pattern.STRIPE_H, HAIR2, 2);
        m.part("hairL", "head", 3.5f, -2.6f, 0, -0.65f, 0, -3.3f, 1.3f, 5.2f, 5.4f, HAIR).rot(0, 0, -7).pattern(Pattern.STRIPE_H, HAIR2, 2);
        float[][] fr = { { -2.5f, -12, 20, 3.2f }, { -0.8f, -14, 7, 3.6f }, { 0.9f, -13, -9, 3.3f }, { 2.6f, -11, -22, 2.9f } };
        for (int i = 0; i < fr.length; i++)
            m.part("fringe" + i, "head", fr[i][0], -2.7f, -3.6f, -0.95f, 0, -0.6f, 1.9f, fr[i][3], 1.2f, i % 2 == 0 ? HAIR : HAIR2).rot(fr[i][1], 0, fr[i][2]);
        m.part("ahoge", "head", 0.6f, -3.6f, -0.5f, -0.3f, -4, -0.3f, 0.6f, 4, 0.6f, HAIR).rot(-30, 0, -30);
        m.part("ahoge2", "ahoge", 0.6f, -7.6f, -0.5f, -0.25f, -3, -0.25f, 0.5f, 3, 0.5f, HAIR).rot(-60, 0, -40);
        m.part("hairS0", "head", -2.2f, -1.2f, 3.2f, -0.8f, 0, -0.6f, 1.6f, 3, 1.2f, HAIR2).rot(25, 0, 22);
        m.part("hairS1", "head", 2.2f, -1.2f, 3.2f, -0.8f, 0, -0.6f, 1.6f, 3, 1.2f, HAIR2).rot(25, 0, -22);
        m.part("crown", "head", 0, -3.5f, 0, -2.9f, -1, -2.9f, 5.8f, 1, 5.8f, BLACK).rot(0, 0, -10);
        float[][] cs = { { 0, -2.5f, -10, 0, 2.6f }, { -2.3f, -1.4f, -6, 18, 2.2f }, { 2.3f, -1.4f, -6, -18, 2.2f }, { -2.2f, 2.2f, 10, 14, 2f }, { 2.2f, 2.2f, 10, -14, 2f },
                { -2.9f, 0.2f, 0, 40, 3.4f }, { 2.9f, 0.2f, 0, -40, 3.4f } };
        for (int i = 0; i < cs.length; i++)
            m.part("cs" + i, "crown", cs[i][0], -4.5f, cs[i][1], -0.55f, -cs[i][4], -0.55f, 1.1f, cs[i][4], 1.1f, 0x0E0E11).rot(cs[i][2], 45, cs[i][3]);
        // ring of six floating black spike wings
        m.group("wings", "body", 0, 6.5f, 2.9f);
        for (int i = 0; i < 6; i++) {
            float L = WL[i];
            m.group("w" + i, "wings", 0, 6.5f, 2.9f).rot(WX[i], 0, WZ[i]);
            m.part("w" + i + "a", "w" + i, 0, 6.5f, 2.9f, -0.95f, -2 - 6 * L, -0.65f, 1.9f, 6 * L, 1.3f, 0x141418).decor(Face.FRONT, 0, 0, 1, 6, 0x2C2C34);
            m.part("w" + i + "b", "w" + i, 0, 6.5f, 2.9f, -0.6f, -2 - 10.5f * L, -0.45f, 1.2f, 4.6f * L, 0.9f, 0x101013);
            m.part("w" + i + "c", "w" + i, 0, 6.5f, 2.9f, -0.28f, -2 - 13.2f * L, -0.28f, 0.56f, 2.8f * L, 0.56f, 0x0A0A0C);
        }
        m.shadow(0.5f);
        m.animator(AliceSpec::animP1);
        return m;
    }

    private static void wingTo(ModelParts m, int i, float k, float x, float y, float z) {
        m.rot("w" + i, Anim.lerp(WX[i], x, k), Anim.lerp(0, y, k), Anim.lerp(WZ[i], z, k));
    }

    /** bend the legs so the hips sink by `a` px with feet staying planted */
    private static void crouchP1(ModelParts m, float a) {
        if (a < 0) { m.move("hips", 0, a, 0); return; }
        float d = (float) Math.toDegrees(Math.acos(1 - Math.min(1.6f, a / 11f)));
        m.move("hips", 0, a, 0);
        for (String k : new String[] { "R", "L" }) { m.addRot("thigh" + k, -d, 0, 0); m.addRot("shin" + k, 2 * d, 0, 0); m.addRot("foot" + k, -d, 0, 0); }
    }

    private static void armP1(ModelParts m, String k, float x, float y, float z, float fore) {
        m.addRot("arm" + k, x, y, z); m.addRot("fore" + k, fore, 0, 0);
    }

    private static void animP1(ModelParts m, AnimCtx c) {
        float t = c.t, age = c.age, w = c.walk();
        float ph = c.limbSwing * 0.75f, sw = Anim.sinr(ph) * w;
        // ---- idle: hunched, head tilted, wings floating, occasional twitch
        float br = Anim.sinr(age * 0.08f);
        m.addRot("body", 7 + br * 1.5f + w * 16, 0, Anim.sinr(age * 0.05f) * 2);
        m.move("body", 0, 0, 0);
        float tw = (age % 70) < 3 ? Anim.sinr(age * 9) * 16 : 0;
        m.addRot("head", c.headPitch * 0.6f - 4 - w * 12, c.headYaw * 0.8f, 13 + Anim.sinr(age * 0.05f) * 4 + tw);
        m.addRot("armR", -sw * 22 + 8 * w + br, 0, 4 + br * 2);
        m.addRot("armL", sw * 22 + 8 * w - br, 0, -4 - br * 2);
        m.addRot("foreR", -10 - w * 15, 0, 0); m.addRot("foreL", -6 - w * 15, 0, 0);
        m.addRot("thighR", sw * 40, 0, 0); m.addRot("thighL", -sw * 40, 0, 0);
        m.addRot("shinR", Math.max(0, Anim.sinr(ph + 1.3f)) * 50 * w, 0, 0); m.addRot("shinL", Math.max(0, Anim.sinr(ph + 1.3f + 3.14f)) * 50 * w, 0, 0);
        m.move("hips", 0, -Math.abs(Anim.sinr(ph)) * 0.7f * w, 0);
        for (int i = 0; i < 6; i++) m.addRot("w" + i, Anim.sinr(age * 0.1f + i) * 4 - w * 12, 0, Anim.sinr(age * 0.07f + i * 1.3f) * 5);
        m.move("wings", 0, Anim.sinr(age * 0.12f) * 0.5f, 0.4f + Anim.sinr(age * 0.09f) * 0.3f);
        m.addRot("ahoge", Anim.sinr(age * 0.11f) * 8, 0, 0);
        for (int i = 0; i < 6; i++) m.addRot("sk" + i, (i < 2 ? -1 : 1) * Math.abs(sw) * 12 + Anim.sinr(age * 0.13f + i) * 2, 0, 0);
        m.hide("mouthOpen");
        m.hide("tendril");

        switch (c.ability) {
            case "wing_stab" -> {
                float tw2 = cv(t, 0, 0, 8, 20, 12, -18, 16, -18, 20, -25, 23, 20, 28, 15, 36, 0);
                m.addRot("body", cv(t, 0, 0, 8, -8, 12, 18, 16, 12, 20, 2, 23, 18, 28, 10, 36, 0), tw2, 0);
                m.addRot("head", cv(t, 0, 0, 8, -10, 12, 15, 20, -5, 23, 15, 36, 0), 0, -6);
                crouchP1(m, cv(t, 0, 0, 8, 2, 12, 1, 20, 2, 23, 1, 36, 0));
                armP1(m, "R", cv(t, 0, 0, 8, -40, 12, 25, 20, 10, 36, 0), 0, cv(t, 0, 0, 8, 25, 12, 10, 36, 0), -40 * win(t, 4, 30, 4));
                armP1(m, "L", cv(t, 0, 0, 8, 20, 12, -10, 20, -40, 23, 25, 36, 0), 0, cv(t, 0, 0, 20, -25, 23, -10, 36, 0), -40 * win(t, 4, 30, 4));
                m.addRot("thighR", cv(t, 0, 0, 12, -25, 20, 0, 23, 15, 36, 0), 0, 0);
                m.addRot("thighL", cv(t, 0, 0, 12, 15, 20, 0, 23, -25, 36, 0), 0, 0);
                stab(m, 1, t, 4, 10, 12, 18);
                stab(m, 4, t, 15, 21, 23, 29);
                for (int i : new int[] { 0, 2, 3, 5 }) m.addRot("w" + i, 0, 0, (i < 3 ? -1 : 1) * 15 * win(t, 8, 28, 4));
            }
            case "wing_whirl" -> {
                float cr = cv(t, 0, 0, 9, 3, 12, 1, 21, 1, 26, 0);
                crouchP1(m, cr);
                float spin = Anim.linear(t, 0, 0, 10, 40, 21, -360, 32, -360);
                m.addRot("root", 0, spin + 360 * (t > 21 ? 1 : 0), 0);
                m.addRot("body", cv(t, 0, 0, 9, 30, 12, 10, 21, 10, 32, 0), 0, 0);
                float spread = win(t, 10, 22, 2);
                for (int i = 0; i < 6; i++) {
                    float fold = cv(t, 0, 0, 9, 1, 11, 0, 32, 0);
                    m.addRot("w" + i, 50 * fold, 0, -(i < 3 ? -1 : 1) * 30 * fold);
                    if (spread > 0) wingTo(m, i, spread, 90, i * 60 + 30, 0);
                    m.scale("w" + i, 1, 1 + 0.45f * spread, 1);
                }
                armP1(m, "R", cv(t, 0, 0, 9, -50, 12, -10, 32, 0), 0, cv(t, 0, 0, 9, -35, 12, 75, 21, 75, 32, 0), 0);
                armP1(m, "L", cv(t, 0, 0, 9, -50, 12, -10, 32, 0), 0, -cv(t, 0, 0, 9, -35, 12, 75, 21, 75, 32, 0), 0);
                m.addRot("head", cv(t, 0, 0, 9, 25, 12, -5, 32, 0), 0, 0);
            }
            case "bandage_whip" -> {
                m.addRot("body", cv(t, 0, 0, 7, -12, 12, 15, 20, 10, 23, -14, 28, -8, 34, 0), cv(t, 0, 0, 7, 30, 12, -25, 20, -20, 23, 10, 34, 0), 0);
                armP1(m, "R", cv(t, 0, 0, 7, -170, 9, -175, 12, -88, 20, -85, 23, -40, 28, -30, 34, 0), 0, cv(t, 0, 0, 7, 15, 12, -5, 34, 0), cv(t, 0, 0, 7, -50, 12, 0, 20, 0, 23, -50, 34, 0));
                armP1(m, "L", cv(t, 0, 0, 7, 30, 12, -25, 23, 25, 34, 0), 0, cv(t, 0, 0, 7, -20, 34, 0), -20);
                m.addRot("thighL", cv(t, 0, 0, 10, -28, 23, -10, 34, 0), 0, 0);
                m.addRot("thighR", cv(t, 0, 0, 10, 18, 23, 20, 34, 0), 0, 0);
                m.addRot("head", cv(t, 0, 0, 7, -10, 12, 10, 34, 0), 0, 0);
                float ext = cv(t, 8, 0.3f, 12, 5.5f, 20, 5.5f, 23, 2f, 26, 0.6f);
                if (t > 8 && t < 26) {
                    m.show("tendril", true);
                    m.scale("tendril", 1, ext, 1);
                    float amp = t < 12 ? 40 : t < 20 ? 6 : 30;
                    for (int i = 0; i < 4; i++) m.addRot("tnd" + i, Anim.sinr(t * 1.4f + i * 1.1f) * amp, 0, Anim.sinr(t * 0.9f + i) * amp * 0.4f);
                }
            }
            case "spike_line" -> {
                float rise = cv(t, 0, 0, 10, 1, 12, 0, 38, 0);
                crouchP1(m, -1.2f * rise + cv(t, 0, 0, 10, 0, 14, 3.5f, 28, 3.2f, 38, 0));
                m.addRot("body", cv(t, 0, 0, 10, -16, 12, 20, 14, 55, 28, 50, 38, 0) + (t > 14 && t < 28 ? Anim.sinr(age * 3) * 2 : 0), 0, 0);
                float ax = cv(t, 0, 0, 10, -168, 12, -150, 14, -92, 28, -88, 38, 0);
                armP1(m, "R", ax, 0, cv(t, 0, 0, 10, 15, 14, 8, 38, 0), cv(t, 0, 0, 10, -20, 14, 5, 38, 0));
                armP1(m, "L", ax, 0, -cv(t, 0, 0, 10, 15, 14, 8, 38, 0), cv(t, 0, 0, 10, -20, 14, 5, 38, 0));
                m.addRot("head", cv(t, 0, 0, 10, -25, 14, -30, 28, -30, 38, 0), 0, 0);
                for (int i = 0; i < 6; i++) {
                    float s = i < 3 ? -1 : 1;
                    m.addRot("w" + i, cv(t, 0, 0, 10, -15, 14, 70, 28, 65, 38, 0), 0, s * cv(t, 0, 0, 10, -30, 14, 10, 38, 0));
                }
            }
            case "blink_rake" -> {
                float wrap = cv(t, 0, 0, 7, 1, 9, 1);
                crouchP1(m, 3 * wrap * (t < 11 ? 1 : 0) + (t >= 11 ? cv(t, 11, 3, 15, 1.5f, 21, 2, 30, 0) : 0));
                if (t < 11) {
                    m.addRot("body", 35 * wrap + Anim.sinr(age * 6) * 3 * wrap, 0, 0);
                    armP1(m, "R", -60 * wrap, 0, -40 * wrap, -60 * wrap);
                    armP1(m, "L", -60 * wrap, 0, 40 * wrap, -60 * wrap);
                    for (int i = 0; i < 6; i++) wingTo(m, i, wrap * 0.8f, 75, 0, (i < 3 ? -1 : 1) * 40);
                    float sc = 1 - 0.45f * Anim.smooth((t - 5) / 4);
                    m.scale("root", sc, sc, sc);
                    if (t > 8.5f) m.hide("root");
                } else {
                    float sc = 0.6f + 0.4f * Anim.easeOut((t - 11) / 3);
                    m.scale("root", sc, sc, sc);
                    m.addRot("body", cv(t, 11, 35, 13, 20, 15, 30, 21, 30, 30, 0), cv(t, 11, 0, 13, 30, 15, -30, 18, -30, 21, 30, 25, 10, 30, 0), 0);
                    armP1(m, "R", cv(t, 11, -40, 13, -140, 15, -60, 17, -30, 30, 0), 0, cv(t, 11, 10, 13, 60, 15, -45, 18, -30, 30, 0), cv(t, 11, -40, 13, -30, 15, 0, 30, 0));
                    armP1(m, "L", cv(t, 11, -40, 17, -40, 19, -140, 21, -60, 24, -30, 30, 0), 0, cv(t, 11, -10, 17, -15, 19, -60, 21, 45, 24, 30, 30, 0), cv(t, 11, -40, 19, -30, 21, 0, 30, 0));
                    m.addRot("head", cv(t, 11, 20, 15, 5, 30, 0), 0, 0);
                    for (int i = 0; i < 6; i++) m.addRot("w" + i, 30 * win(t, 12, 24, 3), 0, (i < 3 ? -1 : 1) * 10 * win(t, 12, 24, 3));
                }
            }
            case "shadow_volley" -> {
                float fl = cv(t, 0, 0, 10, 1, 30, 1, 40, 0);
                m.move("root", 0, -4.5f * fl + Anim.sinr(age * 0.3f) * 0.4f * fl, 0);
                for (String k : new String[] { "R", "L" }) { m.addRot("thigh" + k, 12 * fl, 0, 0); m.addRot("shin" + k, 22 * fl, 0, 0); m.addRot("foot" + k, 45 * fl, 0, 0); }
                m.addRot("thighL", -10 * fl, 0, 0);
                m.addRot("body", -14 * fl, 0, 0);
                m.addRot("head", -18 * fl, 0, -8 * fl);
                armP1(m, "R", 10 * fl, 0, 45 * fl, -20 * fl);
                armP1(m, "L", 10 * fl, 0, -45 * fl, -20 * fl);
                for (int i = 0; i < 6; i++) m.addRot("w" + i, -25 * fl, 0, (i < 3 ? -1 : 1) * 12 * fl);
                for (int s = 0; s < 5; s++) {
                    int wi = s % 2 == 0 ? (s / 2) % 3 : 3 + (s / 2) % 3;
                    float p = pulse(t, 10 + s * 4, 2, 3);
                    m.addRot("w" + wi, -55 * p, 0, 0);
                    m.scale("w" + wi, 1, 1 + 0.25f * p, 1);
                    m.addRot("body", -4 * p, 0, 0);
                }
            }
            case "grab_maul" -> {
                crouchP1(m, cv(t, 0, 0, 7, 2.8f, 10, 0.4f, 36, 1, 38, 0));
                m.addRot("body", cv(t, 0, 0, 7, -6, 10, 42, 14, 30, 36, 30, 38, -22, 42, -15, 48, 0), 0, 0);
                float ax = cv(t, 0, 0, 7, 35, 10, -115, 14, -80, 36, -82, 38, -175, 42, -150, 48, 0);
                float az = cv(t, 0, 0, 7, 45, 10, -12, 36, -18, 38, 30, 48, 0);
                armP1(m, "R", ax, 0, az, cv(t, 0, 0, 10, -10, 14, -45, 36, -45, 38, 0));
                armP1(m, "L", ax, 0, -az, cv(t, 0, 0, 10, -10, 14, -45, 36, -45, 38, 0));
                float bite = pulse(t, 18, 3, 4) + pulse(t, 28, 3, 4);
                m.addRot("head", 25 * bite - 10 * win(t, 3, 9, 2), 0, Anim.sinr(age * 1.3f) * 8 * win(t, 12, 36, 2));
                m.show("mouthOpen", bite > 0.3f);
                m.addRot("thighL", cv(t, 0, 0, 7, 0, 10, -35, 36, -25, 40, 0), 0, 0);
                m.addRot("thighR", cv(t, 0, 0, 10, 20, 36, 15, 40, 0), 0, 0);
                for (int i = 0; i < 6; i++) {
                    float p = pulse(t, i % 2 == 0 ? 18 : 28, 3, 4);
                    m.addRot("w" + i, 75 * p + 20 * win(t, 10, 36, 3), 0, -(i < 3 ? -1 : 1) * 35 * p);
                    m.move("w" + i, (i < 3 ? -2 : 2) * p, 0, -2 * p);
                    m.scale("w" + i, 1, 1 + 0.4f * p, 1);
                }
            }
            case "scream" -> {
                crouchP1(m, cv(t, 0, 0, 10, 2, 13, 2, 15, 0, 36, 0));
                float jit = t > 14 && t < 28 ? Anim.sinr(age * 7) : 0;
                m.addRot("body", cv(t, 0, 0, 10, 35, 13, 38, 15, -28, 28, -24, 36, 0) + jit * 3, 0, jit * 2);
                m.addRot("head", cv(t, 0, 0, 10, 25, 13, 25, 15, -35, 28, -30, 36, 0) + jit * 5, 0, -10 * win(t, 1, 13, 3));
                float ax = cv(t, 0, 0, 8, -150, 13, -150, 15, -70, 28, -65, 36, 0);
                float az = cv(t, 0, 0, 8, -38, 13, -38, 15, 105, 28, 100, 36, 0) + jit * 6;
                armP1(m, "R", ax, 0, az, cv(t, 0, 0, 8, -75, 13, -75, 15, 0, 36, 0));
                armP1(m, "L", ax, 0, -az, cv(t, 0, 0, 8, -75, 13, -75, 15, 0, 36, 0));
                m.show("mouthOpen", t > 14 && t < 30);
                float fl = win(t, 14, 30, 2), fold = win(t, 0, 13, 4);
                for (int i = 0; i < 6; i++) {
                    float s = i < 3 ? -1 : 1;
                    m.addRot("w" + i, 40 * fold - 20 * fl + jit * 6, 0, s * (25 * fl - 30 * fold));
                    m.scale("w" + i, 1, 1 + 0.35f * fl, 1);
                }
            }
            case "wing_burrow" -> {
                crouchP1(m, cv(t, 0, 0, 10, -0.8f, 12, 0, 15, 2.5f, 32, 2.2f, 40, 0));
                m.addRot("body", cv(t, 0, 0, 10, -10, 15, 22, 32, 20, 40, 0) + (t > 15 && t < 32 ? Anim.sinr(age * 2.5f) * 2 : 0), 0, 0);
                m.addRot("head", cv(t, 0, 0, 10, -20, 15, 22, 32, 18, 40, 0), 0, 0);
                armP1(m, "R", cv(t, 0, 0, 10, -100, 15, -55, 32, -50, 40, 0), 0, cv(t, 0, 0, 10, 30, 15, -45, 32, -45, 40, 0), cv(t, 0, 0, 15, -50, 32, -50, 40, 0));
                armP1(m, "L", cv(t, 0, 0, 10, -100, 15, -55, 32, -50, 40, 0), 0, -cv(t, 0, 0, 10, 30, 15, -45, 32, -45, 40, 0), cv(t, 0, 0, 15, -50, 32, -50, 40, 0));
                float up = cv(t, 0, 0, 10, 1, 12, 0), down = cv(t, 10, 0, 14, 1, 32, 1, 40, 0);
                for (int i = 0; i < 6; i++) {
                    float s = i < 3 ? -1 : 1;
                    if (down > 0) wingTo(m, i, down, 25, 0, s * (148 + (i % 3) * 9));
                    else wingTo(m, i, up, -10, 0, s * (12 + (i % 3) * 10));
                    m.scale("w" + i, 1, 1 + 0.4f * down * (t > 13 ? 1 : 0.5f), 1);
                    m.addRot("w" + i, 0, 0, t > 15 && t < 32 ? Anim.sinr(age * 4 + i) * 2 : 0);
                }
            }
            case "skitter" -> {
                float run = win(t, 6, 14, 1.5f);
                crouchP1(m, cv(t, 0, 0, 5, 3, 7, 1.2f, 14, 1.2f, 16, 2, 26, 0));
                m.addRot("body", cv(t, 0, 0, 5, 35, 14, 42, 16, 25, 26, 0), 0, Anim.sinr(t * 1.7f) * 6 * run);
                float ls = Anim.sinr(t * 1.7f) * run;
                m.addRot("thighR", ls * 55, 0, 0); m.addRot("thighL", -ls * 55, 0, 0);
                m.addRot("shinR", Math.max(0, -ls) * 70, 0, 0); m.addRot("shinL", Math.max(0, ls) * 70, 0, 0);
                armP1(m, "R", cv(t, 0, 0, 5, 45, 14, 55, 16, -45, 26, 0), 0, 15 * run, -30);
                armP1(m, "L", cv(t, 0, 0, 5, 45, 14, 55, 16, -45, 26, 0), 0, -15 * run, -30);
                m.addRot("head", cv(t, 0, 0, 5, -25, 14, -30, 16, 0, 26, 0), 0, 0);
                for (int i = 0; i < 6; i++) m.addRot("w" + i, -45 * cv(t, 0, 0, 5, 1, 14, 1, 18, 0), 0, 0);
                stab(m, 0, t, 11, 13, 15, 21);
                stab(m, 3, t, 11, 13, 15, 21);
            }
            case "transform" -> transformP1(m, c);
            default -> {}
        }
        if (c.death > 0) {
            float d = c.death, fall = Anim.easeIn(c.death * 1.4f - 0.3f);
            crouchP1(m, 3.5f * Anim.smooth(d * 2.5f));
            m.addRot("body", 30 * Anim.smooth(d * 2), 0, 0);
            m.addRot("root", 0, 0, 85 * fall);
            m.addRot("head", 30 * d, 0, 20 * d);
            armP1(m, "R", -20 * d, 0, 15 * d, 0);
            armP1(m, "L", -10 * d, 0, -25 * d, 0);
            for (int i = 0; i < 6; i++) wingTo(m, i, Anim.smooth(d * 1.5f) * 0.8f, 40, 0, (i < 3 ? -1 : 1) * (130 + i * 6));
        }
    }

    /** one spike-wing lances forward from the shoulder: wind a..b, strike at c, hold, retract by d */
    private static void stab(ModelParts m, int i, float t, float a, float b, float c, float d) {
        if (t < a - 2 || t > d + 2) return;
        float s = i < 3 ? -1 : 1;
        float wind = cv(t, a - 2, 0, b, 1, c, 0);
        float ext = cv(t, b, 0, c, 1, c + 3, 1, d, 0);
        m.addRot("w" + i, -35 * wind, 0, s * 20 * wind);
        if (ext > 0) wingTo(m, i, ext, 88, 0, s * 25);
        m.move("w" + i, s * 3.2f * ext, -1.5f * ext, -2f * ext);
        m.scale("w" + i, 1, 1 + 0.9f * ext, 1);
    }

    private static void transformP1(ModelParts m, AnimCtx c) {
        float t = Math.min(c.t, 90), age = c.age;
        float I = Anim.smooth(t / 85f), clutch = win(t, 2, 30, 6);
        float jx = Anim.sinr(age * 1.9f), jy = Anim.sinr(age * 2.7f + 1), jz = Anim.sinr(age * 3.3f + 2);
        crouchP1(m, 1.5f + 2.2f * I);
        m.addRot("root", 0, 0, jz * 4 * I);
        m.addRot("body", 20 * clutch + (30 + jx * 9) * I, jy * 10 * I, jz * 6 * I);
        m.addRot("head", 20 * clutch + jx * 28 * I, jy * 25 * I, jz * 35 * I);
        armP1(m, "R", -150 * clutch + (-60 + jx * 70) * I, 0, -38 * clutch + (40 + jy * 45) * I, -70 * clutch + jz * 40 * I);
        armP1(m, "L", -150 * clutch + (-60 + jy * 70) * I, 0, 38 * clutch - (40 + jz * 45) * I, -70 * clutch + jx * 40 * I);
        m.addRot("thighR", jy * 10 * I, 0, 8 * I); m.addRot("thighL", jz * 10 * I, 0, -8 * I);
        for (int i = 0; i < 6; i++) {
            m.addRot("w" + i, Anim.sinr(age * 3 + i) * 25 * I, 0, Anim.sinr(age * 2.3f + i * 2) * 25 * I);
            m.scale("w" + i, 1, 1 + 0.7f * I, 1);
        }
        m.show("mouthOpen", t > 30 && (age % 10) < 6);
        float g = 1 + 0.3f * Anim.smooth((t - 60) / 30);
        m.scale("root", g, g, g);
        if (t > 40) for (int i = 0; i < 5; i++) m.hide("pr" + i);
        if (t > 62) { m.hide("sleeveR"); m.hide("sleeveL"); }
        if (t > 80) { for (int i = 0; i < 6; i++) m.hide("sk" + i); m.hide("cuffL"); }
    }

    // =================================================================== PHASE 2
    private static final int BK = 0x0C0C10, BKH = 0x23232E, WING = 0xDCE0E8, WING2 = 0xA9AEBB, EYE = 0xFF1A3C, TEETH = 0xF2F2EC;

    private static Part blk(ModelSpec m, String n, String par, float px, float py, float pz, float ox, float oy, float oz, float w, float h, float d) {
        return m.part(n, par, px, py, pz, ox, oy, oz, w, h, d, BKH).pattern(Pattern.GRADIENT_V, BK, 1).grain(0.08f);
    }

    private static Part pane(ModelSpec m, String n, String par, float px, float py, float pz, float ox, float oy, float w, float h) {
        Part p = m.part(n, par, px, py, pz, ox, oy, -0.2f, w, h, 0.4f, WING).grain(0.04f);
        int W = (int) Math.ceil(w), H = (int) Math.ceil(h);
        for (Face f : new Face[] { Face.FRONT, Face.BACK }) {
            p.decor(f, 0, 0, W, 1, BK).decor(f, 0, H - 1, W, 1, BK).decor(f, 0, 0, 1, H, BK).decor(f, W - 1, 0, 1, H, BK)
                    .decor(f, W / 2, 1, 1, H - 2, WING2).decor(f, 1, H / 2, W - 2, 1, WING2).decor(f, W / 4, H / 4, 1, H / 2, WING2);
        }
        return p;
    }

    private static ModelSpec buildP2() {
        ModelSpec m = new ModelSpec("alice_boss");
        m.group("root", null, 0, 24, 0);
        m.group("hips", "root", 0, -27, 0);
        blk(m, "pelvis", "hips", 0, -27, 0, -5, -2, -3, 10, 6, 6);
        // long bowed legs with clawed feet
        for (int s = -1; s <= 1; s += 2) {
            String k = s < 0 ? "R" : "L";
            float x = 4.5f * s;
            blk(m, "thigh" + k, "hips", x, -26, 0, -2.5f, -1, -2.5f, 5, 30, 5).rot(-30, 0, -12 * s);
            blk(m, "shin" + k, "thigh" + k, x, 2, 0, -2, 0, -2, 4, 28, 4).rot(58, 0, 20 * s);
            blk(m, "foot" + k, "shin" + k, x, 30, 0, -3.5f, -1, -7, 7, 3, 10).rot(-28, 0, -8 * s);
            for (int i = 0; i < 3; i++)
                m.part("toe" + k + i, "foot" + k, x + (i - 1) * 2.3f, 31, -7, -0.8f, -0.8f, -6, 1.6f, 1.6f, 6, BK).rot(28, (1 - i) * 12 * -1, 0);
            m.part("spur" + k, "foot" + k, x, 30.5f, 3, -0.7f, -0.7f, 0, 1.4f, 1.4f, 4.5f, BK).rot(-25, 0, 0);
        }
        // thin hunched torso
        m.group("body", "hips", 0, -28, 0).rot(20, 0, 0);
        blk(m, "waist", "body", 0, -28, 0, -3.4f, -11, -2.6f, 6.8f, 11, 5.2f);
        blk(m, "chest", "body", 0, -38.5f, 0, -7, -14, -4.2f, 14, 14, 8.4f)
                .decor(Face.FRONT, 3, 7, 8, 1, BK).decor(Face.FRONT, 4, 9, 6, 1, BK).decor(Face.FRONT, 5, 11, 4, 1, BK).decor(Face.FRONT, 2, 1, 3, 1, 0x34344A).decor(Face.FRONT, 9, 1, 3, 1, 0x34344A);
        for (int i = 0; i < 3; i++) m.part("sp" + i, "chest", 0, -50 + i * 4.5f, 4, -0.8f, -0.8f, 0, 1.6f, 1.6f, 6 - i, BK).rot(35, 0, 0);
        m.part("sp3", "waist", 0, -33, 2.4f, -0.7f, -0.7f, 0, 1.4f, 1.4f, 4, BK).rot(35, 0, 0);
        blk(m, "neck", "chest", 0, -52, 0, -2.2f, -4, -2.2f, 4.4f, 5, 4.4f);
        // round head: red slit eyes, wide white grin, antenna curl, spiky hair
        Part head = blk(m, "head", "neck", 0, -55, -1, -8, -15, -7.5f, 16, 15, 15).rot(-20, 0, 0);
        head.decor(Face.FRONT, 2, 9, 12, 3, TEETH).decor(Face.FRONT, 1, 8, 1, 1, TEETH).decor(Face.FRONT, 14, 8, 1, 1, TEETH)
                .decor(Face.FRONT, 2, 10, 12, 1, 0x200508);
        for (int x = 3; x <= 13; x += 2) head.decor(Face.FRONT, x, 9, 1, 1, 0x3A3A3A).decor(Face.FRONT, x, 11, 1, 1, 0x3A3A3A);
        head.decor(Face.FRONT, 1, 12, 14, 1, BK).decor(Face.FRONT, 2, 3, 3, 1, 0x30303E).decor(Face.FRONT, 11, 3, 3, 1, 0x30303E);
        m.part("eyeR", "head", -4, -63.5f, -8.6f, -2.6f, -0.65f, -0.2f, 5.2f, 1.3f, 0.4f, EYE).rot(0, 0, 16).glow().decorGlow(Face.FRONT, 1, 0, 3, 1, 0xFF8090);
        m.part("eyeL", "head", 4, -63.5f, -8.6f, -2.6f, -0.65f, -0.2f, 5.2f, 1.3f, 0.4f, EYE).rot(0, 0, -16).glow().decorGlow(Face.FRONT, 2, 0, 3, 1, 0xFF8090);
        Part maw = m.part("maw", "head", 0, -59.5f, -8.6f, -6, -2.5f, -0.3f, 12, 5, 0.6f, 0x3A0610);
        maw.decor(Face.FRONT, 0, 0, 12, 1, TEETH).decor(Face.FRONT, 0, 4, 12, 1, TEETH);
        for (int x = 0; x < 12; x += 2) maw.decor(Face.FRONT, x, 1, 1, 1, TEETH).decor(Face.FRONT, x + 1, 3, 1, 1, TEETH);
        m.part("ant0", "head", 1, -69.5f, -2, -0.6f, -7, -0.6f, 1.2f, 7, 1.2f, BK).rot(-20, 0, -12);
        m.part("ant1", "ant0", 1, -76.5f, -2, -0.5f, -6, -0.5f, 1f, 6, 1f, BK).rot(45, 0, 0);
        m.part("ant2", "ant1", 1, -82.5f, -2, -0.4f, -5, -0.4f, 0.8f, 5, 0.8f, BK).rot(65, 0, 0);
        float[][] hs = { { -5, -67, 4, 35, -25 }, { 0, -69, 4, 45, 0 }, { 5, -67, 4, 35, 25 }, { -7.2f, -62, 3, 15, -55 }, { 7.2f, -62, 3, 15, 55 } };
        for (int i = 0; i < hs.length; i++)
            m.part("hs" + i, "head", hs[i][0], hs[i][1], hs[i][2], -1.3f, -1.3f, 0, 2.6f, 2.6f, 7.5f, BK).rot(hs[i][3], hs[i][4], 0);
        // very long arms: thin upper arm, thick forearm, giant clawed hand
        for (int s = -1; s <= 1; s += 2) {
            String k = s < 0 ? "R" : "L";
            float x = 7.6f * s;
            blk(m, "upper" + k, "chest", x, -49, 0, -1.8f, -1, -1.8f, 3.6f, 29, 3.6f).rot(-24, 0, -22 * s);
            blk(m, "fore" + k, "upper" + k, x, -21, 0, -3, 0, -3, 6, 24, 6).rot(-14, 0, 30 * s);
            blk(m, "hand" + k, "fore" + k, x, 3, 0, -4.5f, 0, -4, 9, 9, 8).rot(0, 0, -6 * s);
            float[] fx = { -3.4f, -1.2f, 1.0f, 3.2f };
            for (int i = 0; i < 4; i++)
                m.part("f" + k + i, "hand" + k, x + fx[i] * -s, 11.5f, -1.5f, -0.9f, 0, -0.9f, 1.8f, 12, 1.8f, BK).rot(12, 0, (1.5f - i) * 5 * s)
                        .decor(Face.FRONT, 0, 9, 2, 3, 0x2E2E3A);
            m.part("f" + k + "4", "hand" + k, x - 4.2f * s, 7, -3, -0.8f, 0, -0.8f, 1.6f, 9, 1.6f, BK).rot(-25, 0, -30 * s);
            m.part("as" + k + "0", "fore" + k, x + 2.5f * s, -14, 2.5f, -0.6f, -0.6f, 0, 1.2f, 1.2f, 6, BK).rot(30, 30 * s, 0);
            m.part("as" + k + "1", "fore" + k, x + 2.5f * s, -6, 2.5f, -0.6f, -0.6f, 0, 1.2f, 1.2f, 5, BK).rot(20, 30 * s, 0);
            m.part("sh" + k, "chest", x + 0.8f * s, -51, 1.5f, -0.8f, -0.8f, 0, 1.6f, 1.6f, 6.5f, BK).rot(60, 35 * s, 0);
        }
        // four bug wings (pale panes, black frame)
        m.group("wings", "chest", 0, -47, 4.6f);
        for (int s = -1; s <= 1; s += 2) {
            String k = s < 0 ? "R" : "L";
            float x = 2 * s;
            m.group("wU" + k, "wings", x, -48, 4.8f).rot(-12, -22 * s, 40 * s);
            pane(m, "wU" + k + "a", "wU" + k, x, -48, 4.8f, -2.5f, -14, 5, 14);
            pane(m, "wU" + k + "b", "wU" + k, x, -48, 4.8f, -4, -33, 8, 19);
            m.part("wU" + k + "e", "wU" + k, x, -48, 4.8f, 3.4f * -s - 0.6f, -33, -0.6f, 1.2f, 33, 1.2f, BK);
            m.group("wD" + k, "wings", x, -45, 4.8f).rot(10, -22 * s, 112 * s);
            pane(m, "wD" + k + "a", "wD" + k, x, -45, 4.8f, -2, -10, 4, 10);
            pane(m, "wD" + k + "b", "wD" + k, x, -45, 4.8f, -3, -23, 6, 13);
            m.part("wD" + k + "e", "wD" + k, x, -45, 4.8f, 2.4f * -s - 0.5f, -23, -0.5f, 1f, 23, 1f, BK);
        }
        m.shadow(1.6f);
        m.animator(AliceSpec::animP2);
        return m;
    }

    private static void crouchP2(ModelParts m, float a) {
        m.move("hips", 0, a, 0);
        for (String k : new String[] { "R", "L" }) { m.addRot("thigh" + k, -2.05f * a, 0, 0); m.addRot("shin" + k, 4.1f * a, 0, 0); m.addRot("foot" + k, -2.05f * a, 0, 0); }
    }

    /** arm pose (additive). z is mirrored for the left arm so positive = outward on both sides. */
    private static void armP2(ModelParts m, String k, float x, float y, float zOut, float fore) {
        float s = k.equals("R") ? 1 : -1;
        m.addRot("upper" + k, x, y * s, zOut * s);
        m.addRot("fore" + k, fore, 0, 0);
    }

    private static void fingers(ModelParts m, String k, float curl) {
        for (int i = 0; i < 5; i++) m.addRot("f" + k + i, curl, 0, 0);
    }

    private static void wingsP2(ModelParts m, float spread, float buzz, float age) {
        for (int s = -1; s <= 1; s += 2) {
            String k = s < 0 ? "R" : "L";
            float b = Anim.sinr(age * 2.6f + (s < 0 ? 0 : 1.7f)) * buzz;
            m.addRot("wU" + k, b * 6, b * 8 * s, -s * 0 + spread * 18 * s);
            m.addRot("wD" + k, -b * 5, -b * 8 * s, spread * 14 * s);
        }
    }

    private static void animP2(ModelParts m, AnimCtx c) {
        float t = c.t, age = c.age, w = c.walk();
        float ph = c.limbSwing * 0.42f, sw = Anim.sinr(ph) * w;
        float br = Anim.sinr(age * 0.06f);
        // ---- idle: heavy breathing, stalking sway, twitching claws, buzzing wings
        m.addRot("body", br * 2.5f + w * 6, 0, Anim.sinr(ph) * 4 * w);
        m.addRot("head", c.headPitch * 0.5f - br * 2, c.headYaw * 0.7f, Anim.sinr(age * 0.04f) * 7);
        m.addRot("thighR", sw * 26, 0, 0); m.addRot("thighL", -sw * 26, 0, 0);
        m.addRot("shinR", Math.max(0, Anim.sinr(ph + 1.4f)) * 30 * w, 0, 0); m.addRot("shinL", Math.max(0, Anim.sinr(ph + 4.54f)) * 30 * w, 0, 0);
        m.move("hips", 0, -Math.abs(Anim.sinr(ph)) * 2 * w, 0);
        armP2(m, "R", -sw * 18 + Anim.sinr(age * 0.06f + 1) * 3, 0, br * 2, 0);
        armP2(m, "L", sw * 18 + Anim.sinr(age * 0.06f + 2) * 3, 0, br * 2, 0);
        for (int i = 0; i < 4; i++) {
            m.addRot("fR" + i, Math.max(0, Anim.sinr(age * 0.25f + i)) * 12, 0, 0);
            m.addRot("fL" + i, Math.max(0, Anim.sinr(age * 0.22f + i + 2)) * 12, 0, 0);
        }
        wingsP2(m, 0, 1, age);
        for (int i = 0; i < 3; i++) m.addRot("ant" + i, Anim.sinr(age * 0.09f + i) * 6, 0, 0);
        m.hide("maw");

        switch (c.ability) {
            case "tentacle_field" -> {
                crouchP2(m, cv(t, 0, 0, 12, -2, 15, -2, 18, 6, 36, 5, 46, 0));
                m.addRot("body", cv(t, 0, 0, 12, -25, 15, -25, 18, 35, 36, 30, 46, 0) + (t > 18 && t < 36 ? Anim.sinr(age * 3) * 1.5f : 0), 0, 0);
                m.addRot("head", cv(t, 0, 0, 12, -25, 18, 10, 36, 5, 46, 0), 0, 0);
                float ax = cv(t, 0, 0, 12, -160, 15, -165, 18, -55, 36, -50, 46, 0);
                armP2(m, "R", ax, 0, cv(t, 0, 0, 12, -18, 18, 5, 46, 0), cv(t, 0, 0, 12, -30, 18, 10, 36, 10, 46, 0));
                armP2(m, "L", ax, 0, cv(t, 0, 0, 12, -18, 18, 5, 46, 0), cv(t, 0, 0, 12, -30, 18, 10, 36, 10, 46, 0));
                float dig = win(t, 18, 36, 3);
                fingers(m, "R", -25 * win(t, 4, 16, 3) + 45 * dig); fingers(m, "L", -25 * win(t, 4, 16, 3) + 45 * dig);
                m.show("maw", t > 10 && t < 22);
                wingsP2(m, win(t, 16, 30, 3), 1.5f, age);
            }
            case "spike_carpet" -> {
                crouchP2(m, cv(t, 0, 0, 12, 5, 16, 6, 32, 6, 48, 0));
                m.addRot("body", cv(t, 0, 0, 12, 30, 16, 45, 32, 40, 48, 0), 0, 0);
                m.addRot("head", cv(t, 0, 0, 12, -20, 16, -30, 32, -25, 48, 0), 0, 0);
                float ax = cv(t, 0, 0, 12, -40, 16, -70, 32, -65, 48, 0), az = cv(t, 0, 0, 12, 60, 16, 5, 32, 8, 48, 0);
                armP2(m, "R", ax, 0, az, cv(t, 0, 0, 12, -35, 16, -10, 48, 0));
                armP2(m, "L", ax, 0, az, cv(t, 0, 0, 12, -35, 16, -10, 48, 0));
                float f = cv(t, 0, 0, 12, -35, 16, 40, 32, 40, 48, 0);
                fingers(m, "R", f); fingers(m, "L", f);
                m.show("maw", t > 12 && t < 32);
                wingsP2(m, win(t, 14, 32, 3), 1.2f, age);
            }
            case "claw_slam" -> {
                crouchP2(m, cv(t, 0, 0, 14, -3, 18, -3, 21, 7, 34, 6, 44, 0));
                m.addRot("body", cv(t, 0, 0, 14, -20, 18, -22, 21, 45, 34, 40, 44, 0), cv(t, 0, 0, 14, 30, 21, -20, 34, -15, 44, 0), 0);
                m.addRot("head", cv(t, 0, 0, 14, -18, 21, 20, 44, 0), 0, 0);
                armP2(m, "R", cv(t, 0, 0, 14, -195, 18, -200, 21, -65, 34, -60, 44, 0), 0, cv(t, 0, 0, 14, -10, 21, 0, 44, 0), cv(t, 0, 0, 14, -40, 18, -55, 21, 0, 44, 0));
                armP2(m, "L", cv(t, 0, 0, 14, -30, 21, -15, 44, 0), 0, cv(t, 0, 0, 14, 25, 21, 15, 44, 0), 0);
                fingers(m, "R", cv(t, 0, 0, 14, -30, 21, 40, 34, 40, 44, 0));
                m.show("maw", t > 12 && t < 28);
                m.scale("maw", 1, 1 + 0.5f * win(t, 14, 28, 3), 1);
            }
            case "double_sweep" -> {
                crouchP2(m, cv(t, 0, 0, 11, 3, 15, 4, 22, 3, 27, 4, 46, 0));
                m.addRot("body", cv(t, 0, 0, 11, 5, 15, 25, 22, 10, 27, 25, 46, 0), cv(t, 0, 0, 11, 45, 15, -50, 22, -55, 27, 45, 34, 30, 46, 0), 0);
                m.addRot("head", cv(t, 0, 0, 15, 5, 46, 0), cv(t, 0, 0, 11, -25, 15, 25, 22, 30, 27, -25, 46, 0), 0);
                armP2(m, "R", cv(t, 0, 0, 11, -60, 15, -95, 18, -45, 46, 0), cv(t, 0, 0, 11, 20, 15, -40, 46, 0), cv(t, 0, 0, 11, 70, 15, -25, 22, -10, 46, 0), -20);
                armP2(m, "L", cv(t, 0, 0, 15, -20, 22, -60, 27, -95, 30, -45, 46, 0), cv(t, 0, 0, 22, 20, 27, -40, 46, 0), cv(t, 0, 0, 15, 5, 22, 70, 27, -25, 30, -10, 46, 0), -20);
                fingers(m, "R", -30 * win(t, 8, 18, 3)); fingers(m, "L", -30 * win(t, 20, 30, 3));
                m.show("maw", t > 10 && t < 30);
            }
            case "grab_crush" -> {
                crouchP2(m, cv(t, 0, 0, 10, 3, 15, 5, 26, 0, 44, 0, 46, 6, 52, 4, 56, 0));
                m.addRot("body", cv(t, 0, 0, 10, 10, 15, 35, 26, 8, 42, 5, 46, 45, 52, 40, 56, 0), cv(t, 0, 0, 10, 25, 15, -15, 26, -5, 56, 0), 0);
                float sq = pulse(t, 26, 2, 4) + pulse(t, 36, 2, 4);
                m.addRot("head", cv(t, 0, 0, 15, 5, 26, -15, 42, -15, 46, 25, 56, 0) + sq * 6, 0, 12 * win(t, 20, 42, 3));
                armP2(m, "R", cv(t, 0, 0, 10, -20, 15, -100, 18, -100, 26, -150, 42, -152, 46, -50, 50, -50, 56, 0) + sq * Anim.sinr(age * 5) * 5, 0,
                        cv(t, 0, 0, 10, 20, 15, -15, 26, -20, 46, -5, 56, 0), cv(t, 0, 0, 10, -60, 15, -10, 26, -45, 42, -45, 46, 0, 56, 0));
                armP2(m, "L", cv(t, 0, 0, 15, -25, 46, -25, 56, 0), 0, cv(t, 0, 0, 15, 30, 56, 0), 0);
                fingers(m, "R", t < 15 ? cv(t, 0, 0, 12, -40) : cv(t, 15, -40, 17, 70, 44, 70, 47, 0) + sq * 20);
                m.show("maw", t > 18 && t < 46);
                m.scale("maw", 1, 1 + 0.6f * sq, 1);
            }
            case "wing_gust" -> {
                float env = win(t, 12, 38, 3);
                float f = (float) Math.cos(2 * Math.PI * (t - 18) / 8) * env;
                float pre = win(t, 0, 14, 5);
                crouchP2(m, 3 * cv(t, 0, 0, 10, 1, 40, 1, 48, 0));
                m.addRot("body", 10 * pre + (10 - f * 8) * env, 0, 0);
                m.addRot("head", 15 * pre + 8 * env, 0, 0);
                armP2(m, "R", -40 * (pre + env * 0.8f), 0, -35 * (pre + env * 0.8f), -30 * env);
                armP2(m, "L", -40 * (pre + env * 0.8f), 0, -35 * (pre + env * 0.8f), -30 * env);
                for (int s = -1; s <= 1; s += 2) {
                    String k = s < 0 ? "R" : "L";
                    m.addRot("wU" + k, -25 * pre - f * 22, (-30 * pre + f * 55) * -s, 10 * pre * s);
                    m.addRot("wD" + k, -15 * pre - f * 15, (-25 * pre + f * 45) * -s, 0);
                }
            }
            case "orb_barrage" -> {
                float shot = t >= 14 && t < 40 ? 1 - ((t - 14) % 3) / 3f : 0;
                crouchP2(m, cv(t, 0, 0, 10, 2, 40, 2, 52, 0));
                m.addRot("body", cv(t, 0, 0, 10, -25, 14, -10, 38, -10, 44, 0, 52, 0) - shot * 3, 0, 0);
                m.addRot("head", cv(t, 0, 0, 10, -35, 14, 5, 38, 5, 52, 0) - shot * 8, Anim.sinr(age * 0.7f) * 8 * win(t, 14, 40, 2), 0);
                float alt = Anim.sinr((t - 14) * 1.05f) * win(t, 14, 40, 2);
                armP2(m, "R", cv(t, 0, 0, 10, -45, 40, -45, 52, 0) - 35 * Math.max(0, alt), 0, cv(t, 0, 0, 10, 55, 40, 45, 52, 0), -20);
                armP2(m, "L", cv(t, 0, 0, 10, -45, 40, -45, 52, 0) - 35 * Math.max(0, -alt), 0, cv(t, 0, 0, 10, 55, 40, 45, 52, 0), -20);
                fingers(m, "R", -30 * win(t, 8, 42, 3)); fingers(m, "L", -30 * win(t, 8, 42, 3));
                m.show("maw", t > 8 && t < 42);
                m.scale("maw", 1, 1.2f + 0.6f * shot, 1);
                wingsP2(m, win(t, 8, 42, 3) * 0.6f, 1.5f, age);
            }
            case "roar" -> {
                float vib = t > 19 && t < 40 ? Anim.sinr(age * 6) : 0;
                crouchP2(m, cv(t, 0, 0, 14, 6, 16, 6, 19, -1, 40, 0, 50, 0));
                m.addRot("body", cv(t, 0, 0, 14, 40, 16, 42, 19, -28, 40, -25, 50, 0) + vib * 2, 0, 0);
                m.addRot("head", cv(t, 0, 0, 14, 30, 16, 30, 19, -40, 40, -35, 50, 0) + vib * 4, 0, vib * 3);
                armP2(m, "R", cv(t, 0, 0, 14, -20, 19, -45, 40, -40, 50, 0), 0, cv(t, 0, 0, 14, -25, 19, 95, 40, 88, 50, 0) + vib * 4, cv(t, 0, 0, 14, -40, 19, -10, 50, 0));
                armP2(m, "L", cv(t, 0, 0, 14, -20, 19, -45, 40, -40, 50, 0), 0, cv(t, 0, 0, 14, -25, 19, 95, 40, 88, 50, 0) - vib * 4, cv(t, 0, 0, 14, -40, 19, -10, 50, 0));
                fingers(m, "R", -40 * win(t, 17, 42, 3)); fingers(m, "L", -40 * win(t, 17, 42, 3));
                m.show("maw", t > 15 && t < 44);
                m.scale("maw", 1, 1 + 0.9f * win(t, 16, 42, 3), 1);
                wingsP2(m, win(t, 16, 42, 3) * 1.4f, 3, age);
            }
            case "leap_slam" -> {
                float air = win(t, 14, 29, 2.5f);
                crouchP2(m, cv(t, 0, 0, 12, 10, 14, -2, 28, -2, 31, 9, 40, 7, 52, 0));
                m.addRot("thighR", -45 * air, 0, 0); m.addRot("thighL", -45 * air, 0, 0);
                m.addRot("shinR", 70 * air, 0, 0); m.addRot("shinL", 70 * air, 0, 0);
                m.addRot("body", cv(t, 0, 0, 12, 32, 15, -20, 27, -25, 31, 50, 40, 45, 52, 0), 0, 0);
                m.addRot("head", cv(t, 0, 0, 12, -15, 27, -20, 31, 25, 52, 0), 0, 0);
                float ax = cv(t, 0, 0, 12, 35, 15, -170, 27, -178, 31, -45, 40, -42, 52, 0);
                armP2(m, "R", ax, 0, cv(t, 0, 0, 12, 20, 15, -8, 31, 10, 52, 0), cv(t, 0, 0, 12, -10, 15, -30, 31, 0, 52, 0));
                armP2(m, "L", ax, 0, cv(t, 0, 0, 12, 20, 15, -8, 31, 10, 52, 0), cv(t, 0, 0, 12, -10, 15, -30, 31, 0, 52, 0));
                fingers(m, "R", 35 * win(t, 30, 42, 2)); fingers(m, "L", 35 * win(t, 30, 42, 2));
                m.show("maw", t > 14 && t < 34);
                wingsP2(m, air * 1.2f, 3 * air + 1, age);
            }
            case "eye_beam" -> {
                float ch = win(t, 0, 30, 4), fire = win(t, 30, 52, 2);
                float tr = Anim.sinr(age * 5) * 3 * Anim.smooth((t - 10) / 20) * (t < 30 ? 1 : 0.4f);
                crouchP2(m, cv(t, 0, 0, 24, 5, 52, 5, 62, 0));
                m.addRot("body", cv(t, 0, 0, 24, 30, 30, 25, 52, 25, 62, 0), 0, 0);
                m.addRot("head", cv(t, 0, 0, 24, 28, 29, 28, 31, -12, 52, -10, 62, 0) + tr, tr, 0);
                armP2(m, "R", -35 * (ch + fire), 0, 38 * (ch + fire), -20 * ch);
                armP2(m, "L", -35 * (ch + fire), 0, 38 * (ch + fire), -20 * ch);
                fingers(m, "R", 30 * (ch + fire) + tr * 3); fingers(m, "L", 30 * (ch + fire) - tr * 3);
                float es = 1 + 0.8f * Anim.smooth(t / 30) * (t < 52 ? 1 : 1 - Anim.smooth((t - 52) / 6));
                m.scale("eyeR", es, es, 1); m.scale("eyeL", es, es, 1);
                m.show("maw", fire > 0.3f);
            }
            case "vortex" -> {
                float on = win(t, 16, 58, 3);
                float clap = cv(t, 56, 0, 59, 1, 64, 1, 72, 0);
                crouchP2(m, cv(t, 0, 0, 16, -2, 56, -2, 60, 6, 66, 4, 72, 0));
                m.addRot("body", cv(t, 0, 0, 16, -12, 56, -10, 60, 35, 72, 0), Anim.sinr((t - 18) * 0.25f) * 25 * on, 0);
                m.addRot("head", cv(t, 0, 0, 16, -15, 56, -10, 60, 15, 72, 0), 0, Anim.sinr(age * 0.2f) * 15 * on);
                float beck = Math.max(0, Anim.sinr((t - 18) * 0.5f)) * on;
                float az = cv(t, 0, 0, 16, 85, 56, 85, 59, -18, 64, -18, 72, 0) - 45 * beck;
                armP2(m, "R", cv(t, 0, 0, 16, -45, 56, -45, 59, -85, 64, -80, 72, 0), 0, az, -40 * beck - 10 * clap);
                armP2(m, "L", cv(t, 0, 0, 16, -45, 56, -45, 59, -85, 64, -80, 72, 0), 0, az, -40 * beck - 10 * clap);
                fingers(m, "R", 50 * beck); fingers(m, "L", 50 * beck);
                m.show("maw", on > 0.5f || clap > 0.5f);
                wingsP2(m, on * 1.3f, 2.5f, age);
            }
            case "black_rain" -> {
                float up = win(t, 0, 60, 8), tr = Anim.sinr(age * 4) * 3 * win(t, 20, 60, 3);
                m.addRot("body", -20 * up, 0, 0);
                m.addRot("head", -40 * up + tr, 0, 0);
                crouchP2(m, -2 * up);
                armP2(m, "R", -175 * up + tr, 0, 15 * up, 0);
                armP2(m, "L", -175 * up - tr, 0, 15 * up, 0);
                float flex = t >= 20 && t < 60 ? 1 - ((t - 20) % 3) / 3f : 0;
                fingers(m, "R", -40 * up + 50 * flex); fingers(m, "L", -40 * up + 50 * flex);
                m.show("maw", up > 0.5f);
                m.scale("maw", 1, 1.4f, 1);
                wingsP2(m, up * 1.2f, 2, age);
            }
            case "stomp" -> {
                m.addRot("thighR", cv(t, 0, 0, 9, -65, 12, 8, 18, 0, 30, 0), 0, 0);
                m.addRot("shinR", cv(t, 0, 0, 9, 55, 12, -10, 18, 0), 0, 0);
                crouchP2(m, cv(t, 0, 0, 9, -1, 12, 4, 20, 3, 30, 0));
                m.addRot("body", cv(t, 0, 0, 9, -12, 12, 22, 20, 18, 30, 0), 0, cv(t, 0, 0, 9, 6, 12, -4, 30, 0));
                armP2(m, "R", cv(t, 0, 0, 9, -30, 12, 0), 0, cv(t, 0, 0, 9, 35, 12, 5, 30, 0), 0);
                armP2(m, "L", cv(t, 0, 0, 9, -30, 12, 0), 0, cv(t, 0, 0, 9, 35, 12, 5, 30, 0), 0);
                m.addRot("head", cv(t, 0, 0, 9, -10, 12, 20, 30, 0), 0, 0);
            }
            case "abyss" -> {
                float ring = pulse(t, 34, 3, 4) + pulse(t, 42, 3, 4) + pulse(t, 50, 3, 4);
                crouchP2(m, cv(t, 0, 0, 18, -4, 56, -4, 62, -3, 66, 10, 76, 8, 86, 0) + 3 * ring);
                m.addRot("body", cv(t, 0, 0, 18, -30, 56, -25, 62, -30, 66, 55, 76, 50, 86, 0) + 15 * ring, 0, 0);
                m.addRot("head", cv(t, 0, 0, 18, -45, 30, -20, 56, -20, 62, -35, 66, 30, 86, 0), 0, Anim.sinr(age * 0.5f) * 6 * win(t, 20, 56, 3));
                float ax = cv(t, 0, 0, 18, -60, 56, -60, 62, -188, 64, -190, 66, -45, 76, -45, 86, 0) + 45 * ring;
                float az = cv(t, 0, 0, 18, 100, 56, 90, 62, 10, 66, 0, 86, 0) - 30 * ring;
                armP2(m, "R", ax, 0, az, -15 * win(t, 0, 60, 4));
                armP2(m, "L", ax, 0, az, -15 * win(t, 0, 60, 4));
                fingers(m, "R", -40 * win(t, 4, 56, 4) + 50 * ring + 40 * win(t, 64, 76, 2));
                fingers(m, "L", -40 * win(t, 4, 56, 4) + 50 * ring + 40 * win(t, 64, 76, 2));
                m.show("maw", (t > 4 && t < 26) || (t > 60 && t < 76));
                m.scale("maw", 1, 1.8f, 1);
                wingsP2(m, win(t, 4, 64, 4) * 1.5f, 3, age);
                float es = 1 + 0.6f * win(t, 4, 76, 4);
                m.scale("eyeR", es, es, 1); m.scale("eyeL", es, es, 1);
            }
            case "transform" -> transformP2(m, c);
            default -> {}
        }
        if (c.death > 0) {
            float d = c.death, buckle = Anim.smooth(d * 2.2f), fall = Anim.easeIn(Anim.clamp((d - 0.3f) / 0.45f, 0, 1)), melt = Anim.smooth((d - 0.75f) / 0.25f);
            crouchP2(m, 12 * buckle);
            m.addRot("body", 40 * buckle, 0, 0);
            m.addRot("root", 75 * fall, 0, 0);
            m.addRot("head", 25 * buckle, 0, 15 * d);
            armP2(m, "R", 20 * buckle, 0, 25 * buckle, 0);
            armP2(m, "L", 10 * buckle, 0, 35 * buckle, 0);
            wingsP2(m, -1.2f * d, 0, age);
            m.scale("root", 1 + 0.15f * melt, 1 - 0.85f * melt, 1 + 0.15f * melt);
        }
    }

    private static void transformP2(ModelParts m, AnimCtx c) {
        float t = c.t, age = c.age;
        if (t < Alice_T_FLIP) { // not visible in game (phase 1 model is shown) - curled embryo for the preview
            float sh = Anim.sinr(age * 3) * 3;
            m.scale("root", 0.4f, 0.4f, 0.4f);
            crouchP2(m, 12);
            m.addRot("body", 60 + sh, 0, 0);
            armP2(m, "R", -60, 0, -30, -60); armP2(m, "L", -60, 0, -30, -60);
            wingsP2(m, -1.5f, 0, age);
            return;
        }
        float grow = Anim.easeOut((t - 90) / 20), roar = win(t, 111, 122, 3), rise = Anim.smooth((t - 90) / 22);
        float sc = 0.45f + 0.55f * grow;
        float sh = Anim.sinr(age * 4) * 3 * (1 - rise);
        m.scale("root", sc, sc, sc);
        crouchP2(m, 12 * (1 - rise) - 1 * roar);
        m.addRot("body", 55 * (1 - rise) + sh - 28 * roar, 0, 0);
        m.addRot("head", 35 * (1 - rise) - 40 * roar + Anim.sinr(age * 6) * 3 * roar, 0, 0);
        float wrap = 1 - Anim.smooth((t - 104) / 8);
        armP2(m, "R", -55 * wrap - 40 * roar, 0, -35 * wrap + 100 * roar, -60 * wrap);
        armP2(m, "L", -55 * wrap - 40 * roar, 0, -35 * wrap + 100 * roar, -60 * wrap);
        fingers(m, "R", -40 * roar); fingers(m, "L", -40 * roar);
        wingsP2(m, -1.5f * (1 - rise) + 1.4f * roar, 1 + 2 * roar, age);
        float wsc = 0.3f + 0.7f * Anim.smooth((t - 96) / 14);
        for (String k : new String[] { "wUR", "wUL", "wDR", "wDL" }) m.scale(k, wsc, wsc, wsc);
        m.show("maw", roar > 0.2f);
        m.scale("maw", 1, 1 + 0.9f * roar, 1);
    }

    private static final int Alice_T_FLIP = 90; // keep in sync with Alice.T_FLIP (client must not need the entity class here)

    // built last so every constant above is initialised first
    public static final ModelSpec PHASE1 = buildP1();
    public static final ModelSpec PHASE2 = buildP2();
}
