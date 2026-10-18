package com.fpe.client.spec;

import com.fpe.client.model.BbModel;
import com.fpe.client.model.ModelSpec;

public final class MutantLanaSpec {
    private MutantLanaSpec() {}
    public static final ModelSpec SPEC = BbModel.load("mutant_lana", 0.7f);
}
