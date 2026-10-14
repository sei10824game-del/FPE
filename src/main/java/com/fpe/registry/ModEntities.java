package com.fpe.registry;

import com.fpe.FpeMod;
import com.fpe.entity.*;
import com.fpe.entity.characters.*;

import net.minecraft.core.registries.Registries;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.MobCategory;
import net.minecraft.world.entity.SpawnPlacements;
import net.minecraft.world.entity.monster.Monster;
import net.minecraft.world.level.levelgen.Heightmap;
import net.minecraftforge.event.entity.EntityAttributeCreationEvent;
import net.minecraftforge.event.entity.EntityAttributeModificationEvent;
import net.minecraftforge.event.entity.SpawnPlacementRegisterEvent;
import net.minecraftforge.eventbus.api.SubscribeEvent;
import net.minecraftforge.registries.DeferredRegister;
import net.minecraftforge.registries.ForgeRegistries;
import net.minecraftforge.registries.RegistryObject;

public final class ModEntities {
    private ModEntities() {}

    public static final DeferredRegister<EntityType<?>> ENTITIES = DeferredRegister.create(ForgeRegistries.ENTITY_TYPES, FpeMod.MODID);

    private static <T extends FpeEntity> RegistryObject<EntityType<T>> chara(String id, EntityType.EntityFactory<T> f, float w, float h) {
        return ENTITIES.register(id, () -> EntityType.Builder.of(f, MobCategory.MONSTER).sized(w, h).clientTrackingRange(10).updateInterval(2).build(FpeMod.MODID + ":" + id));
    }

    public static final RegistryObject<EntityType<MissCircle>> MISS_CIRCLE = chara("miss_circle", MissCircle::new, 0.7f, 2.2f);
    public static final RegistryObject<EntityType<MissThavel>> MISS_THAVEL = chara("miss_thavel", MissThavel::new, 0.7f, 2.0f);
    public static final RegistryObject<EntityType<MissBloomie>> MISS_BLOOMIE = chara("miss_bloomie", MissBloomie::new, 0.7f, 2.0f);
    public static final RegistryObject<EntityType<Alice>> ALICE = chara("alice", Alice::new, 0.7f, 2.0f);
    public static final RegistryObject<EntityType<RedCircle>> RED_CIRCLE = chara("red_circle", RedCircle::new, 0.7f, 2.3f);
    public static final RegistryObject<EntityType<DangerThavel>> DANGER_THAVEL = chara("danger_thavel", DangerThavel::new, 0.7f, 2.1f);
    public static final RegistryObject<EntityType<DangerBloomie>> DANGER_BLOOMIE = chara("danger_bloomie", DangerBloomie::new, 0.7f, 2.0f);
    public static final RegistryObject<EntityType<InfectedBloomie>> INFECTED_BLOOMIE = chara("infected_bloomie", InfectedBloomie::new, 1.3f, 3.2f);
    public static final RegistryObject<EntityType<InfectedZip>> INFECTED_ZIP = chara("infected_zip", InfectedZip::new, 1.5f, 2.3f);
    public static final RegistryObject<EntityType<Fen>> FEN = chara("fen", Fen::new, 0.7f, 2.0f);
    public static final RegistryObject<EntityType<Aiden>> AIDEN = chara("aiden", Aiden::new, 0.6f, 1.7f);

    public static final RegistryObject<EntityType<FpeProjectile>> PROJECTILE = ENTITIES.register("projectile", () ->
            EntityType.Builder.<FpeProjectile>of(FpeProjectile::new, MobCategory.MISC).sized(0.4f, 0.4f).clientTrackingRange(8).updateInterval(1).build(FpeMod.MODID + ":projectile"));
    public static final RegistryObject<EntityType<FpeFx>> FX = ENTITIES.register("fx", () ->
            EntityType.Builder.<FpeFx>of(FpeFx::new, MobCategory.MISC).sized(0.5f, 0.5f).clientTrackingRange(10).updateInterval(20).fireImmune().build(FpeMod.MODID + ":fx"));

    /** all character types (for eggs, spawns, attributes) */
    @SuppressWarnings("unchecked")
    public static java.util.List<RegistryObject<? extends EntityType<? extends FpeEntity>>> characters() {
        return java.util.List.of(MISS_CIRCLE, MISS_THAVEL, MISS_BLOOMIE, ALICE, RED_CIRCLE, DANGER_THAVEL, DANGER_BLOOMIE, INFECTED_BLOOMIE, INFECTED_ZIP, FEN, AIDEN);
    }

    public static final class Events {
        @SubscribeEvent
        public static void attributes(EntityAttributeCreationEvent e) {
            e.put(MISS_CIRCLE.get(), MissCircle.attributes().build());
            e.put(MISS_THAVEL.get(), MissThavel.attributes().build());
            e.put(MISS_BLOOMIE.get(), MissBloomie.attributes().build());
            e.put(ALICE.get(), Alice.attributes().build());
            e.put(RED_CIRCLE.get(), RedCircle.attributes().build());
            e.put(DANGER_THAVEL.get(), DangerThavel.attributes().build());
            e.put(DANGER_BLOOMIE.get(), DangerBloomie.attributes().build());
            e.put(INFECTED_BLOOMIE.get(), InfectedBloomie.attributes().build());
            e.put(INFECTED_ZIP.get(), InfectedZip.attributes().build());
            e.put(FEN.get(), Fen.attributes().build());
            e.put(AIDEN.get(), Aiden.attributes().build());
        }

        /** give every living type an attack so that all mobs (even cows) can be turned hostile to FPE characters */
        @SubscribeEvent
        @SuppressWarnings("unchecked")
        public static void attackAttrs(EntityAttributeModificationEvent e) {
            for (EntityType<?> t : ForgeRegistries.ENTITY_TYPES) {
                if (t == EntityType.PLAYER || !e.getTypes().contains(t)) continue;
                EntityType<? extends net.minecraft.world.entity.LivingEntity> lt = (EntityType<? extends net.minecraft.world.entity.LivingEntity>) t;
                if (!e.has(lt, net.minecraft.world.entity.ai.attributes.Attributes.ATTACK_DAMAGE)) e.add(lt, net.minecraft.world.entity.ai.attributes.Attributes.ATTACK_DAMAGE, 2.0);
                if (!e.has(lt, net.minecraft.world.entity.ai.attributes.Attributes.ATTACK_KNOCKBACK)) e.add(lt, net.minecraft.world.entity.ai.attributes.Attributes.ATTACK_KNOCKBACK, 0.4);
            }
        }

        @SubscribeEvent
        public static void spawns(SpawnPlacementRegisterEvent e) {
            for (RegistryObject<? extends EntityType<? extends FpeEntity>> r : characters())
                e.register(r.get(), SpawnPlacements.Type.ON_GROUND, Heightmap.Types.MOTION_BLOCKING_NO_LEAVES, (t, l, s, p, rnd) -> Monster.checkMonsterSpawnRules(t, l, s, p, rnd), SpawnPlacementRegisterEvent.Operation.OR);
        }
    }
}
