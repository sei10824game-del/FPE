package com.fpe.client.spec;

import com.fpe.client.model.BbModel;
import com.fpe.client.model.ModelSpec;

public final class GreenAliceSpec {
    private GreenAliceSpec() {}
    public static final ModelSpec PHASE1 = BbModel.load("green_alice", 0.5f);
    public static final ModelSpec PHASE2 = BbModel.load("green_alice_boss", 1.6f);
}
