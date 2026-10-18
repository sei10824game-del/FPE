package com.fpe.client.spec;

import com.fpe.client.model.BbModel;
import com.fpe.client.model.ModelSpec;

public final class MutantBubbleSpec {
    private MutantBubbleSpec() {}
    public static final ModelSpec SPEC = BbModel.load("mutant_bubble", 0.7f);
}
