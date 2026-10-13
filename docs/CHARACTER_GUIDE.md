# FPE mod – character author guide

Minecraft 1.20.1 / Forge 47.3.0 / official mappings / Java 17 toolchain. **No external libraries** (no GeckoLib):
models, textures and animations are procedural Java.  Vanilla particles & sounds only.

## What you own per character
* `src/main/java/com/fpe/entity/characters/<Name>.java` – attributes + abilities (server logic).
* `src/main/java/com/fpe/client/spec/<Name>Spec.java` – model + painted texture + animation (client).
Do not edit framework files (`FpeEntity`, `Ability`, `FpeUtil`, `FpeProjectile`, `FpeFx`, `ModelSpec`, renderers, registry…).
If you need a framework change, say so in your final report. You may add NEW helper files with your character's prefix.

## Build / check loop (do this, repeatedly)
```
./gradlew --no-daemon compileJava -q 2>&1 | grep -E "error|warning: \[" -A3     # first run is slow (minutes)
./gradlew --no-daemon preview -Pspec=<spec_name> -q                              # -> build/preview/<spec_name>.png + _tex.png
```
Then **Read the PNG** (the image) and fix what looks wrong. Rows: idle views (front / 3-4 / side / back) + two walk frames,
one row per ability sampled over its duration (6 frames, alternating camera angle), last row = death.
Spec names: miss_circle, miss_thavel, miss_bloomie, alice, alice_boss, red_circle, danger_thavel, danger_bloomie, fen, aiden.
Iterate until the model clearly resembles the reference art and every attack reads clearly (anticipation → strike → recovery).
Tool limits: preview does not show FX/particles/projectiles (see them by reasoning) and shows the glow layer as solid colour.

## Model (ModelSpec) – see `client/model/ModelSpec.java`
* +x = entity's LEFT, +y = DOWN, entity faces **-z**, ground is y=24, 1 px = 1/16 block. Hitbox is set in `registry/ModEntities.java`
  (a normal 2-block character is ~32 px tall; keep the visual size consistent with the hitbox; hair / hats may exceed it a little).
* `group(name,parent,px,py,pz)` = pivot node, `part(name,parent,px,py,pz, ox,oy,oz, w,h,d, 0xRRGGBB)` = box.
  Pivots are absolute model coords, boxes are relative to their pivot. Parents must be declared first. Part names are unique.
  Always start with `group("root", null, 0,24,0)` and hang everything under it (so you can crouch/lean the whole body).
* Parts take `.rot(xDeg,yDeg,zDeg)` default rotation (use it for spikes, hair locks, tilted hats), `.inflate()`, `.pattern(...)`
  (stripes, check, gradient), `.decor(Face,x,y,w,h,color)` (paint pixels on a face: eyes, teeth, buttons, seams, stitches, blood…),
  `.glow()` / `.decorGlow(...)` (emissive layer: eyes, fire, lights).
* The texture is generated from the spec, no PNG files. Boxes with the same colour look flat – use shading colours, patterns, decor,
  extra thin boxes for trims/cuffs/belts/buttons, and several rotated boxes to fake hair spikes, cloaks, capes, wings, claws.
* Aim for 40-80 parts per character. Read the reference image(s) carefully: silhouette, hair, hat, clothes, colours, accessories, expression
  (sharp teeth grin etc.). Blocky-but-recognisable beats generic.

## Animation (Animator) – `modelSpec.animator((m, c) -> {...})`, called each frame after parts reset to default pose
* `m.rot(name,xDeg,yDeg,zDeg)`, `m.addRot`, `m.move`, `m.scale`, `m.show/hide`. Unknown names are ignored (no crash).
* `AnimCtx c`: `c.age` (ticks, for idle loops), `c.limbSwing`/`c.limbAmt`/`c.walk()` (0..1), `c.headYaw`/`c.headPitch` (degrees; make the head look at the target),
  `c.ability` (id of running ability, "" when idle; `c.is("sweep")`), `c.t` ticks since the ability started (float, includes partial tick),
  `c.dur`, `c.p()` 0..1 progress, `c.seg(a,b)` 0..1 progress between ticks a and b, `c.death` 0..1, `c.variant`.
* `Anim.curve(t, t0,v0, t1,v1, ...)` smooth keyframes (degrees), `Anim.linear`, `Anim.smooth/easeOut/easeIn`, `Anim.sin(deg)`, `Anim.sinr(rad)`.
* Quality bar: **no tacked-on animation**. Every ability needs its own full-body pose sequence: anticipation (wind-up, weight shift, crouch, arm cocked back),
  strike (fast, overshoot, body rotation / lean / step), follow-through & recovery. Use body, hips, spine, head, both arms, legs, hair, cloth, accessories
  (secondary motion: hair/cape swaying with a phase lag). Idle must breathe/sway; walking must look like the character (stalking, skipping, crawling…).
  Death: collapse / crumble using `c.death`.
* The server `t` (tick index inside the ability) and the animation `c.t` are the same timeline – put damage / projectile / FX spawn on the tick where
  the strike pose peaks, and keep `Ability.duration` ≥ the animation length.

## Abilities (Ability / FpeEntity) – see `entity/Ability.java`, `FpeEntity.java`, `FpeUtil.java`
```java
@Override protected void registerAbilities(List<Ability> out) {
    out.add(Ability.of("sweep", 36 /*duration ticks*/, 80 /*cooldown*/).range(0, 5).weight(3)
        .start((e,t,tick)->{ ... }).tick((e, target, tick) -> { if (tick == 14) FpeUtil.hitCone(e, 4.5, 100, e.dmg(1.4f), 0.9, 0.35); }).end(...));
}
```
* The id string is what the animator switches on. Index+1 in the list is synced to the client automatically.
* `range(min,max)` = distance to target where it may be chosen; `.when(e -> e.isEnraged())` gating; `.moving()` = may keep walking; `.blind()` no line of sight needed;
  `.faceUntil(tick)` stops tracking the target after that tick (so dodges are possible). `target` is never null inside callbacks.
* Helpers: `e.dmg(mult)` (attack attribute × mult), `e.dashToward(pos,speed,vy)`, `e.dashForward`, `e.snapFace(target)`, `e.isEnraged()` (<50 % hp),
  `FpeUtil.hitCone / hitRadius / hitLine / arc (particle ring) / particles / sound / projectile(...) / fx(...) / aim(...) / forward / right / ahead / knock`.
* `FpeProjectile.Kind` (see enum for behaviour): COMPASS & AXE boomerangs, PENCIL, GRENADE, BOMBLET, ROCKET, BULLET, SHADOW_ORB (homing), DIAMOND, KNIFE, ABC_BLOCK, BLADE_WAVE, FIREBALL.
* `FpeFx.Kind`: SPIKE (black ground spike; `.param(heightMultiplier)`), TENTACLE (grabs + slows), RING_TRAP (compass-drawn circle that bursts), RING_SHOCK (expanding shockwave), ARC (visual crescent slash, `.param(sweepDeg).color(0xAARRGGBB)`; entity xRot = tilt).
  Spawn: `FpeUtil.fx(e, kind, pos, warmupTicks, lifeTicks, radius, damage)`.
* `FpeEntity` already: chases target, targets players + all non-FPE mobs, is never hurt by other FPE, never attacks other FPE, death takes 40 ticks (`c.death`), optional boss bar
  (`hasBossBar()`). Override `preferredDistance()` (0 for melee, larger for gunners), `restTicks()`, sounds (`getAmbientSound`, `getHurtSound`, `getDeathSound`, `playStepSound`: vanilla `SoundEvents` only), `getDimensions`.
* Server code must not import `net.minecraft.client.*`. Everything is server-authoritative; never trust `target` non-null outside callbacks.
* Block damage: avoid destroying blocks (explosions are already block-safe). Keep damage sane: base attack 4-9, multipliers 0.6-2.5, combos hit 2-3 times.
* Each character should have **many** distinct attacks (≥8 incl. an enraged-only or signature one), mixing melee, mid-range and ranged/zone control, so fights feel varied.
  Research canon moves first (FPE wiki / the FPE game / Fundamental Paper Education fan works, WebSearch/Firecrawl available), then add original, creative attacks that fit the character.
* Hostility rules already exist (FpeHostility): other mobs attack FPE characters and vice versa – nothing to do.

## Finishing
1. `compileJava` clean, preview PNG looked at and good. 2. Commit only your two (or few) files: `git add <files> && git commit -m "<Name>: ..."`.
3. Final report ≤ 150 words: list of abilities (id – what it does), model notes, any framework change you need.
