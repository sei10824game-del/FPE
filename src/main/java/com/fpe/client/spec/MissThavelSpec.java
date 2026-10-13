package com.fpe.client.spec;

import com.fpe.client.model.Anim;
import com.fpe.client.model.ModelSpec;

/** STUB model. */
public final class MissThavelSpec {
    private MissThavelSpec() {}

    public static final ModelSpec SPEC = build();
    private static ModelSpec build() {
        ModelSpec m = new ModelSpec("miss_thavel");
        m.group("root", null, 0, 24, 0);
        m.part("body", "root", 0, 12, 0, -4, -12, -2, 8, 12, 4, 0x303040);
        m.part("head", "body", 0, 0, 0, -4, -8, -4, 8, 8, 8, 0xC0B0A0);
        m.part("armR", "body", -5, 2, 0, -2, 0, -2, 3, 10, 4, 0x303040);
        m.part("armL", "body", 5, 2, 0, -1, 0, -2, 3, 10, 4, 0x303040);
        m.part("legR", "root", -2, 12, 0, -2, 0, -2, 4, 12, 4, 0x202030);
        m.part("legL", "root", 2, 12, 0, -2, 0, -2, 4, 12, 4, 0x202030);
        m.animator((p, c) -> { p.rot("legR", Anim.sinr(c.limbSwing * 0.6f) * 40 * c.walk(), 0, 0); p.rot("legL", -Anim.sinr(c.limbSwing * 0.6f) * 40 * c.walk(), 0, 0); });
        return m;
    }
}
