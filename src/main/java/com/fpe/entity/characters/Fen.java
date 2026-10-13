package com.fpe.entity.characters;

import java.util.List;

import com.fpe.entity.Ability;
import com.fpe.entity.FpeEntity;
import com.fpe.entity.FpeUtil;

import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.level.Level;

/** STUB: replaced by the full implementation. */
public class Fen extends FpeEntity {
    public Fen(EntityType<? extends FpeEntity> type, Level level) { super(type, level); }

    public static AttributeSupplier.Builder attributes() { return baseAttributes(60, 6, 0.3, 4, 0.2); }

    @Override
    protected void registerAbilities(List<Ability> out) {
        out.add(Ability.of("melee", 14, 20).range(0, 3).tick((e, t, tk) -> { if (tk == 8) FpeUtil.hitCone(e, 3, 60, e.dmg(1f), 0.5, 0.2); }));
    }
}
