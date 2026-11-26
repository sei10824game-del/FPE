package com.fpe.tools;

import com.fpe.entity.FpeProjectile;
import com.fpe.entity.characters.ZombieAuCharacter;
import com.fpe.entity.characters.ZombieAuCharacter.Role;
import com.fpe.registry.ModEntities;
import net.minecraft.gametest.framework.GameTest;
import net.minecraft.gametest.framework.GameTestHelper;
import net.minecraft.world.level.block.Blocks;
import net.minecraft.world.phys.Vec3;
import net.minecraftforge.gametest.GameTestHolder;
import net.minecraftforge.gametest.PrefixGameTestTemplate;

@GameTestHolder("fpe")
@PrefixGameTestTemplate(false)
public final class ZombieAuChainsawGameTests {
    @GameTest(template="combat_empty")
    public static void chainsawMaintainsContactWithoutEveryTickDamage(GameTestHelper h) {
        var circle=actor(h,Role.SURVIVOR_CIRCLE,5,2);
        var target=actor(h,Role.ZOMBIE_OLIVER,5,4);
        circle.setTarget(target);circle.forceAbility("signature");
        float before=target.getHealth();
        circle.animTime=23;circle.tick();
        h.assertTrue(target.getHealth()==before,"Revving must telegraph the first chain contact");
        circle.tick();float first=target.getHealth();
        h.assertTrue(first<before,"First contact must deal damage");
        // A source with a slower hit cadence must not prevent the moving chain's next real contact.
        target.invulnerableTime=100;
        for(int tick=25;tick<=27;tick++){circle.animTime=tick;circle.tick();}
        h.assertTrue(target.getHealth()==first,"Damage must not run every tick between chain teeth contacts");
        circle.animTime=28;circle.tick();float second=target.getHealth();
        h.assertTrue(second<first,"A second contact must cut again inside ordinary hurt cooldown");
        target.invulnerableTime=100;circle.animTime=32;circle.tick();
        h.assertTrue(target.getHealth()<second,"Sustained contact must continue beyond two isolated swings");
        float last=target.getHealth();circle.animTime=41;circle.tick();
        h.assertTrue(target.getHealth()==last,"Recovery must stop chain damage");
        h.succeed();
    }

    @GameTest(template="combat_empty")
    public static void chainsawProtectsAlliesAndDoesNotClearTheirCooldown(GameTestHelper h) {
        var circle=actor(h,Role.SURVIVOR_CIRCLE,5,2);
        var target=actor(h,Role.ZOMBIE_OLIVER,5,4);
        var ally=actor(h,Role.SURVIVOR_RILEY,5,3);
        ally.invulnerableTime=100;
        circle.setTarget(target);circle.forceAbility("signature");
        circle.animTime=24;circle.tick();
        h.assertTrue(target.getHealth()<target.getMaxHealth(),"Chain must still reach a hostile victim in the segment");
        h.assertTrue(ally.getHealth()==ally.getMaxHealth(),"Continuous chain must not damage allies");
        h.assertTrue(ally.invulnerableTime==100,"Missed and allied entities must retain their own hurt cooldown");
        h.succeed();
    }

    @GameTest(template="combat_empty")
    public static void chainsawCannotReachThroughCoverOrBehindItsOwner(GameTestHelper h) {
        var circle=actor(h,Role.SURVIVOR_CIRCLE,5,2);
        var target=actor(h,Role.ZOMBIE_OLIVER,5,5);
        var behind=actor(h,Role.ZOMBIE_LANA,5,1);
        for(int x=3;x<=7;x++)for(int y=2;y<=7;y++)h.setBlock(x,y,4,Blocks.STONE);
        target.invulnerableTime=100;behind.invulnerableTime=100;
        circle.setTarget(target);circle.forceAbility("signature");
        circle.animTime=24;circle.tick();circle.animTime=28;circle.tick();
        h.assertTrue(target.getHealth()==target.getMaxHealth(),"A solid wall must stop sustained blade contact");
        h.assertTrue(behind.getHealth()==behind.getMaxHealth(),"Engine activity must not become a full-radius damage aura");
        h.assertTrue(target.invulnerableTime==100&&behind.invulnerableTime==100,"Non-contact victims must retain cooldowns");
        h.assertBlockPresent(Blocks.STONE,5,3,4);h.succeed();
    }

    @GameTest(template="combat_empty")
    public static void chainsawRushUsesBoundedMovementAndStopsWhenBlocked(GameTestHelper h) {
        var circle=actor(h,Role.SURVIVOR_CIRCLE,5,2);
        var target=actor(h,Role.ZOMBIE_OLIVER,5,8);
        circle.setTarget(target);circle.forceAbility("lunge");
        Vec3 start=circle.position();circle.animTime=10;circle.tick();
        h.assertTrue(circle.position().distanceToSqr(start)<.001,"Starting a rush must apply velocity rather than teleporting");
        h.assertTrue(circle.getDeltaMovement().z>0&&circle.getDeltaMovement().horizontalDistance()<=.701,"Rush speed must be bounded and toward the target");
        circle.setDeltaMovement(Vec3.ZERO);
        for(int x=3;x<=7;x++)for(int y=2;y<=7;y++)h.setBlock(x,y,4,Blocks.STONE);
        circle.animTime=14;circle.tick();
        h.assertTrue(circle.getDeltaMovement().horizontalDistance()<.001,"Rush must stop applying forward impulses through solid cover");
        h.assertBlockPresent(Blocks.STONE,5,3,4);h.succeed();
    }

    @GameTest(template="combat_empty")
    public static void gracePistolFiresOnlyThreeTimedBullets(GameTestHelper h) {
        var grace=actor(h,Role.SURVIVOR_GRACE,5,2);
        var target=actor(h,Role.ZOMBIE_OLIVER,5,8);
        grace.setTarget(target);grace.forceAbility("volley");
        for(int tick=0;tick<42;tick++){
            grace.animTime=tick;grace.tick();
            var shots=h.getLevel().getEntitiesOfClass(FpeProjectile.class,grace.getBoundingBox().inflate(3),p->p.getOwner()==grace);
            int expected=tick<18?0:tick<24?1:tick<30?2:3;
            h.assertTrue(shots.size()==expected,"Pistol volley must fire at18/24/30 only, without automatic-fire leakage");
            for(var shot:shots)h.assertTrue(shot.kind()==FpeProjectile.Kind.BULLET,"Grace must fire pistol bullets");
        }
        h.succeed();
    }

    @GameTest(template="combat_empty")
    public static void survivorTeachersStandAboveTheirStudents(GameTestHelper h) {
        var teachers=java.util.EnumSet.of(Role.SURVIVOR_GRACE,Role.SURVIVOR_DEMI,Role.SURVIVOR_SASHA,
                Role.SURVIVOR_THAVEL,Role.SURVIVOR_CIRCLE,Role.SURVIVOR_BLOOMIE);
        float tallestStudent=0;
        for(Role role:Role.values())if(role.survivor()&&!teachers.contains(role)){
            var student=actor(h,role,5,5);tallestStudent=Math.max(tallestStudent,student.getBbHeight());student.discard();
        }
        for(Role role:teachers){
            var teacher=actor(h,role,5,5);
            h.assertTrue(teacher.getBbHeight()>tallestStudent+.15f,"Every survivor teacher must clearly exceed even the tallest survivor student");
            teacher.discard();
        }
        h.succeed();
    }

    private static ZombieAuCharacter actor(GameTestHelper h,Role role,int x,int z) {
        var actor=h.spawn(ModEntities.ZOMBIE_AU.get(role).get(),x,2,z);
        actor.setNoAi(true);actor.setNoGravity(true);return actor;
    }
}
