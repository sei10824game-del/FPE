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
