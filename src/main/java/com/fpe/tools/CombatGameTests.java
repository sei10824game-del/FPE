package com.fpe.tools;

import com.fpe.entity.FpeEntity;
import com.fpe.entity.FpeFx;
import com.fpe.entity.FpeProjectile;
import com.fpe.entity.FpeUtil;
import com.fpe.registry.ModEntities;

import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.Mob;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.EntityHitResult;
import net.minecraftforge.gametest.GameTestHolder;
import net.minecraftforge.gametest.PrefixGameTestTemplate;

/** Real server regression tests: ./gradlew runGameTestServer --no-daemon. */
@GameTestHolder("fpe")
@PrefixGameTestTemplate(false)
public final class CombatGameTests {
    @GameTest(template = "combat_empty")
    public static void attackOwnership(GameTestHelper h) {
        FpeEntity owner = stationary(h, ModEntities.MISS_CIRCLE.get(), 1, 1);
        FpeEntity ally = stationary(h, ModEntities.MISS_THAVEL.get(), 2, 1);
        FpeEntity neutral = stationary(h, ModEntities.ALICE.get(), 3, 1);
        FpeEntity enemy = stationary(h, ModEntities.RED_CIRCLE.get(), 5, 5);
        Mob zombie = stationary(h, EntityType.ZOMBIE, 8, 8);
        TestProjectile shot = new TestProjectile(h.getLevel());
        shot.setOwner(owner);
        FpeFx fx = new FpeFx(ModEntities.FX.get(), h.getLevel());
        fx.setOwner(owner);
        for (var source : new net.minecraft.world.entity.Entity[] {owner, shot, fx}) {
            h.assertTrue(!FpeUtil.canHurt(source, owner), "Attack must protect its owner");
            h.assertTrue(!FpeUtil.canHurt(source, ally), "Attack must protect same faction");
            h.assertTrue(!FpeUtil.canHurt(source, neutral), "Attack must protect non-hostile faction");
            h.assertTrue(FpeUtil.canHurt(source, enemy), "Attack must hit hostile faction");
            h.assertTrue(FpeUtil.canHurt(source, zombie), "Attack must hit ordinary mobs");
        }
        h.assertTrue(FpeUtil.canHurt(zombie, owner), "Ordinary mobs are not FPE allies");
        h.assertTrue(shot.canHit(enemy), "Direct projectile must hit hostile faction");
        h.assertTrue(!shot.canHit(ally) && !shot.canHit(owner), "Direct projectile must protect allies and owner");
        TestProjectile orphanShot = new TestProjectile(h.getLevel());
        h.assertTrue(!FpeUtil.canHurt(orphanShot, enemy), "Unresolved projectile must protect FPE");
        h.assertTrue(!orphanShot.canHit(enemy), "Unresolved direct projectile must protect FPE");
        FpeFx orphan = new FpeFx(ModEntities.FX.get(), h.getLevel());
        h.assertTrue(!FpeUtil.canHurt(orphan, enemy), "Unresolved effect must protect FPE");
        h.succeed();
    }

    @GameTest(template = "combat_empty")
    public static void explosiveFactionDamage(GameTestHelper h) {
        FpeEntity owner = stationary(h, ModEntities.MISS_CIRCLE.get(), 5, 5);
        FpeEntity ally = stationary(h, ModEntities.MISS_THAVEL.get(), 6, 5);
        FpeEntity enemy = stationary(h, ModEntities.RED_CIRCLE.get(), 5, 6);
        float before = enemy.getHealth(), alliedBefore = ally.getHealth(), ownerBefore = owner.getHealth();
        TestProjectile rocket = new TestProjectile(h.getLevel());
        rocket.setOwner(owner);
        rocket.setKind(FpeProjectile.Kind.ROCKET);
        rocket.setDamage(10);
        rocket.setPos(enemy.position());
        rocket.impact(enemy);
        h.assertTrue(enemy.getHealth() < before, "Explosion must damage hostile FPE");
        h.assertTrue(ally.getHealth() == alliedBefore, "Explosion must protect allies");
        h.assertTrue(owner.getHealth() == ownerBefore, "Explosion must protect its owner");
        h.succeed();
    }

    @GameTest(template = "combat_empty")
    public static void zeroWarmupEffects(GameTestHelper h) {
        FpeEntity owner = stationary(h, ModEntities.MISS_CIRCLE.get(), 1, 1);
        FpeEntity ally = stationary(h, ModEntities.MISS_THAVEL.get(), 6, 5);
        FpeEntity enemy = stationary(h, ModEntities.RED_CIRCLE.get(), 5, 5);
        for (FpeFx.Kind kind : new FpeFx.Kind[] {FpeFx.Kind.SPIKE, FpeFx.Kind.RING_TRAP, FpeFx.Kind.TENTACLE}) {
            enemy.setHealth(enemy.getMaxHealth());
            enemy.invulnerableTime = 0;
            float before = enemy.getHealth(), alliedBefore = ally.getHealth();
            FpeFx fx = new FpeFx(ModEntities.FX.get(), h.getLevel());
            fx.setOwner(owner);
            fx.setPos(enemy.position());
            fx.setup(kind, 0, 12, 2, 10);
            h.assertTrue(fx.warmup() == 1, kind + " must sync first-tick warmup");
            fx.tickCount = 1;
            fx.tick();
            h.assertTrue(enemy.getHealth() < before, kind + " must hit on first tick");
            h.assertTrue(ally.getHealth() == alliedBefore, kind + " must protect allied faction");
            float after = enemy.getHealth();
            for (int t = 2; t <= 12; t++) {
                enemy.invulnerableTime = 0;
                fx.tickCount = t;
                fx.tick();
            }
            h.assertTrue(enemy.getHealth() == after, kind + " must not repeat before its next interval");
        }
        h.succeed();
    }

    @GameTest(template = "combat_empty")
    public static void delayedSpike(GameTestHelper h) {
        FpeEntity owner = stationary(h, ModEntities.MISS_CIRCLE.get(), 1, 1);
        FpeEntity enemy = stationary(h, ModEntities.RED_CIRCLE.get(), 5, 5);
        float before = enemy.getHealth();
        FpeFx fx = new FpeFx(ModEntities.FX.get(), h.getLevel());
        fx.setOwner(owner);
        fx.setPos(enemy.position());
        fx.setup(FpeFx.Kind.SPIKE, 4, 12, 2, 10);
        for (int t = 1; t < 4; t++) { fx.tickCount = t; fx.tick(); }
        h.assertTrue(enemy.getHealth() == before, "Warmup must not damage early");
        fx.tickCount = 4;
        fx.tick();
        h.assertTrue(enemy.getHealth() < before, "Spike must erupt at configured tick");
        h.succeed();
    }

    private static <T extends Mob> T stationary(GameTestHelper h, EntityType<T> type, int x, int z) {
        T mob = h.spawn(type, x, 2, z);
        mob.setNoAi(true);
        mob.setNoGravity(true);
        return mob;
    }

    private static final class TestProjectile extends FpeProjectile {
        TestProjectile(Level level) { super(ModEntities.PROJECTILE.get(), level); }
        void impact(Mob victim) { onHitEntity(new EntityHitResult(victim)); }
        boolean canHit(Mob victim) { return canHitEntity(victim); }
    }
}
