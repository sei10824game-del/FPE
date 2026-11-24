package com.fpe.client.spec;

import com.fpe.client.model.BbModel;
import com.fpe.client.model.ModelSpec;

public final class PaperblightHostsSpec {
    private PaperblightHostsSpec() {}
    public static final ModelSpec LANA = BbModel.load("host_lana", .45f);
    public static final ModelSpec EDWARD = BbModel.load("host_edward", .45f);
    public static final ModelSpec OLIVER = BbModel.load("host_oliver", .45f);
    public static final ModelSpec THAVEL = BbModel.load("host_thavel", .6f);
    public static final ModelSpec CLAIRE = BbModel.load("paperblight_claire", .4f);
    public static final ModelSpec ZIP = BbModel.load("host_zip", .5f);
}
