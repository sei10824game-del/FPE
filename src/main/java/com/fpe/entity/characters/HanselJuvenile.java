package com.fpe.entity.characters;

import java.util.List;

import com.fpe.entity.Ability;
import com.fpe.entity.FpeEntity;
import com.fpe.entity.FpeUtil;

import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.level.Level;

/** PLACEHOLDER - to be rebuilt (model, animations, 10+ attacks). */
public class HanselJuvenile extends FpeEntity {
    public HanselJuvenile(EntityType<? extends FpeEntity> type, Level level) { super(type, level); }

    @Override public Faction faction() { return Faction.OUTSIDER; }

    public static AttributeSupplier.Builder attributes() { return baseAttributes(90, 7, 0.32, 3, 0.3); }

    @Override
    protected void registerAbilities(List<Ability> out) {
        out.add(Ability.of("slash", 24, 40).range(0, 3.5).weight(3)
                .tick((e, t, k) -> { if (k == 10) FpeUtil.hitCone(e, 3.2, 90, e.dmg(1.0f), 0.5, 0.2); }));
    }
}
