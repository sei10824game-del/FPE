package com.fpe.client.spec;

import com.fpe.client.model.BbModel;
import com.fpe.client.model.ModelSpec;

public final class HanselJuvenileSpec {
    private HanselJuvenileSpec() {}
    public static final ModelSpec SPEC = BbModel.load("hansel_juvenile", 0.7f);
}
