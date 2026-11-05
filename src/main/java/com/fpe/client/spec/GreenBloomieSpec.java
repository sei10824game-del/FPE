package com.fpe.client.spec;

import com.fpe.client.model.BbModel;
import com.fpe.client.model.ModelSpec;

public final class GreenBloomieSpec {
    private GreenBloomieSpec() {}
    public static final ModelSpec SPEC = BbModel.load("green_bloomie", 0.7f);
}
