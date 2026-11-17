package com.fpe.tools;

import java.util.UUID;

import com.fpe.entity.FpeUtil;
import com.fpe.registry.ModEffects;
import com.mojang.authlib.GameProfile;

import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.monster.Zombie;
import net.minecraft.world.level.GameType;
import net.minecraft.world.phys.Vec3;
import net.minecraftforge.common.util.FakePlayer;
import net.minecraftforge.gametest.GameTestHolder;
import net.minecraftforge.gametest.PrefixGameTestTemplate;

@GameTestHolder("fpe")
@PrefixGameTestTemplate(false)
public final class CrowdControlGameTests {
    @GameTest(template = "combat_empty")
    public static void rootedGroundJumps(GameTestHelper h) {
        JumpingZombie mob = new JumpingZombie(h.getLevel());
        mob.setSprinting(true);
        mob.jump();
        h.assertTrue(mob.getDeltaMovement().y > 0, "Unrooted ground jump must work");
        FpeUtil.root(mob, 10);
        mob.jump();
        h.assertTrue(mob.getDeltaMovement().equals(Vec3.ZERO), "Root must remove jump and sprint impulse");

        JumpingPlayer player = new JumpingPlayer(h.getLevel());
        player.setGameMode(GameType.SURVIVAL);
        player.setSprinting(true);
        FpeUtil.root(player, 10);
        h.assertTrue(player.hasEffect(ModEffects.ROOTED.get()), "Survival player must receive synced root effect");
        player.jump();
        h.assertTrue(player.getDeltaMovement().equals(Vec3.ZERO), "Player ground jump must be suppressed");
        player.removeEffect(ModEffects.ROOTED.get());
        player.jump();
        h.assertTrue(player.getDeltaMovement().y > 0, "Jump must return when root is removed");
        player.removeAllEffects();
        player.setGameMode(GameType.CREATIVE);
        FpeUtil.stun(player, 10);
        h.assertTrue(!player.hasEffect(ModEffects.ROOTED.get()), "Creative player must remain immune");
        h.succeed();
    }

    @GameTest(template = "combat_empty")
    public static void rootExpiresWithoutStealingJumpBoost(GameTestHelper h) {
        Zombie mob = h.spawn(EntityType.ZOMBIE, 5, 2, 5);
        mob.setNoAi(true);
        mob.setNoGravity(true);
        mob.addEffect(new MobEffectInstance(MobEffects.JUMP, 100, 2));
        FpeUtil.root(mob, 4);
        h.assertTrue(mob.getEffect(MobEffects.JUMP).getAmplifier() == 2, "Root must preserve existing Jump Boost");
        h.assertTrue(mob.hasEffect(ModEffects.ROOTED.get()), "Root must be active before expiry");
        h.runAtTickTime(7, () -> {
            h.assertTrue(!mob.hasEffect(ModEffects.ROOTED.get()), "Root must expire through normal effect ticks");
            h.assertTrue(mob.hasEffect(MobEffects.JUMP) && mob.getEffect(MobEffects.JUMP).getAmplifier() == 2,
                    "Jump Boost must remain after root expires");
            h.succeed();
        });
    }

    @GameTest(template = "combat_empty")
    public static void stunAndRootSemantics(GameTestHelper h) {
        JumpingZombie rooted = new JumpingZombie(h.getLevel());
        FpeUtil.root(rooted, 10);
        h.assertTrue(!rooted.hasEffect(MobEffects.JUMP), "Root must not create Jump Boost");
        h.assertTrue(!rooted.hasEffect(MobEffects.WEAKNESS), "Root must allow fighting back");
        h.assertTrue(!rooted.hasEffect(MobEffects.DIG_SLOWDOWN), "Root must not add stun fatigue");
        JumpingZombie stunned = new JumpingZombie(h.getLevel());
        FpeUtil.stun(stunned, 10);
        h.assertTrue(stunned.hasEffect(ModEffects.ROOTED.get()), "Stun must suppress ground jumps");
        h.assertTrue(stunned.hasEffect(MobEffects.WEAKNESS) && stunned.hasEffect(MobEffects.DIG_SLOWDOWN),
                "Stun must retain weakness and fatigue");
        h.assertTrue(!stunned.hasEffect(MobEffects.JUMP), "Stun must not create Jump Boost");
        JumpingZombie untouched = new JumpingZombie(h.getLevel());
        FpeUtil.root(untouched, 0);
        FpeUtil.stun(untouched, -1);
        h.assertTrue(untouched.getActiveEffects().isEmpty(), "Non-positive durations must not apply effects");
        h.succeed();
    }

    private static final class JumpingZombie extends Zombie {
        JumpingZombie(ServerLevel level) { super(EntityType.ZOMBIE, level); }
        void jump() { jumpFromGround(); }
    }

    private static final class JumpingPlayer extends FakePlayer {
        JumpingPlayer(ServerLevel level) { super(level, new GameProfile(UUID.randomUUID(), "FpeJumpTest")); }
        void jump() { jumpFromGround(); }
    }
}
