package com.fpe.client.model;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import net.minecraft.client.model.geom.ModelPart;

/** name -> ModelPart lookup; unknown names return a harmless dummy so animators never NPE. */
public final class ModelParts {
    private final Map<String, ModelPart> map = new HashMap<>();
    private final ModelPart dummy = new ModelPart(List.of(), Map.of());
    /** per-face-UV polygons per part name (rendered by SpecModel itself, see there) */
    final Map<String, ModelPart.Polygon[]> polys = new HashMap<>();
    final Map<String, List<ModelSpec.Part>> children = new HashMap<>();
    public boolean customRender;

    public ModelParts(ModelPart root, ModelSpec spec) {
        for (ModelSpec.Part p : spec.parts) {
            ModelPart cur = root;
            for (String s : spec.path(p.name)) cur = cur.getChild(s);
            map.put(p.name, cur);
            if (p.faceUv != null) { FaceUv.apply(cur, p, spec.texW, spec.texH); polys.put(p.name, FaceUv.build(p, spec.texW, spec.texH)); customRender = true; }
            children.computeIfAbsent(p.parent == null ? "" : p.parent, k -> new ArrayList<>()).add(p);
        }
    }

    public ModelPart get(String name) { return map.getOrDefault(name, dummy); }

    public Iterable<ModelPart> all() { return map.values(); }

    public void resetAll() { for (ModelPart p : map.values()) p.resetPose(); }

    // ---- small helpers
    public void rot(String n, float xDeg, float yDeg, float zDeg) {
        ModelPart p = get(n); p.xRot = (float) Math.toRadians(xDeg); p.yRot = (float) Math.toRadians(yDeg); p.zRot = (float) Math.toRadians(zDeg);
    }
    /** add degrees to the default rotation */
    public void addRot(String n, float xDeg, float yDeg, float zDeg) {
        ModelPart p = get(n); p.xRot += (float) Math.toRadians(xDeg); p.yRot += (float) Math.toRadians(yDeg); p.zRot += (float) Math.toRadians(zDeg);
    }
    public void move(String n, float dx, float dy, float dz) { ModelPart p = get(n); p.x += dx; p.y += dy; p.z += dz; }
    public void scale(String n, float sx, float sy, float sz) { ModelPart p = get(n); p.xScale = sx; p.yScale = sy; p.zScale = sz; }
    public void hide(String n) { get(n).visible = false; }
    public void show(String n, boolean v) { get(n).visible = v; }
}
