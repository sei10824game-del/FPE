# FPE handoff (for Blockbench-based continuation)

Minecraft 1.20.1 / Forge 47.3.0 mod, official mappings, Java 17 toolchain (JDK 21 runs it). No external libs.
Characters: Miss Circle/Thavel/Bloomie, Alice (2 phases), Red Circle / Thavel / Bloomie / Alice (DANGER AU), Infected Bloomie, Infected Zip, Fen, Aiden.

## Current state of visuals (the thing to improve)
Models are procedural Java: `client/spec/<Name>Spec.java` builds a `ModelSpec` (boxes + painted texture + animator lambda) -> no PNG/json assets.
Server logic (attacks, timings) is in `entity/characters/<Name>.java`; the animation `c.is("<abilityId>")` with `c.t` (ticks since start) is synced to ability ticks.
Docs: `docs/CHARACTER_GUIDE.md` (API), reference art `docs/ref/*.png`.

## Wanted
Re-author the character look + animations in Blockbench (Modded Entity / Java export or .bbmodel), keeping:
ability ids + tick timeline (hit ticks), hitboxes in `registry/ModEntities.java`, factions in `FpeEntity.FEUDS`, glow layer (eyes etc).
`./gradlew preview -Pspec=<name> [-Pvariant=1]` renders the CURRENT procedural model headlessly to build/preview/*.png for comparison.
Build: `./gradlew build` -> build/libs/fpe-1.0.0.jar (gradle plugin repo workaround in settings.gradle: googleapis maven mirror).

## CONFIRMED reference art (user-verified) -> docs/ref/confirmed/*.jpg  (older docs/ref/*.png are partly WRONG, do not trust them)
Red/orange-toned sheets = the DANGER AU versions; black-and-white sheets = the normal teachers.
- red_circle.jpg      = Red Circle (DANGER AU Circle): purple-black long hair, wolf-ear hat, orange poncho, bandaged arm, FLAMETHROWER   (the old "miss_circle" model actually depicts THIS one)
- danger_thavel.jpg   = Thavel (DANGER AU): long purple hair, orange jacket + skirt, grenade, ammo bandolier
- danger_bloomie.jpg  = Bloomie (DANGER AU): navy coat, black hat with warning triangle, striped ribbons, rifle
- miss_circle.jpg     = Miss Circle: huge black hair, giant COMPASS + pencil, white trousers, striped boots
- miss_bloomie.jpg    = Miss Bloomie: spiky hair, grey skirt, big blade/cleaver
- miss_thavel.jpg     = Miss Thavel: ABC-block hair ornament, white dress, black claws
- alice_phase1.jpg / alice_phase2.jpg               = Alice (normal) phase 1 / phase 2 (shadow monster)
- danger_alice_phase1.jpg / danger_alice_phase2.jpg = Alice (DANGER AU) phase 1 (patched, bandaged) / phase 2 (black, red eyes)
- infected_bloomie_window/3d/note.jpg = Infected Bloomie (tall spindly monster) -- three views of ONE character
- infected_zip.jpg    = Infected Zip (black ink-line sketch, spiky, winged)
- fen.jpg, aiden.jpg

## Rules from the user (apply to every character)
1. Research ALL canon + fan-work attacks of the character (FPE wiki / game / fan works) and implement them; inventing extra original attacks is welcome
   (e.g. Circle compass sweeps). Never drop a known attack.
2. Every attack needs its own fully authored animation (anticipation, strike, recovery, secondary motion) - no tacked-on poses. Look must match the confirmed art.
3. Alice phase 2: GIANT (scale up), whole body pitch black, monstrous, rougher/flashier attacks: tentacles, black attacks erupting from the ground, etc.
4. FPE characters are hostile to every non-FPE mob and vice versa (already in FpeHostility; keep it).
5. Previous author gave every character ~10-12 attacks; keep at least that many.

## Added later
- Melee rework: Miss Circle / Miss Thavel / Miss Bloomie (ranged attacks replaced by melee; Danger versions keep ranged).
- FPE Green: Mutant Claire/Engel/Bubble/Lana/Abbie, Green Thavel/Bloomie/Circle, Green Alice (2 forms). FPE Advanced Class: Juvenile Hansel, Lord Hansel (3 forms: Matured -> Premature -> True Form).
- Canon heights: Fen 305 cm, Miss Circle 292 cm (1 block = 1 m).
- Tools: tools/bbgen/chars/*.py (model+animation generators), tools/bbgen/connectivity.py (detached-cube check), tools/run_agent.sh (opus sub-agent per character),
  ./gradlew preview -Pspec=<name>, ./gradlew runClient -Pshots=a,b,c (dev screenshots, needs the local-only src/main/java/com/fpe/dev/DevShot.java).
- Known: Windows report of single-colour rendering with the GitHub jar could not be reproduced on macOS (dev + production Forge). Startup now logs "FPE texture <name> WxH glow=.. glError=..".
