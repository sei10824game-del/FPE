package com.fpe.client.spec;

import java.util.EnumMap;
import java.util.Map;

import com.fpe.client.model.ModelSpec;
import com.fpe.client.model.ModelSpec.Face;
import com.fpe.client.model.ModelSpec.Pattern;
import com.fpe.entity.FpeProjectile.Kind;

/** One tiny model per projectile kind. Authored around the pivot (0,0,0); forward = -z. 1px = 1/16 block. */
public final class ProjectileSpecs {
    private ProjectileSpecs() {}

    private static final Map<Kind, ModelSpec> MAP = new EnumMap<>(Kind.class);

    public static ModelSpec get(Kind k) { return MAP.get(k); }
    public static Iterable<ModelSpec> all() { return MAP.values(); }

    private static ModelSpec spec(Kind k) { ModelSpec s = new ModelSpec("proj_" + k.name().toLowerCase()); s.shadow(0f); MAP.put(k, s); s.group("root", null, 0, 0, 0); return s; }

    static {
        // compass: two long steel legs joined by a hinge, drawn as a V, spins like a boomerang
        ModelSpec s = spec(Kind.COMPASS);
        s.part("hinge", "root", 0, 0, 0, -1.5f, -1.5f, -1.5f, 3, 3, 3, 0x6E7480);
        s.part("legA", "root", 0, 0, 0, -0.5f, -0.5f, -14, 1, 1, 14, 0xC9CED6).rot(0, -16, 0).grain(0.1f);
        s.part("legB", "root", 0, 0, 0, -0.5f, -0.5f, -14, 1, 1, 14, 0xAEB4BE).rot(0, 16, 0).grain(0.1f);
        s.part("tipA", "root", 0, 0, 0, -0.5f, -0.5f, -17, 1, 1, 3, 0x30333A).rot(0, -16, 0);
        s.part("tipB", "root", 0, 0, 0, -0.5f, -0.5f, -17, 1, 1, 3, 0xB02030).rot(0, 16, 0).glow();
        s.part("bar", "root", 0, 0, 0, -1, -1, 0, 2, 2, 5, 0x3A3D46);

        // pencil dart
        s = spec(Kind.PENCIL);
        s.part("shaft", "root", 0, 0, 0, -1, -1, -8, 2, 2, 14, 0xE8C040).pattern(Pattern.STRIPE_H, 0xD0A828, 1);
        s.part("wood", "root", 0, 0, 0, -1, -1, -11, 2, 2, 3, 0xE8CFA0);
        s.part("lead", "root", 0, 0, 0, -0.5f, -0.5f, -13, 1, 1, 2, 0x25252B);
        s.part("eraser", "root", 0, 0, 0, -1, -1, 6, 2, 2, 2, 0xE06A80);
        s.part("band", "root", 0, 0, 0, -1.1f, -1.1f, 4, 2.2f, 2.2f, 2, 0xB8BCC4);

        // grenade
        s = spec(Kind.GRENADE);
        s.part("body", "root", 0, 0, 0, -2.5f, -3, -2.5f, 5, 6, 5, 0x4E5A34).pattern(Pattern.CHECK, 0x435029, 1);
        s.part("neck", "root", 0, 0, 0, -1.5f, -4.5f, -1.5f, 3, 1.5f, 3, 0x8A8F8A);
        s.part("lever", "root", 0, 0, 0, 1.5f, -5, -0.5f, 1, 3, 1, 0xB8BCB8);
        s.part("pin", "root", 0, 0, 0, -3, -5, -0.5f, 1.5f, 1.5f, 1, 0xE0B030).glow();

        // bomblet
        s = spec(Kind.BOMBLET);
        s.part("body", "root", 0, 0, 0, -1.5f, -2, -1.5f, 3, 4, 3, 0x6A4B2A).pattern(Pattern.STRIPE_H, 0x4A3320, 1);
        s.part("fuse", "root", 0, 0, 0, -0.5f, -3.5f, -0.5f, 1, 1.5f, 1, 0xFFB030).glow();

        // rocket
        s = spec(Kind.ROCKET);
        s.part("tube", "root", 0, 0, 0, -1.5f, -1.5f, -7, 3, 3, 12, 0x6C7078);
        s.part("nose", "root", 0, 0, 0, -1, -1, -10, 2, 2, 3, 0xB03020);
        s.part("fin1", "root", 0, 0, 0, -3.5f, -0.25f, 2, 7, 0.5f, 3, 0x40434A);
        s.part("fin2", "root", 0, 0, 0, -0.25f, -3.5f, 2, 0.5f, 7, 3, 0x40434A);
        s.part("flame", "root", 0, 0, 0, -1, -1, 5, 2, 2, 4, 0xFFA030).glow();

        // bullet
        s = spec(Kind.BULLET);
        s.part("slug", "root", 0, 0, 0, -0.5f, -0.5f, -3, 1, 1, 6, 0xFFE070).glow();
        s.part("core", "root", 0, 0, 0, -0.25f, -0.25f, -5, 0.5f, 0.5f, 10, 0xFFFFFF).glow();

        // shadow orb
        s = spec(Kind.SHADOW_ORB);
        s.part("core", "root", 0, 0, 0, -3, -3, -3, 6, 6, 6, 0x0A0610).grain(0.05f);
        s.part("shell", "root", 0, 0, 0, -4, -4, -4, 8, 8, 8, 0x1A1024).inflate(0f).rot(45, 45, 0);
        s.part("eye", "root", 0, 0, 0, -1.5f, -1.5f, -3.2f, 3, 3, 1, 0xFF2040).glow();
        s.part("spikeA", "root", 0, 0, 0, -0.5f, -7, -0.5f, 1, 14, 1, 0x1A1024).rot(0, 0, 25);
        s.part("spikeB", "root", 0, 0, 0, -0.5f, -7, -0.5f, 1, 14, 1, 0x1A1024).rot(25, 0, 0);

        // diamond shard
        s = spec(Kind.DIAMOND);
        s.part("d", "root", 0, 0, 0, -2.5f, -2.5f, -0.5f, 5, 5, 1, 0xF4F4FF).rot(0, 0, 45).glow();
        s.part("d2", "root", 0, 0, 0, -1.5f, -1.5f, -0.75f, 3, 3, 1.5f, 0xBFD6FF).rot(0, 0, 45).glow();

        // axe
        s = spec(Kind.AXE);
        s.part("handle", "root", 0, 0, 0, -0.75f, -9, -0.75f, 1.5f, 15, 1.5f, 0x6B4423).pattern(Pattern.STRIPE_H, 0x593819, 2);
        s.part("head", "root", 0, 0, 0, -0.75f, -9, -0.75f, 1.5f, 5, 7, 0x9AA0A8).grain(0.1f);
        s.part("edge", "root", 0, 0, 0, -0.5f, -9.5f, 5.5f, 1, 6, 2, 0xD8DCE2);
        s.part("blood", "root", 0, 0, 0, -0.6f, -8, 3, 1.2f, 2, 2, 0x7A1010);

        // knife
        s = spec(Kind.KNIFE);
        s.part("blade", "root", 0, 0, 0, -0.5f, -1.5f, -9, 1, 3, 10, 0xD0D4DA);
        s.part("guard", "root", 0, 0, 0, -0.75f, -2, 1, 1.5f, 4, 1, 0x3A3A40);
        s.part("grip", "root", 0, 0, 0, -1, -1.25f, 2, 2, 2.5f, 5, 0x3A2A22);

        // ABC block
        s = spec(Kind.ABC_BLOCK);
        s.part("cube", "root", 0, 0, 0, -4, -4, -4, 8, 8, 8, 0xE8D9B0).grain(0.08f)
                .decor(Face.FRONT, 2, 1, 4, 1, 0x3A2A55).decor(Face.FRONT, 2, 3, 4, 1, 0x3A2A55).decor(Face.FRONT, 2, 5, 4, 1, 0x3A2A55).decor(Face.FRONT, 2, 1, 1, 5, 0x3A2A55)
                .decor(Face.BACK, 2, 1, 4, 1, 0x3A2A55).decor(Face.BACK, 2, 6, 4, 1, 0x3A2A55).decor(Face.BACK, 2, 1, 1, 6, 0x3A2A55).decor(Face.BACK, 5, 1, 1, 6, 0x3A2A55)
                .decor(Face.TOP, 3, 3, 2, 2, 0xC05050).decor(Face.LEFT, 3, 3, 2, 2, 0x5070C0);

        // blade wave (crescent made from stacked slabs)
        s = spec(Kind.BLADE_WAVE);
        s.part("mid", "root", 0, 0, 0, -9, -0.5f, -1, 18, 1, 2, 0xF0F0FF).glow();
        s.part("l", "root", 0, 0, 0, -9, -0.5f, -1, 7, 1, 2, 0xDDE0FF).rot(0, 35, 0).glow();
        s.part("r", "root", 0, 0, 0, 2, -0.5f, -1, 7, 1, 2, 0xDDE0FF).rot(0, -35, 0).glow();

        // fireball
        s = spec(Kind.FIREBALL);
        s.part("core", "root", 0, 0, 0, -3, -3, -3, 6, 6, 6, 0xFFB030).glow();
        s.part("outer", "root", 0, 0, 0, -4, -4, -4, 8, 8, 8, 0xE04A10).rot(45, 45, 0).glow();
    }
}
