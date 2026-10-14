package com.fpe;

import com.fpe.entity.FpeHostility;
import com.fpe.registry.ModEntities;
import com.fpe.registry.ModItems;

import net.minecraftforge.common.MinecraftForge;
import net.minecraftforge.eventbus.api.IEventBus;
import net.minecraftforge.fml.common.Mod;
import net.minecraftforge.fml.javafmlmod.FMLJavaModLoadingContext;

@Mod(FpeMod.MODID)
public class FpeMod {
    public static final String MODID = "fpe";

    public FpeMod() {
        IEventBus bus = FMLJavaModLoadingContext.get().getModEventBus();
        ModEntities.ENTITIES.register(bus);
        ModItems.ITEMS.register(bus);
        ModItems.TABS.register(bus);
        bus.register(ModEntities.Events.class);
        MinecraftForge.EVENT_BUS.register(FpeHostility.class);
        if (Boolean.getBoolean("fpe.selftest")) MinecraftForge.EVENT_BUS.register(com.fpe.tools.SelfTest.class);
    }
}
