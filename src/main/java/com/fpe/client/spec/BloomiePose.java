package com.fpe.client.spec;

import java.util.HashMap;
import java.util.Map;

import com.fpe.client.model.ModelParts;

/**
 * Small pose buffer shared by the two Bloomie specs: joint -> (rotX,rotY,rotZ degrees, moveX,moveY,moveZ px),
 * all ADDED on top of the part's default pose. Lets an ability pose start from the idle pose, be blended in/out
 * and be sampled at an earlier time for secondary (lagging) motion of hair and cloth.
 */
final class BloomiePose {
    final Map<String, float[]> j = new HashMap<>();

    float[] g(String n) { return j.computeIfAbsent(n, k -> new float[6]); }

    /** set rotation */
    BloomiePose r(String n, float x, float y, float z) { float[] a = g(n); a[0] = x; a[1] = y; a[2] = z; return this; }
    /** add rotation */
    BloomiePose ar(String n, float x, float y, float z) { float[] a = g(n); a[0] += x; a[1] += y; a[2] += z; return this; }
    /** set offset */
    BloomiePose mv(String n, float x, float y, float z) { float[] a = g(n); a[3] = x; a[4] = y; a[5] = z; return this; }
    /** add offset */
    BloomiePose am(String n, float x, float y, float z) { float[] a = g(n); a[3] += x; a[4] += y; a[5] += z; return this; }

    float get(String n, int i) { float[] a = j.get(n); return a == null ? 0 : a[i]; }

    BloomiePose copy() { BloomiePose p = new BloomiePose(); j.forEach((k, v) -> p.j.put(k, v.clone())); return p; }

    /** a*(1-w) + b*w for every joint of either pose */
    static BloomiePose lerp(BloomiePose a, BloomiePose b, float w) {
        BloomiePose o = a.copy();
        b.j.forEach((k, v) -> { float[] d = o.g(k); for (int i = 0; i < 6; i++) d[i] = d[i] + (v[i] - d[i]) * w; });
        o.j.forEach((k, d) -> { if (!b.j.containsKey(k)) for (int i = 0; i < 6; i++) d[i] *= (1 - w); });
        return o;
    }

    void apply(ModelParts m) {
        j.forEach((k, a) -> { m.addRot(k, a[0], a[1], a[2]); if (a[3] != 0 || a[4] != 0 || a[5] != 0) m.move(k, a[3], a[4], a[5]); });
    }
}
