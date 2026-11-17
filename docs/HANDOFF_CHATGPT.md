# FPE – handoff for ChatGPT (or any other agent)

Repo: https://github.com/sei10824game-del/FPE   branch `main` (push directly to `main`; no PRs used so far).
Read this file first, then `docs/CHARACTER_GUIDE.md` (framework API) and `docs/HANDOFF.md` (user rules + confirmed reference art list).

## 1. What this is
A Minecraft **1.20.1 / Forge 47.3.0** mod (mod id `fpe`, official Mojang mappings, Java 17 toolchain, JDK 21 runs it, no external libs / no GeckoLib)
that adds horror characters from the indie game "Fundamental Paper Education" (FPE) and its AUs. Language of the user: Japanese; keep replies short and
concrete. The user plays on a local Forge client; the agent usually works in a headless Linux container (no GL, no Blockbench app, no Minecraft client).

## 2. Build / verify (all headless)
```
./gradlew --no-daemon compileJava -q                 # fast check (first run downloads Forge, several minutes)
./gradlew --no-daemon build -q                       # -> build/libs/fpe-1.0.0.jar
./gradlew --no-daemon preview -Pspec=<model_id> [-Pvariant=1]   # software renders the REAL model+animations -> build/preview/<id>.png
        # rows: idle views, walk, then one row per ability (6 frames), last row = death. Always LOOK at the png after animation changes.
        # -Pspec=all renders everything. Prints "HEIGHT <id> minY maxY w" (px, 16px = 1 block, ground = 24 for procedural / 0 for bbmodel space).
JAVA_TOOL_OPTIONS="$JAVA_TOOL_OPTIONS -Dfpe.selftest=true" ./gradlew --no-daemon runServer -q --console=plain
        # SelfTest: spawns every character next to a zombie, ticks 1200, prints "SELFTEST alive=N"; grep log for exceptions ("at com.fpe").
```
`settings.gradle` has a googleapis Maven-central mirror because the container proxy rate-limits repo.maven.apache.org (429). Keep it.
Merge conflicts happen in the same 6 registration files every time two sessions add characters:
`registry/ModEntities.java`, `registry/ModItems.java`, `client/ClientSetup.java`, `client/spec/Specs.java`, `tools/Preview.java`, `lang/en_us.json`+`ja_jp.json`.
Resolve by keeping BOTH sides. Past crash: duplicate `e.put(X.get(), ...)` in `ModEntities.Events.attributes` -> "Duplicate DefaultAttributes entry" at startup. Check for duplicates after every merge.

## 3. Architecture
- `entity/FpeEntity` – base class: chase AI, target selection, ability scheduler, boss bar, death animation (40 ticks), factions, grab/hold/stun helpers.
  Subclasses only give `attributes()`, `faction()`, `registerAbilities(List<Ability>)`, optional sounds / `preferredDistance()`.
- `entity/Ability` – `Ability.of(id, durationTicks, cooldownTicks).range(min,max).weight(w).faceUntil(tick).moving().blind().when(pred).tick((e,target,tick)->{...})`.
  The **id is the animation name**; hit logic fires on a specific tick; animation `t` and server `tick` are the same timeline (20 ticks = 1 s).
- `entity/FpeUtil` – hitCone / hitRadius / hitLine / projectile / fx / knock / sound helpers. `entity/FpeCombat` – cone(), slashArc, bleed, shadowStep, rotY.
- `entity/FpeProjectile` (kinds: COMPASS, PENCIL, GRENADE, BOMBLET, ROCKET, BULLET, SHADOW_ORB, DIAMOND, AXE, KNIFE, ABC_BLOCK, BLADE_WAVE, FIREBALL;
  BULLET/PENCIL/KNIFE/DIAMOND reset the victim's invulnerableTime so rapid fire is not eaten by i-frames) and `entity/FpeFx` (SPIKE, TENTACLE, RING_TRAP, RING_SHOCK, ARC).
- Factions (`FpeEntity.Faction`, feud table `FEUDS`): characters never hurt members of non-hostile factions (melee, projectiles, fx, explosions); hostile pairs fight each other.
  All non-FPE mobs hate FPE characters and vice versa (`entity/FpeHostility`).
- Client: `client/spec/<Name>Spec` exposes `SPEC` (a `ModelSpec`). Most characters use `BbModel.load("<id>", shadow)` which reads
  `src/main/resources/assets/fpe/bbmodels/<id>.bbmodel` (Blockbench "free" format, per-face UV atlas + glow atlas; custom renderer so Embeddium/Sodium cannot replace UVs).
  Animations inside the bbmodel are matched by NAME: `idle` (loops), `walk` (loops by limb swing), `death` (scrubbed by death 0..1), `quad_idle`/`quad_walk` (stance 1),
  and **any ability id** (plays on `c.t/20` seconds). Missing animation = the attack plays with no pose change (looks broken) -> always add both sides.
  Older/procedural models (`InsanityCircleSpec`, fx/projectile specs) are Java `ModelSpec.part(...)` + `animator` lambdas.
- Voices: `tools/gen_voice.py` + `assets/fpe/sounds*` (Miss Circle has custom voice lines).

## 4. Characters (generated from the code)
| id | class | faction | hitbox | abilities | model |
|---|---|---|---|---|---|
| miss_circle | MissCircle | MISS | 0.75x2.57 | 17 | bbmodel |
| miss_thavel | MissThavel | MISS | 0.6x2.19 | 16 | bbmodel |
| miss_bloomie | MissBloomie | MISS | 0.6x2.18 | 17 | bbmodel |
| alice | Alice | ALICE | 0.7x2.51 | 8 | bbmodel |
| red_circle | RedCircle | DANGER | 0.75x2.57 | 15 | bbmodel |
| danger_thavel | DangerThavel | DANGER | 0.7x2.44 | 16 | bbmodel |
| danger_bloomie | DangerBloomie | DANGER | 0.65x2.29 | 16 | bbmodel |
| infected_bloomie | InfectedBloomie | INFECTED | 1.3x4.12 | 17 | bbmodel |
| infected_zip | InfectedZip | INFECTED | 1.5x2.94 | 18 | bbmodel |
| danger_alice | DangerAlice | DANGER_ALICE | 0.7x2.51 | 10 | bbmodel |
| crazy_one | CrazyOne | WILD | 0.6x1.9 | 12 | bbmodel |
| wild_wolf | WildWolf | WILD | 1.1x3.0 | 12 | bbmodel |
| insanity_circle | InsanityCircle | MISS | 0.75x2.57 | 18 | procedural |
| fen | Fen | STUDENT | 1.0x3.2 | 26 | bbmodel |
| aiden | Aiden | STUDENT | 0.6x1.64 | 16 | bbmodel |
| mutant_claire | MutantClaire | MUTANT | 0.6x1.53 | 17 | bbmodel |
| mutant_engel | MutantEngel | MUTANT | 0.6x1.93 | 15 | bbmodel |
| mutant_bubble | MutantBubble | MUTANT | 0.6x1.22 | 17 | bbmodel |
| mutant_lana | MutantLana | MUTANT | 0.6x1.72 | 18 | bbmodel |
| mutant_abbie | MutantAbbie | MUTANT | 0.6x1.5 | 16 | bbmodel |
| green_thavel | GreenThavel | GREEN_TEACHER | 0.65x2.29 | 12 | bbmodel |
| green_bloomie | GreenBloomie | GREEN_TEACHER | 0.65x2.29 | 16 | bbmodel |
| green_alice | GreenAlice | GREEN_TEACHER | 0.7x2.51 | 4 | bbmodel |
| green_circle | GreenCircle | GREEN_TEACHER | 0.75x2.62 | 16 | bbmodel |
| hansel_juvenile | HanselJuvenile | OUTSIDER | 0.6x2.15 | 19 | bbmodel |
| lord_hansel | LordHansel | OUTSIDER | 0.8x2.9 | 8 | bbmodel |
| riley | Riley | STUDENT | 0.6x1.94 | 19 | bbmodel |
| daniel_barrel | DanielBarrel | OUTSIDER | 0.75x2.58 | 4 | bbmodel |

Reference art the user confirmed: `docs/ref/confirmed/*` (older `docs/ref/*.png` are partly WRONG). Heights: `docs/HEIGHTS.md`.

## 5. Model/animation pipeline (how the bbmodels are made)
`tools/bbgen/bbgen.py` is a tiny generator: `Model.group/cube/anim(...)` + painters -> writes `.bbmodel`. One script per character in `tools/bbgen/chars/<id>.py`
(`python3 tools/bbgen/chars/<id>.py`). Conventions at the top of each script (Blockbench space: Y up, ground 0, faces -Z; rotation signs in the doc-string of `miss_circle.py`).
`tools/bbgen/extra_melee.py` PATCHES extra melee animations (boot_kick, knee_strike, shoulder_bash, sweep_kick, headbutt, haymaker, elbow_drop, uppercut, jab, quadruped
forepaw_slam/gore_ram) into existing .bbmodel files and adds lagged secondary motion to hair/coat/tail bones. It is idempotent. **If you regenerate a character with
its chars/<id>.py, re-run the patcher only for characters listed in its PLAN** or those extra animations vanish. Crazie and Nameless Werewolf author all 12 attacks in their own generators and need no shared patcher. See [their guide](CRAZIE_WEREWOLF.md).
Blockbench can open and edit the generated `.bbmodel` files by hand; keep bone names and animation names.

## 6. Conventions / lessons
- Hitboxes live in `ModEntities.chara(id, factory, w, h)`; model scale is separate (model px vs hitbox blocks). Compare heights with the preview `HEIGHT` line.
- Ranged attacks: `FpeUtil.projectile`; melee: tick-synced `hitCone/hitRadius`; damage = `e.dmg(mult)` (attack attribute x mult). Keep sane: mult 0.6-2.5.
- Never destroy blocks. Explosions are block-safe.
- New character checklist: `entity/characters/X.java` (+ faction), `client/spec/XSpec.java`, bbmodel (+ `tools/bbgen/chars/x.py`), `ModEntities` (type, attributes, `characters()`),
  `ModItems` (spawn egg), `ClientSetup` (renderer), `Specs.all()`, lang en/ja, `assets/fpe/models/item/<id>_spawn_egg.json`, `data/fpe/forge/biome_modifier/<id>.json`, `tools/Preview.java` map.
- Commit message footer used by the user's tooling: `Co-Authored-By: ...` lines; push with `git push origin main`.
- Copyright: the project is a fan mod. Do not copy third-party assets verbatim; models/textures here are procedurally generated.

## 7. Known gaps / ideas (not done)
- No in-client verification by the agents: all balance numbers (damage, ranges, cooldowns), and the look of attacks in the real client, are untested. Ask the user for play feedback.
- Insanity Miss Circle (`InsanityCircleSpec`) is still the old procedural box model; could be rebuilt as a bbmodel like the others.
- Boss characters with form changes (Alice, Green Alice, Daniel Barrel, Lord Hansel) have no extra melee attacks yet.
- Some silhouettes could be closer to the confirmed art (largest gaps: Danger Alice phase 2 stance, Red Circle hair mass, Miss Bloomie hair shape, Danger Bloomie hat size).

## 8. Prompt to paste into ChatGPT
> You are taking over a Minecraft 1.20.1 Forge mod repo (https://github.com/sei10824game-del/FPE, branch main). Read docs/HANDOFF_CHATGPT.md, docs/HANDOFF.md and
> docs/CHARACTER_GUIDE.md first. Work in small commits, build with ./gradlew build, check animations with ./gradlew preview -Pspec=<id>, and never leave an ability without
> a same-named animation in the character's .bbmodel. Answer the user (Japanese speaker) briefly. Ask before big redesigns.
