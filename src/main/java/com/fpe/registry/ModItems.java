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
    public static final RegistryObject<Item> INFECTED_BLOOMIE = egg("infected_bloomie", ModEntities.INFECTED_BLOOMIE, 0xC4C9D8, 0x14111C);
    public static final RegistryObject<Item> INFECTED_ZIP = egg("infected_zip", ModEntities.INFECTED_ZIP, 0x15141A, 0xE8E6EE);
    public static final RegistryObject<Item> DANGER_ALICE = egg("danger_alice", ModEntities.DANGER_ALICE, 0x17171D, 0xE8A850);
    public static final RegistryObject<Item> FEN = egg("fen", ModEntities.FEN, 0xE8923C, 0x15131C);
    public static final RegistryObject<Item> AIDEN = egg("aiden", ModEntities.AIDEN, 0x6B4A3A, 0x8A1C1C);
    public static final RegistryObject<Item> MUTANT_CLAIRE = egg("mutant_claire", ModEntities.MUTANT_CLAIRE, 0xE6E6EA, 0x14121A);
    public static final RegistryObject<Item> MUTANT_ENGEL = egg("mutant_engel", ModEntities.MUTANT_ENGEL, 0xF0F0F2, 0x101010);
    public static final RegistryObject<Item> MUTANT_BUBBLE = egg("mutant_bubble", ModEntities.MUTANT_BUBBLE, 0xF4F2F0, 0xD04060);
    public static final RegistryObject<Item> MUTANT_LANA = egg("mutant_lana", ModEntities.MUTANT_LANA, 0xB8B0B0, 0x14121A);
    public static final RegistryObject<Item> MUTANT_ABBIE = egg("mutant_abbie", ModEntities.MUTANT_ABBIE, 0x121014, 0xD05060);
    public static final RegistryObject<Item> GREEN_THAVEL = egg("green_thavel", ModEntities.GREEN_THAVEL, 0xF0F0F0, 0x58C040);
    public static final RegistryObject<Item> GREEN_BLOOMIE = egg("green_bloomie", ModEntities.GREEN_BLOOMIE, 0xE8E8EC, 0x58C040);
    public static final RegistryObject<Item> GREEN_ALICE = egg("green_alice", ModEntities.GREEN_ALICE, 0x5A3A2E, 0x58C040);
    public static final RegistryObject<Item> GREEN_CIRCLE = egg("green_circle", ModEntities.GREEN_CIRCLE, 0x1C1A22, 0x58C040);
    public static final RegistryObject<Item> HANSEL_JUVENILE = egg("hansel_juvenile", ModEntities.HANSEL_JUVENILE, 0x3E7A34, 0xF0E8D0);
    public static final RegistryObject<Item> LORD_HANSEL = egg("lord_hansel", ModEntities.LORD_HANSEL, 0xE8DCC0, 0xB01818);
    public static final RegistryObject<Item> RILEY = egg("riley", ModEntities.RILEY, 0xE8E8EA, 0x20202A);
    public static final RegistryObject<Item> DANIEL_BARREL = egg("daniel_barrel", ModEntities.DANIEL_BARREL, 0xB8BCC0, 0x2A2630);

    public static final RegistryObject<CreativeModeTab> TAB = TABS.register("main", () -> CreativeModeTab.builder()
            .title(Component.translatable("itemGroup.fpe"))
            .icon(() -> new ItemStack(MISS_CIRCLE.get()))
            .displayItems((p, out) -> ITEMS.getEntries().forEach(i -> out.accept(i.get())))
            .build());
}
