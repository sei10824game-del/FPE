package com.fpe.client.spec;

import com.fpe.client.model.BbModel;
import com.fpe.client.model.ModelSpec;

public final class PaperblightSpec {
    private PaperblightSpec() {}

    public static final ModelSpec FIRST = BbModel.load("paperblight", 0.48f);
    public static final ModelSpec SECOND = BbModel.load("paperblight_phase2", 0.70f);
    public static final ModelSpec THIRD = BbModel.load("paperblight_phase3", 0.92f);
}
