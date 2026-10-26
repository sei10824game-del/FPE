#!/bin/bash
cd "$(dirname "$0")/.." || exit 1
tools/run_agent.sh mutant_claire MutantClaire "CORRECTION: the earlier reference crop docs/ref/confirmed/mutant_claire.png was wrong (it showed Engel/Bubble) and has just been replaced with the correct Claire (001) crop - LOOK AT IT. Compare the whole current model (silhouette, head, hood/hair with wolf-like ears, huge jagged-tooth mouth and single black eye, oversized white jacket and shorts, hunched stance, black feet) with it and fix everything that clearly differs, mainly the head/face/hair and outfit proportions. Keep abilities, animations, cube names, hitbox and the size from docs/HEIGHTS.md (Claire 1.74 blocks): after regenerating with tools/bbgen/chars/mutant_claire.py re-apply tools/bbgen/rescale.py."
echo QUEUE_DONE
