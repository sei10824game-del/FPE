package com.fpe.client.spec;

import com.fpe.client.model.Anim;
import com.fpe.client.model.AnimCtx;
import com.fpe.client.model.ModelParts;
import com.fpe.client.model.ModelSpec;
import com.fpe.client.model.ModelSpec.Face;
import com.fpe.client.model.ModelSpec.Pattern;

/**
 * Fen: lanky predator girl. Long orange mane covering the eyes, ahoge, shark grin, black tee, rolled denim shorts,
 * bandaged legs, extra-long arms ending in black spiky claws, floating white diamond sparkles, curved dark-red blade
 * (only drawn for blade attacks) and her little black cat with glowing orange ring eyes.
 */
public final class FenSpec {
    private FenSpec() {}

    static final int SKIN = 0xF2D0B4, SKIN_D = 0xD9B096, SHIRT = 0x1E1E27, SHIRT_D = 0x2B2B36, DENIM = 0x4C74AE, DENIM_L = 0x86A9D6,
            BAND = 0xEDE6D8, CLAW = 0x111116, HAIR = 0xF59A2E, HAIR_M = 0xE8801F, HAIR_D = 0xCF6516, BLADE = 0x6A0D1C, BLADE_E = 0xC0283E,
            CAT = 0x18181F, EYE = 0xFF8A1E;

    public static final ModelSpec SPEC = com.fpe.client.model.BbModel.load("fen", 0.9f);
    static final ModelSpec PROC = build();

    private static ModelSpec build() {
        ModelSpec m = new ModelSpec("fen");
        m.group("root", null, 0, 24, 0);
        m.group("body", "root", 0, 12, 0);
        m.part("pelvis", "body", 0, 12, 0, -3.2f, -1, -1.9f, 6.4f, 3, 3.8f, DENIM).grain(0.1f)
                .decor(Face.FRONT, 0, 0, 7, 1, 0x34557F).decor(Face.FRONT, 3, 1, 1, 2, 0x34557F).decor(Face.BACK, 0, 0, 7, 1, 0x34557F);
        for (int s = -1; s <= 1; s += 2) {
            String S = s < 0 ? "R" : "L";
            float x = 1.7f * s;
            m.part("leg" + S, "body", x, 13, 0, -1.6f, 0, -1.7f, 3.2f, 4.2f, 3.4f, DENIM).grain(0.12f)
                    .decor(Face.FRONT, 1, 1, 1, 2, 0x3A5F92).decor(Face.LEFT, 1, 0, 1, 3, 0x3A5F92);
            m.part("cuff" + S, "leg" + S, x, 13, 0, -1.8f, 3.3f, -1.9f, 3.6f, 1.3f, 3.8f, DENIM_L).decor(Face.FRONT, 0, 0, 4, 1, 0xA9C4E6);
            m.part("shin" + S, "leg" + S, x, 17.4f, 0, -0.9f, 0, -0.9f, 1.8f, 4.3f, 1.8f, SKIN).pattern(Pattern.STRIPE_H, BAND, 1)
                    .decor(Face.FRONT, 0, 1, 1, 1, 0xB4505A).decor(Face.FRONT, 1, 3, 1, 1, 0xB4505A);
            m.part("foot" + S, "shin" + S, x, 21.6f, 0, -0.9f, 0, -2.1f, 1.8f, 2.4f, 2.7f, SKIN)
                    .decor(Face.FRONT, 0, 1, 2, 2, 0x26262C).decor(Face.TOP, 0, 0, 2, 1, BAND).decor(Face.RIGHT, 0, 0, 3, 1, BAND).decor(Face.LEFT, 0, 0, 3, 1, BAND);
        }
        // ---- torso
        m.group("chest", "body", 0, 12, 0);
        m.part("torso", "chest", 0, 12, 0, -3, -7.6f, -1.8f, 6, 7.6f, 3.6f, SHIRT).pattern(Pattern.GRADIENT_V, SHIRT_D, 1).grain(0.08f)
                .decor(Face.FRONT, 0, 7, 6, 1, 0x34343F).decor(Face.FRONT, 2, 0, 2, 1, SKIN_D).decor(Face.BACK, 0, 7, 6, 1, 0x34343F)
                .decor(Face.FRONT, 1, 3, 1, 1, 0x5A1018).decor(Face.FRONT, 4, 5, 1, 1, 0x5A1018);
        // ---- head
        m.group("head", "chest", 0, 4.5f, 0);
        m.part("skull", "head", 0, 4.5f, 0, -4, -8, -3.5f, 8, 8, 7, SKIN).grain(0.04f)
                // shark grin
                .decor(Face.FRONT, 0, 4, 8, 1, 0x1A0D10).decor(Face.FRONT, 1, 5, 6, 1, 0xFFFFFF)
                .decor(Face.FRONT, 0, 5, 1, 1, 0x1A0D10).decor(Face.FRONT, 7, 5, 1, 1, 0x1A0D10)
                .decor(Face.FRONT, 1, 6, 6, 1, 0xFFFFFF).decor(Face.FRONT, 2, 5, 1, 1, 0xD8D8D8).decor(Face.FRONT, 5, 5, 1, 1, 0xD8D8D8)
                .decor(Face.FRONT, 1, 6, 1, 1, 0x1A0D10).decor(Face.FRONT, 3, 6, 2, 1, 0xB02840).decor(Face.FRONT, 6, 6, 1, 1, 0x1A0D10)
                .decor(Face.FRONT, 2, 7, 4, 1, 0x1A0D10)
                // the one visible eye (behind the fringe gap)
                .decor(Face.FRONT, 5, 2, 2, 2, 0x111111).decorGlow(Face.FRONT, 6, 2, 1, 1, 0xFFE8C0)
                .decor(Face.FRONT, 0, 3, 1, 1, 0xE9A0A0);
        m.part("tongue", "head", 0, 2.4f, -3.7f, -0.7f, 0, -0.6f, 1.4f, 5, 0.7f, 0xC8304C).decor(Face.FRONT, 0, 4, 2, 1, 0x8A1A2C);
        m.part("hairTop", "head", 0, 4.5f, 0, -4.6f, -8.8f, -4.1f, 9.2f, 3.2f, 8.8f, HAIR).grain(0.1f)
                .decor(Face.TOP, 3, 2, 1, 5, HAIR_M).decor(Face.TOP, 6, 1, 1, 6, HAIR_M);
        m.part("fringeA", "head", -2.4f, -3.3f, -3.9f, -1.9f, 0, -0.7f, 3.8f, 5.6f, 1.3f, HAIR).rot(-4, 0, 7)
                .decor(Face.FRONT, 1, 0, 1, 4, HAIR_M).decor(Face.FRONT, 0, 3, 1, 2, HAIR_D);
        m.part("fringeB", "head", 0.6f, -3.3f, -4.0f, -1.6f, 0, -0.7f, 3.2f, 4.6f, 1.3f, HAIR_M).rot(-6, 0, -5)
                .decor(Face.FRONT, 1, 1, 1, 3, HAIR);
        m.part("fringeC", "head", 3.2f, -3.3f, -3.9f, -1.1f, 0, -0.7f, 2.2f, 2.6f, 1.3f, HAIR).rot(-4, 0, -14);
        m.part("hspkR", "head", -3.5f, -3.6f, 0, -1, -1, -2, 2, 2, 4.5f, HAIR).rot(0, 0, 35);
        m.part("hspkL", "head", 3.5f, -3.6f, 0, -1, -1, -2, 2, 2, 4.5f, HAIR).rot(0, 0, -35);
        m.part("hspkB", "head", 0, -3.8f, 3.4f, -2.5f, -1, -1, 5, 2, 3, HAIR).rot(30, 0, 0);
        m.part("sideR", "head", -4.3f, -3.4f, -0.8f, -1.1f, 0, -3.2f, 2.2f, 10f, 6.2f, HAIR_M).rot(0, 0, 9)
                .pattern(Pattern.GRADIENT_V, HAIR_D, 1).decor(Face.RIGHT, 2, 2, 1, 6, HAIR);
        m.part("sideL", "head", 4.3f, -3.4f, -0.8f, -1.1f, 0, -3.2f, 2.2f, 10f, 6.2f, HAIR_M).rot(0, 0, -9)
                .pattern(Pattern.GRADIENT_V, HAIR_D, 1).decor(Face.LEFT, 2, 2, 1, 6, HAIR);
        m.part("ahoge1", "head", 0.4f, -6.0f, -0.8f, -0.45f, -3.2f, -0.45f, 0.9f, 3.2f, 0.9f, HAIR).rot(0, 0, -12);
        m.part("ahoge2", "ahoge1", 0.4f, -9.2f, -0.8f, -0.45f, -0.9f, -0.45f, 2.6f, 0.9f, 0.9f, HAIR);
        m.part("ahoge3", "ahoge2", 2.6f, -9.2f, -0.8f, -0.45f, -0.1f, -0.45f, 0.9f, 1.9f, 0.9f, HAIR);
        // flowing mane
        m.part("mane1", "head", 0, -1.6f, 2.9f, -5.2f, -1.6f, -0.4f, 10.4f, 9.6f, 4.4f, HAIR).rot(12, 0, 0)
                .pattern(Pattern.GRADIENT_V, HAIR_M, 1).grain(0.1f).decor(Face.BACK, 2, 1, 1, 8, HAIR_D).decor(Face.BACK, 7, 0, 1, 9, HAIR_D);
        m.part("mane2", "mane1", 0, 6.4f, 4.3f, -6.0f, 0, -1.6f, 12f, 7.4f, 4f, HAIR_M).rot(8, 0, 0)
                .pattern(Pattern.GRADIENT_V, HAIR_D, 1).grain(0.1f).decor(Face.BACK, 3, 0, 1, 7, 0xC25814).decor(Face.BACK, 8, 1, 1, 6, 0xC25814);
        m.part("mane3", "mane2", 0, 13.6f, 4.3f, -7f, 0, -1.4f, 14f, 5.4f, 3.4f, HAIR_D).rot(14, 0, 0)
                .pattern(Pattern.GRADIENT_V, 0xB9501A, 1).grain(0.1f);
        m.part("maneTipR", "mane3", -6.2f, 18.8f, 4.3f, -1.3f, 0, -1.1f, 2.6f, 4.2f, 2.2f, HAIR_D).rot(10, 0, 32);
        m.part("maneTipL", "mane3", 6.2f, 18.8f, 4.3f, -1.3f, 0, -1.1f, 2.6f, 4.2f, 2.2f, HAIR_D).rot(10, 0, -32);
        m.part("maneTipM", "mane3", 0, 18.8f, 4.3f, -2.2f, 0, -1.1f, 4.4f, 3.6f, 2.2f, 0xB9501A).rot(24, 0, 0);
        // ---- arms (very long, black spiky claws)
        for (int s = -1; s <= 1; s += 2) {
            String S = s < 0 ? "R" : "L";
            float x = 4.1f * s;
            m.group("arm" + S, "chest", x, 5.6f, 0);
            m.part("sleeve" + S, "arm" + S, x, 5.6f, 0, -1.6f, -1.1f, -1.7f, 3.2f, 3.7f, 3.4f, SHIRT_D).decor(Face.FRONT, 0, 3, 4, 1, 0x3A3A46);
            m.part("upper" + S, "arm" + S, x, 5.6f, 0, -0.9f, 2.4f, -0.9f, 1.8f, 3.8f, 1.8f, SKIN);
            m.part("fore" + S, "arm" + S, x, 11.6f, 0, -1.05f, 0, -1.05f, 2.1f, 4.4f, 2.1f, SKIN).pattern(Pattern.GRADIENT_V, CLAW, 1);
            m.part("hand" + S, "fore" + S, x, 15.8f, 0, -1.8f, 0, -1.8f, 3.6f, 2.4f, 3.6f, CLAW).decor(Face.FRONT, 1, 0, 1, 2, 0x2C2C34);
            m.part("spike" + S, "hand" + S, x, 15.4f, 0.9f, -0.4f, -2.6f, -0.4f, 0.8f, 2.8f, 0.8f, CLAW).rot(-35, 0, -20 * s);
            float[] dx = {-1.4f, -0.47f, 0.47f, 1.4f};
            float[] spread = {-14, -5, 5, 14};
            for (int i = 0; i < 4; i++) {
                String n = "claw" + S + (i + 1);
                float cx = x + dx[i] * (s < 0 ? 1 : -1);
                m.part(n, "hand" + S, cx, 17.8f, -0.5f, -0.55f, 0, -0.55f, 1.1f, 6.4f, 1.1f, CLAW).rot(-8, 0, spread[i] * (s < 0 ? 1 : -1) + 4 * s)
                        .decor(Face.FRONT, 0, 0, 1, 3, 0x34343E);
                m.part(n + "t", n, cx, 24.2f, -0.5f, -0.35f, 0, -0.35f, 0.7f, 4.2f, 0.7f, CLAW).rot(-18, 0, 0);
            }
        }
        // dark-red curved blade (only shown for blade attacks)
        m.group("blade", "handR", -4.1f, 17.0f, 0);
        m.part("bladeHilt", "blade", -4.1f, 17.0f, 0, -0.55f, -0.55f, -2.6f, 1.1f, 1.1f, 3.6f, 0x3C2A2E).decor(Face.TOP, 0, 1, 1, 1, 0x6A5A5E);
        m.part("blade1", "blade", -4.1f, 17.0f, -2.5f, -0.5f, -1.4f, -6, 1, 4.2f, 6, BLADE).rot(-4, 0, 0)
                .decorGlow(Face.RIGHT, 0, 3, 6, 1, BLADE_E).decorGlow(Face.LEFT, 0, 3, 6, 1, BLADE_E).decor(Face.RIGHT, 1, 0, 3, 1, 0x3A0610).decor(Face.LEFT, 1, 0, 3, 1, 0x3A0610)
                .decor(Face.RIGHT, 2, 1, 1, 1, 0x9A1A2C);
        m.part("blade2", "blade1", -4.1f, 17.0f, -8.4f, -0.45f, -1.3f, -5.6f, 0.9f, 3.8f, 5.6f, BLADE).rot(-16, 0, 0)
                .decorGlow(Face.RIGHT, 0, 3, 6, 1, BLADE_E).decorGlow(Face.LEFT, 0, 3, 6, 1, BLADE_E).decor(Face.LEFT, 3, 1, 1, 1, 0x9A1A2C);
        m.part("blade3", "blade2", -4.1f, 17.0f, -13.9f, -0.4f, -1.0f, -5, 0.8f, 2.8f, 5, BLADE).rot(-20, 0, 0)
                .decorGlow(Face.RIGHT, 0, 2, 5, 1, BLADE_E).decorGlow(Face.LEFT, 0, 2, 5, 1, BLADE_E);
        m.part("blade4", "blade3", -4.1f, 17.0f, -18.8f, -0.3f, -0.6f, -4.2f, 0.6f, 1.6f, 4.2f, BLADE_E).rot(-26, 0, 0).glow();
        // white diamond sparkles
        m.part("spark1", "body", 6.5f, -2, -1, -1.1f, -1.1f, -0.3f, 2.2f, 2.2f, 0.6f, 0xFFFFFF).rot(0, 0, 45).glow();
        m.part("spark2", "body", -7, 1, 1, -0.8f, -0.8f, -0.3f, 1.6f, 1.6f, 0.6f, 0xFFFFFF).rot(0, 0, 45).glow();
        m.part("spark3", "body", 4.5f, -6, 2, -0.6f, -0.6f, -0.3f, 1.2f, 1.2f, 0.6f, 0xFFF6E0).rot(0, 0, 45).glow();
        // ---- the little black cat (authored at 2x, scaled down in the animator)
        m.group("cat", "root", 9, 24, 1.5f);
        m.part("catBody", "cat", 7, 24, -3.5f, -3, -5.4f, -2.6f, 6, 5.4f, 6, CAT).grain(0.05f).decor(Face.FRONT, 2, 3, 2, 2, 0x24242C);
        m.part("catPawR", "cat", 5.6f, 24, -6.2f, -1, -1.2f, -0.9f, 2, 1.2f, 1.8f, 0x22222A);
        m.part("catPawL", "cat", 8.4f, 24, -6.2f, -1, -1.2f, -0.9f, 2, 1.2f, 1.8f, 0x22222A);
        m.part("catHead", "cat", 7, 19, -4.2f, -3.5f, -5.6f, -3, 7, 6, 5.5f, CAT).grain(0.05f)
                .decorGlow(Face.FRONT, 0, 1, 3, 3, EYE).decor(Face.FRONT, 1, 2, 1, 1, 0x050505)
                .decorGlow(Face.FRONT, 4, 1, 3, 3, EYE).decor(Face.FRONT, 5, 2, 1, 1, 0x050505);
        m.part("catEarR", "catHead", 4.8f, 13.6f, -4.2f, -1, -2.2f, -0.9f, 2, 2.4f, 1.8f, CAT).rot(0, 0, -18).decor(Face.FRONT, 0, 1, 1, 1, 0x3A2A30);
        m.part("catEarL", "catHead", 9.2f, 13.6f, -4.2f, -1, -2.2f, -0.9f, 2, 2.4f, 1.8f, CAT).rot(0, 0, 18).decor(Face.FRONT, 1, 1, 1, 1, 0x3A2A30);
        m.part("catTail", "cat", 7, 23, 2.2f, -0.7f, -0.7f, 0, 1.4f, 1.4f, 4.2f, CAT).rot(18, 30, 0);
        m.part("catTail2", "catTail", 7, 23, 6.3f, -0.7f, -4.4f, -0.7f, 1.4f, 4.4f, 1.4f, CAT).rot(-30, 0, 0);
        m.animator(FenSpec::animate);
        return m;
    }

    // ================================================================== animation
    static float K(float t, float... kv) { return Anim.curve(t, kv); }
    static void R(ModelParts m, String n, float x, float y, float z) { m.addRot(n, x, y, z); }
    static void M(ModelParts m, String n, float x, float y, float z) { m.move(n, x, y, z); }
    static float S(float deg) { return Anim.sin(deg); }

    /** arm helper: side 'R' / 'L', z & y mirrored so +z is always "outward". */
    static void arm(ModelParts m, char side, float x, float y, float z) { float s = side == 'R' ? 1 : -1; m.addRot("arm" + side, x, y * s, z * s); }
    static void fore(ModelParts m, char side, float x, float y, float z) { float s = side == 'R' ? 1 : -1; m.addRot("fore" + side, x, y * s, z * s); }
    static void hand(ModelParts m, char side, float x, float y, float z) { float s = side == 'R' ? 1 : -1; m.addRot("hand" + side, x, y * s, z * s); }
    /** claw curl (+ = curl inward / grip), spread (+ = fan out) */
    static void claws(ModelParts m, char side, float curl, float spread) {
        float s = side == 'R' ? 1 : -1;
        for (int i = 1; i <= 4; i++) {
            float k = (i - 2.5f) / 1.5f;
            m.addRot("claw" + side + i, -curl, 0, spread * k * s);
            m.addRot("claw" + side + i + "t", -curl * 0.8f, 0, 0);
        }
    }
    static void leg(ModelParts m, char side, float thigh, float shin, float foot, float splay) {
        float s = side == 'R' ? 1 : -1;
        m.addRot("leg" + side, thigh, 0, splay * s); m.addRot("shin" + side, shin, 0, 0); m.addRot("foot" + side, foot, 0, 0);
    }
    static void mane(ModelParts m, float a, float b, float c, float sway) {
        R(m, "mane1", a, sway * 0.4f, sway * 0.3f); R(m, "mane2", b, sway * 0.5f, sway * 0.4f); R(m, "mane3", c, sway * 0.6f, sway * 0.5f);
    }

    static void animate(ModelParts m, AnimCtx c) {
        float age = c.age, t = c.t;
        boolean act = !c.idle();
        float loco = act ? Math.max(1 - c.seg(0, 4), c.seg(c.dur - 4, c.dur)) : 1;
        if (c.is("sprint") || c.is("scuttle")) loco = 0;
        float w = c.walk() * loco;
        float q = Anim.smooth((w - 0.4f) / 0.45f);   // 0 = upright prowl, 1 = on all fours
        float up = w * (1 - q);
        float ph = c.limbSwing * 0.62f;
        float br = S(age * 4.5f);

        // ---------------- stalking idle (always on, abilities layer on top)
        M(m, "body", 0, 1.0f + 0.3f * br, 0);
        R(m, "chest", 14 + 2 * br, 0, 2.5f * S(age * 2.3f));
        R(m, "head", -9 - br + c.headPitch * 0.6f, c.headYaw * 0.75f, 4 * S(age * 1.7f + 40));
        leg(m, 'R', -16, 26, -10, 3);
        leg(m, 'L', -6, 14, -8, 3);
        arm(m, 'R', -12 + 3 * br, 0, 9 + 2 * S(age * 3));
        arm(m, 'L', -7 + 3 * br, 0, 8 + 2 * S(age * 3 + 90));
        fore(m, 'R', -16, 0, 0); fore(m, 'L', -12, 0, 0);
        float tw = (float) Math.pow(Math.max(0, S(age * 7)), 12) * 30;    // occasional claw twitch
        claws(m, 'R', 8 + tw, 4 + tw * 0.5f);
        claws(m, 'L', 6 + (float) Math.pow(Math.max(0, S(age * 7 + 140)), 12) * 30, 4);
        mane(m, 3 * S(age * 3 - 30), 4 * S(age * 3 - 70), 5 * S(age * 3 - 110), 3 * S(age * 2 - 50));
        R(m, "sideR", 0, 0, 3 * S(age * 3 - 20)); R(m, "sideL", 0, 0, -3 * S(age * 3 - 20));
        R(m, "ahoge1", 0, 0, 6 * S(age * 5));
        R(m, "ahoge2", 0, 0, 8 * S(age * 5 - 40));
        m.show("blade", false);
        m.show("tongue", false);
        // sparkles orbit/bob
        for (int i = 1; i <= 3; i++) {
            M(m, "spark" + i, 0, 1.2f * S(age * 6 + i * 120), 0);
            R(m, "spark" + i, 0, age * (6 + i * 3), 0);
        }
        // cat: sits, blinks, tail sways, follows Fen with hops when she moves
        m.scale("cat", 0.45f, 0.45f, 0.45f);
        R(m, "catHead", 4 * S(age * 2), c.headYaw * 0.4f + 10 * S(age * 1.1f), 0);
        R(m, "catTail", 0, 20 * S(age * 4), 0);
        R(m, "catTail2", 12 * S(age * 4 - 60), 0, 0);
        R(m, "catEarR", 0, 0, -6 * (float) Math.pow(Math.max(0, S(age * 5)), 10));
        float hop = Math.abs(S(c.limbSwing * 40)) * w;
        M(m, "cat", 0, -3 * hop, -2 * w);
        R(m, "cat", -10 * hop, 0, 0);

        // ---------------- upright prowl
        if (up > 0.01f) {
            float sw = S(ph * 57.3f);
            M(m, "body", 0, 1.5f * up - Math.abs(sw) * 0.8f * up, 0);
            R(m, "chest", 14 * up, -8 * sw * up, 0);
            R(m, "head", -10 * up, 8 * sw * up, 0);
            leg(m, 'R', -36 * sw * up - 10 * up, Math.max(0, -S(ph * 57.3f + 70)) * 45 * up, 6 * sw * up, 0);
            leg(m, 'L', 36 * sw * up - 10 * up, Math.max(0, S(ph * 57.3f + 70)) * 45 * up, -6 * sw * up, 0);
            arm(m, 'R', 30 * sw * up - 10 * up, 0, 6 * up);
            arm(m, 'L', -30 * sw * up - 10 * up, 0, 6 * up);
            fore(m, 'R', -20 * up, 0, 0); fore(m, 'L', -20 * up, 0, 0);
            mane(m, 18 * up + 5 * sw * up, 6 * up, 6 * up, 6 * sw * up);
        }
        // ---------------- all fours gallop
        if (q > 0.01f) {
            float g = S(ph * 57.3f), g2 = S(ph * 57.3f + 50);
            M(m, "body", 0, 5.5f * q - Math.abs(S(ph * 57.3f + 90)) * 1.2f * q, -1 * q);
            R(m, "chest", 62 * q + 6 * g2 * q, 0, 0);
            R(m, "head", -54 * q - 6 * g2 * q, 0, 0);
            arm(m, 'R', (-108 + 34 * g) * q, 0, -4 * q);
            arm(m, 'L', (-108 + 34 * g2) * q, 0, -4 * q);
            fore(m, 'R', (-6 - Math.max(0, -g) * 40) * q, 0, 0);
            fore(m, 'L', (-6 - Math.max(0, -g2) * 40) * q, 0, 0);
            hand(m, 'R', 30 * q, 0, 0); hand(m, 'L', 30 * q, 0, 0);
            claws(m, 'R', -20 * q, 8 * q); claws(m, 'L', -20 * q, 8 * q);
            leg(m, 'R', (-34 - 34 * g) * q, (72 + 20 * g) * q, -30 * q, 6 * q);
            leg(m, 'L', (-34 - 34 * g2) * q, (72 + 20 * g2) * q, -30 * q, 6 * q);
            mane(m, 40 * q + 8 * g * q, -6 * q + 8 * g2 * q, -6 * q, 4 * g * q);
            R(m, "ahoge1", -40 * q, 0, 0);
        }

        if (act) ability(m, c, t);
        if (c.death > 0) death(m, c.death, age);
    }

    // ================================================================== abilities
    static void ability(ModelParts m, AnimCtx c, float t) {
        switch (c.ability) {
            case "pounce" -> pounce(m, t);
            case "rake" -> rake(m, t);
            case "sprint" -> sprint(m, t);
            case "blade" -> blade(m, t);
            case "crescent" -> crescent(m, t, c.age);
            case "hairwhip" -> hairwhip(m, t);
            case "diamonds" -> diamonds(m, t, c.age);
            case "backflip" -> backflip(m, t);
            case "scuttle" -> scuttle(m, t);
            case "catswarm" -> catswarm(m, t, c.age);
            case "maul" -> maul(m, t);
            case "frenzy" -> frenzy(m, t, c.age);
            default -> {}
        }
    }

    /** pounce: deep crouch, explosive leap with claws overhead, raking landing. hit window ~t12-18 */
    static void pounce(ModelParts m, float t) {
        M(m, "body", 0, K(t, 0, 0, 7, 5, 9, -3, 13, -4, 17, 3, 22, 1.5f, 28, 0), K(t, 0, 0, 7, 1.5f, 9, -1, 16, -2, 28, 0));
        R(m, "chest", K(t, 0, 0, 7, 38, 9, -6, 13, 12, 16, 48, 21, 32, 28, 0), 0, 0);
        R(m, "head", K(t, 0, 0, 7, -32, 9, 4, 13, -6, 16, -36, 21, -20, 28, 0), 0, 0);
        for (char s : new char[] {'R', 'L'}) {
            arm(m, s, K(t, 0, 0, 7, 50, 9, -150, 13, -172, 16, -62, 21, -50, 28, 0), 0, K(t, 0, 0, 7, 14, 13, 30, 16, 6, 28, 0));
            fore(m, s, K(t, 0, 0, 7, -40, 9, 0, 13, -12, 16, -34, 28, 0), 0, 0);
            claws(m, s, K(t, 0, 0, 9, -10, 13, -18, 16, 40, 21, 30, 28, 0), K(t, 0, 0, 9, 16, 13, 26, 16, 6, 28, 0));
        }
        leg(m, 'R', K(t, 0, 0, 7, -60, 9, 34, 13, 18, 16, -64, 21, -44, 28, 0), K(t, 0, 0, 7, 96, 9, 4, 13, 40, 16, 96, 21, 66, 28, 0), K(t, 0, 0, 7, -36, 9, 30, 16, -30, 28, 0), 0);
        leg(m, 'L', K(t, 0, 0, 7, -50, 9, 40, 13, 26, 16, -54, 21, -38, 28, 0), K(t, 0, 0, 7, 90, 9, 8, 13, 46, 16, 90, 21, 60, 28, 0), K(t, 0, 0, 7, -32, 9, 30, 16, -30, 28, 0), 0);
        mane(m, K(t, 0, 0, 7, -10, 10, 45, 15, 22, 18, -14, 23, 6, 28, 0), K(t, 0, 0, 10, 20, 15, 10, 18, -10, 28, 0), K(t, 0, 0, 10, 22, 16, 8, 19, -14, 28, 0), 0);
        R(m, "ahoge1", K(t, 0, 0, 9, -30, 16, 25, 28, 0), 0, 0);
        R(m, "cat", 0, K(t, 0, 0, 8, -30, 20, -30, 28, 0), 0);
    }

    /** rake: right horizontal swipe (t7), left swipe (t14), two-handed overhead downward rake (t23) */
    static void rake(ModelParts m, float t) {
        R(m, "chest", K(t, 0, 0, 5, 18, 7, 26, 10, 14, 12, 24, 14, 26, 18, -8, 21, 6, 23, 44, 27, 30, 30, 0),
                K(t, 0, 0, 5, 42, 7, -34, 10, -30, 12, -44, 14, 36, 18, 0, 30, 0), 0);
        R(m, "head", K(t, 0, 0, 18, 10, 23, -30, 30, 0), K(t, 0, 0, 5, -25, 7, 20, 12, 25, 14, -20, 18, 0, 30, 0), 0);
        M(m, "body", 0, K(t, 0, 0, 5, 1.5f, 7, 2.5f, 12, 1.5f, 14, 2.5f, 18, -1, 23, 3.5f, 30, 0), K(t, 0, 0, 7, -2, 14, -3, 23, -4, 30, 0));
        // right arm: out & back, sweep across
        arm(m, 'R', K(t, 0, 0, 5, -70, 7, -88, 10, -60, 12, -40, 18, -170, 21, -175, 23, -60, 26, -50, 30, 0),
                K(t, 0, 0, 5, 75, 7, -55, 10, -40, 18, 0, 30, 0), K(t, 0, 0, 5, 30, 7, 0, 18, 18, 23, 4, 30, 0));
        fore(m, 'R', K(t, 0, 0, 5, -40, 7, -5, 10, -25, 18, -10, 23, -30, 30, 0), 0, 0);
        claws(m, 'R', K(t, 0, 0, 5, -16, 7, 30, 10, 18, 18, -18, 23, 45, 30, 0), K(t, 0, 0, 5, 22, 7, 4, 18, 22, 23, 0, 30, 0));
        // left arm: sweep at 14
        arm(m, 'L', K(t, 0, 0, 7, -30, 12, -72, 14, -88, 17, -60, 18, -170, 21, -175, 23, -60, 26, -50, 30, 0),
                K(t, 0, 0, 7, 20, 12, 75, 14, -55, 17, -40, 18, 0, 30, 0), K(t, 0, 0, 12, 30, 14, 0, 18, 18, 23, 4, 30, 0));
        fore(m, 'L', K(t, 0, 0, 12, -40, 14, -5, 17, -25, 18, -10, 23, -30, 30, 0), 0, 0);
        claws(m, 'L', K(t, 0, 0, 12, -16, 14, 30, 17, 18, 18, -18, 23, 45, 30, 0), K(t, 0, 0, 12, 22, 14, 4, 18, 22, 23, 0, 30, 0));
        leg(m, 'R', K(t, 0, 0, 5, -20, 7, -34, 14, -14, 23, -40, 30, 0), K(t, 0, 0, 7, 40, 14, 20, 23, 60, 30, 0), 0, 0);
        leg(m, 'L', K(t, 0, 0, 7, 6, 12, -10, 14, -30, 23, -30, 30, 0), K(t, 0, 0, 14, 40, 23, 56, 30, 0), 0, 0);
        mane(m, K(t, 0, 0, 7, 16, 14, 16, 19, -12, 23, 30, 27, 8, 30, 0), K(t, 0, 0, 8, 8, 15, 8, 20, -8, 24, 14, 30, 0), K(t, 0, 0, 9, 8, 16, 8, 21, -10, 25, 14, 30, 0),
                K(t, 0, 0, 5, -20, 7, 30, 12, 20, 14, -30, 18, 0, 30, 0));
    }

    /** sprint: drops to all fours and gallops through the target */
    static void sprint(ModelParts m, float t) {
        float q = K(t, 0, 0, 6, 1, 28, 1, 33, 0);
        float g = Anim.sin(t * 52), g2 = Anim.sin(t * 52 + 60);
        float run = K(t, 0, 0, 6, 0, 8, 1, 27, 1, 30, 0);
        M(m, "body", 0, 6 * q - Math.abs(Anim.sin(t * 52 + 90)) * 2 * run, -1.5f * q);
        R(m, "chest", 70 * q + 8 * g2 * run + K(t, 28, 0, 30, -20, 33, 0), 0, 0);
        R(m, "head", -62 * q - 8 * g2 * run, 0, 0);
        for (char s : new char[] {'R', 'L'}) {
            float gg = s == 'R' ? g : g2;
            arm(m, s, (-112 + 48 * gg * run) * q, 0, -4 * q);
            fore(m, s, (-8 - Math.max(0, -gg) * 50 * run) * q, 0, 0);
            hand(m, s, 32 * q, 0, 0);
            claws(m, s, -20 * q + Math.max(0, gg) * 30 * run, 10 * q);
            float lg = s == 'R' ? g2 : g;
            leg(m, s, (-36 - 48 * lg * run) * q, (76 + 28 * lg * run) * q, -32 * q, 6 * q);
        }
        mane(m, 46 * q + 12 * g * run, -4 * q + 10 * g2 * run, -6 * q + 10 * g * run, 6 * g * run);
        R(m, "ahoge1", -50 * q, 0, 0);
        R(m, "sideR", 30 * q, 0, 20 * q); R(m, "sideL", 30 * q, 0, -20 * q);
    }

    /** blade: draw dark crescent blade, wide slash (t10), backhand + wave (t19), rising slash (t29) */
    static void blade(ModelParts m, float t) {
        m.show("blade", t > 2 && t < 36);
        R(m, "chest", K(t, 0, 0, 8, 10, 10, 30, 14, 20, 17, 10, 19, 26, 24, 34, 29, -18, 33, -6, 38, 0),
                K(t, 0, 0, 8, 55, 10, -50, 14, -55, 17, -60, 19, 40, 23, 10, 29, -6, 38, 0), K(t, 0, 0, 8, -6, 10, 6, 29, 0, 38, 0));
        R(m, "head", K(t, 0, 0, 8, -14, 10, -20, 24, -30, 29, 18, 38, 0), K(t, 0, 0, 8, -40, 10, 40, 17, 45, 19, -30, 24, 0, 38, 0), 0);
        M(m, "body", 0, K(t, 0, 0, 8, 2, 10, 3, 17, 2, 19, 2.5f, 24, 5, 29, -3, 32, 0, 38, 0), K(t, 0, 0, 10, -2.5f, 19, -2, 29, -1, 38, 0));
        arm(m, 'R', K(t, 0, 0, 3, -20, 8, -100, 10, -90, 14, -80, 17, -95, 19, -85, 23, -40, 24, 30, 29, -175, 33, -150, 38, 0),
                K(t, 0, 0, 3, 20, 8, 80, 10, -65, 14, -70, 17, -85, 19, 70, 23, 30, 24, 10, 29, 0, 38, 0),
                K(t, 0, 0, 8, 10, 10, 0, 24, 6, 29, 10, 38, 0));
        fore(m, 'R', K(t, 0, 0, 8, -60, 10, -6, 14, -20, 17, -70, 19, -4, 24, -30, 29, 0, 38, 0), 0, 0);
        hand(m, 'R', K(t, 0, 0, 8, 10, 10, -10, 24, 40, 29, -20, 38, 0), 0, K(t, 0, 0, 8, 30, 10, -10, 17, 40, 19, -20, 24, 0, 38, 0));
        claws(m, 'R', 40 * K(t, 0, 0, 3, 1, 34, 1, 38, 0), 0);
        arm(m, 'L', K(t, 0, 0, 8, -40, 10, 10, 17, -40, 19, 20, 24, -20, 29, 20, 38, 0), 0, K(t, 0, 0, 8, 10, 10, 40, 17, 20, 19, 45, 29, 50, 38, 0));
        fore(m, 'L', K(t, 0, 0, 8, -30, 19, -10, 38, 0), 0, 0);
        claws(m, 'L', 0, K(t, 0, 0, 10, 20, 29, 25, 38, 0));
        leg(m, 'R', K(t, 0, 0, 8, -10, 10, -40, 19, -20, 24, -60, 29, 10, 38, 0), K(t, 0, 0, 10, 50, 19, 30, 24, 90, 29, 0, 38, 0), K(t, 24, -30, 29, 20, 38, 0), 0);
        leg(m, 'L', K(t, 0, 0, 8, 10, 10, 16, 19, 6, 24, -50, 29, 20, 38, 0), K(t, 0, 0, 10, 20, 24, 80, 29, 0, 38, 0), K(t, 24, -30, 29, 30, 38, 0), 0);
        mane(m, K(t, 0, 0, 10, 20, 14, 6, 19, 22, 24, -5, 29, 35, 34, 10, 38, 0), K(t, 0, 0, 11, 10, 20, 12, 30, 20, 38, 0), K(t, 0, 0, 12, 10, 21, 14, 31, 22, 38, 0),
                K(t, 0, 0, 8, -30, 10, 40, 17, 30, 19, -40, 24, 0, 38, 0));
    }

    /** crescent: twirls the blade, then throws two crossing blade waves (t12, t19) and a fan when enraged (t26) */
    static void crescent(ModelParts m, float t, float age) {
        m.show("blade", t > 1 && t < 32);
        float twirl = Anim.linear(t, 1, 0, 11, 720);
        R(m, "chest", K(t, 0, 0, 10, 20, 12, 36, 16, -8, 19, 36, 23, 0, 26, 30, 30, 0, 34, 0),
                K(t, 0, 0, 10, 20, 12, -40, 16, -30, 19, 40, 23, 10, 26, -20, 34, 0), K(t, 0, 0, 10, -14, 12, 16, 16, 10, 19, -16, 23, 0, 34, 0));
        R(m, "head", K(t, 0, 0, 10, -20, 12, -10, 19, -10, 34, 0), K(t, 0, 0, 12, 30, 19, -30, 26, 0, 34, 0), 0);
        M(m, "body", 0, K(t, 0, 0, 10, 2, 12, 3.5f, 16, 1, 19, 3.5f, 23, 1, 26, 3, 34, 0), 0);
        // right arm: raised twirl, then down-left diagonal (12), up for second (16), down-right (19), horizontal sweep (26)
        arm(m, 'R', K(t, 0, 0, 3, -150, 10, -160, 12, -40, 16, -150, 19, -50, 23, -90, 26, -88, 30, -40, 34, 0),
                K(t, 0, 0, 10, 10, 12, -40, 16, -30, 19, 50, 23, 70, 26, -60, 30, -40, 34, 0),
                K(t, 0, 0, 10, 30, 12, -10, 16, -6, 19, 30, 26, 0, 34, 0));
        fore(m, 'R', K(t, 0, 0, 10, -20, 12, 0, 16, -40, 19, 0, 23, -30, 26, 0, 34, 0), 0, 0);
        m.addRot("handR", 0, twirl, 0);
        m.addRot("handR", K(t, 10, 0, 12, -30, 16, 30, 19, -30, 23, 0, 34, 0), 0, 0);
        claws(m, 'R', 40 * K(t, 0, 0, 2, 1, 30, 1, 34, 0), 0);
        arm(m, 'L', K(t, 0, 0, 10, -60, 12, 20, 16, -40, 19, 30, 26, -60, 34, 0), 0, K(t, 0, 0, 10, 50, 12, 30, 19, 50, 26, 70, 34, 0));
        claws(m, 'L', 0, K(t, 0, 0, 10, 20, 34, 0));
        leg(m, 'R', K(t, 0, 0, 10, -20, 12, -46, 19, -16, 26, -40, 34, 0), K(t, 0, 0, 12, 60, 19, 30, 26, 56, 34, 0), 0, 0);
        leg(m, 'L', K(t, 0, 0, 10, 0, 12, 10, 19, -40, 26, -20, 34, 0), K(t, 0, 0, 12, 20, 19, 56, 26, 40, 34, 0), 0, 0);
        mane(m, K(t, 0, 0, 11, 15, 13, 24, 17, 6, 20, 24, 27, 18, 34, 0), K(t, 0, 0, 12, 10, 20, 14, 34, 0), K(t, 0, 0, 13, 10, 21, 16, 34, 0), 8 * Anim.sin(age * 20) * K(t, 0, 0, 3, 1, 11, 1, 13, 0));
    }

    /** hairwhip: coils, spins a full turn so the mane lashes in a ring (hit t13), hair settles with overshoot */
    static void hairwhip(ModelParts m, float t) {
        float spin = Anim.curve(t, 0, 0, 8, 50, 18, -310, 22, -360) + (t > 22 ? 360 : 0);
        R(m, "body", 0, t < 22 ? spin : K(t, 22, 0, 30, 0), 0);
        M(m, "body", 0, K(t, 0, 0, 8, 3, 12, -1, 18, 0, 22, 2, 30, 0), 0);
        R(m, "chest", K(t, 0, 0, 8, 26, 12, 4, 18, 8, 22, 22, 30, 0), K(t, 0, 0, 8, 30, 12, -20, 18, -10, 30, 0), 0);
        R(m, "head", K(t, 0, 0, 8, -10, 12, 6, 18, 0, 30, 0), K(t, 0, 0, 8, 40, 11, -40, 18, -20, 30, 0), K(t, 0, 0, 12, 20, 22, 0));
        for (char s : new char[] {'R', 'L'}) {
            arm(m, s, K(t, 0, 0, 8, s == 'R' ? -40 : 20, 11, -10, 18, -20, 22, -20, 30, 0), 0, K(t, 0, 0, 8, 20, 11, 85, 18, 75, 22, 20, 30, 0));
            fore(m, s, K(t, 0, 0, 8, -60, 11, -5, 18, -10, 30, 0), 0, 0);
            claws(m, s, K(t, 0, 0, 8, 30, 11, -20, 20, -10, 30, 0), K(t, 0, 0, 11, 25, 20, 20, 30, 0));
        }
        leg(m, 'R', K(t, 0, 0, 8, -40, 11, -10, 18, -20, 22, -40, 30, 0), K(t, 0, 0, 8, 70, 11, 20, 22, 60, 30, 0), 0, K(t, 8, 0, 11, 14, 18, 14, 22, 0));
        leg(m, 'L', K(t, 0, 0, 8, -30, 11, -10, 18, -20, 22, -30, 30, 0), K(t, 0, 0, 8, 60, 11, 20, 22, 50, 30, 0), 0, K(t, 8, 0, 11, 14, 18, 14, 22, 0));
        // mane flares out horizontally while spinning, lags behind, then swings back past rest
        mane(m, K(t, 0, 0, 7, -15, 11, 38, 17, 42, 21, -30, 25, 15, 30, 0), K(t, 0, 0, 8, -10, 12, -8, 18, -8, 22, -25, 26, 10, 30, 0),
                K(t, 0, 0, 9, -10, 13, -10, 19, -10, 23, -25, 27, 10, 30, 0), K(t, 0, 0, 8, -40, 12, 60, 18, 60, 22, -30, 26, 10, 30, 0));
        R(m, "sideR", 0, 0, K(t, 8, 0, 12, 50, 18, 50, 22, 0)); R(m, "sideL", 0, 0, -K(t, 8, 0, 12, 50, 18, 50, 22, 0));
    }

    /** diamonds: gathers sparkles (crossed arms), flings diamond fans right (t9), left (t17), both (t24 enraged) */
    static void diamonds(ModelParts m, float t, float age) {
        float charge = K(t, 0, 0, 7, 1, 9, 0.6f, 15, 1, 17, 0.6f, 22, 1, 24, 0.3f, 32, 0);
        for (int i = 1; i <= 3; i++) {
            float sc = 1 + charge * 1.2f;
            m.scale("spark" + i, sc, sc, sc);
            R(m, "spark" + i, 0, age * 20 * charge, 0);
            M(m, "spark" + i, 0, -3 * charge, -2 * charge);
        }
        R(m, "chest", K(t, 0, 0, 7, -12, 9, 22, 15, -10, 17, 22, 22, -18, 24, 26, 32, 0), K(t, 0, 0, 7, -20, 9, 40, 15, 10, 17, -40, 22, 0, 32, 0), 0);
        R(m, "head", K(t, 0, 0, 7, 10, 9, -10, 17, -10, 22, 20, 24, -15, 32, 0), K(t, 0, 0, 9, -30, 17, 30, 24, 0), 0);
        M(m, "body", 0, K(t, 0, 0, 7, -1, 9, 2, 15, -1, 17, 2, 22, -1.5f, 24, 2.5f, 32, 0), 0);
        arm(m, 'R', K(t, 0, 0, 7, -80, 9, -90, 13, -60, 15, -60, 17, -40, 22, -170, 24, -70, 32, 0),
                K(t, 0, 0, 7, -50, 9, 80, 13, 60, 17, 20, 24, 0, 32, 0), K(t, 0, 0, 7, -20, 9, 20, 22, 10, 24, 30, 32, 0));
        arm(m, 'L', K(t, 0, 0, 7, -80, 9, -60, 15, -80, 17, -90, 21, -60, 22, -170, 24, -70, 32, 0),
                K(t, 0, 0, 7, -50, 9, -20, 15, -50, 17, 80, 21, 60, 24, 0, 32, 0), K(t, 0, 0, 7, -20, 15, -20, 17, 20, 22, 10, 24, 30, 32, 0));
        fore(m, 'R', K(t, 0, 0, 7, -50, 9, 0, 15, -20, 24, 0, 32, 0), 0, 0);
        fore(m, 'L', K(t, 0, 0, 7, -50, 15, -50, 17, 0, 24, 0, 32, 0), 0, 0);
        claws(m, 'R', K(t, 0, 0, 7, 40, 9, -30, 15, 10, 22, 40, 24, -30, 32, 0), K(t, 0, 0, 9, 30, 24, 30, 32, 0));
        claws(m, 'L', K(t, 0, 0, 7, 40, 15, 40, 17, -30, 22, 40, 24, -30, 32, 0), K(t, 0, 0, 17, 30, 24, 30, 32, 0));
        leg(m, 'R', K(t, 0, 0, 9, -24, 17, 0, 24, -30, 32, 0), K(t, 0, 0, 9, 40, 17, 10, 24, 50, 32, 0), 0, 0);
        leg(m, 'L', K(t, 0, 0, 9, 0, 17, -24, 24, -30, 32, 0), K(t, 0, 0, 9, 10, 17, 40, 24, 50, 32, 0), 0, 0);
        mane(m, K(t, 0, 0, 7, 30, 9, -5, 17, -5, 22, 40, 24, -10, 32, 0), K(t, 0, 0, 7, 10, 24, -10, 32, 0), K(t, 0, 0, 7, 10, 24, -10, 32, 0), K(t, 0, 0, 9, 30, 17, -30, 24, 0));
    }

    /** backflip: claw jab (t5), kicks off backwards into a full flip slashing a wave mid-air (t13), lands on all fours */
    static void backflip(ModelParts m, float t) {
        float flip = Anim.curve(t, 7, 0, 19, -360);
        R(m, "body", flip, 0, 0);
        M(m, "body", 0, K(t, 0, 0, 5, 1, 7, 4, 10, -6, 16, -7, 19, 3, 23, 5, 32, 0), K(t, 0, 0, 5, -2, 7, 0, 32, 0));
        R(m, "chest", K(t, 0, 0, 3, -10, 5, 26, 7, 30, 10, -10, 13, 10, 19, 50, 24, 40, 32, 0), K(t, 0, 0, 3, 30, 5, -30, 7, 0), 0);
        R(m, "head", K(t, 0, 0, 5, -10, 10, 20, 19, -40, 24, -30, 32, 0), 0, 0);
        arm(m, 'R', K(t, 0, 0, 3, 30, 5, -95, 7, -40, 10, -160, 13, -40, 16, -130, 19, -100, 24, -60, 32, 0), K(t, 0, 0, 3, 20, 5, -10, 7, 0), K(t, 0, 0, 10, 40, 13, 20, 19, 0, 32, 0));
        arm(m, 'L', K(t, 0, 0, 5, 20, 7, -40, 10, -160, 13, -30, 16, -130, 19, -100, 24, -60, 32, 0), 0, K(t, 0, 0, 10, 40, 13, 20, 19, 0, 32, 0));
        fore(m, 'R', K(t, 0, 0, 3, -60, 5, 0, 10, -20, 13, 0, 19, -10, 32, 0), 0, 0);
        fore(m, 'L', K(t, 0, 0, 10, -20, 13, 0, 32, 0), 0, 0);
        claws(m, 'R', K(t, 0, 0, 3, 30, 5, -20, 10, 30, 13, -30, 19, -20, 32, 0), K(t, 0, 0, 13, 30, 24, 10, 32, 0));
        claws(m, 'L', K(t, 0, 0, 10, 30, 13, -30, 19, -20, 32, 0), K(t, 0, 0, 13, 30, 24, 10, 32, 0));
        for (char s : new char[] {'R', 'L'}) leg(m, s, K(t, 0, 0, 5, -20, 7, -50, 9, 20, 12, -90, 16, -100, 19, -60, 24, -50, 32, 0),
                K(t, 0, 0, 5, 30, 7, 90, 9, 0, 12, 120, 16, 120, 19, 90, 24, 80, 32, 0), K(t, 7, -20, 9, 30, 19, -20, 32, 0), 0);
        mane(m, K(t, 0, 0, 7, -10, 10, -40, 14, 40, 19, 80, 23, 10, 32, 0), K(t, 0, 0, 10, -20, 15, 20, 20, 20, 32, 0), K(t, 0, 0, 11, -20, 16, 20, 21, 20, 32, 0), 0);
    }

    /** scuttle: flattens to the floor and skitters forward spider-like, then erupts upward with a claw rake (t24) */
    static void scuttle(ModelParts m, float t) {
        float low = K(t, 0, 0, 6, 1, 21, 1, 24, 0);
        float cyc = K(t, 5, 0, 7, 1, 21, 1, 22, 0);
        float a = Anim.sin(t * 80), b = Anim.sin(t * 80 + 180);
        M(m, "body", 0, 9.5f * low + K(t, 21, 0, 24, -4, 27, -2, 34, 0), -2 * low);
        R(m, "body", 0, 8 * a * cyc, 4 * b * cyc);
        R(m, "chest", 80 * low + K(t, 21, 0, 24, -28, 28, -10, 34, 0), 0, 0);
        R(m, "head", -76 * low + K(t, 21, 0, 24, 10, 34, 0), 6 * a * cyc, 0);
        // spider-like limbs: arms forward & splayed, legs splayed out sideways
        arm(m, 'R', (-150 + 30 * a * cyc) * low + K(t, 21, 0, 22, 20, 24, -175, 28, -150, 34, 0), 20 * a * cyc, 30 * low + K(t, 22, 0, 24, 25, 34, 0));
        arm(m, 'L', (-150 + 30 * b * cyc) * low + K(t, 21, 0, 22, 20, 24, -175, 28, -150, 34, 0), 20 * b * cyc, 30 * low + K(t, 22, 0, 24, 25, 34, 0));
        fore(m, 'R', (-30 + 20 * b * cyc) * low, 0, 0); fore(m, 'L', (-30 + 20 * a * cyc) * low, 0, 0);
        hand(m, 'R', 40 * low, 0, 0); hand(m, 'L', 40 * low, 0, 0);
        claws(m, 'R', -20 * low + K(t, 22, 0, 24, 50, 30, 20, 34, 0), 14 * low);
        claws(m, 'L', -20 * low + K(t, 22, 0, 24, 50, 30, 20, 34, 0), 14 * low);
        leg(m, 'R', (-20 + 30 * b * cyc) * low + K(t, 21, 0, 23, -40, 26, 10, 34, 0), (60 + 30 * Math.max(0, a) * cyc) * low, -30 * low, 60 * low);
        leg(m, 'L', (-20 + 30 * a * cyc) * low + K(t, 21, 0, 23, -40, 26, 10, 34, 0), (60 + 30 * Math.max(0, b) * cyc) * low, -30 * low, 60 * low);
        mane(m, 60 * low + 6 * a * cyc + K(t, 21, 0, 25, -30, 30, 10, 34, 0), 4 * b * cyc + K(t, 22, 0, 26, -20, 34, 0), 6 * a * cyc, 10 * a * cyc);
        R(m, "ahoge1", -50 * low, 0, 0);
    }

    /** catswarm: crouches by her cat, sends it pouncing - shadow cats swarm the target (hits t16/22/28) */
    static void catswarm(ModelParts m, float t, float age) {
        float crouch = K(t, 0, 0, 8, 1, 12, 0.6f, 32, 0.6f, 40, 0);
        float laugh = K(t, 12, 0, 15, 1, 30, 1, 34, 0) * Anim.sin(t * 70);
        M(m, "body", 0, 6 * crouch, 0);
        R(m, "chest", 30 * crouch + 5 * laugh, K(t, 0, 0, 8, -20, 12, 10, 40, 0), 0);
        R(m, "head", -20 * crouch - 6 * laugh, K(t, 0, 0, 8, -40, 12, 0), K(t, 0, 0, 8, -20, 12, 10, 30, 10, 40, 0));
        arm(m, 'R', K(t, 0, 0, 6, -20, 8, -10, 10, -40, 12, -100, 18, -95, 30, -90, 40, 0), K(t, 0, 0, 8, -20, 12, 0), K(t, 0, 0, 8, -10, 12, 10, 40, 0));
        fore(m, 'R', K(t, 0, 0, 8, -10, 12, 0, 30, 0, 40, 0), 0, 0);
        claws(m, 'R', K(t, 0, 0, 8, 10, 12, -30, 30, -30, 40, 0), K(t, 0, 0, 12, 30, 30, 30, 40, 0));
        arm(m, 'L', K(t, 0, 0, 8, -30, 12, -20, 40, 0), 0, K(t, 0, 0, 8, 10, 12, 30, 40, 0));
        fore(m, 'L', K(t, 0, 0, 8, -40, 12, -60, 40, 0), 0, 0);
        claws(m, 'L', 0, 25 * crouch);
        leg(m, 'R', -60 * crouch, 100 * crouch, -40 * crouch, 6 * crouch);
        leg(m, 'L', -30 * crouch, 110 * crouch, -10 * crouch, 6 * crouch);
        mane(m, 20 * crouch + 4 * laugh, 4 * laugh, 4 * laugh, 0);
        // the cat swells, leaps at the target and returns
        float sc = 0.45f + K(t, 6, 0, 10, 0.3f, 26, 0.3f, 34, 0);
        m.scale("cat", sc, sc, sc);
        M(m, "cat", K(t, 8, 0, 12, -8, 30, -8, 36, 0), K(t, 6, 0, 9, 1, 12, -8, 16, -3, 26, -3, 30, -6, 36, 0), K(t, 8, 0, 12, -10, 18, -16, 26, -16, 36, 0));
        R(m, "cat", K(t, 6, 0, 9, 20, 12, -40, 16, 10, 26, 0, 30, -30, 36, 0), K(t, 26, 0, 28, 180, 36, 0), 0);
        R(m, "catHead", K(t, 6, 0, 9, 25, 12, -30, 26, 0), 0, 0);
        R(m, "catTail", K(t, 6, 0, 9, -40, 12, 30, 26, 0), 0, 0);
        R(m, "catEarR", 0, 0, K(t, 6, 0, 9, 30, 26, 30, 30, 0)); R(m, "catEarL", 0, 0, -K(t, 6, 0, 9, 30, 26, 30, 30, 0));
    }

    /** maul (canon): lunging bite (t7) - grabs, slams the victim down three times (t14/23/32) and hurls it (t37) */
    static void maul(ModelParts m, float t) {
        m.show("tongue", t > 3 && t < 41);
        R(m, "tongue", K(t, 3, -60, 7, -30, 12, 10, 14, 30, 23, 30, 32, 30, 40, 0) + 10 * Anim.sin(t * 40), 0, 8 * Anim.sin(t * 30));
        float[] sl = {14, 23, 32};
        float slam = 0;
        for (float s : sl) slam += K(t, s - 5, 0, s - 1, -1, s, 1, s + 3, 0.6f, s + 5, 0);
        M(m, "body", 0, K(t, 0, 0, 5, 3, 7, 2, 10, 0, 40, 0, 44, 0) + Math.max(0, slam) * 3 - Math.max(0, -slam) * 1.5f, K(t, 0, 0, 5, -2, 7, -3, 40, -3, 44, 0));
        R(m, "chest", K(t, 0, 0, 5, 40, 7, 34, 10, 0, 37, 0, 39, 30, 44, 0) + slam * 35, K(t, 34, 0, 37, 50, 39, -40, 44, 0), 0);
        R(m, "head", K(t, 0, 0, 5, -10, 7, 18, 10, 0, 44, 0) - slam * 20, 0, 0);
        for (char s : new char[] {'R', 'L'}) {
            float lift = K(t, 0, 0, 5, -80, 7, -95, 10, -175, 37, -175, 39, -60, 44, 0);
            arm(m, s, t > 10 && t < 37 ? -175 + Math.max(0, slam) * 130 + Math.max(0, -slam) * 10 : lift, K(t, 34, 0, 37, 30, 39, -30, 44, 0), K(t, 0, 0, 7, 10, 10, -14, 37, -14, 44, 0));
            fore(m, s, K(t, 0, 0, 5, -20, 7, -40, 10, -20, 37, -20, 44, 0), 0, 0);
            claws(m, s, K(t, 0, 0, 5, -20, 7, 50, 37, 50, 39, -20, 44, 0), K(t, 0, 0, 5, 30, 7, 5, 44, 0));
        }
        leg(m, 'R', K(t, 0, 0, 5, -40, 7, -30, 10, -20, 44, 0) - Math.max(0, slam) * 30, K(t, 0, 0, 5, 60, 10, 30, 44, 0) + Math.max(0, slam) * 50, 0, 0);
        leg(m, 'L', K(t, 0, 0, 5, 10, 10, -10, 44, 0) - Math.max(0, slam) * 20, K(t, 0, 0, 5, 20, 10, 30, 44, 0) + Math.max(0, slam) * 40, 0, 0);
        mane(m, 20 * slam + K(t, 0, 0, 5, 30, 10, 0), 10 * slam, 10 * slam, 0);
    }

    /** frenzy (enraged): roar, six alternating claw swipes (t10..35), finishing X-slash (t42) */
    static void frenzy(ModelParts m, float t, float age) {
        float roar = K(t, 0, 0, 4, 1, 8, 1, 10, 0);
        float shake = Anim.sin(age * 90) * (roar * 3 + K(t, 8, 0, 10, 1, 38, 1, 40, 0));
        M(m, "body", shake * 0.3f, 2 * roar + K(t, 8, 0, 10, 2, 38, 2, 40, 0, 42, 4, 48, 0), 0);
        R(m, "chest", -14 * roar, 0, shake);
        R(m, "head", -40 * roar + 10, 0, shake * 2);
        arm(m, 'R', -40 * roar, 0, 80 * roar);
        arm(m, 'L', -40 * roar, 0, 80 * roar);
        claws(m, 'R', -30 * roar, 30 * roar); claws(m, 'L', -30 * roar, 30 * roar);
        mane(m, 60 * roar + shake * 3, 20 * roar, 20 * roar, shake * 4);
        R(m, "ahoge1", -30 * roar, 0, 0);
        // flurry: swipe i peaks at 10 + 5i, alternate arms
        for (int i = 0; i < 6; i++) {
            float pk = 10 + 5 * i;
            char s = i % 2 == 0 ? 'R' : 'L';
            float sg = s == 'R' ? 1 : -1;
            float k = K(t, pk - 4, 0, pk - 2, 1, pk, 0, pk + 3, 0);   // wind
            float h = K(t, pk - 2, 0, pk, 1, pk + 2, 0.6f, pk + 4, 0); // strike
            arm(m, s, -60 * k - 90 * h, 70 * k - 60 * h, 40 * k);
            fore(m, s, -50 * k, 0, 0);
            claws(m, s, -20 * k + 40 * h, 20 * k);
            R(m, "chest", 20 * h, (40 * k - 40 * h) * sg, 0);
            R(m, "head", 0, (-20 * k + 25 * h) * sg, 0);
            leg(m, s, -30 * h, 40 * h, 0, 0);
            mane(m, 15 * h, 5 * h, 5 * h, (30 * h - 15 * k) * sg);
        }
        // final X slash
        float xw = K(t, 36, 0, 40, 1, 42, 0), xs = K(t, 40, 0, 42, 1, 45, 0.7f, 48, 0);
        for (char s : new char[] {'R', 'L'}) {
            arm(m, s, -175 * xw - 50 * xs, 0, -30 * xw + 60 * xs);
            fore(m, s, -20 * xw, 0, 0);
            claws(m, s, -30 * xw + 50 * xs, 30 * xw);
            leg(m, s, -50 * xs, 80 * xs, -20 * xs, 0);
        }
        R(m, "chest", -20 * xw + 45 * xs, 0, 0);
        R(m, "head", 20 * xw - 30 * xs, 0, 0);
        M(m, "body", 0, -2 * xw + 3 * xs, -2 * xs);
        mane(m, -10 * xw + 50 * xs, 10 * xs, 10 * xs, 0);
    }

    // ================================================================== death
    static void death(ModelParts m, float d, float age) {
        float twitch = Anim.sin(age * 120) * K(d, 0, 0, 0.2f, 1, 0.5f, 0.5f, 0.75f, 0.8f, 1, 0);
        M(m, "body", 0, K(d, 0, 0, 0.25f, 2, 0.55f, 4, 1, 6.5f), K(d, 0, 0, 1, -4));
        R(m, "body", K(d, 0, 0, 0.25f, -12, 0.55f, 30, 0.85f, 84, 1, 86), 0, K(d, 0, 0, 0.3f, 8, 1, 4));
        R(m, "chest", K(d, 0, 0, 0.25f, -20, 0.6f, 10, 1, 4), 0, 0);
        R(m, "head", K(d, 0, 0, 0.25f, -30, 0.7f, 10, 1, -30), K(d, 0.6f, 0, 1, 40), twitch * 6);
        for (char s : new char[] {'R', 'L'}) {
            arm(m, s, K(d, 0, 0, 0.25f, -30, 0.6f, -120, 1, -150), 0, K(d, 0, 0, 0.25f, 40, 1, 30));
            fore(m, s, K(d, 0, 0, 0.6f, -30, 1, 0), 0, 0);
            claws(m, s, twitch * 30 + K(d, 0.7f, 0, 1, 40), K(d, 0, 0, 0.3f, 30, 1, 10));
            leg(m, s, K(d, 0, 0, 0.3f, -30, 0.6f, 10, 1, 0), K(d, 0, 0, 0.3f, 70, 0.6f, 20, 1, 30), 0, K(d, 0.5f, 0, 1, 8));
        }
        mane(m, K(d, 0, 0, 0.3f, 40, 0.8f, -30, 1, -60), K(d, 0.5f, 0, 1, 10), K(d, 0.5f, 0, 1, 10), 0);
        R(m, "ahoge1", K(d, 0.5f, 0, 1, 60), 0, 0);
        for (int i = 1; i <= 3; i++) { float sc = 1 - d; m.scale("spark" + i, sc, sc, sc); }
        // cat creeps up and lowers its head
        M(m, "cat", K(d, 0.4f, 0, 1, -4), 0, K(d, 0.4f, 0, 1, -3));
        R(m, "catHead", K(d, 0.4f, 0, 1, 30), 0, 0);
        R(m, "catEarR", 0, 0, -K(d, 0.4f, 0, 1, 30)); R(m, "catEarL", 0, 0, K(d, 0.4f, 0, 1, 30));
    }
}
