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

    public static final RegistryObject<EntityType<MissCircle>> MISS_CIRCLE = chara("miss_circle", MissCircle::new, 0.75f, 2.57f);
    public static final RegistryObject<EntityType<MissThavel>> MISS_THAVEL = chara("miss_thavel", MissThavel::new, 0.6f, 2.19f);
    public static final RegistryObject<EntityType<MissBloomie>> MISS_BLOOMIE = chara("miss_bloomie", MissBloomie::new, 0.6f, 2.18f);
    public static final RegistryObject<EntityType<Alice>> ALICE = chara("alice", Alice::new, 0.7f, 2.51f);
    public static final RegistryObject<EntityType<RedCircle>> RED_CIRCLE = chara("red_circle", RedCircle::new, 0.75f, 2.57f);
    public static final RegistryObject<EntityType<DangerThavel>> DANGER_THAVEL = chara("danger_thavel", DangerThavel::new, 0.7f, 2.44f);
    public static final RegistryObject<EntityType<DangerBloomie>> DANGER_BLOOMIE = chara("danger_bloomie", DangerBloomie::new, 0.65f, 2.29f);
    public static final RegistryObject<EntityType<InfectedBloomie>> INFECTED_BLOOMIE = chara("infected_bloomie", InfectedBloomie::new, 1.3f, 4.12f);
    public static final RegistryObject<EntityType<InfectedZip>> INFECTED_ZIP = chara("infected_zip", InfectedZip::new, 1.5f, 2.94f);
    public static final RegistryObject<EntityType<DangerAlice>> DANGER_ALICE = chara("danger_alice", DangerAlice::new, 0.7f, 2.51f);
    public static final RegistryObject<EntityType<Fen>> FEN = chara("fen", Fen::new, 1.0f, 3.2f);
    public static final RegistryObject<EntityType<Aiden>> AIDEN = chara("aiden", Aiden::new, 0.6f, 1.64f);

    public static final RegistryObject<EntityType<MutantClaire>> MUTANT_CLAIRE = chara("mutant_claire", MutantClaire::new, 0.6f, 1.53f);
    public static final RegistryObject<EntityType<MutantEngel>> MUTANT_ENGEL = chara("mutant_engel", MutantEngel::new, 0.6f, 1.93f);
    public static final RegistryObject<EntityType<MutantBubble>> MUTANT_BUBBLE = chara("mutant_bubble", MutantBubble::new, 0.6f, 1.22f);
    public static final RegistryObject<EntityType<MutantLana>> MUTANT_LANA = chara("mutant_lana", MutantLana::new, 0.6f, 1.72f);
    public static final RegistryObject<EntityType<MutantAbbie>> MUTANT_ABBIE = chara("mutant_abbie", MutantAbbie::new, 0.6f, 1.5f);
    public static final RegistryObject<EntityType<GreenThavel>> GREEN_THAVEL = chara("green_thavel", GreenThavel::new, 0.65f, 2.29f);
    public static final RegistryObject<EntityType<GreenBloomie>> GREEN_BLOOMIE = chara("green_bloomie", GreenBloomie::new, 0.65f, 2.29f);
    public static final RegistryObject<EntityType<GreenAlice>> GREEN_ALICE = chara("green_alice", GreenAlice::new, 0.7f, 2.51f);

    public static final RegistryObject<EntityType<GreenCircle>> GREEN_CIRCLE = chara("green_circle", GreenCircle::new, 0.75f, 2.62f);
    public static final RegistryObject<EntityType<HanselJuvenile>> HANSEL_JUVENILE = chara("hansel_juvenile", HanselJuvenile::new, 0.6f, 2.15f);
    public static final RegistryObject<EntityType<LordHansel>> LORD_HANSEL = chara("lord_hansel", LordHansel::new, 0.8f, 2.9f);

    public static final RegistryObject<EntityType<Riley>> RILEY = chara("riley", Riley::new, 0.6f, 1.94f);
    public static final RegistryObject<EntityType<DanielBarrel>> DANIEL_BARREL = chara("daniel_barrel", DanielBarrel::new, 0.75f, 2.58f);

    public static final RegistryObject<EntityType<FpeProjectile>> PROJECTILE = ENTITIES.register("projectile", () ->
            EntityType.Builder.<FpeProjectile>of(FpeProjectile::new, MobCategory.MISC).sized(0.4f, 0.4f).clientTrackingRange(8).updateInterval(1).build(FpeMod.MODID + ":projectile"));
    public static final RegistryObject<EntityType<FpeFx>> FX = ENTITIES.register("fx", () ->
            EntityType.Builder.<FpeFx>of(FpeFx::new, MobCategory.MISC).sized(0.5f, 0.5f).clientTrackingRange(10).updateInterval(20).fireImmune().build(FpeMod.MODID + ":fx"));

    /** all character types (for eggs, spawns, attributes) */
    @SuppressWarnings("unchecked")
    public static java.util.List<RegistryObject<? extends EntityType<? extends FpeEntity>>> characters() {
        return java.util.List.of(MISS_CIRCLE, MISS_THAVEL, MISS_BLOOMIE, ALICE, RED_CIRCLE, DANGER_THAVEL, DANGER_BLOOMIE, INFECTED_BLOOMIE, INFECTED_ZIP, DANGER_ALICE, FEN, AIDEN,
                MUTANT_CLAIRE, MUTANT_ENGEL, MUTANT_BUBBLE, MUTANT_LANA, MUTANT_ABBIE, GREEN_CIRCLE, HANSEL_JUVENILE, LORD_HANSEL, GREEN_THAVEL, GREEN_BLOOMIE, GREEN_ALICE, RILEY, DANIEL_BARREL);
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
            e.put(DANGER_ALICE.get(), DangerAlice.attributes().build());
            e.put(FEN.get(), Fen.attributes().build());
            e.put(AIDEN.get(), Aiden.attributes().build());
            e.put(RILEY.get(), Riley.attributes().build());
            e.put(DANIEL_BARREL.get(), DanielBarrel.attributes().build());
            e.put(GREEN_CIRCLE.get(), GreenCircle.attributes().build());
            e.put(HANSEL_JUVENILE.get(), HanselJuvenile.attributes().build());
            e.put(LORD_HANSEL.get(), LordHansel.attributes().build());
            e.put(MUTANT_CLAIRE.get(), MutantClaire.attributes().build());
            e.put(MUTANT_ENGEL.get(), MutantEngel.attributes().build());
            e.put(MUTANT_BUBBLE.get(), MutantBubble.attributes().build());
            e.put(MUTANT_LANA.get(), MutantLana.attributes().build());
            e.put(MUTANT_ABBIE.get(), MutantAbbie.attributes().build());
            e.put(GREEN_THAVEL.get(), GreenThavel.attributes().build());
            e.put(GREEN_BLOOMIE.get(), GreenBloomie.attributes().build());
            e.put(GREEN_ALICE.get(), GreenAlice.attributes().build());
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
