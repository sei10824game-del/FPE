"""Paperblight HOST Lana, Edward and Oliver from the supplied 2026-11-24 plates.

All shapes are authored solids: polygonal hair/horns/blades use shallow extruded
cube slices, never reference-image billboards. Blockbench units: Y up, -Z front,
16 units = one block. Combat moves are original mod choreography, not canon claims.
Run this file to regenerate the three embedded-texture, articulated bbmodels.
"""
import math
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from bbgen import Model, mix

OUT = Path(__file__).resolve().parents[3] / 'src/main/resources/assets/fpe/bbmodels'
PAPER, WHITE, SHADE = 0xC8C7CF, 0xE5E4E8, 0x92919E
INK, BLACK, PURPLE = 0x24212C, 0x111016, 0x30283E
HAIR, HAIR_D, RED = 0x8D8D9A, 0x60606F, 0x75232E
SIDES = (('r', 1), ('l', -1))


def rib(m, name, bone, a, b, width, depth, color):
    dx, dy, dz = (v-u for u, v in zip(a,b))
    length = math.dist(a,b)
    return m.cube(name,bone,(a[0]-width/2,a[1]-.04,a[2]-depth/2),
                  (a[0]+width/2,a[1]+length+.04,a[2]+depth/2),color,
                  origin=a,rot=(math.degrees(math.asin(dz/length)),0,
                                -math.degrees(math.atan2(dx,dy))),grain=.022)


def solid(m, name, bone, polygon, z, depth, color, step=.25):
    """Extruded polygon, with true thickness and an edge visible in side views."""
    y0, y1 = min(p[1] for p in polygon), max(p[1] for p in polygon)
    n = max(1, math.ceil((y1-y0)/step))
    for k in range(n):
        lo, hi = y0+(y1-y0)*k/n, y0+(y1-y0)*(k+1)/n
        y=(lo+hi)/2
        xs=[]
        for a,b in zip(polygon,polygon[1:]+polygon[:1]):
            if min(a[1],b[1]) <= y < max(a[1],b[1]):
                xs.append(a[0]+(y-a[1])*(b[0]-a[0])/(b[1]-a[1]))
        xs.sort()
        for j in range(0,len(xs)-1,2):
            m.cube(f'{name}_{k}_{j}',bone,(xs[j],lo,z-depth/2),
                   (xs[j+1],hi+.012,z+depth/2),color,grain=.018,res=3)


def cloth(F):
    for x in (int(F.w*.13),int(F.w*.82)):
        F.line(x,F.h*.15,x+1,F.h*.90,SHADE,1)
    F.line(1,F.h-2,F.w-2,F.h-2,SHADE,1)


def puppet_eye(F):
    F.disc(F.w*.5,F.h*.5,min(F.w,F.h)*.30,BLACK)
    F.disc(F.w*.44,F.h*.40,min(F.w,F.h)*.07,WHITE)


def face_oliver(F):
    W,H=F.w,F.h
    for ex in (.27,.73):
        F.poly([(W*(ex-.19),H*.34),(W*(ex-.10),H*.22),
                (W*(ex+.09),H*.25),(W*(ex+.17),H*.42),
                (W*(ex+.10),H*.55),(W*(ex-.12),H*.54)],BLACK)
        F.disc(W*ex,H*.40,W*.024,0xBFC0CB)
        for j in range(3):
            x=W*(ex-.09+j*.085)
            F.line(x,H*.51,x+(-1 if j%2 else 1),H*(.64+j*.035),HAIR_D,1)
    F.poly([(W*.09,H*.73),(W*.25,H*.77),(W*.48,H*.72),
            (W*.74,H*.78),(W*.93,H*.72),(W*.85,H*.87),
            (W*.50,H*.91),(W*.19,H*.87)],BLACK)
    F.line(W*.19,H*.80,W*.82,H*.82,WHITE,1)
    for i in range(7):
        x=W*(.22+i*.09)
        F.line(x,H*.77,x+1,H*.86,HAIR_D,1)
    F.line(W*.48,H*.57,W*.43,H*.67,HAIR_D,1)


def diamond(F):
    W,H=F.w,F.h
    for a,b in [((.5,.21),(.77,.43)),((.77,.43),(.5,.68)),
                ((.5,.68),(.24,.43)),((.24,.43),(.5,.21))]:
        F.line(a[0]*W,a[1]*H,b[0]*W,b[1]*H,SHADE,1.5)
    F.line(W*.25,H*.43,W*.76,H*.43,SHADE,1)


def skeleton(m, hip, shoulder, neck):
    m.group('root')
    m.group('pelvis',(0,hip,0),parent='root')
    m.group('chest',(0,hip+.5,0),parent='pelvis')
    m.group('head',(0,neck,0),parent='chest')
    m.group('hair',(0,neck+3,.8),parent='head')
    m.group('sprout',(0,neck+5,0),parent='head')
    for side,s in SIDES:
        m.group('thigh_'+side,(s*1.18,hip,0),parent='pelvis')
        m.group('shin_'+side,(s*1.30,hip*.48,-.03),parent='thigh_'+side)
        m.group('foot_'+side,(s*1.40,2.6,0),parent='shin_'+side)
        m.group('arm_'+side,(s*2.24,shoulder,0),parent='chest')


def leg(m, side, s, hip, knee, cuff, trouser, sock, boot_height=3.7, stripes=False):
    thigh,shin,foot=('thigh_'+side,'shin_'+side,'foot_'+side)
    m.groups[shin]['origin']=[s*1.30,knee,-.03]
    m.groups[foot]['origin']=[s*1.40,boot_height-.2,0]
    a,b,c=(s*1.18,hip,0),(s*1.30,knee,-.03),(s*1.40,boot_height-.2,0)
    rib(m,'thigh_solid_'+side,thigh,a,b,1.67,1.83,trouser)
    rib(m,'calf_solid_'+side,shin,b,c,1.25,1.45,sock)
    if cuff:
        m.cube('trouser_cuff_'+side,thigh,(s*1.3-1.0,knee-.25,-1.01),
               (s*1.3+1.0,knee+.42,1.01),INK)
    if stripes:
        for y in (5.9,8.8,10.7):
            m.cube(f'shin_band_{side}_{y}',shin,(s*1.34-.67,y,-.77),
                   (s*1.34+.67,y+.75,.76),SHADE)
    m.cube('boot_shaft_'+side,foot,(s*1.4-.94,.6,-.91),
           (s*1.4+.94,boot_height,1.05),BLACK)
    m.cube('boot_toe_'+side,foot,(s*1.4-1.0,0,-1.67),
           (s*1.4+1.0,1.45,.82),INK)
    m.cube('boot_cuff_'+side,foot,(s*1.4-1.08,boot_height-.6,-1.02),
           (s*1.4+1.08,boot_height+.12,1.12),INK)


def puppet(m,side,s,wrist):
    hand='hand_'+side
    x,y,z=wrist
    # A puppet head is the hand itself: bulbous eyes, projecting muzzle and
    # articulated hanging jaw, rather than an ordinary five-fingered hand.
    m.cube('puppet_skull_'+side,hand,(x-1.45,y-2.55,z-1.0),
           (x+1.45,y+.5,z+1.12),PAPER,faces={'north':cloth})
    m.cube('puppet_snout_'+side,hand,(x-1.58,y-2.75,z-2.25),
           (x+1.58,y-1.65,z-.2),SHADE)
    for j,sign in enumerate((-1,1)):
        ex=x+sign*1.05
        circle=[(ex+math.cos(k*math.pi/8)*.66,y+.05+math.sin(k*math.pi/8)*.72) for k in range(16)]
        solid(m,f'eye_bulb_{side}_{j}',hand,circle,z-1.20,1.20,WHITE,.15)
        m.cube(f'eye_pupil_{side}_{j}',hand,(ex-.29,y-.29,z-1.83),
               (ex+.29,y+.31,z-1.79),WHITE,faces={'north':puppet_eye},res=12)
    m.cube('puppet_mouth_void_'+side,hand,(x-1.40,y-3.55,z-1.84),
           (x+1.40,y-2.55,z-.46),BLACK)
    jaw='jaw_'+side
    m.group(jaw,(x,y-2.30,z+.1),parent=hand)
    m.cube('lower_puppet_jaw_'+side,jaw,(x-1.30,y-3.96,z-2.15),
           (x+1.30,y-3.62,z+.18),PAPER)
    m.cube('puppet_tongue_'+side,jaw,(x-.51,y-3.58,z-1.80),
           (x+.51,y-3.39,z-.32),0x595064)
    for j in range(5):
        tx=x-1.24+j*.60
        rib(m,f'puppet_fringe_{side}{j}',hand,(tx,y-2.51,z-2.32),
            (tx+s*.15,y-3.0-(j%2)*.22,z-2.40),.49,.30,PURPLE)


def lana():
    m=Model('host_lana',S=5,atlas=2048)
    skeleton(m,23.7,29.2,32.0)
    # The upper body has a real open, empty neck. Four collar walls expose a
    # recessed dark cavity from the front/above; there is deliberately no head.
    m.cube('jumpsuit_hips','pelvis',(-2.2,22.4,-1.05),(2.2,24.5,1.1),PAPER)
    solid(m,'tapered_jumpsuit','chest',[(-2.15,23.7),(2.15,23.7),
          (2.75,26.2),(1.02,32.3),(-1.02,32.3),(-2.75,26.2)],0,2.3,PAPER,.30)
    m.cube('neck_void','head',(-.78,32.32,-.70),(.78,32.35,.70),BLACK)
    for tag,a,b in [('back',(-1.02,32.4,.60),(1.02,33.6,1.00)),
                    ('front',(-1.02,32.4,-1.0),(1.02,33.1,-.6)),
                    ('right',(.64,32.4,-.60),(1.02,33.4,.60)),
                    ('left',(-1.02,32.4,-.60),(-.64,33.4,.60))]:
        m.cube('hollow_neck_rim_'+tag,'head',a,b,SHADE)
    m.cube('waist_band','pelvis',(-2.35,23.6,-1.20),(2.35,24.25,1.23),SHADE)
    for y in (28.8,27.1):
        m.cube('jumpsuit_button_'+str(y),'chest',(-.16,y,-1.22),(.16,y+.32,-1.12),SHADE)
    for side,s in SIDES:
        leg(m,side,s,23.7,8.1,True,PAPER,PAPER,4.1)
        sh=(s*2.24,29.2,0)
        # One arm reaches sideways toward the viewer, the other drags low.
        el=(s*(6.1 if s<0 else 4.6),26.1 if s<0 else 20.7,-.12)
        wr=(s*(8.0 if s<0 else 5.9),24.4 if s<0 else 13.1,-.48)
        m.group('fore_'+side,el,parent='arm_'+side)
        m.group('hand_'+side,wr,parent='fore_'+side)
        m.group('digits_'+side,wr,parent='hand_'+side)
        rib(m,'sleeve_'+side,'arm_'+side,sh,
            tuple(sh[i]+(el[i]-sh[i])*.28 for i in range(3)),2.46,2.4,PAPER)
        rib(m,'long_purple_upper_'+side,'arm_'+side,sh,el,1.25,1.30,PURPLE)
        rib(m,'long_purple_fore_'+side,'fore_'+side,el,wr,1.12,1.21,PURPLE)
        puppet(m,side,s,wr)
    return m


def goggle(F):
    W,H=F.w,F.h
    # Clear rectangular carrier with a round, thick black rim.
    for y in range(H):
        for x in range(W):
            u,v=(x+.5)/W-.5,(y+.5)/H-.5
            d=math.hypot(u,v)
            if d>.49:F.px(x,y,(0,0,0,0))
            elif d>.37:F.px(x,y,BLACK)
            else:F.px(x,y,0x737786)
    F.line(W*.24,H*.69,W*.64,H*.20,0xA6A9B7,2)


def edward():
    m=Model('host_edward',S=5,atlas=2048)
    skeleton(m,14.7,24.4,26.2)
    m.cube('pelvis_trousers','pelvis',(-1.9,13.2,-1.02),(1.9,15.8,1.05),BLACK)
    solid(m,'pale_jacket','chest',[(-2.85,15.0),(2.85,15.0),(2.10,24.8),
          (-2.10,24.8)],0,2.25,PAPER)
    m.cube('jacket_opening','chest',(-.54,15.0,-1.20),(.54,24.35,-1.12),BLACK)
    solid(m,'tie','chest',[(-.32,24),(.35,24),(.47,18.5),(0,17.9),(-.46,18.5)],-1.34,.18,INK)
    for y in (20.2,21.7,23):
        m.cube('tie_button_'+str(y),'chest',(-.13,y,-1.48),(.13,y+.23,-1.35),WHITE)
    for side,s in SIDES:
        solid(m,'lapel_'+side,'chest',[(s*.1,24.4),(s*1.8,24.4),
              (s*1.15,21.0),(s*.48,22.0)],-1.27,.25,WHITE)
        leg(m,side,s,14.7,7.1,False,BLACK,BLACK,2.3)
        sh=(s*2.24,24.4,0)
        el=(s*4.7,18.2,-.05)
        wr=(s*6.35,13.0 if s>0 else 11.2,-.40)
        m.group('fore_'+side,el,parent='arm_'+side)
        m.group('hand_'+side,wr,parent='fore_'+side)
        m.group('digits_'+side,wr,parent='hand_'+side)
        rib(m,'sleeve_upper_'+side,'arm_'+side,sh,el,1.10,1.38,PAPER)
        rib(m,'sleeve_fore_'+side,'fore_'+side,el,wr,1.22,1.49,PAPER)
        # Cut-off arm in the plate, with a visibly hollow dark circular end.
        m.cube('end_cuff_'+side,'hand_'+side,(wr[0]-.91,wr[1]-.52,-1.27),
               (wr[0]+.91,wr[1]+.51,.56),SHADE)
        m.cube('stub_void_'+side,'hand_'+side,(wr[0]-.60,wr[1]-.57,-1.30),
               (wr[0]+.60,wr[1]-.51,.52),BLACK)
        if s<0:
            solid(m,'ragged_stub_flap','hand_'+side,[(wr[0]-.88,wr[1]+.4),
                  (wr[0]+1.02,wr[1]+.1),(wr[0]+1.5,wr[1]-1.0),
                  (wr[0]+.2,wr[1]-.75)],-.25,1.15,PAPER)
    m.cube('skull','head',(-1.75,26,-1.12),(1.75,31.25,1.2),SHADE)
    m.cube('open_monster_mouth','head',(-1.73,25.9,-1.63),(1.73,29.4,-1.03),BLACK)
    solid(m,'red_throat','head',[(-.90,26.35),(.70,26.2),(1.00,27.0),
          (.74,28.55),(.18,29.12),(-.42,27.45),(-1.03,27.27)],-1.70,.18,RED,.18)
    m.group('jaw_r',(1.30,29.0,-1.2),parent='head')
    m.group('jaw_l',(-1.30,29.0,-1.2),parent='head')
    for s in (-1,1):
        for k in range(3):
            solid(m,f'maw_tooth_{s}_{k}','jaw_r' if s>0 else 'jaw_l',
                  [(s*(.40+k*.42),29.1-k*.24),(s*(.64+k*.42),28.2-k*.33),
                   (s*(.78+k*.39),28.9-k*.25)],-1.83,.26,PAPER,.16)
    # Layered starburst silhouette: numerous tapered solid locks around the skull.
    locks=[([(-.3,31.0),(-2.0,33.6),(-2.8,34.4),(-2.5,31.2)],HAIR),
           ([(0,31),(0,35.2),(1.4,33.4),(1.8,30.5)],HAIR),
           ([(1.0,30.2),(3.5,34.3),(3.4,31.4),(2.8,29)],HAIR),
           ([(-1.4,30.0),(-5.2,33.6),(-4.1,30.1),(-2.4,28.8)],HAIR_D),
           ([(-1.6,29.1),(-6.3,29.0),(-3.9,31.2),(-.9,30.1)],HAIR),
           ([(1.7,29.8),(5.8,28.6),(3.9,28.4),(2.0,28.8)],HAIR),
           ([(-1.6,28.0),(-5.3,26.5),(-3.5,26.3),(-1.4,27.1)],HAIR_D),
           ([(1.4,27.8),(5.6,25.8),(3.1,26.0),(1.4,26.8)],HAIR),
           ([(-1.5,26.8),(-5.0,23.5),(-2.8,24.0),(-1.1,25.7)],HAIR),
           ([(1.3,26.6),(5.6,22.2),(3.0,23.1),(1.1,25.6)],HAIR),
           ([(-1.4,25.8),(-4.7,20.4),(-2.5,22.0),(-.9,25.0)],HAIR_D),
           ([(1.2,25.6),(4.1,20.6),(1.8,21.8),(.7,25.2)],HAIR_D)]
    for k,(poly,col) in enumerate(locks):
        solid(m,'spiky_hair_'+str(k),'hair',poly,.60 if k>5 else .03,1.20,col)
    m.cube('goggle_strap','head',(-2.12,30,-1.28),(2.12,30.37,1.27),BLACK)
    for s in (-1,1):
        m.cube('round_goggle_'+str(s),'head',(s*1.16-1.02,29.2,-1.87),
               (s*1.16+1.02,31.24,-1.52),HAIR,
               faces={'north':goggle,'south':goggle},res=12)
    m.cube('goggle_bridge','head',(-.28,30.0,-1.88),(.28,30.36,-1.52),BLACK)
    return m


def oliver():
    m=Model('host_oliver',S=5,atlas=2048)
    skeleton(m,16.7,25.5,27.3)
    m.cube('black_shirt','chest',(-2.06,17.0,-1.08),(2.06,25.4,1.15),INK,
           faces={'north':diamond},res=8)
    m.cube('shirt_hem','chest',(-2.15,16.9,-1.16),(2.15,17.35,1.22),SHADE)
    m.cube('white_shorts_hip','pelvis',(-2.0,14.7,-1.03),(2.0,17.0,1.1),WHITE)
    for side,s in SIDES:
        leg(m,side,s,16.7,11.9,False,WHITE,PAPER,4.3,True)
        # Short trouser hem and exposed striped shins remain clearly separate.
        m.cube('shorts_hem_'+side,'thigh_'+side,(s*1.3-.93,11.6,-1.0),
               (s*1.3+.93,12.05,1.02),SHADE)
        solid(m,'shirt_collar_'+side,'chest',[(s*.13,25.9),(s*1.48,26.0),
              (s*1.22,24.4),(s*.15,25.0)],-1.25,.22,WHITE)
        sh=(s*2.24,25.5,0)
        el=(s*4.1,16.7,-.05)
        wr=(s*5.55,9.8,-.36)
        m.group('fore_'+side,el,parent='arm_'+side)
        m.group('hand_'+side,wr,parent='fore_'+side)
        m.group('digits_'+side,(wr[0],wr[1]-1,-.5),parent='hand_'+side)
        rib(m,'white_upper_arm_'+side,'arm_'+side,sh,el,1.28,1.48,PAPER)
        rib(m,'long_forearm_'+side,'fore_'+side,el,wr,1.35,1.55,PAPER)
        rib(m,'black_short_sleeve_'+side,'arm_'+side,sh,
            tuple(sh[i]+(el[i]-sh[i])*.27 for i in range(3)),1.69,1.75,INK)
        m.cube('wrist_band_'+side,'hand_'+side,(wr[0]-.85,wr[1]-.08,-1.23),
               (wr[0]+.85,wr[1]+.55,.45),INK)
        if s>0:
            # Long open hand, four separated clawlike fingers plus opposing thumb.
            solid(m,'elongated_palm','hand_'+side,[(wr[0]-.85,wr[1]),
                  (wr[0]+.85,wr[1]),(wr[0]+1.05,wr[1]-2.3),
                  (wr[0]-.90,wr[1]-2.9)],-.43,1.12,PAPER)
            for j in range(4):
                a=(wr[0]-.81+j*.57,wr[1]-2.15,-.61)
                b=(a[0]+.72,wr[1]-4.25-j*.21,-.85)
                c=(a[0]+.15,wr[1]-5.21-j*.24,-.96)
                rib(m,'finger_'+str(j),'digits_'+side,a,b,.40,.47,PAPER)
                rib(m,'finger_tip_'+str(j),'digits_'+side,b,c,.34,.40,WHITE)
            rib(m,'opposing_thumb','digits_'+side,(wr[0]-.7,wr[1]-.6,-.5),
                (wr[0]-1.68,wr[1]-2,-.72),.54,.56,PAPER)
        else:
            # The other hand is an asymmetric broad pointed paper blade.
            solid(m,'blade_hand','hand_'+side,[(wr[0]-.85,wr[1]),
                  (wr[0]+.77,wr[1]),(wr[0]+1.47,wr[1]-4.3),
                  (wr[0]-.03,wr[1]-5.5),(wr[0]-1.17,wr[1]-3.28)],-.43,.99,PAPER)
            rib(m,'blade_ridge','digits_'+side,(wr[0]-.43,wr[1]-.5,-1.00),
                (wr[0]+.05,wr[1]-4.72,-1.00),.12,.10,SHADE)
    m.cube('neck','head',(-.73,25.5,-.68),(.73,28.2,.72),PAPER)
    m.cube('haunted_face','head',(-1.91,27.2,-1.36),(1.91,31.7,1.12),PAPER,
           faces={'north':face_oliver},res=12)
    m.cube('hair_crown','hair',(-2.10,31.1,-1.35),(2.10,32.15,1.48),WHITE)
    for side,s in SIDES:
        polys=[[(s*.1,32.15),(s*3.7,32.0),(s*5.5,31.3),(s*3.8,30.7),(s*1.1,30.8)],
               [(s*.6,31.6),(s*4.8,30.6),(s*6.1,28.1),(s*3.3,28.7),(s*1.0,30.2)],
               [(s*1.2,30.8),(s*2.5,30.8),(s*2.95,23.4),(s*1.9,22.4),(s*1.6,27.8)],
               [(s*.2,31.9),(s*1.2,31.7),(s*1.35,29.6),(s*.7,29.4)],
               [(s*1.2,31.5),(s*2.3,31.4),(s*3.3,30.0),(s*1.7,29.8)]]
        for k,poly in enumerate(polys):
            solid(m,f'white_hair_{side}_{k}','hair',poly,-1.28 if k>=3 else .15,
                  1.03 if k>=3 else 1.7,WHITE if k%2 else PAPER)
        solid(m,'dark_horn_'+side,'head',[(s*1.12,31.5),(s*2.85,31.2),
              (s*3.02,33.3),(s*2.5,33.0)],-1.10,1.18,PURPLE,.20)
        solid(m,'upward_sprout_'+side,'sprout',[(s*.1,32.15),
              (s*.53,32.2),(s*1.70,36.8 if s<0 else 36.3),
              (s*.65,34.2)],.15,.55,WHITE,.18)
    return m


def P(chest=(0,0,0), pelvis=(0,0,0), ar=(0,0,0), al=(0,0,0),
      fr=(0,0,0), fl=(0,0,0), lr=(0,0,0), ll=(0,0,0),
      kr=(0,0,0), kl=(0,0,0), xyz=(0,0,0), head=(0,0,0),
      hands=(0,0), fingers=0, jaw=0):
    """A complete articulated pose; all attack stages own the entire body."""
    return {'chest':chest,'pelvis':pelvis,'head':head,
            'arm_r':ar,'arm_l':al,'fore_r':fr,'fore_l':fl,
            'thigh_r':lr,'thigh_l':ll,'shin_r':kr,'shin_l':kl,
            'foot_r':(-kr[0]*.35,0,-lr[2]*.3),
            'foot_l':(-kl[0]*.35,0,-ll[2]*.3),
            'hand_r':(hands[0],-ar[1]*.24,-ar[2]*.28),
            'hand_l':(hands[1],-al[1]*.24,-al[2]*.28),
            'digits_r':(fingers,0,-fingers*.17),
            'digits_l':(fingers,0,fingers*.17),
            'jaw_r':(-jaw,0,0),'jaw_l':(-jaw,0,0),
            'hair':(-chest[0]*.25,-chest[1]*.25,-chest[2]*.30),
            'sprout':(-head[0]*.50,-head[1]*.22,-chest[2]*.45),
            'root_pos':xyz}


REST=P()
# Choreography table is deliberately authored per move: planted lateral sweep,
# alternating two cuts, low lunge, two-handed closing grasp, overhead slam,
# rising blow, reverse-hand flick, aerial strike, three-way scatter, sustained
# stare, defensive recoil and alternating berserk combo. Contact ticks match
# the entity ability contract; later frames return every joint to its rest pose.
SWEEP_W=P((9,-31,-8),(0,-15,0),(-27,-45,63),(19,24,-25),
          (15,0,15),(25,0,-8),(-15,0,12),(19,0,-9),(22,0,0),(7,0,0),
          (0,-.7,.35),(-7,24,0),(-12,10),-14,8)
SWEEP_H=P((-18,44,14),(0,22,0),(81,42,-31),(39,-23,-42),
          (17,0,12),(38,0,8),(27,0,12),(-27,0,-9),(3,0,0),(33,0,0),
          (.5,-.4,-1.0),(5,-23,-4),(21,-15),22,28)
REVERSE_W=P((2,35,13),(0,13,0),(12,-9,25),(-30,47,-65),
            (35,0,0),(20,0,0),(13,0,9),(-12,0,-10),(9,0,0),(23,0,0),
            (0,-.35,.2),(-3,-20,0),(0,-15),-12,5)
REVERSE_H=P((-12,-43,-15),(0,-20,0),(42,20,44),(86,-41,29),
            (28,0,-8),(8,0,-14),(-23,0,9),(27,0,-10),(28,0,0),(4,0,0),
            (-.5,-.3,-.65),(4,21,3),(-15,24),24,27)
LUNGE_W=P((-25,9,0),(8,-8,0),(-44,-18,12),(36,20,-16),
          (48,0,0),(35,0,0),(-43,0,11),(35,0,-13),(48,0,0),(12,0,0),
          (0,-1.5,.6),(13,-6,0),(-22,-9),-20,5)
LUNGE_H=P((-29,-8,0),(-8,7,0),(100,0,-10),(77,0,14),
          (-5,0,0),(12,0,0),(47,0,8),(-31,0,-8),(7,0,0),(42,0,0),
          (0,-.2,-2.8),(11,4,0),(17,13),35,31)
GRASP_W=P((12,0,0),(6,0,0),(37,-18,44),(37,18,-44),
          (30,-21,0),(30,21,0),(-15,0,18),(-15,0,-18),(29,0,0),(29,0,0),
          (0,-.9,.2),(-9,0,0),(-25,-25),-32,22)
GRASP_H=P((-20,0,0),(-5,0,0),(87,27,-15),(87,-27,15),
          (45,29,-7),(45,-29,7),(19,0,14),(-13,0,-14),(8,0,0),(30,0,0),
          (0,-.4,-1.2),(8,0,0),(37,37),46,39)
GRASP_PULL=P((18,0,0),(8,0,0),(62,15,-9),(62,-15,9),
             (74,22,0),(74,-22,0),(-10,0,16),(-10,0,-16),(30,0,0),(30,0,0),
             (0,-1,.4),(-17,0,0),(51,51),58,46)
SLAM_W=P((22,0,0),(-3,0,0),(158,-15,16),(158,15,-16),
         (40,0,0),(40,0,0),(-12,0,12),(-12,0,-12),(18,0,0),(18,0,0),
         (0,.2,.35),(-20,0,0),(-27,-27),-25,10)
SLAM_H=P((-46,0,0),(11,0,0),(105,0,-3),(105,0,3),
         (-12,0,0),(-12,0,0),(34,0,19),(34,0,-19),(38,0,0),(38,0,0),
         (0,-2,-.9),(20,0,0),(26,26),38,47)
UPPER_W=P((-31,-26,13),(7,-16,0),(-34,-14,19),(46,4,-35),
          (70,0,0),(53,0,-10),(-26,0,12),(8,0,-12),(49,0,0),(29,0,0),
          (.35,-2,.2),(12,20,0),(40,-10),30,10)
UPPER_H=P((22,28,-9),(-4,14,0),(150,17,-6),(31,-16,-34),
          (30,0,0),(42,0,0),(18,0,12),(-16,0,-12),(8,0,0),(12,0,0),
          (0,.5,-.7),(-19,-10,0),(-28,-9),-30,35)
BACK_W=P((3,-20,-9),(0,-13,0),(72,-46,-35),(17,0,-37),
         (43,0,0),(43,0,0),(-7,0,10),(7,0,-10),(12,0,0),(17,0,0),
         (0,-.2,.15),(-5,12,0),(32,0),30,8)
BACK_H=P((-9,40,14),(0,19,0),(85,61,51),(44,-14,-28),
         (-9,0,0),(33,0,0),(21,0,10),(-19,0,-10),(6,0,0),(28,0,0),
         (.3,-.3,-.5),(3,-26,-4),(-39,4),-24,23)
LEAP_W=P((-31,0,0),(12,0,0),(-36,-12,33),(-36,12,-33),
         (50,0,0),(50,0,0),(-49,0,17),(-49,0,-17),(71,0,0),(71,0,0),
         (0,-2.1,.5),(16,0,0),(-20,-20),-20,13)
LEAP_A=P((17,0,0),(-3,0,0),(153,-19,23),(138,21,-28),
         (39,0,0),(58,0,0),(40,0,16),(-37,0,-17),(65,0,0),(78,0,0),
         (0,4.2,-1.2),(-14,0,0),(-30,-30),-35,29)
FAN_W=P((12,0,0),(0,0,0),(42,-44,-12),(42,44,12),
        (78,-13,0),(78,13,0),(-8,0,16),(-8,0,-16),(18,0,0),(18,0,0),
        (0,-.5,.4),(-7,0,0),(44,44),42,15)
FAN_H=P((-12,0,0),(0,0,0),(81,-30,65),(81,30,-65),
        (-8,0,0),(-8,0,0),(13,0,16),(-5,0,-16),(5,0,0),(20,0,0),
        (0,0,-.6),(3,0,0),(-29,-29),-39,35)
RAY_W=P((9,0,0),(0,0,0),(65,8,-15),(65,-8,15),
        (52,0,0),(52,0,0),(-7,0,11),(-7,0,-11),(15,0,0),(15,0,0),
        (0,-.45,.15),(-13,0,0),(12,12),20,15)
RAY_H=P((-16,0,0),(4,0,0),(103,0,-3),(103,0,3),
        (0,0,0),(0,0,0),(12,0,13),(-8,0,-13),(7,0,0),(21,0,0),
        (0,-.3,-.8),(12,0,0),(-14,-14),-15,56)
GUARD_W=P((-14,0,0),(9,0,0),(77,32,-14),(77,-32,14),
          (70,21,-8),(70,-21,8),(-22,0,18),(-22,0,-18),(40,0,0),(40,0,0),
          (0,-1.3,.3),(8,0,0),(32,32),45,5)
GUARD_H=P((14,0,0),(-6,0,0),(56,-35,69),(56,35,-69),
          (-5,0,12),(-5,0,-12),(18,0,20),(18,0,-20),(7,0,0),(7,0,0),
          (0,.25,-.2),(-11,0,0),(-35,-35),-46,38)

ATTACKS={
    'sweep':(34,[(0,REST),(7,SWEEP_W),(11,SWEEP_W),(14,SWEEP_H),(21,REVERSE_W),(34,REST)]),
    'double_cut':(40,[(0,REST),(7,SWEEP_W),(12,SWEEP_H),(19,REVERSE_W),(23,REVERSE_W),(26,REVERSE_H),(32,BACK_W),(40,REST)]),
    'lunge':(36,[(0,REST),(7,LUNGE_W),(10,LUNGE_W),(16,LUNGE_H),(22,GRASP_H),(29,GUARD_W),(36,REST)]),
    'grasp':(42,[(0,REST),(7,GRASP_W),(12,GRASP_H),(18,GRASP_PULL),(23,GRASP_PULL),(26,SLAM_H),(33,GUARD_W),(42,REST)]),
    'slam':(40,[(0,REST),(9,SLAM_W),(16,SLAM_W),(20,SLAM_H),(25,SLAM_H),(33,GUARD_W),(40,REST)]),
    'uppercut':(32,[(0,REST),(8,UPPER_W),(11,UPPER_W),(14,UPPER_H),(20,SLAM_W),(26,GUARD_W),(32,REST)]),
    'backhand':(30,[(0,REST),(6,BACK_W),(9,BACK_W),(12,BACK_H),(18,REVERSE_W),(24,GUARD_W),(30,REST)]),
    'leap_strike':(44,[(0,REST),(8,LEAP_W),(12,LEAP_A),(19,SLAM_W),(24,SLAM_H),(30,SLAM_H),(37,GUARD_W),(44,REST)]),
    'shard_fan':(36,[(0,REST),(8,FAN_W),(13,FAN_W),(16,FAN_H),(19,FAN_W),(22,FAN_H),(29,GUARD_W),(36,REST)]),
    'eye_ray':(52,[(0,REST),(10,RAY_W),(20,RAY_W),(24,RAY_H),(27,RAY_W),(28,RAY_H),(31,RAY_W),(32,RAY_H),(39,GRASP_W),(46,GUARD_W),(52,REST)]),
    'guard_pulse':(44,[(0,REST),(9,GUARD_W),(18,GUARD_W),(22,GUARD_H),(28,GUARD_H),(36,GRASP_W),(44,REST)]),
    'frenzy':(60,[(0,REST),(7,SWEEP_W),(12,SWEEP_H),(21,REVERSE_W),(28,REVERSE_H),(37,SLAM_W),(44,SLAM_H),(50,SLAM_H),(55,GUARD_W),(60,REST)]),
}


def animate(m):
    def authored(name,ticks,stages):
        tracks={}
        # The poses are character-adapted: Lana's arms/puppet jaws dominate,
        # Edward leads with the yawning mouth, Oliver flicks elongated fingers.
        arm_gain=1.07 if m.name=='host_lana' else .92 if m.name=='host_edward' else 1
        for bone in m.groups:
            if bone=='root':
                tracks[bone]={'position':[(t/20,*p['root_pos']) for t,p in stages]}
                continue
            if bone not in REST:continue
            keys=[]
            for tick,p in stages:
                value=p[bone]
                if bone.startswith('arm_'):
                    value=tuple(v*arm_gain for v in value)
                if bone in ('hair','sprout') or bone.startswith('digits_'):
                    tick=min(ticks,tick+1.6) if tick and tick!=ticks else tick
                keys.append((tick/20,*value))
            tracks[bone]={'rotation':keys}
        m.anim(name,ticks/20,tracks)
    for name,(ticks,stages) in ATTACKS.items():
        authored(name,ticks,stages)
    idle={}
    for bone in m.groups:
        if bone=='root':
            idle[bone]={'position':[(0,0,0,0),(.95,0,.15,0),(1.9,0,0,0),(2.85,0,-.12,0),(3.8,0,0,0)]}
        elif bone in REST:
            amp=(1.8,1.1,1.5)
            if bone.startswith('arm_'):amp=(2.2,1.8,2.6 if bone.endswith('r') else -2.6)
            if bone.startswith('jaw_'):amp=(3.6,0,0)
            if bone.startswith('digits_'):amp=(5.5,0,1.2)
            if bone in ('hair','sprout'):amp=(2.5,1.8,2.8)
            idle[bone]={'rotation':[(0,0,0,0),(.95,*amp),(1.9,0,0,0),
                                    (2.85,*tuple(-v for v in amp)),(3.8,0,0,0)]}
    m.anim('idle',3.8,idle,loop=True)
    walk={}
    for bone in m.groups:
        if bone=='root':
            walk[bone]={'position':[(0,0,0,0),(.25,0,.45,0),(.5,0,0,0),(.75,0,.45,0),(1,0,0,0)]}
            continue
        if bone not in REST:continue
        s=1 if bone.endswith('r') else -1
        if bone.startswith('thigh_'):a=(25*s,0,3*s)
        elif bone.startswith('shin_'):a=(15*s,0,0)
        elif bone.startswith('arm_'):a=(-15*s,0,4*s)
        elif bone.startswith('fore_'):a=(9*s,0,0)
        elif bone.startswith('hand_'):a=(9*s,0,4*s)
        elif bone.startswith('digits_'):a=(12*s,0,0)
        elif bone.startswith('jaw_'):a=(-7*s,0,0)
        elif bone=='chest':a=(-3,5,2)
        elif bone=='pelvis':a=(0,-4,-2)
        elif bone in ('hair','sprout'):a=(3,-5,-3)
        elif bone=='head':a=(1,-3,-1)
        else:a=(2*s,0,0)
        walk[bone]={'rotation':[(0,*a),(.25,0,0,0),(.5,*tuple(-v for v in a)),(.75,0,0,0),(1,*a)]}
    m.anim('walk',1,walk,loop=True)
    death1=P((-17,12,11),(8,0,8),(41,-10,32),(23,9,-27),(45,0,0),
             (37,0,0),(-31,0,16),(-22,0,-7),(58,0,0),(45,0,0),
             (0,-3,.3),(12,-8,-11),(16,23),35,43)
    death2=P((-61,23,27),(9,7,23),(101,-15,63),(81,12,-44),
             (28,0,0),(20,0,0),(-63,0,29),(-51,0,-13),(88,0,0),(77,0,0),
             (1.5,-10,1.4),(37,-21,-21),(54,49),62,66)
    authored('death',40,[(0,REST),(7,death1),(20,death2),(40,death2)])


if __name__=='__main__':
    for build in (lana,edward,oliver):
        model=build()
        animate(model)
        model.save(OUT/(model.name+'.bbmodel'))
        print(model.name,len(model.cubes),'solids',len(model.anims),'animations')

