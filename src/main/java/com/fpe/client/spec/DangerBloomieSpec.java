package com.fpe.client.spec;

import com.fpe.client.model.Anim;
import com.fpe.client.model.AnimCtx;
import com.fpe.client.model.ModelParts;
import com.fpe.client.model.ModelSpec;
import com.fpe.client.model.ModelSpec.Face;
import com.fpe.client.model.ModelSpec.Pattern;

/**
 * Danger AU Bloomie: thin angular build, flat black bob with eye-hiding bangs and spiky flares, top-knot with a pale bow,
 * short black jacket with white buttons, grey A-line skirt, long black limbs, white claws (right), huge serrated
 * bandage-wrapped cleaver (left). Animation keyed to entity/characters/DangerBloomie.
 */
public final class DangerBloomieSpec {
    private DangerBloomieSpec() {}

    static final int JACKET = 0x24212B, JACKET_HI = 0x36323F, LAPEL = 0x4A4655, BUTTON = 0xEEEEE8, SKIRT = 0xA6ADB0, SKIRT_LT = 0xD3D7D6,
            SKIRT_DK = 0x8A9296, SKIN = 0xE6E3DC, HAIR = 0x1C1A23, HAIR_HI = 0x2C2934, BOW = 0xDADDDB, TIGHTS = 0x1F1C26,
            CLAW = 0xF0F0EA, BLADE = 0xB9BEC2, BLADE_DK = 0x8D9398, EDGE = 0xE6EAEC, BANDAGE = 0xE4E1D6, BANDAGE_SH = 0xB9B5A8,
            GRIP = 0x2B2522, MOUTH = 0x120D15, BLOOD = 0x7A1420;

    public static final ModelSpec SPEC = build();

    private static ModelSpec build() {
        ModelSpec m = new ModelSpec("danger_bloomie");
        m.group("root", null, 0, 24, 0);
        m.group("hips", "root", 0, 12.5f, 0);

        // ---------------------------------------------------------------- long thin legs, pointed feet
        for (int s = -1; s <= 1; s += 2) {
            String k = s < 0 ? "R" : "L";
            float x = s * 1.25f;
            m.part("leg" + k, "hips", x, 13, 0, -0.85f, 0, -0.85f, 1.7f, 6, 1.7f, TIGHTS);
            m.part("shin" + k, "leg" + k, x, 19, 0, -0.75f, 0, -0.75f, 1.5f, 4.4f, 1.5f, TIGHTS);
            m.part("foot" + k, "shin" + k, x, 23.2f, 0, -0.9f, -0.4f, -1.4f, 1.8f, 1.2f, 2.6f, 0x15131A);
            m.part("toe" + k, "foot" + k, x, 23.6f, -1.4f, -0.5f, -0.4f, -2.2f, 1, 0.8f, 2.2f, 0x15131A).rot(-6, 0, 0);
        }

        // ---------------------------------------------------------------- A-line skirt (grey, lighter front panel)
        m.part("skirtTop", "hips", 0, 11.8f, 0, -3, 0, -2, 6, 2.2f, 4, SKIRT).decor(Face.FRONT, 0, 0, 6, 1, SKIRT_DK);
        m.part("skirtMid", "skirtTop", 0, 14, 0, -4, 0, -2.7f, 8, 2.6f, 5.4f, SKIRT).pattern(Pattern.STRIPE_V, SKIRT_DK, 2).grain(0.03f)
                .decor(Face.FRONT, 3, 0, 3, 1, SKIRT_LT).decor(Face.FRONT, 2, 1, 5, 2, SKIRT_LT);
        m.part("skirtHem", "skirtMid", 0, 16.6f, 0, -5.2f, 0, -3.4f, 10.4f, 2.6f, 6.8f, SKIRT).pattern(Pattern.STRIPE_V, SKIRT_DK, 2).grain(0.03f)
                .decor(Face.FRONT, 1, 0, 8, 1, SKIRT_LT).decor(Face.FRONT, 0, 1, 10, 2, SKIRT_LT).decor(Face.BOTTOM, 0, 0, 11, 7, SKIRT_DK);
        for (int s = -1; s <= 1; s += 2)   // angular corner flares
            m.part("skirtTip" + (s < 0 ? "R" : "L"), "skirtHem", s * 5.2f, 18.6f, -3.4f, -0.6f, -0.6f, -0.6f, 1.2f, 1.2f, 1.2f, SKIRT_LT).rot(0, 0, 45);

        // ---------------------------------------------------------------- jacket
        m.group("torso", "hips", 0, 12, 0);
        m.part("chest", "torso", 0, 12, 0, -2.6f, -6.6f, -1.7f, 5.2f, 6.6f, 3.4f, JACKET)
                .decor(Face.FRONT, 2, 0, 2, 7, JACKET_HI)
                .decor(Face.FRONT, 2, 3, 1, 1, BUTTON).decor(Face.FRONT, 2, 5, 1, 1, BUTTON)
                .decor(Face.BACK, 2, 0, 2, 7, JACKET_HI);
        m.part("jacketHem", "chest", 0, 12, 0, -2.9f, -1, -2.0f, 5.8f, 1.3f, 4.0f, JACKET).decor(Face.FRONT, 2, 0, 2, 2, LAPEL);
        m.part("lapelR", "chest", -0.6f, 5.6f, -1.75f, -1.8f, 0, -0.3f, 1.8f, 3.2f, 0.6f, LAPEL).rot(0, 0, -16).decor(Face.FRONT, 0, 0, 1, 1, 0x5C586A);
        m.part("lapelL", "chest", 0.6f, 5.6f, -1.75f, 0, 0, -0.3f, 1.8f, 3.2f, 0.6f, LAPEL).rot(0, 0, 16).decor(Face.FRONT, 1, 0, 1, 1, 0x5C586A);
        m.part("collar", "chest", 0, 5.8f, 0, -1.8f, -0.9f, -1.6f, 3.6f, 1.2f, 3.2f, LAPEL).decor(Face.FRONT, 1, 0, 2, 1, BUTTON);
        for (int s = -1; s <= 1; s += 2)   // sharp shoulder pads (angular silhouette)
            m.part("pad" + (s < 0 ? "R" : "L"), "chest", s * 2.8f, 5.8f, 0, -1.4f, -0.6f, -1.6f, 2.8f, 1.2f, 3.2f, JACKET_HI).rot(0, 0, s * -12);

        // ---------------------------------------------------------------- head
        m.part("neck", "chest", 0, 5.6f, 0, -0.75f, -1.1f, -0.75f, 1.5f, 1.3f, 1.5f, SKIN);
        m.part("head", "neck", 0, 4.7f, 0, -3, -6, -3, 6, 6, 6, SKIN)
                .decor(Face.FRONT, 0, 0, 6, 3, 0x2A2730)                                // fringe shadow
                .decorGlow(Face.FRONT, 1, 2, 1, 1, 0xE8F0FF).decorGlow(Face.FRONT, 4, 2, 1, 1, 0xE8F0FF)
                .decor(Face.FRONT, 0, 3, 1, 1, MOUTH).decor(Face.FRONT, 5, 3, 1, 1, MOUTH)
                .decor(Face.FRONT, 0, 4, 6, 1, MOUTH)
                .decor(Face.FRONT, 1, 4, 1, 1, CLAW).decor(Face.FRONT, 3, 4, 1, 1, CLAW)
                .decor(Face.FRONT, 2, 3, 1, 1, MOUTH).decor(Face.FRONT, 4, 4, 1, 1, CLAW).decor(Face.FRONT, 2, 5, 2, 1, 0xC8C4BC);
        // flat bob + bangs
        m.part("hairCap", "head", 0, -1.3f, 0, -3.6f, -1.6f, -3.6f, 7.2f, 2.4f, 7.2f, HAIR).pattern(Pattern.STRIPE_V, HAIR_HI, 3);
        m.part("bobBack", "head", 0, -0.5f, 0, -3.6f, 0, 1.6f, 7.2f, 5.6f, 2.0f, HAIR).pattern(Pattern.STRIPE_V, HAIR_HI, 2);
        m.part("bobR", "head", 0, -0.5f, 0, -3.6f, 0, -3.5f, 1.2f, 5.6f, 5.4f, HAIR).pattern(Pattern.STRIPE_H, HAIR_HI, 3);
        m.part("bobL", "head", 0, -0.5f, 0, 2.4f, 0, -3.5f, 1.2f, 5.6f, 5.4f, HAIR).pattern(Pattern.STRIPE_H, HAIR_HI, 3);
        m.part("bangs", "head", 0, -0.6f, 0, -3.4f, 0, -3.7f, 6.8f, 2.3f, 0.6f, HAIR).decor(Face.FRONT, 0, 2, 7, 1, HAIR_HI);
        float[] bx = {-2.6f, -0.9f, 0.9f, 2.6f};
        for (int i = 0; i < 4; i++)
            m.part("bangT" + i, "bangs", bx[i], 1.7f, -3.4f, -0.5f, -0.5f, -0.3f, 1, 1, 0.5f, HAIR).rot(0, 0, 45);
        // spiky flares sticking out horizontally from the bob
        for (int s = -1; s <= 1; s += 2) {
            String k = s < 0 ? "R" : "L";
            m.part("spk1" + k, "head", s * 3.4f, 0.2f, -1.0f, s < 0 ? -5.5f : 0, -0.6f, -0.6f, 5.5f, 1.2f, 1.2f, HAIR).rot(0, s * 10, s * -8);
            m.part("spk2" + k, "head", s * 3.4f, 2.8f, 0.2f, s < 0 ? -4.5f : 0, -0.6f, -0.6f, 4.5f, 1.2f, 1.2f, HAIR).rot(0, s * -15, s * -28);
            m.part("spk3" + k, "head", s * 3.4f, -1.8f, 0.5f, s < 0 ? -4.0f : 0, -0.5f, -0.5f, 4.0f, 1.0f, 1.0f, HAIR_HI).rot(0, s * 20, s * 22);
            m.part("spk4" + k, "head", s * 2.8f, 4.6f, 1.6f, s < 0 ? -3.2f : 0, -0.5f, -0.5f, 3.2f, 1.0f, 1.0f, HAIR).rot(0, s * -35, s * -40);
        }
        // top-knot + pale bow
        m.group("knot", "head", 0, -2.8f, 0.4f);
        m.part("knotBase", "knot", 0, -2.8f, 0.4f, -1.3f, -2.6f, -1.3f, 2.6f, 2.6f, 2.6f, HAIR).rot(0, 45, 0);
        m.part("knotSpike", "knot", 0, -5.2f, 0.4f, -0.7f, -3.2f, -0.7f, 1.4f, 3.2f, 1.4f, HAIR).rot(0, 45, -12);
        m.part("bowC", "knot", 0, -4.6f, -0.9f, -0.8f, -0.8f, -0.8f, 1.6f, 1.6f, 1.6f, BOW);
        m.part("bowR", "knot", -0.6f, -4.6f, -0.9f, -2.6f, -1.2f, -0.4f, 2.6f, 2.4f, 0.8f, BOW).rot(0, 0, 18).decor(Face.FRONT, 0, 1, 1, 1, 0xB4B8B6);
        m.part("bowL", "knot", 0.6f, -4.6f, -0.9f, 0, -1.2f, -0.4f, 2.6f, 2.4f, 0.8f, BOW).rot(0, 0, -18).decor(Face.FRONT, 2, 1, 1, 1, 0xB4B8B6);

        // ---------------------------------------------------------------- right arm: long, white claws
        m.group("armR", "chest", -3.3f, 6.3f, 0);
        m.part("uArmR", "armR", -3.3f, 6.3f, 0, -1.1f, -0.8f, -1.1f, 2, 6.6f, 2.2f, JACKET).decor(Face.FRONT, 0, 0, 2, 1, JACKET_HI);
        m.part("foreR", "uArmR", -3.4f, 12, 0, -0.9f, 0, -0.9f, 1.8f, 5.4f, 1.8f, JACKET).decor(Face.FRONT, 0, 4, 2, 2, LAPEL).decor(Face.RIGHT, 0, 4, 2, 2, LAPEL);
        m.part("handR", "foreR", -3.4f, 17.3f, 0, -1, 0, -1.1f, 2, 1.6f, 2.2f, 0x2B2832);
        float[][] cl = {{-4.1f, -0.7f, -26}, {-3.6f, -1.0f, -9}, {-3.0f, -1.0f, 8}, {-2.5f, -0.6f, 24}};
        for (int i = 0; i < 4; i++) {
            m.part("clR" + i, "handR", cl[i][0], 18.7f, cl[i][1], -0.35f, 0, -0.35f, 0.7f, 2.6f, 0.7f, CLAW).rot(-12, 0, cl[i][2]);
            m.part("clR" + i + "t", "clR" + i, cl[i][0], 21.2f, cl[i][1], -0.25f, 0, -0.25f, 0.5f, 2.4f, 0.5f, CLAW).rot(-28, 0, 0);
        }
        m.part("clRT", "handR", -2.4f, 18f, 0.6f, -0.35f, 0, -0.35f, 0.7f, 2.4f, 0.7f, CLAW).rot(-45, 0, 40);

        // ---------------------------------------------------------------- left arm + the cleaver
        m.group("armL", "chest", 3.3f, 6.3f, 0);
        m.part("uArmL", "armL", 3.3f, 6.3f, 0, -0.9f, -0.8f, -1.1f, 2, 6.6f, 2.2f, JACKET).decor(Face.FRONT, 0, 0, 2, 1, JACKET_HI);
        m.part("foreL", "uArmL", 3.4f, 12, 0, -0.9f, 0, -0.9f, 1.8f, 5.4f, 1.8f, JACKET).decor(Face.FRONT, 0, 4, 2, 2, LAPEL).decor(Face.LEFT, 0, 4, 2, 2, LAPEL);
        m.part("handL", "foreL", 3.4f, 17.3f, 0, -1, 0, -1.1f, 2, 2, 2.2f, 0x2B2832);
        // blade group: pivot in the fist, blade points along -z (forward when the arm hangs)
        m.group("blade", "handL", 3.4f, 18.4f, 0);
        m.part("grip", "blade", 3.4f, 18.4f, 0, -0.55f, -0.55f, -1.6f, 1.1f, 1.1f, 4.6f, GRIP).pattern(Pattern.STRIPE_V, 0x463C36, 1);
        m.part("pommel", "blade", 3.4f, 18.4f, 0, -0.75f, -0.75f, 3.0f, 1.5f, 1.5f, 1.0f, 0x3B3842);
        m.part("guard", "blade", 3.4f, 18.4f, 0, -0.7f, -1.6f, -2.4f, 1.4f, 3.2f, 0.8f, 0x3B3842);
        // wide blade body: wrapped near the hilt, bare serrated steel toward the tip
        m.part("wrap", "blade", 3.4f, 18.4f, 0, -0.5f, -1.8f, -10.4f, 1.0f, 4.2f, 8.0f, BANDAGE).pattern(Pattern.DIAG, BANDAGE_SH, 2).grain(0.05f)
                .decor(Face.LEFT, 2, 1, 1, 2, BLOOD).decor(Face.RIGHT, 5, 2, 1, 1, BLOOD);
        m.part("steel", "blade", 3.4f, 18.4f, 0, -0.4f, -1.7f, -19.4f, 0.8f, 4.0f, 9.0f, BLADE).grain(0.1f)
                .decor(Face.LEFT, 0, 3, 9, 1, BLADE_DK).decor(Face.RIGHT, 0, 3, 9, 1, BLADE_DK)
                .decor(Face.LEFT, 3, 1, 2, 2, BLOOD).decor(Face.RIGHT, 6, 0, 1, 2, BLOOD);
        m.part("band2", "blade", 3.4f, 18.4f, 0, -0.55f, -1.9f, -16.0f, 1.1f, 4.4f, 1.4f, BANDAGE).rot(18, 0, 0);
        m.part("edge", "blade", 3.4f, 18.4f, 0, -0.3f, 2.2f, -19.0f, 0.6f, 0.7f, 16.4f, EDGE).decorGlow(Face.LEFT, 0, 0, 16, 1, 0x9A2232).decorGlow(Face.RIGHT, 0, 0, 16, 1, 0x9A2232);
        m.part("tip", "blade", 3.4f, 21.2f, -19.4f, -0.4f, -4.2f, -2.4f, 0.8f, 4.2f, 2.4f, BLADE).rot(-32, 0, 0);
        for (int i = 0; i < 6; i++)   // serrated back
            m.part("tooth" + i, "blade", 3.4f, 16.6f, -4.5f - i * 2.5f, -0.35f, -0.8f, -0.8f, 0.7f, 1.6f, 1.6f, i < 3 ? BANDAGE_SH : BLADE_DK).rot(45, 0, 0);
        m.part("ribbon", "blade", 3.4f, 18.9f, 1.5f, -0.2f, 0, -0.5f, 0.4f, 5, 1, BANDAGE).pattern(Pattern.STRIPE_H, BANDAGE_SH, 2);
        m.part("ribbon2", "ribbon", 3.4f, 23.9f, 1.5f, -0.2f, 0, -0.4f, 0.4f, 3, 0.8f, BANDAGE);

        m.animator(DangerBloomieSpec::animate);
        return m;
    }

    // =================================================================== animation
    static final String[] CL = {"clR0", "clR1", "clR2", "clR3"};

    static float cv(float t, float... tv) { return Anim.curve(t, tv); }

    static void animate(ModelParts m, AnimCtx c) {
        BloomiePose idle = new BloomiePose();
        idlePose(idle, c);
        BloomiePose p = idle;
        if (!c.idle()) {
            BloomiePose a = idle.copy();
            ability(a, c, c.t);
            float w = Anim.smooth(c.t / 2.5f) * (1 - Anim.smooth((c.t - (c.dur - 5)) / 5f));
            p = BloomiePose.lerp(idle, a, w);
            BloomiePose past = idle.copy();
            ability(past, c, Math.max(0, c.t - 2.5f));
            BloomiePose pb = BloomiePose.lerp(idle, past, w);
            float dx = (p.get("chest", 0) - pb.get("chest", 0)) + (p.get("root", 0) - pb.get("root", 0));
            float dy = p.get("chest", 1) - pb.get("chest", 1) + p.get("root", 1) - pb.get("root", 1);
            float dv = p.get("root", 4) - pb.get("root", 4);
            p.ar("bobBack", Anim.clamp(-dx * 0.4f - dv * 3, -25, 25), 0, 0);
            p.ar("knot", Anim.clamp(-dx * 0.5f, -25, 25), 0, Anim.clamp(dy * 0.3f, -25, 25));
            p.ar("skirtHem", Anim.clamp(-dx * 0.3f + dv * 3, -22, 22), 0, Anim.clamp(-dy * 0.1f, -12, 12));
            p.ar("ribbon", Anim.clamp(-(p.get("armL", 0) - pb.get("armL", 0)) * 0.6f, -60, 60), 0, 0);
            for (int s = 0; s < 2; s++) {   // the horizontal hair flares whip with spins
                String k = s == 0 ? "R" : "L";
                p.ar("spk1" + k, 0, Anim.clamp(-dy * 0.4f, -30, 30), 0);
                p.ar("spk2" + k, 0, Anim.clamp(-dy * 0.3f, -30, 30), 0);
            }
        }
        if (c.death > 0) death(p, c);
        p.apply(m);
        m.show("blade", !(c.is("cleaver_throw") && c.t >= 13 && c.t < 46) && !(c.death > 0.3f));
    }

    static void idlePose(BloomiePose p, AnimCtx c) {
        float age = c.age, br = Anim.sin(age * 3.6f), w = c.walk();
        float sw = Anim.sinr(c.limbSwing * 0.6662f) * w, cw = (float) Math.cos(c.limbSwing * 0.6662f) * w;
        // eerie stillness: slight lean, head cocked hard, a sharp claw twitch every ~3 s
        float twitch = ((int) (age / 23)) % 3 == 1 ? Anim.curve(age % 23, 0, 0, 1, 1, 4, 0) : 0;
        p.r("chest", 8 + br * 1.2f + w * 8, sw * 6, 0);
        p.r("hips", -2, -sw * 5, 0);
        p.mv("root", 0, -Math.abs(cw) * 0.6f, 0);
        p.r("neck", 6, 0, 0);
        p.r("head", -10 - w * 8 + c.headPitch * 0.8f, c.headYaw * 0.85f, 16 + Anim.sin(age * 1.5f) * 4 - twitch * 8);
        // claw arm: hangs forward a little, fingers splayed
        p.r("armR", -12 + br * 2 - sw * 12, 0, 12);
        p.r("foreR", -22 - w * 10, 0, 0);
        p.r("handR", -10, 0, 0);
        for (int i = 0; i < 4; i++) { p.r(CL[i], twitch * -35 + Anim.sin(age * 7 + i * 80) * 4, 0, 0); p.r(CL[i] + "t", twitch * -30, 0, 0); }
        // cleaver arm: blade trails down and back, tip near the floor
        p.r("armL", 8 + sw * 10 + br * 1.5f, 0, -10);
        p.r("foreL", -10, 0, 0);
        p.r("blade", 105 + w * 15, 0, 6);
        // legs: wide angular stance, walk = long gliding strides
        p.r("legR", -sw * 38 - 6 * (1 - w), 0, 7 * (1 - w));
        p.r("shinR", Math.max(0, sw) * 40 + 4 * (1 - w), 0, 0);
        p.r("legL", sw * 38 + 8 * (1 - w), 0, -9 * (1 - w));
        p.r("shinL", Math.max(0, -sw) * 40, 0, 0);
        p.r("footR", 0, 0, 0);
        p.r("bobBack", 3 + Math.abs(cw) * 6, 0, 0);
        p.r("knot", 0, 0, Anim.sin(age * 4) * 3);
        p.r("skirtHem", Anim.sin(age * 4) * 2 - sw * 5, 0, cw * 3);
        p.r("ribbon", Anim.sin(age * 6) * 12 + w * 30, 0, Anim.sin(age * 4) * 8);
        p.r("ribbon2", Anim.sin(age * 6 - 50) * 15, 0, 0);
    }

    static void claws(BloomiePose p, float spread, float curl) {
        for (int i = 0; i < 4; i++) {
            p.ar(CL[i], -curl * 0.6f, 0, (i - 1.5f) / 1.5f * spread);
            p.ar(CL[i] + "t", -curl, 0, 0);
        }
        p.ar("clRT", -curl * 0.5f, 0, -spread * 0.5f);
    }

    /** shadow sink (0-8) / rise (8-14) shared by shadow_step and execution */
    static void shadow(BloomiePose p, float t) {
        float sink = cv(t, 0, 0, 7.5f, 1, 8, 1, 14, 0);
        p.mv("root", 0, sink * 20, 0);
        p.r("chest", 8 + sink * 30, 0, 0);
        p.r("head", -10 + sink * 20, 0, 16 + sink * 30);
        p.r("armR", sink * 40, 0, 12 + sink * 30);
        p.r("armL", sink * 40, 0, -10 - sink * 30);
    }

    static void ability(BloomiePose p, AnimCtx c, float t) {
        switch (c.ability) {
            case "chop" -> {
                // raise two-handed overhead 0-11, CHOP 12-13, blade bites the floor 13-20, eerie lift & flick 20-30
                p.r("armL", cv(t, 0, 8, 10, -185, 11.5f, -190, 13, -45, 20, -42, 26, -20, 30, 8), cv(t, 0, 0, 10, 20, 13, 0), cv(t, 0, -10, 10, 15, 13, 5, 30, -10));
                p.r("foreL", cv(t, 0, -10, 10, -20, 13, 0, 20, 0, 30, -10), 0, 0);
                p.r("blade", cv(t, 0, 105, 10, 60, 12, 40, 13, 5, 20, 5, 25, 60, 27, 40, 30, 105), 0, cv(t, 24, 6, 26, 40, 28, -10, 30, 6));
                p.r("armR", cv(t, 0, -12, 10, -175, 11.5f, -180, 13, -50, 18, -30, 30, -12), 0, cv(t, 0, 12, 10, -25, 13, -20, 20, 25, 30, 12));
                p.r("foreR", cv(t, 0, -22, 10, -40, 13, -10, 30, -22), 0, 0);
                p.r("chest", cv(t, 0, 8, 10, -18, 11.5f, -20, 13, 38, 20, 34, 30, 8), 0, 0);
                p.r("head", cv(t, 0, -10, 10, -30, 13, -40, 20, -38, 26, -10, 30, -10), 0, cv(t, 0, 16, 10, 0, 20, 0, 27, 40, 30, 16));
                p.mv("root", 0, cv(t, 0, 0, 10, -1.5f, 12, -1.6f, 13, 2.6f, 20, 2.4f, 30, 0), cv(t, 11, 0, 13, -2, 30, 0));
                p.r("legL", cv(t, 0, 8, 10, 10, 13, -48, 20, -48, 30, 8), 0, -9);
                p.r("shinL", cv(t, 0, 0, 13, 50, 20, 50, 30, 0), 0, 0);
                p.r("legR", cv(t, 0, -6, 10, -4, 13, 30, 20, 30, 30, -6), 0, 7);
                p.r("shinR", cv(t, 0, 4, 13, 30, 20, 30, 30, 4), 0, 0);
            }
            case "sweep" -> {
                // cleaver held out low to the left 0-9, whips across 10-12 (hit 11) with the whole body, overshoot, return
                p.r("armL", cv(t, 0, 8, 8, -85, 10, -90, 12, -88, 17, -80, 26, 8), cv(t, 0, 0, 8, -105, 9.5f, -110, 11, 10, 12.5f, 75, 17, 85, 26, 0), cv(t, 0, -10, 26, -10));
                p.r("foreL", cv(t, 0, -10, 8, 0, 26, -10), 0, 0);
                p.r("blade", cv(t, 0, 105, 8, 90, 17, 90, 26, 105), 0, cv(t, 9, 0, 12, 20, 26, 6));
                p.r("chest", cv(t, 0, 8, 8, 14, 12, 16, 26, 8), cv(t, 0, 0, 8, -45, 9.5f, -50, 11.5f, 40, 13, 58, 18, 55, 26, 0), cv(t, 8, 0, 12, 8, 26, 0));
                p.r("hips", -2, cv(t, 0, 0, 8, -20, 12, 25, 18, 22, 26, 0), 0);
                p.r("head", -10, cv(t, 0, 0, 8, 35, 12, -30, 18, -45, 26, 0), cv(t, 0, 16, 8, 25, 12, -6, 22, 30, 26, 16));
                p.r("armR", cv(t, 0, -12, 8, -40, 12, 30, 26, -12), 0, cv(t, 0, 12, 8, 40, 12, 60, 26, 12));
                p.mv("root", 0, cv(t, 0, 0, 8, 2.2f, 12, 2.6f, 20, 2, 26, 0), 0);
                p.r("legL", cv(t, 0, 8, 8, -30, 18, -30, 26, 8), 0, cv(t, 0, -9, 8, -20, 26, -9));
                p.r("shinL", cv(t, 0, 0, 8, 40, 18, 40, 26, 0), 0, 0);
                p.r("legR", cv(t, 0, -6, 8, 20, 18, 25, 26, -6), 0, cv(t, 0, 7, 8, 22, 26, 7));
                p.r("shinR", cv(t, 0, 4, 8, 30, 26, 4), 0, 0);
            }
            case "rising_slash" -> {
                // drag crouch 0-9 (blade scraping behind), up-cut 10-13 (hit 12), airborne 13-20, land 20-28
                p.r("armL", cv(t, 0, 8, 8, 55, 10, 60, 12, -150, 14, -175, 20, -160, 28, 8), cv(t, 0, 0, 12, 10, 28, 0), cv(t, 0, -10, 8, -25, 12, 5, 28, -10));
                p.r("foreL", cv(t, 0, -10, 8, 0, 14, -10, 28, -10), 0, 0);
                p.r("blade", cv(t, 0, 105, 8, 140, 10, 140, 12, 95, 14, 75, 22, 80, 28, 105), 0, 6);
                p.r("chest", cv(t, 0, 8, 8, 45, 10, 48, 12, -15, 14, -22, 20, -10, 24, 15, 28, 8), cv(t, 0, 0, 8, -30, 12, 20, 28, 0), 0);
                p.r("head", cv(t, 0, -10, 8, -45, 12, -10, 14, -20, 28, -10), cv(t, 0, 0, 8, 20, 12, -10, 28, 0), cv(t, 0, 16, 8, 30, 14, 0, 28, 16));
                p.r("armR", cv(t, 0, -12, 8, 40, 12, -40, 14, -70, 28, -12), 0, cv(t, 0, 12, 8, 20, 14, 50, 28, 12));
                p.mv("root", 0, cv(t, 0, 0, 8, 4.2f, 10, 4.5f, 12, -1, 14, -3, 18, -2.5f, 21, 1.5f, 28, 0), 0);
                p.r("legR", cv(t, 0, -6, 8, -75, 12, 10, 14, 25, 19, -20, 22, -30, 28, -6), 0, 7);
                p.r("shinR", cv(t, 0, 4, 8, 110, 12, 20, 14, 60, 22, 40, 28, 4), 0, 0);
                p.r("legL", cv(t, 0, 8, 8, -10, 12, -20, 14, -60, 19, -40, 22, 0, 28, 8), 0, -9);
                p.r("shinL", cv(t, 0, 0, 8, 100, 12, 20, 14, 80, 22, 30, 28, 0), 0, 0);
            }
            case "tornado" -> {
                // wind 0-10 (crouch, arms out), spin 10-44 (4 turns, root yaw), dizzy-free eerie stop 44-54
                float spin = Anim.linear(t, 10, 0, 14, 120, 40, 1320, 44, 1440);
                float on = c.seg(8, 11) * (1 - c.seg(42, 46));
                p.r("root", 0, -spin, 0);
                p.r("armL", -88 * on + cv(t, 0, 8, 10, 30, 44, 30, 54, 8) * (1 - on), 0, -10 - 75 * on + 5 * Anim.sin(t * 50) * on);
                p.r("armR", -80 * on - 12 * (1 - on), 0, 12 + 70 * on);
                p.r("foreL", -10 * (1 - on), 0, 0);
                p.r("foreR", -22 * (1 - on), 0, 0);
                p.r("blade", 105 - 15 * on, -90 * on, 6 + 80 * on);
                claws(p, 30 * on, -20 * on);
                p.r("chest", 8 + cv(t, 0, 0, 10, 22, 14, 6, 44, 6, 48, 18, 54, 0), cv(t, 0, 0, 10, 40, 14, 0), on * 6);
                p.r("head", -10 + 10 * on, 0, 16 + 25 * on);
                p.mv("root", 0, cv(t, 0, 0, 10, 2.6f, 14, 0.6f, 44, 0.6f, 47, 2, 54, 0) + on * Anim.sin(t * 90) * 0.3f, 0);
                p.r("legR", cv(t, 0, -6, 10, -30, 14, -10, 44, -10, 54, -6), 0, 7 + 8 * on);
                p.r("legL", cv(t, 0, 8, 10, -30, 14, 10, 44, 10, 54, 8), 0, -9 - 8 * on);
                p.r("shinR", cv(t, 0, 4, 10, 40, 14, 10, 54, 4), 0, 0);
                p.r("shinL", cv(t, 0, 0, 10, 40, 14, 10, 54, 0), 0, 0);
                p.r("skirtHem", -on * 8, 0, 0);
                p.mv("skirtHem", 0, -on * 0.8f, 0);
                p.r("bobBack", 3 + on * 25, 0, 0);
                for (String k : new String[] {"R", "L"}) p.r("spk2" + k, 0, 0, (k.equals("R") ? 1 : -1) * on * 22);
            }
            case "blade_wave" -> {
                // high wind-up behind left 0-11, diagonal slash down-right (wave at 14), reverse up-cut (wave at 22), recover
                p.r("armL", cv(t, 0, 8, 10, -170, 12, -175, 14, -40, 17, -30, 20, -70, 22, -165, 25, -150, 32, 8), cv(t, 0, 0, 10, -30, 14, 50, 18, 55, 22, -20, 32, 0), cv(t, 0, -10, 10, -40, 14, 20, 18, 22, 22, -30, 32, -10));
                p.r("foreL", cv(t, 0, -10, 10, -40, 14, 0, 20, -10, 22, 0, 32, -10), 0, 0);
                p.r("blade", cv(t, 0, 105, 10, 70, 14, 85, 20, 95, 22, 85, 32, 105), 0, cv(t, 0, 6, 14, 30, 22, -20, 32, 6));
                p.r("chest", cv(t, 0, 8, 10, -16, 14, 30, 19, 26, 22, -8, 26, 0, 32, 8), cv(t, 0, 0, 10, -35, 14, 40, 19, 38, 22, -30, 32, 0), cv(t, 10, -6, 14, 10, 22, -8, 32, 0));
                p.r("head", cv(t, 0, -10, 14, -30, 22, -15, 32, -10), cv(t, 0, 0, 10, 30, 14, -30, 22, 20, 32, 0), cv(t, 0, 16, 10, 30, 14, 0, 22, 25, 32, 16));
                p.r("armR", cv(t, 0, -12, 10, 20, 14, -60, 22, 30, 32, -12), 0, cv(t, 0, 12, 10, 40, 14, 20, 22, 50, 32, 12));
                p.mv("root", 0, cv(t, 0, 0, 10, -1, 14, 2.2f, 20, 1.6f, 22, 0.8f, 32, 0), cv(t, 12, 0, 14, -1.5f, 32, 0));
                p.r("legL", cv(t, 0, 8, 12, 8, 14, -40, 22, -35, 32, 8), 0, -9);
                p.r("shinL", cv(t, 0, 0, 14, 45, 22, 30, 32, 0), 0, 0);
                p.r("legR", cv(t, 0, -6, 14, 20, 22, 15, 32, -6), 0, 7);
            }
            case "cleaver_throw" -> {
                // overhand wind 0-11, throw 13 (blade leaves the hand), eerie beckoning wait 15-42, catch 46
                p.r("armL", cv(t, 0, 8, 10, -200, 12, -205, 14, -50, 18, -35, 24, 0, 40, 0, 44, -110, 46, -120, 48, -60, 50, 8), cv(t, 0, 0, 14, 20, 24, 0), cv(t, 0, -10, 10, -20, 14, 10, 24, -10, 44, -25, 50, -10));
                p.r("foreL", cv(t, 0, -10, 10, -60, 13, 0, 24, -10, 44, -10, 46, -40, 50, -10), 0, 0);
                p.r("blade", 105, 0, 6);
                p.r("chest", cv(t, 0, 8, 10, -20, 13, 36, 17, 30, 24, 4, 42, 4, 46, 14, 50, 8), cv(t, 0, 0, 10, -40, 13, 40, 18, 35, 26, 0), 0);
                p.r("head", cv(t, 0, -10, 10, -25, 13, -30, 24, -12, 42, -12, 50, -10), cv(t, 0, 0, 10, 25, 13, -20, 24, 0), cv(t, 0, 16, 13, 0, 24, 45, 40, 50, 46, 10, 50, 16));
                // beckoning claw (fingers curl one after the other)
                float beck = t > 22 && t < 42 ? 1 : 0;
                p.r("armR", cv(t, 0, -12, 10, 30, 13, -40, 20, -60, 42, -60, 50, -12), cv(t, 20, 0, 24, 30, 42, 30, 50, 0), cv(t, 0, 12, 13, 20, 24, -10, 42, -10, 50, 12));
                p.r("foreR", cv(t, 0, -22, 20, -70, 42, -70, 50, -22), 0, 0);
                for (int i = 0; i < 4; i++) {
                    float b = beck * Math.max(0, Anim.sin((t - 22) * 30 - i * 40)) * 70;
                    p.ar(CL[i], -b * 0.6f, 0, 0);
                    p.ar(CL[i] + "t", -b, 0, 0);
                }
                p.mv("root", 0, cv(t, 0, 0, 10, -0.8f, 13, 1.8f, 20, 0, 44, 0, 46, 1.2f, 50, 0), cv(t, 11, 0, 13, -1.5f, 24, 0));
                p.r("legL", cv(t, 0, 8, 11, 10, 13, -40, 20, -15, 30, 8), 0, -9);
                p.r("shinL", cv(t, 0, 0, 13, 40, 20, 10, 30, 0), 0, 0);
                p.r("legR", cv(t, 0, -6, 10, -15, 13, 20, 24, -6), 0, 7);
            }
            case "claw_flurry" -> {
                // four swipes: 8 (high->low), 13 (low->high), 18 (horizontal), 24 (thrust)
                p.r("armR", cv(t, 0, -12, 5, -160, 7.5f, -150, 8.5f, -40, 10, -20, 12, -40, 13.5f, -150, 15, -140, 17, -90, 18.5f, -95, 21, 20, 23.5f, -95, 26, -92, 32, -12),
                        cv(t, 12, 0, 16, 30, 17, 60, 18.5f, -50, 21, 0, 32, 0),
                        cv(t, 0, 12, 5, 40, 8.5f, -45, 10, -50, 12, -45, 13.5f, 45, 15, 40, 18.5f, 0, 23.5f, 0, 32, 12));
                p.r("foreR", cv(t, 0, -22, 5, -40, 8.5f, 0, 12, -10, 13.5f, 0, 17, -20, 18.5f, 0, 21, -80, 23.5f, 0, 28, 0, 32, -22), 0, 0);
                claws(p, cv(t, 0, 0, 5, 40, 23, 35, 24, 0, 32, 0), cv(t, 0, 0, 5, -25, 22, -25, 23.5f, 10, 32, 0));
                p.r("chest", cv(t, 0, 8, 8, 20, 13, 0, 18, 14, 21, 5, 24, 32, 28, 28, 32, 8), cv(t, 0, 0, 5, 25, 8.5f, -25, 12, -28, 13.5f, 25, 17, 35, 18.5f, -35, 21, 30, 24, -10, 32, 0), cv(t, 0, 0, 8, 6, 13, -8, 18, 0));
                p.r("hips", -2, cv(t, 0, 0, 8, -12, 13, 12, 18, -15, 24, 0), 0);
                p.r("head", cv(t, 0, -10, 24, -25, 32, -10), cv(t, 0, 0, 8, 15, 13, -15, 18, 20, 24, 0), cv(t, 0, 16, 8, 30, 13, 0, 18, 30, 24, 10, 32, 16));
                p.r("armL", cv(t, 0, 8, 8, 25, 13, 0, 18, 25, 24, 35, 32, 8), 0, -10);
                p.mv("root", 0, cv(t, 0, 0, 6, 1.5f, 24, 2.4f, 32, 0), cv(t, 20, 0, 24, -1.8f, 32, 0));
                p.r("legR", cv(t, 0, -6, 8, -30, 13, 10, 18, -25, 24, -45, 32, -6), 0, 7);
                p.r("shinR", cv(t, 0, 4, 8, 35, 13, 10, 18, 35, 24, 50, 32, 4), 0, 0);
                p.r("legL", cv(t, 0, 8, 8, 20, 13, -20, 18, 20, 24, 25, 32, 8), 0, -9);
                p.r("shinL", cv(t, 0, 0, 13, 30, 18, 5, 24, 15, 32, 0), 0, 0);
            }
            case "shadow_step" -> {
                // sink 0-8, rise behind the victim 8-14, cock the blade 14-17, stab 18, twist & withdraw 20-34
                shadow(p, t);
                float st = c.seg(13, 15);
                p.r("armL", Anim.lerp(p.get("armL", 0), cv(t, 13, 30, 16, 45, 17.5f, -88, 20, -85, 26, -85, 30, -20, 34, 8), st), 0, Anim.lerp(p.get("armL", 2), -10, st));
                p.r("foreL", cv(t, 13, -10, 16, -60, 17.5f, 0, 30, 0, 34, -10), 0, 0);
                p.r("blade", cv(t, 0, 105, 13, 105, 16, 90, 17.5f, 88, 30, 88, 34, 105), 0, cv(t, 20, 6, 24, 95, 28, 95, 31, 6));
                p.r("chest", Anim.lerp(p.get("chest", 0), cv(t, 13, 8, 16, -5, 17.5f, 30, 26, 28, 34, 8), st), cv(t, 13, 0, 16, -30, 17.5f, 15, 26, 10, 34, 0), 0);
                p.r("head", Anim.lerp(p.get("head", 0), cv(t, 13, -10, 18, -30, 26, -35, 34, -10), st), 0, Anim.lerp(p.get("head", 2), cv(t, 13, 30, 18, 10, 24, 40, 34, 16), st));
                p.r("armR", Anim.lerp(p.get("armR", 0), cv(t, 13, -12, 16, -60, 18, -30, 34, -12), st), 0, Anim.lerp(p.get("armR", 2), cv(t, 13, 12, 18, 30, 34, 12), st));
                claws(p, cv(t, 13, 0, 16, 40, 26, 40, 34, 0), 0);
                p.am("root", 0, st * cv(t, 13, 0, 17.5f, 1.8f, 26, 1.6f, 34, 0), st * cv(t, 15, 0, 17.5f, -1.8f, 34, 0));
                p.r("legL", st * cv(t, 13, 8, 17.5f, -42, 26, -42, 34, 8), 0, -9);
                p.r("shinL", st * cv(t, 13, 0, 17.5f, 45, 26, 45, 34, 0), 0, 0);
                p.r("legR", st * cv(t, 13, -6, 17.5f, 25, 26, 25, 34, -6), 0, 7);
            }
            case "cross_cut" -> {
                // arms crossed in an X high in front 0-9, both tear outward 10-12 (hits 11/13), held flared 13-20, recover
                p.r("armR", cv(t, 0, -12, 8, -150, 10, -155, 12, -40, 20, -35, 30, -12), cv(t, 0, 0, 8, 30, 12, -20, 30, 0), cv(t, 0, 12, 8, -40, 10, -45, 12, 75, 20, 70, 30, 12));
                p.r("armL", cv(t, 0, 8, 8, -150, 10, -155, 13, -40, 20, -35, 30, 8), cv(t, 0, 0, 8, -30, 13, 20, 30, 0), cv(t, 0, -10, 8, 40, 10, 45, 13, -75, 20, -70, 30, -10));
                p.r("foreR", cv(t, 0, -22, 8, -30, 12, 0, 30, -22), 0, 0);
                p.r("foreL", cv(t, 0, -10, 8, -30, 13, 0, 30, -10), 0, 0);
                p.r("blade", cv(t, 0, 105, 8, 60, 13, 90, 20, 90, 30, 105), 0, cv(t, 0, 6, 13, 30, 30, 6));
                claws(p, cv(t, 0, 0, 8, -10, 12, 45, 20, 40, 30, 0), cv(t, 0, 0, 8, 30, 12, -20, 30, 0));
                p.r("chest", cv(t, 0, 8, 8, 30, 10, 32, 12, 0, 14, -8, 20, -5, 30, 8), 0, 0);
                p.r("head", cv(t, 0, -10, 8, 15, 10, 18, 12, -30, 20, -25, 30, -10), 0, cv(t, 0, 16, 8, 0, 12, 0, 18, 45, 30, 16));
                p.mv("root", 0, cv(t, 0, 0, 8, 3, 10, 3.2f, 12, 0.5f, 20, 0.8f, 30, 0), 0);
                p.r("legR", cv(t, 0, -6, 8, -40, 12, -10, 30, -6), 0, cv(t, 0, 7, 12, 16, 30, 7));
                p.r("shinR", cv(t, 0, 4, 8, 60, 12, 10, 30, 4), 0, 0);
                p.r("legL", cv(t, 0, 8, 8, -30, 12, 5, 30, 8), 0, cv(t, 0, -9, 12, -18, 30, -9));
                p.r("shinL", cv(t, 0, 0, 8, 55, 12, 10, 30, 0), 0, 0);
            }
            case "execution" -> {
                // 0-14 shadow step, 16 horizontal cross slash, 26 launcher, 30 leap, 32-42 front flip, 46 plunge, 46-62 kneel, 62-80 rise + blood flick
                if (t < 15) { shadow(p, t); break; }
                float flip = Anim.linear(t, 32, 0, 42, 360);
                p.r("root", t > 31 && t < 43 ? flip : 0, 0, 0);
                p.mv("root", 0, cv(t, 14, 0, 16, 1.6f, 24, 2.6f, 26, -0.5f, 29, 2.5f, 31, -1, 44, -1, 46, 6, 58, 6, 66, 1, 80, 0), 0);
                p.r("armR", cv(t, 14, -12, 15, -80, 16.5f, -90, 18, -85, 22, 30, 26, -150, 30, -60, 46, -40, 62, -30, 80, -12),
                        cv(t, 14, 0, 15, -80, 16.5f, 60, 19, 70, 22, 0), cv(t, 14, 12, 26, 30, 46, 50, 80, 12));
                p.r("armL", cv(t, 14, 8, 15, -90, 16.5f, -95, 19, -90, 22, 50, 25, 60, 26.5f, -160, 30, -180, 44, -190, 46, -60, 58, -55, 66, -60, 70, -40, 72, -70, 80, 8),
                        cv(t, 14, 0, 15, -100, 16.5f, 60, 19, 80, 22, 0), cv(t, 14, -10, 26, 0, 72, -20, 80, -10));
                p.r("foreL", cv(t, 14, -10, 46, -20, 47, 0, 80, -10), 0, 0);
                p.r("blade", cv(t, 14, 105, 15, 90, 19, 90, 22, 140, 26, 95, 30, 50, 44, 40, 46, 0, 58, 0, 66, 60, 70, 100, 72, 140, 76, 105), 0, cv(t, 66, 6, 70, 30, 72, -40, 80, 6));
                claws(p, cv(t, 14, 0, 16, 40, 26, 30, 46, 40, 80, 0), cv(t, 14, 0, 46, -10, 62, 20, 80, 0));
                p.r("chest", cv(t, 14, 8, 15, 20, 16.5f, 10, 22, 45, 26, -20, 30, 10, 42, 30, 46, 50, 58, 48, 66, 20, 80, 8),
                        cv(t, 14, 0, 15, -50, 16.5f, 45, 20, 50, 22, 0), 0);
                p.r("head", cv(t, 14, -10, 22, -40, 26, -20, 46, -45, 58, -40, 64, 0, 70, -20, 80, -10), 0, cv(t, 14, 16, 26, 0, 46, 0, 58, 10, 64, 85, 72, 80, 80, 16));
                p.r("legR", cv(t, 14, -6, 16, -30, 22, -70, 26, 10, 30, 20, 32, -80, 42, -80, 46, -70, 58, -70, 66, -20, 80, -6), 0, 7);
                p.r("shinR", cv(t, 14, 4, 22, 100, 26, 20, 32, 110, 42, 110, 46, 90, 58, 90, 66, 30, 80, 4), 0, 0);
                p.r("legL", cv(t, 14, 8, 16, 20, 22, -40, 26, -20, 32, -80, 42, -80, 46, 10, 58, 10, 66, 5, 80, 8), 0, -9);
                p.r("shinL", cv(t, 14, 0, 22, 90, 26, 30, 32, 110, 42, 110, 46, 100, 58, 100, 66, 20, 80, 0), 0, 0);
            }
            default -> {}
        }
    }

    static void death(BloomiePose p, AnimCtx c) {
        float d = c.death;
        float jolt = Anim.curve(d, 0, 0, 0.1f, 1, 0.3f, 0.3f);
        float drop = Anim.easeIn(Anim.clamp(d / 0.35f, 0, 1));           // cleaver slips & falls (then hidden)
        float buckle = Anim.smooth((d - 0.25f) / 0.3f);
        float fall = Anim.easeIn(Anim.clamp((d - 0.5f) / 0.35f, 0, 1));
        float twitch = d > 0.85f ? Anim.sin(d * 4000) * (1 - d) * 50 : 0;
        p.ar("head", 20 * jolt, 0, 70 * buckle);                          // head lolls sideways
        p.ar("chest", -20 * jolt + 25 * buckle, 0, -10 * buckle);
        p.ar("blade", 60 * drop, 0, 80 * drop);
        p.am("blade", 0, 6 * drop, 0);
        p.ar("armL", 20 * buckle, 0, -20 * buckle);
        p.ar("armR", -40 * jolt + 30 * buckle, 0, 25 * buckle);
        claws(p, 30 * jolt, -40 * jolt + 60 * buckle + twitch);
        p.ar("legR", -50 * buckle * (1 - fall * 0.7f), 0, 0);
        p.ar("shinR", 80 * buckle * (1 - fall * 0.7f), 0, 0);
        p.ar("legL", -20 * buckle, 0, -10 * buckle);
        p.ar("shinL", 40 * buckle * (1 - fall * 0.5f), 0, 0);
        p.am("root", 0, 3.2f * buckle * (1 - fall) - 1.6f * fall, 0);
        p.ar("root", 0, 0, -84 * fall);                                    // keels over sideways
        p.ar("knot", 0, 0, 30 * fall);
    }
}
