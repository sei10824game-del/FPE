package com.fpe.client.spec;

import java.util.ArrayList;
import java.util.List;

import com.fpe.client.model.ModelSpec;

/** Every model that needs a layer definition + dynamic texture. */
public final class Specs {
    private Specs() {}

    public static List<ModelSpec> all() {
        List<ModelSpec> l = new ArrayList<>(List.of(
                MissCircleSpec.SPEC, MissThavelSpec.SPEC, MissBloomieSpec.SPEC, AliceSpec.PHASE1, AliceSpec.PHASE2,
                RedCircleSpec.SPEC, DangerThavelSpec.SPEC, DangerBloomieSpec.SPEC, FenSpec.SPEC, AidenSpec.SPEC,
                FxSpecs.SPIKE, FxSpecs.TENTACLE));
        ProjectileSpecs.all().forEach(l::add);
        return l;
    }
}
