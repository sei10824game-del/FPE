package com.fpe.client.spec;

import static com.fpe.client.model.Anim.curve;
import static com.fpe.client.model.Anim.linear;

import com.fpe.client.model.Anim;
import com.fpe.client.model.AnimCtx;
import com.fpe.client.model.ModelParts;
import com.fpe.client.model.ModelSpec;
import com.fpe.client.model.ModelSpec.Face;
import com.fpe.client.model.ModelSpec.Pattern;

/**
 * Miss Circle (pyromaniac AU): tall teacher, wolf-eared wide hat with orange band, huge purple hair cloak,
 * white grinning face, orange fringed poncho, bandaged right arm, orange trousers, strapped boots,
 * thigh-holstered flamethrower and a GIANT drawing compass in her right hand.
 */
public final class MissCircleSpec {
    private MissCircleSpec() {}

    // palette
    static final int HAIR = 0x3E2C5A, HAIR_D = 0x281C3E, HAIR_L = 0x5C4680;
    static final int SKIN = 0xEFE9DF, SHIRT = 0x241C2E, SHIRT_L = 0x342A42;
    static final int ORANGE = 0xF0A040, ORANGE_D = 0xD07A28, PANTS = 0xE88A2E, PANTS_D = 0xB8661E;
    static final int BOOT = 0x2A2430, BOOT_L = 0x3C3444, STRAP = 0x7A4E2A, GLOVE = 0x16121C;
    static final int HAT = 0x2C2240, HAT_L = 0x3E3258, BAND = 0xE8902E;
    static final int STEEL = 0xD4D6DE, STEEL_D = 0x8A8C98, DARK = 0x150E1C, TOOTH = 0xFAF7EE;
    static final int GUN = 0x5A5A64, TANK = 0xB8361C, FLAME = 0xFFA830;

    /** the live model now comes from Blockbench (assets/fpe/bbmodels/miss_circle.bbmodel); PROC is the old procedural original kept for reference. */
    public static final ModelSpec SPEC = com.fpe.client.model.BbModel.load("miss_circle", 0.7f);
    static final ModelSpec PROC = build();

    private static ModelSpec build() {
        ModelSpec m = new ModelSpec("miss_circle");
        m.shadow(0.7f);
        m.group("root", null, 0, 24, 0);
        m.group("pelvis", "root", 0, 9, 0);

        // ---------------------------------------------------------------- legs (hip y=9, knee y=17, ground 24)
        for (int s = -1; s <= 1; s += 2) {
            String S = s < 0 ? "R" : "L";
            float x = 2.1f * s;
            m.part("leg" + S, "pelvis", x, 9, 0, -2, 0, -2, 4, 8, 4, PANTS).inflate(0.3f)
                    .decor(Face.FRONT, s < 0 ? 1 : 2, 1, 1, 6, PANTS_D).decor(Face.FRONT, 0, 7, 4, 1, PANTS_D);
            m.part("shin" + S, "leg" + S, x, 17, 0, -2, 0, -2, 4, 2.5f, 4, PANTS).inflate(0.25f);
            m.part("boot" + S, "shin" + S, x, 17, 0, -2.2f, 2, -2.2f, 4.4f, 5.5f, 4.4f, BOOT)
                    .decor(Face.FRONT, 0, 1, 5, 1, STRAP).decor(Face.FRONT, 0, 3, 5, 1, STRAP).decor(Face.FRONT, 2, 1, 1, 1, 0xC8A040)
                    .decor(Face.LEFT, 0, 1, 5, 1, STRAP).decor(Face.RIGHT, 0, 1, 5, 1, STRAP).decor(Face.LEFT, 0, 3, 5, 1, STRAP).decor(Face.RIGHT, 0, 3, 5, 1, STRAP);
            m.part("bootTop" + S, "boot" + S, x, 17, 0, -2.5f, 1.4f, -2.5f, 5, 1.2f, 5, BOOT_L);
            m.part("toe" + S, "boot" + S, x, 17, 0, -2.1f, 5.6f, -4.2f, 4.2f, 1.4f, 2.4f, BOOT);
        }
        // thigh holster straps + holstered flamethrower on the left thigh
        m.part("strapL1", "legL", 2.1f, 9, 0, -2.4f, 2.5f, -2.4f, 4.8f, 1, 4.8f, STRAP);
        m.part("strapL2", "legL", 2.1f, 9, 0, -2.4f, 5.5f, -2.4f, 4.8f, 1, 4.8f, STRAP);
        m.part("strapR1", "legR", -2.1f, 9, 0, -2.4f, 4f, -2.4f, 4.8f, 1, 4.8f, STRAP);
        flamer(m, "hol", "legL", 4.9f, 10.5f, 0.6f);

        // ---------------------------------------------------------------- torso
        m.part("body", "pelvis", 0, 9, 0, -4, -11, -2, 8, 11, 4, SHIRT).decor(Face.FRONT, 3, 3, 2, 5, SHIRT_L);
        m.part("belt", "body", 0, 9, 0, -4.3f, -1.6f, -2.3f, 8.6f, 1.6f, 4.6f, 0x4A3020).decor(Face.FRONT, 4, 0, 2, 2, 0xC8A040);
        m.part("poncho", "body", 0, -2.2f, 0, -5.2f, 0, -3.2f, 10.4f, 6.5f, 6.4f, ORANGE).pattern(Pattern.GRADIENT_V, ORANGE_D, 1)
                .decor(Face.FRONT, 4, 0, 3, 1, ORANGE_D).decor(Face.FRONT, 0, 6, 11, 1, 0xB86420);
        m.part("fringe", "poncho", 0, 4.3f, 0, -5.4f, 0, -3.4f, 10.8f, 2.8f, 6.8f, ORANGE).pattern(Pattern.STRIPE_V, SHIRT, 1);
        m.part("scarf", "body", 0, -2, 0, -3.2f, -2.2f, -3f, 6.4f, 2.8f, 6, ORANGE_D).decor(Face.FRONT, 0, 1, 7, 1, 0xB86420);

        // ---------------------------------------------------------------- head, face, hat
        m.part("head", "body", 0, -2, 0, -4, -8, -4, 8, 8, 8, SKIN)
                .decor(Face.FRONT, 0, 0, 8, 2, 0x2C2238).decor(Face.FRONT, 0, 2, 8, 1, 0xB8B0B8)
                // huge sharp grin
                .decor(Face.FRONT, 0, 4, 8, 3, DARK).decor(Face.FRONT, 0, 3, 1, 1, DARK).decor(Face.FRONT, 7, 3, 1, 1, DARK)
                .decor(Face.FRONT, 0, 4, 1, 1, TOOTH).decor(Face.FRONT, 2, 4, 1, 1, TOOTH).decor(Face.FRONT, 4, 4, 1, 1, TOOTH).decor(Face.FRONT, 6, 4, 1, 1, TOOTH)
                .decor(Face.FRONT, 1, 6, 1, 1, TOOTH).decor(Face.FRONT, 3, 6, 1, 1, TOOTH).decor(Face.FRONT, 5, 6, 1, 1, TOOTH).decor(Face.FRONT, 7, 6, 1, 1, TOOTH)
                .decor(Face.FRONT, 1, 5, 6, 1, 0x7A1424);
        m.part("eyeR", "head", -2, -2, 0, -1.4f, -5.7f, -4.15f, 2, 0.8f, 0.3f, FLAME).glow();
        m.part("eyeL", "head", 2, -2, 0, -0.6f, -5.7f, -4.15f, 2, 0.8f, 0.3f, FLAME).glow();
        m.part("hairTop", "head", 0, -2, 0, -4.5f, -8.4f, -1.5f, 9, 8.5f, 6, HAIR).pattern(Pattern.GRADIENT_V, HAIR_D, 1);
        m.part("bangs", "head", 0, -2, 0, -4.4f, -8.3f, -4.4f, 8.8f, 1.6f, 3, HAIR_D);
        for (int s = -1; s <= 1; s += 2) {
            String S = s < 0 ? "R" : "L";
            m.part("hairSide" + S, "head", 4.2f * s, -8, -1, s < 0 ? -1.6f : -0.4f, 0, -3.2f, 2, 12, 5.5f, HAIR)
                    .pattern(Pattern.GRADIENT_V, HAIR_D, 1).decor(Face.FRONT, 0, 2, 1, 8, HAIR_L).rot(0, 0, 6 * -s);
            m.part("hairSideTip" + S, "hairSide" + S, 4.2f * s, 4, -1, s < 0 ? -1.4f : -0.2f, 0, -2.6f, 1.6f, 5, 4, HAIR_D).rot(0, 0, 10 * -s);
        }
        m.part("hatBrim", "head", 0, -9.3f, 0, -6.5f, -0.5f, -6.5f, 13, 1, 13, HAT).rot(9, 0, 0)
                .decor(Face.TOP, 0, 0, 13, 1, HAT_L).decor(Face.BOTTOM, 1, 1, 11, 11, 0x1C1428);
        m.part("hatCrown", "hatBrim", 0, -9.3f, 0, -4.5f, -4.2f, -4.5f, 9, 4, 9, HAT).pattern(Pattern.GRADIENT_V, HAT_L, 1);
        m.part("hatBand", "hatBrim", 0, -9.3f, 0, -4.7f, -1.8f, -4.7f, 9.4f, 1.6f, 9.4f, BAND).decor(Face.FRONT, 0, 0, 10, 1, 0xFFB850);
        m.part("hatBandFront", "hatBrim", 0, -9.3f, 0, -3.5f, -0.6f, -6.6f, 7, 1.2f, 1, BAND).decor(Face.FRONT, 0, 0, 7, 1, 0xFFB850);
        for (int s = -1; s <= 1; s += 2) {
            String S = s < 0 ? "R" : "L";
            m.part("ear" + S, "hatCrown", 2.7f * s, -13.3f, 0, -2.2f, -3.6f, -1, 4.4f, 3.8f, 2, HAT).rot(-6, 0, 14 * s)
                    .decor(Face.FRONT, 1, 1, 1, 3, HAIR_L);
            m.part("earTip" + S, "ear" + S, 2.7f * s, -13.3f, 0, -1.4f, -6.2f, -0.7f, 2.8f, 2.8f, 1.4f, HAT);
            m.part("earPt" + S, "ear" + S, 2.7f * s, -13.3f, 0, -0.6f, -8.2f, -0.5f, 1.2f, 2.2f, 1, HAT);
        }

        // ---------------------------------------------------------------- hair cloak (follows body, chained for secondary motion)
        m.part("hairC1", "body", 0, -9, 3, -6, 0, -0.5f, 12, 11, 3, HAIR).pattern(Pattern.GRADIENT_V, HAIR_D, 1)
                .decor(Face.BACK, 2, 1, 1, 9, HAIR_L).decor(Face.BACK, 8, 2, 1, 8, HAIR_L);
        m.part("hairC2", "hairC1", 0, 2, 3, -7, 0, -0.5f, 14, 11, 3, HAIR).pattern(Pattern.GRADIENT_V, HAIR_D, 1)
                .decor(Face.BACK, 4, 0, 1, 10, HAIR_L).decor(Face.BACK, 10, 1, 1, 8, HAIR_L);
        m.part("hairC3", "hairC2", 0, 13, 3, -8, 0, -0.5f, 16, 8.5f, 3, HAIR_D).pattern(Pattern.GRADIENT_V, 0x1C1430, 1)
                .decor(Face.BACK, 0, 7, 2, 2, 0x1C1430).decor(Face.BACK, 5, 7, 2, 2, 0x1C1430).decor(Face.BACK, 11, 7, 2, 2, 0x1C1430);
        for (int i = 0; i < 4; i++) {
            float x = -6 + i * 4;
            m.part("hairTip" + i, "hairC3", x, 21.5f, 3, -1.2f, 0, -0.4f, 2.4f, 3, 2.4f, HAIR_D).rot(0, 0, (i - 1.5f) * 14);
        }
        for (int s = -1; s <= 1; s += 2) {
            String S = s < 0 ? "R" : "L";
            m.part("hairW" + S, "hairC1", 5.2f * s, -8, 2.5f, s < 0 ? -4.5f : 0, 0, -2, 4.5f, 15, 4, HAIR).pattern(Pattern.GRADIENT_V, HAIR_D, 1)
                    .decor(Face.FRONT, 1, 2, 1, 10, HAIR_L).decor(Face.FRONT, 3, 4, 1, 9, HAIR_L).rot(0, 0, -9 * s);
            m.part("hairW2" + S, "hairW" + S, 5.2f * s + (s < 0 ? -2.2f : 2.2f), 7, 2.5f, -2.6f, 0, -1.6f, 5.2f, 11, 3.4f, HAIR_D).pattern(Pattern.GRADIENT_V, 0x1C1430, 1).rot(0, 0, -6 * s);
            m.part("hairW3" + S, "hairW2" + S, 5.2f * s + (s < 0 ? -2.2f : 2.2f), 18, 2.5f, -1.6f, 0, -1, 3.2f, 4, 2.4f, 0x1C1430).rot(0, 0, -16 * s);
        }

        // ---------------------------------------------------------------- arms (shoulder y=-1, elbow 6.5, wrist 12.5)
        for (int s = -1; s <= 1; s += 2) {
            String S = s < 0 ? "R" : "L";
            float x = 5.6f * s;
            m.part("arm" + S, "body", 5 * s, -1, 0, s < 0 ? -2.6f : -0.4f, -1, -1.5f, 3, 7.5f, 3, SHIRT);
            m.part("shoulder" + S, "arm" + S, 5 * s, -1, 0, s < 0 ? -3.2f : -0.8f, -1.8f, -2.1f, 4, 3.4f, 4.2f, ORANGE)
                    .pattern(Pattern.GRADIENT_V, ORANGE_D, 1).decor(Face.FRONT, 0, 3, 4, 1, SHIRT);
            m.part("fore" + S, "arm" + S, x, 6.5f, 0, -1.5f, 0, -1.5f, 3, 6, 3, s < 0 ? 0xEDE6DA : SHIRT)
                    .pattern(s < 0 ? Pattern.STRIPE_H : Pattern.SOLID, 0xB9B0A4, 1);
            m.part("cuff" + S, "fore" + S, x, 6.5f, 0, -1.8f, 3.5f, -1.8f, 3.6f, 2.5f, 3.6f, GLOVE).decor(Face.FRONT, 0, 0, 4, 1, s < 0 ? 0xEDE6DA : BAND);
            m.part("hand" + S, "fore" + S, x, 12.5f, 0, -1.7f, 0, -1.7f, 3.4f, 3, 3.4f, GLOVE);
            for (int i = 0; i < 3; i++)
                m.part("claw" + S + i, "hand" + S, x, 12.5f, 0, -1.5f + i * 1.15f, 2.6f, -1.6f, 0.7f, 2.4f, 0.7f, 0x0A0810).rot(-12, 0, 0);
        }
        // bandage tail fluttering from the right forearm
        m.part("bandTail", "foreR", -7.1f, 9, 0, -0.2f, 0, -0.4f, 0.4f, 4, 0.8f, 0xEDE6DA).rot(10, 0, 20);

        // ---------------------------------------------------------------- GIANT drawing compass (right hand)
        m.group("comp", "handR", -5.6f, 14, 0);
        m.part("cKnob", "comp", -5.6f, 14, 0, -0.7f, -4.2f, -0.7f, 1.4f, 2.6f, 1.4f, STEEL_D);
        m.part("cHead", "comp", -5.6f, 14, 0, -1.5f, -1.6f, -1.5f, 3, 3.4f, 3, STEEL)
                .decor(Face.FRONT, 1, 1, 1, 1, 0x3A3A44).decor(Face.BACK, 1, 1, 1, 1, 0x3A3A44);
        m.part("cLegA", "comp", -5.6f, 15.8f, 0, -0.6f, 0, -0.6f, 1.2f, 20, 1.2f, STEEL).decor(Face.FRONT, 0, 5, 2, 1, STEEL_D);
        m.part("cNeedle", "cLegA", -5.6f, 15.8f, 0, -0.3f, 20, -0.3f, 0.6f, 4, 0.6f, 0x6E6E78);
        m.part("cLegB", "comp", -5.6f, 15.8f, 0, -0.6f, 0, -0.6f, 1.2f, 15, 1.2f, STEEL).decor(Face.FRONT, 0, 5, 2, 1, STEEL_D);
        m.part("cClamp", "cLegB", -5.6f, 15.8f, 0, -1, 13, -1, 2, 2.4f, 2, 0x3A3A44);
        m.part("cPencil", "cLegB", -5.6f, 15.8f, 0, -0.75f, 15, -0.75f, 1.5f, 5.5f, 1.5f, 0xE8C040).decor(Face.FRONT, 0, 0, 2, 1, 0xC09020);
        m.part("cLead", "cLegB", -5.6f, 15.8f, 0, -0.4f, 20.5f, -0.4f, 0.8f, 2.2f, 0.8f, 0x2A2A30);

        // flamethrower in the left hand (hidden unless drawn)
        flamer(m, "gun", "handL", 5.6f, 14, -0.2f);

        m.animator(MissCircleSpec::animate);
        return m;
    }

    /** flamethrower prop, built along +y from the grip (pointing down when the holding limb hangs). */
    private static void flamer(ModelSpec m, String p, String parent, float x, float y, float z) {
        m.group(p, parent, x, y, z);
        m.part(p + "Grip", p, x, y, z, -0.6f, -2.6f, -0.6f, 1.2f, 2.4f, 1.6f, 0x2A2A30);
        m.part(p + "Body", p, x, y, z, -0.9f, -0.4f, -0.9f, 1.8f, 9, 1.8f, GUN).decor(Face.FRONT, 0, 2, 2, 1, 0x88888F).decor(Face.FRONT, 0, 6, 2, 1, 0x88888F);
        m.part(p + "Tank", p, x, y, z, -1.2f, 0.6f, -2.9f, 2.4f, 5, 2, TANK).decor(Face.FRONT, 0, 1, 3, 1, 0xF0C040).decor(Face.FRONT, 0, 3, 3, 1, 0x6A1A0E);
        m.part(p + "Nozzle", p, x, y, z, -0.6f, 8.4f, -0.6f, 1.2f, 3, 1.2f, 0x2A2A30);
        m.part(p + "Pilot", p, x, y, z, -0.45f, 11.3f, -0.45f, 0.9f, 1.1f, 0.9f, FLAME).glow();
    }

    // =====================================================================================================
    // animation
    // =====================================================================================================

    /** full-body pose; all angles in degrees, offsets in model pixels */
    static final class P {
        float rootX, rootY, rootZ, rootDy, rootDz, drop, pelvisX;
        float bodyX, bodyY, bodyZ, headX, headY, headZ;
        float armRx, armRy, armRz, foreR, armLx, armLy, armLz, foreL, handL;
        float compX, compY, compZ, spread = 14;
        float legRx, legRz, legLx, legLz, shinR, shinL;
        float hairX, hairZ, fringeX, hatX;
        boolean compHidden, gunOut;
    }

    private static void base(P p, AnimCtx c, float age) {
        float br = Anim.sinr(age * 0.09f);
        float w = c.walk(), ph = c.limbSwing * 0.6662f;
        p.bodyX = 5 + br * 1.2f + 10 * w;
        p.headX = c.headPitch - 6 - br;
        p.headY = c.headYaw;
        p.headZ = Anim.sinr(age * 0.045f) * 4;
        p.armRx = -14 + br * 2 + Anim.cos((float) Math.toDegrees(ph)) * 8 * w;
        p.armRz = 9;
        p.foreR = -14;
        p.compX = -42 + Anim.sinr(ph * 2) * 4 * w;
        p.armLx = 4 - br * 2 - Anim.cos((float) Math.toDegrees(ph)) * 26 * w;
        p.armLz = -7 - br * 2;
        p.foreL = -22 - 12 * w;
        p.handL = 10;
        p.legRx = Anim.cos((float) Math.toDegrees(ph)) * 34 * w;
        p.legLx = -Anim.cos((float) Math.toDegrees(ph)) * 34 * w;
        p.shinR = (14 + 18 * Anim.sinr(ph)) * w;
        p.shinL = (14 - 18 * Anim.sinr(ph)) * w;
        p.bodyY = Anim.cos((float) Math.toDegrees(ph)) * 7 * w;
        p.rootDy = -Math.abs(Anim.sinr(ph)) * 1.0f * w;
        p.hairX = 3 + Anim.sinr(age * 0.07f) * 2 + 16 * w;
        p.hairZ = Anim.sinr(age * 0.05f) * 2;
        p.fringeX = Anim.sinr(age * 0.08f) * 3 + 12 * w + Anim.sinr(ph * 2) * 6 * w;
    }

    static P pose(AnimCtx c, float t, float age) {
        P p = new P();
        base(p, c, age);
        if (c.death > 0) { death(p, c.death); return p; }
        switch (c.ability) {
            case "sweep" -> sweep(p, t);
            case "lunge" -> lunge(p, t);
            case "splitSlam" -> splitSlam(p, t);
            case "compassThrow" -> compassThrow(p, t);
            case "drawCircle" -> drawCircle(p, t);
            case "flame" -> flame(p, t);
            case "fireball" -> fireball(p, t);
            case "charge" -> charge(p, t);
            case "hairWhip" -> hairWhip(p, t);
            case "combo" -> combo(p, t);
            case "inferno" -> inferno(p, t);
            default -> { }
        }
        return p;
    }

    // ---- 360° compass sweep: wind to the right, full spin, recover
    private static void sweep(P p, float t) {
        p.drop = curve(t, 0, 0, 10, 4, 20, 3, 34, 0);
        p.rootY = linear(t, 0, 0, 11, 70, 13, 40, 19, -290, 24, -345, 34, -360);
        p.bodyY = curve(t, 0, 0, 11, 25, 15, -10, 34, 0);
        p.bodyX = curve(t, 0, 5, 11, 22, 16, 14, 34, 5);
        p.armRx = curve(t, 0, -14, 10, -20, 14, -8, 26, -10, 34, -14);
        p.armRz = curve(t, 0, 9, 10, 70, 13, 88, 24, 82, 34, 9);
        p.armRy = curve(t, 0, 0, 10, 30, 15, -10, 34, 0);
        p.foreR = curve(t, 0, -14, 10, -40, 13, 0, 26, -5, 34, -14);
        p.compX = curve(t, 0, -42, 10, -10, 13, 0, 26, 0, 34, -42);
        p.spread = curve(t, 0, 14, 12, 2, 24, 2, 34, 14);
        p.armLx = curve(t, 0, 4, 10, -50, 16, -30, 34, 4);
        p.armLz = curve(t, 0, -7, 10, -35, 16, -60, 34, -7);
        p.legRx = curve(t, 0, 0, 10, 22, 20, 15, 34, 0);
        p.legLx = curve(t, 0, 0, 10, -30, 20, -20, 34, 0);
        p.shinL = curve(t, 0, 0, 10, 30, 20, 20, 34, 0);
        p.headX = curve(t, 0, -6, 10, 6, 34, -6);
        p.headY = curve(t, 0, 0, 11, -25, 15, 10, 34, 0);
    }

    // ---- long lunging stab
    private static void lunge(P p, float t) {
        p.drop = curve(t, 0, 0, 9, 3, 12, 5, 18, 5, 30, 0);
        p.rootDz = curve(t, 0, 0, 9, 2, 12, -5, 18, -5, 30, 0);
        p.bodyY = curve(t, 0, 0, 9, 40, 12, -20, 18, -18, 30, 0);
        p.bodyX = curve(t, 0, 5, 9, -6, 12, 30, 18, 28, 30, 5);
        p.armRx = curve(t, 0, -14, 9, 30, 11, -118, 18, -115, 30, -14);
        p.armRz = curve(t, 0, 9, 9, 22, 11, 2, 30, 9);
        p.foreR = curve(t, 0, -14, 9, -95, 11, 0, 18, 0, 30, -14);
        p.compX = curve(t, 0, -42, 9, -10, 11, 0, 18, 0, 30, -42);
        p.spread = curve(t, 0, 14, 9, 0, 22, 0, 30, 14);
        p.armLx = curve(t, 0, 4, 9, -40, 12, 30, 22, 25, 30, 4);
        p.armLz = curve(t, 0, -7, 9, -20, 12, -40, 30, -7);
        p.legLx = curve(t, 0, 0, 9, -20, 12, -62, 20, -62, 30, 0);
        p.shinL = curve(t, 0, 0, 9, 20, 12, 62, 20, 62, 30, 0);
        p.legRx = curve(t, 0, 0, 9, 20, 12, 38, 20, 38, 30, 0);
        p.shinR = curve(t, 0, 0, 9, 10, 12, 5, 30, 0);
        p.headX = curve(t, 0, -6, 9, 0, 12, -24, 20, -24, 30, -6);
        p.headY = curve(t, 0, 0, 9, -30, 12, 18, 30, 0);
        p.hatX = curve(t, 10, 0, 13, -10, 20, 0);
    }

    // ---- hop, compass raised with legs split wide, slam that splits the ground in two lines
    private static void splitSlam(P p, float t) {
        p.drop = curve(t, 0, 0, 7, 4, 9, 0, 18, 0, 20, 6, 28, 6, 40, 0);
        p.rootDy = curve(t, 0, 0, 8, 0, 13, -9, 18, -2, 20, 0, 40, 0);
        p.bodyX = curve(t, 0, 5, 7, 18, 14, -20, 20, 45, 28, 42, 40, 5);
        p.armRx = curve(t, 0, -14, 7, 20, 14, -175, 17, -150, 20, -95, 28, -90, 40, -14);
        p.armLx = curve(t, 0, 4, 7, 20, 14, -175, 17, -150, 20, -95, 28, -90, 40, 4);
        p.armRz = curve(t, 0, 9, 14, -12, 20, -18, 30, -14, 40, 9);
        p.armLz = curve(t, 0, -7, 14, 14, 20, 20, 30, 16, 40, -7);
        p.foreR = curve(t, 0, -14, 14, -10, 20, 0, 40, -14);
        p.foreL = curve(t, 0, -22, 14, -10, 20, 0, 40, -22);
        p.compX = curve(t, 0, -42, 8, -20, 14, 0, 30, 0, 40, -42);
        p.spread = curve(t, 0, 14, 10, 6, 15, 44, 28, 44, 36, 14);
        p.legRx = curve(t, 0, 0, 7, -15, 13, -45, 18, -20, 20, 0, 40, 0);
        p.legLx = curve(t, 0, 0, 7, -15, 13, -45, 18, -20, 20, 0, 40, 0);
        p.shinR = curve(t, 0, 0, 7, 25, 13, 80, 18, 30, 20, 10, 40, 0);
        p.shinL = curve(t, 0, 0, 7, 25, 13, 80, 18, 30, 20, 10, 40, 0);
        p.legRz = curve(t, 0, 0, 18, 0, 20, 30, 30, 30, 40, 0);
        p.legLz = curve(t, 0, 0, 18, 0, 20, -30, 30, -30, 40, 0);
        p.headX = curve(t, 0, -6, 13, -20, 20, -35, 28, -35, 40, -6);
        p.hatX = curve(t, 16, 0, 20, 14, 26, 0);
        if (t > 20 && t < 27) p.rootZ = Anim.sinr(t * 3.1f) * 1.5f; // impact shudder
    }

    // ---- sidearm boomerang throw, empty hand, catch
    private static void compassThrow(P p, float t) {
        p.compHidden = t >= 13 && t < 34;
        p.drop = curve(t, 0, 0, 11, 3, 15, 2, 40, 0);
        p.bodyY = curve(t, 0, 0, 11, 60, 14, -40, 20, -30, 30, 0, 40, 0);
        p.bodyX = curve(t, 0, 5, 11, 0, 14, 22, 24, 6, 40, 5);
        p.armRx = curve(t, 0, -14, 11, -10, 14, -80, 20, -40, 30, -20, 34, -110, 37, -95, 40, -14);
        p.armRz = curve(t, 0, 9, 11, 75, 13, 70, 16, 20, 30, 12, 40, 9);
        p.armRy = curve(t, 0, 0, 11, 45, 14, -50, 20, -30, 30, 0);
        p.foreR = curve(t, 0, -14, 11, -60, 13, -5, 30, -10, 34, -30, 40, -14);
        p.compX = curve(t, 0, -42, 11, 0, 30, 0, 36, -60, 40, -42);
        p.spread = curve(t, 0, 14, 11, 35, 13, 35, 34, 30, 40, 14);
        p.armLx = curve(t, 0, 4, 11, -50, 14, 20, 24, -20, 30, 4);
        p.armLz = curve(t, 0, -7, 11, -40, 14, -15, 40, -7);
        p.legRx = curve(t, 0, 0, 11, 20, 14, -10, 30, 0);
        p.legLx = curve(t, 0, 0, 11, -15, 14, 20, 30, 0);
        p.headY = curve(t, 0, 0, 11, -40, 14, 15, 24, 0);
        p.headZ = curve(t, 16, 0, 22, 18, 30, 18, 34, 0); // cocky tilt while it flies
        p.headX = curve(t, 0, -6, 16, -6, 22, -14, 34, -6);
    }

    // ---- plant the compass and draw a full circle around herself, then the circle bursts
    private static void drawCircle(P p, float t) {
        p.drop = curve(t, 0, 0, 6, 5, 30, 5, 33, 0, 36, 0, 46, 0);
        p.rootDy = curve(t, 0, 0, 30, 0, 33, -4, 36, 0);
        p.rootY = linear(t, 0, 0, 6, 0, 30, -360, 46, -360);
        p.bodyX = curve(t, 0, 5, 6, 32, 30, 32, 33, -18, 38, -14, 46, 5);
        p.bodyZ = curve(t, 0, 0, 6, -10, 30, -10, 33, 0);
        p.armRx = curve(t, 0, -14, 6, -25, 30, -25, 33, -165, 38, -160, 46, -14);
        p.armRz = curve(t, 0, 9, 6, 55, 30, 55, 33, 30, 38, 25, 46, 9);
        p.foreR = curve(t, 0, -14, 6, 0, 30, 0, 46, -14);
        p.compX = curve(t, 0, -42, 6, 18, 30, 18, 33, 0, 40, 0, 46, -42);
        p.spread = curve(t, 0, 14, 6, 60, 30, 60, 34, 10, 46, 14);
        p.armLx = curve(t, 0, 4, 6, -30, 30, -30, 33, -160, 38, -160, 46, 4);
        p.armLz = curve(t, 0, -7, 6, -50, 30, -50, 33, -30, 38, -35, 46, -7);
        p.legRx = curve(t, 0, 0, 6, -10, 30, -10, 33, 0);
        p.legLx = curve(t, 0, 0, 6, 25, 30, 25, 33, 0);
        p.legRz = curve(t, 0, 0, 6, 18, 30, 18, 33, 0);
        p.legLz = curve(t, 0, 0, 6, -18, 30, -18, 33, 0);
        p.headX = curve(t, 0, -6, 6, 25, 30, 25, 33, -30, 40, -30, 46, -6);
        if (t > 6 && t < 30) p.bodyY = Anim.sinr(t * 1.7f) * 3;
    }

    // ---- draw the flamethrower from the thigh, sweep a stream of fire, holster
    private static void flame(P p, float t) {
        p.gunOut = t >= 6 && t < 47;
        float sw = t > 14 && t < 42 ? Anim.sinr((t - 14) * 0.22f) * 18 : 0;
        float jit = t > 14 && t < 42 ? Anim.sinr(t * 2.7f) * 2.5f : 0;
        p.drop = curve(t, 0, 0, 5, 3, 12, 2, 44, 2, 52, 0);
        p.bodyY = curve(t, 0, 0, 5, 10, 12, -28, 42, -28, 52, 0) + sw;
        p.bodyZ = curve(t, 0, 0, 5, 12, 10, 0);
        p.bodyX = curve(t, 0, 5, 5, 20, 12, 8, 42, 8, 52, 5);
        p.armLx = curve(t, 0, 4, 5, 25, 7, 20, 12, -86, 42, -86, 46, 25, 49, 20, 52, 4) + jit;
        p.armLz = curve(t, 0, -7, 5, -2, 7, -2, 12, -6, 42, -6, 46, -2, 52, -7);
        p.armLy = curve(t, 0, 0, 12, 18, 42, 18, 52, 0);
        p.foreL = curve(t, 0, -22, 5, -10, 12, -4, 42, -4, 52, -22);
        p.handL = curve(t, 0, 10, 5, 0, 52, 10);
        p.armRx = curve(t, 0, -14, 10, 15, 42, 15, 52, -14);
        p.armRz = curve(t, 0, 9, 10, 20, 42, 20, 52, 9);
        p.compX = curve(t, 0, -42, 10, -55, 42, -55, 52, -42);
        p.legLx = curve(t, 0, 0, 12, -22, 42, -22, 52, 0);
        p.shinL = curve(t, 0, 0, 12, 18, 42, 18, 52, 0);
        p.legRx = curve(t, 0, 0, 12, 18, 42, 18, 52, 0);
        p.headX = curve(t, 0, -6, 5, 20, 12, 4, 42, 4, 52, -6);
        p.headY = curve(t, 0, 0, 12, 20, 42, 20, 52, 0) - sw * 0.6f;
        p.headZ = curve(t, 12, 0, 16, -10, 42, -10, 48, 0);
        p.fringeX += t > 14 && t < 42 ? Anim.sinr(t * 1.9f) * 5 : 0;
    }

    // ---- quick-draw fireball shot(s)
    private static void fireball(P p, float t) {
        p.gunOut = t >= 4 && t < 27;
        float rec = curve(t, 13, 0, 14, -28, 17, 0, 19, 0, 20, -28, 23, 0);
        p.drop = curve(t, 0, 0, 4, 3, 10, 1, 30, 0);
        p.bodyY = curve(t, 0, 0, 4, 10, 10, -30, 24, -30, 30, 0);
        p.bodyX = curve(t, 0, 5, 4, 18, 10, -6, 24, -6, 30, 5) + rec * 0.25f;
        p.armLx = curve(t, 0, 4, 3, 25, 5, 20, 10, -112, 24, -110, 27, 20, 30, 4) + rec;
        p.armLz = curve(t, 0, -7, 10, -5, 30, -7);
        p.armLy = curve(t, 0, 0, 10, 20, 24, 20, 30, 0);
        p.foreL = curve(t, 0, -22, 4, -10, 10, -2, 24, -2, 30, -22);
        p.armRx = curve(t, 0, -14, 10, 10, 24, 10, 30, -14);
        p.armRz = curve(t, 0, 9, 10, 26, 24, 26, 30, 9);
        p.legLx = curve(t, 0, 0, 10, -20, 24, -20, 30, 0);
        p.legRx = curve(t, 0, 0, 10, 16, 24, 16, 30, 0);
        p.headX = curve(t, 0, -6, 4, 18, 10, -14, 24, -14, 30, -6);
        p.headY = curve(t, 0, 0, 10, 22, 24, 22, 30, 0);
    }

    // ---- crouch, sprint with the compass scraping behind, rising upward slash
    private static void charge(P p, float t) {
        float run = t > 6 && t < 24 ? 1 : 0;
        float ph = t * 0.95f;
        p.drop = curve(t, 0, 0, 5, 6, 8, 3, 23, 3, 25, 0, 28, -1, 34, 0);
        p.rootDy = run * -Math.abs(Anim.sinr(ph)) * 2 + curve(t, 23, 0, 26, -4, 30, 0);
        p.bodyX = curve(t, 0, 5, 5, 40, 23, 42, 26, -18, 30, -10, 34, 5);
        p.bodyY = run * Anim.sinr(ph) * 10 + curve(t, 22, 0, 24, 30, 27, -25, 34, 0);
        p.legRx = run * Anim.sinr(ph) * 60 + curve(t, 0, 0, 5, -30, 7, 0, 23, 0, 25, -20, 34, 0);
        p.legLx = -run * Anim.sinr(ph) * 60 + curve(t, 0, 0, 5, 30, 7, 0, 23, 0, 25, 20, 34, 0);
        p.shinR = run * (40 + 40 * Anim.cos((float) Math.toDegrees(ph))) + curve(t, 0, 0, 5, 50, 7, 0);
        p.shinL = run * (40 - 40 * Anim.cos((float) Math.toDegrees(ph))) + curve(t, 0, 0, 5, 10, 7, 0);
        p.armRx = curve(t, 0, -14, 5, 45, 23, 50, 25, 55, 27, -170, 30, -150, 34, -14);
        p.armRz = curve(t, 0, 9, 5, 20, 23, 20, 27, 12, 34, 9);
        p.foreR = curve(t, 0, -14, 5, 0, 25, 0, 27, 0, 34, -14);
        p.compX = curve(t, 0, -42, 5, -25, 23, -25, 25, 0, 27, 0, 30, 0, 34, -42);
        p.spread = curve(t, 0, 14, 5, 14, 23, 14, 27, 4, 34, 14);
        p.armLx = run * -Anim.sinr(ph) * 50 + curve(t, 0, 4, 5, 40, 7, -10, 23, -10, 27, 40, 34, 4);
        p.armLz = curve(t, 0, -7, 5, -20, 23, -20, 34, -7);
        p.foreL = curve(t, 0, -22, 5, -60, 23, -60, 34, -22);
        p.headX = curve(t, 0, -6, 5, -40, 23, -40, 27, -10, 34, -6);
        p.hairX = 3 + run * 40 + curve(t, 0, 0, 5, 10, 7, 30);
    }

    // ---- turn away and lash the enormous hair around
    private static void hairWhip(P p, float t) {
        p.rootY = curve(t, 0, 0, 9, 150, 13, -45, 18, -30, 28, 0);
        p.drop = curve(t, 0, 0, 9, 3, 13, 4, 28, 0);
        p.bodyX = curve(t, 0, 5, 9, -8, 13, 22, 28, 5);
        p.headY = curve(t, 0, 0, 9, -70, 12, 0, 28, 0);
        p.headX = curve(t, 0, -6, 9, -15, 13, 20, 28, -6);
        p.hairX = curve(t, 0, 3, 9, -10, 12, 70, 16, 55, 28, 3);
        p.hairZ = curve(t, 0, 0, 9, 35, 12, -70, 17, -40, 28, 0);
        p.armRz = curve(t, 0, 9, 9, 40, 13, 20, 28, 9);
        p.armLz = curve(t, 0, -7, 9, -50, 13, -20, 28, -7);
        p.armLx = curve(t, 0, 4, 9, -30, 13, 20, 28, 4);
        p.legRx = curve(t, 0, 0, 9, 18, 13, -12, 28, 0);
        p.legLx = curve(t, 0, 0, 9, -18, 13, 12, 28, 0);
        p.hatX = curve(t, 9, 0, 12, -12, 18, 0);
    }

    // ---- enraged three-hit combo: slash, backhand, jumping plant
    private static void combo(P p, float t) {
        p.drop = curve(t, 0, 0, 5, 4, 10, 3, 14, 4, 19, 3, 22, 4, 24, 0, 30, 6, 36, 6, 44, 0);
        p.rootDy = curve(t, 0, 0, 22, 0, 26, -8, 30, 0);
        p.rootDz = curve(t, 0, 0, 8, -2, 18, -3, 30, -4, 44, 0);
        p.bodyY = curve(t, 0, 0, 5, 45, 9, -45, 13, -50, 18, 40, 22, 20, 30, 0, 44, 0);
        p.bodyX = curve(t, 0, 5, 5, 15, 9, 20, 18, 10, 24, -18, 30, 45, 36, 40, 44, 5);
        p.armRx = curve(t, 0, -14, 5, -20, 9, -40, 13, -30, 18, -120, 22, -150, 26, -175, 30, -95, 36, -90, 44, -14);
        p.armRz = curve(t, 0, 9, 5, 80, 9, 85, 13, 40, 18, 70, 22, 10, 30, -10, 44, 9);
        p.armRy = curve(t, 0, 0, 5, 40, 9, -50, 13, -60, 18, 30, 22, 0);
        p.foreR = curve(t, 0, -14, 5, -30, 9, 0, 13, -40, 18, 0, 44, -14);
        p.compX = curve(t, 0, -42, 5, 0, 36, 0, 44, -42);
        p.spread = curve(t, 0, 14, 22, 6, 27, 40, 36, 40, 44, 14);
        p.armLx = curve(t, 0, 4, 9, -40, 18, -30, 22, -150, 26, -175, 30, -95, 36, -90, 44, 4);
        p.armLz = curve(t, 0, -7, 9, -40, 18, -50, 26, 14, 36, 14, 44, -7);
        p.legLx = curve(t, 0, 0, 5, -30, 18, -30, 22, -10, 26, -40, 30, -10, 44, 0);
        p.shinL = curve(t, 0, 0, 5, 30, 18, 30, 26, 70, 30, 30, 44, 0);
        p.legRx = curve(t, 0, 0, 5, 20, 18, 20, 26, -40, 30, 15, 44, 0);
        p.shinR = curve(t, 0, 0, 26, 70, 30, 20, 44, 0);
        p.headX = curve(t, 0, -6, 9, 0, 24, -20, 30, -30, 44, -6);
        p.headY = curve(t, 0, 0, 5, -30, 9, 25, 18, -20, 22, 0);
    }

    // ---- enraged: spinning inferno with the flamethrower, then compass slam + fireball nova
    private static void inferno(P p, float t) {
        p.gunOut = t >= 5 && t < 58;
        p.drop = curve(t, 0, 0, 5, 3, 10, 2, 46, 2, 48, 7, 54, 7, 64, 0);
        p.rootY = linear(t, 0, 0, 10, 0, 46, -720, 64, -720);
        p.bodyX = curve(t, 0, 5, 5, -15, 9, -25, 12, 0, 46, 0, 48, 45, 54, 40, 64, 5);
        p.headX = curve(t, 0, -6, 5, -25, 9, -35, 12, -5, 46, -5, 48, -30, 64, -6);
        p.headZ = t < 10 ? Anim.sinr(t * 2.4f) * 8 : 0; // cackling
        p.armLx = curve(t, 0, 4, 4, 25, 6, 20, 12, -10, 46, -10, 48, 20, 58, 20, 64, 4);
        p.armLz = curve(t, 0, -7, 6, -2, 12, -88, 46, -88, 48, -30, 64, -7);
        p.foreL = curve(t, 0, -22, 6, -10, 12, 0, 46, 0, 64, -22);
        p.armRx = curve(t, 0, -14, 9, -170, 12, -150, 44, -160, 47, -175, 48, -95, 54, -90, 64, -14);
        p.armRz = curve(t, 0, 9, 9, -10, 12, 10, 46, 10, 48, -15, 64, 9);
        p.compX = curve(t, 0, -42, 9, 0, 54, 0, 64, -42);
        p.spread = curve(t, 0, 14, 12, 25, 46, 25, 48, 50, 56, 50, 64, 14);
        p.legRz = curve(t, 0, 0, 12, 14, 46, 14, 48, 26, 54, 26, 64, 0);
        p.legLz = curve(t, 0, 0, 12, -14, 46, -14, 48, -26, 54, -26, 64, 0);
        if (t > 48 && t < 54) p.rootZ = Anim.sinr(t * 3.3f) * 1.8f;
    }

    private static void death(P p, float d) {
        p.compHidden = false;
        p.drop = curve(d, 0, 0, 0.3f, 7, 1, 7);
        p.shinR = curve(d, 0, 0, 0.3f, 95, 1, 95);
        p.shinL = curve(d, 0, 0, 0.3f, 95, 1, 95);
        p.legRx = curve(d, 0, 0, 0.3f, -45, 1, -45);
        p.legLx = curve(d, 0, 0, 0.3f, -45, 1, -45);
        p.rootX = curve(d, 0, 0, 0.35f, 0, 0.85f, 70, 1, 66);
        p.rootDy = curve(d, 0, 0, 0.35f, 0, 0.85f, 2, 1, 2);
        p.bodyX = curve(d, 0, 5, 0.3f, 25, 0.6f, -10, 1, 0);
        p.headX = curve(d, 0, -6, 0.3f, 30, 1, 20);
        p.headY = 0;
        p.armRx = curve(d, 0, -14, 0.3f, 10, 0.85f, -150, 1, -160);
        p.armLx = curve(d, 0, 4, 0.3f, 10, 0.85f, -150, 1, -165);
        p.armRz = curve(d, 0, 9, 1, 25);
        p.armLz = curve(d, 0, -7, 1, -25);
        p.compX = curve(d, 0, -42, 0.3f, 30, 0.6f, 80, 1, 80);
        p.spread = curve(d, 0, 14, 0.5f, 45, 1, 45);
        p.hatX = curve(d, 0, 0, 0.5f, -30, 1, -60);
        p.hairX = curve(d, 0, 3, 0.85f, -40, 1, -30);
    }

    // ---------------------------------------------------------------------------------------- apply
    private static void animate(ModelParts m, AnimCtx c) {
        P p = pose(c, c.t, c.age);
        P q = pose(c, c.t - 3, c.age - 3);    // lagged pose -> secondary motion
        P r = pose(c, c.t - 6, c.age - 6);
        boolean rage = c.fpe != null && c.fpe.isEnraged();

        m.rot("root", p.rootX, p.rootY, p.rootZ);
        m.move("root", 0, p.rootDy, p.rootDz);
        m.move("pelvis", 0, p.drop, 0);
        m.rot("pelvis", p.pelvisX, 0, 0);
        m.rot("body", p.bodyX, p.bodyY, p.bodyZ);
        m.rot("head", p.headX - p.bodyX * 0.5f, p.headY, p.headZ);
        m.rot("hatBrim", 9 + p.hatX, 0, 0);

        // legs: crouch IK-ish (thigh forward, knee back) + per-pose offsets
        float a = (float) Math.toDegrees(Math.acos(Anim.clamp(1 - p.drop / 15f, -1, 1)));
        m.rot("legR", p.legRx - a, 0, p.legRz + 2);
        m.rot("legL", p.legLx - a, 0, p.legLz - 2);
        m.rot("shinR", p.shinR + a * 2, 0, 0);
        m.rot("shinL", p.shinL + a * 2, 0, 0);
        m.rot("bootR", -(p.legRx + p.shinR) * 0.3f, 0, 0);
        m.rot("bootL", -(p.legLx + p.shinL) * 0.3f, 0, 0);

        m.rot("armR", p.armRx, p.armRy, p.armRz);
        m.rot("foreR", p.foreR, 0, 0);
        m.rot("armL", p.armLx, p.armLy, p.armLz);
        m.rot("foreL", p.foreL, 0, 0);
        m.rot("handL", p.handL, 0, 0);
        m.rot("comp", p.compX, p.compY, p.compZ);
        m.rot("cLegA", 0, 0, p.spread * 0.5f);
        m.rot("cLegB", 0, 0, -p.spread * 0.5f);
        m.show("comp", !p.compHidden);
        m.show("gun", p.gunOut);
        m.show("hol", !p.gunOut);

        // secondary motion: velocities from lagged poses
        float yawV = (p.rootY + p.bodyY) - (q.rootY + q.bodyY);
        float yawV2 = (q.rootY + q.bodyY) - (r.rootY + r.bodyY);
        float leanV = p.bodyX - q.bodyX, upV = p.rootDy - q.rootDy;
        float flare = p.hairX + Anim.clamp(Math.abs(yawV) * 0.5f, 0, 50) + Anim.clamp(-upV * 3f, -20, 25) - leanV * 0.4f;
        float side = Anim.clamp(p.hairZ - yawV * 0.45f, -70, 70), side2 = Anim.clamp(q.hairZ - yawV2 * 0.45f, -70, 70);
        float comp = -p.bodyX * 0.8f;
        m.rot("hairC1", comp + flare * 0.45f, 0, side * 0.4f);
        m.rot("hairC2", flare * 0.35f + Anim.sinr(c.age * 0.11f) * 2, 0, side2 * 0.4f);
        m.rot("hairC3", flare * 0.25f + Anim.sinr(c.age * 0.11f - 1) * 3, 0, side2 * 0.3f);
        m.addRot("hairWR", flare * 0.25f, 0, Math.max(0, -side) * 0.4f + Anim.sinr(c.age * 0.09f) * 2);
        m.addRot("hairWL", flare * 0.25f, 0, -Math.max(0, side) * 0.4f - Anim.sinr(c.age * 0.09f) * 2);
        m.addRot("hairW2R", flare * 0.15f, 0, Anim.sinr(c.age * 0.09f - 0.8f) * 3);
        m.addRot("hairW2L", flare * 0.15f, 0, -Anim.sinr(c.age * 0.09f - 0.8f) * 3);
        m.addRot("hairSideR", -p.headX * 0.4f + flare * 0.1f, 0, 0);
        m.addRot("hairSideL", -p.headX * 0.4f + flare * 0.1f, 0, 0);
        m.rot("poncho", -leanV * 0.3f + Anim.clamp(-upV * 1.5f, -8, 12), 0, -yawV * 0.08f);
        m.rot("fringe", p.fringeX + Anim.clamp(Math.abs(yawV) * 0.4f, 0, 40), 0, 0);
        m.addRot("bandTail", Anim.sinr(c.age * 0.3f) * 15 + flare * 0.3f, 0, 0);

        // blink / rage eyes
        boolean blink = c.death == 0 && (c.age % 90) > 86;
        m.show("eyeR", !blink && c.death < 0.6f);
        m.show("eyeL", !blink && c.death < 0.6f);
        if (rage) { m.scale("eyeR", 1.2f, 1.8f, 1); m.scale("eyeL", 1.2f, 1.8f, 1); }
    }
}
