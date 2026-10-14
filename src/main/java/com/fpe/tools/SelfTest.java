package com.fpe.tools;

import com.fpe.entity.FpeEntity;
import com.fpe.registry.ModEntities;

import net.minecraft.core.BlockPos;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.level.block.Blocks;
import net.minecraftforge.event.TickEvent;
import net.minecraftforge.event.server.ServerStartedEvent;
import net.minecraftforge.eventbus.api.SubscribeEvent;

/** dev only (-Dfpe.selftest=true): spawns every character vs a zombie and ticks 1200 ticks, then stops. */
public final class SelfTest {
    static int ticks;
    static ServerLevel lvl;

    @SubscribeEvent
    public static void started(ServerStartedEvent e) {
        lvl = e.getServer().overworld();
        for (int cx = -3; cx <= 3; cx++) for (int cz = -2; cz <= 2; cz++) lvl.setChunkForced(cx, cz, true);
        BlockPos o = new BlockPos(0, 100, 0);
        for (int x = -30; x <= 30; x++) for (int z = -30; z <= 30; z++) lvl.setBlock(o.offset(x, -1, z), Blocks.STONE.defaultBlockState(), 3);
        int i = 0;
        for (var r : ModEntities.characters()) {
            FpeEntity c = (FpeEntity) r.get().create(lvl);
            c.moveTo(-18 + i * 4.5, 100, 0, 0, 0);
            System.out.println("SELFTEST spawn " + c + " ok=" + lvl.addFreshEntity(c));
            Mob z = EntityType.ZOMBIE.create(lvl);
            z.moveTo(-18 + i * 4.5, 100, 6, 0, 0);
            lvl.addFreshEntity(z);
            i++;
        }
    }

    @SubscribeEvent
    public static void tick(TickEvent.ServerTickEvent e) {
        if (e.phase != TickEvent.Phase.END || lvl == null) return;
        if (ticks % 200 == 0) { long n = 0; for (var en : lvl.getAllEntities()) if (en instanceof FpeEntity) n++; System.out.println("SELFTEST t=" + ticks + " fpe=" + n + " diff=" + lvl.getDifficulty()); }
        if (++ticks == 1200) {
            long alive = 0;
            for (var en : lvl.getAllEntities()) if (en instanceof FpeEntity f) { alive++; System.out.println("SELFTEST " + f.getType().getDescriptionId() + " hp=" + f.getHealth()); }
            System.out.println("SELFTEST alive=" + alive);
            lvl.getServer().halt(false);
        }
    }
}
