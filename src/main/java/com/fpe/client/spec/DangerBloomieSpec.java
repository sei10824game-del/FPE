package com.fpe.client.spec;

import static com.fpe.client.model.Anim.curve;

import com.fpe.client.model.Anim;
import com.fpe.client.model.AnimCtx;
import com.fpe.client.model.ModelParts;
import com.fpe.client.model.ModelSpec;
import com.fpe.client.model.ModelSpec.Face;
import com.fpe.client.model.ModelSpec.Pattern;

/**
 * Danger AU Bloomie: long navy double-breasted coat, tall black pointed hat with horn spikes and a hazard '!' sign,
 * two very long black/tan hazard-striped ribbons, pale-blue mask face, bandage-striped cuffs and an AK-47.
 */
public final class DangerBloomieSpec {
    private DangerBloomieSpec() {}

    static final int NAVY = 0x1A1A20, NAVY_D = 0x111116, NAVY_L = 0x2A2A33, BTN = 0xC8CCD4, FACE = 0xAFCADA;
    static final int HAIR = 0x0F0F14, HAT = 0x15151D, HAT_L = 0x24242F, TAN = 0xDCC690, STRIPE_D = 0x16161C;
    static final int GLOVE = 0x121218, WOOD = 0x8A4E24, WOOD_D = 0x5E3416, STEEL = 0x1F2026, STEEL_L = 0x34363F;

    public static final ModelSpec SPEC = com.fpe.client.model.BbModel.load("danger_bloomie", 0.66f);
    static final ModelSpec PROC = build();

    private static ModelSpec build() {
        ModelSpec m = new ModelSpec("danger_bloomie");
        m.group("root", null, 0, 24, 0);
        m.group("spin", "root", 0, 12, 0);

        // ---------------------------------------------------------------- legs
        for (int s = -1; s <= 1; s += 2) {
            String k = s < 0 ? "R" : "L";
            float x = 2 * s;
            m.part("leg" + k, "spin", x, 12, 0, -1.4f, 0, -1.4f, 2.8f, 7, 2.8f, NAVY_D);
            m.part("shin" + k, "leg" + k, x, 19, 0, -1.5f, 0, -1.5f, 3, 5, 3, GLOVE).decor(Face.FRONT, 0, 0, 3, 1, TAN);
            m.part("toe" + k, "shin" + k, x, 19, 0, -1.3f, 3.6f, -2.8f, 2.6f, 1.4f, 1.4f, GLOVE);
        }

        // ---------------------------------------------------------------- hips + long coat skirt
        m.group("hips", "spin", 0, 12, 0);
        m.part("coatR", "hips", -2, 12, 0, -2.6f, 0, -2.7f, 4.8f, 11, 5.4f, NAVY).rot(0, 0, 4)
                .decor(Face.FRONT, 4, 0, 1, 11, NAVY_D).decor(Face.FRONT, 0, 10, 5, 1, NAVY_D).decor(Face.RIGHT, 0, 10, 6, 1, NAVY_D)
                .decor(Face.FRONT, 1, 2, 1, 1, BTN);
        m.part("coatL", "hips", 2, 12, 0, -2.2f, 0, -2.7f, 4.8f, 11, 5.4f, NAVY).rot(0, 0, -4)
                .decor(Face.FRONT, 0, 0, 1, 11, NAVY_L).decor(Face.FRONT, 0, 10, 5, 1, NAVY_D).decor(Face.LEFT, 0, 10, 6, 1, NAVY_D)
                .decor(Face.FRONT, 3, 2, 1, 1, BTN);
        m.part("coatBack", "hips", 0, 12, 2.3f, -4.6f, 0, -0.5f, 9.2f, 11.4f, 1.2f, NAVY).rot(7, 0, 0)
                .decor(Face.BACK, 4, 2, 1, 9, NAVY_D).decor(Face.BACK, 0, 10, 10, 2, NAVY_D);

        // ---------------------------------------------------------------- torso
        m.part("torso", "hips", 0, 12, 0, -4, -10, -2.25f, 8, 10, 4.5f, NAVY)
                .decor(Face.FRONT, 5, 0, 1, 10, NAVY_D)
                .decor(Face.FRONT, 1, 2, 1, 1, BTN).decor(Face.FRONT, 6, 2, 1, 1, BTN)
                .decor(Face.FRONT, 1, 5, 1, 1, BTN).decor(Face.FRONT, 6, 5, 1, 1, BTN)
                .decor(Face.FRONT, 1, 8, 1, 1, BTN).decor(Face.FRONT, 6, 8, 1, 1, BTN)
                .decor(Face.FRONT, 0, 9, 8, 1, NAVY_D).decor(Face.BACK, 3, 0, 2, 10, NAVY_D);
        m.part("lapel", "torso", 0, 12, 0, -3.4f, -10, -2.6f, 6.8f, 3, 0.6f, NAVY_L)
                .decor(Face.FRONT, 3, 0, 1, 3, NAVY_D).decor(Face.FRONT, 0, 2, 1, 1, BTN);
        m.part("collar", "torso", 0, 12, 0, -3.9f, -12.6f, -3.9f, 7.8f, 3.4f, 7, NAVY)
                .decor(Face.FRONT, 0, 0, 8, 1, NAVY_L).decor(Face.FRONT, 4, 1, 1, 3, NAVY_D);
        m.part("shoulderR", "torso", -4, 2.2f, 0, -2.4f, -0.6f, -2.5f, 3, 1.6f, 5, NAVY_L);
        m.part("shoulderL", "torso", 4, 2.2f, 0, -0.6f, -0.6f, -2.5f, 3, 1.6f, 5, NAVY_L);
        m.part("strap", "torso", 0, 7, -2.4f, -0.6f, -6.5f, -0.4f, 1.2f, 13, 0.5f, 0x3A2A1E).rot(0, 0, -38);
        m.part("strapB", "torso", 0, 7, 2.4f, -0.6f, -6.5f, -0.1f, 1.2f, 13, 0.5f, 0x3A2A1E).rot(0, 0, 38);

        // ---------------------------------------------------------------- head + hair
        m.group("neck", "torso", 0, 2, 0);
        m.part("head", "neck", 0, 2, 0, -3.5f, -7, -3.5f, 7, 7, 7, FACE)
                .decor(Face.FRONT, 1, 3, 2, 1, 0x3A2E10).decorGlow(Face.FRONT, 1, 3, 1, 1, 0xFFD84A)
                .decor(Face.FRONT, 4, 2, 3, 3, HAIR).decor(Face.FRONT, 2, 5, 3, 1, 0x8AA6B8);
        m.part("hairBack", "head", 0, 2, 0, -3.9f, -6.6f, 2.6f, 7.8f, 6.8f, 1.6f, HAIR);
        m.part("hairSideR", "head", -3.6f, -4.6f, 0, -0.8f, 0, -3.8f, 1.6f, 6.4f, 7, HAIR).rot(0, 0, 4)
                .decor(Face.RIGHT, 0, 5, 7, 1, NAVY_D);
        m.part("hairSideL", "head", 3.6f, -4.6f, 0, -0.8f, 0, -3.8f, 1.6f, 6.4f, 7, HAIR).rot(0, 0, -4)
                .decor(Face.LEFT, 0, 5, 7, 1, NAVY_D);
        m.part("fringe", "head", 0, -4.6f, -3.6f, -3.8f, 0, -0.5f, 7.6f, 1.6f, 0.8f, HAIR)
                .decor(Face.FRONT, 2, 1, 1, 1, FACE).decor(Face.FRONT, 5, 1, 1, 1, FACE);

        // ---------------------------------------------------------------- black horns + choppy bun wrapped in marking tape (canon)
        m.part("hairTop", "head", 0, -7, 0, -3.9f, -1.2f, -3.9f, 7.8f, 1.6f, 7.8f, HAIR);
        m.part("bun", "head", 0, -8.2f, 1.4f, -2.2f, -3.4f, -2.2f, 4.4f, 3.4f, 4.4f, HAIR).pattern(Pattern.DIAG, 0x24242F, 2);
        m.part("bunTape", "bun", 0, -9.6f, 1.4f, -2.5f, -0.6f, -2.5f, 5, 1.2f, 5, TAN).pattern(Pattern.DIAG, STRIPE_D, 1);
        m.part("bunTuft1", "bun", 0, -11.4f, 1.4f, -0.5f, -2.4f, -0.5f, 1, 2.4f, 1, HAIR).rot(-20, 0, 12);
        m.part("bunTuft2", "bun", 0, -11.4f, 1.4f, -0.5f, -2.2f, -0.5f, 1, 2.2f, 1, HAIR).rot(10, 0, -18);
        m.part("hornR", "head", -2.4f, -7.4f, -0.6f, -1, -5.4f, -1, 2, 5.4f, 2, HAT).pattern(Pattern.STRIPE_H, 0xE8E8EC, 4).rot(-10, 0, -26);
        m.part("hornTipR", "hornR", -2.4f, -12.4f, -0.6f, -0.6f, -3, -0.6f, 1.2f, 3, 1.2f, HAT).rot(0, 0, -14);
        m.part("hornL", "head", 2.4f, -7.4f, -0.6f, -1, -5.4f, -1, 2, 5.4f, 2, HAT).rot(-10, 0, 26);
        m.part("hornTipL", "hornL", 2.4f, -12.4f, -0.6f, -0.6f, -3, -0.6f, 1.2f, 3, 1.2f, HAT).rot(0, 0, 14);

        // ---------------------------------------------------------------- two very long hazard ribbons (4 segments each)
        for (int s = -1; s <= 1; s += 2) {
            String k = s < 0 ? "R" : "L";
            float x = 3.4f * s;
            String par = "head";
            float y = -5.4f;
            float[] len = {7, 7, 6.5f, 5.5f};
            for (int i = 0; i < 4; i++) {
                String n = "rib" + k + (i + 1);
                ModelSpec.Part pt = m.part(n, par, x, y, 3.8f, -1.2f, 0, -0.3f, 2.4f, len[i], 0.6f, TAN).pattern(Pattern.DIAG, STRIPE_D, 2);
                if (i == 0) pt.rot(14, 0, 9 * -s);
                par = n; y += len[i];
            }
            m.part("ribEnd" + k, "rib" + k + "4", x, y, 3.8f, -1.4f, 0, -0.35f, 2.8f, 1, 0.7f, STRIPE_D);
            m.part("ribKnot" + k, "head", x, -5.4f, 3.6f, -1.3f, -1.3f, -0.8f, 2.6f, 2.6f, 1.6f, TAN).pattern(Pattern.DIAG, STRIPE_D, 1);
        }

        // ---------------------------------------------------------------- arms
        for (int s = -1; s <= 1; s += 2) {
            String k = s < 0 ? "R" : "L";
            float x = 5.5f * s;
            m.part("arm" + k, "torso", x, 2.6f, 0, -1.75f, -1, -1.75f, 3.5f, 8, 3.5f, NAVY).decor(Face.FRONT, 0, 7, 4, 1, NAVY_D);
            m.part("cuff" + k, "arm" + k, x, 2.6f, 0, -2, 6.4f, -2, 4, 2.6f, 4, TAN).pattern(Pattern.STRIPE_H, STRIPE_D, 1);
            m.part("hand" + k, "arm" + k, x, 2.6f, 0, -1.3f, 9, -1.3f, 2.6f, 2.6f, 2.6f, GLOVE);
        }

        // ---------------------------------------------------------------- AK-47 (held in the right hand, barrel along -z)
        String G = "gun";
        float gx = -3.9f, gy = 12.6f, gz = -0.2f;
        m.group(G, "armR", gx, gy, gz);
        m.part("receiver", G, gx, gy, gz, -0.8f, -3, -4.2f, 1.6f, 2.3f, 6, STEEL)
                .decor(Face.LEFT, 1, 0, 4, 1, STEEL_L).decor(Face.RIGHT, 1, 0, 4, 1, STEEL_L).decor(Face.RIGHT, 3, 1, 1, 1, 0x50525C);
        m.part("dustCover", G, gx, gy, gz, -0.7f, -3.5f, -3.4f, 1.4f, 0.6f, 4.8f, STEEL_L);
        m.part("rearSight", G, gx, gy, gz, -0.5f, -3.9f, -4.3f, 1, 0.9f, 0.9f, STEEL);
        m.part("stock", G, gx, gy, gz, -0.65f, -2.6f, 1.6f, 1.3f, 2, 4.6f, WOOD).rot(8, 0, 0)
                .decor(Face.LEFT, 0, 0, 5, 1, 0xA0602E).decor(Face.RIGHT, 0, 0, 5, 1, 0xA0602E);
        m.part("buttPlate", "stock", gx, gy, gz, -0.75f, -2.8f, 6.1f, 1.5f, 2.6f, 0.6f, STEEL);
        m.part("grip", G, gx, gy, gz, -0.55f, -1, 0.2f, 1.1f, 2.8f, 1.2f, WOOD_D).rot(20, 0, 0);
        m.part("trigGuard", G, gx, gy, gz, -0.25f, -0.9f, -1.4f, 0.5f, 1, 1.6f, STEEL);
        m.group("mag", G, gx, gy - 0.9f, gz - 2.8f);
        m.part("mag1", "mag", gx, gy - 0.9f, gz - 2.8f, -0.6f, 0, -0.9f, 1.2f, 2.4f, 1.7f, 0x2C2A30).rot(-10, 0, 0)
                .decor(Face.LEFT, 0, 0, 2, 1, STEEL_L);
        m.part("mag2", "mag1", gx, gy + 1.4f, gz - 3.2f, -0.6f, 0, -0.9f, 1.2f, 2, 1.7f, 0x2C2A30).rot(-24, 0, 0);
        m.part("handguard", G, gx, gy, gz, -0.85f, -2.7f, -7.8f, 1.7f, 1.9f, 3.7f, WOOD)
                .decor(Face.LEFT, 0, 1, 4, 1, WOOD_D).decor(Face.RIGHT, 0, 1, 4, 1, WOOD_D);
        m.part("gasTube", G, gx, gy, gz, -0.6f, -3.5f, -8.6f, 1.2f, 0.8f, 5, WOOD_D);
        m.part("launcherTube", G, gx, gy, gz, -0.65f, -0.9f, -8.6f, 1.3f, 1.2f, 4, 0x3A3B44);
        m.part("barrel", G, gx, gy, gz, -0.35f, -2.4f, -12, 0.7f, 0.7f, 4.4f, STEEL_L);
        m.part("frontSight", G, gx, gy, gz, -0.3f, -3.6f, -11.4f, 0.6f, 1.3f, 0.6f, STEEL);
        m.part("muzzle", G, gx, gy, gz, -0.5f, -2.55f, -13.2f, 1, 1, 1.3f, STEEL);
        m.group("flashG", G, gx, gy - 2.05f, gz - 13.2f);
        m.part("flash", "flashG", gx, gy - 2.05f, gz - 13.2f, -1.4f, -1.4f, -3.2f, 2.8f, 2.8f, 3.2f, 0xFFD45A).glow();
        m.part("flashX", "flashG", gx, gy - 2.05f, gz - 13.2f, -0.4f, -3, -1.6f, 0.8f, 6, 1, 0xFFF0A0).glow();
        m.part("flashY", "flashG", gx, gy - 2.05f, gz - 13.2f, -3, -0.4f, -1.6f, 6, 0.8f, 1, 0xFFF0A0).glow();

        m.animator(DangerBloomieSpec::animate);
        return m;
    }

    // ==================================================================== animation
    private static final class P {
        float rootX, rootDY, spinX, spinY, spinDY, spinDZ;
        float bodyX, bodyY, bodyZ, headX, headY, headZ;
        float aRx, aRy, aRz, aLx, aLy, aLz;
        float lRx, lRz, sRx, lLx, lLz, sLx;
        float gunP, gunYaw, gunRoll, gunDY, gunDZ;
        float ribX, ribZ, ribOut, crouch, kneel;
    }

    /** ticks since the last shot of a schedule start..end step (huge if none yet) */
    static float since(float t, int start, int end, int step) {
        if (t < start) return 99;
        int k = Math.min(end, start + (int) ((t - start) / step) * step);
        return t - k;
    }

    /** blend between low-ready (k=0) and shouldered aim (k=1) */
    static void aim(P p, float k, float pitch) {
        p.aRx = Anim.lerp(-26, -84, k); p.aRy = Anim.lerp(0, -6, k); p.aRz = Anim.lerp(6, 0, k);
        p.aLx = Anim.lerp(-46, -86, k); p.aLy = Anim.lerp(36, 38, k); p.aLz = Anim.lerp(0, -4, k);
        p.gunP = Anim.lerp(36, pitch, k);
    }

    private static void animate(ModelParts m, AnimCtx c) {
        P p = new P();
        float w = c.walk();
        float sw = Anim.sinr(c.limbSwing * 0.6f);
        float breathe = Anim.sin(c.age * 6f);
        float t = c.t;
        float pitch = Anim.clamp(c.headPitch, -40, 40);

        // ---------------- idle: cold, still, rifle at low ready; only breath and ribbons move
        aim(p, 0, 0);
        p.aRx += breathe * 1.5f; p.aLx += breathe * 1.5f;
        p.bodyX = 1 + breathe * 0.8f;
        p.headX = pitch * 0.8f + 3; p.headY = c.headYaw; p.headZ = -3;
        p.lLx = -3; p.lRz = 2; p.lLz = -2;
        p.ribZ = Anim.sin(c.age * 2.2f) * 4;

        // ---------------- walk: measured military march, rifle steady, coat swinging
        if (w > 0.01f) {
            p.lRx += sw * 32 * w; p.lLx -= sw * 32 * w;
            p.sRx += Math.max(0, -Anim.sinr(c.limbSwing * 0.6f + 1.3f)) * 35 * w;
            p.sLx += Math.max(0, Anim.sinr(c.limbSwing * 0.6f + 1.3f)) * 35 * w;
            p.bodyX += 4 * w; p.bodyY += sw * 4 * w;
            p.spinDY -= Math.abs(Anim.sinr(c.limbSwing * 0.6f)) * 0.6f * w;
            p.aRx += sw * 4 * w; p.aLx -= sw * 4 * w; p.gunP += sw * 3 * w;
            p.ribX += 22 * w + Math.abs(sw) * 6 * w;
            p.ribZ += sw * 5 * w;
        }

        float flash = 99; float flashScale = 1;

        if (c.is("burst")) {
            float k = curve(t, 0, 0, 7, 1, 25, 1, 30, 0);
            aim(p, k, pitch);
            float s1 = since(t, 10, 14, 2), s2 = since(t, 20, 24, 2);
            flash = (t < 20) ? s1 : s2;
            float rec = Math.max(0, 1 - flash / 2f) * (t < 26 ? 1 : 0);
            p.gunP -= rec * 7; p.aRx -= rec * 5; p.aLx -= rec * 4; p.bodyX -= rec * 3; p.spinDZ += rec * 0.4f;
            p.headX = Anim.lerp(p.headX, 8 + pitch * 0.5f, k); p.headZ = Anim.lerp(-3, -10, k); p.headY = Anim.lerp(c.headYaw, -6, k);
            p.bodyY = 8 * k; p.lLx = Anim.lerp(-3, -16, k); p.lRx = Anim.lerp(0, 12, k);
        } else if (c.is("spray")) {
            float k = curve(t, 0, 0, 8, 1, 44, 1, 52, 0);
            aim(p, k * 0.75f, 2);
            float sweep = Anim.lerp(-40, 40, Anim.smooth(c.seg(10, 42))) * k;
            p.spinY = sweep * 0.55f; p.bodyY = sweep * 0.45f;
            p.headY = 0; p.headZ = -6 * k;
            flash = since(t, 10, 42, 2);
            float rec = t <= 43 ? Math.max(0, 1 - flash / 1.6f) : 0;
            p.gunP -= rec * 6 + Anim.sin(t * 97) * 2 * c.seg(10, 12); p.aRx -= rec * 4; p.aLx -= rec * 3;
            p.bodyX = Anim.lerp(1, 6, k) - rec * 2; p.bodyZ = Anim.sin(t * 140) * 1.5f * c.seg(10, 12) * (1 - c.seg(42, 44));
            p.crouch = 1.6f * k; p.lRz = 2 + 9 * k; p.lLz = -2 - 9 * k; p.lLx = -12 * k; p.lRx = 10 * k;
            p.ribZ += -sweep * 0.4f; p.ribX += 10 * k;
        } else if (c.is("grenade_launcher")) {
            p.kneel = curve(t, 3, 0, 10, 1, 26, 1, 33, 0);
            float k = curve(t, 2, 0, 10, 1, 26, 1, 32, 0);
            aim(p, k, -26);
            p.aLx = Anim.lerp(p.aLx, -70, k); p.aLy = Anim.lerp(p.aLy, 26, k); // hand under the GP tube
            p.aLx += curve(t, 10, 0, 12, 12, 14, 0); // thumb the launcher
            flash = since(t, 16, 16, 1); flashScale = 1.6f;
            float rec = Math.max(0, 1 - flash / 5f) * (t >= 16 ? 1 : 0);
            p.gunP -= rec * 26; p.aRx -= rec * 18; p.aLx -= rec * 18; p.bodyX = 4 * k - rec * 14; p.spinDZ += rec * 1.4f;
            p.headX = Anim.lerp(p.headX, -6, k) - rec * 10; p.headZ = -8 * k;
            p.ribX += rec * 20;
        } else if (c.is("shotgun")) {
            float k = curve(t, 0, 0, 7, 1, 20, 1, 26, 0);
            // hip fire: rifle level at the hip
            p.aRx = Anim.lerp(p.aRx, -38, k); p.aLx = Anim.lerp(p.aLx, -62, k); p.aLy = Anim.lerp(p.aLy, 32, k);
            p.gunP = Anim.lerp(p.gunP, 4, k);
            p.crouch = curve(t, 0, 0, 8, 2.4f, 10, 2.6f, 12, 1, 26, 0);
            p.bodyX = curve(t, 0, 1, 8, 16, 10, 16, 11.5f, -16, 18, -4, 26, 1);
            flash = since(t, 10, 10, 1); flashScale = 2.1f;
            float rec = Math.max(0, 1 - flash / 4f) * (t >= 10 ? 1 : 0);
            p.gunP -= rec * 34; p.aRx -= rec * 20; p.aLx -= rec * 14;
            p.spinDZ += curve(t, 10, 0, 12, 3, 20, 1.5f, 26, 0);
            p.lLx = -20 * k; p.lRx = 16 * k; p.lRz = 2 + 6 * k; p.lLz = -2 - 6 * k;
            p.headX = curve(t, 0, p.headX, 8, 15, 11, -15, 20, p.headX);
            p.ribX += curve(t, 10, 0, 12, 40, 20, 10, 26, 0);
        } else if (c.is("butt_bash")) {
            float flip = curve(t, 0, 0, 7, 180, 15, 180, 22, 0);
            p.gunYaw = flip;
            p.gunP = curve(t, 0, 36, 7, 6, 15, 6, 22, 36);
            p.aRx = curve(t, 0, -26, 7, -40, 9, -38, 11, -98, 15, -90, 22, -26);
            p.aLx = curve(t, 0, -46, 7, -54, 9, -52, 11, -104, 15, -96, 22, -46);
            p.aLy = curve(t, 0, 36, 7, 30, 11, 22, 22, 36);
            p.bodyY = curve(t, 0, 0, 8, -32, 11, 18, 16, 10, 26, 0);
            p.bodyX = curve(t, 0, 1, 8, -8, 11, 20, 16, 12, 26, 1);
            p.spinDZ = curve(t, 8, 0, 11, -2.6f, 18, -1.5f, 26, 0);
            p.lLx = curve(t, 6, -3, 11, -36, 18, -20, 26, -3);
            p.lRx = curve(t, 6, 0, 11, 24, 18, 12, 26, 0);
            p.headX = curve(t, 6, p.headX, 11, 14, 18, p.headX);
            p.ribX += curve(t, 8, 0, 12, 30, 20, 0);
            p.ribZ += curve(t, 6, 0, 9, 20, 12, -25, 20, 0);
        } else if (c.is("ribbon_whip")) {
            float spin = Anim.easeOut(c.seg(10, 21));
            p.crouch = curve(t, 0, 0, 8, 2.4f, 21, 2, 28, 0);
            p.spinY = curve(t, 0, 0, 9, -40, 10, -40) * (1 - spin) + spin * 400 - 40 * spin;
            p.bodyY = curve(t, 0, 0, 9, -35, 12, 10, 22, 0);
            p.aRx = curve(t, 0, -26, 8, -60, 20, -60, 28, -26); p.aLx = curve(t, 0, -46, 8, -70, 20, -70, 28, -46);
            p.gunP = curve(t, 0, 36, 8, 70, 20, 70, 28, 36);
            p.headX = curve(t, 0, p.headX, 9, 18, 12, -20, 20, -15, 28, p.headX);
            p.lRz = curve(t, 8, 2, 12, 14, 22, 2); p.lLz = curve(t, 8, -2, 12, -14, 22, -2);
            p.ribOut = curve(t, 8, 0, 11, 1, 19, 1, 23, 0);
            float wob = Anim.sin((t - 21) * 55) * 30 * Math.max(0, 1 - (t - 21) / 12f) * (t > 21 ? 1 : 0);
            p.ribX += wob + curve(t, 0, 0, 9, 25, 10, 25);
            p.ribZ += wob * 0.6f;
        } else if (c.is("suppress")) {
            p.kneel = curve(t, 2, 0, 10, 1, 58, 1, 64, 0);
            float k = curve(t, 2, 0, 11, 1, 57, 1, 63, 0);
            aim(p, k, pitch + 3);
            float sweep = Anim.sin((t - 14) * 9) * 10 * c.seg(14, 20) * (1 - c.seg(54, 58));
            p.bodyY = sweep; p.headY = sweep * 0.3f;
            flash = since(t, 14, 56, 3);
            float rec = t <= 57 ? Math.max(0, 1 - flash / 2f) : 0;
            p.gunP -= rec * 5; p.aRx -= rec * 4; p.aLx -= rec * 3; p.bodyX = 6 * k - rec * 2;
            p.headX = Anim.lerp(p.headX, 10, k); p.headZ = -10 * k;
        } else if (c.is("reload")) {
            // tilt rifle, rip the mag, fetch a new one from the coat, slam it, rack the bolt
            p.gunRoll = curve(t, 0, 0, 4, 40, 22, 40, 26, 10, 32, 0);
            p.gunP = curve(t, 0, 36, 4, 12, 26, 12, 32, 36);
            p.aRx = curve(t, 0, -26, 4, -48, 26, -48, 32, -26);
            p.aLx = curve(t, 0, -46, 4, -40, 8, -36, 11, -10, 15, 10, 18, -30, 20, -40, 23, -78, 25, -60, 27, -66, 32, -46);
            p.aLy = curve(t, 0, 36, 4, 22, 11, 10, 15, -10, 18, 15, 21, 22, 23, 44, 32, 36);
            p.aLz = curve(t, 11, 0, 15, -14, 18, 0);
            p.headX = curve(t, 0, p.headX, 4, 32, 27, 30, 32, p.headX);
            p.headY = curve(t, 0, c.headYaw, 4, 0, 13, 22, 17, 22, 20, 0, 32, c.headYaw);
            p.bodyX = curve(t, 0, 1, 4, 10, 24, 10, 25.5f, 4, 27, 10, 32, 1);
            p.bodyY = curve(t, 10, 0, 15, 14, 19, 0);
            boolean has = t < 9 || t >= 17.5f;
            m.show("mag", has || t < 13);
            if (t >= 9 && t < 13) { float d = c.seg(9, 13); m.move("mag", 0, d * d * 9, -d * 2); m.rot("mag", d * 70, 0, d * 40); }
            if (t >= 17.5f && t < 21) { float d = 1 - c.seg(17.5f, 21); m.move("mag", 0, d * 4, d * 1); m.rot("mag", d * 20, 0, 0); }
        } else if (c.is("backstep")) {
            float flip = Anim.smooth(c.seg(4, 14));
            p.spinX = -360 * flip;
            p.spinDY = curve(t, 0, 0, 3, 1.5f, 15, 1.5f, 22, 0) - Anim.sin(flip * 180) * 13;
            p.crouch = curve(t, 0, 0, 3, 2, 5, 0, 13, 0, 15, 2.6f, 22, 0);
            float tuck = Anim.sin(flip * 180);
            p.lRx -= tuck * 85; p.lLx -= tuck * 95; p.sRx += tuck * 110; p.sLx += tuck * 120;
            float k = curve(t, 13, 0, 16, 1, 19, 1, 22, 0);
            aim(p, k, pitch);
            p.aRx -= tuck * 30; p.aLx -= tuck * 30;
            flash = since(t, 16, 16, 1);
            float rec = Math.max(0, 1 - flash / 2.5f) * (t >= 16 ? 1 : 0);
            p.gunP -= rec * 10; p.aRx -= rec * 6;
            p.ribX += tuck * 70; p.headX += tuck * 20;
        } else if (c.is("bullet_hail")) {
            // fire the whole drum into the sky, then calmly aim while the bullets come down
            float up = curve(t, 0, 0, 10, 1, 38, 1, 48, 0);
            float k = curve(t, 40, 0, 50, 1, 76, 1, 84, 0);
            aim(p, Math.max(up, k), Anim.lerp(pitch, -82, up));
            p.aRx -= up * 55; p.aLx -= up * 70; p.aLy = Anim.lerp(p.aLy, 10, up);
            p.headX = Anim.lerp(p.headX, -40, up) + Anim.sin(t * 70) * 6 * up * c.seg(12, 14);
            p.bodyX = -14 * up + 4 * k;
            float s1 = since(t, 12, 40, 2), s2 = since(t, 50, 74, 4);
            flash = t < 46 ? s1 : s2;
            float rec = Math.max(0, 1 - flash / 2f) * ((t < 42 || (t > 49 && t < 76)) ? 1 : 0);
            p.gunP -= rec * 6; p.aRx -= rec * 4; p.bodyZ = Anim.sin(t * 150) * 2 * up * c.seg(12, 14);
            p.lRz = 2 + 7 * up; p.lLz = -2 - 7 * up; p.crouch = 1.2f * up;
            p.ribX += 10 * up + Anim.sin(t * 40) * 8 * up;
            p.headZ = -10 * k;
        }

        // ---------------- death: rifle slips, knees buckle, falls face-first
        if (c.death > 0) {
            float d = c.death;
            float fall = Anim.easeIn(Anim.clamp((d - 0.4f) / 0.55f, 0, 1));
            float drop = Anim.smooth(d / 0.35f);
            p.kneel = Anim.smooth((d - 0.15f) / 0.3f);
            p.gunP = Anim.lerp(36, 95, drop); p.gunRoll = 50 * drop;
            p.aRx = Anim.lerp(-26, -5, drop) - 60 * fall; p.aLx = Anim.lerp(-46, 0, drop) - 70 * fall; p.aLy = 36 * (1 - drop); p.aLz = -10 * drop;
            p.bodyX = 20 * drop; p.headX = 30 * drop; p.headZ = 12 * drop;
            p.rootX = 84 * fall; p.rootDY = 0;
            p.ribX = -40 * fall + 30 * drop * (1 - fall);
        }

        // flash visibility
        boolean f = flash < 1.5f;
        m.show("flashG", f);
        if (f) { float s = flashScale * (1.2f - flash * 0.4f); m.scale("flashG", s, s, s); m.rot("flashG", 0, 0, c.age * 47 % 90); }

        apply(m, p, c, w);
    }

    private static void apply(ModelParts m, P p, AnimCtx c, float w) {
        if (p.crouch > 0.01f) {
            float th = (float) Math.toDegrees(Math.acos(Anim.clamp(1 - p.crouch / 12f, -1, 1)));
            p.spinDY += p.crouch; p.lRx -= th; p.lLx -= th; p.sRx += 2 * th; p.sLx += 2 * th; p.bodyX += th * 0.3f;
        }
        if (p.kneel > 0.001f) {
            float k = p.kneel;
            p.spinDY += 4.2f * k;
            p.lLx = Anim.lerp(p.lLx, -62, k); p.sLx = Anim.lerp(p.sLx, 62, k);
            p.lRx = Anim.lerp(p.lRx, 8, k); p.sRx = Anim.lerp(p.sRx, 84, k);
        }
        m.rot("root", p.rootX, 0, 0); m.move("root", 0, p.rootDY, 0);
        m.rot("spin", p.spinX, p.spinY, 0); m.move("spin", 0, p.spinDY, p.spinDZ);
        m.rot("torso", p.bodyX, p.bodyY, p.bodyZ);
        m.rot("head", Anim.clamp(p.headX, -55, 45), Anim.clamp(p.headY, -70, 70), p.headZ);
        m.rot("armR", p.aRx, p.aRy, p.aRz); m.rot("armL", p.aLx, p.aLy, p.aLz);
        m.rot("legR", p.lRx, 0, p.lRz); m.rot("shinR", p.sRx, 0, 0);
        m.rot("legL", p.lLx, 0, p.lLz); m.rot("shinL", p.sLx, 0, 0);
        // gun: cancel the arm pitch so gunP is the rifle's pitch relative to the body (flip-aware)
        float cy = Anim.cos(p.gunYaw);
        m.rot("gun", p.gunP - p.aRx * cy, p.gunYaw - p.aRy, p.gunRoll);
        m.move("gun", 0, p.gunDY, p.gunDZ);

        // coat panels follow the legs
        m.addRot("coatR", Math.max(-45, Math.min(40, p.lRx * 0.7f)), 0, Math.max(0, -p.lRx) * 0.05f);
        m.addRot("coatL", Math.max(-45, Math.min(40, p.lLx * 0.7f)), 0, -Math.max(0, -p.lLx) * 0.05f);
        m.addRot("coatBack", Math.max(0, Math.max(p.lRx, p.lLx)) * 0.5f + w * 8 + p.ribX * 0.08f, 0, 0);

        // ribbons: hang straight down against head/body tilt, trail, ripple with phase lag; ribOut = lashing horizontally
        float base = Anim.clamp(-p.headX - p.bodyX + p.ribX - p.rootX, -60, 100);
        float out = p.ribOut;
        for (int s = -1; s <= 1; s += 2) {
            String k = s < 0 ? "R" : "L";
            float side = s < 0 ? 1 : -1;
            float ph = s < 0 ? 0 : 35;
            m.addRot("rib" + k + "1", Anim.lerp(base * 0.7f + Anim.sin(c.age * 4 + ph) * 3, 75, out), 0,
                    Anim.lerp(p.ribZ * 0.5f, 70 * side, out));
            for (int i = 2; i <= 4; i++) {
                float wave = Anim.sin(c.age * 4 + ph - i * 45) * (2 + i * 1.5f);
                m.rot("rib" + k + i, Anim.lerp(base * 0.12f + wave + w * 4, Anim.sin(c.age * 30 - i * 60) * 10, out), 0,
                        Anim.lerp(p.ribZ * 0.25f, 0, out));
            }
        }
        m.addRot("crown2", Anim.sin(c.age * 3) * 1.5f - w * 3, 0, 0);
        m.addRot("crown3", Anim.sin(c.age * 3 - 40) * 2.5f - w * 4, 0, 0);
        m.addRot("crownTip", Anim.sin(c.age * 3 - 80) * 3.5f - w * 5, 0, 0);
    }
}
