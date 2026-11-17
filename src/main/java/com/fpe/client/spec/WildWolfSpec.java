package com.fpe.client.spec;

import com.fpe.client.model.BbModel;
import com.fpe.client.model.ModelSpec;

/** Nameless Werewolf: horned humanoid, bandages, black coat and a heavy pickaxe. */
public final class WildWolfSpec {
    private WildWolfSpec() {}
    public static final ModelSpec SPEC = BbModel.load("wild_wolf", 1.1f);
}
