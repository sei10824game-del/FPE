"""Seven FPE Zombie AU figures, authored from the supplied character sheets.

Solid articulated geometry only. Combat choreography is mod-original.
"""
from pathlib import Path
import sys, math
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from zombie_au_common import *

def poly(m,n,b,pts,z,c,d=.55): solid_poly(m,n,b,pts,z,d,c,step=.32)
def box(m,n,b,a,e,c): m.cube(n,b,a,e,c,grain=.012)
def spikes(m,color=PAPER,length=1):
    # Individual overlapping hair locks give volume from front and rear.
    box(m,'hair_cap','hair',(-2.8,28.2,-1.5),(2.8,30.8,1.9),color)
    for s in (-1,1):
        for j in range(4):
            y=29.6-j*1.25
            poly(m,f'side_lock_{s}_{j}','hair_r' if s>0 else 'hair_l',[(s*1.7,y+1.6),(s*(3.1+length),y+.3),(s*2.8,y-.5),(s*4.0,y-.9),(s*1.8,y-1)],-.1,color,2.8)
    for j in range(5):
        x=-2.5+j*1.1
        poly(m,'fringe_'+str(j),'hair',[(x,30.5),(x+1.4,30.2),(x+.7,27.6),(x-.15,28.5)],-1.72,color,.55)

def eye(m,x,y=27.8,color=INK,r=.38):
    for j in range(5):
        w=r*math.sqrt(1-((j+.5)/2.5-1)**2)
        box(m,'eye','head',(x-w,y-r+j*2*r/5,-2.10),(x+w,y-r+(j+1)*2*r/5,-1.98),color)

def stitches(m,y=26.2):
    rib(m,'mouth_seam','head',(-1.35,y,-1.9),(1.35,y+.1,-1.9),.12,.12,INK)
    for x in (-1,-.5,0,.5,1): rib(m,'stitch','head',(x,y-.28,-1.96),(x+.12,y+.3,-1.96),.08,.1,INK)

def tie(m,color=GOLD):
    poly(m,'tie','chest',[(-.6,22.9),(.6,22.9),(.33,21.8),(.75,18.6),(0,18),(-.75,18.6),(-.33,21.8)],-1.35,color,.25)

def dagger(m):
    box(m,'knife_grip','weapon',(3.65,12.4,-.4),(4.35,15.1,.4),BLACK)
    box(m,'knife_guard','weapon',(3.1,12.3,-.5),(4.9,12.7,.5),GREY)
    poly(m,'knife_blade','weapon',[(3.65,12.3),(4.35,12.3),(4.35,7.5),(3.65,6.4)],-.1,PAPER,.28)
    rib(m,'knife_edge','weapon',(3.72,7, -.28),(3.72,12.2,-.28),.09,.08,WHITE)

def riley():
    m=Rig('survivor_riley',1.75,'claw'); limbs(m,DARK,INK,BLACK,PAPER,4)
    head(m); spikes(m,GREY,.15)
    eye(m,-1.05,color=INK,r=.52);eye(m,-1.05,color=PAPER,r=.30);eye(m,-1.05,color=INK,r=.13)
    eye(m,1.05,color=INK,r=.25); stitches(m)
    box(m,'damaged_eye_plate','head',(-1.75,27.0,-1.67),(-.35,28.8,-1.55),DARK)
    # Overlay the circular lens in front of its square mounting plate.
    for c,r in [(GREY,.65),(INK,.46),(MINT,.20)]:eye(m,-1.05,27.9,c,r)
    tie(m,PAPER)
    for side,s in [('r',1),('l',-1)]:
        for j in range(3):box(m,'leg_bandage','shin_'+side,(s*1.25-.78,4.2+j*.65,-.79),(s*1.25+.78,4.65+j*.65,.8),GREY)
    box(m,'belt','body',(-2.5,14.9,-1.2),(2.5,15.5,1.3),BLACK);dagger(m)
    return m.finish()

def bubble():
    m=Rig('survivor_bubble',1.8,'medic');limbs(m,PAPER,INK,BLACK,PAPER,2.5);head(m)
    # Puffy curls, rather than the angular locks worn by the other students.
    for j,(x,y) in enumerate([(-3.3,28),(-3.0,30),(-1.8,31.2),(0,31.5),(1.9,31.1),(3,29.6),(3.3,27.5)]):
        for k in range(5):
            t=(k+.5)/5;w=1.2*math.sqrt(1-(2*t-1)**2)
            box(m,'curl','hair',(x-w,y-1+k*.4,-1.0),(x+w,y-1+(k+1)*.4,1.7),PAPER)
    for s in (-1,1):
        for c,r in [(DARK,.82),(PAPER,.62),(MINT,.35)]:eye(m,s*.98,27.8,c,r)
    rib(m,'goggle_bridge','head',(-.3,27.8,-1.94),(.3,27.8,-1.94),.15,.18,DARK)
    box(m,'respirator','head',(-.85,25.5,-2.2),(.85,26.8,-1.6),DARK)
    for s in (-1,1):box(m,'filter','head',(s*1.1-.4,25.7,-2.3),(s*1.1+.4,26.6,-1.9),GREY)
    poly(m,'skirt','coat',[(-2.3,16),(2.3,16),(3.5,10.2),(-3.5,10.2)],0,INK,2.4)
    poly(m,'apron','coat',[(-1.7,20),(1.7,20),(1.9,11),(-1.9,11)],-1.42,PAPER,.25)
    box(m,'apron_cross_h','coat',(-.9,13.4,-1.63),(.9,14,-1.48),MINT);box(m,'apron_cross_v','coat',(-.3,12.8,-1.65),(.3,14.6,-1.5),MINT)
    for s,side in [(1,'r'),(-1,'l')]:
        for j in range(6):box(m,'bandage','shin_'+side,(s*1.25-.8,3+j*.65,-.82),(s*1.25+.8,3.5+j*.65,.83),GREY if j%2 else PAPER)
    box(m,'medkit','weapon',(3.2,10.2,-.8),(6.3,13.4,1),GREY)
    box(m,'kit_cross_h','weapon',(3.6,11.5,-.92),(5.9,12.05,-.79),PAPER);box(m,'kit_cross_v','weapon',(4.5,10.7,-.94),(5,12.8,-.8),PAPER)
    for s in (-1,1):poly(m,'hair_bow','hair',[(s*1.5,30.5),(s*3.1,31.8),(s*3.4,29.7)],-.4,MINT,.6)
    return m.finish()

def lizzy():
    m=Rig('survivor_lizzy',1.9,'gun');m.gun_axis=(0,0,-1)
    limbs(m,INK,INK,BLACK,PAPER,4.4);head(m)
    box(m,'long_hair','hair',(-3,19.5,.4),(3.1,30,2),INK)
    spikes(m,INK,.25)
    poly(m,'beret','hair',[(-3.7,30),(-2.7,32),(1.8,32.2),(3.5,30.1)],0,MINT,3.6)
    poly(m,'hat_star','hair',[(-.6,31),(0,32),(.6,31),(.1,31.2)],-1.95,GOLD,.2)
    eye(m,-1,color=PAPER);box(m,'eyepatch','head',(.35,27.2,-1.95),(1.75,28.6,-1.65),DARK)
    rib(m,'eyepatch_strap','head',(-2.1,28.9,-1.85),(2.2,27,-1.85),.22,.16,GREY)
    stitches(m,26.1)
    for s,b in [(1,'coat_r'),(-1,'coat_l')]:poly(m,'coat_panel',b,[(s*.7,23),(s*2.7,22.2),(s*3.4,8),(s*.8,10)],.3,PAPER,2.7)
    poly(m,'dress','body',[(-2,18),(2,18),(2.8,12),(-2.8,12)],0,INK,2.4);tie(m,GOLD)
    for side,s in [('r',1),('l',-1)]:
        for j in range(3):box(m,'boot_stripe','foot_'+side,(s*1.25-.94,1.2+j*.85,-1.56),(s*1.25+.94,1.5+j*.85,-1.42),GREY)
    box(m,'pistol_grip','weapon',(3.7,13,-.4),(4.4,15,.5),DARK)
    box(m,'pistol_receiver','weapon',(3.5,14.9,-2.9),(4.6,16,.7),GREY)
    box(m,'pistol_muzzle','weapon',(3.7,15.1,-3.4),(4.4,15.8,-2.8),BLACK)
    return m.finish()

def kevin():
    m=Rig('survivor_kevin',1.9,'shield');limbs(m,PAPER,PAPER,INK,PAPER,3.7);head(m);spikes(m,INK,.1)
    for s in (-1,1):
        poly(m,'tall_horn','hair',[(s*1.3,29.8),(s*2,34),(s*2.5,31),(s*2.2,29.8)],.6,INK,1)
        box(m,'horn_cap','hair',(s*2-.45,32.4,-.05),(s*2+.45,33.1,1.15),PAPER)
        # Square glasses retain his recognisable academic face.
        x=s*1.05
        for a,b in [((x-.78,27,-1.92),(x+.78,27.18,-1.7)),((x-.78,28.4,-1.92),(x+.78,28.58,-1.7)),((x-.78,27,-1.92),(x-.6,28.58,-1.7)),((x+.6,27,-1.92),(x+.78,28.58,-1.7))]:box(m,'glasses','head',a,b,INK)
        eye(m,x,27.7,INK,.22)
    rib(m,'glasses_bridge','head',(-.3,27.8,-1.92),(.3,27.8,-1.92),.18,.15,INK);stitches(m,26.2);tie(m,INK)
    for s,b in [(1,'coat_r'),(-1,'coat_l')]:poly(m,'lab_coat',b,[(s*.65,23),(s*2.6,22.3),(s*2.9,11),(s*.7,11)],.1,PAPER,2.5)
    box(m,'book','weapon',(3,12,-1),(6,16.5,.8),MINT);box(m,'book_pages','weapon',(3.25,12.2,-1.1),(5.75,16.2,-.95),PAPER)
    box(m,'book_spine','weapon',(2.9,12,-1.15),(3.4,16.5,1),DARK)
    return m.finish()

def oliver(zombie=False):
    name='zombie_oliver' if zombie else 'survivor_oliver';m=Rig(name,2.2 if zombie else 2.1,'monster' if zombie else 'claw')
    limbs(m,INK,PAPER,BLACK,PAPER,5);head(m);spikes(m,PAPER,.8)
    for s in (-1,1):poly(m,'horn','hair',[(s*1.25,30.1),(s*2,33),(s*2.65,30)],.6,BLACK,1.2)
    for s in (-1,1):rib(m,'sprout','hair',(s*.15,30.6,.4),(s*.7,34.3,.4),.22,.3,PAPER)
    if zombie:
        for s in (-1,1):poly(m,'white_collar','chest',[(s*.15,23.5),(s*1.5,23.2),(s*.65,21.8)],-1.3,PAPER,.25)
        for s in (-1,1):
            eye(m,s*1.05,27.8,INK,.9);eye(m,s*1.05,27.8,GREEN,.68)
            rib(m,'eye_drip','head',(s*1.05,27.2,-1.93),(s*1.3,25.9,-1.93),.27,.16,GREEN)
        stitches(m,25.8)
        # The infected Oliver wears shorts with exposed/bandaged shins.
        for e in m.cubes:
            if e['name'].startswith('trouser_'):
                e['from'][1]=12.5*m.unit
        for side,sgn in [('r',1),('l',-1)]:
            box(m,'exposed_thigh','leg_'+side,(sgn*1.25-.74,7.3,-.7),(sgn*1.25+.74,12.7,.75),PAPER)
            for j in range(3):box(m,'shin_wrap','shin_'+side,(sgn*1.25-.77,5.5+j*.8,-.82),(sgn*1.25+.77,5.9+j*.8,.81),GREY)
        for side,s in [('r',1),('l',-1)]:
            box(m,'mutant_palm','hand_'+side,(s*4-1,12.7,-.9),(s*4+1,15,.9),GREEN)
            for j in range(3):rib(m,'infected_finger','hand_'+side,(s*(3.35+j*.65),13.3,-.2),(s*(3.2+j*.85),10.6,-.5),.35,.45,GREEN)
    else:
        box(m,'face_bandage','head',(-2.3,25.8,-1.9),(2.3,27.5,-1.65),BLACK)
        eye(m,1.05,28.0,INK,.34)
        for s in (-1,1):
            poly(m,'green_bow','chest',[(s*.2,23),(s*1.5,23.7),(s*1.3,21.8)],-1.5,GREEN,.3)
            box(m,'boot_green_stripe','foot_r' if s>0 else 'foot_l',(s*1.25-.94,3.6,-1.56),(s*1.25+.94,4,-1.4),GREEN)
        dagger(m)
        # Reference has long swept hair behind the shoulder, not just a short crown.
        for x,bone in [(1.9,'hair_l'),(2.7,'hair_l')]:
            poly(m,'long_swept_lock',bone,[(x,29),(x+1.3,26),(x+1.2,18),(x+.4,15),(x-.3,21)],1.5,PAPER,1.4)
        # Belt loops and glove cuffs make the trousers/hand joins readable in 3D.
        for side,sgn in [('r',1),('l',-1)]:
            box(m,'glove_cuff','hand_'+side,(sgn*4-.77,14.4,-.85),(sgn*4+.77,15.3,.85),BLACK)
        for s,side in [(1,'r'),(-1,'l')]:
            box(m,'cargo_pocket','leg_'+side,(s*1.25-.7,9.6,-.99),(s*1.25+.7,12,-.77),PAPER)
            box(m,'pocket_flap','leg_'+side,(s*1.25-.74,11.6,-1.07),(s*1.25+.74,12.05,-.94),GREY)
    # Diamond insignia uses four solid strips, leaving a dark centre.
    for a,b in [((0,20.8),(1,19.2)),((1,19.2),(0,17.6)),((0,17.6),(-1,19.2)),((-1,19.2),(0,20.8))]:rib(m,'shirt_diamond','chest',(*a,-1.35),(*b,-1.35),.14,.12,GREEN if not zombie else GREY)
    box(m,'shorts_hem','body',(-2.2,12.6,-.9),(2.2,13.1,1),GREY)
    return m.finish()

def zip_zombie():
    m=Rig('zombie_zip',2.5,'monster');limbs(m,PAPER,INK,BLACK,GREY,4.6);head(m,GREY)
    spikes(m,PAPER,.65)
    # Half-black hair and her written equation identify Zip independently of wings.
    poly(m,'black_half_fringe','hair',[(-3.2,30.8),(0,31.1),(-.4,27),(-1.9,25.9),(-3.8,26.6)],-1.95,INK,.65)
    box(m,'equation_plate','hair',(.2,29.4,-2.1),(3.2,30.7,-1.9),PAPER)
    # Authored tiny 2+2=8 strokes, no image texture.
    for ox in (.45,1.65):
        for a,b in [((0,.9),(.45,.9)),((.45,.9),(.45,.5)),((.45,.5),(0,.1)),((0,.1),(.5,.1))]:rib(m,'equation_2','hair',(ox+a[0],29.6+a[1],-2.23),(ox+b[0],29.6+b[1],-2.23),.07,.05,DARK)
    for a,b in [((1.1,30),(1.5,30)),((1.3,29.8),(1.3,30.2)),((2.3,29.9),(2.6,29.9)),((2.3,30.2),(2.6,30.2))]:rib(m,'equation_sign','hair',(*a,-2.23),(*b,-2.23),.07,.05,DARK)
    box(m,'equation_8','hair',(2.8,29.65,-2.25),(3.05,30.5,-2.19),DARK)
    eye(m,.95,27.8,INK,.28)
    poly(m,'monster_maw','head',[(-2.3,27.1),(2.3,27.1),(2.6,25.1),(-2.7,24.8)],-1.9,INK,.28)
    for j in range(9):
        x=-2.3+j*.52
        poly(m,'upper_tooth','head',[(x,27.1),(x+.4,27.1),(x+.2,26.1)],-2.1,PAPER,.22)
        poly(m,'lower_tooth','head',[(x,25),(x+.4,25),(x+.22,25.9)],-2.1,PAPER,.22)
    for s,b in [(1,'coat_r'),(-1,'coat_l')]:poly(m,'torn_tunic',b,[(s*.3,23),(s*2.8,22),(s*4,12),(s*2.9,13),(s*2.7,10.3),(s*1,11)],0,PAPER,2.5)
    # Ragged black bat membranes attach to articulated wing bones.
    for s,b in [(1,'wing_r'),(-1,'wing_l')]:
        poly(m,'infected_wing',b,[(s*2.1,23),(s*6.8,23.5),(s*6.4,16),(s*8.0,1),(s*5.3,2.8),(s*4.8,.7),(s*3.5,7),(s*2.2,14)],1.6,INK,.6)
        for ex,ey in [(6.8,23.5),(6.4,16),(8,1),(4.8,.7)]:rib(m,'wing_bone',b,(s*2.2,22,1.7),(s*ex,ey,1.7),.22,.35,DARK)
    poly(m,'long_tail','tail',[(0,15),(2,11),(4,6),(6,3),(9,5),(7,1),(4,1),(1,7),(-1,12)],1.3,INK,.7)
    for side,sgn in [('r',1),('l',-1)]:
        for j in range(3):
            rib(m,'elongated_claw','hand_'+side,(sgn*(3.4+j*.6),13.7,-.3),(sgn*(3+j*.95),9.6,-.5),.3,.4,GREY if sgn<0 else INK)
    # Spiral antenna above the left half.
    pts=[(-1,30),(-1.3,33),(-3.5,33.5),(-3.8,31.8),(-2.3,31.5),(-2.2,32.4),(-3,32.4)]
    for a,b in zip(pts,pts[1:]):rib(m,'antenna','hair',(*a,.6),(*b,.6),.22,.3,INK)
    return m.finish()

if __name__=='__main__':
    for fn in (riley,bubble,lizzy,kevin,oliver,lambda:oliver(True),zip_zombie):
        m=fn(); print(m.name,len(m.cubes),len(m.anims))
