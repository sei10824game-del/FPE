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
 * Red Circle (DANGER AU): wild spiky black mane with ears, sharp grin + glowing red eye, short dark buttoned jacket,
 * pale baggy cuffed trousers, tall striped boots, big gauntlet holding a giant pencil and a compass leg like twin blades.
 * Idle: the compass leg rides in the left fist next to the pencil; during attacks the right hand takes it (dual wield).
 */
public final class RedCircleSpec {
    private RedCircleSpec() {}

    static final int HAIR = 0x2B2433, HAIR_D = 0x1C1622, HAIR_L = 0x463C55;
    static final int SKIN = 0xE6E6E2, ARM = 0xCFD0CB, JACKET = 0x2E2638, JACKET_D = 0x221C2A, GRAY = 0x8E9AA0;
    static final int PANTS = 0xDCDCD4, PANTS_D = 0xB4B4AC, BOOT = 0x2A2433, STRIPE = 0x9FB0B8;
    static final int BLOOD = 0xB0101E, BLOOD_D = 0x6A0A12, EYE = 0xFF2030, DARK = 0x14101A, TOOTH = 0xFAF8F0;
    static final int WHITE = 0xE9E9E4, WOOD = 0xD9CDB5, METAL = 0xC6C8D0;

    public static final ModelSpec SPEC = build();

    private static ModelSpec build() {
        ModelSpec m = new ModelSpec("red_circle");
        m.shadow(0.7f);
        m.group("root", null, 0, 24, 0);
        m.group("pelvis", "root", 0, 8, 0);

        // ---------------------------------------------------------------- legs (hip 8, knee 16, ground 24)
        for (int s = -1; s <= 1; s += 2) {
            String S = s < 0 ? "R" : "L";
            float x = 1.95f * s;
            m.part("leg" + S, "pelvis", x, 8, 0, -1.9f, 0, -1.9f, 3.8f, 8, 3.8f, PANTS).inflate(0.4f)
                    .decor(Face.FRONT, s < 0 ? 1 : 2, 1, 1, 6, PANTS_D).decor(Face.FRONT, s < 0 ? 2 : 1, 4, 1, 1, BLOOD);
            m.part("shin" + S, "leg" + S, x, 16, 0, -1.9f, 0, -1.9f, 3.8f, 2, 3.8f, PANTS).inflate(0.35f);
            m.part("cuff" + S, "shin" + S, x, 16, 0, -2.3f, 0.6f, -2.3f, 4.6f, 1.5f, 4.6f, 0xEDEDE8).decor(Face.FRONT, 0, 1, 5, 1, PANTS_D);
            m.part("boot" + S, "shin" + S, x, 16, 0, -2, 2, -2, 4, 6, 4, BOOT)
                    .decor(Face.FRONT, 0, 2, 4, 1, STRIPE).decor(Face.FRONT, 0, 4, 4, 1, STRIPE).decor(Face.FRONT, 0, 3, 4, 1, BLOOD)
                    .decor(Face.LEFT, 0, 2, 4, 1, STRIPE).decor(Face.RIGHT, 0, 2, 4, 1, STRIPE).decor(Face.LEFT, 0, 4, 4, 1, STRIPE).decor(Face.RIGHT, 0, 4, 4, 1, STRIPE);
            m.part("bootTop" + S, "boot" + S, x, 16, 0, -2.5f, 1.6f, -2.5f, 5, 1.6f, 5, BOOT);
            m.part("foot" + S, "boot" + S, x, 16, 0, -2.3f, 6.4f, -4.8f, 4.6f, 1.6f, 3, BOOT).decor(Face.TOP, 0, 0, 5, 1, HAIR_L);
        }

        // ---------------------------------------------------------------- torso
        m.part("body", "pelvis", 0, 8, 0, -3.8f, -11, -2.2f, 7.6f, 8.8f, 4.4f, JACKET)
                .decor(Face.FRONT, 2, 0, 2, 2, GRAY).decor(Face.FRONT, 4, 0, 2, 2, GRAY).decor(Face.FRONT, 3, 0, 2, 1, SKIN)
                .decor(Face.FRONT, 5, 3, 1, 1, GRAY).decor(Face.FRONT, 5, 5, 1, 1, GRAY).decor(Face.FRONT, 4, 2, 1, 7, JACKET_D)
                .decor(Face.FRONT, 1, 6, 1, 2, GRAY);
        m.part("hem", "body", 0, 8, 0, -4, -3.4f, -2.4f, 8, 1.3f, 4.8f, JACKET_D);
        m.part("waist", "body", 0, 8, 0, -3.6f, -2.3f, -2, 7.2f, 2.3f, 4, PANTS).decor(Face.FRONT, 3, 0, 2, 2, PANTS_D);

        // ---------------------------------------------------------------- head
        m.part("head", "body", 0, -3, 0, -3.5f, -7, -3.5f, 7, 7, 7, SKIN)
                .decor(Face.FRONT, 0, 0, 7, 2, 0x3A3240)
                .decor(Face.FRONT, 0, 4, 7, 2, DARK).decor(Face.FRONT, 0, 3, 1, 1, DARK).decor(Face.FRONT, 6, 3, 1, 1, DARK).decor(Face.FRONT, 1, 6, 5, 1, DARK)
                .decor(Face.FRONT, 0, 4, 1, 1, TOOTH).decor(Face.FRONT, 2, 4, 1, 1, TOOTH).decor(Face.FRONT, 4, 4, 1, 1, TOOTH).decor(Face.FRONT, 6, 4, 1, 1, TOOTH)
                .decor(Face.FRONT, 1, 6, 1, 1, TOOTH).decor(Face.FRONT, 3, 6, 1, 1, TOOTH).decor(Face.FRONT, 5, 6, 1, 1, TOOTH)
                .decor(Face.FRONT, 2, 5, 3, 1, BLOOD);
        m.part("eyeL", "head", 1.8f, -3, 0, -1, -5.4f, -3.75f, 2, 1.2f, 0.3f, EYE).glow();
        m.part("eyeR", "head", -1.8f, -3, 0, -1, -5.2f, -3.95f, 1.4f, 0.8f, 0.3f, EYE).glow();
        m.part("rageEyeL", "head", 1.8f, -3, 0, -1.4f, -5.8f, -3.8f, 2.8f, 2, 0.3f, EYE).glow();
        // bangs covering her right eye
        m.part("bangs", "head", 0, -3, 0, -3.9f, -7.4f, -3.9f, 4.4f, 4.6f, 1.2f, HAIR).rot(0, 0, -8).decor(Face.FRONT, 1, 1, 1, 3, HAIR_L);
        m.part("bangs2", "head", 0, -3, 0, 0.2f, -7.4f, -3.9f, 3.6f, 1.8f, 1, HAIR);
        m.part("hairTop", "head", 0, -3, 0, -4, -7.8f, -2.9f, 8, 4, 7.6f, HAIR).decor(Face.TOP, 2, 2, 3, 1, HAIR_L);
        m.part("hairBack", "head", 0, -3, 0, -4.2f, -7.2f, 0.4f, 8.4f, 9, 4.4f, HAIR).pattern(Pattern.GRADIENT_V, HAIR_D, 1);
        for (int s = -1; s <= 1; s += 2) {
            String S = s < 0 ? "R" : "L";
            m.part("ear" + S, "head", 2.3f * s, -10.5f, 0.3f, -1.6f, -4.5f, -0.9f, 3.2f, 5, 1.8f, HAIR).rot(-4, 0, 16 * s)
                    .decor(Face.FRONT, 1, 1, 1, 3, s < 0 ? GRAY : HAIR_L);
            m.part("earTip" + S, "ear" + S, 2.3f * s, -10.5f, 0.3f, -0.8f, -8.5f, -0.6f, 1.6f, 4.2f, 1.2f, HAIR);
            m.part("hairSide" + S, "head", 3.7f * s, -9.5f, -0.5f, s < 0 ? -1.8f : -0.4f, 0, -2.8f, 2.2f, 12, 5, HAIR)
                    .pattern(Pattern.GRADIENT_V, HAIR_D, 1).rot(0, 0, 10 * -s);
            for (int i = 0; i < 3; i++)
                m.part("sideSpk" + S + i, "hairSide" + S, 3.7f * s + (s < 0 ? -1 : 1), -7 + i * 3.5f, -0.5f, -0.8f, 0, -1.2f, 1.6f, 4.5f, 2.4f, HAIR)
                        .rot(0, 0, -(55 + i * 8) * s);
        }

        // ---------------------------------------------------------------- spiky mane (body-attached chain)
        m.part("hairC1", "body", 0, -10, 3, -7, 0, -0.6f, 14, 10, 3.4f, HAIR).pattern(Pattern.GRADIENT_V, HAIR_D, 1)
                .decor(Face.BACK, 3, 1, 1, 8, HAIR_L).decor(Face.BACK, 10, 2, 1, 7, HAIR_L);
        m.part("hairC2", "hairC1", 0, 0, 3, -9, 0, -0.6f, 18, 10, 3.4f, HAIR).pattern(Pattern.GRADIENT_V, HAIR_D, 1)
                .decor(Face.BACK, 6, 0, 1, 9, HAIR_L).decor(Face.BACK, 13, 1, 1, 7, HAIR_L);
        m.part("hairC3", "hairC2", 0, 10, 3, -10.5f, 0, -0.6f, 21, 9, 3.4f, HAIR_D).pattern(Pattern.GRADIENT_V, 0x120E16, 1)
                .decor(Face.BACK, 2, 3, 3, 1, GRAY).decor(Face.BACK, 2, 5, 3, 1, GRAY); // light slash marks like the art
        String[] seg = {"hairC1", "hairC2", "hairC3"};
        float[] segY = {-10, 0, 10}, segW = {7, 9, 10.5f};
        for (int k = 0; k < 3; k++)
            for (int s = -1; s <= 1; s += 2)
                for (int i = 0; i < 2; i++) {
                    String n = "spk" + k + (s < 0 ? "R" : "L") + i;
                    m.part(n, seg[k], segW[k] * s, segY[k] + 2 + i * 4.5f, 3, -1, 0, -1.3f, 2, 7 + k, 2.6f, k == 2 ? HAIR_D : HAIR)
                            .rot(0, 0, -(26 + i * 12 + k * 4) * s);
                }
        for (int i = 0; i < 6; i++) {
            float x = -9 + i * 3.6f;
            m.part("tip" + i, "hairC3", x, 18.5f, 3, -1.1f, 0, -1.2f, 2.2f, 4 + (i % 2) * 1.5f, 2.6f, HAIR_D).rot(0, 0, (i - 2.5f) * 12);
        }

        // ---------------------------------------------------------------- arms (shoulder -2, elbow 4.5, wrist 10)
        for (int s = -1; s <= 1; s += 2) {
            String S = s < 0 ? "R" : "L";
            float x = 5.2f * s;
            m.part("arm" + S, "body", 4.6f * s, -2, 0, s < 0 ? -1.9f : -0.7f, -0.5f, -1.3f, 2.6f, 6.5f, 2.6f, ARM);
            m.part("sleeve" + S, "arm" + S, 4.6f * s, -2, 0, s < 0 ? -2.6f : -0.8f, -1.3f, -2, 3.4f, 4.6f, 4, JACKET)
                    .decor(Face.FRONT, 0, 3, 4, 1, GRAY);
            m.part("fore" + S, "arm" + S, x, 4.5f, 0, -1.3f, 0, -1.3f, 2.6f, 5.5f, 2.6f, ARM);
            m.part("hand" + S, "fore" + S, x, 10, 0, -1.5f, 0, -1.5f, 3, 2.6f, 3, 0x221C29);
            m.group("grip" + S, "hand" + S, x, 11.3f, 0);
        }
        m.part("gauntL", "foreL", 5.2f, 4.5f, 0, -2, 1.4f, -2, 4, 4.4f, 4, 0x221C29)
                .decor(Face.FRONT, 1, 2, 2, 1, GRAY).decor(Face.LEFT, 1, 2, 2, 1, GRAY).decor(Face.FRONT, 0, 0, 4, 1, BLOOD_D);
        for (int i = 0; i < 3; i++)
            m.part("claw" + i, "handR", -5.2f, 10, 0, -1.3f + i * 1.05f, 2.2f, -1.4f, 0.6f, 2.4f, 0.6f, 0x120E16).rot(-15, 0, 0);
        m.part("clawTip", "handR", -5.2f, 10, 0, -1.4f, 4.3f, -1.9f, 2.9f, 0.5f, 0.6f, BLOOD).rot(-15, 0, 0);

        // ---------------------------------------------------------------- twin blades
        pencil(m, "pen", "gripL", 5.2f, 11.3f, 0);
        compassRod(m, "rodL", "gripL", 5.2f, 11.3f, 0);
        compassRod(m, "rodR", "gripR", -5.2f, 11.3f, 0);

        m.animator(RedCircleSpec::animate);
        return m;
    }

    /** giant pencil along -z (forward) from the fist */
    private static void pencil(ModelSpec m, String p, String parent, float x, float y, float z) {
        m.group(p, parent, x, y, z);
        m.part(p + "Shaft", p, x, y, z, -0.85f, -0.85f, -16, 1.7f, 1.7f, 19, WHITE).decor(Face.TOP, 0, 2, 2, 6, 0xC8C8C2);
        m.part(p + "Band", p, x, y, z, -1, -1, -9.5f, 2, 2, 2.2f, HAIR);
        m.part(p + "Cap", p, x, y, z, -0.95f, -0.95f, 2.6f, 1.9f, 1.9f, 1.2f, HAIR);
        m.part(p + "Wood", p, x, y, z, -0.6f, -0.6f, -19, 1.2f, 1.2f, 3, WOOD);
        m.part(p + "Lead", p, x, y, z, -0.3f, -0.3f, -21, 0.6f, 0.6f, 2, BLOOD).glow();
    }

    /** compass leg blade along -z with a long needle */
    private static void compassRod(ModelSpec m, String p, String parent, float x, float y, float z) {
        m.group(p, parent, x, y, z);
        m.part(p + "Shaft", p, x, y, z, -0.7f, -0.7f, -14, 1.4f, 1.4f, 17, METAL).decor(Face.TOP, 0, 3, 1, 8, 0xF0F0F4);
        m.part(p + "Joint", p, x, y, z, -1, -1, 2.4f, 2, 2, 1.4f, HAIR);
        m.part(p + "Holder", p, x, y, z, -0.5f, -0.5f, -17, 1, 1, 3, 0xA8AAB4);
        m.part(p + "Needle", p, x, y, z, -0.2f, -0.2f, -21.5f, 0.4f, 0.4f, 4.5f, 0xD8DAE0);
        m.part(p + "Tip", p, x, y, z, -0.15f, -0.15f, -23, 0.3f, 0.3f, 1.6f, EYE).glow();
    }

    // =====================================================================================================
    static final class P {
        float rootX, rootY, rootZ, rootDy, rootDz, drop, pelvisX;
        float bodyX, bodyY, bodyZ, headX, headY, headZ;
        float armRx, armRy, armRz, foreR, armLx, armLy, armLz, foreL;
        float gripRx, gripRy, gripRz, gripLx, gripLy, gripLz;
        float legRx, legRz, legLx, legLz, shinR, shinL;
        float hairX, hairZ, spikes;
        boolean twin, thrown;
    }

    private static void base(P p, AnimCtx c, float age, boolean rage) {
        float sp = rage ? 1.6f : 1f;
        float br = Anim.sinr(age * 0.17f * sp);
        float w = c.walk(), ph = c.limbSwing * 0.6662f;
        float cph = (float) Math.toDegrees(ph);
        p.bodyX = 12 + br * 1.5f + 14 * w;
        p.headX = c.headPitch - 10 - br;
        p.headY = c.headYaw;
        p.headZ = 8 + Anim.sinr(age * 0.05f) * 4;
        // twitch every few seconds
        float tw = (age % 53f);
        if (tw > 48) p.headZ += Anim.sinr(tw * 4f) * 10;
        if (rage) p.headZ += Anim.sinr(age * 1.9f) * 2;
        p.armRx = 6 + br * 3 - Anim.cos(cph) * 30 * w;
        p.armRz = 12 + br * 2;
        p.foreR = -10 - 25 * w;
        p.armLx = -28 + br * 2 + Anim.cos(cph) * 6 * w;
        p.armLz = -14;
        p.armLy = 10;
        p.foreL = -55;
        p.gripLx = -62; p.gripLy = 0; p.gripLz = 38;
        p.legRx = Anim.cos(cph) * 40 * w;
        p.legLx = -Anim.cos(cph) * 40 * w;
        p.legRz = 7; p.legLz = -7;
        p.shinR = (16 + 22 * Anim.sinr(ph)) * w;
        p.shinL = (16 - 22 * Anim.sinr(ph)) * w;
        p.bodyY = Anim.cos(cph) * 10 * w;
        p.rootDy = -Math.abs(Anim.sinr(ph)) * 1.4f * w;
        p.drop = 1 + w;
        p.hairX = 4 + Anim.sinr(age * 0.08f) * 2 + 18 * w;
        p.hairZ = Anim.sinr(age * 0.06f) * 3;
        p.spikes = rage ? 8 + Anim.sinr(age * 0.5f) * 3 : 0;
    }

    static P pose(AnimCtx c, float t, float age, boolean rage) {
        P p = new P();
        base(p, c, age, rage);
        if (c.death > 0) { death(p, c.death); return p; }
        if (c.ability.isEmpty()) return p;
        p.twin = !c.is("roar");
        float rx = p.armRx, ry = p.armRy, rz = p.armRz, fr = p.foreR;
        switch (c.ability) {
            case "xSlash" -> xSlash(p, t);
            case "flurry" -> flurry(p, t);
            case "tornado" -> tornado(p, t);
            case "pencilVolley" -> pencilVolley(p, t, rage);
            case "bladeWave" -> bladeWave(p, t);
            case "bloodRing" -> bloodRing(p, t);
            case "leapSlam" -> leapSlam(p, t);
            case "rush" -> rush(p, t);
            case "twinThrow" -> twinThrow(p, t);
            case "frenzy" -> frenzy(p, t);
            case "execution" -> execution(p, t);
            case "roar" -> roar(p, t);
            default -> { }
        }
        if (p.twin) {
            // right hand reaches across to take the compass leg (first ticks) and hands it back (last ticks)
            float in = Anim.smooth(t / 5f), out = Anim.smooth((c.dur - t) / 5f);
            float k = Math.min(in, out);
            p.armRx = Anim.lerp(-55, p.armRx, k); p.armRy = Anim.lerp(-45, p.armRy, k); p.armRz = Anim.lerp(-10, p.armRz, k);
            p.foreR = Anim.lerp(-40, p.foreR, k);
            p.twin = t >= 2 && t <= c.dur - 2;
        }
        return p;
    }

    /** neutral fighting stance helper for both blades: gripX 0 = blade perpendicular to the forearm (sword grip) */
    private static void blades(P p) { p.gripLx = 0; p.gripRx = 0; }

    // ---- X cross slash
    private static void xSlash(P p, float t) {
        blades(p);
        p.drop = curve(t, 0, 1, 7, 4, 11, 5, 16, 5, 24, 1);
        p.rootDz = curve(t, 0, 0, 8, 1, 11, -3, 18, -3, 24, 0);
        p.bodyX = curve(t, 0, 12, 7, -14, 11, 34, 16, 30, 24, 12);
        p.armRx = curve(t, 0, 6, 7, -165, 11, -30, 16, -25, 24, 6);
        p.armLx = curve(t, 0, -28, 7, -165, 11, -30, 16, -25, 24, -28);
        p.armRz = curve(t, 0, 12, 7, -28, 11, 45, 16, 40, 24, 12);
        p.armLz = curve(t, 0, -14, 7, 28, 11, -45, 16, -40, 24, -14);
        p.armLy = 0;
        p.foreR = curve(t, 0, -10, 7, -20, 11, 0, 24, -10);
        p.foreL = curve(t, 0, -55, 7, -20, 11, 0, 24, -55);
        p.gripLz = curve(t, 0, 0, 11, -20, 24, 0);
        p.gripRz = curve(t, 0, 0, 11, 20, 24, 0);
        p.legRx = curve(t, 0, 0, 7, 10, 11, 30, 24, 0);
        p.legLx = curve(t, 0, 0, 7, -10, 11, -40, 24, 0);
        p.shinL = curve(t, 0, 0, 11, 40, 24, 0);
        p.headX = curve(t, 0, -10, 7, 5, 11, -30, 24, -10);
    }

    // ---- alternating twin thrusts
    private static void flurry(P p, float t) {
        p.gripLx = 90; p.gripRx = 90;
        p.drop = curve(t, 0, 1, 6, 4, 30, 4, 36, 1);
        float on = t > 6 && t < 30 ? 1 : 0;
        float cyc = (t - 6) / 3f;                 // one thrust every 3 ticks, alternating hands
        int i = (int) Math.floor(cyc);
        float f = cyc - i;
        float ext = (float) Math.sin(Math.PI * Anim.clamp(f, 0, 1));
        boolean right = (i & 1) == 0;
        float r = on * (right ? ext : 0), l = on * (right ? 0 : ext);
        p.bodyX = curve(t, 0, 12, 6, 18, 30, 22, 36, 12);
        p.bodyY = on * (right ? -18 : 18) * ext + curve(t, 0, 0, 6, 15, 7, 0);
        p.armRx = curve(t, 0, 6, 6, 30, 30, 30, 36, 6) * (1 - on) + on * (35 - r * 145);
        p.armLx = curve(t, 0, -28, 6, 30, 30, 30, 36, -28) * (1 - on) + on * (35 - l * 145);
        p.foreR = curve(t, 0, -10, 6, -100, 36, -10) * (1 - on) + on * (-100 + r * 100);
        p.foreL = curve(t, 0, -55, 6, -100, 36, -55) * (1 - on) + on * (-100 + l * 100);
        p.armRz = 8; p.armLz = -8; p.armLy = 0;
        p.legRx = 20; p.legLx = -30; p.shinL = 30;
        p.headX = -18;
        p.rootDz = on * -ext * 1.5f;
    }

    // ---- spinning blade tornado
    private static void tornado(P p, float t) {
        blades(p);
        p.gripLx = 70; p.gripRx = 70;
        p.drop = curve(t, 0, 1, 6, 4, 40, 3, 44, 2, 48, 1);
        p.rootY = linear(t, 0, 0, 8, 0, 40, -1440, 48, -1440);
        p.rootDy = t > 8 && t < 40 ? -1 - Anim.sinr(t * 0.8f) : 0;
        p.bodyX = curve(t, 0, 12, 6, 25, 9, -4, 40, -4, 44, 20, 48, 12);
        p.armRz = curve(t, 0, 12, 6, 30, 9, 90, 40, 90, 44, 20, 48, 12);
        p.armLz = curve(t, 0, -14, 6, -30, 9, -90, 40, -90, 44, -20, 48, -14);
        p.armRx = curve(t, 0, 6, 6, 20, 9, 0, 40, 0, 48, 6);
        p.armLx = curve(t, 0, -28, 6, 20, 9, 0, 40, 0, 48, -28);
        p.foreR = curve(t, 0, -10, 9, 0, 40, 0, 48, -10);
        p.foreL = curve(t, 0, -55, 9, 0, 40, 0, 48, -55);
        p.armLy = 0;
        p.legRz = curve(t, 0, 7, 9, 2, 40, 2, 48, 7);
        p.legLz = curve(t, 0, -7, 9, -2, 40, -2, 48, -7);
        p.headX = curve(t, 0, -10, 9, -20, 40, -20, 48, -10);
        p.headZ = curve(t, 38, 0, 42, 25, 45, -20, 48, 8); // dizzy wobble after spin
    }

    // ---- fan of pencils flung from both hands (enraged: second fan)
    private static void pencilVolley(P p, float t, boolean rage) {
        p.gripLx = -100; p.gripRx = -100;
        p.drop = curve(t, 0, 1, 9, 4, 13, 2, 30, 1);
        p.bodyX = curve(t, 0, 12, 9, 28, 13, -8, 18, 0, 22, -8, 30, 12);
        p.armRx = curve(t, 0, 6, 9, -60, 13, -80, 18, -50, 22, -80, 30, 6);
        p.armLx = curve(t, 0, -28, 9, -60, 13, -80, 18, -50, 22, -80, 30, -28);
        p.armRy = curve(t, 0, 0, 9, -60, 13, 60, 18, -20, 22, 50, 30, 0);
        p.armLy = curve(t, 0, 10, 9, 60, 13, -60, 18, 20, 22, -50, 30, 10);
        p.armRz = curve(t, 0, 12, 9, -10, 13, 30, 30, 12);
        p.armLz = curve(t, 0, -14, 9, 10, 13, -30, 30, -14);
        p.foreR = curve(t, 0, -10, 9, -70, 13, 0, 30, -10);
        p.foreL = curve(t, 0, -55, 9, -70, 13, 0, 30, -55);
        p.headX = curve(t, 0, -10, 9, 10, 13, -20, 30, -10);
        p.legRx = curve(t, 0, 0, 9, 15, 13, -5, 30, 0);
        p.legLx = curve(t, 0, 0, 9, -15, 13, 10, 30, 0);
    }

    // ---- two sweeping slashes that launch blade waves
    private static void bladeWave(P p, float t) {
        blades(p);
        p.drop = curve(t, 0, 1, 8, 4, 11, 5, 15, 3, 18, 5, 30, 1);
        p.bodyY = curve(t, 0, 0, 8, 55, 11, -35, 15, -50, 18, 40, 22, 30, 30, 0);
        p.bodyX = curve(t, 0, 12, 8, 0, 11, 30, 15, 10, 18, 25, 30, 12);
        p.armRx = curve(t, 0, 6, 8, -150, 11, -20, 15, -80, 18, -85, 30, 6);
        p.armLx = curve(t, 0, -28, 8, -150, 11, -20, 15, -80, 18, -85, 30, -28);
        p.armRz = curve(t, 0, 12, 8, 30, 11, 10, 15, 10, 18, 60, 30, 12);
        p.armLz = curve(t, 0, -14, 8, 10, 11, -20, 15, -60, 18, -10, 30, -14);
        p.armRy = curve(t, 0, 0, 15, 50, 18, -40, 30, 0);
        p.armLy = curve(t, 0, 10, 15, 50, 18, -40, 30, 10);
        p.foreR = curve(t, 0, -10, 8, -20, 11, 0, 30, -10);
        p.foreL = curve(t, 0, -55, 8, -20, 11, 0, 30, -55);
        p.legRx = curve(t, 0, 0, 8, 20, 11, 25, 30, 0);
        p.legLx = curve(t, 0, 0, 8, -20, 11, -35, 30, 0);
        p.shinL = curve(t, 0, 0, 11, 30, 30, 0);
        p.headY = curve(t, 0, 0, 8, -40, 11, 20, 15, 30, 18, -25, 30, 0);
    }

    // ---- hop and plunge both blades into the ground -> bloody expanding ring
    private static void bloodRing(P p, float t) {
        p.gripLx = -90; p.gripRx = -90;                   // reverse grip, blades along the forearm downward
        p.drop = curve(t, 0, 1, 5, 5, 7, 0, 13, 0, 16, 8, 26, 8, 38, 1);
        p.rootDy = curve(t, 0, 0, 6, 0, 11, -8, 14, -3, 16, 0);
        p.bodyX = curve(t, 0, 12, 5, 25, 11, -20, 16, 55, 26, 50, 38, 12);
        p.armRx = curve(t, 0, 6, 5, 30, 11, -170, 16, -60, 26, -60, 38, 6);
        p.armLx = curve(t, 0, -28, 5, 30, 11, -170, 16, -60, 26, -60, 38, -28);
        p.armRz = curve(t, 0, 12, 11, -10, 16, 15, 38, 12);
        p.armLz = curve(t, 0, -14, 11, 10, 16, -15, 38, -14);
        p.armLy = 0;
        p.foreR = curve(t, 0, -10, 11, 0, 38, -10);
        p.foreL = curve(t, 0, -55, 11, 0, 38, -55);
        p.legRx = curve(t, 0, 0, 7, -30, 12, -50, 16, 0, 38, 0);
        p.legLx = curve(t, 0, 0, 7, -30, 12, -50, 16, 0, 38, 0);
        p.shinR = curve(t, 0, 0, 7, 50, 12, 90, 16, 0, 38, 0);
        p.shinL = curve(t, 0, 0, 7, 50, 12, 90, 16, 0, 38, 0);
        p.legRz = curve(t, 0, 7, 16, 25, 26, 25, 38, 7);
        p.legLz = curve(t, 0, -7, 16, -25, 26, -25, 38, -7);
        p.headX = curve(t, 0, -10, 11, -25, 16, -55, 26, -60, 38, -10);
        p.spikes = curve(t, 14, p.spikes, 17, 30, 28, 12, 36, p.spikes);
        if (t > 16 && t < 22) p.rootZ = Anim.sinr(t * 3.2f) * 1.5f;
    }

    // ---- crouch, leap with a forward flip, blades-down landing
    private static void leapSlam(P p, float t) {
        p.gripLx = -90; p.gripRx = -90;
        p.drop = curve(t, 0, 1, 7, 7, 9, 0, 20, 0, 22, 8, 30, 8, 38, 1);
        p.rootDy = curve(t, 0, 0, 8, 0, 13, -14, 18, -8, 22, 0);
        p.pelvisX = linear(t, 0, 0, 9, 0, 19, 360, 38, 360);
        p.bodyX = curve(t, 0, 12, 7, 35, 9, 0, 19, 20, 22, 50, 30, 45, 38, 12);
        p.armRx = curve(t, 0, 6, 7, 50, 10, -170, 19, -170, 22, -40, 30, -40, 38, 6);
        p.armLx = curve(t, 0, -28, 7, 50, 10, -170, 19, -170, 22, -40, 30, -40, 38, -28);
        p.armRz = curve(t, 0, 12, 10, -10, 22, 20, 38, 12);
        p.armLz = curve(t, 0, -14, 10, 10, 22, -20, 38, -14);
        p.armLy = 0;
        p.foreR = curve(t, 0, -10, 10, 0, 38, -10);
        p.foreL = curve(t, 0, -55, 10, 0, 38, -55);
        p.legRx = curve(t, 0, 0, 9, 10, 12, -80, 19, -80, 22, -20, 30, -20, 38, 0);
        p.legLx = curve(t, 0, 0, 9, 10, 12, -80, 19, -80, 22, 20, 30, 20, 38, 0);
        p.shinR = curve(t, 0, 0, 12, 110, 19, 110, 22, 30, 38, 0);
        p.shinL = curve(t, 0, 0, 12, 110, 19, 110, 22, 10, 38, 0);
        p.headX = curve(t, 0, -10, 7, -30, 19, -10, 22, -50, 30, -50, 38, -10);
    }

    // ---- three dashes: slash R, slash L, rising X
    private static void rush(P p, float t) {
        blades(p);
        p.drop = curve(t, 0, 1, 3, 5, 7, 4, 13, 5, 17, 4, 23, 6, 28, 0, 32, 0, 42, 1);
        p.rootDy = curve(t, 0, 0, 26, 0, 29, -4, 33, 0);
        p.bodyX = curve(t, 0, 12, 3, 40, 7, 25, 13, 40, 17, 25, 23, 45, 28, -20, 34, -10, 42, 12);
        p.bodyY = curve(t, 0, 0, 4, 50, 8, -50, 13, -55, 18, 50, 23, 0, 42, 0);
        p.armRx = curve(t, 0, 6, 4, -60, 8, -70, 13, 30, 18, 30, 23, 40, 28, -175, 33, -160, 42, 6);
        p.armRz = curve(t, 0, 12, 4, 90, 8, 60, 13, 20, 23, 15, 28, -10, 42, 12);
        p.armRy = curve(t, 0, 0, 4, 50, 8, -60, 13, 0);
        p.foreR = curve(t, 0, -10, 4, -30, 8, 0, 23, -10, 28, 0, 42, -10);
        p.armLx = curve(t, 0, -28, 8, 30, 13, -60, 18, -70, 23, 40, 28, -175, 33, -160, 42, -28);
        p.armLz = curve(t, 0, -14, 8, -20, 13, -90, 18, -60, 23, -15, 28, 10, 42, -14);
        p.armLy = curve(t, 0, 10, 13, -50, 18, 60, 23, 0);
        p.foreL = curve(t, 0, -55, 13, -30, 18, 0, 23, -10, 28, 0, 42, -55);
        p.legRx = curve(t, 0, 0, 3, 30, 7, -30, 13, 30, 17, -30, 23, 25, 28, 0, 42, 0);
        p.legLx = curve(t, 0, 0, 3, -30, 7, 30, 13, -30, 17, 30, 23, -25, 28, 0, 42, 0);
        p.shinR = curve(t, 0, 0, 7, 40, 13, 10, 17, 40, 23, 20, 28, 0);
        p.headX = curve(t, 0, -10, 3, -40, 23, -40, 28, -15, 42, -10);
        p.hairX = 4 + curve(t, 0, 0, 4, 40, 23, 40, 30, 10);
    }

    // ---- throw both blades as spinning boomerangs, catch them
    private static void twinThrow(P p, float t) {
        blades(p);
        p.thrown = t >= 14 && t < 38;
        p.drop = curve(t, 0, 1, 11, 4, 15, 2, 44, 1);
        p.bodyX = curve(t, 0, 12, 11, -22, 15, 35, 22, 15, 44, 12);
        p.armRx = curve(t, 0, 6, 11, -170, 14, -60, 22, -40, 32, -20, 37, -100, 40, -95, 44, 6);
        p.armLx = curve(t, 0, -28, 11, -170, 14, -60, 22, -40, 32, -20, 37, -100, 40, -95, 44, -28);
        p.armRz = curve(t, 0, 12, 11, 25, 14, 15, 32, 25, 37, 10, 44, 12);
        p.armLz = curve(t, 0, -14, 11, -25, 14, -15, 32, -25, 37, -10, 44, -14);
        p.armLy = 0;
        p.foreR = curve(t, 0, -10, 11, -60, 14, 0, 44, -10);
        p.foreL = curve(t, 0, -55, 11, -60, 14, 0, 44, -55);
        p.legRx = curve(t, 0, 0, 11, 20, 15, -10, 30, 0);
        p.legLx = curve(t, 0, 0, 11, -20, 15, 25, 30, 0);
        p.headX = curve(t, 0, -10, 11, -20, 15, -30, 22, -10, 44, -10);
        p.headZ = curve(t, 18, 8, 24, 25, 32, 25, 36, 8); // cocky head tilt
    }

    // ---- enraged: 6 alternating berserk slashes + X finisher
    private static void frenzy(P p, float t) {
        blades(p);
        float on = t > 4 && t < 36 ? 1 : 0;
        float cyc = (t - 4) / 5f;
        int i = (int) Math.floor(cyc);
        float f = Anim.smooth(Anim.clamp((cyc - i) * 1.6f, 0, 1));
        float dir = (i & 1) == 0 ? 1 : -1;
        float sw = on * dir * Anim.lerp(-1, 1, f);    // -1 -> 1 sweep, alternating direction
        p.drop = on * 5 + curve(t, 0, 1, 4, 4, 36, 4, 38, 2, 42, 6, 46, 6, 52, 1) * (1 - on);
        p.bodyY = on * sw * -55;
        p.bodyX = on * 28 + (1 - on) * curve(t, 0, 12, 4, 25, 36, 25, 39, -15, 42, 35, 46, 30, 52, 12);
        p.rootDz = on * -Anim.sinr(f * 3.14f) * 2;
        p.armRx = on * -70 + (1 - on) * curve(t, 0, 6, 36, -70, 39, -165, 42, -30, 46, -25, 52, 6);
        p.armLx = on * -70 + (1 - on) * curve(t, 0, -28, 36, -70, 39, -165, 42, -30, 46, -25, 52, -28);
        p.armRz = on * (60 + sw * 30) + (1 - on) * curve(t, 0, 12, 36, 60, 39, -28, 42, 45, 52, 12);
        p.armLz = on * (-60 + sw * 30) + (1 - on) * curve(t, 0, -14, 36, -60, 39, 28, 42, -45, 52, -14);
        p.armRy = on * sw * -40;
        p.armLy = on * sw * -40;
        p.foreR = on * -10 + (1 - on) * curve(t, 0, -10, 42, 0, 52, -10);
        p.foreL = on * -10 + (1 - on) * curve(t, 0, -55, 42, 0, 52, -55);
        p.legRx = on * (dir > 0 ? 25 : -20); p.legLx = on * (dir > 0 ? -25 : 20);
        p.headX = -25;
        p.headY = on * sw * 20;
        p.spikes += 6;
    }

    // ---- enraged: point, crouch, spinning leap into the drawn circle, plunge
    private static void execution(P p, float t) {
        p.gripLx = curve(t, 0, 0, 14, 0, 16, -90);
        p.gripRx = curve(t, 0, 0, 14, 0, 16, -90);
        p.drop = curve(t, 0, 1, 6, 1, 14, 7, 17, 0, 28, 0, 32, 8, 38, 8, 46, 1);
        p.rootDy = curve(t, 0, 0, 16, 0, 21, -16, 28, -8, 32, 0);
        p.rootY = linear(t, 0, 0, 16, 0, 28, -720, 46, -720);
        p.bodyX = curve(t, 0, 12, 6, 0, 14, 40, 17, -10, 28, 10, 32, 55, 38, 50, 42, -25, 46, 12);
        p.armRx = curve(t, 0, 6, 4, -95, 10, -95, 14, 40, 17, -170, 28, -170, 32, -40, 38, -40, 42, -170, 46, 6);
        p.armRz = curve(t, 0, 12, 4, 0, 10, 0, 14, 20, 17, -10, 32, 20, 42, 40, 46, 12);
        p.armLx = curve(t, 0, -28, 6, -10, 14, 40, 17, -170, 28, -170, 32, -40, 38, -40, 42, -170, 46, -28);
        p.armLz = curve(t, 0, -14, 6, -30, 17, 10, 32, -20, 42, -40, 46, -14);
        p.armLy = 0;
        p.foreR = curve(t, 0, -10, 4, 0, 46, -10);
        p.foreL = curve(t, 0, -55, 6, -30, 17, 0, 46, -55);
        p.legRx = curve(t, 0, 0, 14, 20, 18, -70, 28, -70, 32, 0, 46, 0);
        p.legLx = curve(t, 0, 0, 14, -30, 18, -70, 28, -70, 32, 0, 46, 0);
        p.shinR = curve(t, 0, 0, 18, 100, 28, 100, 32, 0);
        p.shinL = curve(t, 0, 0, 14, 40, 18, 100, 28, 100, 32, 0);
        p.headX = curve(t, 0, -10, 6, -5, 14, -40, 32, -55, 38, -55, 42, -40, 46, -10);
        p.headZ = curve(t, 0, 8, 4, 20, 10, 20, 14, 8);
        p.spikes += curve(t, 30, 0, 33, 20, 40, 5);
    }

    // ---- rage transformation roar
    private static void roar(P p, float t) {
        p.drop = curve(t, 0, 1, 6, 5, 10, 2, 30, 1);
        p.bodyX = curve(t, 0, 12, 6, 45, 10, -30, 24, -25, 30, 12);
        p.headX = curve(t, 0, -10, 6, 30, 10, -45, 24, -45, 30, -10);
        p.armRz = curve(t, 0, 12, 6, 10, 10, 75, 24, 75, 30, 12);
        p.armLz = curve(t, 0, -14, 6, -10, 10, -75, 24, -75, 30, -14);
        p.armRx = curve(t, 0, 6, 6, 30, 10, -30, 24, -30, 30, 6);
        p.armLx = curve(t, 0, -28, 6, 30, 10, -30, 24, -30, 30, -28);
        p.foreR = curve(t, 0, -10, 10, -40, 24, -40, 30, -10);
        p.spikes = curve(t, 0, 0, 10, 40, 24, 35, 30, 10);
        if (t > 10 && t < 24) { p.rootZ = Anim.sinr(t * 3.7f) * 1.5f; p.headZ = Anim.sinr(t * 2.9f) * 8; }
    }

    private static void death(P p, float d) {
        p.drop = curve(d, 0, 1, 0.25f, 8, 1, 8);
        p.shinR = curve(d, 0, 0, 0.25f, 100, 1, 100);
        p.shinL = curve(d, 0, 0, 0.25f, 100, 1, 100);
        p.legRx = curve(d, 0, 0, 0.25f, -50, 1, -50);
        p.legLx = curve(d, 0, 0, 0.25f, -50, 1, -50);
        p.rootX = curve(d, 0, 0, 0.3f, 0, 0.8f, -75, 1, -72); // falls backward
        p.bodyX = curve(d, 0, 12, 0.25f, -20, 0.5f, 25, 1, 10);
        p.headX = curve(d, 0, -10, 0.25f, -50, 0.8f, 10, 1, 25);
        p.headY = 0;
        p.armRz = curve(d, 0, 12, 0.3f, 60, 1, 85);
        p.armLz = curve(d, 0, -14, 0.3f, -60, 1, -85);
        p.armRx = curve(d, 0, 6, 1, -20);
        p.armLx = curve(d, 0, -28, 1, -20);
        p.foreL = curve(d, 0, -55, 1, -10);
        p.gripLx = curve(d, 0, -48, 0.6f, -10, 1, 0);
        p.hairX = curve(d, 0, 4, 0.8f, 60, 1, 50);
    }

    // ---------------------------------------------------------------------------------------- apply
    private static void animate(ModelParts m, AnimCtx c) {
        boolean rage = c.fpe != null && c.fpe.isEnraged();
        P p = pose(c, c.t, c.age, rage);
        P q = pose(c, c.t - 3, c.age - 3, rage);
        P r = pose(c, c.t - 6, c.age - 6, rage);

        m.rot("root", p.rootX, p.rootY, p.rootZ);
        m.move("root", 0, p.rootDy, p.rootDz);
        m.move("pelvis", 0, p.drop, 0);
        m.rot("pelvis", p.pelvisX, 0, 0);
        m.rot("body", p.bodyX, p.bodyY, p.bodyZ);
        m.rot("head", p.headX - p.bodyX * 0.6f, p.headY, p.headZ);

        float a = (float) Math.toDegrees(Math.acos(Anim.clamp(1 - p.drop / 16f, -1, 1)));
        m.rot("legR", p.legRx - a, 0, p.legRz);
        m.rot("legL", p.legLx - a, 0, p.legLz);
        m.rot("shinR", p.shinR + a * 2, 0, -p.legRz * 0.7f);
        m.rot("shinL", p.shinL + a * 2, 0, -p.legLz * 0.7f);
        m.rot("bootR", -(p.legRx + p.shinR) * 0.3f, 0, 0);
        m.rot("bootL", -(p.legLx + p.shinL) * 0.3f, 0, 0);

        m.rot("armR", p.armRx, p.armRy, p.armRz);
        m.rot("foreR", p.foreR, 0, 0);
        m.rot("armL", p.armLx, p.armLy, p.armLz);
        m.rot("foreL", p.foreL, 0, 0);
        m.rot("gripL", p.gripLx, p.gripLy, p.gripLz);
        m.rot("gripR", p.gripRx, p.gripRy, p.gripRz);
        // pencil + compass leg splay in the left fist like a V; when dual wielding the left fist keeps only the pencil
        m.rot("pen", 0, 4, 0);
        m.rot("rodL", 0, -8, 0);
        m.move("rodL", 0.9f, 0, 0);
        m.show("rodL", !p.twin && !p.thrown);
        m.show("rodR", p.twin && !p.thrown);
        m.show("pen", !p.thrown);

        // secondary motion
        float yawV = (p.rootY + p.bodyY + p.pelvisX * 0) - (q.rootY + q.bodyY);
        float yawV2 = (q.rootY + q.bodyY) - (r.rootY + r.bodyY);
        float leanV = (p.bodyX + p.pelvisX) - (q.bodyX + q.pelvisX), upV = p.rootDy - q.rootDy;
        float flare = p.hairX + Anim.clamp(Math.abs(yawV) * 0.5f, 0, 55) + Anim.clamp(-upV * 3f, -25, 30) - Anim.clamp(leanV * 0.4f, -30, 30);
        float side = Anim.clamp(p.hairZ - yawV * 0.45f, -70, 70), side2 = Anim.clamp(q.hairZ - yawV2 * 0.45f, -70, 70);
        m.rot("hairC1", -p.bodyX * 0.8f + flare * 0.45f, 0, side * 0.35f);
        m.rot("hairC2", flare * 0.35f + Anim.sinr(c.age * 0.13f) * 2.5f, 0, side2 * 0.35f);
        m.rot("hairC3", flare * 0.25f + Anim.sinr(c.age * 0.13f - 1) * 3.5f, 0, side2 * 0.3f);
        for (int k = 0; k < 3; k++)
            for (int i = 0; i < 2; i++) {
                float jig = Anim.sinr(c.age * 0.2f + k + i * 2) * 4;
                m.addRot("spk" + k + "R" + i, 0, 0, p.spikes + jig);
                m.addRot("spk" + k + "L" + i, 0, 0, -p.spikes - jig);
            }
        m.addRot("hairSideR", -p.headX * 0.4f + flare * 0.1f, 0, p.spikes * 0.3f);
        m.addRot("hairSideL", -p.headX * 0.4f + flare * 0.1f, 0, -p.spikes * 0.3f);
        m.addRot("earR", 0, 0, p.spikes * 0.3f);
        m.addRot("earL", 0, 0, -p.spikes * 0.3f);

        boolean blink = c.death == 0 && (c.age % 70) > 67 && !rage;
        m.show("eyeL", !blink && c.death < 0.7f);
        m.show("eyeR", !blink && c.death < 0.7f);
        m.show("rageEyeL", rage && c.death == 0);
    }
}
