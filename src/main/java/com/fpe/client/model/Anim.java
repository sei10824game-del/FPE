package com.fpe.client.model;

/** Math helpers for animators. */
public final class Anim {
    private Anim() {}

    public static float clamp(float v, float lo, float hi) { return v < lo ? lo : Math.min(v, hi); }
    public static float lerp(float a, float b, float t) { return a + (b - a) * t; }
    public static float smooth(float t) { t = clamp(t, 0, 1); return t * t * (3 - 2 * t); }
    public static float easeOut(float t) { t = clamp(t, 0, 1); return 1 - (1 - t) * (1 - t) * (1 - t); }
    public static float easeIn(float t) { t = clamp(t, 0, 1); return t * t * t; }
    public static float sin(float deg) { return (float) Math.sin(Math.toRadians(deg)); }
    public static float cos(float deg) { return (float) Math.cos(Math.toRadians(deg)); }
    /** sin with radians argument */
    public static float sinr(float rad) { return (float) Math.sin(rad); }

    /**
     * Smooth keyframe curve: pairs of (time, value). e.g. curve(t, 0,0, 6,-90, 10,20, 20,0).
     * Eases between neighbouring keys; clamps outside the range.
     */
    public static float curve(float t, float... tv) {
        if (t <= tv[0]) return tv[1];
        for (int i = 0; i + 3 < tv.length; i += 2) {
            if (t <= tv[i + 2]) {
                float k = (t - tv[i]) / Math.max(0.0001f, tv[i + 2] - tv[i]);
                return lerp(tv[i + 1], tv[i + 3], smooth(k));
            }
        }
        return tv[tv.length - 1];
    }

    /** same as curve but linear between keys (for constant-speed spins) */
    public static float linear(float t, float... tv) {
        if (t <= tv[0]) return tv[1];
        for (int i = 0; i + 3 < tv.length; i += 2) {
            if (t <= tv[i + 2]) return lerp(tv[i + 1], tv[i + 3], (t - tv[i]) / Math.max(0.0001f, tv[i + 2] - tv[i]));
        }
        return tv[tv.length - 1];
    }
}
