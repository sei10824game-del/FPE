package com.fpe.client.spec;

import com.fpe.client.model.Anim;
import com.fpe.client.model.AnimCtx;
import com.fpe.client.model.ModelParts;
import com.fpe.client.model.ModelSpec;
import com.fpe.client.model.ModelSpec.Face;
import com.fpe.client.model.ModelSpec.Pattern;

/**
 * ∆iden: small, blood-stained child in a fur ushanka (triangle emblem), long black hair, tired sunken eyes with a scar,
 * navy army coat over a white undershirt, black/orange scarf, fingerless gloves, jeans, boots.
 * Every tool from the workshop wall is a separate prop sub-model, only visible while that tool is in use.
 */
public final class AidenSpec {
    private AidenSpec() {}

    static final int SKIN = 0xE8DAD0, SKIN_D = 0xC9B4AA, COAT = 0x2D3957, COAT_D = 0x222B44, COAT_L = 0x3D4B6E, SHIRT = 0xD6D0C2,
            JEANS = 0x3F4F72, BOOT = 0x2B231E, HAIR = 0x15151B, HAIR_L = 0x26262F, FUR = 0xCDB99A, FUR_L = 0xE0D0B2, FUR_D = 0xA8957A,
            BLOOD = 0x7A1414, BLOOD_D = 0x4E0C0C, GLOVE = 0x17171B, WOOD = 0x7A5534, WOOD_D = 0x5A3D24, STEEL = 0xA4AAB2, STEEL_D = 0x5E636C,
            IRON = 0x3E4248;

    static final String[] PROPS = {"axe", "axeL", "hammer", "saw", "knivesR", "knivesL", "crowbar", "pliers", "drill", "nailgun"};

    public static final ModelSpec SPEC = build();

    private static ModelSpec build() {
        ModelSpec m = new ModelSpec("aiden");
        m.group("root", null, 0, 24, 0);
        m.group("body", "root", 0, 14.5f, 0);
        // ---- legs
        for (int s = -1; s <= 1; s += 2) {
            String S = s < 0 ? "R" : "L";
            float x = 1.6f * s;
            m.part("leg" + S, "body", x, 14.5f, 0, -1.5f, 0, -1.5f, 3, 4.2f, 3, JEANS).grain(0.1f).decor(Face.FRONT, 1, 2, 1, 1, 0x2E3B58);
            m.part("shin" + S, "leg" + S, x, 18.5f, 0, -1.45f, 0, -1.45f, 2.9f, 3.6f, 2.9f, JEANS).grain(0.12f)
                    .decor(Face.FRONT, 0, 1, 2, 1, 0x5A6A8C).decor(Face.FRONT, 1, 2, 1, 1, BLOOD_D);
            m.part("boot" + S, "shin" + S, x, 22, 0, -1.7f, 0, -2.4f, 3.4f, 2, 3.9f, BOOT).decor(Face.FRONT, 0, 0, 4, 1, 0x3E342C)
                    .decor(Face.TOP, 1, 0, 1, 2, 0x4A3E34);
        }
        // ---- torso: navy army coat, white undershirt, belt, scarf
        m.group("chest", "body", 0, 14.5f, 0);
        m.part("coat", "chest", 0, 14.5f, 0, -3.6f, -8, -2.1f, 7.2f, 8, 4.2f, COAT).grain(0.1f)
                .decor(Face.FRONT, 3, 0, 2, 8, SHIRT).decor(Face.FRONT, 2, 0, 1, 8, COAT_D).decor(Face.FRONT, 5, 0, 1, 8, COAT_D)
                .decor(Face.FRONT, 5, 4, 1, 1, 0xB8A060).decor(Face.FRONT, 3, 3, 1, 2, BLOOD).decor(Face.FRONT, 4, 5, 1, 1, BLOOD_D)
                .decor(Face.FRONT, 0, 5, 2, 1, COAT_L).decor(Face.FRONT, 6, 5, 2, 1, COAT_L).decor(Face.FRONT, 1, 2, 1, 1, BLOOD_D)
                .decor(Face.BACK, 2, 2, 2, 1, BLOOD_D).decor(Face.BACK, 5, 4, 1, 2, 0x1C2236);
        m.part("belt", "chest", 0, 14.5f, 0, -3.75f, -1.3f, -2.25f, 7.5f, 1.1f, 4.5f, 0x4A3424).decor(Face.FRONT, 3, 0, 2, 1, 0x9A8A50);
        m.part("coatTail", "chest", 0, 14.5f, 0, -3.8f, 0, -2.3f, 7.6f, 2.8f, 4.6f, COAT_D).grain(0.1f)
                .decor(Face.FRONT, 3, 0, 2, 3, JEANS).decor(Face.FRONT, 0, 2, 8, 1, 0x1A2236).decor(Face.FRONT, 6, 1, 1, 1, BLOOD_D);
        m.part("scarf", "chest", 0, 14.5f, 0, -3.95f, -8.7f, -2.5f, 7.9f, 2, 5, 0x1A1A1E).pattern(Pattern.STRIPE_V, 0xE07A1E, 2);
        m.part("scarfTail", "chest", 2, 7.5f, -2.5f, -1, 0, -0.5f, 2, 5.2f, 0.8f, 0xE07A1E).pattern(Pattern.STRIPE_H, 0x1A1A1E, 1).rot(-6, 0, -6);
        // pouch with tool handles on the belt (always visible)
        m.part("pouch", "chest", 3.4f, 13.5f, 0.5f, -0.6f, -0.5f, -1.5f, 1.6f, 2.6f, 3, 0x4A3424);
        m.part("pouchTool", "pouch", 3.4f, 13.5f, 0.5f, -0.2f, -2.4f, -0.4f, 0.6f, 2.2f, 0.6f, WOOD).rot(0, 0, -10);
        // ---- head
        m.group("head", "chest", 0, 6.5f, 0);
        m.part("skull", "head", 0, 6.5f, 0, -4.5f, -9, -4, 9, 9, 8, SKIN).grain(0.05f)
                // tired, half-lidded big eyes with dark bags
                .decor(Face.FRONT, 1, 3, 3, 1, 0x3E343C).decor(Face.FRONT, 1, 4, 3, 2, 0xF2EEE8).decor(Face.FRONT, 2, 5, 1, 1, 0x101014)
                .decor(Face.FRONT, 5, 3, 3, 1, 0x3E343C).decor(Face.FRONT, 5, 4, 3, 2, 0xF2EEE8).decor(Face.FRONT, 6, 5, 1, 1, 0x101014)
                .decorGlow(Face.FRONT, 1, 4, 1, 1, 0xFFFFFF).decorGlow(Face.FRONT, 5, 4, 1, 1, 0xFFFFFF)
                .decor(Face.FRONT, 1, 6, 3, 1, 0xA88E9C).decor(Face.FRONT, 5, 6, 3, 1, 0xA88E9C)
                // scar by the right eye, flat mouth, blood
                .decor(Face.FRONT, 8, 2, 1, 4, 0x9A3A3A).decor(Face.FRONT, 0, 3, 1, 1, 0x9A3A3A)
                .decor(Face.FRONT, 3, 7, 3, 1, 0x5A3A3E)
                .decor(Face.FRONT, 0, 6, 1, 3, BLOOD).decor(Face.FRONT, 1, 7, 1, 1, BLOOD_D).decor(Face.FRONT, 6, 1, 2, 1, BLOOD)
                .decor(Face.FRONT, 7, 7, 1, 2, BLOOD).decor(Face.FRONT, 4, 8, 1, 1, BLOOD_D)
                .decor(Face.LEFT, 2, 6, 2, 2, BLOOD_D).decor(Face.RIGHT, 5, 5, 1, 2, BLOOD);
        // long black hair
        m.part("bangs", "head", 0, 6.5f, 0, -4.7f, -9.2f, -4.4f, 9.4f, 3.2f, 1.1f, HAIR)
                .decor(Face.FRONT, 2, 2, 1, 1, HAIR_L).decor(Face.FRONT, 6, 2, 1, 1, HAIR_L).decor(Face.FRONT, 4, 2, 1, 1, SKIN_D);
        m.part("hairSideR", "head", -4.4f, -1.5f, -2.6f, -0.9f, 0, -1.3f, 1.8f, 11.5f, 2.6f, HAIR).rot(0, 0, 4).pattern(Pattern.GRADIENT_V, HAIR_L, 1);
        m.part("hairSideL", "head", 4.4f, -1.5f, -2.6f, -0.9f, 0, -1.3f, 1.8f, 11.5f, 2.6f, HAIR).rot(0, 0, -4).pattern(Pattern.GRADIENT_V, HAIR_L, 1);
        m.part("hairBack", "head", 0, -1.5f, 3.4f, -4.9f, 0, -0.9f, 9.8f, 11, 2.2f, HAIR).rot(6, 0, 0).decor(Face.BACK, 3, 0, 1, 11, HAIR_L).decor(Face.BACK, 7, 2, 1, 9, HAIR_L);
        m.part("hairBack2", "hairBack", 0, 9.5f, 3.4f, -4.7f, 0, -0.8f, 9.4f, 4.5f, 1.9f, HAIR).rot(4, 0, 0)
                .decor(Face.BACK, 1, 3, 1, 2, 0x000000).decor(Face.BACK, 5, 3, 1, 2, 0x000000).decor(Face.FRONT, 3, 3, 1, 2, 0x000000);
        // ushanka
        m.group("hat", "head", 0, -2.5f, 0);
        m.part("hatCrown", "hat", 0, -2.5f, 0, -5.2f, -4.2f, -4.8f, 10.4f, 4.4f, 9.6f, FUR).grain(0.18f)
                .decor(Face.TOP, 2, 2, 3, 2, FUR_D).decor(Face.TOP, 6, 5, 2, 3, FUR_D).decor(Face.TOP, 4, 7, 2, 1, 0x7A5A4A);
        m.part("hatFront", "hat", 0, -2.5f, -4.9f, -5.5f, -5.2f, -1.0f, 11, 5, 1.5f, FUR_L).grain(0.16f).rot(-8, 0, 0)
                .decor(Face.FRONT, 5, 0, 1, 1, 0x3A3A3A).decor(Face.FRONT, 4, 1, 3, 1, 0x3A3A3A).decor(Face.FRONT, 3, 2, 5, 1, 0x3A3A3A)
                .decor(Face.FRONT, 2, 3, 7, 1, 0x3A3A3A).decor(Face.FRONT, 5, 2, 1, 1, FUR_L).decor(Face.FRONT, 0, 2, 11, 1, 0x8A2A2A)
                .decor(Face.FRONT, 5, 0, 1, 4, 0x8A2A2A).decor(Face.FRONT, 1, 4, 2, 1, BLOOD_D);
        m.part("flapR", "hat", -5.2f, -2.8f, 0.2f, -1.3f, 0, -2.7f, 1.5f, 7, 5.4f, FUR).grain(0.16f).rot(0, 0, 8)
                .decor(Face.RIGHT, 1, 5, 2, 2, FUR_D);
        m.part("flapL", "hat", 5.2f, -2.8f, 0.2f, -0.2f, 0, -2.7f, 1.5f, 7, 5.4f, FUR).grain(0.16f).rot(0, 0, -8)
                .decor(Face.LEFT, 2, 4, 1, 2, BLOOD_D);
        m.part("flapB", "hat", 0, -3.0f, 4.6f, -5.2f, 0, -0.7f, 10.4f, 3.4f, 1.4f, FUR).grain(0.16f).rot(14, 0, 0);
        m.part("hatFluff", "hat", 0, -2.5f, 0, -1.5f, -5.4f, -1.5f, 3, 1.4f, 3, FUR_L).grain(0.2f);
        // ---- arms (with fingerless gloves)
        for (int s = -1; s <= 1; s += 2) {
            String S = s < 0 ? "R" : "L";
            float x = 4.6f * s;
            m.group("arm" + S, "chest", x, 7.6f, 0);
            m.part("sleeve" + S, "arm" + S, x, 7.6f, 0, -1.5f, -1.1f, -1.5f, 3, 5.2f, 3, COAT).grain(0.1f).decor(Face.FRONT, 0, 3, 1, 1, BLOOD_D);
            m.part("fore" + S, "arm" + S, x, 11.6f, 0, -1.45f, 0, -1.45f, 2.9f, 3.2f, 2.9f, COAT).decor(Face.FRONT, 0, 2, 3, 1, COAT_L)
                    .decor(Face.BACK, 0, 2, 3, 1, COAT_L).decor(Face.RIGHT, 0, 2, 3, 1, COAT_L).decor(Face.LEFT, 0, 2, 3, 1, COAT_L);
            m.part("hand" + S, "fore" + S, x, 14.6f, 0, -1.3f, 0, -1.3f, 2.6f, 2.4f, 2.6f, GLOVE)
                    .decor(Face.FRONT, 0, 2, 3, 1, SKIN).decor(Face.LEFT, 0, 2, 3, 1, SKIN).decor(Face.RIGHT, 0, 2, 3, 1, SKIN).decor(Face.FRONT, 1, 0, 1, 1, BLOOD);
        }
        // ================= tool props (grip point = centre of the fist) =================
        float gx = -4.6f, gy = 15.8f, lx = 4.6f;
        // axe (right)
        m.group("axe", "handR", gx, gy, 0);
        m.part("axeHandle", "axe", gx, gy, 0, -0.5f, -0.5f, -11, 1, 1, 13.5f, WOOD).grain(0.15f).decor(Face.TOP, 0, 3, 1, 2, WOOD_D).decor(Face.TOP, 0, 9, 1, 1, BLOOD);
        m.part("axeHead", "axe", gx, gy, 0, -0.6f, -1.6f, -12.4f, 1.2f, 2.6f, 3.0f, IRON);
        m.part("axeBlade", "axe", gx, gy, 0, -0.35f, 0.8f, -13.0f, 0.7f, 3.4f, 4.2f, STEEL)
                .decor(Face.RIGHT, 0, 3, 5, 1, 0xD8DCE0).decor(Face.LEFT, 0, 3, 5, 1, 0xD8DCE0).decor(Face.RIGHT, 1, 1, 2, 2, BLOOD).decor(Face.LEFT, 3, 2, 1, 1, BLOOD);
        // second axe (left hand, enraged throws)
        m.group("axeL", "handL", lx, gy, 0);
        m.part("axeLHandle", "axeL", lx, gy, 0, -0.5f, -0.5f, -11, 1, 1, 13.5f, WOOD).grain(0.15f);
        m.part("axeLHead", "axeL", lx, gy, 0, -0.6f, -1.6f, -12.4f, 1.2f, 2.6f, 3.0f, IRON);
        m.part("axeLBlade", "axeL", lx, gy, 0, -0.35f, 0.8f, -13.0f, 0.7f, 3.4f, 4.2f, STEEL).decor(Face.RIGHT, 0, 3, 5, 1, 0xD8DCE0).decor(Face.LEFT, 0, 3, 5, 1, 0xD8DCE0);
        // sledgehammer
        m.group("hammer", "handR", gx, gy, 0);
        m.part("hamHandle", "hammer", gx, gy, 0, -0.5f, -0.5f, -12, 1, 1, 14.5f, WOOD).grain(0.15f).decor(Face.TOP, 0, 2, 1, 3, 0x2A2A2A);
        m.part("hamHead", "hammer", gx, gy, 0, -1.7f, -3.2f, -14.4f, 3.4f, 6.4f, 3.4f, IRON).grain(0.1f)
                .decor(Face.TOP, 0, 0, 4, 4, 0x6A7078).decor(Face.BOTTOM, 0, 0, 4, 4, 0x6A7078).decor(Face.FRONT, 1, 4, 2, 1, BLOOD);
        // hand saw
        m.group("saw", "handR", gx, gy, 0);
        m.part("sawHandle", "saw", gx, gy, 0, -0.7f, -1.8f, -1.6f, 1.4f, 3.8f, 3.2f, 0x8A3A2A).decor(Face.RIGHT, 1, 1, 1, 2, 0x2A1410).decor(Face.LEFT, 1, 1, 1, 2, 0x2A1410);
        m.part("sawBlade", "saw", gx, gy, 0, -0.25f, -1.6f, -12.8f, 0.5f, 3.8f, 11.2f, STEEL).pattern(Pattern.GRADIENT_V, 0x80868E, 1)
                .decor(Face.RIGHT, 0, 3, 12, 1, 0x50555C).decor(Face.LEFT, 0, 3, 12, 1, 0x50555C)
                .decor(Face.RIGHT, 1, 3, 1, 1, STEEL).decor(Face.RIGHT, 3, 3, 1, 1, STEEL).decor(Face.RIGHT, 5, 3, 1, 1, STEEL).decor(Face.RIGHT, 7, 3, 1, 1, STEEL).decor(Face.RIGHT, 9, 3, 1, 1, STEEL)
                .decor(Face.LEFT, 2, 3, 1, 1, STEEL).decor(Face.LEFT, 4, 3, 1, 1, STEEL).decor(Face.LEFT, 6, 3, 1, 1, STEEL).decor(Face.LEFT, 8, 3, 1, 1, STEEL).decor(Face.LEFT, 10, 3, 1, 1, STEEL)
                .decor(Face.RIGHT, 2, 1, 3, 1, BLOOD).decor(Face.LEFT, 6, 2, 2, 1, BLOOD).decor(Face.RIGHT, 8, 0, 1, 2, BLOOD_D);
        // knives fanned between the fingers (both hands)
        for (int s = -1; s <= 1; s += 2) {
            String S = s < 0 ? "R" : "L", g = "knives" + S;
            float x = s < 0 ? gx : lx;
            m.group(g, "hand" + S, x, gy, 0);
            for (int i = 0; i < 3; i++) {
                String n = "kn" + S + i;
                m.part(n, g, x, gy, 0, -0.45f, -0.45f, -2.2f, 0.9f, 0.9f, 2.6f, 0x1E1E22).rot(0, (i - 1) * 24, 0);
                m.part(n + "b", n, x, gy, 0, -0.2f, -0.8f, -6.6f, 0.4f, 1.6f, 4.5f, STEEL).decor(Face.RIGHT, 0, 0, 2, 1, BLOOD).decor(Face.LEFT, 0, 1, 1, 1, BLOOD_D);
            }
        }
        // crowbar
        m.group("crowbar", "handR", gx, gy, 0);
        m.part("cbShaft", "crowbar", gx, gy, 0, -0.5f, -0.5f, -12, 1, 1, 14.5f, 0x9C2222).grain(0.12f).decor(Face.TOP, 0, 6, 1, 2, 0x5A1212);
        m.part("cbHook", "crowbar", gx, gy, 0, -0.5f, -0.5f, -13.2f, 1, 3.6f, 1.2f, 0x9C2222).decor(Face.FRONT, 0, 2, 1, 2, BLOOD);
        m.part("cbClaw", "crowbar", gx, gy, 0, -0.5f, -1.6f, 2.0f, 1, 1.4f, 0.8f, 0x9C2222);
        // pliers (two hinged halves)
        m.group("pliers", "handR", gx, gy, 0);
        m.part("plGripA", "pliers", gx, gy, 0, -0.85f, -0.45f, -3.2f, 0.75f, 0.9f, 4.4f, 0xB02A2A);
        m.part("plGripB", "pliers", gx, gy, 0, 0.1f, -0.45f, -3.2f, 0.75f, 0.9f, 4.4f, 0xB02A2A);
        m.part("plJawA", "pliers", gx, gy, -3.2f, -0.6f, -0.4f, -4.4f, 0.6f, 0.8f, 4.4f, STEEL).decor(Face.TOP, 0, 0, 1, 1, BLOOD);
        m.part("plJawB", "pliers", gx, gy, -3.2f, 0.0f, -0.4f, -4.4f, 0.6f, 0.8f, 4.4f, STEEL_D);
        m.part("plRivet", "pliers", gx, gy, -3.2f, -0.7f, -0.6f, -0.6f, 1.4f, 1.2f, 1.2f, IRON);
        // power drill (points along the arm: aimed with the arm raised forward)
        m.group("drill", "handR", gx, gy, 0);
        m.part("drBody", "drill", gx, gy, 0, -1.1f, -0.6f, -3.6f, 2.2f, 5.2f, 2.6f, 0xE0B020).decor(Face.RIGHT, 0, 1, 3, 2, 0x1A1A1A).decor(Face.LEFT, 0, 1, 3, 2, 0x1A1A1A)
                .decorGlow(Face.TOP, 1, 1, 1, 1, 0x60FF60);
        m.part("drBattery", "drill", gx, gy, 0, -1.0f, -1.9f, -1.6f, 2, 1.4f, 3.0f, 0x1E1E1E);
        m.part("drChuck", "drill", gx, gy, -2.3f, -0.7f, 4.6f, -0.7f, 1.4f, 1.6f, 1.4f, 0x222222);
        m.part("drBit", "drill", gx, gy + 6.2f, -2.3f, -0.3f, 0, -0.3f, 0.6f, 4.5f, 0.6f, STEEL).decor(Face.FRONT, 0, 1, 1, 1, STEEL_D).decor(Face.FRONT, 0, 3, 1, 1, STEEL_D)
                .decor(Face.LEFT, 0, 2, 1, 1, BLOOD);
        // nail gun
        m.group("nailgun", "handR", gx, gy, 0);
        m.part("ngBody", "nailgun", gx, gy, 0, -1.1f, -1.0f, -3.8f, 2.2f, 6.6f, 2.8f, 0xD8661E).decor(Face.RIGHT, 0, 2, 3, 3, 0x2A2A2A).decor(Face.LEFT, 0, 2, 3, 3, 0x2A2A2A)
                .decorGlow(Face.TOP, 1, 1, 1, 1, 0xFF4030);
        m.part("ngNose", "nailgun", gx, gy, 0, -0.65f, 5.6f, -3.2f, 1.3f, 2.0f, 1.3f, 0x2A2A2A);
        m.part("ngMag", "nailgun", gx, gy, 0, -0.4f, 0.0f, -1.0f, 0.8f, 5.6f, 1.0f, 0x8A8E96).pattern(Pattern.STRIPE_H, 0x5A5E66, 1);
        m.animator(AidenSpec::animate);
        return m;
    }

    // ================================================================== animation
    static float K(float t, float... kv) { return Anim.curve(t, kv); }
    static void R(ModelParts m, String n, float x, float y, float z) { m.addRot(n, x, y, z); }
    static void M(ModelParts m, String n, float x, float y, float z) { m.move(n, x, y, z); }
    static float S(float deg) { return Anim.sin(deg); }
    static void arm(ModelParts m, char side, float x, float y, float z) { float s = side == 'R' ? 1 : -1; m.addRot("arm" + side, x, y * s, z * s); }
    static void fore(ModelParts m, char side, float x, float y, float z) { float s = side == 'R' ? 1 : -1; m.addRot("fore" + side, x, y * s, z * s); }
    static void hand(ModelParts m, char side, float x, float y, float z) { float s = side == 'R' ? 1 : -1; m.addRot("hand" + side, x, y * s, z * s); }
    static void leg(ModelParts m, char side, float thigh, float shin, float foot, float splay) {
        float s = side == 'R' ? 1 : -1;
        m.addRot("leg" + side, thigh, 0, splay * s); m.addRot("shin" + side, shin, 0, 0); m.addRot("boot" + side, foot, 0, 0);
    }
    static void hair(ModelParts m, float back, float sway) {
        R(m, "hairBack", back, 0, sway); R(m, "hairBack2", back * 0.6f, 0, sway * 0.6f);
        R(m, "hairSideR", back * 0.5f, 0, sway * 0.5f); R(m, "hairSideL", back * 0.5f, 0, sway * 0.5f);
        R(m, "flapR", back * 0.3f, 0, Math.max(0, sway) * 0.8f); R(m, "flapL", back * 0.3f, 0, Math.min(0, sway) * 0.8f);
        R(m, "scarfTail", -back * 0.6f, 0, sway); R(m, "coatTail", -back * 0.15f, 0, 0);
    }
    /** "draw" a tool: right hand reaches back to the belt pouch (0..1 weight) */
    static void draw(ModelParts m, char side, float w) {
        arm(m, side, 35 * w, 0, 18 * w); fore(m, side, -30 * w, 0, 0);
        R(m, "chest", 0, (side == 'R' ? 14 : -14) * w, 0);
        R(m, "head", 10 * w, (side == 'R' ? 24 : -24) * w, 0);
    }

    static void animate(ModelParts m, AnimCtx c) {
        float age = c.age, t = c.t;
        boolean act = !c.idle();
        float loco = act ? Math.max(1 - c.seg(0, 4), c.seg(c.dur - 4, c.dur)) : 1;
        float w = c.walk() * loco;
        float ph = c.limbSwing * 0.66f * 57.3f;
        float br = S(age * 5);
        for (String p : PROPS) m.show(p, false);

        // ---------------- creepy idle: slumped, head tilted, slow sway, occasional twitch
        float twitch = (float) Math.pow(Math.max(0, S(age * 3.1f)), 30) * 14;
        M(m, "body", 0, 0.2f * br, 0);
        R(m, "chest", 6 + 1.5f * br, 0, 2 * S(age * 1.6f));
        R(m, "head", -4 + c.headPitch * 0.7f, c.headYaw * 0.8f, 12 + 4 * S(age * 1.3f) + twitch);
        arm(m, 'R', 2 + 2 * br, 0, 4 + 1.5f * S(age * 2));
        arm(m, 'L', 2 + 2 * br, 0, 4 + 1.5f * S(age * 2 + 70));
        fore(m, 'R', -8, 0, 0); fore(m, 'L', -6, 0, 0);
        leg(m, 'R', 0, 0, 0, 2); leg(m, 'L', 0, 0, 0, 3);
        hair(m, 2 * S(age * 2.5f - 40), 2 * S(age * 1.6f - 30));

        // ---------------- walk: small shuffling steps, limp arms, head lolling
        if (w > 0.01f) {
            float sw = S(ph);
            M(m, "body", 0, -Math.abs(S(ph)) * 0.8f * w, 0);
            R(m, "chest", 6 * w, 6 * sw * w, 0);
            R(m, "head", 0, -6 * sw * w, 6 * S(ph * 0.5f) * w);
            leg(m, 'R', -34 * sw * w, Math.max(0, -S(ph + 70)) * 40 * w, 0, 0);
            leg(m, 'L', 34 * sw * w, Math.max(0, S(ph + 70)) * 40 * w, 0, 0);
            arm(m, 'R', 22 * sw * w, 0, 4 * w);
            arm(m, 'L', -22 * sw * w, 0, 4 * w);
            fore(m, 'R', -10 * w - 10 * Math.max(0, sw) * w, 0, 0); fore(m, 'L', -10 * w - 10 * Math.max(0, -sw) * w, 0, 0);
            hair(m, 10 * w + 3 * S(ph * 2) * w, 3 * sw * w);
        }

        if (act) ability(m, c, t);
        if (c.death > 0) death(m, c.death, age);
    }

    static void ability(ModelParts m, AnimCtx c, float t) {
        boolean rage = c.variant == 1;
        switch (c.ability) {
            case "axechop" -> axechop(m, t);
            case "axethrow" -> axethrow(m, t, rage);
            case "hammer" -> hammer(m, t);
            case "hacksaw" -> hacksaw(m, t);
            case "knives" -> knives(m, t);
            case "crowbar" -> crowbar(m, t);
            case "pliers" -> pliers(m, t);
            case "drill" -> drill(m, t, c.age);
            case "nailgun" -> nailgun(m, t);
            case "workshop" -> workshop(m, t, c.age);
            default -> {}
        }
    }

    /** axechop: draws axe, slow heavy two-handed overhead wind-up, chop (t16), axe stuck, yanked free */
    static void axechop(ModelParts m, float t) {
        m.show("axe", t > 2);
        draw(m, 'R', K(t, 0, 0, 2, 1, 4, 0));
        float yank = K(t, 22, 0, 24, 1, 25, 0, 26, 1, 28, 0);
        M(m, "body", 0, K(t, 0, 0, 12, -0.5f, 14, -1, 16, 2.5f, 26, 2, 30, 0.5f, 36, 0), K(t, 0, 0, 16, -1.5f, 36, 0));
        R(m, "chest", K(t, 0, 0, 6, 4, 12, -22, 14, -26, 16, 38, 20, 34, 26, 30, 30, 4, 36, 0) - yank * 12, K(t, 0, 0, 12, 12, 16, -6, 36, 0), 0);
        R(m, "head", K(t, 0, 0, 12, -18, 14, -22, 16, 10, 26, -10, 36, 0), 0, K(t, 0, 0, 14, -10, 16, 6, 36, 0));
        for (char s : new char[] {'R', 'L'}) {
            float x = K(t, 3, 0, 6, -70, 12, -175, 14, -190, 16, -52, 20, -46, 26, -50, 30, -70, 36, 0);
            if (s == 'L' && t < 5) x = K(t, 0, 0, 5, -40);
            arm(m, s, x - yank * 15, 0, K(t, 3, 0, 6, -24, 12, -14, 16, -22, 30, -20, 36, 0));
            fore(m, s, K(t, 3, 0, 6, -20, 12, -30, 14, -40, 16, -8, 30, -20, 36, 0), 0, 0);
        }
        hand(m, 'R', K(t, 3, 0, 12, 10, 14, 0, 16, 70, 26, 70, 30, 20, 36, 0), K(t, 3, 0, 6, 10, 36, 0), 0);
        leg(m, 'R', K(t, 0, 0, 12, 10, 16, -40, 30, -30, 36, 0), K(t, 12, 0, 16, 50, 30, 40, 36, 0), K(t, 12, 0, 16, -12, 36, 0), 0);
        leg(m, 'L', K(t, 0, 0, 12, -10, 16, 20, 30, 10, 36, 0), K(t, 12, 10, 16, 30, 36, 0), 0, 0);
        hair(m, K(t, 0, 0, 12, -10, 14, -14, 16, 26, 20, 10, 36, 0), K(t, 12, 0, 16, 8, 26, 0));
        R(m, "hat", K(t, 14, 0, 16, -8, 19, 4, 22, 0), 0, 0);
    }

    /** axethrow: wind-up behind the head, full-body throw (t12); second axe from the left when enraged (t20); catch (t26) */
    static void axethrow(ModelParts m, float t, boolean rage) {
        m.show("axe", (t > 2 && t < 12.5f) || t > 26);
        m.show("axeL", rage && t > 3 && t < 20.5f);
        draw(m, 'R', K(t, 0, 0, 2, 1, 4, 0));
        R(m, "chest", K(t, 0, 0, 10, -16, 12, 28, 16, 18, 18, -10, 20, 26, 26, 6, 30, 0), K(t, 0, 0, 10, 40, 12, -36, 16, -30, 18, -40, 20, 30, 26, 0, 30, 0), 0);
        R(m, "head", K(t, 0, 0, 10, -10, 12, 10, 30, 0), K(t, 0, 0, 10, -30, 12, 20, 18, 30, 20, -20, 30, 0), 0);
        M(m, "body", 0, K(t, 0, 0, 10, 0.5f, 12, 2, 18, 1, 20, 2, 30, 0), K(t, 0, 0, 12, -1.5f, 20, -1, 30, 0));
        arm(m, 'R', K(t, 3, 0, 6, -100, 10, -200, 12, -40, 14, -20, 20, -10, 26, -80, 28, -60, 30, 0), K(t, 6, 0, 10, 20, 12, -30, 20, 0), K(t, 3, 0, 10, 20, 12, -10, 26, 0));
        fore(m, 'R', K(t, 3, 0, 10, -60, 12, 0, 26, -20, 30, 0), 0, 0);
        hand(m, 'R', K(t, 6, 0, 10, -20, 12, 40, 14, 0), 0, 0);
        arm(m, 'L', rage ? K(t, 0, 0, 6, -40, 12, -60, 16, -110, 18, -200, 20, -40, 22, -20, 30, 0) : K(t, 0, 0, 10, -60, 12, 30, 30, 0), 0, rage ? K(t, 16, 0, 18, 20, 20, -10, 30, 0) : K(t, 0, 0, 10, 30, 12, 10, 30, 0));
        fore(m, 'L', rage ? K(t, 16, 0, 18, -60, 20, 0, 30, 0) : K(t, 0, 0, 10, -30, 30, 0), 0, 0);
        leg(m, 'R', K(t, 0, 0, 10, 20, 12, -36, 18, -10, 20, 16, 30, 0), K(t, 10, 10, 12, 40, 20, 10, 30, 0), 0, 0);
        leg(m, 'L', K(t, 0, 0, 10, -26, 12, 20, 18, -30, 20, 10, 30, 0), K(t, 10, 30, 12, 10, 18, 40, 30, 0), 0, 0);
        hair(m, K(t, 0, 0, 10, -8, 12, 20, 18, -8, 20, 20, 30, 0), K(t, 10, -6, 12, 8, 18, -6, 20, 8, 30, 0));
    }

    /** hammer: hoists sledge with both hands, little hop (t12), ground slam (t17) with shockwave, drags it back up */
    static void hammer(ModelParts m, float t) {
        m.show("hammer", t > 2 && t < 36);
        draw(m, 'R', K(t, 0, 0, 2, 1, 4, 0));
        M(m, "body", 0, K(t, 0, 0, 10, 1.5f, 12, -3, 15, -2, 17, 3.5f, 26, 3, 32, 1, 38, 0), K(t, 0, 0, 12, -1, 17, -2, 38, 0));
        R(m, "chest", K(t, 0, 0, 8, -10, 12, -28, 15, -24, 17, 50, 26, 46, 32, 10, 38, 0), 0, 0);
        R(m, "head", K(t, 0, 0, 12, -20, 17, 10, 19, 24, 26, 0, 38, 0), 0, K(t, 17, 0, 19, -10, 26, -6, 38, 0));
        for (char s : new char[] {'R', 'L'}) {
            arm(m, s, K(t, 3, 0, 6, -90, 10, -160, 12, -190, 15, -195, 17, -40, 19, -30, 26, -32, 32, -60, 38, 0), 0,
                    K(t, 3, 0, 8, -26, 15, -20, 17, -24, 32, -20, 38, 0));
            fore(m, s, K(t, 3, 0, 10, -40, 15, -50, 17, 0, 32, -20, 38, 0), 0, 0);
        }
        hand(m, 'R', K(t, 3, 0, 15, 20, 17, 60, 26, 60, 32, 10, 38, 0), 0, 0);
        leg(m, 'R', K(t, 0, 0, 10, -40, 12, 10, 15, -20, 17, -60, 26, -50, 32, -20, 38, 0), K(t, 0, 0, 10, 60, 12, 10, 15, 40, 17, 80, 26, 70, 38, 0), K(t, 10, -20, 12, 30, 17, -20, 38, 0), 4);
        leg(m, 'L', K(t, 0, 0, 10, -30, 12, 10, 15, -10, 17, -20, 26, -20, 38, 0), K(t, 0, 0, 10, 50, 12, 10, 15, 30, 17, 60, 26, 50, 38, 0), K(t, 10, -20, 12, 30, 17, -40, 38, 0), 4);
        hair(m, K(t, 0, 0, 10, 14, 12, -20, 15, -24, 17, 30, 20, 0, 38, 0), K(t, 17, 0, 19, 10, 24, -4, 30, 0));
        R(m, "hat", K(t, 15, 0, 17, -6, 18, 10, 21, 0), 0, 0);
    }

    /** hacksaw: braces the saw and saws back and forth (strokes peak at 10/16/22/28) */
    static void hacksaw(ModelParts m, float t) {
        m.show("saw", t > 2 && t < 38);
        draw(m, 'R', K(t, 0, 0, 2, 1, 4, 0));
        float on = K(t, 3, 0, 7, 1, 30, 1, 34, 0);
        float st = t < 7 || t > 31 ? 0 : -Anim.cos((t - 7) * 60);   // -1 back .. +1 forward, peaks at 10,16,22,28
        R(m, "chest", 20 * on + 8 * st * on, -16 * on + 12 * st * on, 0);
        R(m, "head", -14 * on, 24 * on - 6 * st * on, 16 * on);
        M(m, "body", 0, 2 * on, -st * on * 0.8f);
        arm(m, 'R', (-60 - 22 * st) * on, -10 * on, -10 * on);
        fore(m, 'R', (-40 + 36 * st) * on, 0, 0);
        hand(m, 'R', (40 - 10 * st) * on, 0, 0);
        arm(m, 'L', -50 * on, -30 * on, -30 * on);
        fore(m, 'L', -40 * on, 0, 0);
        leg(m, 'R', -30 * on, 40 * on, 0, 4 * on);
        leg(m, 'L', 10 * on, 20 * on, 0, 4 * on);
        hair(m, 6 * st * on, 4 * st * on);
    }

    /** knives: fans three knives in each fist, flings the right fan (t10) then the left (t18) */
    static void knives(ModelParts m, float t) {
        m.show("knivesR", t > 3 && t < 10.5f);
        m.show("knivesL", t > 4 && t < 18.5f);
        R(m, "chest", K(t, 0, 0, 4, 10, 8, -10, 10, 20, 14, 0, 16, -10, 18, 22, 24, 6, 28, 0), K(t, 0, 0, 4, 0, 8, 40, 10, -40, 14, -30, 16, -40, 18, 34, 24, 0, 28, 0), 0);
        R(m, "head", K(t, 0, 0, 4, 20, 8, -10, 28, 0), K(t, 0, 0, 8, -30, 10, 20, 16, 30, 18, -20, 28, 0), K(t, 0, 0, 4, 20, 8, 6, 28, 0));
        // pulls both fans from inside the coat (crossed arms), then throws
        arm(m, 'R', K(t, 0, 0, 3, -50, 6, -60, 8, -110, 10, -80, 12, -60, 18, -30, 28, 0), K(t, 0, 0, 3, -50, 6, 40, 8, 60, 10, -40, 14, -20, 28, 0), K(t, 0, 0, 3, -30, 6, 30, 10, 0, 28, 0));
        fore(m, 'R', K(t, 0, 0, 3, -70, 6, -60, 8, -50, 10, 0, 28, 0), 0, 0);
        arm(m, 'L', K(t, 0, 0, 3, -50, 6, -60, 10, -60, 14, -80, 16, -110, 18, -80, 20, -60, 28, 0), K(t, 0, 0, 3, -50, 10, -40, 14, 40, 16, 60, 18, -40, 22, -20, 28, 0), K(t, 0, 0, 3, -30, 14, 30, 18, 0, 28, 0));
        fore(m, 'L', K(t, 0, 0, 3, -70, 14, -60, 16, -50, 18, 0, 28, 0), 0, 0);
        leg(m, 'R', K(t, 0, 0, 8, 10, 10, -30, 16, 0, 18, 10, 28, 0), K(t, 8, 0, 10, 30, 18, 10, 28, 0), 0, 0);
        leg(m, 'L', K(t, 0, 0, 8, -10, 10, 10, 16, 10, 18, -30, 28, 0), K(t, 10, 10, 18, 30, 28, 0), 0, 0);
        hair(m, K(t, 8, 0, 10, 14, 16, 0, 18, 14, 28, 0), K(t, 8, -6, 10, 8, 16, 6, 18, -8, 28, 0));
    }

    /** crowbar: low-slung uppercut (t10), then a backhand hook swing (t19) */
    static void crowbar(ModelParts m, float t) {
        m.show("crowbar", t > 2 && t < 27);
        draw(m, 'R', K(t, 0, 0, 2, 1, 4, 0));
        M(m, "body", 0, K(t, 0, 0, 8, 2.5f, 10, -1.5f, 13, 0, 17, 1.5f, 19, 1, 28, 0), K(t, 0, 0, 10, -1.5f, 19, -1, 28, 0));
        R(m, "chest", K(t, 0, 0, 8, 30, 10, -24, 13, -10, 17, 10, 19, 14, 28, 0), K(t, 0, 0, 8, 20, 10, -10, 15, -50, 17, -55, 19, 40, 23, 30, 28, 0), 0);
        R(m, "head", K(t, 0, 0, 8, -20, 10, 10, 28, 0), K(t, 13, 0, 17, 30, 19, -20, 28, 0), 0);
        arm(m, 'R', K(t, 3, 0, 8, 40, 10, -170, 13, -150, 15, -90, 17, -90, 19, -85, 23, -70, 28, 0),
                K(t, 10, 0, 13, 0, 15, -70, 17, -80, 19, 60, 23, 50, 28, 0), K(t, 3, 0, 8, 10, 10, -10, 28, 0));
        fore(m, 'R', K(t, 3, 0, 8, -10, 10, -10, 15, -60, 17, -50, 19, 0, 28, 0), 0, 0);
        hand(m, 'R', K(t, 3, 0, 8, 60, 10, -20, 15, 0, 28, 0), 0, K(t, 15, 0, 17, 30, 19, -20, 28, 0));
        arm(m, 'L', K(t, 0, 0, 8, -30, 10, 20, 17, -40, 19, 10, 28, 0), 0, K(t, 0, 0, 8, 20, 10, 30, 19, 30, 28, 0));
        leg(m, 'R', K(t, 0, 0, 8, -30, 10, 0, 17, -10, 19, -30, 28, 0), K(t, 0, 0, 8, 60, 10, 0, 19, 40, 28, 0), 0, 0);
        leg(m, 'L', K(t, 0, 0, 8, -20, 10, 10, 19, 10, 28, 0), K(t, 0, 0, 8, 50, 10, 10, 28, 0), 0, 0);
        hair(m, K(t, 0, 0, 8, 10, 10, -20, 13, 10, 19, 0, 28, 0), K(t, 15, -8, 19, 10, 24, 0));
    }

    /** pliers: extends the pliers (t11 snap), yanks the victim in (t12-20), twisting pinch (t22) */
    static void pliers(ModelParts m, float t) {
        m.show("pliers", t > 2 && t < 34);
        draw(m, 'R', K(t, 0, 0, 2, 1, 4, 0));
        float open = K(t, 4, 0, 9, 1, 11, 0, 20, 0, 21, 0.6f, 22, 0, 30, 0, 33, 0.5f);
        R(m, "plJawA", 0, 18 * open, 0); R(m, "plJawB", 0, -18 * open, 0);
        R(m, "plGripA", 0, -8 * open, 0); R(m, "plGripB", 0, 8 * open, 0);
        float yank = K(t, 11, 0, 13, 1, 18, 1, 20, 0);
        M(m, "body", 0, K(t, 0, 0, 9, 1, 11, 1.5f, 20, 2.5f, 22, 1, 36, 0), K(t, 0, 0, 9, -2, 11, -3, 13, 0, 20, 1, 36, 0));
        R(m, "chest", K(t, 0, 0, 9, 18, 11, 24, 13, -10, 18, -20, 20, 0, 22, 14, 30, 6, 36, 0), K(t, 20, 0, 22, -40, 26, -40, 30, 0), 0);
        R(m, "head", K(t, 0, 0, 9, -24, 11, -20, 18, -6, 22, 10, 36, 0), 0, K(t, 0, 0, 9, 26, 20, 30, 24, -10, 36, 0));
        arm(m, 'R', K(t, 3, 0, 9, -100, 11, -92, 13, -60, 18, -30, 20, -80, 22, -90, 26, -90, 30, -60, 36, 0), K(t, 3, 0, 11, 0, 22, -20, 26, -20, 36, 0), K(t, 0, 0, 9, -8, 36, 0));
        fore(m, 'R', K(t, 3, 0, 9, -5, 11, 0, 13, -60, 18, -80, 20, -30, 22, 0, 30, -20, 36, 0), 0, 0);
        hand(m, 'R', K(t, 3, 0, 9, 80, 11, 90, 18, 80, 22, 90, 30, 60, 36, 0), 0, K(t, 20, 0, 22, 90, 26, 90, 30, 0));
        arm(m, 'L', K(t, 0, 0, 11, 20, 13, 40, 18, 40, 22, -40, 36, 0), 0, K(t, 0, 0, 11, 20, 22, 20, 36, 0));
        leg(m, 'R', K(t, 0, 0, 9, -30, 13, 10, 18, 20, 22, -20, 36, 0), K(t, 0, 0, 9, 40, 13, 10, 22, 30, 36, 0), 0, 0);
        leg(m, 'L', K(t, 0, 0, 9, 10, 13, -20, 18, -24, 22, 10, 36, 0), K(t, 0, 0, 9, 20, 13, 40, 22, 20, 36, 0), 0, 0);
        hair(m, 10 * yank - 6 * K(t, 0, 0, 9, 1, 11, 0), 6 * yank);
    }

    /** drill: spins up the drill and stabs it forward four times (10/16/22/28) */
    static void drill(ModelParts m, float t, float age) {
        m.show("drill", t > 2 && t < 34);
        draw(m, 'R', K(t, 0, 0, 2, 1, 4, 0));
        R(m, "drBit", 0, t * 70, 0);
        float on = K(t, 3, 0, 7, 1, 30, 1, 34, 0);
        float th = 0;
        for (int i = 0; i < 4; i++) { float pk = 10 + 6 * i; th += K(t, pk - 3, 0, pk - 1.5f, -0.5f, pk, 1, pk + 2, 0.3f, pk + 3, 0); }
        float buzz = S(age * 160) * on;
        M(m, "body", buzz * 0.15f, 1.5f * on, -2 * th);
        R(m, "chest", 14 * on + 12 * th, -26 * on + 18 * th, buzz);
        R(m, "head", -10 * on, 20 * on, 14 * on + buzz * 2);
        arm(m, 'R', -88 * on, 22 * on - 10 * th, -4 * on);
        fore(m, 'R', (-40 + 40 * th) * on, 0, 0);
        hand(m, 'R', 0, 0, buzz * 2);
        arm(m, 'L', (-70 + 20 * th) * on, -40 * on, -10 * on);
        fore(m, 'L', -50 * on, 0, 0);
        leg(m, 'R', (-26 - 20 * th) * on, (30 + 20 * th) * on, 0, 0);
        leg(m, 'L', (16 + 10 * th) * on, 10 * on, 0, 0);
        hair(m, -8 * th + 4 * buzz, 4 * buzz);
    }

    /** nailgun: raises the nail gun and rattles off a stream of nails (t8..24), each shot kicks back */
    static void nailgun(ModelParts m, float t) {
        m.show("nailgun", t > 2 && t < 30);
        draw(m, 'R', K(t, 0, 0, 2, 1, 4, 0));
        float on = K(t, 3, 0, 7, 1, 25, 1, 30, 0);
        float kick = t >= 8 && t <= 25 ? Math.max(0, Anim.cos(((t - 8) % 2) * 180)) : 0;
        M(m, "body", 0, 0.5f * on, 0.6f * kick);
        R(m, "chest", 6 * on - 4 * kick, -20 * on, 0);
        R(m, "head", -6 * on, 22 * on, 20 * on);
        arm(m, 'R', -90 * on - 8 * kick, 18 * on, 0);
        fore(m, 'R', 0, 0, 0);
        hand(m, 'R', -6 * kick, 0, 0);
        arm(m, 'L', -84 * on, -14 * on, -6 * on);   // steadying hand
        fore(m, 'L', -36 * on, 0, 0);
        leg(m, 'R', -20 * on, 20 * on, 0, 0);
        leg(m, 'L', 14 * on, 6 * on, 0, 0);
        hair(m, 3 * kick, 2 * kick);
    }

    /** workshop (enraged): knives (t8) -> saw cuts (t18/22) -> hammer slam (t34) -> axe chop (t48) -> axe barrage (t56) */
    static void workshop(ModelParts m, float t, float age) {
        // phase 1: knives fan 0-12
        if (t < 12) {
            m.show("knivesR", t > 2 && t < 8.5f);
            float w = K(t, 0, 0, 3, 1, 6, 1, 8, 0, 11, 0);
            float th = K(t, 6, 0, 8, 1, 10, 0.4f, 12, 0);
            arm(m, 'R', -60 * w - 100 * th, 60 * w - 40 * th, 0);
            fore(m, 'R', -60 * w, 0, 0);
            R(m, "chest", -10 * w + 20 * th, 30 * w - 30 * th, 0);
            R(m, "head", 0, -20 * w + 20 * th, 14);
            leg(m, 'R', -30 * th, 30 * th, 0, 0);
        }
        // phase 2: saw 12-26
        else if (t < 26) {
            m.show("saw", true);
            float on = K(t, 12, 0, 14, 1, 24, 1, 26, 0);
            float st = K(t, 14, -1, 18, 1, 20, -1, 22, 1, 24, -1);
            R(m, "chest", 18 * on + 8 * st * on, -18 * on + 14 * st * on, 0);
            R(m, "head", -10 * on, 20 * on, 18 * on);
            arm(m, 'R', (-60 - 24 * st) * on, -10 * on, -10 * on);
            fore(m, 'R', (-40 + 36 * st) * on, 0, 0);
            hand(m, 'R', 40 * on, 0, 0);
            arm(m, 'L', -50 * on, -30 * on, -30 * on);
            leg(m, 'R', -30 * on, 40 * on, 0, 4 * on);
            M(m, "body", 0, 2 * on, -st * on);
        }
        // phase 3: hammer 26-40
        else if (t < 40) {
            m.show("hammer", true);
            float u = t - 26;
            M(m, "body", 0, K(u, 0, 0, 5, -2.5f, 8, 3.5f, 14, 0), 0);
            R(m, "chest", K(u, 0, 0, 5, -26, 8, 50, 12, 40, 14, 0), 0, 0);
            R(m, "head", K(u, 0, 0, 5, -20, 8, 20, 14, 0), 0, 0);
            for (char s : new char[] {'R', 'L'}) {
                arm(m, s, K(u, 0, 0, 5, -190, 8, -40, 12, -35, 14, -20), 0, -22 * K(u, 0, 0, 2, 1, 12, 1, 14, 0));
                fore(m, s, K(u, 0, 0, 5, -50, 8, 0, 14, 0), 0, 0);
                leg(m, s, K(u, 0, 0, 5, 10, 8, -50, 12, -40, 14, 0), K(u, 0, 0, 5, 10, 8, 70, 12, 60, 14, 0), 0, 4);
            }
            hand(m, 'R', K(u, 5, 20, 8, 60, 14, 0), 0, 0);
        }
        // phase 4: axe chop 40-52, phase 5: spinning axe barrage 52-64
        else if (t < 52) {
            m.show("axe", true);
            float u = t - 40;
            R(m, "chest", K(u, 0, 0, 6, -24, 8, 40, 12, 10), 0, 0);
            R(m, "head", K(u, 0, 0, 6, -20, 8, 10, 12, 0), 0, 0);
            M(m, "body", 0, K(u, 0, 0, 6, -1, 8, 2.5f, 12, 1), 0);
            for (char s : new char[] {'R', 'L'}) {
                arm(m, s, K(u, 0, -40, 6, -190, 8, -50, 12, -60), 0, -20);
                fore(m, s, K(u, 0, -20, 6, -40, 8, -5, 12, -10), 0, 0);
            }
            hand(m, 'R', K(u, 0, 0, 6, 10, 8, 70, 12, 40), 0, 0);
            leg(m, 'R', K(u, 0, 0, 8, -40, 12, -20), K(u, 0, 0, 8, 50, 12, 20), 0, 0);
        } else {
            float u = t - 52;
            m.show("axe", u < 4);
            m.show("axeL", u < 4);
            float spin = Anim.curve(u, 0, 0, 6, -360);
            R(m, "body", 0, spin, 0);
            M(m, "body", 0, K(u, 0, 1, 3, -2, 6, 1, 12, 0), 0);
            for (char s : new char[] {'R', 'L'}) {
                arm(m, s, K(u, 0, -60, 4, -90, 8, -40, 12, 0), 0, K(u, 0, 10, 4, 80, 8, 30, 12, 0));
                leg(m, s, K(u, 0, -20, 6, -10, 12, 0), K(u, 0, 30, 12, 0), 0, 6);
            }
            R(m, "head", 0, 0, 20 + 10 * S(age * 40) * K(u, 6, 1, 12, 0));
        }
        hair(m, 8 * S(t * 24), 6 * S(t * 18));
    }

    // ================================================================== death
    static void death(ModelParts m, float d, float age) {
        float shiver = S(age * 110) * K(d, 0, 0, 0.15f, 1, 0.45f, 0);
        // drops to the knees, then slumps over sideways; the ushanka tumbles off
        M(m, "body", 0, K(d, 0, 0, 0.35f, 4.5f, 1, 9.5f), K(d, 0, 0, 1, 1));
        R(m, "body", K(d, 0, 0, 0.35f, 8, 0.7f, 20, 1, 12), 0, K(d, 0.35f, 0, 0.75f, -60, 1, -86));
        R(m, "chest", K(d, 0, 0, 0.35f, 26, 1, 10), 0, shiver * 3);
        R(m, "head", K(d, 0, 0, 0.35f, 30, 1, 10), 0, K(d, 0, 0, 0.35f, 20, 1, 30));
        leg(m, 'R', K(d, 0, 0, 0.35f, -80, 1, -60), K(d, 0, 0, 0.35f, 150, 1, 120), K(d, 0, 0, 0.35f, 30, 1, 20), 0);
        leg(m, 'L', K(d, 0, 0, 0.35f, -80, 1, -40), K(d, 0, 0, 0.35f, 150, 1, 100), K(d, 0, 0, 0.35f, 30, 1, 20), 0);
        arm(m, 'R', K(d, 0, 0, 0.35f, -10, 1, -40), 0, K(d, 0.35f, 0, 1, 60));
        arm(m, 'L', K(d, 0, 0, 0.35f, -10, 1, 20), 0, K(d, 0, 0, 1, 10));
        hair(m, K(d, 0, 0, 0.35f, -20, 1, 0), K(d, 0.35f, 0, 1, 40));
        M(m, "hat", K(d, 0.3f, 0, 0.7f, -3, 1, -6), K(d, 0.3f, 0, 0.5f, -5, 0.8f, -2, 1, -1), K(d, 0.3f, 0, 1, -7));
        R(m, "hat", K(d, 0.3f, 0, 1, -50), 0, K(d, 0.3f, 0, 1, 70));
    }
}
