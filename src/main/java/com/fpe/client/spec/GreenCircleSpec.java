package com.fpe.client.spec;

import com.fpe.client.model.BbModel;
import com.fpe.client.model.ModelSpec;

public final class GreenCircleSpec {
    private GreenCircleSpec() {}
    public static final ModelSpec SPEC = BbModel.load("green_circle", 0.7f);
}
