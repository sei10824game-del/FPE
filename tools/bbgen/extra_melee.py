"""Patches extra melee animations into existing .bbmodel files (idempotent: replaces animations by name).
Run:  python3 tools/bbgen/extra_melee.py      Ability ids/timings must match entity/characters/<Name>.java.
Keys are (tick, x, y, z); conventions as in the other generators: limb x+ = swing forward/up, shin x- = knee bend,
chest/body x- = lean forward, body position y- = down."""
import json, os, uuid

BB = os.path.join(os.path.dirname(__file__), "../../src/main/resources/assets/fpe/bbmodels")
RA, LA = (3, 0, 6), (6, 0, -8)   # arm rest poses


def kick(D, H):
    return {"chest": [(0, 0, 0, 0), (H - 6, 8, 0, 0), (H, -6, 0, 0), (H + 7, 4, 0, 0), (D, 0, 0, 0)],
            "leg_r": [(0, 0, 0, 0), (H - 6, -16, 0, 0), (H, 95, 0, 0), (H + 3, 80, 0, 0), (H + 8, 10, 0, 0), (D, 0, 0, 0)],
            "shin_r": [(0, 0, 0, 0), (H - 6, -50, 0, 0), (H, -4, 0, 0), (H + 8, -24, 0, 0), (D, 0, 0, 0)],
            "leg_l": [(0, 0, 0, 0), (H, -10, 0, 0), (D, 0, 0, 0)],
            "arm_r": [(0, *RA), (H - 6, 20, 0, 10), (H, -34, 0, 16), (D, *RA)],
            "arm_l": [(0, *LA), (H - 6, -10, 0, -14), (H, 38, 0, -16), (D, *LA)],
            "head": [(0, 0, 0, 0), (H, -6, 0, 0), (D, 0, 0, 0)]}


def knee(D, H):
    return {"chest": [(0, 0, 0, 0), (H - 6, 6, 0, 0), (H, -16, 0, 0), (H + 6, -6, 0, 0), (D, 0, 0, 0)],
            "leg_r": [(0, 0, 0, 0), (H - 6, -14, 0, 0), (H, 104, 0, 0), (H + 6, 30, 0, 0), (D, 0, 0, 0)],
            "shin_r": [(0, 0, 0, 0), (H - 6, -30, 0, 0), (H, -100, 0, 0), (H + 6, -40, 0, 0), (D, 0, 0, 0)],
            "arm_r": [(0, *RA), (H - 6, 96, 0, 12), (H, 24, 0, 10), (D, *RA)],
            "arm_l": [(0, *LA), (H - 6, 96, 0, -12), (H, 24, 0, -10), (D, *LA)],
            "fore_r": [(0, 10, 0, 0), (H - 6, 40, 0, 0), (H, 70, 0, 0), (D, 10, 0, 0)],
            "fore_l": [(0, 10, 0, 0), (H - 6, 40, 0, 0), (H, 70, 0, 0), (D, 10, 0, 0)],
            "head": [(0, 0, 0, 0), (H, -10, 0, 0), (D, 0, 0, 0)]}


def bash(D, H):
    return {"body": [(0, 0, 0, 0), (H - 6, 4, 34, 0), (H, -14, -22, 0), (H + 6, -12, -22, 0), (D, 0, 0, 0)],
            "chest": [(0, 0, 0, 0), (H - 6, 4, 10, 0), (H, -18, -8, 0), (H + 6, -14, -8, 0), (D, 0, 0, 0)],
            "head": [(0, 0, 0, 0), (H - 6, 0, -30, 0), (H, 8, 22, 0), (D, 0, 0, 0)],
            "arm_r": [(0, *RA), (H - 6, -20, 0, 20), (H, 62, -30, 24), (H + 6, 62, -30, 24), (D, *RA)],
            "fore_r": [(0, 10, 0, 0), (H, 96, 0, 0), (H + 6, 96, 0, 0), (D, 10, 0, 0)],
            "arm_l": [(0, *LA), (H, -30, 0, -20), (H + 6, -30, 0, -20), (D, *LA)],
            "leg_r": [(0, 0, 0, 0), (H - 3, 32, 0, 0), (H, -26, 0, 0), (H + 3, 32, 0, 0), (H + 6, -12, 0, 0), (D, 0, 0, 0)],
            "leg_l": [(0, 0, 0, 0), (H - 3, -26, 0, 0), (H, 32, 0, 0), (H + 3, -26, 0, 0), (H + 6, 14, 0, 0), (D, 0, 0, 0)],
            "shin_r": [(0, 0, 0, 0), (H, -40, 0, 0), (H + 3, -10, 0, 0), (D, 0, 0, 0)],
            "shin_l": [(0, 0, 0, 0), (H - 3, -40, 0, 0), (H, -10, 0, 0), (H + 3, -40, 0, 0), (D, 0, 0, 0)]}


def sweep(D, H):
    return {"body": {"rotation": [(0, 0, 0, 0), (H - 8, -10, 0, 0), (H - 4, -12, 120, 0), (H, -12, 240, 0), (H + 4, -10, 360, 0), (D, 0, 360, 0)],
                     "position": [(0, 0, 0, 0), (H - 8, 0, -4.5, 0), (H + 4, 0, -4.5, 0), (D, 0, 0, 0)]},
            "leg_r": [(0, 0, 0, 0), (H - 8, 46, 0, 0), (H + 4, 46, 0, 0), (D, 0, 0, 0)],
            "shin_r": [(0, 0, 0, 0), (H - 8, -96, 0, 0), (H + 4, -96, 0, 0), (D, 0, 0, 0)],
            "leg_l": [(0, 0, 0, 0), (H - 8, 30, 0, -70), (H + 4, 30, 0, -70), (D, 0, 0, 0)],
            "arm_r": [(0, *RA), (H - 8, 20, 0, 64), (H + 4, 20, 0, 64), (D, *RA)],
            "arm_l": [(0, *LA), (H - 8, 20, 0, -64), (H + 4, 20, 0, -64), (D, *LA)],
            "head": [(0, 0, 0, 0), (H - 8, 10, 0, 0), (H + 4, 10, 0, 0), (D, 0, 0, 0)]}


def headbutt(D, H):
    return {"chest": [(0, 0, 0, 0), (H - 6, 14, 0, 0), (H, -30, 0, 0), (H + 6, -8, 0, 0), (D, 0, 0, 0)],
            "head": [(0, 0, 0, 0), (H - 6, 26, 0, 0), (H, -38, 0, 0), (H + 6, 0, 0, 0), (D, 0, 0, 0)],
            "body": [(0, 0, 0, 0), (H - 6, 4, 0, 0), (H, -12, 0, 0), (D, 0, 0, 0)],
            "arm_r": [(0, *RA), (H - 6, 20, 0, 14), (H, -40, 0, 14), (D, *RA)],
            "arm_l": [(0, *LA), (H - 6, 20, 0, -14), (H, -40, 0, -14), (D, *LA)],
            "leg_r": [(0, 0, 0, 0), (H, 24, 0, 0), (D, 0, 0, 0)],
            "leg_l": [(0, 0, 0, 0), (H, -16, 0, 0), (D, 0, 0, 0)]}


def uppercut(D, H):
    return {"body": {"rotation": [(0, 0, 0, 0), (H - 6, -12, -20, 0), (H, 8, 20, 0), (D, 0, 0, 0)],
                     "position": [(0, 0, 0, 0), (H - 6, 0, -3, 0), (H, 0, 1.2, 0), (D, 0, 0, 0)]},
            "chest": [(0, 0, 0, 0), (H - 6, -8, -14, 0), (H, 12, 16, 0), (D, 0, 0, 0)],
            "arm_l": [(0, *LA), (H - 6, -34, 0, -12), (H, 168, 0, -10), (H + 8, 110, 0, -10), (D, *LA)],
            "fore_l": [(0, 10, 0, 0), (H - 6, 84, 0, 0), (H, 8, 0, 0), (D, 10, 0, 0)],
            "arm_r": [(0, *RA), (H - 6, 30, 0, 22), (H, -24, 0, 14), (D, *RA)],
            "leg_r": [(0, 0, 0, 0), (H - 6, 30, 0, 0), (H, -10, 0, 0), (D, 0, 0, 0)],
            "shin_r": [(0, 0, 0, 0), (H - 6, -50, 0, 0), (H, 0, 0, 0), (D, 0, 0, 0)],
            "leg_l": [(0, 0, 0, 0), (H - 6, 20, 0, 0), (H, 6, 0, 0), (D, 0, 0, 0)],
            "shin_l": [(0, 0, 0, 0), (H - 6, -40, 0, 0), (H, 0, 0, 0), (D, 0, 0, 0)],
            "head": [(0, 0, 0, 0), (H - 6, -8, 0, 0), (H, 14, 0, 0), (D, 0, 0, 0)]}


def jab(D, H):
    return {"chest": [(0, 0, 0, 0), (H - 5, 4, -26, 0), (H, -12, 26, 0), (H + 6, -4, 10, 0), (D, 0, 0, 0)],
            "arm_r": [(0, *RA), (H - 5, 36, 0, 22), (H, 98, 0, 4), (H + 6, 50, 0, 8), (D, *RA)],
            "fore_r": [(0, 10, 0, 0), (H - 5, 104, 0, 0), (H, 4, 0, 0), (D, 10, 0, 0)],
            "arm_l": [(0, *LA), (H, -20, 0, -14), (D, *LA)],
            "leg_r": [(0, 0, 0, 0), (H, -14, 0, 0), (D, 0, 0, 0)],
            "leg_l": [(0, 0, 0, 0), (H, 20, 0, 0), (D, 0, 0, 0)],
            "head": [(0, 0, 0, 0), (H - 5, 0, 20, 0), (H, -6, -16, 0), (D, 0, 0, 0)]}


def haymaker(D, H):
    return {"chest": [(0, 0, 0, 0), (H - 6, 2, -42, 0), (H, -12, 52, 0), (H + 6, -6, 30, 0), (D, 0, 0, 0)],
            "body": [(0, 0, 0, 0), (H - 6, 0, -14, 0), (H, -6, 18, 0), (D, 0, 0, 0)],
            "arm_r": [(0, *RA), (H - 6, 30, 0, 74), (H, 84, -44, 12), (H + 6, 60, -30, 8), (D, *RA)],
            "fore_r": [(0, 10, 0, 0), (H - 6, 70, 0, 0), (H, 22, 0, 0), (D, 10, 0, 0)],
            "arm_l": [(0, *LA), (H - 6, 30, 0, -20), (H, -30, 0, -24), (D, *LA)],
            "leg_r": [(0, 0, 0, 0), (H - 6, -16, 0, 0), (H, 22, 0, 0), (D, 0, 0, 0)],
            "leg_l": [(0, 0, 0, 0), (H - 6, 12, 0, 0), (H, -14, 0, 0), (D, 0, 0, 0)],
            "head": [(0, 0, 0, 0), (H - 6, 0, 30, 0), (H, -6, -24, 0), (D, 0, 0, 0)]}


def elbow(D, H):
    return {"body": {"rotation": [(0, 0, 0, 0), (H - 6, 6, 0, 0), (H, -14, 0, 0), (D, 0, 0, 0)],
                     "position": [(0, 0, 0, 0), (H - 6, 0, 1, 0), (H, 0, -3.5, 0), (H + 6, 0, -2.5, 0), (D, 0, 0, 0)]},
            "chest": [(0, 0, 0, 0), (H - 6, 16, 0, 0), (H, -34, 0, 0), (H + 6, -20, 0, 0), (D, 0, 0, 0)],
            "arm_r": [(0, *RA), (H - 6, 172, 0, 10), (H, 44, 0, 10), (H + 6, 44, 0, 10), (D, *RA)],
            "fore_r": [(0, 10, 0, 0), (H - 6, 124, 0, 0), (H, 112, 0, 0), (D, 10, 0, 0)],
            "arm_l": [(0, *LA), (H - 6, 30, 0, -24), (H, -24, 0, -20), (D, *LA)],
            "leg_r": [(0, 0, 0, 0), (H, 40, 0, 0), (D, 0, 0, 0)],
            "shin_r": [(0, 0, 0, 0), (H, -70, 0, 0), (D, 0, 0, 0)],
            "leg_l": [(0, 0, 0, 0), (H, 30, 0, 0), (D, 0, 0, 0)],
            "shin_l": [(0, 0, 0, 0), (H, -60, 0, 0), (D, 0, 0, 0)],
            "head": [(0, 0, 0, 0), (H - 6, 14, 0, 0), (H, -16, 0, 0), (D, 0, 0, 0)]}


# ---- quadruped kit (infected_zip: pelvis/body/neck/head/jaw, fore limbs arm_*)
def forepaw_slam(D, H):
    return {"body": [(0, 0, 0, 0), (H - 6, 26, 0, 0), (H, -14, 0, 0), (H + 8, -8, 0, 0), (D, 0, 0, 0)],
            "arm_r": [(0, 0, 0, 0), (H - 6, -120, 0, 20), (H, 60, 0, 0), (H + 8, 30, 0, 0), (D, 0, 0, 0)],
            "arm_l": [(0, 0, 0, 0), (H - 6, -120, 0, -20), (H, 60, 0, 0), (H + 8, 30, 0, 0), (D, 0, 0, 0)],
            "fore_r": [(0, 0, 0, 0), (H - 6, -40, 0, 0), (H, -10, 0, 0), (D, 0, 0, 0)],
            "fore_l": [(0, 0, 0, 0), (H - 6, -40, 0, 0), (H, -10, 0, 0), (D, 0, 0, 0)],
            "neck": [(0, 0, 0, 0), (H - 6, -16, 0, 0), (H, 20, 0, 0), (D, 0, 0, 0)],
            "jaw": [(0, 0, 0, 0), (H - 6, -30, 0, 0), (H, -10, 0, 0), (D, 0, 0, 0)],
            "tail0": [(0, 0, 0, 0), (H - 6, -14, 0, 0), (H, 12, 0, 0), (D, 0, 0, 0)]}


def gore_ram(D, H):
    return {"root": {"position": [(0, 0, 0, 0), (H - 6, 0, 0, 1.5), (H, 0, 0, -4), (H + 8, 0, 0, -2), (D, 0, 0, 0)]},
            "body": [(0, 0, 0, 0), (H - 6, 8, 0, 0), (H, -12, 0, 0), (H + 8, -8, 0, 0), (D, 0, 0, 0)],
            "neck": [(0, 0, 0, 0), (H - 6, 22, 0, 0), (H, 34, 0, 0), (H + 8, 12, 0, 0), (D, 0, 0, 0)],
            "head": [(0, 0, 0, 0), (H - 6, 18, 0, 0), (H, -22, 0, 0), (H + 8, 0, 0, 0), (D, 0, 0, 0)],
            "arm_r": [(0, 0, 0, 0), (H - 6, -24, 0, 0), (H, 44, 0, 0), (D, 0, 0, 0)],
            "arm_l": [(0, 0, 0, 0), (H - 6, -24, 0, 0), (H, 44, 0, 0), (D, 0, 0, 0)],
            "leg_r": [(0, 0, 0, 0), (H - 6, 14, 0, 0), (H, -18, 0, 0), (D, 0, 0, 0)],
            "leg_l": [(0, 0, 0, 0), (H - 6, 14, 0, 0), (H, -18, 0, 0), (D, 0, 0, 0)],
            "tail0": [(0, 0, 0, 0), (H, 16, 0, 0), (D, 0, 0, 0)]}


# model -> [(ability id, duration ticks, hit tick, builder)]
PLAN = {
    "red_circle": [("boot_kick", 30, 13, kick), ("shoulder_bash", 34, 14, bash), ("flame_uppercut", 36, 14, uppercut)],
    "danger_bloomie": [("knee_strike", 28, 12, knee), ("shoulder_check", 32, 13, bash), ("sweep_kick", 32, 16, sweep)],
    "danger_thavel": [("headbutt", 26, 11, headbutt), ("sweep_kick", 32, 16, sweep), ("knee_strike", 28, 12, knee)],
    "infected_bloomie": [("gore_shove", 30, 13, headbutt), ("shoulder_ram", 34, 14, bash)],
    "danger_alice": [("pommel_strike", 28, 11, jab), ("spin_kick", 32, 16, sweep)],
    "aiden": [("headbutt", 26, 11, headbutt), ("knee_strike", 28, 12, knee), ("haymaker", 30, 13, haymaker)],
    "mutant_engel": [("boot_kick", 30, 13, kick), ("haymaker", 30, 13, haymaker), ("elbow_drop", 34, 15, elbow)],
    "mutant_bubble": [("shoulder_bash", 34, 14, bash), ("headbutt", 26, 11, headbutt)],
    "mutant_claire": [("knee_strike", 28, 12, knee), ("sweep_kick", 32, 16, sweep), ("haymaker", 30, 13, haymaker)],
    "riley": [("boot_kick", 30, 13, kick), ("elbow_drop", 34, 15, elbow), ("shoulder_bash", 34, 14, bash)],
    "hansel_juvenile": [("headbutt", 26, 11, headbutt), ("haymaker", 30, 13, haymaker)],
    "mutant_abbie": [("knee_strike", 28, 12, knee), ("elbow_drop", 34, 15, elbow)],
    "infected_zip": [("forepaw_slam", 36, 16, forepaw_slam), ("gore_ram", 32, 14, gore_ram)],
    "mutant_lana": [("boot_kick", 30, 13, kick), ("sweep_kick", 32, 16, sweep)],
}


def bones(doc):
    out = {}
    def walk(ns):
        for n in ns:
            if isinstance(n, dict):
                out[n["name"]] = n["uuid"]
                walk(n.get("children", []))
    walk(doc["outliner"])
    return out


def main():
    for model, anims in PLAN.items():
        path = os.path.join(BB, model + ".bbmodel")
        doc = json.load(open(path))
        b = bones(doc)
        for name, D, H, fn in anims:
            animators = {}
            for bone, tr in fn(D, H).items():
                if bone not in b:
                    continue
                chans = tr if isinstance(tr, dict) else {"rotation": tr}
                kfs = [{"channel": ch, "data_points": [{"x": x, "y": y, "z": z}], "uuid": str(uuid.uuid4()), "time": t / 20.0, "color": -1, "interpolation": "catmullrom"}
                       for ch, keys in chans.items() for (t, x, y, z) in keys]
                animators[b[bone]] = {"name": bone, "type": "bone", "keyframes": kfs}
            # effect bones (flames, muzzle flashes, spare props) are hidden by a constant scale key in "idle": keep them hidden here too
            idle = next((a for a in doc["animations"] if a["name"] == "idle"), None)
            for uid, an in (idle["animators"].items() if idle else []):
                sk = [k for k in an["keyframes"] if k["channel"] == "scale"]
                if sk and uid not in animators:
                    dp = sk[0]["data_points"][0]
                    animators[uid] = {"name": an["name"], "type": "bone", "keyframes": [
                        {"channel": "scale", "data_points": [dict(dp)], "uuid": str(uuid.uuid4()), "time": 0, "color": -1, "interpolation": "linear"}]}
            doc["animations"] = [a for a in doc["animations"] if a["name"] != name]
            doc["animations"].append({"uuid": str(uuid.uuid4()), "name": name, "loop": "once", "override": False, "length": D / 20.0, "snapping": 24,
                                      "selected": False, "anim_time_update": "", "blend_weight": "", "start_delay": "", "loop_delay": "", "animators": animators})
        json.dump(doc, open(path, "w"))
        print(model, [a[0] for a in anims])


if __name__ == "__main__":
    main()
