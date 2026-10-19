package com.fpe.client.spec;

import com.fpe.client.model.BbModel;
import com.fpe.client.model.ModelSpec;

public final class RileySpec {
    private RileySpec() {}
    public static final ModelSpec SPEC = BbModel.load("riley", 0.7f);
}
