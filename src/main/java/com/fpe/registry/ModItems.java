package com.fpe.registry;

import com.fpe.FpeMod;
import com.fpe.entity.FpeEntity;

import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraftforge.common.ForgeSpawnEggItem;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.ForgeRegistries;
import net.minecraftforge.registries.RegistryObject;

public final class ModItems {
    private ModItems() {}

    public static final DeferredRegister<Item> ITEMS = DeferredRegister.create(ForgeRegistries.ITEMS, FpeMod.MODID);
    public static final DeferredRegister<CreativeModeTab> TABS = DeferredRegister.create(Registries.CREATIVE_MODE_TAB, FpeMod.MODID);

    private static RegistryObject<Item> egg(String id, RegistryObject<? extends EntityType<? extends FpeEntity>> t, int c1, int c2) {
        return ITEMS.register(id + "_spawn_egg", () -> new ForgeSpawnEggItem(t, c1, c2, new Item.Properties()));
    }

    public static final RegistryObject<Item> MISS_CIRCLE = egg("miss_circle", ModEntities.MISS_CIRCLE, 0x3A2A55, 0xE8923C);
    public static final RegistryObject<Item> MISS_THAVEL = egg("miss_thavel", ModEntities.MISS_THAVEL, 0x3A2A55, 0xD9732B);
    public static final RegistryObject<Item> MISS_BLOOMIE = egg("miss_bloomie", ModEntities.MISS_BLOOMIE, 0x2B2B3A, 0xC9D0CC);
    public static final RegistryObject<Item> ALICE = egg("alice", ModEntities.ALICE, 0x5A3A2E, 0x151018);
    public static final RegistryObject<Item> RED_CIRCLE = egg("red_circle", ModEntities.RED_CIRCLE, 0x241B30, 0xC01830);
    public static final RegistryObject<Item> DANGER_THAVEL = egg("danger_thavel", ModEntities.DANGER_THAVEL, 0x1D1A2B, 0xE0C060);
    public static final RegistryObject<Item> DANGER_BLOOMIE = egg("danger_bloomie", ModEntities.DANGER_BLOOMIE, 0x241B30, 0x9FB0AE);
    public static final RegistryObject<Item> FEN = egg("fen", ModEntities.FEN, 0xE8923C, 0x15131C);
    public static final RegistryObject<Item> AIDEN = egg("aiden", ModEntities.AIDEN, 0x6B4A3A, 0x8A1C1C);

    public static final RegistryObject<CreativeModeTab> TAB = TABS.register("main", () -> CreativeModeTab.builder()
            .title(Component.translatable("itemGroup.fpe"))
            .icon(() -> new ItemStack(MISS_CIRCLE.get()))
            .displayItems((p, out) -> ITEMS.getEntries().forEach(i -> out.accept(i.get())))
            .build());
}
