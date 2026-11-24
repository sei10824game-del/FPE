package com.fpe.tools;

import com.fpe.entity.FpeFx;
import com.fpe.registry.ModEntities;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.world.phys.Vec3;
import net.minecraftforge.gametest.GameTestHolder;
import net.minecraftforge.gametest.PrefixGameTestTemplate;

@GameTestHolder("fpe")
@PrefixGameTestTemplate(false)
public final class VisualBoundsGameTests {
    @GameTest(template = "combat_empty")
    public static void effectBoundsContainVisibleGeometry(GameTestHelper h) {
        FpeFx fx = new FpeFx(ModEntities.FX.get(), h.getLevel());
        fx.setPos(h.absoluteVec(new Vec3(5, 2, 5)));
        var collision = fx.getBoundingBox();
        for (var kind : new FpeFx.Kind[] {FpeFx.Kind.RING_TRAP, FpeFx.Kind.RING_SHOCK}) {
            fx.setup(kind, 10, 40, 14, 0);
            for (Vec3 rim : new Vec3[] {new Vec3(13.9, 0.05, 0), new Vec3(-13.9, 0.05, 0),
                    new Vec3(0, 0.05, 13.9), new Vec3(0, 0.05, -13.9)}) {
                h.assertTrue(fx.getBoundingBoxForCulling().contains(fx.position().add(rim)), "Large warning rim must survive camera culling");
            }
        }
        fx.setup(FpeFx.Kind.ARC, 0, 7, 6, 0);
        fx.setXRot(90);
        h.assertTrue(fx.getBoundingBoxForCulling().contains(fx.position().add(0, 6.2, 0)), "Vertical slash must include its bright outer edge");
        fx.setup(FpeFx.Kind.SPIKE, 10, 40, 1, 0);
        fx.param(2);
        h.assertTrue(fx.getBoundingBoxForCulling().contains(fx.position().add(0, 4.6, 0)), "Double-height spike tip must not be culled");
        h.assertTrue(fx.getBoundingBoxForCulling().contains(fx.position().add(0, -0.87, 0)), "Scaled spike base must fit below its origin");
        fx.setup(FpeFx.Kind.TENTACLE, 10, 40, 1, 0);
        h.assertTrue(fx.getBoundingBoxForCulling().contains(fx.position().add(7.4, 0, 0)), "Scaled tentacle sway must fit render bounds");
        h.assertTrue(fx.getBoundingBox().equals(collision), "Visual bounds must not enlarge collision geometry");
        h.succeed();
    }
}
