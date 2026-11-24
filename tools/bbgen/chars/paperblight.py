"""Paperblight's three articulated bodies, generated from the four supplied views.
Coordinates are Blockbench units (+Y up, facing -Z). One design grid is enlarged
for each form after painting, so the paper grain and pen marks retain their scale.
"""
import itertools
import math
from pathlib import Path
import sys
import uuid

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import bbgen
from bbgen import Model, mix

OUT = Path(__file__).resolve().parents[3] / "src/main/resources/assets/fpe/bbmodels"
WHITE, PAPER, BAND = 0xF2F0ED, 0xDCDBDE, 0x9695A3
HAIR, LOCK, INK = 0x51475E, 0x3D354C, 0x272331
VEST, BLACK, SHADOW = 0x423A50, 0x09090C, 0x17151B
WING, RIB, MEMBRANE = 0x39324C, 0x46405B, 0xD4D5E4
SIDES = (("r", 1), ("l", -1))


def lerp(a, b, t):
    return tuple(x + (y - x) * t for x, y in zip(a, b))


def rib(m, name, bone, a, b, width, depth, color, **kw):
    """Solid rectangular segment oriented from one joint to the next."""
    dx, dy, dz = (v - u for u, v in zip(a, b))
    length = math.dist(a, b)
    x, y, z = a
    pitch = math.degrees(math.asin(dz / length))
    roll = -math.degrees(math.atan2(dx, dy))
    return m.cube(name, bone, (x-width/2, y-.08, z-depth/2),
                  (x+width/2, y+length+.08, z+depth/2), color, origin=a,
                  rot=(pitch, 0, roll), grain=.018, **kw)


def eye(f):
    # A single almond-shaped brown eye, recessed in the otherwise solid rectangle.
    for y in range(f.h):
        for x in range(f.w):
            u, v = (x+.5)/f.w-.5, (y+.5)/f.h-.5
            if abs(u) < .205 and abs(v) < .158*(1-(abs(u)/.205)**1.55):
                f.px(x, y, 0xD9C9B7)
                if (u/.065)**2+(v/.15)**2 < 1:
                    f.px(x, y, 0x8F6952)
                if (u/.029)**2+(v/.12)**2 < 1:
                    f.px(x, y, 0x30252B)


def vest(f):
    def ribbon(points, color):
        f.poly([(x*f.w, y*f.h) for x, y in points], color)
    ribbon([(0,0),(1,0),(.53,.45)], PAPER)
    ribbon([(.35,0),(.63,0),(.53,.11)], BAND)
    ribbon([(.52,.09),(.57,.19),(.51,.34),(.46,.21)], INK)
    f.line(.06*f.w, .05*f.h, .52*f.w, .46*f.h, 0xA6A0AB, 1)
    f.line(.52*f.w, .46*f.h, .94*f.w, .05*f.h, 0xA6A0AB, 1)


def build_body(m, phase):
    dark = phase == 2
    trim = BLACK if dark else INK
    white = BLACK if dark else WHITE
    purple = SHADOW if dark else HAIR
    lock = BLACK if dark else LOCK
    g = m.group
    g("root")
    g("pelvis", (0,16,0), parent="root")
    g("chest", (0,17.1,0), parent="pelvis")
    g("head", (0,25.4,0), parent="chest")
    g("sprout", (0,31.0,.1), parent="head")

    torso = 1.05 if dark else 1.60
    m.cube("blouse", "chest", (-torso,17,-1.05), (torso,25.4,1.1), white, grain=.022)
    m.cube("waistcoat", "chest", (-torso-.1,17.2,-1.14),(torso+.1,24.6,1.18),
           BLACK if dark else VEST, faces={} if dark else {"north":vest})
    m.cube("hip", "pelvis", (-1.55,15.6,-.94),(1.55,17.8,.95), white)
    m.cube("neck", "chest", (-.85,24.6,-.6),(.85,26.4,.68), white)
    m.cube("face", "head", (-1.92,25.85,-1.32),(1.92,30.25,1.42), SHADOW if dark else PAPER)
    m.cube("face_bar", "head", (-2.2,26.35,-1.67),(2.2,29.2,-1.26),
           BLACK, grain=0, faces={"north": eye} if phase == 1 else {}, res=11)
    if dark:
        rib(m,"paper_sliver_l","head",(-.98,26.60,-1.72),(-.56,27.30,-1.72),.16,.09,0xD0CCCA)
        rib(m,"paper_sliver_r","head",(-.56,27.30,-1.72),(-.32,26.88,-1.72),.11,.09,0xA6A1A1)

    m.cube("crown", "head", (-2.38,29.30,-1.52),(2.38,31.1,1.74),purple, color2=lock,grad=True)
    m.cube("crown_ridge","head",(-1.50,30.55,-1.18),(1.58,31.45,1.22),purple)
    g("nape",(0,30.2,1.4),parent="head")
    for j,(x,y) in enumerate(((-1.55,21.7),(-.40,20.9),(.74,20.4),(1.63,22.1))):
        rib(m,f"nape_lock_{j}","nape",(x,30.5,1.33),(x*1.17,y,1.58+.12*(j%2)),
            1.33,1.12,lock if j%2==0 else purple)
    for side,s in SIDES:
        hair = "hair_"+side
        g(hair,(s*2,30,-.96),parent="head")
        rib(m,"sidelock_"+side,hair,(s*1.99,30.2,-1.12),(s*2.28,19.1+(s<0)*1.5,-1.21),1.16,1.23,purple)
        rib(m,"outer_lock_"+side,hair,(s*2.24,29.8,.14),(s*2.72,21.0+(s<0)*1.3,.27),.92,1.14,lock)
        # Layer the fringe from a high central part; keep the bar legible.
        for j,(x,y,w) in enumerate(((1.8,29.1,1.08),(2.9,29.5,1.12),(3.35,28.8,.68))):
            rib(m,f"fringe_{side}{j}","head",(s*(.10+.65*j),30.7-.25*j,-1.6+.12*j),
                (s*x,y,-1.75+.18*j),w,.91,purple if j!=2 else lock)
        leafcolor = BLACK if dark else WHITE
        tip = (s*(1.62 if s>0 else 1.12),35.12-(s<0)*.55, .2+s*.26)
        mid = (s*(.93 if s>0 else .67),33.45,.10)
        rib(m,"leaf_base_"+side,"sprout",(s*.10,31.34,.1),mid,.63,.53,leafcolor)
        rib(m,"leaf_blade_"+side,"sprout",mid,tip,.82 if not dark else .38,.49,leafcolor)
        for part, parent, pt in (("thigh","pelvis",(s*.9,16.5,0)),
                                 ("shin","thigh_"+side,(s*1.38,8.8,-.13)),
                                 ("foot","shin_"+side,(s*1.54,2.45,.05))):
            g(part+"_"+side,pt,parent=parent)
        diameter = .83 if dark else 1.53
        hip, knee, ankle = (s*.91,16.55,0),(s*1.38,8.81,-.13),(s*1.54,2.18,.05)
        rib(m,"trouser_"+side,"thigh_"+side,hip,knee,diameter,diameter*1.08,white)
        rib(m,"sock_"+side,"shin_"+side,knee,ankle,diameter*.91,diameter,white)
        if not dark:
            rib(m,"knee_band_"+side,"shin_"+side,knee,lerp(knee,ankle,.22),diameter*.99,diameter*1.07,BAND)
            rib(m,"ankle_band_"+side,"shin_"+side,lerp(knee,ankle,.82),ankle,diameter*.95,diameter*1.06,0xB0ACB9)
        boot_width = .65 if dark else .94
        m.cube("boot_"+side,"foot_"+side,(s*1.54-boot_width,0,-1.40),(s*1.54+boot_width,2.5,.94),trim)

    # Bent primary arms in the first plate, branching hooked forearms in the second,
    # and three independently articulated pairs in the last.
    for side,s in SIDES:
        if phase == 1:
            points = [((1.69,24.4,0),(5.45,17.85,.08),(10.0,20.7,-.75),24)] if s>0 else [
                      ((1.69,24.4,0),(3.50,14.4,.22),(7.8,12.35,-.45),-12)]
        elif dark:
            points = [((1.00,23.8,-.1),(5.42,24.45,0),(9.44,27.90,-.48),32),
                      ((1.05,21.2,.28),(7.90,12.65,.12),(12.0,17,-.50),67)]
            if s<0:
                points[0]=((1.0,23.8,-.1),(5.1,21.3,0),(9.2,20.1,-.4),3)
        else:
            points = [((1.65,22.4,.8),(9.90,22.2,.35),(18.75,22.9,-.34),8),
                      ((1.61,23.0,-.1),(6.55,17.35,-.7),(11.5,15.52,-1.33),-14),
                      ((1.42,18.1,.1),(4.78,10.62,-.12),(6.00,5.9,-1.03),-53)]
            if s<0:
                points[1]=((1.61,21.0,-.1),(7.2,17.64,-.4),(9.6,13.30,-1),-38)
                points[2]=((1.42,18.1,.12),(4.04,11.24,-.12),(5.6,3.95,-1.02),-36)
        for level,(a,b,c,angle) in enumerate(points):
            build_arm(m,phase,side,s,level,a,b,c,angle)
        if phase==3:
            build_wing(m,side,s)


def build_arm(m,phase,side,s,level,a,b,c,angle):
    def point(p):
        return (p[0]*s,p[1],p[2])
    shoulder,elbow,wrist = map(point,(a,b,c))
    tag=f"{level}_{side}"
    arm, fore, hand = ("arm_"+tag, "fore_"+tag, "hand_"+tag)
    for name,at,parent in ((arm,shoulder,"chest"),(fore,elbow,arm),(hand,wrist,fore)):
        m.group(name,at,parent=parent)
    shadow=phase==2
    dark=shadow or (phase==3 and level==0)
    color=BLACK if shadow else LOCK if dark else WHITE
    width=(.64 if level==0 else 1.17) if shadow else 1.38 if dark else .88
    rib(m,"upper_"+tag,arm,shoulder,elbow,width,width*1.02,color)
    rib(m,"radius_"+tag,fore,elbow,wrist,width*1.07,width*1.02,color)
    if not dark:
        rib(m,"short_sleeve_"+tag,arm,shoulder,lerp(shoulder,elbow,.33),1.51,1.44,PAPER)
        rib(m,"sleeve_edge_"+tag,arm,lerp(shoulder,elbow,.30),lerp(shoulder,elbow,.37),1.54,1.47,BAND)
    # The palm's long axis points outward. Finger roots are separated along its
    # edge and each digit has two phalanges, including an opposing raised thumb.
    phi=math.radians(angle)
    extension=1.38 if phase==1 and s>0 else 1.15 if shadow and level==1 else 1
    def palm(u,v,z):
        return (wrist[0]+s*extension*(u*math.cos(phi)-v*math.sin(phi)),
                wrist[1]+extension*(u*math.sin(phi)+v*math.cos(phi)),wrist[2]+z)
    rib(m,"palm_"+tag,hand,palm(0,0,0),palm(2.1,0,-.12),2.0*extension,.95,color)
    m.group("digits_"+tag,palm(1.65,0,-.1),parent=hand)
    fingers=[((.55,.60),(1.16,2.38),(.94,3.62)),
             ((1.68,.77),(3.55,2.22),(4.92,3.24)),
             ((1.95,.32),(4.22,1.14),(6.14,1.81)),
             ((2.04,-.24),(4.26,-.39),(6.07,-.69)),
             ((1.76,-.73),(3.78,-1.40),(5.11,-2.03))]
    if shadow and level==1:
        fingers=[((.7,.6),(1.5,2.2),(2.4,2.6)),((1.7,.6),(4.3,1.7),(5.2,3.3)),
                 ((1.92,-.2),(4.5,-1.0),(5.9,.4)),((1.55,-.7),(3.3,-2.1),(5.1,-2.3))]
    for j,(start,middle,end) in enumerate(fingers):
        root=palm(*start,-.13)
        knuckle=palm(*middle,-.33+.10*j)
        tip=palm(*end,-.59+.17*j)
        thickness=(.54 if phase==1 or dark else .49)*extension
        rib(m,f"finger_{tag}_{j}","digits_"+tag,root,knuckle,thickness,.60,color)
        rib(m,f"tip_{tag}_{j}","digits_"+tag,knuckle,tip,thickness*.78,.48,color)


def build_wing(m,side,s):
    wing="wing_"+side
    m.group(wing,(s*1.3,21.1,1.26),parent="chest")
    # The silhouette has two deep notches in its trailing edge. Continuous
    # narrow solid slices keep the web visible on both sides and edge-on.
    outline=[(4.0,21.1),(9.2,28.0),(10.6,34.2),(15.4,35.5),(29.1,45.0),
             (27.63,39.5),(26.6,33.1),(27.6,30.2),(29.1,28.0),(23.4,26.2),
             (18.9,23.2),(15.2,17.0),(13.5,20.7),(11.7,22.3),(9.0,20.4),(5.7,18.8)]
    # Ink outline is made by separate framing bones along the spars, leaving
    # white membrane all the way to the notched trailing edge as in the plate.
    step=.46
    low=min(y for _,y in outline)
    high=max(y for _,y in outline)
    for row in range(math.ceil((high-low)/step)):
        y=low+row*step
        mid=y+step/2
        xs=[]
        for (a,b),(c,d) in zip(outline,outline[1:]+outline[:1]):
            if min(b,d)<=mid<max(b,d):
                xs.append(a+(c-a)*(mid-b)/(d-b))
        xs.sort()
        for k,(l,r) in enumerate(zip(xs[::2],xs[1::2])):
            x1,x2=sorted((s*l,s*r))
            m.cube(f"membrane_{side}_{row}_{k}",wing,(x1,y,2.73),(x2,y+step+.001,3.15),
                   MEMBRANE,grain=.009,res=1)
    def strut(name,a,b,w,d,col=WING):
        rib(m,name+"_"+side,wing,(s*a[0],a[1],2.91),(s*b[0],b[1],2.91),w,d,col)
    strut("wing_root",(1.4,21.4),(7.0,22.1),2.13,1.72)
    strut("leading_arm",(6.65,21.7),(11.3,28.8),2.55,1.50)
    strut("leading_joint",(11.2,28.1),(12.1,34.9),2.70,1.38)
    strut("leading_spar",(11.65,34.3),(19.1,37.28),1.72,1.22)
    strut("leading_tip",(18.78,37.1),(29.0,45.0),.78,.86)
    strut("upper_rib",(11.6,29.4),(21.5,29.4),2,1.25,RIB)
    strut("upper_rib_point",(21.0,29.4),(28.47,28.0),1.03,.92)
    strut("lower_rib",(8.46,24.75),(13.74,21.33),1.77,1.07)
    strut("lower_point",(13.66,21.37),(15.17,17.04),.84,.81)


# Arm poses are articulated in the natural frame of an outward-reaching arm.
# Angles per pose: shoulder turns forward and rises, elbow turns and rises,
# wrist turns and rolls, then digits fold toward the palm.
ARMS = {
    "rest": (0,0,0,0,0,0,0),
    "ready": (12,8,8,8,-13,6,-15),
    "drag": (-18,-22,-17,-11,9,-12,-15),
    "backswing": (-39,18,-18,18,10,18,-18),
    "sweep": (95,2,24,-13,17,-26,15),
    "cross": (80,18,40,12,12,29,33),
    "stab": (78,4,6,4,0,-4,2),
    "clutch": (56,12,32,21,14,17,59),
    "hug": (62,15,48,31,17,17,76),
    "open": (-11,18,-16,14,-18,22,-22),
    "raise": (12,59,30,27,-24,12,-15),
    "pound": (52,-39,10,-30,8,-12,23),
    "coil": (4,22,67,30,18,12,46),
    "shield": (55,36,65,27,-14,25,28),
    "float": (-8,30,-10,13,12,19,-15),
    "drop": (7,-42,-19,-12,-23,-8,18),
}

# Full-body snapshots: torso pitch/yaw/roll, face pitch/yaw/roll, stance drop,
# stride (right leg positive), left/right arm gestures and wing opening.
# Timelines below combine these as anticipation, contact and follow-through.
POSES = {
    "neutral": ((0,0,0),(0,0,0),0,0,"rest","rest",0),
    "watch": ((-4,-9,4),(4,23,-11),.45,9,"ready","drag",-5),
    "wind_r": ((8,-32,12),(5,19,-6),1.4,24,"ready","backswing",-21),
    "cut_r": ((-17,38,-10),(7,-19,4),1.0,-26,"drag","sweep",11),
    "wind_l": ((9,28,-11),(5,-15,9),1.3,-22,"backswing","ready",-19),
    "cut_l": ((-16,-37,12),(8,21,-9),.9,24,"sweep","drag",16),
    "wind_both": ((9,4,-4),(5,0,6),2,0,"backswing","backswing",-32),
    "cleave": ((-23,4,1),(10,-6,3),1.8,-12,"cross","cross",24),
    "bunch": ((-19,-12,7),(-11,9,-6),2.6,18,"shield","coil",-44),
    "stretch": ((-27,20,-4),(18,-18,-4),1.1,-36,"drag","stab",6),
    "trail": ((-12,23,-8),(1,-13,6),1,-20,"drop","ready",-4),
    "take": ((-17,11,-2),(9,-9,2),1.1,-21,"stab","stab",7),
    "hold": ((-14,6,3),(0,-6,-4),1.15,-15,"clutch","clutch",2),
    "pull": ((13,-12,5),(-13,10,-5),1.65,20,"hug","hug",-18),
    "throw": ((-16,-34,10),(8,23,-5),.9,26,"sweep","cross",21),
    "jaw": ((9,-1,-4),(32,6,8),1.45,15,"clutch","hug",-15),
    "bite": ((-34,3,3),(-24,-2,-6),2.3,-24,"hug","clutch",9),
    "swallow": ((7,7,-3),(16,-7,6),.8,-6,"clutch","ready",-9),
    "hide_face": ((-15,0,1),(-26,6,-9),2.1,0,"shield","shield",-36),
    "glare": ((16,0,-2),(-7,0,0),.18,-7,"open","open",37),
    "blink": ((3,4,-2),(1,-3,3),.3,-4,"float","ready",18),
    "aim": ((6,-19,6),(-5,15,-6),.95,18,"ready","coil",-9),
    "flick_r": ((-6,19,-4),(2,-16,1),.77,-8,"coil","stab",12),
    "flick_l": ((-8,-17,6),(5,13,-2),.65,11,"stab","coil",7),
    "flick_both": ((-13,1,1),(7,-2,0),1.0,-16,"stab","stab",20),
    "tiptoe": ((-9,14,-10),(-7,-21,13),1.28,37,"drop","ready",-27),
    "spring": ((-21,-18,6),(10,18,-5),.35,-43,"drag","coil",-39),
    "rake_up": ((-5,24,10),(-8,-15,-8),.8,15,"drag","raise",24),
    "overhead": ((19,0,-3),(12,1,3),.48,7,"raise","raise",33),
    "ground": ((-48,0,2),(15,2,-2),3.1,-8,"pound","pound",-6),
    "kneel": ((-27,-3,4),(5,2,-6),2.4,4,"drop","drop",-12),
    "launch": ((2,-2,2),(8,2,-3),1.7,26,"open","open",43),
    "glide": ((-27,0,3),(21,0,-2),.3,-38,"drag","drag",-43),
    "ram": ((-40,7,-2),(13,-8,0),.5,-24,"stab","cross",12),
    "land": ((-18,-5,4),(11,6,-4),2.0,9,"drop","ready",24),
    "listen": ((-2,6,-5),(-16,-6,20),.8,2,"float","ready",-5),
    "summon": ((17,-4,-1),(30,6,2),.18,-5,"raise","float",30),
    "release": ((-7,0,1),(-13,0,-7),1.2,1,"open","open",40),
    "shiver": ((-17,13,11),(-22,-13,-20),2.1,-3,"shield","coil",-50),
    "rupture": ((19,-6,-7),(29,6,12),.12,6,"raise","open",45),
    "spent": ((-16,-4,7),(-18,6,-12),1.7,-5,"drop","drag",-17),
}

ACTIONS = {
    "long_sweep": (36,[(6,"watch"),(12,"wind_r"),(16,"cut_r"),(21,"trail"),(28,"watch")]),
    "double_rake": (42,[(8,"wind_r"),(12,"cut_r"),(18,"trail"),(22,"wind_l"),
                          (26,"cut_l"),(32,"land")]),
    "elastic_thrust": (38,[(6,"aim"),(11,"bunch"),(12,"spring"),(18,"stretch"),
                            (21,"stretch"),(29,"trail")]),
    "grasp_pull": (48,[(8,"wind_both"),(14,"take"),(16,"hold"),(23,"pull"),
                        (27,"pull"),(30,"throw"),(36,"trail")]),
    "assimilation_bite": (54,[(8,"watch"),(12,"open",), (16,"take"),(20,"hold"),
                              (26,"jaw"),(30,"bite"),(34,"bite"),(41,"swallow"),(48,"spent")]),
    "eye_flash": (42,[(6,"listen"),(13,"hide_face"),(19,"hide_face"),(20,"glare"),
                      (24,"glare"),(29,"blink"),(35,"watch")]),
    "paper_shards": (38,[(7,"watch"),(13,"aim"),(18,"flick_r"),(20,"aim"),
                         (22,"flick_l"),(24,"wind_both"),(26,"flick_both"),(30,"trail")]),
    "stalking_step": (40,[(4,"watch"),(7,"tiptoe"),(8,"spring"),(13,"spring"),
                          (17,"wind_r"),(20,"rake_up"),(25,"trail"),(32,"watch")]),
    "ground_slam": (46,[(6,"bunch"),(14,"overhead"),(20,"overhead"),(24,"ground"),
                        (28,"ground"),(34,"kneel"),(40,"spent")]),
    "wing_rush": (44,[(6,"bunch"),(11,"launch"),(12,"glide"),(17,"glide"),
                      (20,"ram"),(25,"land"),(33,"watch")]),
    "host_echo": (64,[(8,"listen"),(16,"hide_face"),(21,"listen"),(28,"summon"),
                      (32,"release"),(37,"glare"),(45,"listen"),(54,"spent")]),
    "frenzy": (66,[(5,"shiver"),(11,"wind_r"),(14,"cut_r"),(20,"trail"),
                   (26,"wind_l"),(30,"cut_l"),(36,"land"),(42,"overhead"),
                   (46,"cleave"),(50,"ground"),(58,"spent")]),
    "transform_second": (60,[(8,"listen"),(16,"shiver"),(22,"hide_face"),(26,"shiver"),
                             (30,"bunch"),(35,"rupture"),(41,"glare"),(49,"spent")]),
    "transform_third": (70,[(9,"spent"),(17,"listen"),(26,"hide_face"),(32,"shiver"),
                            (35,"bunch"),(40,"rupture"),(47,"launch"),(52,"glare"),
                            (60,"blink")]),
}
POSES["open"] = ((5,3,-2),(4,-3,0),.7,9,"open","open",13)


def full_pose(m,phase,key):
    chest,head,drop,stride,left,right,wing=POSES[key]
    lean,twist,tilt=chest
    pose={"chest":chest,"head":head,"pelvis":(-drop*2,-twist*.18,-tilt*.23),
          "sprout":(-lean*.42,twist*.17,-tilt*.56),"nape":(-lean*.57,-twist*.18,-tilt*.35)}
    for side,s in SIDES:
        pose["hair_"+side]=(-lean*.56,-twist*.25,-tilt*.31+s*drop*1.2)
        pose["thigh_"+side]=(s*stride+drop*8,twist*s*.09,s*drop*2)
        pose["shin_"+side]=(-drop*15-max(0,s*stride)*.45,0,0)
        pose["foot_"+side]=(drop*5-s*stride*.32,0,0)
        if phase==3:
            pose["wing_"+side]=(lean*.10,s*(wing*.89+twist*.12),s*wing*.22)
        for level in range(3 if phase==3 else 2 if phase==2 else 1):
            tag=f"{level}_{side}"
            motion=right if s==1 else left
            advance,lift,bend,rise,turn,roll,grip=ARMS[motion]
            # Additional arms reach and recoil from their own initial elevations.
            # Middle ranks lead frontal attacks; the high pair frames the head.
            factor=1-level*.11
            pose["arm_"+tag]=(lean*.12,s*advance*factor,s*(lift*factor-level*advance*.07))
            pose["fore_"+tag]=(bend*.09,s*(bend+level*advance*.08),s*rise*factor)
            pose["hand_"+tag]=(-roll*.18,s*turn,s*(roll+level*bend*.10))
            pose["digits_"+tag]=(0,s*grip,s*grip*.12)
    return pose,(tilt*.047,-drop,lean*.045)


def track(tracks,bone,channel,tick,value):
    frames=tracks.setdefault(bone,{}).setdefault(channel,[])
    frames.append((tick/20,*(round(v,3) for v in value)))


def author_action(m,phase,name,length,beats,scale):
    tracks={}
    for tick,key in [(0,"neutral"),*beats,(length,"neutral")]:
        pose,shift=full_pose(m,phase,key)
        for bone,value in pose.items():
            # Hair finishes the movement after the head and shoulders.
            delay=2 if bone.startswith(("hair_","nape","sprout")) and tick not in (0,length) else 0
            track(tracks,bone,"rotation",tick+delay,value)
        track(tracks,"pelvis","position",tick,tuple(v*scale for v in shift))
    if name=="elastic_thrust":
        for side,s in SIDES:
            tag="0_"+side
            # Stretch the forearm on its bone's outward axis, carrying the palm along.
            for tick,k in [(0,1),(11,.91),(18,1.7 if s>0 else 1.05),(22,1.55 if s>0 else 1),(30,1),(length,1)]:
                track(tracks,"fore_"+tag,"scale",tick,(k,1+(k-1)*.23,1))
    if name in ("transform_second","transform_third"):
        next_phase=2 if name=="transform_second" else 3
        middle=30 if next_phase==2 else 35
        ratio={2:2.2/3.6,3:3.6/4.8}[next_phase]
        minimum=(ratio if phase==next_phase else 1)*.90
        for tick,size in [(0,1),(middle-7,.90),(middle,minimum),(middle+9,1.04),(length,1)]:
            track(tracks,"root","scale",tick,(size,size,size))
    m.anim(name,length/20,tracks)


def locomotion(m,phase,scale,walking):
    length=28 if walking else 80
    tracks={}
    for j in range(9):
        f=j*math.pi/4
        tick=length*j/8
        wave,second=math.sin(f),math.sin(2*f)
        if walking:
            drop=.48*(1-math.cos(f*2))
            torso=(-4+1.6*second,6*wave,2*math.cos(f))
            head=(2.0*math.cos(f*2),-4*wave,-2*math.cos(f))
        else:
            drop=.14*(1-math.cos(f))
            torso=(1.8*wave,1.7*math.cos(f),1.25*math.sin(f+.6))
            head=(1.3*math.cos(f),3.4*math.sin(f+.4),2.2*math.cos(f-.6))
        bones={"chest":torso,"head":head,"sprout":(-1.7*wave,0,2.5*math.cos(f+.3)),
               "pelvis":(0,-torso[1]*.45,-torso[2]*.45),"nape":(-2*wave,0,torso[2]*-.42)}
        for side,s in SIDES:
            bones["hair_"+side]=(-1.9*math.sin(f-.4),-1.5*wave,s*.7+torso[2]*-.7)
            if walking:
                stride=s*30*wave
                bend=max(0,-s*math.cos(f))*32
                bones["thigh_"+side]=(stride+3,0,s*1.2)
                bones["shin_"+side]=(-bend-3,0,0)
                bones["foot_"+side]=(bend*.6-stride*.54,0,0)
            for level in range(3 if phase==3 else 2 if phase==2 else 1):
                w=math.sin(f-level*.55+s*.18)
                amp=15 if walking else 2.3
                tag=f"{level}_{side}"
                bones["arm_"+tag]=(w*amp*.24,w*amp,s*2.4*math.cos(f+.4*level))
                bones["fore_"+tag]=(0,amp*.43*w,s*2.8*math.sin(f-.5))
                bones["hand_"+tag]=(w*1.4,-amp*.28*w,s*3*math.sin(f-.8))
                bones["digits_"+tag]=(0,s*(3+3*w),0)
            if phase==3:
                bones["wing_"+side]=(1.7*wave,s*(4.5 if walking else 2.4)*wave,
                                     s*(2.7 if walking else 1.4)*math.cos(f))
        for bone,value in bones.items():
            track(tracks,bone,"rotation",tick,value)
        track(tracks,"pelvis","position",tick,(wave*scale*(.36 if walking else .10),-drop*scale,0))
    m.anim("walk" if walking else "idle",length/20,tracks,loop=True)


def death(m,phase,scale):
    tracks={}
    for tick,key in [(0,"neutral"),(4,"rupture"),(10,"hide_face"),(17,"kneel"),
                     (25,"spent"),(32,"ground"),(40,"spent")]:
        pose,_=full_pose(m,phase,key)
        for bone,value in pose.items():
            if tick>=25 and bone.startswith("wing_"):
                s=1 if bone.endswith("_r") else -1
                value=(0,-s*38,s*-12)
            track(tracks,bone,"rotation",tick,value)
    # Rearward collapse leaves the two long hands and wing webs lying beside
    # the torso. A small rebound keeps the final impact visible.
    for tick,angle,height in [(0,0,0),(7,0,0),(14,10,-.9),(20,38,-1.2),
                              (27,79,.55),(31,84,1.65),(34,80,1.8),(40,83,1.65)]:
        track(tracks,"root","rotation",tick,(angle,0,0))
        track(tracks,"root","position",tick,(0,height*scale,0))
    m.anim("death",2,tracks)


def make(phase):
    name=("paperblight","paperblight_phase2","paperblight_phase3")[phase-1]
    scale=(1,3.6/2.2,4.8/2.2)[phase-1]
    # Re-running this generator produces identical group and animation IDs.
    serial=itertools.count()
    bbgen.u=lambda: str(uuid.uuid5(uuid.NAMESPACE_URL,f"fpe/{name}/{next(serial)}"))
    m=Model(name,S=3,atlas=512)
    build_body(m,phase)
    for group in m.groups.values():
        group["origin"]=[round(v*scale,4) for v in group["origin"]]
    for cube in m.cubes:
        for field in ("origin","from","to"):
            cube[field]=[round(v*scale,4) for v in cube[field]]
        cube["rotation"]=[round(v,4) for v in cube["rotation"]]
    locomotion(m,phase,scale,False)
    locomotion(m,phase,scale,True)
    for action,(length,beats) in ACTIONS.items():
        author_action(m,phase,action,length,beats,scale)
    death(m,phase,scale)
    m.save(OUT/(name+".bbmodel"))
    print(name,len(m.cubes),"elements,",len(m.anims),"animations")


if __name__=="__main__":
    for form in (1,2,3):
        make(form)

