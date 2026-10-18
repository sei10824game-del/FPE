package com.fpe.client.spec;

import com.fpe.client.model.Anim;
import com.fpe.client.model.AnimCtx;
import com.fpe.client.model.ModelParts;
import com.fpe.client.model.ModelSpec;
import com.fpe.client.model.ModelSpec.Face;
import com.fpe.client.model.ModelSpec.Pattern;

/**
 * Danger AU Circle (canon per the Danger AU fanon wiki): tall muscular, very long spiky black hair, black horns (one with two white lines),
 * large yellow fleece scarf over neck and half the body, red glasses, gold tooth, bandaged right-ish forearm, clawed burnt paw, tall belted
 * combat boots, flamethrower replacing the left forearm, fuel tank on the back. No compass.
 */
public final class RedCircleSpec {
    private RedCircleSpec() {}

    static final int HAIR = 0x0E0D13, HAIR2 = 0x1C1A24, FACE = 0xE9E6EA, JACKET = 0x2E2C36, JACKET_D = 0x23212A, PANTS = 0x24222C, BOOT = 0x121116,
            BELT = 0xB89430, YEL = 0xE8B830, YEL_D = 0xC8941E, YEL_L = 0xF4D058, RED = 0xC01830, BAND = 0xDCD8CC, STEEL = 0x4A4C56, STEEL_D = 0x30323A,
            TANK = 0xA02828, GLOVE = 0x1A1920, CLAW = 0xE8E6EE, GOLD = 0xE8C030, WHITE = 0xF0F0F4;

    public static final ModelSpec SPEC = com.fpe.client.model.BbModel.load("red_circle", 0.8f);
    static final ModelSpec PROC = build();

    private static ModelSpec build() {
        ModelSpec m = new ModelSpec("red_circle").shadow(0.8f);
        m.group("root", null, 0, 24, 0);
        m.group("spin", "root", 0, 11, 0);

        // ---------------------------------------------------------------- legs: trousers + tall belted combat boots
        for (int s = -1; s <= 1; s += 2) {
            String k = s < 0 ? "R" : "L";
            float x = 2.3f * s;
            m.part("leg" + k, "spin", x, 11, 0, -2, 0, -2, 4, 7, 4, PANTS);
            m.part("shin" + k, "leg" + k, x, 18, 0, -2.2f, 0, -2.2f, 4.4f, 6, 4.4f, BOOT)
                    .decor(Face.FRONT, 0, 1, 4, 1, BELT).decor(Face.FRONT, 0, 3, 4, 1, BELT).decor(Face.RIGHT, 0, 1, 4, 1, BELT).decor(Face.LEFT, 0, 1, 4, 1, BELT);
            m.part("toe" + k, "shin" + k, x, 23, 0, -2.2f, -1.2f, -4.4f, 4.4f, 1.6f, 2.6f, BOOT);
        }

        // ---------------------------------------------------------------- torso, belt, scarf
        m.part("hips", "spin", 0, 11, 0, -4.4f, -2, -2.4f, 8.8f, 3, 4.8f, JACKET_D).decor(Face.FRONT, 0, 1, 9, 1, BELT).decor(Face.FRONT, 4, 1, 1, 1, GOLD);
        m.part("torso", "spin", 0, 11, 0, -4.8f, -12, -2.6f, 9.6f, 10, 5.2f, JACKET).decor(Face.FRONT, 4, 3, 1, 5, JACKET_D).decor(Face.BACK, 4, 0, 1, 10, JACKET_D);
        m.part("scarf", "torso", 0, -1, 0, -5.8f, -3, -3.6f, 11.6f, 5, 7.2f, YEL).pattern(Pattern.STRIPE_V, YEL_D, 1).grain(0.1f);
        m.part("scarfFlap", "scarf", 0, 2, -3.5f, -4.6f, 0, -0.4f, 9.2f, 9.5f, 1, YEL).pattern(Pattern.STRIPE_V, YEL_D, 2).grain(0.1f)
                .decor(Face.FRONT, 0, 8, 9, 1, YEL_L).decor(Face.FRONT, 1, 9, 1, 1, YEL_D).decor(Face.FRONT, 3, 9, 1, 1, YEL_D).decor(Face.FRONT, 5, 9, 1, 1, YEL_D).decor(Face.FRONT, 7, 9, 1, 1, YEL_D);
        m.part("scarfBack", "scarf", 0, 2, 3.4f, -4.8f, 0, -0.5f, 9.6f, 8, 1, YEL).pattern(Pattern.STRIPE_V, YEL_D, 2).grain(0.1f);
        m.part("tank", "torso", 0, -9, 3.2f, -2.4f, 0, 0, 4.8f, 9, 3.6f, TANK).decor(Face.BACK, 0, 2, 5, 1, BELT).decor(Face.BACK, 0, 6, 5, 1, BELT);
        m.part("tankCap", "tank", 0, -9.6f, 4.4f, -1, -1, -0.2f, 2, 1, 2, STEEL);

        // ---------------------------------------------------------------- head: grin with gold tooth, red glasses
        m.part("head", "torso", 0, -3, 0, -3.6f, -7.4f, -3.6f, 7.2f, 7.4f, 7.2f, FACE)
                .decor(Face.FRONT, 0, 3, 7, 1, RED).decorGlow(Face.FRONT, 1, 3, 2, 1, 0xFF5030).decorGlow(Face.FRONT, 4, 3, 2, 1, 0xFF5030)
                .decor(Face.FRONT, 0, 5, 7, 2, 0x16121A).decor(Face.FRONT, 0, 5, 1, 1, WHITE).decor(Face.FRONT, 2, 5, 1, 1, WHITE).decor(Face.FRONT, 4, 5, 1, 1, WHITE)
                .decor(Face.FRONT, 6, 5, 1, 1, WHITE).decor(Face.FRONT, 1, 6, 1, 1, WHITE).decor(Face.FRONT, 5, 6, 1, 1, WHITE).decor(Face.FRONT, 3, 6, 1, 1, GOLD)
                .decor(Face.RIGHT, 0, 3, 7, 1, RED).decor(Face.LEFT, 0, 3, 7, 1, RED);
        m.part("hairTop", "head", 0, -7.4f, 0, -4, -1.4f, -4, 8, 2, 8, HAIR).decor(Face.FRONT, 0, 0, 8, 1, HAIR2);
        m.part("fringe", "head", 0, -6.2f, -3.8f, -3.8f, 0, -0.4f, 7.6f, 1.6f, 0.8f, HAIR);
        m.part("hairBack", "head", 0, -7, 3.2f, -4.2f, 0, 0, 8.4f, 18, 3, HAIR).pattern(Pattern.STRIPE_V, HAIR2, 3).grain(0.02f);
        m.part("hairSideR", "head", -3.8f, -5.5f, 0, -1.4f, 0, -3.5f, 1.6f, 14, 7, HAIR);
        m.part("hairSideL", "head", 3.8f, -5.5f, 0, -0.2f, 0, -3.5f, 1.6f, 14, 7, HAIR);
        for (int i = 0; i < 9; i++) {   // jagged long spikes
            float x = -3.6f + i * 0.9f, len = 5 + (i % 3) * 2.5f;
            m.part("hairSpk" + i, "hairBack", x, 10 + i % 2, 4.5f, -0.9f, 0, -0.5f, 1.8f, len, 1.2f, i % 2 == 0 ? HAIR : HAIR2).rot(8 + i % 3 * 4, 0, (i - 4) * 5);
        }
        m.part("hornR", "head", -2.6f, -8.6f, -0.6f, -1, -6, -1, 2, 6, 2, HAIR2).pattern(Pattern.STRIPE_H, WHITE, 4).rot(-8, 0, -22);
        m.part("hornTipR", "hornR", -2.6f, -14.4f, -0.6f, -0.6f, -3, -0.6f, 1.2f, 3, 1.2f, HAIR2).rot(0, 0, -16);
        m.part("hornL", "head", 2.6f, -8.6f, -0.6f, -1, -6, -1, 2, 6, 2, HAIR2).rot(-8, 0, 22);
        m.part("hornTipL", "hornL", 2.6f, -14.4f, -0.6f, -0.6f, -3, -0.6f, 1.2f, 3, 1.2f, HAIR2).rot(0, 0, 16);

        // ---------------------------------------------------------------- arms: right = bandaged, burnt clawed paw; left = flamethrower
        m.part("armR", "torso", -6.8f, -10.5f, 0, -2.2f, -1, -2.2f, 4.4f, 8, 4.4f, JACKET).decor(Face.FRONT, 0, 6, 4, 2, JACKET_D);
        m.part("foreR", "armR", -6.8f, -2.5f, 0, -2, 0, -2, 4, 7, 4, BAND).pattern(Pattern.STRIPE_H, 0xB4B0A0, 1).decor(Face.FRONT, 1, 3, 2, 2, 0x8A1A1A);
        m.part("handR", "foreR", -6.8f, 4.5f, 0, -2.2f, 0, -2.2f, 4.4f, 3.2f, 4.4f, GLOVE);
        for (int i = -1; i <= 1; i++) m.part("clawR" + (i + 1), "handR", -6.8f + i * 1.4f, 7.7f, -1.4f, -0.4f, 0, -0.4f, 0.8f, 3.6f, 0.8f, CLAW).rot(-10, 0, i * 6);
        m.part("armL", "torso", 6.8f, -10.5f, 0, -2.2f, -1, -2.2f, 4.4f, 8, 4.4f, JACKET).decor(Face.FRONT, 0, 6, 4, 2, JACKET_D);
        m.part("foreL", "armL", 6.8f, -2.5f, 0, -2.4f, 0, -2.4f, 4.8f, 7, 4.8f, STEEL).decor(Face.FRONT, 0, 1, 5, 1, BELT).decor(Face.FRONT, 0, 5, 5, 1, BELT).decor(Face.RIGHT, 1, 2, 3, 3, STEEL_D);
        m.part("nozzle", "foreL", 6.8f, 4.5f, 0, -1.4f, 0, -1.4f, 2.8f, 4, 2.8f, STEEL_D);
        m.part("nozzleTip", "nozzle", 6.8f, 8.5f, 0, -1, 0, -1, 2, 1.4f, 2, 0xFF7A20).glow();
        m.part("pilot", "foreL", 6.8f, 3, 0, -0.5f, 0, -3.4f, 1, 1, 1, 0xFFD040).glow();
        m.part("hose", "tank", 3.4f, -4, 4, -0.5f, 0, -0.5f, 1, 10, 1, STEEL_D).rot(0, 0, -12);

        m.animator(RedCircleSpec::animate);
        return m;
    }

    private static float sgn(String k) { return k.equals("R") ? -1f : 1f; }

    private static void animate(ModelParts m, AnimCtx c) {
        float a = c.age, t = c.t, w = c.walk(), ls = c.limbSwing;

        // idle + walk (heavy confident stride)
        for (String k : new String[] {"R", "L"}) {
            float ph = k.equals("R") ? 0 : 3.14159f, sw = Anim.sinr(ls * 0.6f + ph) * w;
            m.addRot("leg" + k, sw * 36, 0, 0);
            m.addRot("shin" + k, Math.max(0, -sw) * 30, 0, 0);
            m.addRot("arm" + k, -sw * 26 + Anim.sinr(a * 0.07f + ph) * 2.5f, 0, sgn(k) * -3);
        }
        m.addRot("torso", Anim.sinr(a * 0.08f) * 1.5f, Anim.sinr(ls * 0.6f) * 6 * w, 0);
        m.addRot("head", 0, Math.max(-40, Math.min(40, c.headYaw)) * 0.7f, 0);
        m.addRot("hairBack", 4 + Anim.sinr(a * 0.06f) * 2 + w * 8, 0, 0);
        for (int i = 0; i < 9; i++) m.addRot("hairSpk" + i, Anim.sinr(a * 0.1f + i * 0.7f) * 5 + w * 10, 0, 0);
        m.addRot("scarfFlap", Anim.sinr(a * 0.09f) * 3 + w * 8, 0, 0);
        m.addRot("scarfBack", Anim.sinr(a * 0.09f + 1) * 3 + w * 10, 0, 0);
        m.move("spin", 0, Anim.sinr(ls * 1.2f) * 0.5f * w, 0);

        if (c.is("flame_stream")) {
            float up = Anim.curve(t, 0, 0, 12, 1, 48, 1, 58, 0);
            float sweep = t > 14 && t < 48 ? Anim.sinr((t - 14) * 0.2f) : 0;
            m.addRot("torso", -8 * up, 20 * sweep, 0);
            m.addRot("head", 0, -10 * sweep, 0);
            m.addRot("armL", -78 * up, 0, 0);
            m.addRot("foreL", -12 * up, 0, 0);
            m.addRot("armR", -30 * up, 0, 14 * up);
            m.addRot("legR", 14 * up, 0, 0); m.addRot("legL", -12 * up, 0, 0);
        } else if (c.is("fireball")) {
            float aim = Anim.curve(t, 0, 0, 10, 1, 17, 0.6f, 34, 0);
            float kick = t > 15 && t < 22 ? Anim.curve(t, 15, 1, 22, 0) : 0;
            m.addRot("torso", -10 * aim - 8 * kick, 0, 0);
            m.addRot("armL", -86 * aim + 14 * kick, 0, 0);
            m.addRot("armR", -20 * aim, 0, 0);
            m.addRot("legR", 16 * aim, 0, 0);
        } else if (c.is("flame_burst")) {
            float crouch = Anim.curve(t, 0, 0, 14, 1, 17, 0, 40, 0);
            float open = Anim.curve(t, 0, 0, 14, 0, 18, 1, 32, 1, 40, 0);
            m.move("spin", 0, 4 * crouch, 0);
            m.addRot("torso", 18 * crouch - 10 * open, 0, 0);
            m.addRot("legR", -26 * crouch, 0, 0); m.addRot("legL", -26 * crouch, 0, 0);
            m.addRot("shinR", 40 * crouch, 0, 0); m.addRot("shinL", 40 * crouch, 0, 0);
            m.addRot("armR", -25 * crouch - 40 * open, 0, 70 * open);
            m.addRot("armL", -25 * crouch - 40 * open, 0, -70 * open);
            m.addRot("head", -16 * open, 0, 0);
        } else if (c.is("claw")) {
            m.addRot("torso", 8, Anim.curve(t, 0, 0, 9, -26, 17, 26, 30, 0), 0);
            float r = Anim.curve(t, 0, 0, 4, -100, 9, 50, 12, 0, 12.5f, -100, 17, 50, 22, 0, 30, 0);
            m.addRot("armR", r, 0, 0); m.addRot("foreR", -r * 0.3f, 0, 0);
            m.addRot("armL", 15, 0, 0);
            m.addRot("legR", -14, 0, 0); m.addRot("legL", 14, 0, 0);
        } else if (c.is("hair_whip")) {
            float st = Anim.curve(t, 0, 0, 8, 1, 24, 1, 32, 0);
            m.addRot("spin", 0, Anim.linear(t, 0, 0, 10, 0, 22, -420, 99, -420), 0);
            m.addRot("torso", 6 * st, 0, 0);
            m.addRot("hairBack", 40 * st, 0, 0);
            for (int i = 0; i < 9; i++) m.addRot("hairSpk" + i, 25 * st, 0, (i - 4) * 9 * st);
            m.addRot("armR", -60 * st, 0, 60 * st); m.addRot("armL", -60 * st, 0, -60 * st);
        } else if (c.is("bike_charge")) {
            float rev = Anim.curve(t, 0, 0, 6, 1, 18, 1, 20, 0, 52, 0);
            float run = t >= 20 && t <= 38 ? 1 : 0;
            m.move("spin", 0, 3 * rev, 0);
            m.addRot("torso", 14 * rev + 26 * run, Anim.sinr(a * 3f) * 3 * rev, 0);
            m.addRot("armL", -30 * rev - 80 * run, 0, 0);
            m.addRot("armR", -30 * rev - 80 * run, 0, 0);
            m.addRot("legR", -22 * rev, 0, 0); m.addRot("legL", -22 * rev, 0, 0);
            m.addRot("shinR", 34 * rev, 0, 0); m.addRot("shinL", 34 * rev, 0, 0);
            m.addRot("head", -12 * run, 0, 0);
            m.addRot("hairBack", 40 * run, 0, 0);
        } else if (c.is("molotov")) {
            float wind = Anim.curve(t, 0, 0, 12, 1, 14, 0, 46, 0);
            float thr = Anim.curve(t, 0, 0, 12, 0, 15, 1, 24, 0, 46, 0);
            m.addRot("torso", -16 * wind + 22 * thr, Anim.curve(t, 0, 0, 12, 18, 15, -18, 46, 0), 0);
            m.addRot("armR", -140 * wind + 170 * thr, 0, 0);
            m.addRot("armL", -20 * wind, 0, 0);
            m.addRot("legR", 18 * thr - 10 * wind, 0, 0);
        } else if (c.is("inferno")) {
            float up = Anim.curve(t, 0, 0, 18, 1, 66, 1, 74, 0);
            float sh = t > 18 && t < 66 ? 1 : 0;
            m.addRot("torso", -22 * up + Anim.sinr(a * 2.5f) * 2 * sh, 0, 0);
            m.addRot("head", -30 * up, 0, 0);
            m.addRot("armR", -40 * up, 0, 80 * up);
            m.addRot("armL", -40 * up, 0, -80 * up);
            m.addRot("hairBack", 30 * up, 0, 0);
            for (int i = 0; i < 9; i++) m.addRot("hairSpk" + i, 20 * up + Anim.sinr(a * 0.6f + i) * 10 * sh, 0, (i - 4) * 6 * up);
            m.addRot("scarfFlap", 22 * up, 0, 0);
            m.move("spin", 0, Anim.sinr(a * 3f) * 0.4f * sh, 0);
        }

        if (c.death > 0) {
            float d = Anim.easeOut(c.death);
            m.addRot("root", -86 * d, 0, 0);
            m.move("root", 0, -2 * d, 0);
            m.addRot("armR", 40 * d, 0, 20 * d); m.addRot("armL", 30 * d, 0, -20 * d);
        }
    }
}
