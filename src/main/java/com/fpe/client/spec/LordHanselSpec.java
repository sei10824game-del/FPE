package com.fpe.client.spec;

import com.fpe.client.model.BbModel;
import com.fpe.client.model.ModelSpec;

/** forms by variant: 0 Matured, 1 Premature, 2 True Form */
public final class LordHanselSpec {
    private LordHanselSpec() {}
    public static final ModelSpec MATURED = BbModel.load("lord_hansel", 0.7f);
    public static final ModelSpec PREMATURE = BbModel.load("lord_hansel_premature", 0.9f);
    public static final ModelSpec TRUE_FORM = BbModel.load("lord_hansel_true", 1.8f);
}
