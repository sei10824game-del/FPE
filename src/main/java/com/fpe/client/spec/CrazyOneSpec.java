package com.fpe.client.spec;

import com.fpe.client.model.BbModel;
import com.fpe.client.model.ModelSpec;

/** Crazie: original model based on the supplied Current Wiki reference. */
public final class CrazyOneSpec {
    private CrazyOneSpec() {}
    public static final ModelSpec SPEC = BbModel.load("crazy_one", 0.6f);
}
