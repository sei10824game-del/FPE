package com.fpe.tools;

import com.fpe.entity.FpeEntity;
import com.fpe.entity.FpeProjectile;
import com.fpe.entity.FpeUtil;
import com.fpe.registry.ModEntities;

import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.phys.Vec3;
import net.minecraftforge.gametest.GameTestHolder;
import net.minecraftforge.gametest.PrefixGameTestTemplate;

@GameTestHolder("fpe")
@PrefixGameTestTemplate(false)
public final class ProjectileGameTests {
    @GameTest(template = "combat_empty")
    public static void rocketDetonatesAtWall(GameTestHelper h) {
        FpeEntity owner = stationary(h, ModEntities.MISS_CIRCLE.get(), 1.5, 5.5);
        FpeEntity enemy = stationary(h, ModEntities.RED_CIRCLE.get(), 7.9, 8.7);
        FpeEntity ally = stationary(h, ModEntities.MISS_THAVEL.get(), 7.9, 3.5);
        h.setBlock(8, 3, 5, Blocks.STONE);
        FpeProjectile rocket = launch(h, owner, FpeProjectile.Kind.ROCKET, 6.45, 1.6);
        float enemyHealth = enemy.getHealth(), allyHealth = ally.getHealth();

        rocket.tick();

        h.assertTrue(rocket.isRemoved(), "Rocket must detonate on impact");
        assertImpactX(h, rocket, 7.9);
        h.assertTrue(enemy.getHealth() < enemyHealth, "Blast must reach the enemy at the impact site");
        h.assertTrue(ally.getHealth() == allyHealth, "Blast must protect allied FPE");
        h.assertBlockPresent(Blocks.STONE, 8, 3, 5);
        h.succeed();
    }

    @GameTest(template = "combat_empty")
    public static void directFireballDetonatesAtContact(GameTestHelper h) {
        FpeEntity owner = stationary(h, ModEntities.MISS_CIRCLE.get(), 1.5, 5.5);
        FpeEntity enemy = stationary(h, ModEntities.RED_CIRCLE.get(), 7.5, 5.5);
        FpeProjectile fireball = launch(h, owner, FpeProjectile.Kind.FIREBALL, 4.5, 3.0);
        float before = enemy.getHealth();
        double contactX = enemy.getBoundingBox().minX - 0.3f;

        fireball.tick();

        h.assertTrue(fireball.isRemoved(), "Fireball must detonate on a direct hit");
        h.assertTrue(Math.abs(fireball.getX() - contactX) < 0.001, "Explosion must start at the swept contact");
        h.assertTrue(enemy.getHealth() < before, "A direct hit must damage the enemy outside the launch position's blast radius");
        h.succeed();
    }

    @GameTest(template = "combat_empty")
    public static void boomerangsReflectAtWall(GameTestHelper h) {
        FpeEntity owner = stationary(h, ModEntities.MISS_CIRCLE.get(), 1.5, 5.5);
        h.setBlock(5, 3, 5, Blocks.STONE);
        for (FpeProjectile.Kind kind : new FpeProjectile.Kind[] {FpeProjectile.Kind.AXE, FpeProjectile.Kind.COMPASS}) {
            FpeProjectile shot = launch(h, owner, kind, 4.5, 1.2);

            shot.tick();

            h.assertTrue(!shot.isRemoved() && shot.getDeltaMovement().x < 0, kind + " must reverse at the wall");
            assertImpactX(h, shot, 4.9);
            double impactX = shot.getX();
            shot.tick();
            h.assertTrue(shot.getX() < impactX, kind + " must return on the next tick");
            shot.discard();
        }
        h.succeed();
    }

    @GameTest(template = "combat_empty")
    public static void grenadeBouncesOnFollowingTick(GameTestHelper h) {
        FpeEntity owner = stationary(h, ModEntities.MISS_CIRCLE.get(), 1.5, 5.5);
        h.setBlock(5, 3, 5, Blocks.STONE);
        FpeProjectile grenade = launch(h, owner, FpeProjectile.Kind.GRENADE, 4.5, 1.0);

        grenade.tick();

        h.assertTrue(!grenade.isRemoved() && grenade.getDeltaMovement().x < 0, "Grenade must reflect at the wall");
        assertImpactX(h, grenade, 4.9);
        double impactX = grenade.getX();
        grenade.tick();
        h.assertTrue(grenade.getX() < impactX, "Grenade must move along the rebound on the next tick");
        grenade.discard();
        h.succeed();
    }

    @GameTest(template = "combat_empty")
    public static void knifeKeepsPreviousFlightAngles(GameTestHelper h) {
        FpeEntity owner = stationary(h, ModEntities.MISS_CIRCLE.get(), 1.5, 5.5);
        Vec3 start = h.absoluteVec(new Vec3(4.5, 3.4, 5.5));
        FpeProjectile knife = FpeUtil.projectile(owner, FpeProjectile.Kind.KNIFE, start, new Vec3(1, 0.5, 0), 10);
        float launchPitch = (float) -Math.toDegrees(Math.atan(0.5));
        h.assertTrue(knife.getYRot() == -90 && Math.abs(knife.getXRot() - launchPitch) < 0.001,
                "Knife must face its launch velocity before its first tick");
        h.assertTrue(knife.yRotO == knife.getYRot() && knife.xRotO == knife.getXRot(),
                "Knife must initialize both previous flight angles at launch");

        knife.tick();

        h.assertTrue(knife.getXRot() > launchPitch + 0.1, "Gravity must pitch the knife down");
        h.assertTrue(knife.yRotO == -90 && Math.abs(knife.xRotO - launchPitch) < 0.001,
                "Rendering must retain the launch angles for interpolation after the first tick");
        knife.discard();
        h.succeed();
    }

    private static <T extends FpeEntity> T stationary(GameTestHelper h, EntityType<T> type, double x, double z) {
        T entity = h.spawn(type, new Vec3(x, 2, z));
        entity.setNoAi(true);
        entity.setNoGravity(true);
        return entity;
    }

    private static FpeProjectile launch(GameTestHelper h, FpeEntity owner, FpeProjectile.Kind kind, double x, double speed) {
        Vec3 start = h.absoluteVec(new Vec3(x, 3.4, 5.5));
        return FpeUtil.projectile(owner, kind, start, new Vec3(speed, 0, 0), 10);
    }

    private static void assertImpactX(GameTestHelper h, FpeProjectile projectile, double x) {
        double expected = h.absoluteVec(new Vec3(x, 3.4, 5.5)).x;
        h.assertTrue(Math.abs(projectile.getX() - expected) < 0.001, projectile.kind() + " must stop just before the wall on impact");
    }
}
