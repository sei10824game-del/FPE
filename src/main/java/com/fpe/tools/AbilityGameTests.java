package com.fpe.tools;

import java.util.List;

import com.fpe.entity.Ability;
import com.fpe.entity.FpeEntity;
import com.fpe.registry.ModEntities;

import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.monster.Zombie;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.Vec3;
import net.minecraftforge.gametest.GameTestHolder;
import net.minecraftforge.gametest.PrefixGameTestTemplate;

@GameTestHolder("fpe")
@PrefixGameTestTemplate(false)
public final class AbilityGameTests {
    @GameTest(template = "combat_empty")
    public static void pliersCannotGrabDodgedVictimThroughBystander(GameTestHelper h) {
        var aiden = h.spawn(ModEntities.AIDEN.get(), 5, 2, 2);
        aiden.setNoAi(true);
        aiden.setNoGravity(true);
        Zombie victim = target(h, 5, 7), bystander = target(h, 5, 5);
        aiden.setTarget(victim);
        aiden.forceAbility("pliers");
        aiden.animTime = 10;
        aiden.tick(); // Last tracking tick: let the committed victim dodge after this.
        victim.setPos(victim.position().add(3, 0, 0));
        Vec3 untouched = victim.position();
        float before = bystander.getHealth();
        aiden.tick();
        h.assertTrue(bystander.getHealth() < before, "Pliers must really hit the bystander on the old line");
        aiden.tick();
        h.assertTrue(victim.position().equals(untouched) && victim.getDeltaMovement().equals(Vec3.ZERO)
                && !victim.hasEffect(net.minecraft.world.effect.MobEffects.MOVEMENT_SLOWDOWN),
                "Dodged victim must not be grabbed because somebody else was hit");
        h.succeed();
    }

    @GameTest(template = "combat_empty")
    public static void snareRequiresDamageToItsOwnVictim(GameTestHelper h) {
        var alice = h.spawn(ModEntities.DANGER_ALICE.get(), 5, 2, 2);
        alice.setNoAi(true);
        alice.setNoGravity(true);
        Zombie victim = target(h, 5, 7), bystander = target(h, 5, 5);
        victim.setInvulnerable(true);
        Vec3 untouched = victim.position();
        alice.setTarget(victim);
        alice.forceAbility("bandage_snare");
        alice.animTime = 12;
        float before = bystander.getHealth();
        alice.tick();
        h.assertTrue(bystander.getHealth() < before, "Snare line must actually damage another mob");
        alice.tick();
        h.assertTrue(victim.position().equals(untouched), "Protected victim must not be teleported when only a bystander was hit");
        h.succeed();
    }

    @GameTest(template = "combat_empty")
    public static void pliersStillGrabActualVictim(GameTestHelper h) {
        var aiden = h.spawn(ModEntities.AIDEN.get(), 5, 2, 2);
        aiden.setNoAi(true);
        aiden.setNoGravity(true);
        Zombie victim = target(h, 5, 6);
        aiden.setTarget(victim);
        aiden.forceAbility("pliers");
        aiden.animTime = 11;
        aiden.tick();
        aiden.tick();
        h.assertTrue(victim.hasEffect(net.minecraft.world.effect.MobEffects.MOVEMENT_SLOWDOWN)
                && victim.getDeltaMovement().lengthSqr() > 0, "Direct pliers contact must still reel the struck victim in");
        h.succeed();
    }

    @GameTest(template = "combat_empty")
    public static void grabDoesNotTransferWithAggro(GameTestHelper h) {
        var grabber = h.spawn(ModEntities.DANIEL_BARREL.get(), 5, 2, 5);
        grabber.setNoAi(true);
        grabber.setNoGravity(true);
        Zombie first = target(h, 5, 6), second = target(h, 9, 9);
        grabber.setTarget(first);
        grabber.forceAbility("fang_bite");
        grabber.animTime = 12;
        float before = first.getHealth();
        grabber.tick();
        h.assertTrue(first.getHealth() < before, "First target must be successfully grabbed");
        Vec3 untouched = second.position();
        float secondHealth = second.getHealth();
        first.setDeltaMovement(Vec3.ZERO);
        second.setDeltaMovement(Vec3.ZERO);
        grabber.setTarget(second);
        grabber.tick();
        h.assertTrue(second.position().equals(untouched) && second.getHealth() == secondHealth
                        && second.getDeltaMovement().equals(Vec3.ZERO),
                "New aggro target must not inherit the grab");
        h.assertTrue(first.getDeltaMovement().y > 0, "Original victim must remain held");
        grabber.cancelAbility();
        first.setPos(first.position().add(3, 0, 0));
        first.setDeltaMovement(Vec3.ZERO);
        Vec3 released = first.position();
        grabber.tick();
        h.assertTrue(first.position().equals(released) && first.getDeltaMovement().equals(Vec3.ZERO),
                "Cancelled grab must release its victim");
        h.succeed();
    }

    @GameTest(template = "combat_empty")
    public static void invalidVictimAbortsAttack(GameTestHelper h) {
        Probe actor = new Probe(h.getLevel());
        Zombie victim = target(h, 5, 6), replacement = target(h, 9, 9);
        actor.setTarget(victim);
        actor.forceAbility("observe");
        victim.discard();
        actor.setTarget(replacement);
        actor.tick();
        h.assertTrue(!actor.isBusy() && actor.observed == null, "Removed pinned victim must abort callbacks");
        h.succeed();
    }

    @GameTest(template = "combat_empty")
    public static void callbackTransitionsKeepTheirTimeline(GameTestHelper h) {
        Probe actor = new Probe(h.getLevel());
        actor.setTarget(target(h, 5, 6));
        actor.forceAbility("cancel");
        actor.tick();
        h.assertTrue(!actor.isBusy() && actor.animTime == 0, "Callback cancellation must not advance stale animation");
        actor.forceAbility("chain");
        actor.tick();
        h.assertTrue(actor.currentAbilityId().equals("observe") && actor.animTime == 0,
                "End callback must be able to start a fresh ability");
        actor.tick();
        h.assertTrue(actor.observed == actor.getTarget(), "Chained ability must retain its own target");
        actor.forceAbility("restart");
        actor.tick();
        h.assertTrue(actor.animTime == 0, "Same-ability restart must not advance old timeline");
        h.succeed();
    }

    @GameTest(template = "combat_empty")
    public static void callbacksRejectInvalidTargets(GameTestHelper h) {
        Probe actor = new Probe(h.getLevel());
        Zombie victim = target(h, 5, 6);
        victim.discard();
        actor.setTarget(victim);
        h.assertTrue(!actor.forceAbility("start_observe"), "Forced attacks must reject invalid victims");
        h.assertTrue(actor.observed == null && !actor.isBusy(), "Invalid victim must not reach onStart");
        actor.setTarget(target(h, 5, 6));
        actor.forceAbility("finish_kill");
        actor.tick();
        h.assertTrue(!actor.isBusy() && !actor.ended, "Victim removed on final tick must not reach onEnd");
        h.succeed();
    }

    @GameTest(template = "combat_empty")
    public static void targetlessTransformationAnimation(GameTestHelper h) {
        Probe actor = new Probe(h.getLevel());
        actor.forceAbility("transform");
        actor.tick();
        h.assertTrue(actor.isBusy() && actor.animTime == 1, "Pure transformation animation must run without a victim");
        actor.tick();
        actor.tick();
        h.assertTrue(!actor.isBusy(), "Pure transformation animation must finish normally");
        h.succeed();
    }

    private static Zombie target(GameTestHelper h, int x, int z) {
        Zombie mob = h.spawn(EntityType.ZOMBIE, x, 2, z);
        mob.setNoAi(true);
        mob.setNoGravity(true);
        return mob;
    }

    private static final class Probe extends FpeEntity {
        private LivingEntity observed;
        private boolean ended;
        Probe(Level level) { super(ModEntities.MISS_CIRCLE.get(), level); setNoAi(true); setNoGravity(true); }
        @Override protected void registerAbilities(List<Ability> out) {
            out.add(Ability.of("observe", 5, 0).tick((e, t, k) -> ((Probe) e).observed = t));
            out.add(Ability.of("cancel", 5, 0).tick((e, t, k) -> e.cancelAbility()));
            out.add(Ability.of("chain", 1, 0).end((e, t, k) -> e.forceAbility("observe")));
            out.add(Ability.of("restart", 5, 0).tick((e, t, k) -> e.forceAbility("restart")));
            out.add(Ability.of("transform", 3, 0));
            out.add(Ability.of("start_observe", 3, 0).start((e, t, k) -> ((Probe) e).observed = t));
            out.add(Ability.of("finish_kill", 1, 0).tick((e, t, k) -> t.discard())
                    .end((e, t, k) -> ((Probe) e).ended = true));
        }
    }
}
