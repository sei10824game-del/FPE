package com.fpe.client.model;

import java.awt.image.BufferedImage;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.Base64;
import java.util.HashMap;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

import javax.imageio.ImageIO;

import com.google.gson.JsonArray;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;

/**
 * Loads a Blockbench .bbmodel (format "Modded Entity", box UV) from assets/fpe/bbmodels/&lt;name&gt;.bbmodel into a {@link ModelSpec}.
 * Bone animations named like an ability id play on the ability timeline (seconds = tick / 20).
 * Special animation names: "idle" (loops on age), "walk" (loops on limbSwing, weighted by walk()), "death" (scrubbed by death 0..1).
 * A texture named "glow" (if present) becomes the emissive layer; the first other texture is the colour texture.
 * Blockbench (Y up, ground 0, +x = world east) -> model space (Y down, ground 24, x mirrored): x' = -x, y' = 24 - y, rot = (-rx, -ry, rz).
 */
public final class BbModel {
    private BbModel() {}

    public static ModelSpec load(String name, float shadow) { return load(name).shadow(shadow); }

    public static ModelSpec load(String name) {
        try (InputStream in = BbModel.class.getResourceAsStream("/assets/fpe/bbmodels/" + name + ".bbmodel")) {
            if (in == null) throw new IllegalStateException("missing bbmodel " + name);
            return parse(name, JsonParser.parseReader(new InputStreamReader(in, StandardCharsets.UTF_8)).getAsJsonObject());
        } catch (java.io.IOException e) { throw new IllegalStateException(e); }
    }

    private static float f(JsonObject o, String k, float d) { return o.has(k) ? o.get(k).getAsFloat() : d; }
    private static float[] v3(JsonObject o, String k, float x, float y, float z) {
        if (!o.has(k)) return new float[] { x, y, z };
        JsonArray a = o.getAsJsonArray(k);
        return new float[] { a.get(0).getAsFloat(), a.get(1).getAsFloat(), a.get(2).getAsFloat() };
    }
    private static float num(JsonElement e) {
        if (e == null || e.isJsonNull()) return 0;
        try { return e.getAsFloat(); } catch (Exception ex) { try { return Float.parseFloat(e.getAsString().trim()); } catch (Exception ex2) { return 0; } }
    }

    static ModelSpec parse(String name, JsonObject root) {
        ModelSpec m = new ModelSpec(name);
        int tw = 64, th = 64;
        if (root.has("resolution")) { tw = root.getAsJsonObject("resolution").get("width").getAsInt(); th = root.getAsJsonObject("resolution").get("height").getAsInt(); }
        else if (root.has("texture_width")) { tw = root.get("texture_width").getAsInt(); th = root.get("texture_height").getAsInt(); }

        Map<String, JsonObject> cubes = new HashMap<>();
        for (JsonElement e : root.getAsJsonArray("elements")) { JsonObject c = e.getAsJsonObject(); if (!c.has("type") || c.get("type").getAsString().equals("cube")) cubes.put(c.get("uuid").getAsString(), c); }

        Set<String> used = new HashSet<>();
        Map<String, String> boneName = new HashMap<>();
        for (JsonElement e : root.getAsJsonArray("outliner")) walk(m, e, null, cubes, used, boneName, 0);

        // textures
        int[] tex = null, glow = null, size = new int[2], texSize = new int[2];
        if (root.has("textures")) for (JsonElement e : root.getAsJsonArray("textures")) {
            JsonObject t = e.getAsJsonObject();
            String src = t.get("source").getAsString();
            int[] px = decode(src.substring(src.indexOf(',') + 1), size);
            boolean isGlow = t.has("name") && t.get("name").getAsString().toLowerCase().contains("glow");
            if (isGlow && glow == null) { for (int i = 0; i < px.length; i++) if ((px[i] >>> 24) < 128) px[i] = 0xFF000000; glow = px; } else if (!isGlow && tex == null) { tex = px; texSize[0] = size[0]; texSize[1] = size[1]; }
        }
        if (tex == null) throw new IllegalStateException("bbmodel " + name + " has no texture");
        float su = texSize[0] / (float) tw, sv = texSize[1] / (float) th;
        for (ModelSpec.Part p : faceParts) for (float[] r : p.faceUv) { r[0] *= su; r[2] *= su; r[1] *= sv; r[3] *= sv; }
        faceParts.clear();
        m.external(tex, glow, texSize[0], texSize[1]);
        // animations
        if (root.has("animations")) m.animator(animator(root.getAsJsonArray("animations"), boneName));
        return m;
    }

    private static int[] decode(String b64, int[] size) {
        try {
            BufferedImage img = ImageIO.read(new java.io.ByteArrayInputStream(Base64.getDecoder().decode(b64)));
            int w = img.getWidth(), h = img.getHeight();
            size[0] = w; size[1] = h;
            int[] px = new int[w * h];
            img.getRGB(0, 0, w, h, px, 0, w);
            return px;
        } catch (java.io.IOException e) { throw new IllegalStateException(e); }
    }

    private static String unique(Set<String> used, String base) {
        String n = base.replaceAll("\\s+", "_"); int i = 2; String c = n;
        while (!used.add(c)) c = n + "_" + i++;
        return c;
    }

    private static final List<ModelSpec.Part> faceParts = new ArrayList<>();

    private static void walk(ModelSpec m, JsonElement node, String parent, Map<String, JsonObject> cubes, Set<String> used, Map<String, String> boneName, int depth) {
        if (node.isJsonPrimitive()) {
            JsonObject c = cubes.get(node.getAsString());
            if (c == null) return;
            float[] from = v3(c, "from", 0, 0, 0), to = v3(c, "to", 0, 0, 0), o = v3(c, "origin", 0, 0, 0), r = v3(c, "rotation", 0, 0, 0);
            float inf = f(c, "inflate", 0);
            ModelSpec.Part p = m.part(unique(used, c.has("name") ? c.get("name").getAsString() : "cube"), parent,
                    -o[0], 24 - o[1], o[2], o[0] - to[0], o[1] - to[1], from[2] - o[2], to[0] - from[0], to[1] - from[1], to[2] - from[2], 0xFFFFFF);
            p.rot(-r[0], -r[1], r[2]);
            p.inflate = inf;
            if (c.has("mirror_uv") && c.get("mirror_uv").getAsBoolean()) p.mirror = true;
            float[] uv = v3(c, "uv_offset", 0, 0, 0);
            p.u = (int) uv[0]; p.v = (int) uv[1];
            if (c.has("box_uv") && !c.get("box_uv").getAsBoolean() && c.has("faces")) {
                JsonObject fs = c.getAsJsonObject("faces");
                p.faceUv = new float[6][4];
                String[] names = { "north", "east", "south", "west", "up", "down" };
                for (int i = 0; i < 6; i++) if (fs.has(names[i]) && fs.getAsJsonObject(names[i]).has("uv")) {
                    JsonArray a = fs.getAsJsonObject(names[i]).getAsJsonArray("uv");
                    for (int j = 0; j < 4; j++) p.faceUv[i][j] = a.get(j).getAsFloat();
                }
                faceParts.add(p);
            }
            return;
        }
        JsonObject g = node.getAsJsonObject();
        float[] o = v3(g, "origin", 0, 0, 0), r = v3(g, "rotation", 0, 0, 0);
        String nm = unique(used, g.has("name") ? g.get("name").getAsString() : "group");
        boneName.put(g.get("uuid").getAsString(), nm);
        m.group(nm, parent, -o[0], 24 - o[1], o[2]).rot(-r[0], -r[1], r[2]);
        for (JsonElement ch : g.getAsJsonArray("children")) walk(m, ch, nm, cubes, used, boneName, depth + 1);
    }

    // ------------------------------------------------------------------ animation
    private record Key(float t, float[] v, boolean smooth) {}
    private static final class Track { final List<Key> rot = new ArrayList<>(), pos = new ArrayList<>(), scl = new ArrayList<>(); }
    private static final class Anim_ { float length; boolean loop; final Map<String, Track> bones = new HashMap<>(); }

    private static Animator animator(JsonArray anims, Map<String, String> boneName) {
        Map<String, Anim_> byName = new HashMap<>();
        for (JsonElement e : anims) {
            JsonObject a = e.getAsJsonObject();
            Anim_ an = new Anim_();
            an.length = f(a, "length", 1f);
            an.loop = a.has("loop") && a.get("loop").getAsString().equals("loop");
            if (a.has("animators")) for (Map.Entry<String, JsonElement> en : a.getAsJsonObject("animators").entrySet()) {
                JsonObject ao = en.getValue().getAsJsonObject();
                String bone = boneName.get(en.getKey());
                if (bone == null && ao.has("name")) bone = ao.get("name").getAsString().replaceAll("\\s+", "_");
                if (bone == null || !ao.has("keyframes")) continue;
                Track tr = new Track();
                for (JsonElement ke : ao.getAsJsonArray("keyframes")) {
                    JsonObject k = ke.getAsJsonObject();
                    JsonObject dp = k.getAsJsonArray("data_points").get(0).getAsJsonObject();
                    float[] v = { num(dp.get("x")), num(dp.get("y")), num(dp.get("z")) };
                    boolean smooth = !k.has("interpolation") || k.get("interpolation").getAsString().equals("catmullrom");
                    Key key = new Key(f(k, "time", 0), v, smooth);
                    switch (k.get("channel").getAsString()) { case "rotation" -> tr.rot.add(key); case "position" -> tr.pos.add(key); case "scale" -> tr.scl.add(key); default -> {} }
                }
                for (List<Key> l : List.of(tr.rot, tr.pos, tr.scl)) l.sort((x, y) -> Float.compare(x.t, y.t));
                an.bones.put(bone, tr);
            }
            byName.put(a.get("name").getAsString(), an);
        }
        return (parts, c) -> {
            // base layers: idle always, walk by weight, then ability / death override
            Anim_ idle = byName.get("idle"), walk = byName.get("walk");
            Anim_ ab = c.ability.isEmpty() ? null : byName.get(c.ability), de = c.death > 0 ? byName.get("death") : null;
            if (de != null) apply(parts, de, c.death * de.length, 1f);          // death replaces everything
            else if (ab != null) apply(parts, ab, c.t / 20f, 1f);                // an ability replaces idle + walk
            else {
                Anim_ qi = c.stance == 1 ? byName.get("quad_idle") : null, qw = c.stance == 1 ? byName.get("quad_walk") : null;
                Anim_ i2 = qi != null ? qi : idle, w2 = qw != null ? qw : walk;
                if (i2 != null) apply(parts, i2, c.age / 20f, 1f);
                if (w2 != null && c.walk() > 0.01f) apply(parts, w2, c.limbSwing * 0.6662f / 6.2832f * w2.length, c.walk());
            }
            // head look (only when idle/walking so authored attack poses stay in control)
            if (c.ability.isEmpty()) parts.addRot("head", c.headPitch, c.headYaw, 0);
        };
    }

    private static void apply(ModelParts parts, Anim_ a, float time, float w) {
        if (a.loop && a.length > 0) time = ((time % a.length) + a.length) % a.length; else time = Math.min(time, a.length);
        for (Map.Entry<String, Track> en : a.bones.entrySet()) {
            Track t = en.getValue(); String b = en.getKey();
            if (!t.rot.isEmpty()) { float[] v = sample(t.rot, time, 0f); parts.addRot(b, -v[0] * w, -v[1] * w, v[2] * w); }
            if (!t.pos.isEmpty()) { float[] v = sample(t.pos, time, 0f); parts.move(b, -v[0] * w, -v[1] * w, v[2] * w); }
            if (!t.scl.isEmpty()) { float[] v = sample(t.scl, time, 1f); parts.scale(b, 1 + (v[0] - 1) * w, 1 + (v[1] - 1) * w, 1 + (v[2] - 1) * w); }
        }
    }

    private static float[] sample(List<Key> k, float t, float dflt) {
        if (k.size() == 1 || t <= k.get(0).t) return k.get(0).v;
        Key last = k.get(k.size() - 1);
        if (t >= last.t) return last.v;
        int i = 0; while (k.get(i + 1).t < t) i++;
        Key a = k.get(i), b = k.get(i + 1);
        float u = (t - a.t) / Math.max(1e-5f, b.t - a.t);
        float[] r = new float[3];
        boolean cat = a.smooth && b.smooth;
        Key p0 = k.get(Math.max(0, i - 1)), p3 = k.get(Math.min(k.size() - 1, i + 2));
        for (int j = 0; j < 3; j++) {
            if (cat) {
                float u2 = u * u, u3 = u2 * u;
                r[j] = 0.5f * ((2 * a.v[j]) + (-p0.v[j] + b.v[j]) * u + (2 * p0.v[j] - 5 * a.v[j] + 4 * b.v[j] - p3.v[j]) * u2 + (-p0.v[j] + 3 * a.v[j] - 3 * b.v[j] + p3.v[j]) * u3);
            } else r[j] = a.v[j] + (b.v[j] - a.v[j]) * u;
        }
        return r;
    }
}
