package com.fpe.client.spec;

import com.fpe.client.model.BbModel;
import com.fpe.client.model.ModelSpec;

public final class MutantEngelSpec {
    private MutantEngelSpec() {}
    public static final ModelSpec SPEC = BbModel.load("mutant_engel", 0.7f);
}
