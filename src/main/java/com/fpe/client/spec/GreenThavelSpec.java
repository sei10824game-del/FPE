package com.fpe.client.spec;

import com.fpe.client.model.BbModel;
import com.fpe.client.model.ModelSpec;

public final class GreenThavelSpec {
    private GreenThavelSpec() {}
    public static final ModelSpec SPEC = BbModel.load("green_thavel", 0.7f);
}
