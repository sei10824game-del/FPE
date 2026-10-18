package com.fpe.tools;

import java.awt.image.BufferedImage;
import java.io.ByteArrayOutputStream;
import java.io.File;
import java.nio.file.Files;
import java.util.ArrayList;
import java.util.Base64;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.UUID;

import javax.imageio.ImageIO;

import com.fpe.client.model.AnimCtx;
import com.fpe.client.model.ModelParts;
import com.fpe.client.model.ModelSpec;
import com.fpe.client.spec.Specs;
import com.fpe.entity.Ability;
import com.google.gson.Gson;
import com.google.gson.JsonArray;
import com.google.gson.JsonObject;

import net.minecraft.client.model.geom.ModelPart;

/**
 * One-off bootstrap: converts a procedural ModelSpec (+ its animator sampled per ability) into an editable Blockbench .bbmodel
 * ("Generic Model", per-face UV, texture upscaled K times so detail can be painted).
 * Usage: ./gradlew bbexport -Pspec=miss_circle|all   -> src/main/resources/assets/fpe/bbmodels/NAME.bbmodel
 */
public final class BbExport {
    static final int K = 4;           // texture upscale (nearest neighbour)
    static final int STEP = 2;        // ticks between sampled keyframes
    static final float WALK_CYCLE = 9.4316f;   // limbSwing range of one stride (2*PI / 0.6662)

    public static void main(String[] args) throws Exception {
        try { net.minecraft.SharedConstants.tryDetectVersion(); net.minecraft.server.Bootstrap.bootStrap(); } catch (Throwable t) { System.err.println("bootstrap failed: " + t); }
        String which = args[0];
        File out = new File(args.length > 1 ? args[1] : "src/main/resources/assets/fpe/bbmodels");
        out.mkdirs();
        for (ModelSpec s : Specs.all()) if (which.equals("all") ? Preview.ENTITY.containsKey(s.name) : s.name.equals(which)) {
            Files.writeString(new File(out, s.name + ".bbmodel").toPath(), new Gson().toJson(export(s)));
            System.out.println("wrote " + s.name);
        }
    }

    static String uuid() { return UUID.randomUUID().toString(); }
    static JsonArray arr(double... v) { JsonArray a = new JsonArray(); for (double d : v) a.add(d); return a; }
    static double r(double d) { return Math.round(d * 1000.0) / 1000.0; }

    static String png(int[] argb, int w, int h, boolean glow) throws Exception {
        BufferedImage im = new BufferedImage(w * K, h * K, BufferedImage.TYPE_INT_ARGB);
        for (int y = 0; y < h * K; y++) for (int x = 0; x < w * K; x++) {
            int c = argb[(y / K) * w + x / K];
            if (glow && (c & 0xFFFFFF) == 0) c = 0; // black = no glow -> transparent
            im.setRGB(x, y, c);
        }
        ByteArrayOutputStream bo = new ByteArrayOutputStream();
        ImageIO.write(im, "png", bo);
        return "data:image/png;base64," + Base64.getEncoder().encodeToString(bo.toByteArray());
    }

    static JsonObject texture(String name, String src, String id) {
        JsonObject t = new JsonObject();
        t.addProperty("name", name); t.addProperty("path", ""); t.addProperty("folder", ""); t.addProperty("namespace", ""); t.addProperty("id", id);
        t.addProperty("particle", false); t.addProperty("render_mode", "default"); t.addProperty("render_sides", "auto"); t.addProperty("visible", true);
        t.addProperty("internal", true); t.addProperty("saved", true); t.addProperty("uuid", uuid()); t.addProperty("source", src);
        return t;
    }

    static JsonObject face(double x1, double y1, double x2, double y2) {
        JsonObject f = new JsonObject(); f.add("uv", arr(x1 * K, y1 * K, x2 * K, y2 * K)); f.addProperty("texture", 0); return f;
    }

    static JsonObject export(ModelSpec s) throws Exception {
        s.bake();
        JsonObject doc = new JsonObject();
        JsonObject meta = new JsonObject(); meta.addProperty("format_version", "4.10"); meta.addProperty("model_format", "free"); meta.addProperty("box_uv", false);
        doc.add("meta", meta); doc.addProperty("name", s.name); doc.addProperty("model_identifier", "");
        JsonObject res = new JsonObject(); res.addProperty("width", s.texW * K); res.addProperty("height", s.texH * K); doc.add("resolution", res);

        JsonArray elements = new JsonArray(), outliner = new JsonArray();
        Map<String, JsonObject> groups = new LinkedHashMap<>();
        for (ModelSpec.Part p : s.parts) {
            JsonObject g = new JsonObject();
            g.addProperty("name", p.name); g.add("origin", arr(r(-p.px), r(24 - p.py), r(p.pz)));
            g.add("rotation", arr(r(-Math.toDegrees(p.rx)), r(-Math.toDegrees(p.ry)), r(Math.toDegrees(p.rz))));
            g.addProperty("uuid", uuid()); g.addProperty("color", 0); g.addProperty("export", true);
            JsonArray ch = new JsonArray(); g.add("children", ch);
            groups.put(p.name, g);
            (p.parent == null ? outliner : groups.get(p.parent).getAsJsonArray("children")).add(g);
            if (!p.hasBox) continue;
            JsonObject c = new JsonObject();
            double x0 = -(p.px + p.ox + p.w), x1 = -(p.px + p.ox), y0 = 24 - (p.py + p.oy + p.h), y1 = 24 - (p.py + p.oy), z0 = p.pz + p.oz, z1 = p.pz + p.oz + p.d;
            c.addProperty("name", p.name + "_box"); c.addProperty("type", "cube"); c.addProperty("uuid", uuid()); c.addProperty("box_uv", false); c.addProperty("autouv", 0);
            c.addProperty("inflate", p.inflate); c.add("from", arr(r(x0), r(y0), r(z0))); c.add("to", arr(r(x1), r(y1), r(z1)));
            c.add("origin", arr(r(-p.px), r(24 - p.py), r(p.pz))); c.add("rotation", arr(0, 0, 0));
            double u = p.u, v = p.v, w = Math.ceil(p.w), h = Math.ceil(p.h), d = Math.ceil(p.d);
            JsonObject f = new JsonObject();
            f.add("north", face(u + d, v + d, u + d + w, v + d + h));
            f.add("east", face(u, v + d, u + d, v + d + h));
            f.add("south", face(u + d + w + d, v + d, u + d + w + d + w, v + d + h));
            f.add("west", face(u + d + w, v + d, u + d + w + d, v + d + h));
            f.add("up", face(u + d, v, u + d + w, v + d));
            f.add("down", face(u + d + w, v + d, u + d + w + w, v));   // bottom face is stored v-flipped, like Blockbench does
            c.add("faces", f);
            elements.add(c); ch.add(c.get("uuid").getAsString());
        }
        doc.add("elements", elements); doc.add("outliner", outliner);
        JsonArray texs = new JsonArray();
        texs.add(texture(s.name + ".png", png(s.pixels(), s.texW, s.texH, false), "0"));
        if (s.hasGlow()) texs.add(texture(s.name + "_glow.png", png(s.glowPixels(), s.texW, s.texH, true), "1"));
        doc.add("textures", texs);

        // ---- animations: sample the Java animator
        ModelPart root = s.layerDefinition().bakeRoot();
        ModelParts parts = new ModelParts(root, s);
        parts.resetAll();
        Map<String, float[]> rest = pose(s, parts);
        JsonArray anims = new JsonArray();
        List<Ability> abil = Preview.ENTITY.containsKey(s.name) ? Preview.abilitiesOf(Preview.ENTITY.get(s.name)) : List.of();
        if (s.animator != null) {
            anims.add(animation(s, parts, groups, rest, "idle", 80, true, (c, t) -> c.age = t));
            anims.add(animation(s, parts, groups, rest, "walk", 40, true, (c, t) -> { c.limbSwing = t / 40f * WALK_CYCLE; c.limbAmt = 0.625f; c.age = 0; }));
            for (Ability a : abil) anims.add(animation(s, parts, groups, rest, a.id, a.duration, false, (c, t) -> { c.ability = a.id; c.dur = a.duration; c.t = t; c.age = 20 + t; }));
            anims.add(animation(s, parts, groups, rest, "death", 40, false, (c, t) -> c.death = t / 40f));
        }
        doc.add("animations", anims);
        return doc;
    }

    interface Setup { void set(AnimCtx c, float ticks); }

    static Map<String, float[]> pose(ModelSpec s, ModelParts parts) {
        Map<String, float[]> m = new LinkedHashMap<>();
        for (ModelSpec.Part p : s.parts) {
            ModelPart mp = parts.get(p.name);
            m.put(p.name, new float[] { mp.x, mp.y, mp.z, mp.xRot, mp.yRot, mp.zRot, mp.xScale, mp.yScale, mp.zScale });
        }
        return m;
    }

    static JsonObject animation(ModelSpec s, ModelParts parts, Map<String, JsonObject> groups, Map<String, float[]> rest, String name, int ticks, boolean loop, Setup setup) {
        List<Integer> times = new ArrayList<>();
        for (int t = 0; t < ticks; t += STEP) times.add(t);
        times.add(ticks);
        Map<String, List<float[]>> samples = new LinkedHashMap<>();
        for (int t : times) {
            parts.resetAll();
            AnimCtx c = new AnimCtx(); c.dur = 1; c.age = 5;
            setup.set(c, t);
            s.animator.animate(parts, c);
            for (Map.Entry<String, float[]> e : pose(s, parts).entrySet()) samples.computeIfAbsent(e.getKey(), k -> new ArrayList<>()).add(e.getValue());
        }
        JsonObject an = new JsonObject();
        an.addProperty("uuid", uuid()); an.addProperty("name", name); an.addProperty("loop", loop ? "loop" : "once"); an.addProperty("override", false);
        an.addProperty("length", ticks / 20.0); an.addProperty("snapping", 20); an.addProperty("selected", false);
        an.addProperty("anim_time_update", ""); an.addProperty("blend_weight", ""); an.addProperty("start_delay", ""); an.addProperty("loop_delay", "");
        JsonObject animators = new JsonObject();
        for (Map.Entry<String, List<float[]>> e : samples.entrySet()) {
            float[] r0 = rest.get(e.getKey());
            JsonArray kfs = new JsonArray();
            boolean rot = false, pos = false, scl = false;
            for (float[] v : e.getValue()) {
                rot |= Math.abs(v[3] - r0[3]) + Math.abs(v[4] - r0[4]) + Math.abs(v[5] - r0[5]) > 1e-3;
                pos |= Math.abs(v[0] - r0[0]) + Math.abs(v[1] - r0[1]) + Math.abs(v[2] - r0[2]) > 1e-3;
                scl |= Math.abs(v[6] - r0[6]) + Math.abs(v[7] - r0[7]) + Math.abs(v[8] - r0[8]) > 1e-3;
            }
            for (int i = 0; i < times.size(); i++) {
                float[] v = e.getValue().get(i); double tm = r(times.get(i) / 20.0);
                if (rot) kfs.add(key("rotation", tm, -Math.toDegrees(v[3] - r0[3]), -Math.toDegrees(v[4] - r0[4]), Math.toDegrees(v[5] - r0[5])));
                if (pos) kfs.add(key("position", tm, -(v[0] - r0[0]), -(v[1] - r0[1]), v[2] - r0[2]));
                if (scl) kfs.add(key("scale", tm, v[6], v[7], v[8]));
            }
            if (kfs.isEmpty()) continue;
            JsonObject ao = new JsonObject(); ao.addProperty("name", e.getKey()); ao.addProperty("type", "bone"); ao.add("keyframes", kfs);
            animators.add(groups.get(e.getKey()).get("uuid").getAsString(), ao);
        }
        an.add("animators", animators);
        return an;
    }

    static JsonObject key(String ch, double time, double x, double y, double z) {
        JsonObject k = new JsonObject(); k.addProperty("channel", ch);
        JsonObject d = new JsonObject(); d.addProperty("x", r(x)); d.addProperty("y", r(y)); d.addProperty("z", r(z));
        JsonArray dp = new JsonArray(); dp.add(d); k.add("data_points", dp);
        k.addProperty("uuid", uuid()); k.addProperty("time", time); k.addProperty("color", -1); k.addProperty("interpolation", "linear");
        return k;
    }
}
