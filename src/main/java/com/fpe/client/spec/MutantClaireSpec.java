package com.fpe.client.spec;

import com.fpe.client.model.BbModel;
import com.fpe.client.model.ModelSpec;

public final class MutantClaireSpec {
    private MutantClaireSpec() {}
    public static final ModelSpec SPEC = BbModel.load("mutant_claire", 0.6f);
}
