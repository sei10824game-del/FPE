package com.fpe.client.spec;

import com.fpe.client.model.BbModel;
import com.fpe.client.model.ModelSpec;

public final class MutantAbbieSpec {
    private MutantAbbieSpec() {}
    public static final ModelSpec SPEC = BbModel.load("mutant_abbie", 0.5f);
}
