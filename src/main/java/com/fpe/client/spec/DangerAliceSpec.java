package com.fpe.client.spec;

import com.fpe.client.model.Anim;
import com.fpe.client.model.AnimCtx;
import com.fpe.client.model.ModelParts;
import com.fpe.client.model.ModelSpec;
import com.fpe.client.model.ModelSpec.Face;

/**
 * Danger AU Alice (Δlice), canon per the Danger AU fanon wiki: short messy brown hair, pointed ahoge, spiky black crown, black ear piercings, tan skin,
 * long black trench coat with leather belt, grey turtleneck, yellow danger-sign pendant, dagger under the skirt, black leggings, long pointed-heel boots.
 * Variant 1 (partially transformed): six huge black spikes with claws, long black tail, giant black claw hand, yellow slit-pupil eyes, tattered hem.
 */
public final class DangerAliceSpec {
    private DangerAliceSpec() {}

    static final int HAIR = 0x5E4234, HAIR_D = 0x46301F, SKIN = 0xD6A476, COAT = 0x17171D, COAT_L = 0x24242C, GREY = 0x484852, GREY_D = 0x34343E,
            BLACK = 0x0F0F13, BOOT = 0x131318, SIGN = 0xE8A850, STEEL = 0xC4C8D0, EYE = 0xFFD83A;

    public static final ModelSpec SPEC = com.fpe.client.model.BbModel.load("danger_alice", 0.68f);
    /** variant 1 (monster form); needs registering: FpeRenderer(c, SPEC, PHASE2) in ClientSetup + Specs.all() */
    public static final ModelSpec PHASE2 = com.fpe.client.model.BbModel.load("danger_alice_boss", 1.58f);
    static final ModelSpec PROC = build();

    private static final String[] SPIKES = {"spk0", "spk1", "spk2", "spk3", "spk4", "spk5"};

    private static ModelSpec build() {
        ModelSpec m = new ModelSpec("danger_alice");
        m.group("root", null, 0, 24, 0);
        m.group("spin", "root", 0, 12, 0);

        for (int s = -1; s <= 1; s += 2) {
            String k = s < 0 ? "R" : "L";
            float x = 1.9f * s;
            m.part("leg" + k, "spin", x, 12, 0, -1.6f, 0, -1.6f, 3.2f, 6, 3.2f, BLACK);
            m.part("shin" + k, "leg" + k, x, 18, 0, -1.9f, 0, -1.9f, 3.8f, 6, 3.8f, BOOT).decor(Face.FRONT, 0, 0, 4, 1, COAT_L);
            m.part("toe" + k, "shin" + k, x, 23, 0, -1.9f, -0.9f, -4.6f, 3.8f, 1.5f, 2.8f, BOOT);
            m.part("heel" + k, "shin" + k, x, 23, 1.6f, -0.5f, -0.4f, 0, 1, 1.4f, 2, BOOT).rot(25, 0, 0);
            m.part("ankSpk" + k, "shin" + k, x, 22.4f, 0, -0.4f, -0.4f, -2.6f, 0.8f, 0.8f, 3, BLACK).rot(0, s * 30, 0);
        }
        m.part("skirtPanel", "spin", 0, 12, 0, -2.4f, -0.4f, -2.7f, 4.8f, 11, 0.7f, GREY).decor(Face.FRONT, 0, 9, 5, 2, GREY_D);
        m.part("coatR", "spin", -2.6f, 12, 0, -2.3f, -0.5f, -2.5f, 4.6f, 11, 5, COAT).rot(0, 0, 3).decor(Face.FRONT, 0, 9, 5, 2, COAT_L);
        m.part("coatL", "spin", 2.6f, 12, 0, -2.3f, -0.5f, -2.5f, 4.6f, 11, 5, COAT).rot(0, 0, -3).decor(Face.FRONT, 0, 9, 5, 2, COAT_L);
        m.part("coatBack", "spin", 0, 12, 2.4f, -4.5f, -0.5f, -0.4f, 9, 11, 1, COAT).rot(5, 0, 0);
        m.part("hemTear", "spin", 0, 12, 0, -4.8f, 10, -2.7f, 9.6f, 1.2f, 5.4f, BLACK);

        m.part("torso", "spin", 0, 12, 0, -3.8f, -12, -2.2f, 7.6f, 12, 4.4f, COAT).decor(Face.FRONT, 3, 0, 1, 12, COAT_L);
        m.part("turtle", "torso", 0, 2.4f, 0, -3, -1, -2, 6, 8, 4, GREY).decor(Face.FRONT, 0, 6, 6, 1, GREY_D);
        m.part("collar", "torso", 0, 0, 0, -2.2f, -1.4f, -2.2f, 4.4f, 2, 4.4f, GREY_D);
        m.part("belt", "torso", 0, 12, 0, -4, -3, -2.5f, 8, 1.6f, 5, BLACK).decor(Face.FRONT, 3, 0, 2, 2, STEEL);
        m.part("chain", "torso", 0, 2, -2.3f, -0.3f, 0, 0, 0.6f, 3, 0.4f, STEEL);
        m.part("sign", "torso", 0, 5, -2.5f, -1.5f, 0, 0, 3, 3, 0.5f, SIGN).decor(Face.FRONT, 1, 0, 1, 2, BLACK).decor(Face.FRONT, 1, 2, 1, 1, BLACK);
        m.part("dagger", "legR", -1.9f, 15, -1.9f, -0.4f, 0, -1.5f, 0.8f, 5, 0.8f, STEEL).rot(-6, 0, 0);   // revealed only while used

        // head, hair, ahoge, spiky crown, piercings
        m.part("head", "torso", 0, 0, 0, -3.4f, -7, -3.4f, 6.8f, 7, 6.8f, SKIN)
                .decor(Face.FRONT, 1, 3, 2, 1, 0x30200E).decor(Face.FRONT, 4, 3, 2, 1, 0x30200E).decor(Face.FRONT, 0, 4, 1, 1, 0xC47E70).decor(Face.FRONT, 5, 4, 2, 1, 0xC47E70)
                .decor(Face.FRONT, 2, 5, 3, 1, 0x7A4030).decor(Face.RIGHT, 3, 3, 1, 2, BLACK).decor(Face.LEFT, 3, 3, 1, 2, BLACK);
        m.part("eyeR", "head", -2, -4, -3.5f, -1.2f, -0.6f, -0.5f, 2.4f, 1.2f, 0.4f, EYE).glow().decor(Face.FRONT, 1, 0, 1, 1, BLACK);
        m.part("eyeL", "head", 2, -4, -3.5f, -1.2f, -0.6f, -0.5f, 2.4f, 1.2f, 0.4f, EYE).glow().decor(Face.FRONT, 1, 0, 1, 1, BLACK);
        m.part("hairTop", "head", 0, -7, 0, -3.8f, -1.6f, -3.8f, 7.6f, 2.4f, 7.6f, HAIR);
        m.part("hairBack", "head", 0, -6, 3, -3.8f, 0, 0, 7.6f, 8, 1.8f, HAIR);
        m.part("fringeA", "head", -1.6f, -5.6f, -3.6f, -2.4f, 0, -0.3f, 3.4f, 2.4f, 0.7f, HAIR).rot(0, 0, 8);
        m.part("fringeB", "head", 1.6f, -5.6f, -3.6f, -1, 0, -0.3f, 3.2f, 3.4f, 0.7f, HAIR_D).rot(0, 0, -10);
        m.part("lockR", "head", -3.6f, -5, 0, -1, 0, -3.2f, 1.6f, 6, 6.4f, HAIR).rot(0, 0, 6);
        m.part("lockL", "head", 3.6f, -5, 0, -0.6f, 0, -3.2f, 1.6f, 7, 6.4f, HAIR_D).rot(0, 0, -6);
        for (int i = 0; i < 5; i++) {
            float x = -3.2f + i * 1.6f;
            m.part("crown" + i, "head", x, -8, 0, -0.9f, -3 - (i % 2 == 0 ? 2.4f : 0.8f), -0.9f, 1.8f, 3 + (i % 2 == 0 ? 2.4f : 0.8f), 1.8f, BLACK).rot(0, 0, (i - 2) * 10);
        }
        m.part("ahoge0", "head", 1, -8.4f, 0.5f, -0.4f, -2.6f, -0.4f, 0.8f, 2.6f, 0.8f, HAIR).rot(-10, 0, 14);
        m.part("ahoge1", "ahoge0", 1.6f, -10.8f, 0.2f, -0.4f, -2.4f, -0.4f, 0.8f, 2.4f, 0.8f, HAIR).rot(-18, 0, 20);
        m.part("ahoge2", "ahoge1", 2.6f, -13, -0.4f, -0.4f, -2, -0.4f, 0.8f, 2, 0.8f, HAIR).rot(-24, 0, 24);

        // arms: right hand human, left hand turns into a giant black claw
        for (int s = -1; s <= 1; s += 2) {
            String k = s < 0 ? "R" : "L";
            float x = 5.2f * s;
            m.part("arm" + k, "torso", x, 2, 0, -1.7f, -1, -1.7f, 3.4f, 9, 3.4f, COAT);
            m.part("hand" + k, "arm" + k, x, 10, 0, -1.4f, 0, -1.4f, 2.8f, 2.8f, 2.8f, SKIN);
        }
        m.part("bigClaw", "armL", 5.2f, 10, 0, -3, 0, -3, 6, 6, 6, BLACK);
        for (int i = 0; i < 4; i++) m.part("bclaw" + i, "bigClaw", 5.2f + (i - 1.5f) * 1.4f, 16, -1, -0.5f, 0, -0.5f, 1, 9, 1, BLACK).rot(-8, 0, (i - 1.5f) * 9);

        // six huge spikes with claws + long tail (partially transformed form)
        for (int i = 0; i < 6; i++) {
            float s = i % 2 == 0 ? -1 : 1, row = i / 2;
            m.part("spk" + i, "torso", s * (2.4f + row), 3 + row * 2.8f, 2.6f, -0.9f, -20 - row * 3, -0.9f, 1.8f, 20 + row * 3, 1.8f, BLACK).rot(-36 - row * 8, 0, s * (24 + row * 16));
            m.part("spkClaw" + i, "spk" + i, s * (2.4f + row), -17 - row * 0.2f, 2.6f, -0.6f, -9, -0.6f, 1.2f, 9, 1.2f, BLACK).rot(70, 0, 0);
        }
        String par = "spin";
        float z = 2.4f;
        for (int i = 0; i < 7; i++) {
            float w = Math.max(1.2f, 3 - i * 0.28f);
            m.part("tail" + i, par, 0, 10, z, -w / 2, -w / 2, 0, w, w, 5, BLACK).rot(i == 0 ? 18 : -4, 0, 0);
            par = "tail" + i;
            z += 5;
        }

        m.animator(DangerAliceSpec::animate);
        return m;
    }

    private static float sgn(String k) { return k.equals("R") ? -1f : 1f; }

    private static void animate(ModelParts m, AnimCtx c) {
        float a = c.age, t = c.t, w = c.walk(), ls = c.limbSwing;
        boolean tf = c.variant == 1 || c.is("reveal");
        boolean full = c.variant == 1 && !c.is("reveal");
        boolean armed = c.is("dagger_combo") || c.is("dagger_throw") || c.is("blink_stab");
        for (String n : SPIKES) { m.show(n, tf); }
        for (int i = 0; i < 6; i++) m.show("spkClaw" + i, tf);
        for (int i = 0; i < 7; i++) m.show("tail" + i, tf);
        m.show("bigClaw", full);
        for (int i = 0; i < 4; i++) m.show("bclaw" + i, full);
        m.show("handL", !full);
        m.show("eyeR", tf); m.show("eyeL", tf);
        m.show("hemTear", tf); m.show("dagger", armed);
        for (String k : new String[] {"R", "L"}) { m.show("ankSpk" + k, tf); }
        m.show("sign", true);

        for (String k : new String[] {"R", "L"}) {
            float ph = k.equals("R") ? 0 : 3.14159f, sw = Anim.sinr(ls * 0.6f + ph) * w;
            m.addRot("leg" + k, sw * 38, 0, 0);
            m.addRot("shin" + k, Math.max(0, -sw) * 28, 0, 0);
            m.addRot("arm" + k, -sw * 28 + Anim.sinr(a * 0.07f + ph) * 2, 0, sgn(k) * -2);
        }
        m.addRot("torso", Anim.sinr(a * 0.08f) * 1.2f, Anim.sinr(ls * 0.6f) * 5 * w, 0);
        m.addRot("head", Anim.sinr(a * 0.05f) * 2, Math.max(-40, Math.min(40, c.headYaw)) * 0.7f, 0);
        m.addRot("ahoge0", Anim.sinr(a * 0.1f) * 5, 0, Anim.sinr(a * 0.08f) * 4);
        m.addRot("ahoge1", Anim.sinr(a * 0.12f + 1) * 6, 0, 0);
        m.addRot("coatBack", w * 12 + Anim.sinr(a * 0.07f) * 2, 0, 0);
        for (int i = 0; i < 6; i++) m.addRot("spk" + i, Anim.sinr(a * 0.06f + i * 0.8f) * 5 + w * 6, 0, 0);
        for (int i = 0; i < 6; i++) m.addRot("spkClaw" + i, Anim.sinr(a * 0.08f + i) * 8, 0, 0);
        for (int i = 0; i < 7; i++) m.addRot("tail" + i, Anim.sinr(a * 0.09f - i * 0.6f) * 3, Anim.sinr(a * 0.11f - i * 0.7f) * (6 + i) + Anim.sinr(ls * 0.6f - i * 0.5f) * 8 * w, 0);
        m.move("spin", 0, Anim.sinr(ls * 1.2f) * 0.4f * w, 0);

        if (c.is("dagger_combo")) {
            m.addRot("torso", 8, Anim.curve(t, 0, 0, 12, -24, 19, 24, 26, -8, 30, 0, 38, 0), 0);
            float r = Anim.curve(t, 0, 0, 5, -100, 12, 40, 14, 0, 16, -100, 19, 40, 22, 0, 24, -120, 26, -85, 30, -85, 38, 0);
            m.addRot("armR", r, 0, 0);
            m.addRot("legR", Anim.curve(t, 0, 0, 24, 0, 26, -28, 38, 0), 0, 0);
            m.addRot("legL", Anim.curve(t, 0, 0, 24, 0, 26, 18, 38, 0), 0, 0);
        } else if (c.is("dagger_throw")) {
            float wind = Anim.curve(t, 0, 0, 12, 1, 14, 0, 32, 0);
            float thr = Anim.curve(t, 0, 0, 12, 0, 15, 1, 24, 0, 32, 0);
            m.addRot("torso", -12 * wind + 14 * thr, Anim.curve(t, 0, 0, 12, 18, 15, -14, 32, 0), 0);
            m.addRot("armR", -150 * wind + 190 * thr, 0, 0);
        } else if (c.is("blink_stab")) {
            float crouch = Anim.curve(t, 0, 0, 6, 1, 8, 0, 32, 0);
            float stab = Anim.curve(t, 0, 0, 16, 0, 20, 1, 28, 0.6f, 32, 0);
            m.move("spin", 0, 4 * crouch, 0);
            m.addRot("torso", 14 * crouch + 16 * stab, 0, 0);
            m.addRot("armR", -110 * stab, 0, 0);
            m.addRot("legR", -22 * stab, 0, 0);
        } else if (c.is("pendant_pulse")) {
            float up = Anim.curve(t, 0, 0, 14, 1, 30, 1, 40, 0);
            m.addRot("torso", -10 * up, 0, 0);
            m.addRot("head", -16 * up, 0, 0);
            m.addRot("armR", -50 * up, 0, 40 * up); m.addRot("armL", -50 * up, 0, -40 * up);
        } else if (c.is("reveal")) {
            float k = Anim.clamp(t / 44f, 0, 1);
            float shake = Anim.sinr(a * 3.2f) * 4 * k;
            m.addRot("torso", 10 * k + shake, shake, Anim.sinr(a * 2.7f) * 3 * k);
            m.addRot("head", -14 * k, shake * 2, 0);
            m.addRot("armR", -20 * k, 0, 30 * k); m.addRot("armL", -20 * k, 0, -30 * k);
            for (int i = 0; i < 6; i++) m.addRot("spk" + i, 40 * (1 - k), 0, 0);
        } else if (c.is("spike_barrage")) {
            for (int i = 0; i < 6; i++) {
                float hit = 16 + i * 2;
                float st = Anim.curve(t, 0, 0, hit - 4, 0, hit, 1, hit + 6, 0, 46, 0);
                m.addRot("spk" + i, -14 * Anim.curve(t, 0, 0, 14, 1, 40, 1, 46, 0) + 110 * st, 0, -(i % 2 == 0 ? -1 : 1) * 26 * st);
                m.addRot("spkClaw" + i, -20 * st, 0, 0);
            }
            m.addRot("torso", Anim.curve(t, 0, 0, 14, -12, 20, 10, 46, 0), 0, 0);
            m.addRot("head", Anim.curve(t, 0, 0, 14, -12, 46, 0), 0, 0);
            m.addRot("armR", -40, 0, 20); m.addRot("armL", -40, 0, -20);
        } else if (c.is("spike_impale")) {
            float ld = Anim.curve(t, 0, 0, 16, 1, 20, 0, 42, 0);
            float th = Anim.curve(t, 0, 0, 16, 0, 19, 1, 32, 1, 42, 0);
            for (int i = 0; i < 6; i++) { m.addRot("spk" + i, -18 * ld + 118 * th, 0, (i % 2 == 0 ? 1 : -1) * 22 * th); m.addRot("spkClaw" + i, -30 * th, 0, 0); }
            m.addRot("torso", -16 * ld + 26 * th, 0, 0);
            m.addRot("head", 10 * th, 0, 0);
            m.addRot("legR", -24 * th, 0, 0); m.addRot("legL", 18 * th, 0, 0);
        } else if (c.is("claw_rake")) {
            m.addRot("torso", 8, Anim.curve(t, 0, 0, 10, 20, 16, -18, 22, 20, 36, 0), 0);
            float r = Anim.curve(t, 0, 0, 5, -110, 10, 55, 13, -110, 16, 55, 19, -110, 22, 55, 28, 0, 36, 0);
            m.addRot("armL", r, 0, 0);
            m.addRot("armR", 15, 0, 0);
            m.addRot("legR", -14, 0, 0); m.addRot("legL", 14, 0, 0);
        } else if (c.is("tail_whip")) {
            float st = Anim.curve(t, 0, 0, 10, 1, 26, 1, 38, 0);
            m.addRot("spin", 0, Anim.linear(t, 0, 0, 10, 0, 24, -340, 99, -340), 0);
            for (int i = 0; i < 7; i++) m.addRot("tail" + i, 0, 16 * st, 0);
            m.addRot("torso", 6 * st, 0, 0);
            for (int i = 0; i < 6; i++) m.addRot("spk" + i, 20 * st, 0, (i % 2 == 0 ? 1 : -1) * 20 * st);
        } else if (c.is("eruption")) {
            float up = Anim.curve(t, 0, 0, 16, 1, 18, 0, 46, 0);
            float sl = Anim.curve(t, 0, 0, 16, 0, 20, 1, 38, 1, 46, 0);
            m.addRot("torso", -20 * up + 30 * sl, 0, 0);
            m.addRot("armR", -120 * up + 160 * sl, 0, 0); m.addRot("armL", -120 * up + 160 * sl, 0, 0);
            for (int i = 0; i < 6; i++) m.addRot("spk" + i, -20 * up + 60 * sl, 0, 0);
        } else if (c.is("welcome_home")) {
            float up = Anim.curve(t, 0, 0, 16, 1, 54, 1, 58, 0);
            float sh = t > 16 && t < 54 ? 1 : 0;
            m.addRot("torso", -22 * up + Anim.sinr(a * 2.6f) * 2 * sh, 0, 0);
            m.addRot("head", -32 * up, Anim.sinr(a * 3f) * 4 * sh, 0);
            m.addRot("armR", -40 * up, 0, 80 * up); m.addRot("armL", -40 * up, 0, -80 * up);
            for (int i = 0; i < 6; i++) m.addRot("spk" + i, -20 * up + Anim.sinr(a * 0.5f + i) * 10 * sh, 0, (i % 2 == 0 ? 1 : -1) * 30 * up);
        }

        if (c.death > 0) {
            float d = Anim.easeOut(c.death);
            m.addRot("root", -86 * d, 0, 0);
            m.move("root", 0, -2 * d, 0);
            m.addRot("armR", 40 * d, 0, 25 * d); m.addRot("armL", 30 * d, 0, -25 * d);
        }
    }
}
