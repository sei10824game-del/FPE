package com.fpe.client.model;

import net.minecraft.client.model.geom.ModelPart;
import net.minecraft.client.model.geom.ModelPart.Cube;
import net.minecraft.client.model.geom.ModelPart.Polygon;
import net.minecraft.client.model.geom.ModelPart.Vertex;
import net.minecraft.core.Direction;

/** Replaces the vanilla box-UV polygons of a one-cube part by polygons using free per-face UV rectangles (needs the access transformer). */
final class FaceUv {
    private FaceUv() {}

    static void apply(ModelPart mp, ModelSpec.Part p, int tw, int th) {
        Cube c = mp.cubes.get(0);
        float x0 = p.ox - p.inflate, y0 = p.oy - p.inflate, z0 = p.oz - p.inflate;
        float x1 = p.ox + p.w + p.inflate, y1 = p.oy + p.h + p.inflate, z1 = p.oz + p.d + p.inflate;
        if (p.mirror) { float t = x0; x0 = x1; x1 = t; }
        Vertex a = new Vertex(x0, y0, z0, 0, 0), b = new Vertex(x1, y0, z0, 0, 8), c2 = new Vertex(x1, y1, z0, 8, 8), d = new Vertex(x0, y1, z0, 8, 0);
        Vertex e = new Vertex(x0, y0, z1, 0, 0), f = new Vertex(x1, y0, z1, 0, 8), g = new Vertex(x1, y1, z1, 8, 8), h = new Vertex(x0, y1, z1, 8, 0);
        Vertex[][] verts = { { f, e, a, b }, { c2, d, h, g }, { a, e, h, d }, { b, a, d, c2 }, { f, b, c2, g }, { e, f, g, h } };
        // vanilla polygon order: y-min(top), y-max, x-min, z-min, x-max, z-max  <->  faceUv slots up, down, east, north, west, south
        int[] slot = { 4, 5, 1, 0, 3, 2 };
        Direction[] dir = { Direction.DOWN, Direction.UP, Direction.WEST, Direction.NORTH, Direction.EAST, Direction.SOUTH };
        for (int i = 0; i < 6 && i < c.polygons.length; i++) {
            float[] uv = p.faceUv[slot[i]];
            c.polygons[i] = new Polygon(verts[i], uv[0], uv[1], uv[2], uv[3], tw, th, p.mirror, dir[i]);
        }
    }
}
