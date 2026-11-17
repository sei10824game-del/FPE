package com.fpe.registry;

import com.fpe.FpeMod;

import net.minecraft.world.effect.MobEffect;
import net.minecraft.world.effect.MobEffectCategory;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.ForgeRegistries;
import net.minecraftforge.registries.RegistryObject;

/** Synced marker for ground-jump suppression; leaves vanilla Jump Boost intact. */
public final class ModEffects {
    private ModEffects() {}

    public static final DeferredRegister<MobEffect> EFFECTS = DeferredRegister.create(ForgeRegistries.MOB_EFFECTS, FpeMod.MODID);
    public static final RegistryObject<MobEffect> ROOTED = EFFECTS.register("rooted", Rooted::new);

    private static final class Rooted extends MobEffect {
        private Rooted() { super(MobEffectCategory.HARMFUL, 0x504858); }
    }
}
