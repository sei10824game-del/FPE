package com.fpe.client.spec;

import com.fpe.client.model.BbModel;
import com.fpe.client.model.ModelSpec;

/** forms by variant: 0 Matured, 1 Cyborg Armed */
public final class DanielBarrelSpec {
    private DanielBarrelSpec() {}
    public static final ModelSpec PHASE1 = BbModel.load("daniel_barrel", 0.7f);
    public static final ModelSpec PHASE2 = BbModel.load("daniel_barrel_cyborg", 0.9f);
}
