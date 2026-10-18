package com.fpe.tools;

import java.awt.Color;
import java.awt.Font;
import java.awt.Graphics2D;
import java.awt.image.BufferedImage;
import java.io.File;
import java.lang.reflect.Field;
import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Map;

import javax.imageio.ImageIO;

import com.fpe.client.model.AnimCtx;
import com.fpe.client.model.ModelParts;
import com.fpe.client.model.ModelSpec;
import com.fpe.client.spec.ProjectileSpecs;
import com.fpe.client.spec.Specs;
import com.fpe.entity.Ability;
import com.fpe.entity.FpeEntity;
import com.fpe.entity.characters.*;
import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.blaze3d.vertex.VertexConsumer;

import net.minecraft.client.model.geom.ModelPart;

/**
 * Headless model/animation previewer (no GL): renders the REAL ModelPart geometry + procedural texture with a tiny
 * software rasterizer.   ./gradlew preview -Pspec=miss_circle [-Pout=build/preview]
 * Writes build/preview/<spec>.png (poses) and build/preview/<spec>_tex.png (texture atlas).
 * Rows: idle views (front/3-4/side/back) + walk, then one row per ability sampled over its duration.
 */
public final class Preview {
    private static final class Quad { float[] x = new float[4], y = new float[4], z = new float[4], u = new float[4], v = new float[4]; }

    private static final class Collector implements VertexConsumer {
        final List<Quad> quads = new ArrayList<>();
        Quad cur = new Quad(); int n;
        float px, py, pz, pu, pv;
        @Override public VertexConsumer vertex(double x, double y, double z) { px = (float) x; py = (float) y; pz = (float) z; return this; }
        @Override public VertexConsumer color(int r, int g, int b, int a) { return this; }
        @Override public VertexConsumer uv(float u, float v) { pu = u; pv = v; return this; }
        @Override public VertexConsumer overlayCoords(int u, int v) { return this; }
        @Override public VertexConsumer uv2(int u, int v) { return this; }
        @Override public VertexConsumer normal(float x, float y, float z) { return this; }
        @Override public void endVertex() {
            cur.x[n] = px; cur.y[n] = py; cur.z[n] = pz; cur.u[n] = pu; cur.v[n] = pv;
            if (++n == 4) { quads.add(cur); cur = new Quad(); n = 0; }
        }
        @Override public void defaultColor(int r, int g, int b, int a) { }
        @Override public void unsetDefaultColor() { }
    }

    static final Map<String, Class<? extends FpeEntity>> ENTITY = new java.util.HashMap<>(Map.of(
            "miss_circle", MissCircle.class, "miss_thavel", MissThavel.class, "miss_bloomie", MissBloomie.class,
            "alice", Alice.class, "alice_boss", Alice.class, "red_circle", RedCircle.class,
            "danger_thavel", DangerThavel.class, "danger_bloomie", DangerBloomie.class,  "fen", Fen.class, "aiden", Aiden.class));

    static { ENTITY.put("green_circle", GreenCircle.class); ENTITY.put("hansel_juvenile", HanselJuvenile.class); ENTITY.put("lord_hansel", LordHansel.class); ENTITY.put("lord_hansel_premature", LordHansel.class); ENTITY.put("lord_hansel_true", LordHansel.class); ENTITY.put("mutant_claire", MutantClaire.class); ENTITY.put("mutant_engel", MutantEngel.class); ENTITY.put("mutant_bubble", MutantBubble.class); ENTITY.put("mutant_lana", MutantLana.class); ENTITY.put("mutant_abbie", MutantAbbie.class); ENTITY.put("green_thavel", GreenThavel.class); ENTITY.put("green_bloomie", GreenBloomie.class); ENTITY.put("green_alice", GreenAlice.class); ENTITY.put("green_alice_boss", GreenAlice.class); ENTITY.put("danger_alice_boss", DangerAlice.class); ENTITY.put("infected_bloomie", InfectedBloomie.class); ENTITY.put("infected_zip", InfectedZip.class); ENTITY.put("danger_alice", DangerAlice.class); }

    @SuppressWarnings("unchecked")
    static List<Ability> abilitiesOf(Class<? extends FpeEntity> c) throws Exception {
        Field uf = Class.forName("sun.misc.Unsafe").getDeclaredField("theUnsafe");
        uf.setAccessible(true);
        Object unsafe = uf.get(null);
        Method alloc = unsafe.getClass().getMethod("allocateInstance", Class.class);
        Object e = alloc.invoke(unsafe, c);
        Method m = FpeEntity.class.getDeclaredMethod("abilities");
        m.setAccessible(true);
        return (List<Ability>) m.invoke(e);
    }

    public static void main(String[] args) throws Exception {
        try { net.minecraft.SharedConstants.tryDetectVersion(); net.minecraft.server.Bootstrap.bootStrap(); } catch (Throwable t) { System.err.println("bootstrap failed: " + t); }
        String which = args.length > 0 ? args[0] : "all";
        File out = new File(args.length > 1 ? args[1] : "build/preview");
        out.mkdirs();
        List<ModelSpec> specs = new ArrayList<>();
        for (ModelSpec s : Specs.all()) if (which.equals("all") || s.name.equals(which) || (which.equals("proj") && s.name.startsWith("proj_")) || (which.equals("fx") && s.name.startsWith("fx_"))) specs.add(s);
        if (specs.isEmpty()) { System.err.println("no spec " + which); return; }
        for (ModelSpec s : specs) {
            s.bake();
            ImageIO.write(texImage(s), "png", new File(out, s.name + "_tex.png"));
            ImageIO.write(sheet(s), "png", new File(out, s.name + ".png"));
            System.out.println("wrote " + new File(out, s.name + ".png") + " (tex " + s.texW + "x" + s.texH + ", parts " + s.parts.size() + ")");
        }
    }

    static BufferedImage texImage(ModelSpec s) {
        BufferedImage im = new BufferedImage(s.texW, s.texH, BufferedImage.TYPE_INT_ARGB);
        im.setRGB(0, 0, s.texW, s.texH, s.pixels(), 0, s.texW);
        BufferedImage big = new BufferedImage(s.texW * 3, s.texH * 3, BufferedImage.TYPE_INT_ARGB);
        Graphics2D g = big.createGraphics();
        g.setColor(new Color(60, 60, 70)); g.fillRect(0, 0, big.getWidth(), big.getHeight());
        g.drawImage(im, 0, 0, big.getWidth(), big.getHeight(), null);
        g.dispose();
        return big;
    }

    static final int FW = 170, FH = 250;

    static BufferedImage sheet(ModelSpec s) throws Exception {
        ModelPart root = s.layerDefinition().bakeRoot();
        ModelParts parts = new ModelParts(root, s);
        Class<? extends FpeEntity> ec = ENTITY.get(s.name);
        List<Ability> abil = ec == null ? List.of() : abilitiesOf(ec);
        int variant = s.name.equals("alice_boss") || s.name.equals("danger_alice_boss") || s.name.equals("green_alice_boss") || Integer.getInteger("fpe.variant", 0) == 1 ? 1 : 0;

        // framing from idle pose
        float[] bb = bounds(root, parts, s, 0, 0, null);
        float height = Math.max(24f, bb[3] - bb[2]);
        float scale = (FH - 40) / (height * 1.15f);
        float groundY = FH - 22;

        List<String> labels = new ArrayList<>();
        List<List<BufferedImage>> rows = new ArrayList<>();
        // row 0: idle views
        List<BufferedImage> row = new ArrayList<>();
        for (int yaw : new int[] {0, 40, 90, 180}) row.add(frame(root, parts, s, yaw, scale, groundY, idleCtx(variant, 0f, 0f), "idle " + yaw));
        AnimCtx w = idleCtx(variant, 0f, 0f); w.limbSwing = 3.1f; w.limbAmt = 0.8f; w.age = 10;
        row.add(frame(root, parts, s, 40, scale, groundY, w, "walk"));
        AnimCtx wa = idleCtx(variant, 0f, 0f); wa.limbSwing = 5.2f; wa.limbAmt = 0.8f; wa.age = 14;
        row.add(frame(root, parts, s, 40, scale, groundY, wa, "walk2"));
        rows.add(row);
        for (Ability a : abil) {
            row = new ArrayList<>();
            int n = 6;
            for (int i = 0; i < n; i++) {
                AnimCtx c = idleCtx(variant, 0f, 0f);
                c.ability = a.id; c.dur = a.duration; c.t = a.duration * (i / (float) (n - 1)) * 0.98f; c.age = 20 + c.t;
                row.add(frame(root, parts, s, i % 2 == 0 ? 40 : 70, scale, groundY, c, a.id + " t=" + (int) c.t + "/" + a.duration));
            }
            rows.add(row);
        }
        // death row
        row = new ArrayList<>();
        for (int i = 0; i < 4; i++) { AnimCtx c = idleCtx(variant, 0f, 0f); c.death = i / 3f; row.add(frame(root, parts, s, 40, scale, groundY, c, "death " + i / 3f)); }
        rows.add(row);

        int cols = rows.stream().mapToInt(List::size).max().orElse(1);
        BufferedImage img = new BufferedImage(cols * FW, rows.size() * FH, BufferedImage.TYPE_INT_ARGB);
        Graphics2D g = img.createGraphics();
        for (int r = 0; r < rows.size(); r++) for (int c = 0; c < rows.get(r).size(); c++) g.drawImage(rows.get(r).get(c), c * FW, r * FH, null);
        g.dispose();
        return img;
    }

    static AnimCtx idleCtx(int variant, float a, float b) { AnimCtx c = new AnimCtx(); c.variant = variant; c.dur = 1; c.age = 5; return c; }

    static float[] bounds(ModelPart root, ModelParts parts, ModelSpec s, int yaw, int pitch, AnimCtx c) {
        parts.resetAll();
        if (s.animator != null) s.animator.animate(parts, c == null ? idleCtx(0, 0, 0) : c);
        Collector col = new Collector();
        root.render(new PoseStack(), col, 0xF000F0, 0, 1f, 1f, 1f, 1f);
        float minX = 1e9f, maxX = -1e9f, minY = 1e9f, maxY = -1e9f;
        for (Quad q : col.quads) for (int i = 0; i < 4; i++) { minX = Math.min(minX, q.x[i]); maxX = Math.max(maxX, q.x[i]); minY = Math.min(minY, q.y[i]); maxY = Math.max(maxY, q.y[i]); }
        // model space: units of 1/16 block already divided; convert back to px
        return new float[] {minX * 16, maxX * 16, minY * 16, maxY * 16};
    }

    static BufferedImage frame(ModelPart root, ModelParts parts, ModelSpec s, int yawDeg, float scale, float groundY, AnimCtx c, String label) {
        parts.resetAll();
        if (s.animator != null) s.animator.animate(parts, c);
        Collector col = new Collector();
        root.render(new PoseStack(), col, 0xF000F0, 0, 1f, 1f, 1f, 1f);
        BufferedImage im = new BufferedImage(FW, FH, BufferedImage.TYPE_INT_ARGB);
        Graphics2D g = im.createGraphics();
        g.setColor(new Color(38, 40, 50)); g.fillRect(0, 0, FW, FH);
        g.setColor(new Color(70, 74, 88)); g.fillRect(0, (int) groundY, FW, FH - (int) groundY);
        g.setColor(Color.WHITE); g.setFont(new Font("SansSerif", Font.PLAIN, 10)); g.drawString(label, 4, 12);
        g.dispose();

        double a = Math.toRadians(yawDeg), ca = Math.cos(a), sa = Math.sin(a);
        float k = scale * 16f; // model coords are px/16 -> px
        List<float[]> tris = new ArrayList<>();
        class P { Quad q; float depth; float[] sx = new float[4], sy = new float[4]; }
        List<P> ps = new ArrayList<>();
        // model y=24 px (1.5) is ground; shift so ground is at groundY
        for (Quad q : col.quads) {
            P p = new P(); p.q = q; float d = 0;
            for (int i = 0; i < 4; i++) {
                float x = q.x[i], z = q.z[i], y = q.y[i];
                float rx = (float) (x * ca + z * sa), rz = (float) (-x * sa + z * ca);
                p.sx[i] = FW / 2f + rx * k;
                p.sy[i] = groundY + (y - 1.5f) * k;
                d += rz;
            }
            p.depth = d / 4f;
            // backface cull (screen-space winding)
            float area = 0;
            for (int i = 0; i < 4; i++) { int j = (i + 1) % 4; area += p.sx[i] * p.sy[j] - p.sx[j] * p.sy[i]; }
            if (area > 0) continue;
            ps.add(p);
        }
        ps.sort(Comparator.comparingDouble(p -> -p.depth)); // far first (larger rz = farther? camera looks along -z after rotation)
        int[] pix = im.getRGB(0, 0, FW, FH, null, 0, FW);
        int[] tex = s.pixels(), glow = s.glowPixels();
        for (P p : ps) {
            raster(pix, tex, glow, s.texW, s.texH, p.sx[0], p.sy[0], p.q.u[0], p.q.v[0], p.sx[1], p.sy[1], p.q.u[1], p.q.v[1], p.sx[2], p.sy[2], p.q.u[2], p.q.v[2]);
            raster(pix, tex, glow, s.texW, s.texH, p.sx[0], p.sy[0], p.q.u[0], p.q.v[0], p.sx[2], p.sy[2], p.q.u[2], p.q.v[2], p.sx[3], p.sy[3], p.q.u[3], p.q.v[3]);
        }
        im.setRGB(0, 0, FW, FH, pix, 0, FW);
        g = im.createGraphics();
        g.setColor(Color.WHITE); g.setFont(new Font("SansSerif", Font.PLAIN, 10)); g.drawString(label, 4, 12);
        g.dispose();
        return im;
    }

    private static void raster(int[] pix, int[] tex, int[] glow, int tw, int th, float x0, float y0, float u0, float v0, float x1, float y1, float u1, float v1, float x2, float y2, float u2, float v2) {
        int minX = Math.max(0, (int) Math.floor(Math.min(x0, Math.min(x1, x2)))), maxX = Math.min(FW - 1, (int) Math.ceil(Math.max(x0, Math.max(x1, x2))));
        int minY = Math.max(0, (int) Math.floor(Math.min(y0, Math.min(y1, y2)))), maxY = Math.min(FH - 1, (int) Math.ceil(Math.max(y0, Math.max(y1, y2))));
        float den = (y1 - y2) * (x0 - x2) + (x2 - x1) * (y0 - y2);
        if (Math.abs(den) < 1e-6f) return;
        for (int y = minY; y <= maxY; y++) for (int x = minX; x <= maxX; x++) {
            float px = x + 0.5f, py = y + 0.5f;
            float l0 = ((y1 - y2) * (px - x2) + (x2 - x1) * (py - y2)) / den;
            float l1 = ((y2 - y0) * (px - x2) + (x0 - x2) * (py - y2)) / den;
            float l2 = 1 - l0 - l1;
            if (l0 < -0.02f || l1 < -0.02f || l2 < -0.02f) continue;
            float u = (l0 * u0 + l1 * u1 + l2 * u2) * tw, v = (l0 * v0 + l1 * v1 + l2 * v2) * th;
            int tx = Math.min(tw - 1, Math.max(0, (int) Math.floor(u))), ty = Math.min(th - 1, Math.max(0, (int) Math.floor(v)));
            int c = tex[ty * tw + tx];
            if ((c >>> 24) < 128) continue;
            int gl = glow[ty * tw + tx] & 0xFFFFFF;
            if (gl != 0) c = 0xFF000000 | gl;
            pix[y * FW + x] = c;
        }
    }
}
