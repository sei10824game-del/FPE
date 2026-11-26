"""Seven Zombie AU infected, authored from the user's character sheet.

Solid articulated geometry, no screenshot planes. Mint paper, ink silhouettes and
acid green infection marks distinguish this AU from the Paperblight hosts.
"""
from pathlib import Path
import sys, math
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from zombie_au_common import Rig,rib,solid_poly,head,limbs,INK,BLACK,PAPER,WHITE,GREY,MINT,DARK,GREEN,BLOOD

SIDES=(('r',1),('l',-1))

def poly(m,n,b,p,z=0,d=.8,c=INK):
    solid_poly(m,n,b,p,z,d,c,step=.4)

def eye(m,n,x,y,w=.7,h=1,c=GREEN,z=-1.8):
    m.cube(n,'head',(x-w/2,y-h/2,z),(x+w/2,y+h/2,z+.14),c,grain=0)
    m.cube(n+'_pupil','head',(x-.10,y-h*.36,z-.025),(x+.10,y+h*.36,z+.02),BLACK,grain=0)

def pivot(m,bone,point):
    # Custom monsters do not share a human elbow/knee position. Bone pivots must
    # meet the actual authored segments or rotations visibly pull them apart.
    m.groups[bone]['origin']=[v*m.unit for v in point]

def oval(m,name,bone,x,y,w,h,z,color,depth=.15):
    for j in range(14):
        t=(j+.5)/14
        half=w*.5*math.sqrt(max(0,1-(t*2-1)**2))
        m.cube(name+'_'+str(j),bone,(x-half,y-h*.5+j*h/14,z),
               (x+half,y-h*.5+(j+1)*h/14+.005,z+depth),color,grain=0)

def spikes(m,color=PAPER,wide=4):
    for s in (-1,1):
        for j in range(4):
            y=25+j*1.8
            poly(m,f'hair_{s}_{j}','hair',[(s*.7,y+1.8),(s*2.5,y+2.5),(s*(wide+.5*(j%2)),y+.4),(s*1.4,y-.3)],.4,2.7,color)
    poly(m,'forelock','hair',[(-2.7,29.4),(-1,32.3),(0,30.9),(2.8,32),(1.8,28),(0,29.1),(-1,27)],-1.65,.8,color)

def maw(m,y=26,w=2.5):
    m.cube('open_maw','head',(-w/2,y-.65,-1.83),(w/2,y+.6,-1.60),DARK,grain=0)
    for j in range(6):
        x=-w/2+(j+.5)*w/6
        poly(m,'upper_fang_'+str(j),'head',[(x-.17,y+.6),(x+.17,y+.6),(x,y+.10)],-1.92,.15,GREEN)
        poly(m,'lower_fang_'+str(j),'head',[(x-.17,y-.65),(x+.17,y-.65),(x,y-.17)],-1.93,.15,GREEN)

def claws(m,side,s,x,y,color=INK):
    for j in range(3):
        a=(x+s*(j-1)*.6,y,-.25)
        rib(m,'claw_'+side+str(j),'hand_'+side,a,(a[0]+s*.5,y-2-j*.25,-.8),.25,.5,color)

def edward():
    m=Rig('zombie_edward',2.25,'monster');head(m);spikes(m,PAPER,4.2)
    m.cube('ragged_jacket','chest',(-2.6,16,-1),(2.6,24,1),GREY)
    for s in (-1,1):
        poly(m,'jacket_flap_'+str(s),'coat',[(s*.2,23),(s*2.8,23),(s*3.8,13),(s*.4,16)],-.9,.35,PAPER)
        poly(m,'collar_'+str(s),'chest',[(0,23),(s*2.4,24),(s*1.3,21)],-1.4,.3,WHITE)
        rib(m,'horn_'+str(s),'head',(s*.8,30,.2),(s*1.2,33,.3),.42,.7,INK)
    for side,sign in SIDES:
        oval(m,'eye_outline_'+side,'head',sign*1.08,28.15,1.8,2.0,-2.03,INK)
        oval(m,'white_eye_'+side,'head',sign*1.08,28.15,1.48,1.68,-2.10,WHITE)
        oval(m,'eye_pupil_'+side,'head',sign*1.05,28.0,.40,.85,-2.18,BLACK)
    maw(m,26.3,3.3)
    m.cube('dark_tie','chest',(-.35,18,-1.2),(.35,22,-1.05),INK)
    for i in range(3):m.cube('shirt_button_'+str(i),'chest',(.55,20+i*.8,-1.15),(.75,20.2+i*.8,-1.03),WHITE)
    for side,s in SIDES:
        rib(m,'upper_arm_'+side,'arm_'+side,(s*2.6,23,0),(s*5,17,0),1.2,1.4,PAPER)
        rib(m,'long_forearm_'+side,'fore_'+side,(s*5,17,0),(s*7,7,0),.9,1,INK)
        poly(m,'hook_hand_'+side,'hand_'+side,[(s*6,8),(s*8,8),(s*8.4,3),(s*6.4,5)],0,.9,BLACK)
        rib(m,'crawler_thigh_'+side,'leg_'+side,(s*1.2,16,0),(s*3.8,8,1),1.15,1.2,INK)
        rib(m,'crawler_shin_'+side,'shin_'+side,(s*3.8,8,1),(s*2.2,1,-.3),.7,.9,BLACK)
        poly(m,'point_foot_'+side,'foot_'+side,[(s*2.2,2),(s*4,0),(s*.5,0)],-.5,1.4,INK)
    for side,sgn in SIDES:
        for bone,point in [('arm',(sgn*2.6,23,0)),('fore',(sgn*5,17,0)),('hand',(sgn*7,7,0)),
                           ('leg',(sgn*1.2,16,0)),('shin',(sgn*3.8,8,1)),('foot',(sgn*2.2,1,-.3))]:
            pivot(m,bone+'_'+side,point)
    return m.finish()

def robby():
    m=Rig('zombie_robby',2.65,'monster');head(m,INK,width=4.1,height=5)
    spikes(m,BLACK,3.9);eye(m,'single_infected_eye',-.75,27.5,.75,1.5,z=-1.85)
    poly(m,'face_slash','head',[(-.3,26.2),(1.8,27),(1.4,25.4)],-1.85,.15,MINT)
    m.cube('narrow_torso','chest',(-1.1,14,-.65),(1.1,24,.65),BLACK)
    poly(m,'neck_kerchief','chest',[(-1.8,24),(1.8,24),(0,20.5)],-.9,.4,0x8C6A43)
    for side,s in SIDES:
        rib(m,'stick_arm_'+side,'arm_'+side,(s*1.1,23,0),(s*3.4,17,0),.55,.7,INK)
        rib(m,'long_needle_fore_'+side,'fore_'+side,(s*3.4,17,0),(s*4.2,6,-.1),.40,.6,BLACK)
        claws(m,side,s,s*4.2,6)
        rib(m,'needle_thigh_'+side,'leg_'+side,(s*.6,15,0),(s*1.8,7,0),.65,.7,INK)
        rib(m,'needle_shin_'+side,'shin_'+side,(s*1.8,7,0),(s*2.2,.5,0),.40,.5,BLACK)
        poly(m,'needle_shoe_'+side,'foot_'+side,[(s*2,1),(s*4,0),(s*1.3,0)],-.25,1,INK)
    rib(m,'fork_shaft','weapon',(4.2,6,-.2),(6.4,32,-.2),.38,.5,MINT)
    for j in range(3):rib(m,'fork_tine_'+str(j),'weapon',(6.4,30,-.2),(5.3+j*1.1,34,-.2),.24,.35,GREEN)
    for side,sgn in SIDES:
        for bone,point in [('arm',(sgn*1.1,23,0)),('fore',(sgn*3.4,17,0)),('hand',(sgn*4.2,6,-.1)),
                           ('leg',(sgn*.6,15,0)),('shin',(sgn*1.8,7,0)),('foot',(sgn*2.2,.5,0))]:
            pivot(m,bone+'_'+side,point)
    pivot(m,'weapon',(4.2,6,-.2))
    return m.finish()

def skell():
    m=Rig('zombie_skell',3.6,'monster')
    poly(m,'hood','head',[(-3,23),(-4,27),(-2.4,31),(-1.5,34),(1,35),(2.8,32),(4,26),(2.7,23)],.3,3.6,BLACK)
    poly(m,'hood_opening','head',[(-2.4,29),(0,32),(2.4,29),(1.4,25),(-1.7,25)],-1.62,.3,INK)
    eye(m,'face_eye',.5,28.2,.9,1.7,z=-1.85)
    poly(m,'hood_wrap','head',[(-3,31),(0,33.3),(2.8,31.7),(2.9,32.4),(-.2,34),(-2.3,32.5)],-1.7,.25,DARK)
    poly(m,'tapered_trunk','chest',[(-3,25),(3,25),(2,14),(.8,8),(0,12),(-1.6,8),(-3,16)],.2,2.5,BLACK)
    for side,s in SIDES:
        # Two narrow lobes joined below the shoulder leave the long open cutout
        # visible in the supplied sheet. The negative space is real, not white paint.
        pts=[(s*2.3,26),(s*4.9,31.6),(s*5.8,30),(s*5.3,23),(s*5.5,17),
             (s*6.8,13),(s*7.8,17),(s*7.2,24),(s*8.3,21),(s*10.2,15),
             (s*11,8),(s*9.8,7.5),(s*8.4,9),(s*6.2,8.7),(s*4.8,10),(s*3.4,13)]
        poly(m,'open_notched_membrane_'+side,'wing_'+side,pts,1.1,.8,BLACK)
        rib(m,'outer_wing_bone_'+side,'wing_'+side,(s*7.5,22,1),(s*10.6,8,1),.23,.5,DARK)
        rib(m,'inner_wing_bone_'+side,'wing_'+side,(s*3.1,25,1),(s*5.1,11,1),.23,.5,DARK)
        # Acid eye symbols are real thin solids on the wing's front.
        cx=s*9;cy=13.5
        poly(m,'wing_green_eye_'+side,'wing_'+side,[(cx-s*1.2,cy),(cx,cy+2.3),(cx+s*1.2,cy),(cx,cy-2.3)],.58,.12,GREEN)
        poly(m,'wing_eye_pupil_'+side,'wing_'+side,[(cx-s*.5,cy),(cx,cy+1.35),(cx+s*.5,cy),(cx,cy-1.35)],.47,.12,BLACK)
        rib(m,'hanging_claw_'+side,'arm_'+side,(s*2.8,23,-.5),(s*3.8,12,-.6),.8,1,BLACK)
        claws(m,side,s,s*3.8,12)
        poly(m,'hanging_leg_'+side,'leg_'+side,[(s*.4,14),(s*2,14),(s*2.8,1),(s*.8,3)],.2,1.2,BLACK)
    poly(m,'chest_eye','chest',[(-1.2,20),(0,22.5),(1.2,20),(0,17.5)],-1.2,.2,GREEN)
    rib(m,'chest_pupil','chest',(0,18.5,-1.4),(0,21.5,-1.4),.2,.15,BLACK)
    for side,sgn in SIDES:
        pivot(m,'arm_'+side,(sgn*2.8,23,-.5))
        pivot(m,'fore_'+side,(sgn*3.8,12,-.6))
        pivot(m,'hand_'+side,(sgn*3.8,12,-.6))
    return m.finish()

def lana():
    m=Rig('zombie_lana',2.15,'monster');limbs(m,INK,PAPER,INK,PAPER);head(m,GREY);spikes(m,GREY,3.5)
    poly(m,'infected_face','head',[(-2.3,29),(0,30),(2.1,28),(.8,26),(-1.8,26)],-1.68,.2,GREEN)
    eye(m,'dead_eye',.9,28,.75,1.2,INK,z=-1.94);maw(m,26.2,2)
    rib(m,'hanging_tongue','head',(-.3,25.9,-1.98),(-1.1,22.8,-2.2),.38,.32,GREEN)
    for side,s in SIDES:
        m.cube('sock_'+side,'shin_'+side,(s*1.25-.76,4,-.8),(s*1.25+.76,7,.82),GREY)
        m.cube('puppet_hand_'+side,'hand_'+side,(s*4-1,12,-1.1),(s*4+1,15.6,1.1),DARK)
        for j in range(2):m.cube('puppet_eye_'+side+str(j),'hand_'+side,(s*4-.85+j*1.15,15.5,-1.2),(s*4-.2+j*1.15,16.3,-.6),GREEN)
        poly(m,'puppet_jaw_'+side,'hand_'+side,[(s*4-1,13),(s*4+1,13),(s*4+.7,11.4),(s*4-.6,11.6)],-1.2,.4,GREEN)
        rib(m,'puppet_tongue_'+side,'hand_'+side,(s*4,12,-1.6),(s*5,10,-1.6),.25,.25,GREEN)
    for j in range(5):
        import math
        a=j*math.tau/5
        m.cube('hair_flower_'+str(j),'hair',(-2.8+math.cos(a)*.65,29.6+math.sin(a)*.65,-1.9),(-2.2+math.cos(a)*.65,30.2+math.sin(a)*.65,-1.5),PAPER)
    return m.finish()

def abbie():
    m=Rig('zombie_abbie',3.25,'monster')
    # The zoomed character sheet shows WHITE wrapped sleeves, long black hair,
    # and a split/flared lower silhouette. Earlier low-resolution readings mistook
    # the sleeves for background and produced black needle arms; do not restore it.
    poly(m,'narrow_dark_face','head',[(-2.5,25.3),(-2.8,28.7),(-1.7,30.6),
         (1.8,30.7),(2.8,28.4),(2.3,24.6),(.7,23.6),(-1.3,24.0)],0,2.8,BLACK)
    for name,pts in [
        ('left_crown',[(-1.0,29.5),(-4.2,32.0),(-3.5,29.6),(-5.1,30.1),(-3.9,28.0),(-2.0,27.5)]),
        ('top_fringe',[(-2.2,30.0),(-1.7,32.7),(-.5,31.2),(.8,32.4),(2.7,31.1),(1.5,28.5)]),
        ('right_crown',[(1.2,30.4),(5.1,31.6),(3.7,29.0),(5.0,28.7),(3.4,27.2),(1.5,27.1)]),
        ('long_left_hair',[(-1.9,29.1),(-4.3,28.9),(-3.8,27.2),(-4.8,26.3),
             (-3.9,25.5),(-4.8,23.6),(-3.3,24.3),(-3.4,21.9),(-1.9,23.1),(-1.3,26.0)]),
        ('long_right_hair',[(1.7,29.0),(4.0,29.0),(3.7,27.2),(4.6,26.5),(3.8,25.5),
             (4.5,23.5),(3.1,24.1),(3.3,21.8),(1.6,23.3),(1.2,26.0)])]:
        poly(m,name,'hair',pts,.30,3.0,BLACK)
    oval(m,'sole_eye_outline','head',-.28,27.3,2.15,3.10,-1.65,0xB9CFAB)
    oval(m,'sole_eye_pupil','head',-.28,27.3,.62,2.47,-1.81,BLACK,.15)
    for side,sgn in SIDES:
        rib(m,'sprout_stem_'+side,'head',(sgn*.30,31.0,.2),(sgn*.72,33.0,.2),.24,.35,GREY)
        poly(m,'sprout_leaf_'+side,'head',[(sgn*.60,32.1),(sgn*.95,34.3),
             (sgn*1.4,33.8),(sgn*1.1,31.8)],.2,.32,PAPER)
    # Long wrapped white shirt with jagged hip panels; black tie visible down centre.
    poly(m,'long_ragged_uniform','chest',[(-2.0,24.1),(2.0,24.1),(1.85,19.0),
         (1.7,14.0),(.85,15.0),(.25,13.8),(-.45,15.2),(-1.1,14.0),(-1.85,16.0)],-.03,1.8,PAPER)
    for sgn in (-1,1):
        poly(m,'collar_'+str(sgn),'chest',[(0,23.8),(sgn*1.75,24.3),(sgn*.9,22.0)],-1.10,.22,WHITE)
    poly(m,'long_black_tie','chest',[(-.37,23.3),(.37,23.3),(.54,19.0),
         (0,16.7),(-.48,18.8)],-1.23,.18,INK)
    # The two black flared lobes leave the long white/background slit present in
    # the art. It is a real opening, not a flat white mark painted on a solid pillar.
    m.cube('dark_waist','body',(-1.5,13.4,-.6),(1.5,18.5,1.3),BLACK)
    # The opening closes above the hem in the drawing: one fused black base,
    # not two separate trouser legs.
    poly(m,'fused_bottom_bridge','body',[(-2.6,.05),(2.6,.05),(2.3,2.0),
         (1.1,2.3),(0,3.0),(-1.0,2.4),(-2.3,2.0)],.4,1.7,BLACK)
    for side,sgn in SIDES:
        poly(m,'flared_split_lower_'+side,'body',[(sgn*.55,15.6),(sgn*1.7,17.0),
             (sgn*3.2,11),(sgn*6.6,.15),(sgn*1.2,.05),(sgn*.65,1.8),
             (sgn*1.0,4.0),(sgn*.85,12.0)],.40,1.7,BLACK)
        elbow=(sgn*3.45,14.7,-.02);wrist=(sgn*6.0,4.3,-.05)
        rib(m,'white_wrapped_upper_'+side,'arm_'+side,(sgn*2.3,23.1,0),elbow,1.25,1.35,PAPER)
        poly(m,'broad_white_forearm_'+side,'fore_'+side,[(sgn*2.80,15.0),(sgn*4.10,15.0),
             (sgn*6.75,5.1),(sgn*5.25,4.0)],-.10,1.4,PAPER)
        # Broad cuffs and diagonal seams make the bandaged sleeve segmentation readable.
        poly(m,'grey_sleeve_cuff_'+side,'fore_'+side,[(sgn*4.85,8.2),(sgn*6.15,8.6),
             (sgn*6.75,5.1),(sgn*5.25,4.0)],-.87,.18,GREY)
        for j in range(4):
            t=.12+j*.19;x=sgn*(3.45+(6.0-3.45)*t);y=14.7+(4.3-14.7)*t
            rib(m,'forearm_wrap_seam_'+side+str(j),'fore_'+side,
                (x-sgn*.65,y-.13,-.91),(x+sgn*.65,y+.25,-.91),.10,.08,GREY)
        for j in range(3):
            yy=21.2-j*2.0;xx=sgn*(2.3+(23.1-yy)*.137)
            rib(m,'upper_wrap_seam_'+side+str(j),'arm_'+side,
                (xx-sgn*.6,yy-.1,-.76),(xx+sgn*.6,yy+.22,-.76),.09,.08,GREY)
        poly(m,'black_melted_hand_'+side,'hand_'+side,[(sgn*5.3,4.5),(sgn*6.7,5.0),
             (sgn*7.3,.15),(sgn*4.9,.15)],-.05,1.1,BLACK)
        pivot(m,'arm_'+side,(sgn*2.3,23.1,0));pivot(m,'fore_'+side,elbow);pivot(m,'hand_'+side,wrist)
    pivot(m,'head',(0,24.5,0))
    return m.finish()

def petunia():
    m=Rig('zombie_petunia',2.15,'monster');limbs(m,PAPER,PAPER,GREY,PAPER,boot_height=4);head(m,PAPER,width=5.2);spikes(m,PAPER,3.6)
    for side,s in SIDES:
        poly(m,'bunny_ear_'+side,'head',[(s*.6,30),(s*.8,36),(s*2.1,38),(s*2.4,34),(s*1.8,30)],.2,1.1,PAPER)
        poly(m,'ear_infection_'+side,'head',[(s*1.1,31),(s*1.25,35.6),(s*1.85,36.7),(s*1.9,33.9)],-.4,.15,GREEN)
        eye(m,'green_eye_'+side,s*1.2,28,1.0,1.35,z=-1.85)
        rib(m,'cheek_tendril_'+side,'head',(s*1.3,26.7,-1.8),(s*2.7,24,-1.9),.45,.6,INK)
        rib(m,'cheek_hook_'+side,'head',(s*2.7,24,-1.9),(s*.7,24.9,-2),.35,.5,INK)
        poly(m,'bell_cuff_'+side,'shin_'+side,[(s*.4,7),(s*2.1,7),(s*3.2,.5),(s*.3,.5)],0,1.8,PAPER)
        claws(m,side,s,s*4,13,GREY)
    maw(m,26.1,2.3)
    poly(m,'neck_bow','chest',[(-1.8,23),(0,22),(1.8,23),(1.2,20),(0,21),(-1.2,20)],-1.3,.4,GREY)
    return m.finish()

def cubbie():
    m=Rig('zombie_cubbie',2.75,'monster');head(m,GREY,width=4.5)
    poly(m,'cat_hood','hair',[(-3.1,25),(-3,31),(-2.5,34),(0,31),(2.5,34),(3.1,30),(2.9,25)],.35,3.4,0x203C45)
    poly(m,'face_opening','head',[(-1.9,29),(1.9,29),(2,26),(.2,25),(-1.8,26)],-1.55,.25,GREY)
    oval(m,'large_round_green_eye','head',-1.75,29.0,2.15,2.65,-1.90,GREEN)
    oval(m,'round_eye_dark_pupil','head',-1.74,29.0,.65,1.65,-2.04,BLACK)
    m.cube('mask','head',(-2.2,25.5,-1.95),(2.2,27.1,-1.6),MINT)
    for j in range(3):rib(m,'mask_fold_'+str(j),'head',(-1.9,25.8+j*.45,-2),(1.9,25.8+j*.45,-2),.06,.04,DARK)
    poly(m,'long_dark_coat','coat',[(-2.3,24),(2.3,24),(3.2,3),(.5,4),(0,8),(-.5,4),(-3.2,3)],.3,2.2,0x203C45)
    m.cube('pale_coat_panel','chest',(-.6,15,-1),(1,23,-.85),PAPER)
    for side,s in SIDES:
        rib(m,'long_arm_'+side,'arm_'+side,(s*2.4,23,0),(s*3.7,13,0),.8,1.1,BLACK)
        rib(m,'reaching_forearm_'+side,'fore_'+side,(s*3.7,13,0),(s*4.9,3,0),.55,.8,INK)
        claws(m,side,s,s*4.9,3)
        poly(m,'flared_leg_'+side,'leg_'+side,[(s*.4,14),(s*1.7,14),(s*2.7,0),(s*.3,0)],0,1.7,INK)
    for j in range(3):rib(m,'green_shoulder_streak_'+str(j),'chest',(-2.8,22-j*.75,-.9),(-1.2,21-j*.75,-1),.25,.18,GREEN)
    for side,sgn in SIDES:
        pivot(m,'arm_'+side,(sgn*2.4,23,0));pivot(m,'fore_'+side,(sgn*3.7,13,0));pivot(m,'hand_'+side,(sgn*4.9,3,0))
    return m.finish()

if __name__=='__main__':
    for build in (edward,robby,skell,lana,abbie,petunia,cubbie):
        m=build();print(m.name,len(m.anims),'animations')
