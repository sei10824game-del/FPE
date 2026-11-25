package com.fpe.client.spec;
import com.fpe.client.model.BbModel;
import com.fpe.client.model.ModelSpec;
import com.fpe.entity.characters.ZombieAuCharacter.Role;
public final class ZombieAuSpec {
    private ZombieAuSpec() {}
    public static final java.util.Map<Role,ModelSpec> MODELS = new java.util.LinkedHashMap<>();
    static { for(Role role:Role.values()) MODELS.put(role,BbModel.load(role.id,.5f)); }
}
