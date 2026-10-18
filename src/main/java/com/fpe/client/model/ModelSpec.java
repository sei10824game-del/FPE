package com.fpe.client.model;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

import com.fpe.FpeMod;

import net.minecraft.client.model.geom.ModelLayerLocation;
import net.minecraft.client.model.geom.PartPose;
import net.minecraft.client.model.geom.builders.CubeDeformation;
import net.minecraft.client.model.geom.builders.CubeListBuilder;
import net.minecraft.client.model.geom.builders.LayerDefinition;
import net.minecraft.client.model.geom.builders.MeshDefinition;
import net.minecraft.client.model.geom.builders.PartDefinition;
import net.minecraft.resources.ResourceLocation;

/**
 * Single source of truth for a procedural model: geometry + painted texture + animation.
 * Coordinates follow vanilla humanoid convention: +x = entity's LEFT, +y = DOWN, entity faces -z,
 * y=24 is the ground. Pivots are ABSOLUTE model-space (converted to parent-relative automatically).
 * One pixel = 1/16 block. Parent must be declared before child.
 */
public final class ModelSpec {
    public enum Face { TOP, BOTTOM, RIGHT, FRONT, LEFT, BACK }
    public enum Pattern { SOLID, STRIPE_H, STRIPE_V, DIAG, CHECK, GRADIENT_V }

    public static final class Decor {
        public final Face face; public final int x, y, w, h, color; public final boolean glow;
        Decor(Face f, int x, int y, int w, int h, int c, boolean g) { face = f; this.x = x; this.y = y; this.w = w; this.h = h; color = c; glow = g; }
    }

    public static final class Part {
        public final String name, parent;
        public float px, py, pz, rx, ry, rz;
        public float ox, oy, oz, w, h, d, inflate;
        public boolean hasBox, glow, mirror;
        public int color = 0x808080, color2 = 0x404040, period = 2;
        public float grain = 0.06f;
        public Pattern pattern = Pattern.SOLID;
        public int u, v;
        /** per-face UV in texture pixels, order north,east,south,west,up,down (each {x1,y1,x2,y2}); null = vanilla box UV from u/v */
        public float[][] faceUv;
        public final List<Decor> decor = new ArrayList<>();
        Part(String name, String parent) { this.name = name; this.parent = parent; }

        /** default rotation in DEGREES */
        public Part rot(float xDeg, float yDeg, float zDeg) { rx = (float) Math.toRadians(xDeg); ry = (float) Math.toRadians(yDeg); rz = (float) Math.toRadians(zDeg); return this; }
        public Part inflate(float i) { inflate = i; return this; }
        public Part grain(float g) { grain = g; return this; }
        public Part glow() { glow = true; return this; }
        public Part mirror() { mirror = true; return this; }
        public Part pattern(Pattern p, int color2, int period) { pattern = p; this.color2 = color2; this.period = Math.max(1, period); return this; }
        /** paint a rectangle on one face (face-local pixels, (0,0)=top-left as seen from outside). */
        public Part decor(Face f, int x, int y, int w, int h, int color) { decor.add(new Decor(f, x, y, w, h, color, false)); return this; }
        public Part decorGlow(Face f, int x, int y, int w, int h, int color) { decor.add(new Decor(f, x, y, w, h, color, true)); return this; }
    }

    public final String name;
    public final List<Part> parts = new ArrayList<>();
    private final Map<String, Part> byName = new LinkedHashMap<>();
    public int texW = 256, texH;
    public float shadow = 0.6f;
    /** animation; may be null */
    public Animator animator;
    private int[] pixels, glowPixels;
    private boolean baked, externalGlow;

    public ModelSpec(String name) { this.name = name; }

    public ModelSpec shadow(float s) { shadow = s; return this; }
    public ModelSpec animator(Animator a) { animator = a; return this; }

    /** Box part. (px,py,pz)=pivot, (ox,oy,oz)=box corner relative to pivot, (w,h,d)=size. */
    public Part part(String name, String parent, float px, float py, float pz, float ox, float oy, float oz, float w, float h, float d, int color) {
        Part p = group(name, parent, px, py, pz);
        p.ox = ox; p.oy = oy; p.oz = oz; p.w = w; p.h = h; p.d = d; p.color = color; p.hasBox = true;
        return p;
    }

    /** Empty pivot node (no geometry). */
    public Part group(String name, String parent, float px, float py, float pz) {
        if (byName.containsKey(name)) throw new IllegalArgumentException("dup part " + name + " in " + this.name);
        if (parent != null && !byName.containsKey(parent)) throw new IllegalArgumentException("parent " + parent + " missing for " + name);
        Part p = new Part(name, parent);
        p.px = px; p.py = py; p.pz = pz;
        parts.add(p); byName.put(name, p);
        return p;
    }

    public Part get(String n) { return byName.get(n); }

    public ResourceLocation texture() { return new ResourceLocation(FpeMod.MODID, "dyn/" + name); }
    public ResourceLocation glowTexture() { return new ResourceLocation(FpeMod.MODID, "dyn/" + name + "_glow"); }
    public ModelLayerLocation layer() { return new ModelLayerLocation(new ResourceLocation(FpeMod.MODID, name), "main"); }
    public boolean hasGlow() { if (externalGlow) return true; for (Part p : parts) { if (p.glow) return true; for (Decor d : p.decor) if (d.glow) return true; } return false; }

    /** path of part names from root (for ModelPart.getChild chain). */
    public List<String> path(String n) {
        List<String> r = new ArrayList<>();
        for (Part p = byName.get(n); p != null; p = p.parent == null ? null : byName.get(p.parent)) r.add(0, p.name);
        return r;
    }

    // ---------------------------------------------------------------- packing & painting
    /** use ready-made pixels (e.g. from a .bbmodel); parts must already have u/v set. glow may be null. */
    public synchronized ModelSpec external(int[] argb, int[] glowArgb, int w, int h) {
        texW = w; texH = h; pixels = argb;
        externalGlow = glowArgb != null;
        glowPixels = glowArgb != null ? glowArgb : new int[w * h];
        if (glowArgb == null) java.util.Arrays.fill(glowPixels, 0xFF000000);
        baked = true;
        return this;
    }

    public synchronized ModelSpec bake() {
        if (baked) return this;
        int cx = 0, cy = 0, rowH = 0;
        for (Part p : parts) {
            if (!p.hasBox) continue;
            int w = (int) Math.ceil(p.w), h = (int) Math.ceil(p.h), d = (int) Math.ceil(p.d);
            int rw = 2 * (d + w), rh = d + h;
            if (cx + rw > texW) { cx = 0; cy += rowH; rowH = 0; }
            p.u = cx; p.v = cy; cx += rw; rowH = Math.max(rowH, rh);
        }
        texH = Math.max(16, ((cy + rowH + 15) / 16) * 16);
        pixels = new int[texW * texH];
        glowPixels = new int[texW * texH];
        for (int i = 0; i < pixels.length; i++) glowPixels[i] = 0xFF000000;
        int idx = 0;
        for (Part p : parts) { if (p.hasBox) paint(p, idx); idx++; }
        baked = true;
        return this;
    }

    /** ARGB pixels (texW*texH). */
    public int[] pixels() { bake(); return pixels; }
    public int[] glowPixels() { bake(); return glowPixels; }

    private static int hash(int a, int b, int c) {
        int h = a * 374761393 + b * 668265263 + c * 2147483647;
        h = (h ^ (h >>> 13)) * 1274126177;
        return h ^ (h >>> 16);
    }

    private static int shade(int rgb, float m) {
        int r = Math.min(255, Math.max(0, Math.round(((rgb >> 16) & 255) * m)));
        int g = Math.min(255, Math.max(0, Math.round(((rgb >> 8) & 255) * m)));
        int b = Math.min(255, Math.max(0, Math.round((rgb & 255) * m)));
        return 0xFF000000 | r << 16 | g << 8 | b;
    }

    private static int mix(int a, int b, float t) {
        int r = Math.round(((a >> 16) & 255) * (1 - t) + ((b >> 16) & 255) * t);
        int g = Math.round(((a >> 8) & 255) * (1 - t) + ((b >> 8) & 255) * t);
        int bl = Math.round((a & 255) * (1 - t) + (b & 255) * t);
        return 0xFF000000 | r << 16 | g << 8 | bl;
    }

    private void paint(Part p, int idx) {
        int w = (int) Math.ceil(p.w), h = (int) Math.ceil(p.h), d = (int) Math.ceil(p.d);
        for (Face f : Face.values()) {
            int fw, fh, fx0, fy0; float sh;
            switch (f) {
                case TOP -> { fw = w; fh = d; fx0 = d; fy0 = 0; sh = 1.15f; }
                case BOTTOM -> { fw = w; fh = d; fx0 = d + w; fy0 = 0; sh = 0.6f; }
                case RIGHT -> { fw = d; fh = h; fx0 = 0; fy0 = d; sh = 0.88f; }
                case FRONT -> { fw = w; fh = h; fx0 = d; fy0 = d; sh = 1.0f; }
                case LEFT -> { fw = d; fh = h; fx0 = d + w; fy0 = d; sh = 0.88f; }
                default -> { fw = w; fh = h; fx0 = d + w + d; fy0 = d; sh = 0.78f; }
            }
            for (int y = 0; y < fh; y++) for (int x = 0; x < fw; x++) {
                int base = switch (p.pattern) {
                    case SOLID -> p.color;
                    case STRIPE_H -> ((y / p.period) & 1) == 0 ? p.color : p.color2;
                    case STRIPE_V -> ((x / p.period) & 1) == 0 ? p.color : p.color2;
                    case DIAG -> (((x + y) / p.period) & 1) == 0 ? p.color : p.color2;
                    case CHECK -> (((x / p.period) + (y / p.period)) & 1) == 0 ? p.color : p.color2;
                    case GRADIENT_V -> mix(p.color, p.color2, fh <= 1 ? 0 : (float) y / (fh - 1));
                };
                float n = 1f + ((hash(idx, fx0 + x, fy0 + y + f.ordinal() * 97) & 255) / 255f - 0.5f) * 2f * p.grain;
                put(p.u + fx0 + x, p.v + fy0 + y, shade(base, sh * n), p.glow ? 0xFF000000 | base : 0xFF000000);
            }
            for (Decor dc : p.decor) {
                if (dc.face != f) continue;
                for (int y = dc.y; y < dc.y + dc.h; y++) for (int x = dc.x; x < dc.x + dc.w; x++) {
                    if (x < 0 || y < 0 || x >= fw || y >= fh) continue;
                    put(p.u + fx0 + x, p.v + fy0 + y, 0xFF000000 | dc.color, dc.glow ? 0xFF000000 | dc.color : glowPixels[(p.v + fy0 + y) * texW + p.u + fx0 + x]);
                }
            }
        }
    }

    private void put(int x, int y, int argb, int glowArgb) {
        if (x < 0 || y < 0 || x >= texW || y >= texH) return;
        pixels[y * texW + x] = argb;
        glowPixels[y * texW + x] = glowArgb;
    }

    // ---------------------------------------------------------------- vanilla layer
    public LayerDefinition layerDefinition() {
        bake();
        MeshDefinition mesh = new MeshDefinition();
        Map<String, PartDefinition> defs = new LinkedHashMap<>();
        PartDefinition root = mesh.getRoot();
        for (Part p : parts) {
            PartDefinition parentDef = p.parent == null ? root : defs.get(p.parent);
            Part par = p.parent == null ? null : byName.get(p.parent);
            float ax = par == null ? 0 : par.px, ay = par == null ? 0 : par.py, az = par == null ? 0 : par.pz;
            CubeListBuilder b = CubeListBuilder.create();
            if (p.hasBox) {
                b.texOffs(p.u, p.v).mirror(p.mirror).addBox(p.ox, p.oy, p.oz, p.w, p.h, p.d, new CubeDeformation(p.inflate));
            }
            defs.put(p.name, parentDef.addOrReplaceChild(p.name, b, PartPose.offsetAndRotation(p.px - ax, p.py - ay, p.pz - az, p.rx, p.ry, p.rz)));
        }
        return LayerDefinition.create(mesh, texW, texH);
    }
}
