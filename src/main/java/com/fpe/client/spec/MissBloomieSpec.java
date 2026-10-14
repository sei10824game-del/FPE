package com.fpe.client.spec;

import com.fpe.client.model.Anim;
import com.fpe.client.model.AnimCtx;
import com.fpe.client.model.ModelParts;
import com.fpe.client.model.ModelSpec;
import com.fpe.client.model.ModelSpec.Face;
import com.fpe.client.model.ModelSpec.Pattern;

/**
 * Miss Bloomie: messy dark hair crowned with A/B/C blocks + spiral antenna, sharp grin, pale collared dress with a
 * torn hem, black arms, one enormous shard-claw (right), pointed boots. Animation keyed to entity/characters/MissBloomie.
 */
public final class MissBloomieSpec {
    private MissBloomieSpec() {}

    static final int DRESS = 0xDCDCD6, DRESS_SH = 0xBFC2C2, PANEL = 0x9EA5AA, WHITE = 0xF4F4F0, SKIN = 0xE8E6E0,
            HAIR = 0x2A2733, HAIR_HI = 0x3B3746, ARM = 0x1D1B24, CLAW = 0x23202C, CLAW_HI = 0x4A4560, BOOT = 0x29262F,
            BLOCK = 0xB2B7BC, INK = 0x2E2B3A, MOUTH = 0x140F18;

    public static final ModelSpec SPEC = build();

    private static void glyph(ModelSpec.Part p, String... rows) {
        for (int y = 0; y < rows.length; y++) for (int x = 0; x < rows[y].length(); x++)
            if (rows[y].charAt(x) == '#') { p.decor(Face.FRONT, x, y, 1, 1, INK); p.decor(Face.BACK, 3 - x, y, 1, 1, INK); }
    }

    private static ModelSpec build() {
        ModelSpec m = new ModelSpec("miss_bloomie");
        m.group("root", null, 0, 24, 0);
        m.group("hips", "root", 0, 13, 0);

        // ---------------------------------------------------------------- legs + boots
        for (int s = -1; s <= 1; s += 2) {
            String k = s < 0 ? "R" : "L";
            float x = s * 1.5f;
            m.part("leg" + k, "hips", x, 13.5f, 0, -1, 0, -1, 2, 6, 2, SKIN).grain(0.03f);
            m.part("shin" + k, "leg" + k, x, 19.5f, 0, -1, 0, -1, 2, 4.5f, 2, SKIN).grain(0.03f);
            m.part("boot" + k, "shin" + k, x, 21, 0, -1.5f, 0, -1.9f, 3, 3, 3.6f, BOOT).decor(Face.FRONT, 0, 2, 3, 1, 0x1A1820);
            m.part("cuff" + k, "boot" + k, x, 21, 0, -1.8f, -0.6f, -2.1f, 3.6f, 1.2f, 4, 0x34303C).decor(Face.FRONT, 1, 0, 2, 1, 0x1A1820);
            m.part("toe" + k, "boot" + k, x, 23, -1.9f, -1, -1, -2.2f, 2, 2, 2.4f, BOOT).rot(-12, 0, 0);
            m.part("toeTip" + k, "toe" + k, x, 23.2f, -4.0f, -0.5f, -0.6f, -1.6f, 1, 1, 1.8f, 0x1A1820).rot(-10, 0, 0);
        }

        // ---------------------------------------------------------------- skirt with torn hem (hangs from the hips)
        m.part("skirtTop", "hips", 0, 12, 0, -3.5f, 0, -2.5f, 7, 2.5f, 5, DRESS).decor(Face.FRONT, 0, 0, 7, 1, DRESS_SH);
        m.part("skirtMid", "skirtTop", 0, 14.5f, 0, -4.5f, 0, -3, 9, 3, 6, DRESS)
                .decor(Face.FRONT, 5, 0, 4, 1, PANEL).decor(Face.FRONT, 4, 1, 5, 1, PANEL).decor(Face.FRONT, 3, 2, 6, 1, PANEL)
                .decor(Face.LEFT, 0, 0, 6, 3, PANEL);
        m.part("skirtHem", "skirtMid", 0, 17.5f, 0, -5.5f, 0, -3.5f, 11, 3, 7, DRESS)
                .decor(Face.FRONT, 2, 0, 9, 1, PANEL).decor(Face.FRONT, 1, 1, 10, 1, PANEL).decor(Face.FRONT, 0, 2, 11, 1, DRESS_SH)
                .decor(Face.LEFT, 0, 0, 7, 3, PANEL).decor(Face.BACK, 0, 2, 11, 1, DRESS_SH).decor(Face.RIGHT, 0, 2, 7, 1, DRESS_SH);
        float[][] rags = {{-4.6f, -3.5f}, {-1.8f, -3.5f}, {1.2f, -3.5f}, {4.0f, -3.5f}, {-3.6f, 3.5f}, {-0.4f, 3.5f}, {2.8f, 3.5f}};
        for (int i = 0; i < rags.length; i++)
            m.part("rag" + i, "skirtHem", rags[i][0], 20.5f, rags[i][1], -1, -1, -0.35f, 2, 2, 0.7f, i == 2 || i == 3 ? PANEL : DRESS)
                    .rot(0, 0, 45 + (i % 2) * 8);
        for (int i = 0; i < 4; i++)
            m.part("ragS" + i, "skirtHem", i < 2 ? -5.5f : 5.5f, 20.5f, i % 2 == 0 ? -1.6f : 1.8f, -0.35f, -1, -1, 0.7f, 2, 2, i >= 2 ? PANEL : DRESS)
                    .rot(45 + (i % 2) * 10, 0, 0);

        // ---------------------------------------------------------------- torso
        m.group("torso", "hips", 0, 12, 0);
        m.part("chest", "torso", 0, 12, 0, -3, -6, -2, 6, 6, 4, DRESS)
                .decor(Face.FRONT, 0, 5, 6, 1, DRESS_SH)                              // waist seam
                .decor(Face.FRONT, 2, 2, 2, 2, 0xA6AAAE).decor(Face.FRONT, 2, 2, 1, 1, 0x7E8286) // oval pendant
                .decor(Face.FRONT, 1, 0, 4, 1, 0xC8CACA).decor(Face.BACK, 0, 5, 6, 1, DRESS_SH);
        m.part("collarBand", "chest", 0, 6.2f, 0, -2.3f, -1, -1.7f, 4.6f, 1.3f, 3.4f, WHITE);
        m.part("collarR", "chest", -0.9f, 6.2f, -2.05f, -2.2f, -0.3f, -0.3f, 2.4f, 1.8f, 0.6f, WHITE).rot(0, 0, -28).decor(Face.FRONT, 0, 1, 1, 1, 0xC8C8C4);
        m.part("collarL", "chest", 0.9f, 6.2f, -2.05f, -0.2f, -0.3f, -0.3f, 2.4f, 1.8f, 0.6f, WHITE).rot(0, 0, 28).decor(Face.FRONT, 1, 1, 1, 1, 0xC8C8C4);

        // ---------------------------------------------------------------- head
        m.part("neck", "chest", 0, 6, 0, -1, -1.2f, -1, 2, 1.4f, 2, SKIN);
        m.part("head", "neck", 0, 5.2f, 0, -3.5f, -7, -3.5f, 7, 7, 7, SKIN)
                .decor(Face.FRONT, 0, 0, 7, 1, 0xB9B7B2)                               // hair shadow
                .decor(Face.FRONT, 1, 2, 2, 1, MOUTH).decor(Face.FRONT, 4, 2, 2, 1, MOUTH)  // sunken eyes
                .decorGlow(Face.FRONT, 2, 2, 1, 1, 0xF4F2FF).decorGlow(Face.FRONT, 4, 2, 1, 1, 0xF4F2FF)
                .decor(Face.FRONT, 0, 3, 1, 1, MOUTH).decor(Face.FRONT, 6, 3, 1, 1, MOUTH)  // grin corners
                .decor(Face.FRONT, 0, 4, 7, 3, MOUTH)
                .decor(Face.FRONT, 1, 4, 1, 1, WHITE).decor(Face.FRONT, 2, 3, 1, 1, MOUTH).decor(Face.FRONT, 3, 4, 1, 1, WHITE)
                .decor(Face.FRONT, 4, 3, 1, 1, MOUTH).decor(Face.FRONT, 5, 4, 1, 1, WHITE)   // upper fangs
                .decor(Face.FRONT, 2, 6, 3, 1, 0x8E1E2A);                                    // tongue (seen when the jaw drops)
        // jaw plate with the lower fangs: drops open for screech/laugh
        m.part("jaw", "head", 0, 3.2f, -3.5f, -3.0f, 0, -0.4f, 6, 2, 0.6f, SKIN)
                .decor(Face.FRONT, 0, 0, 6, 1, MOUTH).decor(Face.FRONT, 1, 0, 1, 1, WHITE).decor(Face.FRONT, 3, 0, 1, 1, WHITE).decor(Face.FRONT, 5, 0, 1, 1, WHITE);

        // ---------------------------------------------------------------- hair
        m.part("hairCap", "head", 0, -1.8f, 0, -4, -1.6f, -4, 8, 3, 8, HAIR).pattern(Pattern.DIAG, HAIR_HI, 3).grain(0.08f);
        m.part("hairBackMass", "head", 0, -0.5f, 2.6f, -4, 0, -0.5f, 8, 5, 1.6f, HAIR).pattern(Pattern.STRIPE_V, HAIR_HI, 2);
        float[][] bangs = {{-2.8f, 2.4f, 14}, {-1.0f, 1.2f, 4}, {0.9f, 2.8f, -6}, {2.7f, 1.6f, -16}};
        for (int i = 0; i < bangs.length; i++)
            m.part("bang" + i, "head", bangs[i][0], -0.6f, -4.0f, -0.8f, 0, -0.5f, 1.6f, bangs[i][1], 1, HAIR).rot(-12, 0, bangs[i][2]);
        for (int s = -1; s <= 1; s += 2) {
            String k = s < 0 ? "R" : "L";
            m.part("hairS1" + k, "head", s * 3.9f, -1.5f, -1.5f, -0.8f, 0, -0.8f, 1.6f, 5.5f, 1.6f, HAIR).rot(-5, 0, -s * 18);
            m.part("hairS2" + k, "head", s * 3.9f, -1.8f, 1.2f, -0.8f, 0, -0.8f, 1.6f, 4.5f, 1.6f, HAIR).rot(15, 0, -s * 38);
            m.part("hairS3" + k, "head", s * 3.6f, -2.8f, -0.5f, -0.7f, -3.5f, -0.7f, 1.4f, 3.5f, 1.4f, HAIR).rot(0, 0, s * 55);
            m.part("hairS4" + k, "head", s * 3.6f, 0.6f, -2.6f, -0.6f, 0, -0.6f, 1.2f, 4, 1.2f, HAIR_HI).rot(-15, 0, -s * 26);
        }
        m.part("hairSideR", "head", -3.9f, -1.8f, 0, -0.4f, 0, -3.0f, 1, 4.5f, 6.6f, HAIR).pattern(Pattern.STRIPE_H, HAIR_HI, 2);
        m.part("hairSideL", "head", 3.9f, -1.8f, 0, -0.6f, 0, -3.0f, 1, 4.5f, 6.6f, HAIR).pattern(Pattern.STRIPE_H, HAIR_HI, 2);
        m.group("hairBack", "head", 0, -1.5f, 3.4f);
        float[][] back = {{-3.2f, 7, -18}, {-1.2f, 8.5f, -6}, {1.0f, 8, 7}, {3.0f, 6.5f, 20}, {-2.2f, 5.5f, -30}, {2.2f, 5.5f, 32}};
        for (int i = 0; i < back.length; i++)
            m.part("hB" + i, "hairBack", back[i][0], -1.0f, 3.4f + (i >= 4 ? 0.4f : 0), -0.9f, 0, -0.8f, 1.8f, back[i][1], 1.6f, i % 2 == 0 ? HAIR : HAIR_HI)
                    .rot(22 + (i % 3) * 4, 0, back[i][2]);
        m.part("hTop0", "head", -1.5f, -3.2f, 1, -0.7f, -3, -0.7f, 1.4f, 3, 1.4f, HAIR).rot(-25, 0, -20);
        m.part("hTop1", "head", 1.8f, -3.2f, 1.5f, -0.7f, -2.5f, -0.7f, 1.4f, 2.5f, 1.4f, HAIR).rot(-35, 0, 25);

        // ---------------------------------------------------------------- crown: A B C blocks + spiral antenna
        m.group("crown", "head", 0, -3.2f, -1.2f);
        glyph(m.part("blkA", "crown", -3.2f, -3.0f, -1.2f, -2, -4, -2, 4, 4, 4, BLOCK).grain(0.08f).rot(-8, 18, -22), ".##.", "#..#", "####", "#..#");
        glyph(m.part("blkB", "crown", 0, -3.8f, -1.6f, -2, -4, -2, 4, 4, 4, BLOCK).grain(0.08f).rot(-8, 0, 0), "###.", "#.##", "#..#", "###.");
        glyph(m.part("blkC", "crown", 3.2f, -3.0f, -1.2f, -2, -4, -2, 4, 4, 4, BLOCK).grain(0.08f).rot(-8, -18, 22), ".###", "#...", "#...", ".###");
        m.part("antenna", "head", -2.6f, -6.0f, 1.2f, -0.45f, -3.5f, -0.45f, 0.9f, 3.5f, 0.9f, HAIR).rot(0, 0, 14);
        m.group("spiral", "antenna", -2.6f, -9.5f, 1.2f);
        m.part("sp1", "spiral", -2.6f, -9.5f, 1.2f, -2, -1, -0.5f, 5, 1, 1, HAIR);
        m.part("sp2", "spiral", -2.6f, -9.5f, 1.2f, 2, -5, -0.5f, 1, 4, 1, HAIR);
        m.part("sp3", "spiral", -2.6f, -9.5f, 1.2f, -2, -5, -0.5f, 4, 1, 1, HAIR);
        m.part("sp4", "spiral", -2.6f, -9.5f, 1.2f, -2, -4, -0.5f, 1, 2, 1, HAIR);
        m.part("sp5", "spiral", -2.6f, -9.5f, 1.2f, -1, -3, -0.5f, 2, 1, 1, HAIR);

        // ---------------------------------------------------------------- right arm: the giant shard claw
        m.group("armR", "chest", -3.6f, 6.8f, 0);
        m.part("sleeveR", "armR", -3.6f, 6.8f, 0, -1.7f, -1, -1.7f, 3.2f, 3.2f, 3.4f, DRESS).decor(Face.FRONT, 0, 2, 4, 1, DRESS_SH).decor(Face.RIGHT, 0, 2, 4, 1, DRESS_SH);
        m.part("uArmR", "armR", -3.6f, 6.8f, 0, -1.1f, 1, -1.1f, 2.2f, 4.4f, 2.2f, ARM);
        m.part("foreR", "uArmR", -3.6f, 11.6f, 0, -1.3f, 0, -1.3f, 2.6f, 3.6f, 2.6f, ARM);
        m.part("clawR", "foreR", -3.6f, 15, 0, -2.6f, 0, -2.6f, 5.2f, 3.6f, 5.2f, CLAW).decor(Face.FRONT, 0, 0, 5, 1, CLAW_HI).decor(Face.RIGHT, 0, 0, 5, 1, CLAW_HI);
        m.part("knuckR", "clawR", -3.6f, 15, 0, -3.0f, 2.0f, -3.0f, 6, 1.8f, 6, 0x2C2836);
        float[][] fing = {{-5.8f, -1.6f, -26, -24}, {-4.4f, -2.3f, -30, -8}, {-2.8f, -2.3f, -30, 8}, {-1.4f, -1.6f, -26, 24}};
        for (int i = 0; i < 4; i++) {
            float fx = fing[i][0], fz = fing[i][1];
            m.part("cR" + i, "clawR", fx, 18.4f, fz, -1.0f, 0, -1.0f, 2, 5.6f, 2, CLAW).rot(fing[i][2], 0, fing[i][3])
                    .decor(Face.FRONT, 0, 0, 1, 4, CLAW_HI);
            m.part("cR" + i + "t", "cR" + i, fx, 23.8f, fz, -0.7f, 0, -0.7f, 1.4f, 6.4f, 1.4f, CLAW).rot(-24, 0, 0)
                    .decor(Face.FRONT, 0, 0, 1, 6, CLAW_HI).decorGlow(Face.FRONT, 0, 5, 1, 2, 0x6A5A90);
            m.part("cR" + i + "s", "cR" + i, fx, 20.5f, fz, -0.4f, -1.6f, -0.4f, 0.8f, 1.8f, 0.8f, CLAW).rot(0, 0, (i < 2 ? 1 : -1) * 40); // jagged barb
        }
        m.part("cRT", "clawR", -1.2f, 17f, 0.8f, -0.8f, 0, -0.8f, 1.6f, 5f, 1.6f, CLAW).rot(-50, 0, 30).decor(Face.FRONT, 0, 0, 1, 4, CLAW_HI);
        m.part("cRTt", "cRT", -1.2f, 21.8f, 0.8f, -0.55f, 0, -0.55f, 1.1f, 4.4f, 1.1f, CLAW).rot(-30, 0, 0).decorGlow(Face.FRONT, 0, 3, 1, 1, 0x6A5A90);
        m.part("shardR", "foreR", -4.9f, 12.2f, 0.4f, -0.5f, -3.4f, -0.5f, 1, 3.4f, 1, CLAW).rot(0, 0, 32);  // jagged spur on the forearm

        // ---------------------------------------------------------------- left arm: small black clawed hand
        m.group("armL", "chest", 3.6f, 6.8f, 0);
        m.part("sleeveL", "armL", 3.6f, 6.8f, 0, -1.5f, -1, -1.7f, 3.2f, 3.2f, 3.4f, DRESS).decor(Face.FRONT, 0, 2, 4, 1, DRESS_SH).decor(Face.LEFT, 0, 2, 4, 1, DRESS_SH);
        m.part("uArmL", "armL", 3.6f, 6.8f, 0, -0.9f, 1, -0.9f, 1.8f, 4.6f, 1.8f, ARM);
        m.part("foreL", "uArmL", 3.6f, 11.8f, 0, -0.85f, 0, -0.85f, 1.7f, 4, 1.7f, ARM);
        m.part("handL", "foreL", 3.6f, 15.6f, 0, -1, 0, -1.1f, 2, 1.8f, 2.2f, ARM);
        for (int i = 0; i < 3; i++)
            m.part("fL" + i, "handL", 3.6f + (i - 1) * 0.6f, 17.3f, -0.6f + i * 0.2f, -0.3f, 0, -0.3f, 0.6f, 1.8f, 0.6f, CLAW).rot(-15, 0, (i - 1) * -12);
        m.part("heldBlk", "handL", 3.6f, 17.6f, -0.4f, -1.6f, 0, -1.6f, 3.2f, 3.2f, 3.2f, BLOCK).decor(Face.FRONT, 1, 1, 1, 2, INK).decor(Face.FRONT, 2, 1, 1, 1, INK);

        m.animator(MissBloomieSpec::animate);
        return m;
    }

    // =================================================================== animation
    static final String[] FINGERS = {"cR0", "cR1", "cR2", "cR3"};

    static void animate(ModelParts m, AnimCtx c) {
        BloomiePose idle = new BloomiePose();
        idlePose(idle, c);
        BloomiePose p = idle;
        if (!c.idle()) {
            BloomiePose a = idle.copy();
            ability(a, c, c.t);
            float w = Anim.smooth(c.t / 3f) * (1 - Anim.smooth((c.t - (c.dur - 5)) / 5f));
            p = BloomiePose.lerp(idle, a, w);
            // secondary motion: hair / antenna / skirt lag behind the body by sampling the pose 3 ticks earlier
            BloomiePose past = idle.copy();
            ability(past, c, Math.max(0, c.t - 3));
            BloomiePose pastB = BloomiePose.lerp(idle, past, w);
            float dx = (p.get("chest", 0) - pastB.get("chest", 0)) + (p.get("root", 0) - pastB.get("root", 0)) + (p.get("hips", 0) - pastB.get("hips", 0));
            float dz = (p.get("chest", 2) - pastB.get("chest", 2)) + (p.get("hips", 2) - pastB.get("hips", 2));
            float dy = (p.get("root", 4) - pastB.get("root", 4));
            p.ar("hairBack", Anim.clamp(-dx * 0.9f - dy * 4, -50, 50), 0, Anim.clamp(-dz * 0.6f, -30, 30));
            p.ar("spiral", 0, 0, Anim.clamp(-dz * 1.2f + dx * 0.6f, -50, 50));
            p.ar("skirtHem", Anim.clamp(-dx * 0.35f + dy * 3, -25, 25), 0, Anim.clamp(-dz * 0.3f, -15, 15));
            p.ar("skirtMid", Anim.clamp(-dx * 0.15f, -12, 12), 0, 0);
        }
        if (c.death > 0) death(p, c);
        p.apply(m);
        boolean held = c.is("abc_throw") && c.t > 5 && c.t < 12.5f || c.is("alphabet_barrage") && c.t > 14 && c.t < 66 && ((int) c.t) % 4 < 2;
        m.show("heldBlk", held);
        boolean crown = !(c.is("abc_throw") && c.t > 5 && c.t < 26);
        m.show("blkB", crown);
    }

    static void idlePose(BloomiePose p, AnimCtx c) {
        float age = c.age, br = Anim.sin(age * 4.6f), w = c.walk();
        float sw = Anim.sinr(c.limbSwing * 0.6662f) * w, cw = (float) Math.cos(c.limbSwing * 0.6662f) * w;
        // hunched, head cocked, claw held up and out like the reference
        p.r("chest", 6 + br * 1.5f + w * 10, sw * 10, sw * 3);
        p.r("hips", 0, -sw * 6, 0);
        p.mv("root", 0, -Math.abs(cw) * 1.1f, 0);
        p.r("neck", -4, 0, 0);
        p.r("head", -6 - br * 1.5f - w * 8 + c.headPitch * 0.8f, c.headYaw * 0.8f, 9 + Anim.sin(age * 2.1f) * 3);
        p.r("jaw", 0, 0, 0);
        // claw arm: heavy, swings with lag while walking
        p.r("armR", -22 + br * 3 - sw * 18, 10, 24 + br * 2);
        p.r("uArmR", 0, 0, 0);
        p.r("foreR", -48 - br * 3 - cw * 8, 0, -6);
        p.r("clawR", -18, 0, 0);
        for (int i = 0; i < 4; i++) {
            float tw = Anim.sin(age * 9 + i * 70) * 4 + (((int) (age / 37)) % 3 == 0 ? Anim.sin(age * 40 + i * 90) * 6 : 0);
            p.r(FINGERS[i], tw, 0, 0);
            p.r(FINGERS[i] + "t", tw * 0.5f, 0, 0);
        }
        // left hand on hip / swinging
        p.r("armL", sw * 26 * 1 + br * 2, 0, -24 + w * 14);
        p.r("foreL", -28 - w * 20, 0, 52 - w * 40);
        p.r("handL", 0, 0, -20);
        // legs: idle has a cocked knee, walk is a hunched stalking stride
        p.r("legR", -sw * 34 - 2 * (1 - w), 0, 4 * (1 - w));
        p.r("shinR", Math.max(0, sw) * 44 + 4 * w, 0, 0);
        p.r("legL", sw * 34 - 10 * (1 - w), 0, -5 * (1 - w));
        p.r("shinL", Math.max(0, -sw) * 44 + 4 * w + 14 * (1 - w), 0, 0);
        p.r("bootL", -6 * (1 - w), 0, 0);
        // secondary: hair, antenna, skirt
        p.r("hairBack", 6 + br * 2 + Math.abs(cw) * 10, 0, Anim.sin(age * 3) * 3);
        p.r("spiral", 0, 0, Anim.sin(age * 8) * 8 - sw * 12);
        p.r("antenna", 0, 0, Anim.sin(age * 8 - 40) * 4);
        p.r("skirtHem", Anim.sin(age * 5) * 2 - sw * 4, 0, cw * 4);
        p.r("skirtMid", w * 4, 0, 0);
        p.r("crown", 0, 0, 0);
    }

    static float cv(float t, float... tv) { return Anim.curve(t, tv); }

    /** finger spread (+ = open wide) and curl (+ = clench) */
    static void claw(BloomiePose p, float spread, float curl) {
        for (int i = 0; i < 4; i++) {
            float side = (i - 1.5f) / 1.5f;
            p.ar(FINGERS[i], -curl * 0.6f, 0, side * spread);
            p.ar(FINGERS[i] + "t", -curl, 0, 0);
        }
        p.ar("cRT", -curl * 0.5f, 0, -spread * 0.6f);
        p.ar("cRTt", -curl * 0.7f, 0, 0);
    }

    static void ability(BloomiePose p, AnimCtx c, float t) {
        switch (c.ability) {
            case "abc_throw" -> {
                // 0-6 reach up to the crown and pluck a block, 6-11 wind back, 12 throw (3 blocks), 16-21 claw cocks, 22 claw hurl
                float pluck = cv(t, 0, 0, 5, 1, 8, 0.6f, 11, 0);
                p.r("armL", cv(t, 0, 0, 5, -165, 8, -120, 11, 40, 13, -110, 17, -70, 26, 0), 0, cv(t, 0, -20, 5, -30, 11, -25, 13, 10, 20, -20));
                p.r("foreL", cv(t, 0, -20, 5, -70, 11, -40, 13, 0, 20, -20), 0, 0);
                p.r("head", -6 - pluck * 22 + cv(t, 11, 0, 13, 10, 20, 0), cv(t, 8, 0, 11, -20, 13, 15, 20, 0), 9 + pluck * 10);
                p.r("chest", 6 + cv(t, 8, -4, 11, -12, 13, 18, 18, 8, 22, 22, 26, 6), cv(t, 0, 0, 8, -10, 11, -32, 13, 30, 17, 40, 22, -35, 28, 0), 0);
                p.r("hips", 0, cv(t, 8, 0, 11, -12, 13, 12, 17, 10, 22, -14, 28, 0), 0);
                p.r("legL", cv(t, 9, -10, 12, -38, 22, -10), 0, 0);
                p.r("shinL", cv(t, 9, 14, 12, 30, 22, 12), 0, 0);
                p.r("legR", cv(t, 17, 0, 22, -30, 28, 0), 0, 0);
                p.r("shinR", cv(t, 17, 0, 22, 25, 28, 4), 0, 0);
                p.mv("root", 0, cv(t, 10, 0, 13, 1.2f, 18, 0, 22, 1.4f, 28, 0), cv(t, 11, 0, 13, -1, 22, -2, 30, 0));
                p.r("armR", cv(t, 0, -22, 12, -10, 18, 30, 20, 35, 22, -125, 25, -95, 32, -22), cv(t, 18, 10, 22, -10), cv(t, 12, 24, 18, 60, 22, 10, 30, 24));
                p.r("foreR", cv(t, 14, -48, 19, -90, 22, -5, 28, -48), 0, -6);
                claw(p, cv(t, 18, 0, 21, -8, 22, 30, 26, 10, 30, 0), cv(t, 18, 0, 21, 50, 22, -15, 28, 0));
            }
            case "letter_rain" -> {
                // 0-14 claw rises to the sky while she cackles, 20 yanks down, 22-44 conducts each drop, 44 final point
                float rise = cv(t, 0, 0, 14, 1, 20, 1.08f, 22, 0);
                float beat = t >= 22 && t < 44 ? Anim.sin((t - 22) / 3f * 360f) : 0;
                p.r("armR", cv(t, 0, -22, 14, -175, 19, -185, 22, -70, 24, -120, 44, -120, 47, -95, 56, -22) + beat * 22, 0, cv(t, 0, 24, 14, 12, 22, 20, 44, 18, 56, 24));
                p.r("foreR", cv(t, 0, -48, 14, -5, 22, -30, 44, -20, 48, -5, 56, -48), 0, 0);
                claw(p, cv(t, 0, 0, 12, 35, 19, 40, 21, -10, 44, 10, 46, 20, 56, 0), cv(t, 12, 0, 19, -10, 21, 60, 24, 10, 44, 20, 47, -10, 56, 0) + beat * 20);
                p.r("armL", cv(t, 0, 0, 14, -100, 22, -150, 44, -140, 56, 0) - beat * 22, 0, cv(t, 0, -24, 14, -70, 44, -50, 56, -24));
                p.r("foreL", cv(t, 0, -28, 14, -20, 56, -28), 0, cv(t, 0, 52, 14, 0, 56, 52));
                p.r("chest", 6 + cv(t, 0, 0, 14, -22, 20, -26, 22, 14, 44, 6, 47, 18, 56, 0) - beat * 4, 0, beat * 4);
                p.r("head", cv(t, 0, -6, 14, -35, 20, -38, 22, -5, 56, -6) + beat * 6, c.headYaw * 0.5f, 9 + Anim.sin(t * 40) * 6 * rise);
                p.mv("jaw", 0, rise * 1.4f + Math.abs(beat) * 0.8f, 0);
                p.mv("root", 0, -rise * 1.3f + cv(t, 20, 0, 22, 1.5f, 26, 0.5f), 0);
                p.r("legR", 0, 0, cv(t, 0, 4, 22, 10, 56, 4));
                p.r("legL", -6, 0, cv(t, 0, -5, 22, -10, 56, -5));
                p.r("shinL", cv(t, 0, 14, 14, 0, 22, 14), 0, 0);
            }
            case "rake" -> {
                // forehand rake (hit 9), backhand (hit 18), overhead rake (hit 30)
                p.r("armR", cv(t, 0, -22, 6, -20, 9, -85, 11, -80, 15, -75, 18, -70, 20, -80, 25, -185, 27, -190, 30, -35, 33, -25, 40, -22),
                        cv(t, 0, 10, 6, 40, 9, -40, 12, -60, 15, -70, 18, 50, 21, 55, 25, 10, 40, 10),
                        cv(t, 0, 24, 6, 80, 9, 20, 15, -20, 18, 50, 21, 60, 25, 20, 30, 10, 40, 24));
                p.r("foreR", cv(t, 0, -48, 6, -60, 9, -5, 15, -55, 18, -5, 25, -30, 28, -40, 30, 0, 36, -10, 40, -48), 0, 0);
                claw(p, cv(t, 5, 0, 8, 35, 10, 15, 16, 35, 19, 15, 27, 40, 31, 25, 40, 0), cv(t, 5, 0, 8, -20, 10, 35, 16, -20, 19, 40, 27, -25, 31, 50, 38, 0));
                p.r("chest", 6 + cv(t, 0, 0, 6, 8, 9, 14, 18, 14, 25, -18, 28, -22, 30, 32, 34, 34, 40, 0),
                        cv(t, 0, 0, 6, 38, 9, -42, 11, -50, 15, -48, 18, 42, 21, 50, 25, 5, 40, 0), cv(t, 0, 0, 6, 8, 9, -6, 18, 6, 25, 0));
                p.r("hips", 0, cv(t, 0, 0, 6, 14, 9, -14, 15, -16, 18, 16, 25, 0), 0);
                p.r("head", cv(t, 0, -6, 25, -16, 30, -30, 40, -6), cv(t, 0, 0, 6, -25, 9, 30, 15, 35, 18, -30, 25, 0), 9);
                p.r("armL", cv(t, 0, 0, 6, -40, 9, 30, 15, 20, 18, -50, 25, -30, 30, 40, 40, 0), 0, cv(t, 0, -24, 6, -55, 18, -60, 30, -45, 40, -24));
                p.r("legR", cv(t, 5, -2, 9, -26, 13, -10, 16, -4, 18, 15, 22, 0, 27, -10, 30, -40, 40, -2), 0, 4);
                p.r("shinR", cv(t, 5, 0, 9, 30, 13, 10, 27, 10, 30, 45, 40, 0), 0, 0);
                p.r("legL", cv(t, 5, -10, 9, 16, 16, -30, 18, -36, 25, -5, 30, 28, 40, -10), 0, -5);
                p.r("shinL", cv(t, 5, 14, 9, 10, 16, 30, 18, 35, 25, 10, 30, 14, 40, 14), 0, 0);
                p.mv("root", 0, cv(t, 5, 0, 9, 1, 13, 0.3f, 18, 1, 22, 0, 26, -0.6f, 30, 2.2f, 36, 2, 40, 0), cv(t, 25, 0, 30, -2, 40, 0));
            }
            case "claw_smash" -> {
                // rear up 0-16, trembling hold 16-20, SLAM 22, stuck 22-34, wrench free 34-44
                float tremble = t > 14 && t < 21 ? Anim.sin(t * 120) * 3 : 0;
                float stuck = t > 23 && t < 34 ? Anim.sin(t * 70) * 3 : 0;
                p.r("armR", cv(t, 0, -22, 14, -195, 20, -200, 22, -45, 24, -38, 34, -40, 39, -70, 44, -22) + tremble, cv(t, 0, 10, 14, 0, 22, 0, 44, 10), cv(t, 0, 24, 14, 15, 22, 5, 34, 5, 44, 24) + stuck);
                p.r("foreR", cv(t, 0, -48, 14, -40, 20, -60, 22, 0, 34, 0, 40, -30, 44, -48), 0, 0);
                p.r("clawR", cv(t, 0, -18, 20, -30, 22, 10, 34, 10, 44, -18), 0, 0);
                claw(p, cv(t, 0, 0, 14, 40, 22, 30, 34, 30, 40, 0), cv(t, 0, 0, 14, -25, 20, -30, 22, 20, 34, 25, 38, -10, 44, 0));
                p.r("chest", cv(t, 0, 6, 14, -26, 20, -30, 22, 48, 25, 50, 34, 44, 40, 20, 44, 6), cv(t, 0, 0, 14, 22, 22, -8, 44, 0), stuck * 0.5f);
                p.r("hips", cv(t, 0, 0, 14, -6, 22, 14, 34, 14, 44, 0), 0, 0);
                p.r("head", cv(t, 0, -6, 14, -30, 20, -28, 22, -45, 34, -40, 44, -6), cv(t, 0, 0, 14, -15, 22, 0), 9);
                p.mv("jaw", 0, cv(t, 0, 0, 12, 1.6f, 20, 1.6f, 22, 0.5f, 34, 0.5f, 40, 0), 0);
                p.r("armL", cv(t, 0, 0, 14, -60, 20, -70, 22, 40, 34, 30, 44, 0), 0, cv(t, 0, -24, 14, -80, 22, -40, 44, -24));
                p.r("foreL", cv(t, 0, -28, 14, -10, 44, -28), 0, cv(t, 0, 52, 14, 10, 34, 10, 44, 52));
                p.mv("root", 0, cv(t, 0, 0, 14, -1.8f, 20, -2, 22, 3.6f, 26, 3.2f, 34, 3.2f, 42, 0), cv(t, 20, 0, 22, -1.5f, 40, -1.5f, 44, 0));
                p.r("legR", cv(t, 0, -2, 14, 5, 22, -55, 34, -55, 44, -2), 0, cv(t, 14, 4, 22, 14, 40, 4));
                p.r("shinR", cv(t, 0, 0, 22, 75, 34, 75, 44, 0), 0, 0);
                p.r("legL", cv(t, 0, -10, 14, 10, 22, 18, 34, 18, 44, -10), 0, cv(t, 14, -5, 22, -14, 40, -5));
                p.r("shinL", cv(t, 0, 14, 14, 0, 22, 40, 34, 40, 44, 14), 0, 0);
                p.r("crown", cv(t, 20, 0, 22, 18, 26, -8, 30, 0), 0, 0);
            }
            case "scratch_lunge" -> {
                // coil 0-9, launch 10, claw rips upward 13-15, skid 16-30
                p.r("chest", cv(t, 0, 6, 9, 38, 11, 62, 14, 40, 18, 30, 30, 6), cv(t, 0, 0, 9, 25, 14, -30, 22, 0), 0);
                p.r("head", cv(t, 0, -6, 9, -45, 12, -60, 15, -30, 30, -6), cv(t, 0, 0, 9, -20, 14, 10, 22, 0), 9);
                p.mv("jaw", 0, cv(t, 6, 0, 10, 1.4f, 16, 1.2f, 22, 0), 0);
                p.mv("root", 0, cv(t, 0, 0, 9, 4, 11, 1.5f, 14, 1, 18, 2.5f, 30, 0), cv(t, 9, 0, 12, -3, 16, -2, 30, 0));
                p.r("armR", cv(t, 0, -22, 9, 55, 11, 40, 13, -100, 15, -150, 18, -140, 30, -22), cv(t, 9, 30, 14, -20, 30, 10), cv(t, 0, 24, 9, 40, 14, 10, 30, 24));
                p.r("foreR", cv(t, 0, -48, 9, -20, 13, -40, 15, 0, 22, -10, 30, -48), 0, 0);
                claw(p, cv(t, 0, 0, 9, 20, 12, 40, 15, 20, 30, 0), cv(t, 0, 0, 9, 30, 12, -20, 15, 50, 22, 10, 30, 0));
                p.r("armL", cv(t, 0, 0, 9, 50, 11, 70, 14, 30, 30, 0), 0, cv(t, 0, -24, 9, -50, 14, -60, 30, -24));
                p.r("legR", cv(t, 0, -2, 9, -70, 11, 30, 14, 40, 18, -20, 30, -2), 0, 4);
                p.r("shinR", cv(t, 0, 0, 9, 100, 11, 10, 14, 20, 18, 60, 30, 0), 0, 0);
                p.r("legL", cv(t, 0, -10, 9, -40, 11, -70, 14, -50, 18, -45, 30, -10), 0, -5);
                p.r("shinL", cv(t, 0, 14, 9, 110, 11, 60, 14, 40, 18, 70, 30, 14), 0, 0);
                p.r("hairBack", cv(t, 9, 6, 12, 45, 18, 30, 30, 6), 0, 0);
            }
            case "shard_throw" -> {
                // claw drawn across to the left hip 0-12 (fingers coiled), flung out at 14, shards fly; pose held, recover
                p.r("armR", cv(t, 0, -22, 10, -35, 12, -30, 14, -85, 18, -90, 34, -22), cv(t, 0, 10, 10, 30, 14, -30, 34, 10), cv(t, 0, 24, 10, -55, 12, -62, 14, 70, 18, 75, 34, 24));
                p.r("foreR", cv(t, 0, -48, 10, -70, 13, -40, 14, 0, 24, -10, 34, -48), 0, 0);
                p.r("clawR", cv(t, 0, -18, 12, 20, 14, -40, 20, -30, 34, -18), 0, 0);
                claw(p, cv(t, 0, 0, 12, -10, 14, 45, 22, 40, 34, 0), cv(t, 0, 0, 12, 70, 13.5f, 70, 14.5f, -25, 22, -20, 34, 0));
                p.r("chest", 6 + cv(t, 0, 0, 12, 12, 14, -6, 34, 0), cv(t, 0, 0, 12, -45, 14, 38, 18, 42, 34, 0), cv(t, 12, 0, 14, 8, 34, 0));
                p.r("hips", 0, cv(t, 0, 0, 12, -15, 14, 15, 34, 0), 0);
                p.r("head", cv(t, 0, -6, 12, 4, 14, -12, 34, -6), cv(t, 0, 0, 12, 35, 14, -12, 34, 0), cv(t, 0, 9, 12, 20, 16, -4, 34, 9));
                p.r("armL", cv(t, 0, 0, 12, 20, 14, -20, 34, 0), 0, cv(t, 0, -24, 12, -40, 14, -15, 34, -24));
                p.r("legR", cv(t, 10, -2, 14, 22, 34, -2), 0, cv(t, 10, 4, 14, 12, 34, 4));
                p.r("legL", cv(t, 10, -10, 14, -28, 34, -10), 0, -5);
                p.r("shinL", cv(t, 10, 14, 14, 26, 34, 14), 0, 0);
                p.mv("root", 0, cv(t, 8, 0, 12, 1.2f, 14, 0.4f, 34, 0), 0);
            }
            case "spelling_test" -> {
                // 0-8 teacher finger raised, 8-30 writes letters in the air with the claw, 30-38 points, 38 snap -> bursts, laughs
                float write = t > 8 && t < 30 ? 1 : 0;
                float wx = write * Anim.sin(t * 52) * 18, wz = write * Anim.sin(t * 31 + 40) * 16;
                p.r("armL", cv(t, 0, 0, 6, -150, 30, -150, 36, -40, 44, 0), 0, cv(t, 0, -24, 6, -10, 30, -12, 44, -24));
                p.r("foreL", cv(t, 0, -28, 6, -30, 30, -30, 44, -28), 0, cv(t, 0, 52, 6, 0, 30, 0, 44, 52));
                p.r("fL1", cv(t, 0, 0, 6, 40, 30, 40, 36, 0), 0, 0);
                p.r("armR", cv(t, 0, -22, 8, -80, 30, -85, 34, -95, 38, -100, 41, -60, 50, -22) + wx, cv(t, 8, 10, 30, -10, 50, 10), cv(t, 0, 24, 8, 10, 30, 10, 50, 24) + wz);
                p.r("foreR", cv(t, 0, -48, 8, -30, 30, -30, 34, 0, 38, 0, 41, -30, 50, -48), 0, 0);
                p.r("clawR", -18, 0, 0);
                // index (cR2) extended, others curled; at 38 snap shut
                for (int i = 0; i < 4; i++) {
                    float curl = i == 2 ? cv(t, 36, 0, 38, 70, 42, 0) : cv(t, 0, 0, 6, 60, 36, 60, 38, 80, 44, 0);
                    p.ar(FINGERS[i], -curl * 0.6f, 0, 0);
                    p.ar(FINGERS[i] + "t", -curl, 0, 0);
                }
                p.r("chest", 6 + cv(t, 0, 0, 8, 4, 30, 6, 34, 12, 38, 14, 40, -10, 50, 0) + (t > 38 ? Anim.sin(t * 90) * 4 * (1 - c.seg(38, 50)) : 0), cv(t, 0, 0, 8, -6, 30, 0, 34, 15, 50, 0) + wz * 0.3f, wz * 0.2f);
                p.r("head", cv(t, 0, -6, 8, -10, 30, -8, 38, -4, 40, -25, 50, -6) + wx * 0.2f, c.headYaw * 0.4f + wz * 0.6f, 9 + cv(t, 0, 0, 6, 12, 30, 8, 38, 0, 40, -10, 50, 0));
                p.mv("jaw", 0, cv(t, 38, 0, 40, 1.6f, 47, 1.6f, 50, 0) * (t > 40 ? 0.6f + 0.4f * Anim.sin(t * 110) : 1), 0);
                p.r("legL", cv(t, 0, -10, 8, -14, 34, -26, 40, -10), 0, -5);
            }
            case "grab_rip" -> {
                // reach 0-9, snap shut 10, lift & squeeze 10-34 (pulses 16/22/28), rip down & fling 36, recover
                float sq = t > 12 && t < 34 ? Math.max(0, Anim.sin((t - 13) / 6f * 360f)) : 0;
                p.r("armR", cv(t, 0, -22, 5, 20, 9, -90, 11, -85, 16, -125, 33, -135, 36, -30, 40, -20, 52, -22) + sq * 4, cv(t, 0, 10, 9, -5, 33, 0, 36, -40, 52, 10), cv(t, 0, 24, 5, 40, 9, 8, 33, 12, 36, -45, 42, -30, 52, 24));
                p.r("foreR", cv(t, 0, -48, 5, -70, 9, -5, 12, -15, 33, -30, 36, 0, 52, -48), 0, 0);
                p.r("clawR", cv(t, 0, -18, 9, -40, 12, -25, 33, -30, 36, 20, 52, -18), 0, 0);
                claw(p, cv(t, 0, 0, 7, 45, 9.5f, 50, 10.5f, -5, 34, -5, 37, 50, 44, 20, 52, 0), cv(t, 0, 0, 7, -30, 9.5f, -35, 11, 75, 34, 75, 36.5f, -30, 44, -10, 52, 0) + sq * 25);
                p.r("chest", 6 + cv(t, 0, 0, 5, -6, 9, 30, 12, 20, 33, -12, 36, 34, 40, 30, 52, 0), cv(t, 0, 0, 5, 25, 9, -10, 33, 10, 36, -40, 42, -30, 52, 0), sq * 3);
                p.r("hips", 0, cv(t, 0, 0, 5, 10, 9, -8, 33, 5, 36, -15, 52, 0), 0);
                p.r("head", cv(t, 0, -6, 9, -20, 16, -30, 33, -35, 36, 10, 52, -6), cv(t, 0, 0, 9, 10, 33, 18, 36, -20, 52, 0), cv(t, 0, 9, 16, 28, 33, 30, 36, 0, 52, 9) + sq * 6);
                p.mv("jaw", 0, cv(t, 10, 0, 14, 1.4f, 33, 1.4f, 36, 1.8f, 44, 0) * (t > 14 && t < 33 ? 0.5f + 0.5f * Anim.sin(t * 100) : 1), 0);
                p.r("armL", cv(t, 0, 0, 9, 30, 16, -120, 33, -150, 36, -40, 40, 10, 52, 0), 0, cv(t, 0, -24, 16, -30, 33, -40, 36, 20, 42, 0, 52, -24));
                p.r("foreL", cv(t, 0, -28, 16, -60, 33, -70, 36, 0, 52, -28), 0, cv(t, 0, 52, 16, 0, 44, 0, 52, 52));
                p.r("legR", cv(t, 0, -2, 6, 0, 9, -35, 16, -12, 33, -8, 36, -30, 52, -2), 0, 4);
                p.r("shinR", cv(t, 0, 0, 9, 35, 16, 10, 36, 30, 52, 0), 0, 0);
                p.r("legL", cv(t, 0, -10, 9, 20, 16, 12, 36, 25, 52, -10), 0, -5);
                p.mv("root", 0, cv(t, 0, 0, 9, 1.5f, 16, -0.5f, 33, -0.8f, 36, 2, 44, 1, 52, 0), cv(t, 0, 0, 9, -1.5f, 33, -0.5f, 52, 0));
            }
            case "screech" -> {
                // inhale 0-10 (arch back, arms open), SCREECH 12-28 (shaking, jaw wide, arms flung back), recover
                float sc = c.seg(11, 13) * (1 - c.seg(27, 31));
                float shake = sc * Anim.sin(t * 150);
                p.r("chest", 6 + cv(t, 0, 0, 10, -28, 12, 34, 28, 30, 34, 0) + shake * 2, shake * 3, 0);
                p.r("neck", cv(t, 0, -4, 10, -10, 12, 12, 28, 12, 34, -4), 0, 0);
                p.r("head", cv(t, 0, -6, 10, -42, 12, 12, 28, 10, 34, -6) + shake * 4, c.headYaw * 0.3f + shake * 4, cv(t, 0, 9, 10, 0, 28, 0, 36, 9));
                p.mv("jaw", 0, cv(t, 0, 0, 10, 0.8f, 12, 3.2f, 28, 3.2f, 33, 0), cv(t, 10, 0, 12, -0.5f, 28, -0.5f, 33, 0));
                p.r("jaw", cv(t, 10, 0, 12, 25, 28, 25, 33, 0), 0, 0);
                p.r("armR", cv(t, 0, -22, 10, -60, 12, 45, 28, 50, 36, -22), cv(t, 0, 10, 10, 30, 12, -20, 28, -20, 36, 10), cv(t, 0, 24, 10, 70, 12, 55, 28, 55, 36, 24));
                p.r("foreR", cv(t, 0, -48, 10, -30, 12, -5, 28, -5, 36, -48), 0, 0);
                claw(p, cv(t, 0, 0, 10, 40, 28, 45, 36, 0) + shake * 8, cv(t, 0, 0, 10, -20, 12, -40, 28, -40, 36, 0));
                p.r("armL", cv(t, 0, 0, 10, -60, 12, 45, 28, 50, 36, 0), cv(t, 10, -30, 12, 20, 36, 0), cv(t, 0, -24, 10, -70, 12, -55, 28, -55, 36, -24));
                p.r("foreL", cv(t, 0, -28, 10, -20, 12, -5, 28, -5, 36, -28), 0, cv(t, 0, 52, 10, 0, 34, 0, 36, 52));
                p.mv("root", shake * 0.4f, cv(t, 0, 0, 10, -0.8f, 12, 1.4f, 28, 1.4f, 36, 0), 0);
                p.r("legR", cv(t, 0, -2, 12, -18, 28, -18, 36, -2), 0, cv(t, 0, 4, 12, 12, 28, 12, 36, 4));
                p.r("legL", cv(t, 0, -10, 12, 20, 28, 20, 36, -10), 0, cv(t, 0, -5, 12, -12, 28, -12, 36, -5));
                p.r("shinL", cv(t, 0, 14, 12, 0, 36, 14), 0, 0);
                p.r("hairBack", 6 + sc * 55 + shake * 6, 0, shake * 8);
                p.r("skirtHem", sc * 14, 0, shake * 4);
                p.r("spiral", 0, 0, sc * -40 + shake * 15);
            }
            case "alphabet_barrage" -> {
                // 0-14 crouch then rear up cackling, 16-66 alternating rapid throws (left on 4k, claw on 4k+2), 66-80 finale + slump
                float on = c.seg(14, 16) * (1 - c.seg(66, 70));
                float ph = (t - 16) / 4f * 360f;                  // one left + one claw throw per 4 ticks
                float l = on * Anim.sin(ph + 90), r = on * Anim.sin(ph + 270);
                float rear = cv(t, 0, 0, 5, -0.6f, 14, 1, 16, 0.4f, 66, 0.4f, 72, 1, 80, 0);
                p.r("chest", 6 + cv(t, 0, 0, 5, 24, 14, -24, 16, 12, 66, 12, 72, -20, 80, 0) + Math.abs(l - r) * 4, on * l * 26, 0);
                p.r("hips", 0, on * l * 10, 0);
                p.r("head", cv(t, 0, -6, 5, 10, 14, -40, 16, -8, 66, -8, 72, -45, 80, -6), c.headYaw * 0.4f - on * l * 16, 9 + on * Anim.sin(t * 50) * 6);
                p.mv("jaw", 0, Math.max(0, rear) * 1.8f + on * 1.0f, 0);
                p.r("armL", cv(t, 0, 0, 5, 30, 14, -140, 16, -60, 66, -60, 72, -160, 80, 0) + l * 55, 0, cv(t, 0, -24, 14, -70, 16, -15, 66, -15, 72, -60, 80, -24));
                p.r("foreL", cv(t, 0, -28, 14, -10, 16, -30, 66, -30, 80, -28) - Math.max(0, l) * 40, 0, cv(t, 0, 52, 14, 0, 72, 0, 80, 52));
                p.r("armR", cv(t, 0, -22, 5, 30, 14, -150, 16, -70, 66, -70, 72, -170, 80, -22) + r * 55, 0, cv(t, 0, 24, 14, 70, 16, 18, 66, 18, 72, 60, 80, 24));
                p.r("foreR", cv(t, 0, -48, 14, -10, 16, -30, 66, -30, 80, -48) - Math.max(0, r) * 40, 0, 0);
                claw(p, cv(t, 0, 0, 14, 45, 66, 25, 72, 50, 80, 0) + r * 15, -r * 35);
                p.mv("root", 0, cv(t, 0, 0, 5, 3, 14, -1.6f, 16, 1, 66, 1, 72, -1.2f, 80, 0), 0);
                p.r("legR", cv(t, 0, -2, 5, -40, 14, 0, 16, -14, 66, -14, 80, -2), 0, cv(t, 0, 4, 16, 14, 66, 14, 80, 4));
                p.r("shinR", cv(t, 0, 0, 5, 60, 14, 0, 16, 25, 66, 25, 80, 0), 0, 0);
                p.r("legL", cv(t, 0, -10, 5, -40, 14, 0, 16, 10, 66, 10, 80, -10), 0, cv(t, 0, -5, 16, -14, 66, -14, 80, -5));
                p.r("shinL", cv(t, 0, 14, 5, 60, 14, 0, 16, 18, 66, 18, 80, 14), 0, 0);
                p.mv("crown", 0, -on * (1.2f + Anim.sin(t * 60) * 0.6f) - Math.max(0, rear) * 1.5f, 0);
                p.r("crown", 0, on * Anim.sin(t * 30) * 12, 0);
                p.r("hairBack", 6 + on * 20 + Math.abs(l) * 10, 0, l * 10);
            }
            default -> {}
        }
    }

    static void death(BloomiePose p, AnimCtx c) {
        float d = c.death;
        float recoil = Anim.curve(d, 0, 0, 0.15f, 1, 0.35f, 0.4f);
        float kneel = Anim.smooth((d - 0.2f) / 0.3f);
        float fall = Anim.easeIn(Anim.clamp((d - 0.45f) / 0.35f, 0, 1));
        float twitch = d > 0.82f ? Anim.sin(d * 3000) * (1 - d) * 40 : 0;
        p.ar("chest", -28 * recoil + 20 * kneel, 0, 6 * recoil);
        p.ar("head", -30 * recoil + 25 * kneel + 15 * fall, 0, 20 * kneel);
        p.am("jaw", 0, 1.8f * recoil + 1.4f * kneel, 0);
        p.ar("armR", -50 * recoil + 40 * kneel - 140 * fall, 0, 10 * kneel - 20 * fall);
        p.ar("foreR", 30 * fall, 0, 0);
        claw(p, 30 * recoil - 20 * fall, -40 * recoil + 50 * kneel - 30 * fall + twitch);
        p.ar("armL", 30 * kneel - 130 * fall, 0, 20 * kneel);
        float bend = kneel * (1 - 0.85f * fall);
        p.ar("legR", -75 * bend, 0, 0);
        p.ar("shinR", 95 * bend + 10 * fall, 0, 0);
        p.ar("legL", -60 * bend, 0, 0);
        p.ar("shinL", 80 * bend + 25 * fall, 0, 0);
        p.am("root", 0, 5.5f * bend - 2.2f * fall, -1.5f * bend);
        p.ar("root", 86 * fall, 0, 0);
        p.ar("spiral", 0, 0, 55 * kneel + twitch);
        p.ar("hairBack", -30 * fall, 0, 0);
        p.ar("crown", 0, 0, 25 * fall);
    }
}
