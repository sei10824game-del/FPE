package com.fpe.client.spec;

import static com.fpe.client.model.Anim.curve;

import com.fpe.client.model.Anim;
import com.fpe.client.model.AnimCtx;
import com.fpe.client.model.ModelParts;
import com.fpe.client.model.ModelSpec;
import com.fpe.client.model.ModelSpec.Face;
import com.fpe.client.model.ModelSpec.Pattern;

/**
 * Miss Thavel "the bomb": long spiky dark-purple hair, striped knit hat with a square-spiral antenna,
 * white face with an orange visor and a huge shark grin, cropped orange jacket + shell bandolier,
 * bandaged midriff, hazard pouch, long tan skirt, black gloves (grenade in the left hand), tall boots.
 */
public final class MissThavelSpec {
    private MissThavelSpec() {}

    // palette
    static final int ORANGE = 0xE8862C, ORANGE_D = 0xC0641C, ORANGE_L = 0xF4A24A, CREAM = 0xF2DDB2;
    static final int SKIN = 0xF3F0E8, HAIR = 0x3B2452, HAIR_D = 0x2A1940, HAIR_L = 0x4E3270;
    static final int TAN = 0xD9A064, TAN_D = 0xB57A43, BLACK = 0x17151D, GLOVE = 0x1D1A24, BROWN = 0x8A4A2A, BROWN_D = 0x5E301A;
    static final int BRASS = 0xD9A447, HAZ = 0xF2C230, SOCK_L = 0xD8C49A;

    public static final ModelSpec SPEC = build();

    private static ModelSpec build() {
        ModelSpec m = new ModelSpec("miss_thavel");
        m.group("root", null, 0, 24, 0);
        m.group("spin", "root", 0, 12, 0);

        // ---------------------------------------------------------------- legs (striped socks + tall pointed boots)
        for (int s = -1; s <= 1; s += 2) {
            String k = s < 0 ? "R" : "L";
            float x = 2 * s;
            m.part("leg" + k, "spin", x, 12, 0, -1.5f, 0, -1.5f, 3, 7, 3, SOCK_L).pattern(Pattern.STRIPE_H, BLACK, 1);
            m.part("boot" + k, "leg" + k, x, 19, 0, -1.75f, 0, -1.75f, 3.5f, 5, 3.5f, BLACK)
                    .decor(Face.FRONT, 1, 1, 2, 1, 0x2E2A38).decor(Face.LEFT, 0, 4, 4, 1, 0x0C0B10).decor(Face.RIGHT, 0, 4, 4, 1, 0x0C0B10);
            m.part("bootCuff" + k, "boot" + k, x, 19, 0, -2.1f, -0.6f, -2.1f, 4.2f, 1.6f, 4.2f, 0x24212E);
            m.part("toe" + k, "boot" + k, x, 19, 0, -1.4f, 3.4f, -3.3f, 2.8f, 1.6f, 1.6f, BLACK);
            m.part("heel" + k, "boot" + k, x, 19, 0, -1f, 4.2f, 1.6f, 2, 0.8f, 1, 0x0C0B10);
        }

        // ---------------------------------------------------------------- hips, skirt
        m.group("hips", "spin", 0, 12, 0);
        m.part("skirtTop", "hips", 0, 10.5f, 0, -4.4f, 0, -2.6f, 8.8f, 3, 5.2f, TAN)
                .decor(Face.FRONT, 5, 0, 1, 3, TAN_D);
        m.part("skirtF", "hips", 0, 13, -2.4f, -4.6f, 0, -0.7f, 9.2f, 6.2f, 1, TAN).pattern(Pattern.GRADIENT_V, TAN_D, 1).rot(-9, 0, 0)
                .decor(Face.FRONT, 5, 0, 1, 7, 0xA86F3A).decor(Face.FRONT, 0, 5, 10, 2, 0xA86F3A);
        m.part("skirtB", "hips", 0, 13, 2.4f, -4.6f, 0, -0.3f, 9.2f, 6.4f, 1, TAN).pattern(Pattern.GRADIENT_V, TAN_D, 1).rot(11, 0, 0)
                .decor(Face.BACK, 0, 5, 10, 2, 0xA86F3A);
        m.part("skirtR", "hips", -4.3f, 13, 0, -0.9f, 0, -2.6f, 1, 6, 5.2f, TAN).pattern(Pattern.GRADIENT_V, TAN_D, 1).rot(0, 0, 9);
        m.part("skirtL", "hips", 4.3f, 13, 0, -0.1f, 0, -2.6f, 1, 6, 5.2f, TAN).pattern(Pattern.GRADIENT_V, TAN_D, 1).rot(0, 0, -9);

        // ---------------------------------------------------------------- torso: cropped jacket, bandage, bandolier, pouch
        m.part("torso", "hips", 0, 12, 0, -4, -10, -2, 8, 10, 4, ORANGE)
                .decor(Face.FRONT, 4, 0, 1, 5, ORANGE_D)                     // jacket opening
                .decor(Face.FRONT, 2, 1, 2, 1, BROWN_D).decor(Face.FRONT, 5, 1, 2, 1, BROWN_D) // frog toggles
                .decor(Face.FRONT, 2, 3, 2, 1, BROWN_D).decor(Face.FRONT, 5, 3, 2, 1, BROWN_D)
                .decor(Face.BACK, 3, 1, 2, 3, ORANGE_D);
        m.part("jacketHem", "torso", 0, 12, 0, -4.3f, -6.4f, -2.3f, 8.6f, 1.3f, 4.6f, ORANGE_D);
        m.part("bandage", "torso", 0, 12, 0, -4, -5.4f, -2, 8, 4, 4, 0xEFEBE2).inflate(0.15f)
                .pattern(Pattern.STRIPE_H, 0xCFC8B8, 1).decor(Face.FRONT, 6, 1, 1, 2, 0xB9B0A0).decor(Face.FRONT, 2, 2, 2, 1, 0xFFFFFF);
        m.part("belt", "torso", 0, 12, 0, -4.3f, -1.6f, -2.3f, 8.6f, 0.9f, 4.6f, BROWN_D);
        m.part("collar", "torso", 0, 12, 0, -3.6f, -11.6f, -2.6f, 7.2f, 2.6f, 5.2f, ORANGE)
                .decor(Face.FRONT, 3, 0, 1, 3, ORANGE_D).decor(Face.TOP, 0, 0, 8, 1, ORANGE_L);
        // shell bandolier: left shoulder -> right hip, front and back
        m.part("band", "torso", 0, 6.5f, -2.25f, -1.1f, -7.5f, -0.5f, 2.2f, 15, 0.8f, BROWN_D).rot(0, 0, 40);
        m.part("shells", "band", 0, 6.5f, -2.25f, -0.7f, -6.5f, -1.1f, 1.4f, 13, 0.8f, BRASS).pattern(Pattern.STRIPE_H, 0xA0381E, 1);
        m.part("bandB", "torso", 0, 6.5f, 2.25f, -1.1f, -7.5f, -0.3f, 2.2f, 15, 0.8f, BROWN_D).rot(0, 0, -40);
        m.part("shellsB", "bandB", 0, 6.5f, 2.25f, -0.7f, -6.5f, 0.3f, 1.4f, 13, 0.8f, BRASS).pattern(Pattern.STRIPE_H, 0xA0381E, 1);
        // hazard pouch on the right hip
        m.part("pouch", "torso", -3.4f, 10.4f, -2.2f, -2.5f, -0.4f, -1.6f, 5, 4, 2.2f, BROWN)
                .decor(Face.FRONT, 2, 0, 1, 1, HAZ).decor(Face.FRONT, 1, 1, 3, 2, HAZ).decor(Face.FRONT, 0, 3, 5, 1, HAZ)
                .decor(Face.FRONT, 2, 1, 1, 1, BLACK).decor(Face.FRONT, 2, 3, 1, 1, BLACK);
        m.part("pouchFlap", "pouch", -3.4f, 10.4f, -2.2f, -2.7f, -1.2f, -1.8f, 5.4f, 1.2f, 2.6f, BROWN_D);

        // ---------------------------------------------------------------- head
        m.group("neck", "torso", 0, 2, 0);
        m.part("head", "neck", 0, 2, 0, -4, -8, -4, 8, 8, 8, SKIN)
                .decor(Face.FRONT, 0, 3, 1, 1, BLACK).decor(Face.FRONT, 7, 3, 1, 1, BLACK)
                .decor(Face.FRONT, 0, 4, 8, 3, 0x1A0F16)
                .decor(Face.FRONT, 0, 4, 1, 1, 0xFFFFFF).decor(Face.FRONT, 2, 4, 1, 1, 0xFFFFFF).decor(Face.FRONT, 4, 4, 1, 1, 0xFFFFFF).decor(Face.FRONT, 6, 4, 1, 1, 0xFFFFFF)
                .decor(Face.FRONT, 1, 6, 1, 1, 0xFFFFFF).decor(Face.FRONT, 3, 6, 1, 1, 0xFFFFFF).decor(Face.FRONT, 5, 6, 1, 1, 0xFFFFFF).decor(Face.FRONT, 7, 6, 1, 1, 0xFFFFFF)
                .decor(Face.FRONT, 1, 5, 6, 1, 0x7A1F2A)
                .decor(Face.FRONT, 6, 2, 1, 1, 0x9A93A0)  // cheek mole
                .decor(Face.LEFT, 0, 4, 2, 1, 0x1A0F16).decor(Face.RIGHT, 6, 4, 2, 1, 0x1A0F16);
        m.part("visor", "head", -2, -2.6f, -4, -1.8f, -1.2f, -0.7f, 3.6f, 2.4f, 0.9f, 0xFF8A1E).glow()
                .decorGlow(Face.FRONT, 1, 0, 2, 1, 0xFFE2A8).decorGlow(Face.FRONT, 0, 2, 4, 1, 0xC85A10);
        m.part("visorStrap", "head", 0, -2.6f, 0, -4.2f, -0.6f, -4.2f, 8.4f, 0.8f, 8.4f, 0x2A2030);
        // hair
        m.part("hairCap", "head", 0, 2, 0, -4.4f, -8.4f, -4.4f, 8.8f, 3.2f, 8.8f, HAIR);
        m.part("fringe", "head", 0, -4.8f, -4.3f, -4.4f, -0.6f, -0.6f, 8.8f, 1.8f, 1, HAIR)
                .decor(Face.FRONT, 1, 1, 1, 1, HAIR_D).decor(Face.FRONT, 4, 1, 1, 1, HAIR_D);
        m.part("bangL", "head", 1, -5, -4.4f, -0.5f, 0, -0.6f, 4.2f, 5.2f, 1.1f, HAIR).rot(0, 0, -12)
                .pattern(Pattern.GRADIENT_V, HAIR_L, 1).decor(Face.FRONT, 0, 4, 1, 1, HAIR_D);
        m.part("hairSideR", "head", -4.2f, -4, -1, -0.9f, 0, -3, 1.8f, 9, 5.5f, HAIR).rot(0, 0, 6).pattern(Pattern.GRADIENT_V, HAIR_D, 1);
        m.part("hairSideL", "head", 4.2f, -4, -1, -0.9f, 0, -3, 1.8f, 10, 5.5f, HAIR).rot(0, 0, -6).pattern(Pattern.GRADIENT_V, HAIR_D, 1);
        m.part("hairB1", "head", 0, -5, 3.6f, -5, 0, -1.2f, 10, 11, 3.2f, HAIR).pattern(Pattern.GRADIENT_V, HAIR_D, 1)
                .decor(Face.BACK, 2, 0, 1, 11, HAIR_L).decor(Face.BACK, 7, 2, 1, 9, HAIR_D);
        m.part("hairB2", "hairB1", 0, 6, 4, -6, 0, -1.2f, 12, 8, 2.8f, HAIR).pattern(Pattern.GRADIENT_V, HAIR_D, 1)
                .decor(Face.BACK, 3, 0, 1, 8, HAIR_L).decor(Face.BACK, 9, 0, 1, 8, HAIR_L);
        m.part("hairB3", "hairB2", 0, 14, 4.4f, -6.5f, 0, -1, 13, 5, 2.2f, HAIR_D).pattern(Pattern.GRADIENT_V, 0x21143A, 1);
        // jagged spiky tips
        float[][] tips = { {-5.5f, 18, 18}, {-2.5f, 18, 6}, {0.5f, 18, -4}, {3.5f, 18, -14}, {6, 17, -30}, {-7, 16, 34} };
        for (int i = 0; i < tips.length; i++)
            m.part("hairTip" + i, "hairB3", tips[i][0], 19, 4.4f, -1.2f, 0, -0.8f, 2.4f, 4.5f - (i % 2), 1.6f, HAIR_D).rot(0, 0, tips[i][2]);
        m.part("hairSpikeR", "hairB2", -5.5f, 8, 4, -4, -1, -0.8f, 4.5f, 2, 1.6f, HAIR).rot(0, 0, -28);
        m.part("hairSpikeR2", "hairB1", -5, 3, 3.6f, -4, -1, -0.8f, 4.5f, 2.2f, 1.8f, HAIR).rot(0, 0, -40);
        m.part("hairSpikeL2", "hairB1", 5, 5, 3.6f, -0.5f, -1, -0.8f, 4.5f, 2.2f, 1.8f, HAIR).rot(0, 0, 44);
        m.part("hairSpikeR3", "hairB3", -6, 16, 4.4f, -3.5f, -1, -0.8f, 4, 1.8f, 1.6f, HAIR_D).rot(0, 0, -50);
        m.part("hairSpikeL", "hairB2", 5.5f, 10, 4, -0.5f, -1, -0.8f, 4.5f, 2, 1.6f, HAIR).rot(0, 0, 32);

        // ---------------------------------------------------------------- knit hat + spiral antenna + side radio
        m.group("hat", "head", 0, -6, 0).rot(0, 0, -5);
        m.part("hatBrim", "hat", 0, -6, 0, -4.8f, -1.4f, -4.8f, 9.6f, 2.2f, 9.6f, ORANGE).pattern(Pattern.STRIPE_V, ORANGE_D, 1);
        m.part("hatBody", "hat", 0, -6, 0, -4.4f, -5.6f, -4.4f, 8.8f, 4.3f, 8.8f, CREAM).pattern(Pattern.STRIPE_H, ORANGE, 1);
        m.part("hatTop", "hat", 0, -6, 0, -3.6f, -6.6f, -3.6f, 7.2f, 1.1f, 7.2f, ORANGE).pattern(Pattern.STRIPE_V, ORANGE_D, 1);
        m.part("radio", "hat", -4.6f, -9, 0, -2, -2.5f, -1.5f, 2.2f, 4, 3, ORANGE_D)
                .decor(Face.RIGHT, 1, 1, 1, 2, 0x3A2A2A).decor(Face.FRONT, 0, 0, 2, 1, ORANGE_L);
        m.part("radioRod", "radio", -5.6f, -11.5f, 0, -0.3f, -5, -0.3f, 0.6f, 5, 0.6f, 0x2A2030);
        m.part("radioTip", "radioRod", -5.6f, -16.5f, 0, -0.5f, -0.9f, -0.5f, 1, 1, 1, 0xFF4A2A).glow();
        m.part("stalk", "hat", 1, -12.6f, 0, -0.4f, -3, -0.4f, 0.8f, 3, 0.8f, 0x2A2030);
        m.group("spiral", "stalk", 1, -15.4f, 0);
        int SP = 0xEFE8DA;
        m.part("sp1", "spiral", 1, -15.4f, 0, -0.4f, -0.4f, -0.35f, 5, 0.8f, 0.7f, SP);
        m.part("sp2", "spiral", 1, -15.4f, 0, 3.8f, -5, -0.35f, 0.8f, 5.4f, 0.7f, SP);
        m.part("sp3", "spiral", 1, -15.4f, 0, -1.2f, -5, -0.35f, 5.4f, 0.8f, 0.7f, SP);
        m.part("sp4", "spiral", 1, -15.4f, 0, -1.2f, -4.6f, -0.35f, 0.8f, 3.8f, 0.7f, SP);
        m.part("sp5", "spiral", 1, -15.4f, 0, -1.2f, -1.6f, -0.35f, 3.6f, 0.8f, 0.7f, SP);
        m.part("sp6", "spiral", 1, -15.4f, 0, 1.6f, -3.2f, -0.35f, 0.8f, 2.2f, 0.7f, SP);
        m.part("spark", "spiral", 1, -15.4f, 0, 0.4f, -3.4f, -0.8f, 1.6f, 1.6f, 1.6f, 0xFFE070).glow();

        // ---------------------------------------------------------------- arms (shoulder / elbow / hand)
        for (int s = -1; s <= 1; s += 2) {
            String k = s < 0 ? "R" : "L";
            float x = 5 * s;
            m.part("arm" + k, "torso", x, 3, 0, -1.5f, -1, -1.5f, 3, 6, 3, ORANGE).decor(Face.TOP, 0, 0, 3, 3, ORANGE_L);
            m.part("fore" + k, "arm" + k, x, 8, 0, -1.4f, 0, -1.4f, 2.8f, 2.4f, 2.8f, ORANGE);
            m.part("cuff" + k, "fore" + k, x, 8, 0, -1.9f, 1.9f, -1.9f, 3.8f, 2, 3.8f, ORANGE_D).decor(Face.FRONT, 1, 1, 2, 1, BROWN_D);
            m.part("hand" + k, "fore" + k, x, 11.5f, 0, -1.3f, 0, -1.3f, 2.6f, 2.7f, 2.6f, GLOVE);
        }
        // grenade in the left fist
        m.group("grenade", "handL", 5, 13.4f, -1.4f);
        m.part("grenBody", "grenade", 5, 13.4f, -1.4f, -1.2f, -1.2f, -1.2f, 2.4f, 2.6f, 2.4f, 0x6A5530).pattern(Pattern.CHECK, 0x40331C, 1);
        m.part("grenCap", "grenade", 5, 13.4f, -1.4f, -0.6f, -2, -0.6f, 1.2f, 0.9f, 1.2f, 0x8C8C94);
        m.part("grenPin", "grenade", 5, 13.4f, -1.4f, 0.6f, -2.3f, -0.2f, 1, 1, 0.4f, 0xC8C8D0);
        // round fuse bomb (right hand) for bandolier/rain
        m.group("bombR", "handR", -5, 14, -0.6f);
        m.part("bombBall", "bombR", -5, 14, -0.6f, -1.4f, -1, -1.4f, 2.8f, 2.8f, 2.8f, 0x22202A).decor(Face.FRONT, 0, 0, 1, 1, 0x5A5868);
        m.part("bombFuse", "bombR", -5, 14, -0.6f, -0.3f, -2, -0.3f, 0.6f, 1.1f, 0.6f, 0xC8B080);
        m.part("bombSpark", "bombR", -5, 14, -0.6f, -0.6f, -2.8f, -0.6f, 1.2f, 1.2f, 1.2f, 0xFFD040).glow();
        // detonator (right hand) for carpet bombing
        m.group("detonator", "handR", -5, 14, -0.6f);
        m.part("detBox", "detonator", -5, 14, -0.6f, -1, -1.5f, -1.2f, 2, 3, 2.2f, 0x3A3A44).decor(Face.FRONT, 0, 2, 2, 1, HAZ);
        m.part("detBtn", "detonator", -5, 14, -0.6f, -0.5f, -2.1f, -0.5f, 1, 0.7f, 1, 0xFF2020).glow();
        m.part("detAnt", "detonator", -5, 14, -0.6f, 0.4f, -4.5f, 0.3f, 0.4f, 3, 0.4f, 0x1A1A1A);
        // shoulder rocket launcher (pulled out of the hair)
        m.group("launcher", "torso", -6.3f, -1.4f, 0);
        m.part("tube", "launcher", -6.3f, -1.4f, 0, -1.6f, -1.6f, -6, 3.4f, 3.4f, 13, 0xB8402A).pattern(Pattern.STRIPE_H, 0x9A3220, 3)
                .decor(Face.LEFT, 2, 0, 1, 4, HAZ).decor(Face.RIGHT, 9, 0, 1, 4, HAZ);
        m.part("tubeFront", "launcher", -6.3f, -1.4f, 0, -2, -2, -7.4f, 4, 4, 1.8f, HAZ).pattern(Pattern.DIAG, BLACK, 1);
        m.part("tubeBack", "launcher", -6.3f, -1.4f, 0, -1.9f, -1.9f, 6.6f, 3.8f, 3.8f, 1.4f, 0x3A3F24);
        m.part("rocketTip", "launcher", -6.3f, -1.4f, 0, -1.1f, -1.1f, -9, 2.2f, 2.2f, 1.8f, 0xD02A20).decor(Face.FRONT, 0, 0, 1, 1, 0xFF7060);
        m.part("tubeGrip", "launcher", -6.3f, -1.4f, 0, -0.5f, 1.5f, -3, 1, 2.2f, 1.2f, BLACK);
        m.part("tubeSight", "launcher", -6.3f, -1.4f, 0, 1.5f, -2.6f, -4, 1, 1.4f, 1.2f, BLACK);
        m.part("backBlast", "launcher", -6.3f, -1.4f, 0, -1.4f, -1.4f, 8, 2.8f, 2.8f, 3.5f, 0xFFB040).glow();
        // free-flying kicked grenade (root space)
        m.part("kickBomb", "root", 0, 0, 0, -1.2f, -1.2f, -1.2f, 2.4f, 2.6f, 2.4f, 0x6A5530).pattern(Pattern.CHECK, 0x40331C, 1);

        m.animator(MissThavelSpec::animate);
        return m;
    }

    // ==================================================================== animation
    /** pose accumulator (degrees / pixels) */
    private static final class P {
        float rootX, rootY, rootZ, rootDY, spinX, spinY, spinZ, spinDY, spinDZ;
        float bodyX, bodyY, bodyZ, headX, headY, headZ;
        float aRx, aRy, aRz, fRx, hRx, aLx, aLy, aLz, fLx, hLx;
        float lRx, lRz, bRx, lLx, lLz, bLx;
        float hairX, hairZ, crouch, kneel;
    }

    private static void animate(ModelParts m, AnimCtx c) {
        P p = new P();
        float w = c.walk();
        float sw = Anim.sinr(c.limbSwing * 0.62f);
        float breathe = Anim.sin(c.age * 7f);

        // ---------------- idle: smug lopsided stance, toying with the grenade
        p.bodyX = 2 + breathe * 1.2f;
        p.bodyZ = -2;
        p.headX = c.headPitch * 0.8f - 4;
        p.headY = c.headYaw;
        p.headZ = 5 + Anim.sin(c.age * 3.3f) * 2;
        p.aRx = -4 + breathe * 2; p.aRz = 7; p.fRx = -12;
        p.aLx = -24 + Anim.sin(c.age * 9) * 4; p.aLz = -10; p.fLx = -48 + Anim.sin(c.age * 9) * 8; p.hLx = -10; // weighs the grenade
        p.lRz = 3; p.lLz = -4; p.lLx = -4;
        p.hairX = 4 + breathe * 2; p.hairZ = Anim.sin(c.age * 2.6f) * 3;

        // ---------------- walk: long strutting strides, arms pumping, grenade tossed in rhythm
        if (w > 0.01f) {
            p.lRx += sw * 42 * w; p.lLx += -sw * 42 * w;
            p.bRx += Math.max(0, -Anim.sinr(c.limbSwing * 0.62f + 1.2f)) * 45 * w;
            p.bLx += Math.max(0, Anim.sinr(c.limbSwing * 0.62f + 1.2f)) * 45 * w;
            p.aRx += -sw * 38 * w; p.fRx += -20 * w;
            p.aLx += sw * 30 * w;
            p.bodyX += 7 * w; p.bodyY += sw * 9 * w; p.bodyZ += sw * 2 * w;
            p.spinDY += -Math.abs(Anim.sinr(c.limbSwing * 0.62f)) * 1.1f * w;
            p.hairX += 20 * w + Math.abs(sw) * 6 * w;
            p.headZ += -sw * 4 * w;
        }

        // ---------------- abilities
        float t = c.t;
        m.show("bombR", false); m.show("detonator", false); m.show("launcher", false); m.show("kickBomb", false);
        m.show("spark", false); m.show("backBlast", false);
        boolean grenade = true;

        if (c.is("grenade_lob")) {
            // pin to the teeth -> pull -> big overhand wind-up -> whip -> follow-through
            p.aLx = curve(t, 0, -24, 5, -55, 7, -50, 11, -175, 15, -185, 17, -35, 21, -20, 30, -24);
            p.aLz = curve(t, 0, -10, 5, 30, 7, 24, 11, -15, 16, -10, 30, -10);
            p.aLy = curve(t, 0, 0, 5, -25, 8, 0);
            p.fLx = curve(t, 0, -48, 5, -110, 7, -95, 11, -80, 15, -95, 17, -5, 22, -20, 30, -48);
            p.headY = curve(t, 0, c.headYaw, 5, 18, 7, -22, 10, c.headYaw);
            p.headZ = curve(t, 5, 5, 7, 18, 10, 4);
            p.headX = curve(t, 4, p.headX, 6, 14, 9, p.headX - 6, 16, p.headX + 8, 22, p.headX);
            p.bodyY = curve(t, 6, 0, 13, -32, 16, 30, 21, 12, 30, 0);
            p.bodyX = curve(t, 6, 2, 13, -10, 16, 12, 21, 6, 30, 2);
            p.bodyZ = curve(t, 8, -2, 13, 8, 17, -6, 30, -2);
            p.aRx = curve(t, 8, -4, 13, -80, 17, -30, 22, 10, 30, -4);
            p.aRy = curve(t, 8, 0, 13, 20, 17, 0);
            p.lLx = curve(t, 9, -4, 14, 12, 17, -36, 24, -18, 30, -4);
            p.lRx = curve(t, 9, 0, 14, -12, 17, 28, 24, 10, 30, 0);
            p.bLx = curve(t, 14, 0, 17, 20, 24, 8, 30, 0);
            p.crouch = curve(t, 10, 0, 14, 1.2f, 17, 1.8f, 24, 0.4f, 30, 0);
            p.hairX += curve(t, 10, 0, 14, -15, 18, 35, 26, 0);
            grenade = t < 16 || t > 25;
            if (t >= 6.5f) m.hide("grenPin");
        } else if (c.is("bandolier_burst")) {
            // grab the bandolier across the chest, crouch, rip it open -> fan of bomblets, maniac laugh
            float rip = c.seg(11, 14);
            p.crouch = curve(t, 0, 0, 9, 3.2f, 12, 3.6f, 15, 0, 20, -0.8f, 26, 0);
            p.bodyX = curve(t, 0, 2, 9, 12, 12, 14, 15, -16, 22, -22, 36, 2);
            p.headX = curve(t, 0, p.headX, 9, 20, 13, 20, 16, -30, 22, -36, 28, -20, 36, p.headX);
            p.headZ = curve(t, 15, 0, 18, 10, 21, -10, 24, 10, 27, -6, 36, 5);
            p.aRx = curve(t, 0, -4, 8, -70, 12, -76, 15, -120, 26, -130, 36, -4);
            p.aRy = curve(t, 0, 0, 8, 40, 12, 46, 15, -10, 36, 0);
            p.aRz = curve(t, 0, 7, 8, -20, 12, -24, 15, 70, 26, 75, 36, 7);
            p.fRx = curve(t, 0, -12, 8, -70, 12, -70, 15, 0, 36, -12);
            p.aLx = curve(t, 0, -24, 8, -70, 12, -76, 15, -120, 26, -130, 36, -24);
            p.aLy = curve(t, 0, 0, 8, -40, 12, -46, 15, 10, 36, 0);
            p.aLz = curve(t, 0, -10, 8, 20, 12, 24, 15, -70, 26, -75, 36, -10);
            p.fLx = curve(t, 0, -48, 8, -70, 12, -70, 15, 0, 36, -48);
            p.lRz = curve(t, 12, 3, 15, 14, 30, 3); p.lLz = curve(t, 12, -4, 15, -14, 30, -4);
            p.spinDY += curve(t, 13, 0, 15, -2.5f, 18, 0);
            p.hairX += curve(t, 12, 20, 16, -10, 24, 25, 36, 0);
            p.hairZ += Anim.sin(t * 40) * 6 * c.seg(15, 30);
            m.scale("shells", 1, 1 - rip * 0.7f, 1); m.scale("shellsB", 1, 1 - rip * 0.7f, 1);
            if (t > 4 && t < 14) { m.show("bombR", true); }
        } else if (c.is("mine_field")) {
            // drop to a knee, spin low scattering mines, then hop away
            float spin = Anim.smooth(c.seg(10, 30));
            p.kneel = curve(t, 0, 0, 8, 1, 30, 1, 33, 0);
            p.crouch = curve(t, 31, 0, 33, 1.5f, 36, -2.5f, 40, 0);
            p.spinY = spin * 360;
            p.bodyX = curve(t, 0, 2, 8, 22, 30, 18, 34, -15, 44, 2);
            p.aRx = curve(t, 0, -4, 8, -40, 10, -20, 30, -20, 34, -150, 40, -150, 44, -4);
            p.aRz = curve(t, 0, 7, 10, 60, 30, 60, 34, 20, 44, 7);
            p.fRx = curve(t, 0, -12, 10, 0, 30, 0, 44, -12);
            p.hRx = Anim.sin(t * 90) * 30 * c.seg(10, 30) * (1 - c.seg(29, 31));
            p.aLx = curve(t, 0, -24, 8, -30, 30, -30, 34, -150, 40, -150, 44, -24);
            p.aLz = curve(t, 0, -10, 8, -50, 30, -50, 34, -20, 44, -10);
            p.headX = curve(t, 0, p.headX, 8, -10, 30, -10, 34, -25, 44, p.headX);
            p.headY = -spin * 40 * (1 - c.seg(28, 32));
            p.hairZ += 40 * Anim.sin(spin * 180) ;
            p.hairX += 15 * Anim.sin(spin * 180) + curve(t, 32, 0, 36, 30, 44, 0);
            p.spinDY += curve(t, 31, 0, 35, -4, 39, 0);
        } else if (c.is("rocket")) {
            // reach behind the hair, haul out the launcher, kneel, aim, FIRE, recoil, toss it
            m.show("launcher", true);
            float pull = c.seg(4, 14);
            m.show("backBlast", t >= 24 && t < 28);
            m.scale("backBlast", 1, 1, 1 + c.seg(24, 27) * 1.5f);
            p.aRx = curve(t, 0, -4, 5, -170, 9, -160, 14, -60, 24, -58, 26, -78, 32, -60, 37, -150, 41, -40, 44, -4);
            p.aRz = curve(t, 0, 7, 5, -10, 14, 10, 44, 7);
            p.fRx = curve(t, 0, -12, 5, -60, 9, -100, 14, -50, 32, -50, 37, -30, 44, -12);
            p.aLx = curve(t, 0, -24, 10, -24, 15, -78, 24, -80, 26, -96, 34, -80, 37, -24);
            p.aLy = curve(t, 10, 0, 15, -38, 34, -38, 37, 0);
            p.fLx = curve(t, 10, -48, 15, -20, 34, -20, 37, -48);
            p.kneel = curve(t, 10, 0, 16, 1, 32, 1, 37, 0);
            p.bodyX = curve(t, 0, 2, 5, -12, 14, 8, 22, 10, 24, 10, 25.5f, -14, 30, 4, 44, 2);
            p.bodyY = curve(t, 12, 0, 18, -12, 32, -12, 38, 0);
            p.headY = curve(t, 12, c.headYaw, 18, 14, 32, 14, 36, c.headYaw);
            p.headZ = curve(t, 16, 5, 20, -18, 24, -18, 26, 6, 32, 5);
            p.headX = curve(t, 22, p.headX, 25, -20, 30, p.headX);
            p.spinDZ = curve(t, 24, 0, 26, 2.5f, 32, 0);
            p.hairX += curve(t, 0, 0, 5, -25, 12, 0, 25, 30, 32, 0);
            // launcher: out of the hair (behind/above), onto the shoulder, then tossed
            m.move("launcher", 0, Anim.lerp(-8, 0, pull), Anim.lerp(10, 0, pull));
            m.rot("launcher", Anim.lerp(-70, 0, pull) + curve(t, 24, 0, 25.5f, -18, 32, 0) + curve(t, 34, 0, 41, 80), 0, curve(t, 34, 0, 41, -60));
            if (t > 41) m.hide("launcher");
            m.scale("launcher", Anim.lerp(0.4f, 1, pull), Anim.lerp(0.4f, 1, pull), Anim.lerp(0.4f, 1, pull));
            m.show("rocketTip", t < 24);
        } else if (c.is("bomb_rain")) {
            // giggle, then hurl fistfuls of bombs straight up, then conduct the downpour
            m.show("bombR", t < 16);
            grenade = t < 16 || t > 46;
            p.crouch = curve(t, 0, 0, 10, 2.6f, 14, 0, 16, -2, 20, 0);
            p.bodyX = curve(t, 0, 2, 10, 18, 15, -24, 22, -10, 56, 2) + Anim.sin(t * 60) * 3 * c.seg(2, 10);
            p.headX = curve(t, 0, p.headX, 10, 18, 15, -40, 24, -30, 46, -30, 56, p.headX);
            p.headZ = Anim.sin(t * 35) * 14 * c.seg(18, 46) * (1 - c.seg(44, 50));
            p.aRx = curve(t, 0, -4, 10, 20, 15, -180, 20, -170) ;
            p.aLx = curve(t, 0, -24, 10, 20, 15, -180, 20, -170);
            p.aRz = curve(t, 0, 7, 10, 30, 15, 10); p.aLz = curve(t, 0, -10, 10, -30, 15, -10);
            p.fRx = curve(t, 0, -12, 10, -60, 15, 0); p.fLx = curve(t, 0, -48, 10, -60, 15, 0);
            if (t > 20) { // conducting: alternate arms stabbing the sky
                float k = c.seg(20, 48);
                float conduct = Anim.sin((t - 20) * 32);
                float fade = 1 - c.seg(46, 54);
                p.aRx = Anim.lerp(-4, -150 + conduct * 40, fade); p.aLx = Anim.lerp(-24, -150 - conduct * 40, fade);
                p.aRz = Anim.lerp(7, 25, fade); p.aLz = Anim.lerp(-10, -25, fade);
                p.fRx = -20 * fade + conduct * 15; p.fLx = -20 * fade - conduct * 15;
                p.spinDY += -Math.abs(conduct) * 1.5f * (k < 1 ? 1 : 0) * fade;
                p.lRx = conduct * 14 * fade; p.lLx = -conduct * 14 * fade;
            }
            p.hairX += curve(t, 10, 0, 15, 30, 24, 10, 56, 0);
        } else if (c.is("kamikaze")) {
            // light the antenna, quiver, launch into a bear-hug dive, BOOM, blown back tumbling
            m.show("spark", t > 6 && t < 28);
            float sh = Anim.sin(t * 160) * Anim.lerp(0, 4, c.seg(6, 16)) * (t < 16 ? 1 : 0);
            m.show("bombR", t < 8);
            p.aRx = curve(t, 0, -4, 5, -170, 8, -165, 12, -60, 16, -80, 18, -95, 28, -95, 30, -160, 44, -60, 50, -4);
            p.aRz = curve(t, 0, 7, 5, -20, 8, -20, 12, 60, 16, 50, 18, -10, 28, -10, 30, 60, 50, 7);
            p.fRx = curve(t, 0, -12, 5, -80, 8, -80, 12, -10, 50, -12);
            p.aLx = curve(t, 0, -24, 10, -40, 16, -80, 18, -95, 28, -95, 30, -160, 44, -60, 50, -24);
            p.aLz = curve(t, 0, -10, 10, -60, 16, -50, 18, 10, 28, 10, 30, -60, 50, -10);
            p.fLx = curve(t, 0, -48, 10, -10, 50, -48);
            p.crouch = curve(t, 6, 0, 15, 3.5f, 17, 0) ;
            p.bodyX = curve(t, 6, 2, 15, 25, 17, 60, 27, 65, 29, 20, 50, 2) + sh;
            p.bodyZ = sh;
            p.headX = curve(t, 6, p.headX, 15, -15, 18, -40, 27, -35, 29, 10, 50, p.headX);
            p.headZ = curve(t, 6, 5, 15, 20, 18, 0) + sh * 2;
            p.lRx = curve(t, 15, 0, 18, 35, 27, 40, 29, -30, 50, 0);
            p.lLx = curve(t, 15, -4, 18, 55, 27, 50, 29, -40, 50, -4);
            p.bRx = curve(t, 15, 0, 18, 30, 29, 20, 50, 0);
            p.bLx = curve(t, 15, 0, 18, 40, 29, 20, 50, 0);
            // blast: thrown back into a backflip tumble, lands on her feet
            p.spinX = curve(t, 28, 0, 40, -360, 50, -360);
            p.spinDY = curve(t, 15, 0, 18, -2, 27, -2, 28, 0, 33, -10, 40, -3, 44, 0);
            p.hairX += curve(t, 17, 0, 19, 60, 28, 50, 32, -40, 44, 10, 50, 0);
            p.hairZ += sh * 3;
        } else if (c.is("stomp")) {
            // knee to the chest, arms flung up, SLAM -> shockwave
            p.lRx = curve(t, 0, 0, 9, -105, 11, -110, 13, 15, 20, 10, 32, 0);
            p.bRx = curve(t, 0, 0, 9, 95, 11, 100, 13, 0, 32, 0);
            p.lLx = curve(t, 0, -4, 9, 6, 13, -25, 20, -18, 32, -4);
            p.bLx = curve(t, 9, 0, 13, 40, 20, 30, 32, 0);
            p.spinDY = curve(t, 0, 0, 7, -0.5f, 9, -3, 11, -3.5f, 13, 1.8f, 20, 1.5f, 32, 0);
            p.bodyX = curve(t, 0, 2, 9, -14, 11, -16, 13, 32, 20, 26, 32, 2);
            p.aRx = curve(t, 0, -4, 9, -165, 11, -170, 13, -30, 20, -20, 32, -4);
            p.aLx = curve(t, 0, -24, 9, -165, 11, -170, 13, -30, 20, -20, 32, -24);
            p.aRz = curve(t, 0, 7, 9, 35, 13, 60, 20, 50, 32, 7); p.aLz = curve(t, 0, -10, 9, -35, 13, -60, 20, -50, 32, -10);
            p.fRx = curve(t, 0, -12, 9, -30, 13, 0); p.fLx = curve(t, 0, -48, 9, -30, 13, 0, 32, -48);
            p.headX = curve(t, 0, p.headX, 9, -25, 13, 25, 20, 15, 32, p.headX);
            p.hairX += curve(t, 8, 0, 11, -20, 14, 45, 22, 10, 32, 0);
            p.hairZ += Anim.sin(t * 50) * 6 * c.seg(13, 26);
        } else if (c.is("kick_back")) {
            // flick the grenade up, it drops to her boot, wind the leg, VOLLEY KICK
            grenade = t < 3.5f || t > 30;
            if (t >= 3.5f && t < 16) {
                m.show("kickBomb", true);
                float k = c.seg(3.5f, 15.5f);
                float x = Anim.lerp(5, -2.5f, k), z = Anim.lerp(-3, -5.5f, k);
                float y = Anim.lerp(9.5f, 22.5f, k) - 4 * 8 * k * (1 - k) * 2.2f;
                m.move("kickBomb", x, y - 24 + 24, z);
                m.rot("kickBomb", t * 40, t * 25, 0);
            }
            p.aLx = curve(t, 0, -24, 3, -70, 4, -110, 8, -40, 14, 20, 17, 40, 24, -10, 38, -24);
            p.fLx = curve(t, 0, -48, 3, -90, 4, -30, 8, -20, 38, -48);
            p.aLz = curve(t, 8, -10, 15, -60, 24, -30, 38, -10);
            p.aRz = curve(t, 8, 7, 15, 60, 24, 30, 38, 7);
            p.aRx = curve(t, 8, -4, 13, -40, 16, 30, 24, 0, 38, -4);
            p.lRx = curve(t, 5, 0, 12, 40, 14, 45, 16.5f, -120, 21, -95, 30, 0);
            p.bRx = curve(t, 5, 0, 12, 80, 14, 85, 16.5f, 0, 21, 10, 30, 0);
            p.lLx = curve(t, 5, -4, 14, -10, 16.5f, 15, 24, 8, 38, -4);
            p.bodyX = curve(t, 0, 2, 12, 16, 16.5f, -28, 22, -18, 38, 2);
            p.bodyY = curve(t, 8, 0, 14, 18, 17, -16, 30, 0);
            p.headX = curve(t, 0, p.headX, 3, -20, 8, -10, 13, 30, 17, 0, 30, p.headX);
            p.spinDY = curve(t, 14, 0, 16.5f, -2, 20, -1, 26, 0);
            p.hairX += curve(t, 12, 0, 17, 40, 26, 0);
        } else if (c.is("boom_punch")) {
            // cock the grenade fist, lunge-punch, point-blank blast, shake out the hand
            grenade = t < 10.5f || t > 20;
            p.aLx = curve(t, 0, -24, 7, 25, 9, 20, 10.5f, -92, 14, -88, 18, -40, 24, -24);
            p.aLy = curve(t, 0, 0, 7, 30, 10.5f, -8, 18, 0);
            p.aLz = curve(t, 0, -10, 7, -30, 10.5f, -2, 20, -10);
            p.fLx = curve(t, 0, -48, 7, -110, 9, -115, 10.5f, -5, 14, -10, 18, -60, 24, -48);
            p.hLx = Anim.sin(t * 120) * 25 * c.seg(14, 22) * (1 - c.seg(21, 24));
            p.bodyY = curve(t, 0, 0, 7, -38, 9, -40, 10.5f, 28, 16, 18, 24, 0);
            p.bodyX = curve(t, 0, 2, 7, -6, 10.5f, 22, 16, 12, 24, 2);
            p.aRx = curve(t, 0, -4, 7, -60, 10.5f, 25, 18, 10, 24, -4);
            p.lLx = curve(t, 6, -4, 10.5f, -42, 18, -20, 24, -4);
            p.lRx = curve(t, 6, 0, 10.5f, 25, 18, 10, 24, 0);
            p.crouch = curve(t, 6, 0, 10.5f, 1.8f, 18, 0.6f, 24, 0);
            p.headX = curve(t, 6, p.headX, 10.5f, 12, 13, -18, 20, p.headX);
            p.hairX += curve(t, 8, 0, 11, 30, 15, -10, 22, 0);
        } else if (c.is("carpet_bomb")) {
            // pull the detonator, hold it high, CLICK, then a deranged victory dance while the sky falls
            m.show("detonator", t > 3);
            float dance = c.seg(18, 62) * (1 - c.seg(60, 66));
            float b = Anim.sin((t - 18) * 22);
            p.aRx = curve(t, 0, -4, 4, 20, 10, -175, 13, -170, 14.5f, -150, 16, -172, 18, -165);
            p.aRz = curve(t, 0, 7, 10, 10, 18, 14);
            p.fRx = curve(t, 0, -12, 10, -10, 14.5f, -40, 16, 0);
            p.aLx = curve(t, 0, -24, 8, -10, 18, -10); p.aLz = curve(t, 0, -10, 8, -45, 18, -45); p.fLx = curve(t, 0, -48, 8, -100, 18, -100);
            p.headX = curve(t, 0, p.headX, 10, -30, 16, -35, 18, -10);
            p.bodyX = curve(t, 0, 2, 10, -12, 16, -14, 18, 2);
            if (t > 18) {
                p.spinDY += -Math.abs(b) * 3 * dance;
                p.spinY += Anim.sin((t - 18) * 11) * 40 * dance;
                p.aRx = Anim.lerp(-4, -165 + b * 20, dance); p.aRz = Anim.lerp(7, 14 + b * 20, dance);
                p.aLx = Anim.lerp(-24, -150 - b * 30, dance); p.aLz = Anim.lerp(-10, -30, dance); p.fLx = Anim.lerp(-48, -30, dance);
                p.lRx = b * 30 * dance; p.lLx = -b * 30 * dance; p.bRx = Math.max(0, b) * 40 * dance; p.bLx = Math.max(0, -b) * 40 * dance;
                p.headX = Anim.lerp(p.headX, -30 + b * 15, dance); p.headZ = Anim.sin((t - 18) * 44) * 18 * dance;
                p.bodyZ = b * 10 * dance;
                p.hairX += Math.abs(b) * 30 * dance; p.hairZ += b * 25 * dance;
            }
            // final bow
            p.bodyX += curve(t, 62, 0, 66, 45, 70, 45, 72, 0);
            p.aRz += curve(t, 62, 0, 66, 50, 72, 0);
        }
        if (!grenade) m.hide("grenade");

        // ---------------- death: stagger, hat pops off, keel over backwards with a last puff
        if (c.death > 0) {
            float d = c.death;
            float fall = Anim.easeIn(Anim.clamp((d - 0.25f) / 0.6f, 0, 1));
            p.bodyX = Anim.lerp(p.bodyX, 30, Anim.smooth(d / 0.25f)) * (1 - fall) - 10 * fall;
            p.rootX = -86 * fall;
            p.rootDY = 0;
            p.crouch = 2.5f * Anim.smooth(d / 0.3f) * (1 - fall);
            p.aRx = Anim.lerp(-40, -170, fall); p.aRz = Anim.lerp(20, 50, fall); p.fRx = -30 * (1 - fall);
            p.aLx = Anim.lerp(-40, -170, fall); p.aLz = Anim.lerp(-20, -50, fall); p.fLx = -30 * (1 - fall);
            p.headX = Anim.lerp(20, -30, fall); p.headY = 0; p.headZ = 25 * Anim.smooth(d / 0.3f);
            p.lRx = -20 * fall; p.lLx = -50 * fall; p.bLx = 40 * fall;
            p.hairX = 70 * fall;
            float pop = Anim.clamp(d / 0.5f, 0, 1);
            m.move("hat", 6 * pop, -14 * Anim.sin(pop * 180) - 2 * pop, 4 * pop);
            m.rot("hat", -60 * pop, 0, -5 + 120 * pop);
            m.show("spark", d > 0.85f);
        }

        apply(m, p, c, w);
    }

    private static void apply(ModelParts m, P p, AnimCtx c, float w) {
        // crouch: drop the body and fold both legs so the boots stay planted
        if (p.crouch > 0.01f) {
            float th = (float) Math.toDegrees(Math.acos(Anim.clamp(1 - p.crouch / 12f, -1, 1)));
            p.spinDY += p.crouch;
            p.lRx -= th; p.lLx -= th; p.bRx += 2 * th; p.bLx += 2 * th;
            p.bodyX += th * 0.35f;
        } else if (p.crouch < 0) p.spinDY += p.crouch; // hop
        // kneel: right knee on the ground, left foot planted forward
        if (p.kneel > 0.001f) {
            float k = p.kneel;
            p.spinDY += 4.2f * k;
            p.lLx = Anim.lerp(p.lLx, -62, k); p.bLx = Anim.lerp(p.bLx, 62, k);
            p.lRx = Anim.lerp(p.lRx, 8, k); p.bRx = Anim.lerp(p.bRx, 84, k);
        }

        m.rot("root", p.rootX, p.rootY, p.rootZ);
        m.move("root", 0, p.rootDY, 0);
        m.rot("spin", p.spinX, p.spinY, p.spinZ);
        m.move("spin", 0, p.spinDY, p.spinDZ);
        m.rot("torso", p.bodyX, p.bodyY, p.bodyZ);
        m.rot("head", Anim.clamp(p.headX, -60, 50), Anim.clamp(p.headY, -70, 70), p.headZ);
        m.rot("armR", p.aRx, p.aRy, p.aRz); m.rot("foreR", p.fRx, 0, 0); m.rot("handR", p.hRx, 0, 0);
        m.rot("armL", p.aLx, p.aLy, p.aLz); m.rot("foreL", p.fLx, 0, 0); m.rot("handL", p.hLx, 0, 0);
        m.rot("legR", p.lRx, 0, p.lRz); m.rot("bootR", p.bRx, 0, 0);
        m.rot("legL", p.lLx, 0, p.lLz); m.rot("bootL", p.bLx, 0, 0);

        // skirt panels follow the legs
        float fwd = Math.min(Math.min(p.lRx, p.lLx), 0), back = Math.max(Math.max(p.lRx, p.lLx), 0);
        m.addRot("skirtF", Math.max(fwd * 0.5f, -38), 0, 0);
        m.addRot("skirtB", Math.min(back * 0.6f, 70) + p.hairX * 0.08f, 0, 0);
        m.addRot("skirtR", p.lRx * 0.3f, 0, Math.max(0, -p.lRx) * 0.08f);
        m.addRot("skirtL", p.lLx * 0.3f, 0, -Math.max(0, -p.lLx) * 0.08f);

        // hair: hangs against the body lean, lags & ripples down the chain
        float lag = Anim.sin(c.age * 5f - 40) * 2.5f;
        float h1 = Anim.clamp(p.hairX - p.bodyX * 0.7f - p.headX * 0.5f + lag, -40, 90);
        m.rot("hairB1", h1 * 0.6f, 0, p.hairZ * 0.4f);
        m.rot("hairB2", h1 * 0.35f + Anim.sin(c.age * 5f - 80) * 3, 0, p.hairZ * 0.3f);
        m.rot("hairB3", h1 * 0.3f + Anim.sin(c.age * 5f - 120) * 4, 0, p.hairZ * 0.3f);
        m.addRot("hairSideR", Anim.clamp(-p.headX * 0.6f, -20, 30) + w * 8, 0, Anim.sin(c.age * 4) * 2);
        m.addRot("hairSideL", Anim.clamp(-p.headX * 0.6f, -20, 30) + w * 8, 0, -Anim.sin(c.age * 4) * 2);
        // antenna wobble
        m.addRot("stalk", Anim.sin(c.age * 9) * 4 - w * 10 - p.hairX * 0.05f, 0, Anim.sin(c.age * 6) * 5);
        m.addRot("radioRod", Anim.sin(c.age * 11 + 30) * 5 - w * 8, 0, 0);
    }
}
