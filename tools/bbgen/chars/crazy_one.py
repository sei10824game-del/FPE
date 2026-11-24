"""Crazie, saved id crazy_one. Original fan-model based on supplied Current Wiki image.
Orange/strawberry hair, split ahoge with blue tie, bandaged eyes and limbs,
white puff blouse, black overall bib and a blue star skirt. No supernatural powers.
All twelve knife/body moves are mod-original, not canon claims.
Rig coordinates: +Y up, ground zero, front -Z, right hand +X. 20 ticks = 1 sec.
Run python tools/bbgen/chars/crazy_one.py; no shared patcher required.
"""
import math, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from bbgen import Model

OUT = os.path.join(os.path.dirname(__file__), "../../../src/main/resources/assets/fpe/bbmodels/crazy_one.bbmodel")
m = Model("crazy_one", S=8, atlas=2048)
HAIR, SHADE, LIGHT = 0xDD896B, 0xAD5B54, 0xF0A078
SKIN, SCAR, BAND = 0xE6B8A0, 0xAF6460, 0xEAE0D1
WHITE, WH_D, DARK = 0xEEE9DE, 0xC8B8AE, 0x24243B
BLUE, BLUE_D, STAR = 0x345784, 0x263B65, 0xE4B878
ALL = ("north","south","east","west","up","down")

def flat(c): return lambda F: F.rect(0,0,F.w,F.h,c)
def faces(fn): return {f:fn for f in ALL}
def cube(name,bone,lo,hi,col,**kw): return m.cube(name,bone,lo,hi,col,grain=0,**kw)

def card(name,bone,points,z,col,yaw=0,depth=.35,stars=False):
    x0,x1=min(x for x,y in points),max(x for x,y in points)
    y0,y1=min(y for x,y in points),max(y for x,y in points)
    def clear(F):
        for y in range(F.h):
            for x in range(F.w):F.px(x,y,col,a=0)
    def painter(F,back=False):
        clear(F)
        pts=[((x-x0)/(x1-x0)*F.w,(y1-y)/(y1-y0)*F.h) for x,y in points]
        if back:pts=[(F.w-x,y) for x,y in pts]
        F.poly(pts,col)
        # Broad flat cel shadow, masked to the cutout.
        for y in range(F.h):
            for x in range(F.w):
                if F.cv.get(F.x+x,F.y+y)[3] and x<F.w*.14:F.px(x,y,BLUE_D if stars else SHADE if col==HAIR else col)
        if stars:
            for u,v,r in ((.28,.28,.12),(.73,.57,.13),(.28,.81,.11)):
                pts=[]
                for i in range(10):
                    a=-math.pi/2+i*math.pi/5; rad=r*min(F.w,F.h)*(1 if i%2==0 else .45)
                    pts.append((u*F.w+math.cos(a)*rad,v*F.h+math.sin(a)*rad))
                F.poly(pts,STAR)
    fs={f:clear for f in ALL};fs['north']=lambda F:painter(F);fs['south']=lambda F:painter(F,True)
    return cube(name,bone,(x0,y0,z-depth/2),(x1,y1,z+depth/2),col,origin=(0,0,0),rot=(0,yaw,0),faces=fs)

def bandages(F):
    F.rect(0,0,F.w,F.h,SKIN)
    for k in range(3):
        yy=(k+.4)*F.h/3
        F.line(0,yy,F.w,yy+F.h*.1,BAND,max(2,F.h*.13))
        F.line(F.w*.18,yy+F.h*.14,F.w*.35,yy+F.h*.2,SCAR,1)

def face(F):
    F.rect(0,0,F.w,F.h,SKIN)
    # Opaque eye wrap, including two oblique overlaps; no visible supernatural eyes.
    F.rect(0,F.h*.18,F.w,F.h*.42,BAND)
    F.line(0,F.h*.27,F.w,F.h*.43,WH_D,2)
    F.line(0,F.h*.48,F.w,F.h*.31,WHITE,2)
    # Current reference: broad, off-centre open laugh beneath the opaque eye wrap.
    # Keep a dark mouth cavity around the pale upper teeth rather than a straight neutral line.
    W,H=F.w,F.h
    F.poly([(W*.28,H*.68),(W*.85,H*.59),(W*.80,H*.80),
            (W*.62,H*.91),(W*.40,H*.87)],0x963F3D)
    F.poly([(W*.35,H*.69),(W*.79,H*.63),(W*.73,H*.72),
            (W*.47,H*.78)],BAND)
    F.poly([(W*.58,H*.85),(W*.77,H*.77),(W*.70,H*.85)],0xCD7567)
    F.line(W*.79,H*.60,W*.88,H*.56,SCAR,1)
    F.line(W*.20,H*.70,W*.27,H*.65,SCAR,1)

# Skeleton: named secondary-motion groups and articulated limbs.
m.group('root',(0,0,0));m.group('body',(0,13.5,0),parent='root')
m.group('chest',(0,17,0),parent='body');m.group('head',(0,23.2,0),parent='chest')
m.group('hair_back',(0,27,2.2),parent='head');m.group('hair_r',(2.6,27,0),parent='head');m.group('hair_l',(-2.6,27,0),parent='head')
m.group('bangs',(0,28,-2.5),parent='head');m.group('ahoge',(0,29,0),parent='head')
for s,k in ((1,'r'),(-1,'l')):
    m.group('arm_'+k,(s*3.2,22.2,0),parent='chest');m.group('fore_'+k,(s*3.65,18.8,0),parent='arm_'+k)
    m.group('hand_'+k,(s*3.8,15.2,0),parent='fore_'+k)
    m.group('leg_'+k,(s*1.2,13.5,0),parent='root');m.group('shin_'+k,(s*1.2,6.7,0),parent='leg_'+k)
    m.group('foot_'+k,(s*1.2,1,0),parent='shin_'+k)
    m.group('skirt_'+k,(s*1,15.3,0),parent='body')
m.group('knife',(3.8,14.8,-.2),parent='hand_r')
# Blue skirt under the black bib, with stars on all sides.
cube('skirt_core','body',(-2.6,7,-1.8),(2.6,16,1.8),BLUE,faces=faces(flat(BLUE)))
for side,k in ((1,'r'),(-1,'l')):
    pts=[(side*.0,16),(side*2.6,16),(side*4.5,6.7),(side*.0,6.3)]
    card('skirt_front_'+k,'skirt_'+k,pts,-2.05,BLUE,stars=True)
    card('skirt_back_'+k,'skirt_'+k,pts,2.05,BLUE,stars=True)
    card('skirt_side_'+k,'skirt_'+k,[(-1.8,16),(1.8,16),(2.7,6.6),(-2.7,6.6)],side*2.65,BLUE,yaw=90,stars=True)
# White blouse, overall bib, straps, collar.
cube('blouse','chest',(-2.65,16,-1.7),(2.65,22.6,1.7),WHITE,faces=faces(flat(WHITE)))
cube('bib','chest',(-2.15,16,-1.94),(2.15,20.8,-1.7),DARK)
cube('bib_back','chest',(-2.15,16,1.7),(2.15,20.8,1.94),DARK)
for s in (-1,1):
    cube('strap_front'+str(s),'chest',(s*1.55-.35,20.4,-1.98),(s*1.55+.35,22.7,-1.72),DARK)
    cube('strap_back'+str(s),'chest',(s*1.55-.35,20.4,1.72),(s*1.55+.35,22.7,1.98),DARK)
    cube('button'+str(s),'chest',(s*1.55-.16,20.5,-2.05),(s*1.55+.16,20.85,-1.96),STAR)
cube('neck','chest',(-.65,22.4,-.7),(.65,23.7,.7),SKIN)
card('collar','chest',[(-1.5,22.9),(0,22.2),(1.5,22.9),(.7,21.5),(0,21.9),(-.7,21.5)],-1.9,WHITE)
# Limbs: puff sleeves and visible bandage wraps.
for s,k in ((1,'r'),(-1,'l')):
    x=s*3.25
    cube('puff_'+k,'arm_'+k,(x-1.2,19.9,-1.15),(x+1.2,22.5,1.15),WHITE,faces=faces(flat(WHITE)))
    cube('cuff_'+k,'arm_'+k,(x-.85,19.5,-.85),(x+.85,20.2,.85),WH_D)
    cube('forearm_'+k,'fore_'+k,(s*3.65-.72,15.3,-.75),(s*3.65+.72,19.6,.75),SKIN,faces=faces(bandages))
    cube('hand_'+k,'hand_'+k,(s*3.8-.78,13.8,-.78),(s*3.8+.78,15.5,.78),SKIN)
    cube('thigh_'+k,'leg_'+k,(s*1.2-.8,6.5,-.8),(s*1.2+.8,13.6,.8),SKIN,faces=faces(bandages))
    cube('shin_'+k,'shin_'+k,(s*1.2-.65,3,-.7),(s*1.2+.65,6.8,.7),SKIN,faces=faces(bandages))
    cube('boot_'+k,'foot_'+k,(s*1.2-.72,.3,-1),(s*1.2+.72,3.4,.8),DARK)
    card('pointed_toe_'+k,'foot_'+k,[(3.0,.2),(-.8,.2),(-.75,1.35),(.6,1.4)],s*1.2,DARK,yaw=90)
# Head and large flowing strawberry-orange silhouette.
cube('face','head',(-2.45,23,-2.45),(2.45,28.4,2),SKIN,faces={'north':face,'south':flat(SKIN)})
cube('eye_wrap_sides','head',(-2.5,25.0,-2.48),(2.5,27.25,2.05),BAND,faces=faces(flat(BAND)))
# Face plane sits just in front of the wrap volume, preserving the overlap lines.
cube('face_front','head',(-2.45,23,-2.52),(2.45,28.4,-2.49),SKIN,faces={'north':face})
cube('hair_cap','head',(-2.7,27.7,-2.35),(2.7,29.4,2.4),HAIR,faces=faces(flat(HAIR)))
cube('rear_volume','hair_back',(-2.8,13.5,1.8),(2.8,28.8,3.3),SHADE,faces=faces(flat(SHADE)))
card('back_hair','hair_back',[(-2.5,29),(2.6,29),(4.1,26.5),(3.5,23),(5.9,19.4),(6.5,14),(5.1,10.5),(3.5,9),(1,8.4),(-1.5,9.1),(-4.1,8.3),(-5.2,10.5),(-4.5,13),(-6.2,13.5),(-5.2,16.8),(-3.5,20.5),(-3.9,25.8)],3.6,HAIR)
card('fringe','bangs',[(-3,28.8),(.6,29.3),(4.3,27.9),(2.4,27.3),(3.3,26.1),(.4,26.8),(-1.5,25.0),(-2.2,26.4),(-3.9,25.7),(-3,27)],-2.8,HAIR)
for s,k in ((1,'r'),(-1,'l')):
    card('side_lock_'+k,'hair_'+k,[(s*2.2,28.8),(s*3.3,27.5),(s*4.5,24.6),(s*3.1,25),(s*4.0,22.5),(s*2.5,23.8)],-.3,HAIR)
    card('side_hair_profile_'+k,'hair_back',[(-1,28.5),(2.6,28.9),(4.3,24),(3.5,20),(4.7,15.3),(3.8,10.1),(1.7,8.8),(.8,12.5),(1.5,19),(.3,24)],s*2.5,HAIR,yaw=90)
# Defining split ahoge tied with blue ribbon.
card('ahoge_left','ahoge',[(-.25,29.3),(-2.1,30),(-3.5,32.2),(-2.1,34.4),(-.6,32.6),(.15,30.2)],.0,LIGHT)
card('ahoge_right','ahoge',[(.0,29.5),(.4,32.1),(3.8,34.4),(3.1,31.8),(1.2,29.8)],.15,HAIR)
card('ahoge_depth','ahoge',[(-.6,29.4),(-.5,32),(1,34),(1.4,31),(.7,29.6)],0,HAIR,yaw=90)
cube('blue_hair_tie','ahoge',(-.65,29.0,-.6),(.65,30.1,.8),BLUE_D)
# Visible steel knife, never a wrench. Point down at rest.
cube('knife_grip','knife',(3.5,13.4,-.4),(4.1,15.7,.3),DARK)
cube('knife_guard','knife',(3.0,13.2,-.5),(4.6,13.6,.4),0x837D82)
card('knife_blade','knife',[(3.15,13.2),(4.35,13.2),(4.05,8.6),(3.25,9.5)],-.1,0xB9BDC7)

# Full-body pose authoring. Positive arm pitch brings hanging arms forward.
BONES=['body','chest','head','arm_r','fore_r','hand_r','arm_l','fore_l','leg_r','shin_r','foot_r','leg_l','shin_l','foot_l','knife']
REST={'arm_r':(8,0,8),'arm_l':(4,0,-8),'fore_r':(8,0,0),'fore_l':(8,0,0)}
def pose(t,**kw):return (t,kw)
def anim(name,duration,poses,loop=False):
    tracks={b:{'rotation':[]} for b in BONES}
    tracks['body']['position']=[]
    for t,p in poses:
        for b in BONES:tracks[b]['rotation'].append((t/20,*p.get(b,REST.get(b,(0,0,0)))))
        tracks['body']['position'].append((t/20,*p.get('position',(0,0,0))))
    # Lagged secondary motion on hair, ahoge and skirt, explicitly recovered at the end.
    for bone,scale,delay in [('hair_back',.45,2),('hair_r',.3,1),('hair_l',.3,1),('bangs',.18,1),('ahoge',.55,2),('skirt_r',.35,1),('skirt_l',.35,1)]:
        keys=[]
        for t,p in poses:
            bx,by,bz=p.get('body',(0,0,0));tt=min(duration,t+delay) if t else 0
            value=(-bx*scale,by*scale,-bz*scale)
            if t==duration:value=(0,0,0)
            if keys and keys[-1][0]==tt/20:keys[-1]=(tt/20,*value)
            else:keys.append((tt/20,*value))
        tracks[bone]={'rotation':keys}
    m.anim(name,duration/20,tracks,loop=loop)

anim('idle',80,[pose(0,body=(0,0,2),head=(0,-5,-4)),pose(20,body=(2,2,-1),head=(-3,4,2)),pose(40,body=(0,0,-2),head=(0,6,4)),pose(60,body=(2,-2,1),head=(-3,-4,-2)),pose(80,body=(0,0,2),head=(0,-5,-4))],True)
anim('walk',24,[pose(0,body=(-5,5,2),arm_r=(-20,0,12),arm_l=(28,0,-10),leg_r=(30,0,0),leg_l=(-28,0,0),shin_l=(-35,0,0)),pose(6,body=(-7,0,0),position=(0,.5,0),leg_r=(0,0,0),leg_l=(0,0,0),shin_l=(-55,0,0)),pose(12,body=(-5,-5,-2),arm_r=(28,0,10),arm_l=(-20,0,-12),leg_r=(-28,0,0),leg_l=(30,0,0),shin_r=(-35,0,0)),pose(18,body=(-7,0,0),position=(0,.5,0),leg_r=(0,0,0),leg_l=(0,0,0),shin_r=(-55,0,0)),pose(24,body=(-5,5,2),arm_r=(-20,0,12),arm_l=(28,0,-10),leg_r=(30,0,0),leg_l=(-28,0,0),shin_l=(-35,0,0))],True)

# Each timeline below includes anticipation, exact server contact, follow-through and recovery.
anim('frantic_flurry',40,[pose(0),pose(6,body=(8,25,-8),head=(6,-15,0),arm_r=(115,30,45),arm_l=(45,0,-30),leg_r=(15,0,5)),pose(10,body=(-24,-28,7),head=(12,12,-4),arm_r=(80,-50,-25),fore_r=(12,0,0),arm_l=(20,0,-55),leg_l=(28,0,-8)),pose(14,body=(5,-25,5),arm_r=(105,-40,-45),arm_l=(55,0,-25)),pose(18,body=(-20,30,-6),head=(8,-20,0),arm_r=(90,50,45),arm_l=(15,0,-45),leg_r=(30,0,8)),pose(22,body=(8,25,-5),arm_r=(150,0,10),arm_l=(45,0,-20)),pose(26,body=(-28,-10,0),head=(15,0,0),arm_r=(75,0,5),arm_l=(35,0,-40),leg_l=(35,0,-8)),pose(31,body=(-14,-20,5),arm_r=(25,-20,-15),leg_l=(15,0,0)),pose(40)])
anim('wrench_smash',34,[pose(0),pose(10,body=(15,15,0),head=(-12,-10,0),arm_r=(160,0,10),arm_l=(65,0,-25),leg_r=(-15,0,4)),pose(14,body=(20,8,0),position=(0,.5,0),arm_r=(175,0,5),arm_l=(80,0,-20)),pose(17,body=(-35,-15,0),head=(15,10,0),position=(0,-1,0),arm_r=(65,0,-5),fore_r=(10,0,0),arm_l=(20,0,-45),leg_r=(30,0,5),shin_l=(-25,0,0)),pose(22,body=(-28,-20,0),arm_r=(30,0,-15),arm_l=(10,0,-30),leg_r=(20,0,5)),pose(34)])
anim('zigzag_dash',40,[pose(0),pose(5,body=(-20,20,-15),arm_r=(45,0,30),arm_l=(-30,0,-15),leg_r=(35,0,10),shin_l=(-40,0,0)),pose(10,body=(-25,-30,15),head=(10,20,0),arm_r=(85,-30,-30),arm_l=(35,0,-55),leg_l=(40,0,-10)),pose(14,body=(-18,-20,15),arm_r=(120,-30,-10),leg_r=(35,0,5),shin_l=(-45,0,0)),pose(18,body=(-25,30,-15),head=(10,-20,0),arm_r=(90,35,45),arm_l=(-20,0,-30),leg_r=(45,0,10)),pose(22,body=(-20,20,-10),arm_r=(150,0,10),leg_l=(40,0,-10)),pose(26,body=(-30,-10,8),arm_r=(70,0,-10),arm_l=(40,0,-40),leg_l=(30,0,-10)),pose(32,body=(-10,-15,5),arm_r=(30,0,-10)),pose(40)])
anim('cackle',44,[pose(0),pose(10,body=(12,0,0),head=(20,0,-15),arm_l=(75,0,-25),fore_l=(50,0,0),arm_r=(-20,15,15),leg_r=(8,0,5)),pose(14,body=(18,10,5),head=(28,-10,15),arm_l=(85,0,-20),fore_l=(70,0,0),arm_r=(-25,20,25)),pose(20,body=(8,25,-5),head=(-5,-15,-10),arm_r=(105,35,35),arm_l=(30,0,-20)),pose(24,body=(-25,-30,8),head=(10,20,0),arm_r=(85,-45,-20),arm_l=(15,0,-55),leg_r=(28,0,8)),pose(30,body=(-10,-25,0),arm_r=(25,-30,-15)),pose(44)])
anim('junk_throw',34,[pose(0),pose(10,body=(8,30,0),head=(-5,-20,0),arm_r=(150,25,10),fore_r=(55,0,0),arm_l=(45,0,-35),leg_l=(15,0,-5)),pose(15,body=(-20,-25,5),arm_r=(100,-15,0),fore_r=(0,0,0),arm_l=(10,0,-45),leg_r=(25,0,5)),pose(17,body=(5,25,0),arm_r=(145,25,10),fore_r=(45,0,0)),pose(19,body=(-20,-25,5),arm_r=(100,-15,0),fore_r=(0,0,0),leg_l=(20,0,-5)),pose(21,body=(5,25,0),arm_r=(145,25,10),fore_r=(45,0,0)),pose(23,body=(-20,-25,5),arm_r=(100,-15,0),fore_r=(0,0,0),arm_l=(10,0,-40),leg_r=(25,0,5)),pose(28,body=(-8,-15,0),arm_r=(55,-15,0)),pose(34)])
anim('tantrum',40,[pose(0),pose(10,body=(10,10,-10),head=(-10,-5,10),arm_r=(140,0,30),arm_l=(90,0,-45),leg_r=(70,0,8),shin_r=(-80,0,0)),pose(16,body=(-25,-15,8),position=(0,-1,0),head=(15,10,-5),arm_r=(30,-20,-10),arm_l=(20,0,-50),leg_r=(-8,0,5)),pose(20,body=(10,-10,10),arm_r=(100,0,40),arm_l=(140,0,-30),leg_l=(75,0,-8),shin_l=(-80,0,0)),pose(24,body=(-25,15,-8),position=(0,-1,0),head=(15,-10,5),arm_r=(20,0,40),arm_l=(25,0,-10),leg_l=(-8,0,-5)),pose(30,body=(-10,10,0),arm_r=(15,0,20),arm_l=(15,0,-20)),pose(40)])
anim('jump_scare',36,[pose(0),pose(6,body=(-25,10,0),position=(0,-1.7,0),head=(10,0,0),arm_r=(130,10,20),arm_l=(-15,0,-35),leg_r=(55,0,8),leg_l=(45,0,-8),shin_r=(-75,0,0),shin_l=(-65,0,0)),pose(8,body=(-18,10,0),arm_r=(150,10,10),arm_l=(65,0,-40),leg_r=(50,0,8),leg_l=(-30,0,-8)),pose(15,body=(5,20,0),head=(-10,-10,0),arm_r=(170,10,5),arm_l=(45,0,-35),leg_r=(60,0,8),shin_r=(-50,0,0)),pose(20,body=(-35,-20,0),head=(15,10,0),arm_r=(70,-10,-5),arm_l=(20,0,-50),leg_r=(20,0,8),shin_l=(-35,0,0)),pose(26,body=(-20,-25,0),position=(0,-1,0),arm_r=(30,-20,-10),leg_r=(25,0,5)),pose(36)])
# Enraged three-pass charge, each pass has its own windup and recovery beat.
mel=[pose(0),pose(6,body=(-20,20,-8),arm_r=(135,25,35),arm_l=(-20,0,-30),leg_r=(35,0,5))]
for t,s in ((12,1),(28,-1),(44,1)):
    if t>12:mel.append(pose(t-5,body=(5,25*s,-8*s),arm_r=(145,25*s,35*s),arm_l=(45,0,-25),leg_r=(30,0,5)))
    mel.append(pose(t,body=(-30,-30*s,10*s),head=(12,20*s,-5*s),arm_r=(90,-45*s,-30*s),arm_l=(15,0,-50),leg_l=(35,0,-8),shin_r=(-25,0,0)))
    mel.append(pose(t+5,body=(-12,-25*s,5*s),arm_r=(35,-20*s,-15*s),leg_r=(20,0,5)))
mel.append(pose(60));anim('meltdown',60,mel)
anim('reverse_cut',30,[pose(0),pose(7,body=(5,-30,8),head=(0,20,0),arm_r=(105,-55,-40),arm_l=(55,0,-20),leg_l=(25,0,-5)),pose(12,body=(-18,35,-8),head=(10,-20,0),arm_r=(95,55,55),arm_l=(10,0,-45),leg_r=(30,0,8)),pose(17,body=(-8,40,-5),arm_r=(45,55,60),leg_r=(15,0,5)),pose(30)])
anim('heel_kick',32,[pose(0),pose(8,body=(12,-20,-10),head=(-5,10,0),arm_r=(100,0,35),arm_l=(75,0,-40),leg_r=(85,0,8),shin_r=(-95,0,0)),pose(14,body=(18,10,-12),head=(-10,-10,0),arm_r=(35,0,45),arm_l=(45,0,-60),leg_r=(90,0,8),shin_r=(0,0,0),foot_r=(-15,0,0)),pose(19,body=(8,15,-5),arm_r=(45,0,25),leg_r=(40,0,5),shin_r=(-65,0,0)),pose(32)])
anim('knife_lunge',36,[pose(0),pose(7,body=(8,25,0),head=(-5,-15,0),position=(0,-1,0),arm_r=(65,20,30),fore_r=(65,0,0),arm_l=(20,0,-20),leg_r=(35,0,5),shin_l=(-40,0,0)),pose(10,body=(-20,20,0),arm_r=(90,0,10),fore_r=(35,0,0),arm_l=(-20,0,-25),leg_r=(45,0,8)),pose(16,body=(-32,-15,0),head=(12,10,0),arm_r=(100,-5,0),fore_r=(0,0,0),knife=(85,0,0),arm_l=(-35,0,-40),leg_r=(35,0,8),leg_l=(-30,0,-5)),pose(23,body=(-20,-20,0),arm_r=(70,-10,10),knife=(45,0,0),leg_r=(20,0,5)),pose(36)])
anim('low_sweep',38,[pose(0),pose(10,body=(-10,30,-10),head=(5,-20,0),position=(0,-1.2,0),arm_r=(30,45,55),arm_l=(60,0,-20),leg_r=(40,0,10),shin_r=(-65,0,0)),pose(18,body=(-35,-40,12),head=(20,20,-5),position=(0,-2.0,0),arm_r=(35,-65,-45),knife=(45,0,0),arm_l=(30,0,-70),leg_r=(35,0,15),shin_r=(-70,0,0),leg_l=(-25,0,-12)),pose(24,body=(-25,-45,8),position=(0,-1.6,0),arm_r=(15,-50,-30),arm_l=(15,0,-50),leg_r=(25,0,10)),pose(38)])
anim('death',40,[pose(0),pose(5,body=(20,0,-10),head=(20,0,15),arm_r=(45,0,30),arm_l=(30,0,-30)),pose(14,body=(-20,0,10),position=(0,-4,0),head=(-20,0,-15),arm_r=(15,0,10),arm_l=(10,0,-15),leg_r=(70,0,10),leg_l=(60,0,-10),shin_r=(-110,0,0),shin_l=(-100,0,0)),pose(25,body=(-65,10,25),position=(0,-7,0),head=(-20,0,20),arm_r=(25,0,65),arm_l=(20,0,-25),leg_r=(80,0,15),leg_l=(70,0,-15),shin_r=(-110,0,0),shin_l=(-100,0,0)),pose(40,body=(-85,10,35),position=(0,-8,0),head=(-15,0,20),arm_r=(10,0,75),arm_l=(10,0,-30),leg_r=(85,0,15),leg_l=(80,0,-15),shin_r=(-115,0,0),shin_l=(-105,0,0))])
os.makedirs(os.path.dirname(OUT),exist_ok=True);m.save(OUT)
print('Crazie cubes',len(m.cubes),'animations',[(a['name'],a['length']) for a in m.anims])
