#!/bin/bash
cd "$(dirname "$0")/.." || exit 1
C="USER REQUEST: add CROWD-CONTROL attacks that affect what the victim can do (grabs, holds, pins, stuns, pulls, disarm, daze, fear). Framework helpers (already written in entity/FpeUtil.java, use them): FpeUtil.stun(victim,ticks) (cannot walk/jump), root(victim,ticks), daze(victim,ticks), hold(grabber,victim,fwd,up,side) / holdAt(victim,pos) (call EVERY tick of a grab: teleports + zeroes motion, players synced), pull(victim,toward,speed), fling(victim,dir,speed,up), disarm(victim). Add 2-3 such attacks to this character, each with its own fully authored animation (grab = reach, snatch, hold pose with the victim in front of/above her, hits or squeeze, throw/slam/release). Rules: pick the victim with the existing hit helpers (nearest valid enemy in a cone/line; skip if none), release on victim death / invalid / ability end, never grab creative/spectator players or FPE allies (FpeUtil.canHurt), use long cooldowns (120+ ticks) and weights so they are not spammy, keep damage sane, keep existing abilities (10-12+ total) and heights. Update only this character's Java class and its generator script/bbmodel."
tools/run_agent.sh mutant_bubble MutantBubble "$C Ideas: encase the target in a bubble that holds it floating/drifting, then pops and drops it."
tools/run_agent.sh mutant_lana MutantLana "$C Ideas: swallow the victim into the toothy bag (hold + chew) and tongue reel-in."
tools/run_agent.sh mutant_claire MutantClaire "$C Ideas: jaw-lock bite that holds the victim, and a howl that makes victims flee/daze."
tools/run_agent.sh green_bloomie GreenBloomie "$C Ideas: paralysing syringe injection (stun) and gas that dazes."
tools/run_agent.sh green_circle GreenCircle "$C Ideas: hose lasso that pulls the target in, then a choke hold."
tools/run_agent.sh riley Riley "$C Ideas: pin the victim with the knife (root) and an ambush grab-and-stab."
tools/run_agent.sh alice Alice "$C Apply to BOTH forms where it fits (phase 1: shadow hands that grab/root; phase 2 giant: a hand grab that lifts the victim and squeezes/slams, plus a tentacle bind). Keep all existing attacks, the quadruped mode and the boss plumbing."
tools/run_agent.sh infected_zip InfectedZip "$C Ideas: snatch the victim and carry it into the air (hold) then dive-bomb drop, and a wing-pin."
tools/run_agent.sh hansel_juvenile HanselJuvenile "$C Ideas: vine bind (root + daze) and pollen that dazes."
echo QUEUE_DONE
