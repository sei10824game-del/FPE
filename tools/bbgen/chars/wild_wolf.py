"""Nameless Werewolf: generate wild_wolf.bbmodel (Minecraft Y-up, forward -Z).
Reference: ../new-character-refs/nameless-werewolf.webp, confirmed FPE wiki appearance.
Tall humanoid WOMAN, black horns/hair, face behind hair and mouth wraps, open black
fur-lined coat, chest wraps, belt, ragged knee pants, shin wraps, black paws/tail.
No animal muzzle. Existing howl/shockwave effects are mod-original interpretations; all pick attacks are physical.
Run this file only. All 13 ability names and strike ticks match WildWolf.java.
"""
import math
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from bbgen import Model

OUT = os.path.join(os.path.dirname(__file__), '../../../src/main/resources/assets/fpe/bbmodels/wild_wolf.bbmodel')
m = Model('wild_wolf', S=6, atlas=2048)
BLACK, DARK, EDGE = 0x141820, 0x202632, 0x3B4553
COAT, COAT_D, COAT_H = 0x242A34, 0x141820, 0x414956
WRAP, WRAP_D, WRAP_H = 0xAAA8A4, 0x737780, 0xC6C4BF
FUR, FUR_D = 0x8A939C, 0x525C69
BLOOD, IRON, WOOD = 0x632A35, 0x747D87, 0x34252E
CLEAR = (0, 0, 0, 0)
FACES = ('north', 'south', 'east', 'west', 'up', 'down')


def flat(c): return lambda f: f.rect(0, 0, f.w, f.h, c)

def planes(base, shade):
    def p(f):
        f.rect(0, 0, f.w, f.h, base)
        f.poly([(0, 0), (f.w * .19, 0), (f.w * .07, f.h), (0, f.h)], shade)
    return p

def wrap(stained=False):
    def p(f):
        f.rect(0, 0, f.w, f.h, WRAP)
        for k in range(1, 5):
            y = f.h * k / 5
            f.line(0, y + f.h * .09, f.w, y - f.h * .07, WRAP_D, max(1, f.h * .035))
        if stained:
            f.poly([(f.w * .62, f.h * .2), (f.w * .84, f.h * .26),
                    (f.w * .73, f.h * .46), (f.w * .6, f.h * .38)], BLOOD)
    return p

def cube(name, bone, a, b, c=BLACK, **kw):
    kw.setdefault('grain', 0)
    return m.cube(name, bone, a, b, c, **kw)

def card(name, bone, points, z, color=BLACK, depth=.55, origin=None, rot=(0,0,0), shade=None):
    """Broad two-sided cutout blade over a solid 3D body; not a billboard-only character."""
    xs, ys = [p[0] for p in points], [p[1] for p in points]
    x0,x1,y0,y1=min(xs),max(xs),min(ys),max(ys)
    def face(reverse=False):
        def p(f):
            f.rect(0,0,f.w,f.h,CLEAR)
            def xy(x,y):
                u=(x-x0)/(x1-x0)
                return ((1-u if reverse else u)*f.w,(y1-y)/(y1-y0)*f.h)
            f.poly([xy(*q) for q in points],color)
            if shade:
                f.poly([xy(*q) for q in shade[0]],shade[1])
        return p
    faces={k:flat(CLEAR) for k in FACES}
    faces.update(north=face(),south=face(True))
    return cube(name,bone,(x0,y0,z-depth/2),(x1,y1,z+depth/2),color,
                origin=origin,rot=rot,faces=faces)

def blade(name,bone,base,length,width,depth,rot=(0,0,0),color=BLACK):
    """A thick tapered three-segment lock, visible from every angle."""
    x,y,z=base
    for i,(lo,hi,w) in enumerate([(0,.45,1),(.4,.78,.66),(.73,1,.25)]):
        cube(name+str(i),bone,(x-width*w/2,y-length*hi,z-depth*w/2),
             (x+width*w/2,y-length*lo,z+depth*w/2),color,
             origin=base,rot=rot,faces={'north':planes(color,DARK if color==BLACK else COAT_D)})

# ------------------------------------------------------------------ skeleton: humanoid proportions, no snout
m.group('root',(0,0,0))
m.group('hips',(0,24,0),parent='root')
m.group('body',(0,27,0),parent='hips')
m.group('chest',(0,35,0),parent='body')
m.group('head',(0,42,0),parent='chest')
m.group('hair_back',(0,48,2.5),parent='head')
m.group('hair_r',(3,48,0),parent='head')
m.group('hair_l',(-3,48,0),parent='head')
m.group('bangs',(0,49,-3),parent='head')
m.group('coat_back',(0,29,2.8),parent='body')
for s,k in ((1,'r'),(-1,'l')):
    m.group('arm_'+k,(s*6,39,0),parent='chest')
    m.group('fore_'+k,(s*7,30,0),parent='arm_'+k)
    m.group('hand_'+k,(s*7.5,22,0),parent='fore_'+k)
    m.group('coat_'+k,(s*3.2,29,0),parent='body')
    m.group('thigh_'+k,(s*2.5,24,0),parent='hips')
    m.group('shin_'+k,(s*2.6,13.5,0),parent='thigh_'+k)
    m.group('foot_'+k,(s*2.6,4.2,-.6),parent='shin_'+k)
m.group('weapon',(7.5,22,-1),parent='hand_r')
m.group('tail0',(0,25,2.5),parent='hips')
m.group('tail1',(0,21,9),parent='tail0')
m.group('tail2',(0,22,16),parent='tail1')

# ------------------------------------------------------------------ legs and paws
for s,k in ((1,'r'),(-1,'l')):
    x=2.6*s
    cube('trouser_'+k,'thigh_'+k,(x-2,14,-2),(x+2,25,2.2),COAT,
         faces={'north':planes(COAT,COAT_D),'south':planes(COAT_D,BLACK)})
    for j in range(3):
        xx=x+(j-1)*1.2
        card('pant_hem_'+k+str(j),'thigh_'+k,[(xx-.8,16),(xx+.8,16),(xx+.5,12.8+j%2),(xx-.4,14)],-2.1,COAT)
    cube('shin_wrap_'+k,'shin_'+k,(x-1.35,5.0,-1.4),(x+1.35,14.3,1.4),WRAP,
         faces={f:wrap() for f in FACES})
    cube('heel_'+k,'foot_'+k,(x-1.6,1,-1.3),(x+1.6,5.3,1.6),BLACK)
    cube('paw_'+k,'foot_'+k,(x-2.15,.5,-4),(x+2.15,3.0,.8),DARK,
         faces={'north':planes(DARK,BLACK),'up':planes(DARK,EDGE)})
    for j in range(3):
        xx=x+(j-1)*1.3
        cube('toe_'+k+str(j),'foot_'+k,(xx-.55,.1,-5),(xx+.55,1.8,-2.7),BLACK)
        cube('claw_'+k+str(j),'foot_'+k,(xx-.23,0,-6),(xx+.23,.7,-4.5),EDGE,
             origin=(xx,.5,-4.5),rot=(-10,0,(j-1)*3))

# ------------------------------------------------------------------ torso / chest wraps / open coat / belt
cube('pelvis','hips',(-4.5,23,-2.6),(4.5,28,2.7),COAT_D)
cube('waist','body',(-3.5,27,-2.15),(3.5,33,2.1),DARK)
cube('torso','chest',(-4.2,32,-2.6),(4.2,40.5,2.7),COAT)
cube('chest_wrap','chest',(-3.7,32,-2.9),(3.7,39.5,-2.55),WRAP,
     faces={'north':wrap(True)})
cube('neck','chest',(-1.3,40,-1.3),(1.3,43.4,1.2),DARK)
cube('back_coat','chest',(-4.45,31,2.0),(4.45,40.4,3.3),COAT_D,
     faces={'south':planes(COAT,BLACK)})
for s,k in ((1,'r'),(-1,'l')):
    a,b=sorted((s*2.9,s*5.0))
    cube('coat_front_'+k,'chest',(a,29,-3.0),(b,40,1.1),COAT,
         faces={'north':planes(COAT,EDGE)})
    card('lapel_'+k,'chest',[(s*1.1,40.4),(s*5.0,40.7),(s*4.6,34.5),(s*2.4,37.0)],-3.3,COAT_H)
    pts=[(s*3,30),(s*5.1,31),(s*7.0,18),(s*5.1,19.4),(s*4.2,16.5),(s*2.8,20)]
    card('coat_tail_'+k,'coat_'+k,pts,.4,COAT,depth=1.0,origin=(s*3.2,29,0),rot=(-8,0,-s*8))
    blade('coat_side_'+k,'coat_'+k,(s*4.4,29,1),10.5,3,2.5,(0,0,s*12),COAT_D)
# Broad rear tails retain thickness, separated only at the frayed tips.
cube('coat_rear_top','coat_back',(-4.6,23,2.4),(4.6,30,3.5),COAT)
for s in (-1,1):
    card('coat_rear_'+str(s),'coat_back',[(s*.2,27),(s*4.8,27),(s*6.2,17.5),(s*3.5,19),(s*1,16)],3.3,COAT_D,depth=.8)
cube('belt','body',(-4.1,27,-2.7),(4.1,28.5,2.7),BLACK)
cube('buckle','body',(-.9,26.9,-2.95),(.9,28.5,-2.65),IRON,
     faces={'north':lambda f:(f.rect(0,0,f.w,f.h,IRON),f.rect(f.w*.24,f.h*.22,f.w*.52,f.h*.56,BLACK))})
# Fur framing the collar is lighter than the coat, not a grey wolf's body.
for s,k in ((1,'r'),(-1,'l')):
    for i in range(3):
        x=s*(1.8+i*1.4)
        card('fur_lapel_'+k+str(i),'chest',[(x-s*.85,41.3-i*.65),(x+s*1.1,41-i*.7),
             (x+s*.4,37.8-i*.3),(x-s*.7,39.2-i*.3)],-3.35,FUR if i%2==0 else FUR_D,depth=.7)
cube('fur_back','chest',(-5,39.8,1.1),(5,41.8,3.1),FUR_D)

# ------------------------------------------------------------------ long sleeves, hands and broad hooked black claws
for s,k in ((1,'r'),(-1,'l')):
    x=6.6*s
    cube('shoulder_'+k,'arm_'+k,(x-2.2,35,-2.1),(x+2.2,40.5,2.3),COAT,
         faces={'north':planes(COAT,EDGE)})
    cube('sleeve_'+k,'arm_'+k,(x-1.8,29,-1.8),(x+1.8,36.6,1.9),COAT_D)
    x=7.2*s
    cube('forearm_'+k,'fore_'+k,(x-1.45,22,-1.4),(x+1.45,30.5,1.4),COAT,
         faces={'north':planes(COAT,BLACK)})
    cube('cuff_'+k,'fore_'+k,(x-1.7,22,-1.6),(x+1.7,24,1.6),FUR_D)
    x=7.5*s
    cube('palm_'+k,'hand_'+k,(x-1.8,18.8,-1.3),(x+1.8,22.5,1.1),DARK)
    for i in range(3):
        xx=x+(i-1)*1.15
        card('finger_'+k+str(i),'hand_'+k,[(xx-.65,19.8),(xx+.65,19.8),(xx+.8,17.3),
             (xx+.2,14.6+abs(i-1)*.6),(xx-.55,17.4)],-.7,BLACK,depth=.7,
             origin=(xx,19.4,-.6),rot=(16,0,(i-1)*-9))
    blade('thumb_'+k,'hand_'+k,(x-s*1.5,20.7,-.8),3.4,1.3,1.1,(18,0,s*28),DARK)

# ------------------------------------------------------------------ head: human silhouette entirely hidden by black hair/mouth wraps
cube('head_core','head',(-3.5,42,-3),(3.5,49.6,2.8),DARK)
def mouth_wrap(f):
    f.rect(0,0,f.w,f.h,0x66717B)
    for q in (.27,.57,.82):
        f.line(0,f.h*q+1,f.w,f.h*q-1,0x36414D,max(1,f.h*.06))
cube('mouth_wrap','head',(-2.8,42.3,-3.17),(2.8,44.9,-2.92),0x56616D,
     faces={'north':mouth_wrap})
cube('hair_cap','head',(-4,47,-3.3),(4,50.6,3.4),BLACK,
     faces={'north':planes(BLACK,DARK),'up':flat(DARK)})
cube('hair_rear_core','hair_back',(-3.9,32,2.6),(3.9,49,5),BLACK,
     faces={'south':planes(BLACK,DARK)})
# Swept locks overlap into one bedraggled mass, rather than thousands of hair needles.
for s,k in ((1,'r'),(-1,'l')):
    cube('hair_side_core_'+k,'hair_'+k,(min(s*2.9,s*4.5),40,-2.7),(max(s*2.9,s*4.5),49,3.5),BLACK)
    for i,(top,low,reach) in enumerate([(49.6,43.5,7.5),(45.8,38.4,7.0),(41.5,33,7.9),(37,28,7.4)]):
        pts=[(s*2.8,top),(s*reach,top-.6),(s*(reach-1.8),top-2.3),
             (s*(reach+.4),low+1.4),(s*4.7,low),(s*2.8,low+2.2)]
        card('hair_sweep_'+k+str(i),'hair_'+k,pts,1.1+i*.7,BLACK if i%2 else DARK,depth=.9,
             origin=(s*3,48,0),rot=(-6,s*12,0))
    blade('hair_back_lock_'+k,'hair_back',(s*2.6,43,4.4),16,4.0,2.1,(-7,0,-s*9),BLACK)
card('fringe','bangs',[(-4.2,50.3),(4.2,50.3),(3.6,45.3),(1.6,43.7),(1.8,46.2),
     (-.7,44.4),(-.2,46.5),(-3.2,44.8)],-3.5,BLACK,depth=.6,
     shade=([(-3.6,50),(3.3,50),(-1.1,46.8)],DARK))
# Two black horns: narrow at the tips, leaning outward. No wolf ears or muzzle.
for s,k in ((1,'r'),(-1,'l')):
    cube('horn_base_'+k,'head',(s*2.3-.8,49.3,-.6),(s*2.3+.8,52.0,1.0),BLACK,
         origin=(s*2.3,49.5,0),rot=(-20,0,-s*16))
    cube('horn_tip_'+k,'head',(s*3.1-.38,51.5,.4),(s*3.1+.38,54.3,1.2),DARK,
         origin=(s*3.1,51.5,.8),rot=(-24,0,-s*22))

# ------------------------------------------------------------------ long black tail curves behind the coat
cube('tail_base','tail0',(-1.4,20.2,2.4),(1.4,25.3,9.7),BLACK,origin=(0,25,2.5),rot=(-12,0,0))
cube('tail_middle','tail1',(-1.2,20.1,8.7),(1.2,23.2,16.5),DARK)
cube('tail_end','tail2',(-1.0,21.7,15.5),(1.0,26.6,18.1),BLACK,origin=(0,22,16),rot=(22,0,0))
blade('tail_tip','tail2',(0,27,17.4),3.7,2.7,2,(155,0,0),BLACK)

# ------------------------------------------------------------------ carried pick: dark handle, battered metal head with restrained red staining
cube('pick_handle','weapon',(6.85,9.5,-1.55),(8.15,32,-.45),WOOD,
     faces={'north':planes(WOOD,BLACK)})
cube('pick_grip','weapon',(6.7,19.1,-1.7),(8.3,23.0,-.3),WRAP_D,faces={'north':wrap()})
cube('pick_socket','weapon',(6.1,9,-2.1),(8.9,12,-.1),IRON)
card('pick_head','weapon',[(.5,8.4),(3.5,12),(7.5,12.7),(12,11.5),(15.3,8.2),
     (11.5,9.4),(8,10.1),(4,10.0)],-1.2,IRON,depth=1.0,
     shade=([(.5,8.4),(3.5,12),(5.0,12.2),(3.8,10.1)],BLOOD))
cube('pick_rear_spike','weapon',(12.8,8.4,-1.6),(14.8,9.4,-.7),BLOOD)

# ------------------------------------------------------------------ fully authored body animation, shared timing with server attacks
REST={'body':(-7,0,0),'chest':(6,0,0),'head':(-2,0,-4),
      'arm_r':(8,0,12),'fore_r':(16,0,-6),'hand_r':(0,0,0),
      'arm_l':(6,0,-12),'fore_l':(12,0,5),'hand_l':(0,0,0),
      'thigh_r':(-5,0,3),'thigh_l':(6,0,-3),'shin_r':(8,0,0),'shin_l':(-4,0,0),
      'foot_r':(-3,0,0),'foot_l':(2,0,0),'weapon':(0,0,-8),
      'hair_back':(-3,0,0),'hair_r':(0,0,0),'hair_l':(0,0,0),
      'coat_back':(-2,0,0),'coat_r':(0,0,0),'coat_l':(0,0,0),
      'tail0':(0,12,0),'tail1':(0,-18,0),'tail2':(0,12,0)}

class Anim:
    def __init__(self,name,dur,loop=False):
        self.name,self.dur,self.loop=name,dur,loop
        self.tr={b:{'rotation':[(0,*r),(dur,*r)]} for b,r in REST.items()}
    def key(self,b,ch,t,v):
        channels=self.tr.setdefault(b,{})
        if ch not in channels:
            neutral=(1,1,1) if ch=='scale' else (0,0,0)
            channels[ch]=[(0,*neutral),(self.dur,*neutral)]
        keys=channels[ch]
        keys[:]=[q for q in keys if q[0]!=t]
        keys.append((t,*v));return self
    def pose(self,t,**bones):
        for b,v in bones.items():self.key(b,'rotation',t,v)
        # Cloth/hair lag follows the authored spine and shoulders.
        if 'body' in bones:
            x,y,z=bones['body']; lag=min(self.dur,t+2)
            for b,mul in [('hair_back',-.5),('hair_r',-.3),('hair_l',-.35),('coat_back',-.35)]:
                self.key(b,'rotation',lag,(x*mul,-y*.25,-z*.25))
            self.key('coat_r','rotation',lag,(-x*.18,0,-y*.3))
            self.key('coat_l','rotation',lag,(-x*.18,0,-y*.3))
            self.key('tail0','rotation',lag,(x*.3,12-y*.5,-z*.5))
            self.key('tail1','rotation',min(self.dur,t+4),(-x*.25,-18+y*.7,z*.4))
        return self
    def pos(self,t,b,v):return self.key(b,'position',t,v)
    def done(self):
        if self.loop:
            for chans in self.tr.values():
                for keys in chans.values():
                    first=min(keys,key=lambda q:q[0])
                    keys[:]=[q for q in keys if q[0]!=self.dur]
                    keys.append((self.dur,*first[1:]))
        # BbModel's torso/head +X bends backward; poses above use forward-positive.
        # Convert these axes once, keeping limbs (forward-positive already) unchanged.
        reverse_x={'body','chest','head','hair_back','hair_r','hair_l',
                   'coat_back','coat_r','coat_l','tail0','tail1'}
        tracks={}
        for bone,chans in self.tr.items():
            tracks[bone]={}
            for channel,keys in chans.items():
                tracks[bone][channel]=[(t/20, -x if channel=='rotation' and bone in reverse_x else x,y,z)
                                       for t,x,y,z in sorted(keys)]
        m.anim(self.name,self.dur/20,tracks,loop=self.loop)

# Breathing stalk; hands flex through wrist motion and heavy tail counterbalances.
a=Anim('idle',80,True)
for t,q in [(0,0),(20,1),(40,0),(60,-1),(80,0)]:
    a.pose(t,body=(-7+q,0,q),chest=(6-q,0,0),head=(-2,2*q,-4),
           fore_l=(12+q*3,0,5),fore_r=(16-q*2,0,-6))
    a.pos(t,'body',(0,.22*q,0))
    a.key('tail1','rotation',t,(0,-18+10*q,2*q))
a.done()
a=Anim('walk',24,True)
for t,q in [(0,1),(6,0),(12,-1),(18,0),(24,1)]:
    a.pose(t,body=(-9,-5*q,2*q),chest=(5,8*q,-2*q),head=(-1,-3*q,-3),
           thigh_r=(26*q,0,3),thigh_l=(-26*q,0,-3),shin_r=(max(0,-q)*26,0,0),shin_l=(max(0,q)*26,0,0),
           foot_r=(-10*q,0,0),foot_l=(10*q,0,0),arm_r=(8-10*q,0,12),arm_l=(6+20*q,0,-12),
           fore_r=(16,0,-6),fore_l=(12+8*max(0,q),0,5))
    a.pos(t,'hips',(0,-.6*abs(q),0))
a.done()

# Overhead pick impact: anticipation 17, hit21, heavy compression25.
a=Anim('pick_smash',44)
a.pose(10,body=(-18,-12,4),chest=(-15,-10,0),head=(8,8,0),arm_r=(-145,-15,18),fore_r=(15,0,0),arm_l=(-55,0,-25),thigh_r=(-18,0,6),shin_r=(25,0,0))
a.pose(18,body=(-24,-16,4),chest=(-18,-12,0),arm_r=(-175,-10,12),fore_r=(30,0,0),arm_l=(-100,0,-28),head=(12,10,0))
a.pose(21,body=(38,12,-8),chest=(26,14,0),head=(-20,-10,0),arm_r=(70,0,8),fore_r=(12,0,0),arm_l=(45,0,-28),thigh_l=(-24,0,-5),shin_l=(32,0,0))
a.pose(26,body=(46,18,-8),chest=(22,8,0),arm_r=(83,0,8),fore_r=(20,0,0),arm_l=(54,0,-18),head=(-26,-8,0));a.pos(21,'hips',(0,-2.5,-.4));a.pos(32,'hips',(0,-.8,0));a.pos(44,'hips',(0,0,0));a.pose(35,body=(8,0,0),arm_r=(18,0,10));a.done()

# Wide horizontal pick sweep with torso/hip counter-twist.
a=Anim('pick_sweep',40)
a.pose(8,body=(-8,-42,7),chest=(0,-24,0),head=(0,30,-5),arm_r=(-18,-35,72),fore_r=(28,0,0),arm_l=(18,0,-28),thigh_r=(-12,-8,5),thigh_l=(12,8,-5))
a.pose(14,body=(-10,-58,10),chest=(-4,-24,0),arm_r=(-12,-35,88),fore_r=(8,0,0),head=(0,38,-5))
a.pose(17,body=(12,46,-10),chest=(8,30,0),arm_r=(68,38,-12),fore_r=(32,0,0),arm_l=(10,-10,-38),head=(-4,-28,0))
a.pose(23,body=(16,66,-12),chest=(10,20,0),arm_r=(95,55,-30),fore_r=(45,0,0),arm_l=(-22,0,-35),head=(-6,-30,0));a.pose(32,body=(-2,12,-2),arm_r=(20,10,12));a.done()

# Alternating claw rake, each strike has a distinct shoulder lead.
a=Anim('claw_rake',34)
for wind,hit,sign in [(5,9,1),(12,15,-1),(18,21,1)]:
    a.pose(wind,body=(-8,-25*sign,6*sign),chest=(-5,-18*sign,0),head=(0,15*sign,0),
           arm_l=(-35,-20, -65) if sign>0 else (20,25,-5),fore_l=(48,0,0),arm_r=(0,0,25),
           thigh_r=(-10*sign,0,4),thigh_l=(10*sign,0,-4))
    a.pose(hit,body=(18,30*sign,-6*sign),chest=(12,20*sign,0),head=(-8,-20*sign,0),
           arm_l=(90,25,25) if sign>0 else (90,-35,-65),fore_l=(12,0,0),hand_l=(30,0,10*sign),arm_r=(25,0,18))
a.pose(27,body=(6,8,0),arm_l=(34,0,-20),fore_l=(18,0,0));a.done()

# Grounded coil -> launch14 -> airborne reach -> landing readiness.
a=Anim('pounce',44)
a.pose(8,body=(26,0,0),chest=(16,0,0),head=(-22,0,0),thigh_r=(-55,0,12),thigh_l=(-55,0,-12),shin_r=(75,0,0),shin_l=(75,0,0),arm_r=(-35,0,30),arm_l=(-48,0,-30));a.pos(8,'hips',(0,-4,0))
a.pose(14,body=(24,0,0),chest=(8,0,0),head=(-25,0,0),thigh_r=(28,0,6),thigh_l=(22,0,-6),shin_r=(-12,0,0),shin_l=(-12,0,0),arm_r=(80,0,18),arm_l=(105,0,-18),fore_l=(8,0,0));a.pos(14,'hips',(0,0,0))
a.pose(22,body=(32,0,0),head=(-28,0,0),thigh_r=(-42,0,14),thigh_l=(-40,0,-14),shin_r=(52,0,0),shin_l=(48,0,0),arm_l=(70,0,-30),arm_r=(48,0,18));a.pose(32,body=(16,0,0),thigh_r=(-18,0,4),thigh_l=(-18,0,-4),shin_r=(28,0,0),shin_l=(28,0,0));a.done()

# Fear howl: chest opens, bandaged face tilts skyward, coat and hair recoil.
a=Anim('howl',50)
a.pose(8,body=(12,0,0),chest=(18,0,0),head=(25,0,0),arm_l=(18,0,-18),arm_r=(18,0,18),thigh_r=(-12,0,10),thigh_l=(-12,0,-10),shin_r=(18,0,0),shin_l=(18,0,0))
for t,q in [(14,0),(19,1),(24,-1),(29,1),(34,0)]:
    a.pose(t,body=(-16+q*2,0,q),chest=(-18,0,0),head=(-40+q*4,0,0),arm_r=(-22,0,48),arm_l=(-25,0,-55),fore_r=(8,0,0),fore_l=(12,0,0),thigh_r=(0,0,12),thigh_l=(0,0,-12),shin_r=(4,0,0),shin_l=(4,0,0))
a.pose(41,body=(-2,0,0),chest=(4,0,0),head=(-6,0,0),arm_l=(8,0,-22));a.done()

# Pick throw hides only the carried prop during its travel; keep full follow-through.
a=Anim('pick_throw',40)
a.pose(8,body=(-14,-30,6),chest=(-10,-22,0),head=(4,25,-3),arm_r=(-120,-25,35),fore_r=(48,0,0),arm_l=(30,0,-30),thigh_r=(-16,0,5),shin_r=(24,0,0))
a.pose(16,body=(-20,-40,10),arm_r=(-155,-30,30),fore_r=(60,0,0),head=(8,30,0))
a.pose(17,body=(20,28,-8),chest=(16,25,0),arm_r=(100,15,8),fore_r=(4,0,0),arm_l=(-15,0,-35),head=(-10,-18,0),thigh_l=(-18,0,-4),shin_l=(28,0,0))
a.pose(24,body=(28,48,-10),arm_r=(125,35,-12),fore_r=(12,0,0),head=(-18,-25,0));a.pose(34,body=(0,10,0),arm_r=(28,0,16))
for t,v in [(0,(1,1,1)),(16.9,(1,1,1)),(17,(.001,.001,.001)),(34,(.001,.001,.001)),(38,(1,1,1))]:a.key('weapon','scale',t,v)
a.done()

# Braced pick thrust: draw the tool to the ribs, step14, straight contact18, retract.
# Replaces ground_pick; there are no summoned spikes or tentacles in this character.
a=Anim('pick_thrust',36)
a.pose(7,body=(-8,-22,3),chest=(-4,-14,0),head=(3,18,-2),
       arm_r=(30,-22,22),fore_r=(78,0,0),hand_r=(-8,0,0),weapon=(-12,0,8),
       arm_l=(42,-15,15),fore_l=(62,10,0),hand_l=(5,0,0),
       thigh_r=(-22,0,7),thigh_l=(10,0,-5),shin_r=(32,0,0),shin_l=(2,0,0))
a.pos(7,'hips',(0,-1.1,.3))
a.pose(13,body=(-12,-30,4),chest=(-6,-18,0),head=(5,24,-2),
       arm_r=(24,-26,20),fore_r=(90,0,0),hand_r=(-10,0,0),weapon=(-12,0,8),
       arm_l=(40,-18,18),fore_l=(78,10,0),thigh_r=(-28,0,8),thigh_l=(14,0,-6),
       shin_r=(38,0,0),shin_l=(2,0,0))
a.pos(13,'hips',(0,-1.5,.4))
a.pose(18,body=(22,15,-4),chest=(8,18,0),head=(-8,-20,0),
       arm_r=(105,5,-8),fore_r=(0,0,0),hand_r=(-5,0,0),weapon=(0,0,0),
       arm_l=(100,-25,25),fore_l=(20,10,0),hand_l=(12,0,0),
       thigh_r=(20,0,5),thigh_l=(-28,0,-6),shin_r=(0,0,0),shin_l=(32,0,0),
       foot_r=(-7,0,0),foot_l=(5,0,0))
a.pos(18,'hips',(0,-.4,-.6))
a.pose(21,body=(26,20,-5),chest=(10,18,0),head=(-12,-20,0),
       arm_r=(109,5,-8),fore_r=(4,0,0),hand_r=(-5,0,0),weapon=(0,0,0),
       arm_l=(104,-25,25),fore_l=(22,10,0),thigh_r=(16,0,5),thigh_l=(-24,0,-6),shin_l=(28,0,0))
a.pose(28,body=(4,8,-2),chest=(5,6,0),head=(-2,-8,-2),
       arm_r=(42,0,12),fore_r=(52,0,0),hand_r=(0,0,0),weapon=(-5,0,-4),
       arm_l=(30,-10,0),fore_l=(38,0,0),hand_l=(0,0,0),
       thigh_r=(-8,0,4),thigh_l=(3,0,-4),shin_r=(12,0,0),shin_l=(3,0,0))
a.pos(30,'hips',(0,0,0));a.done()

# Four weight-shifted charging blows, alternating left/right hips.
a=Anim('rampage',66)
for start,hit,sgn in [(8,14,1),(22,28,-1),(36,42,1),(50,56,-1)]:
    a.pose(start,body=(-12,-35*sgn,10*sgn),chest=(-8,-20*sgn,0),head=(2,25*sgn,0),
           arm_r=(-105 if sgn>0 else 12,-25*sgn,60),fore_r=(35,0,0),arm_l=(-35,0,-55),
           thigh_r=(-24*sgn,0,8),thigh_l=(24*sgn,0,-8),shin_r=(max(0,sgn)*35,0,0),shin_l=(max(0,-sgn)*35,0,0))
    a.pose(hit,body=(30,38*sgn,-8*sgn),chest=(16,25*sgn,0),head=(-18,-22*sgn,0),
           arm_r=(78,30*sgn,8),fore_r=(14,0,0),arm_l=(90,30,-15),fore_l=(8,0,0),
           thigh_r=(12*sgn,0,6),thigh_l=(-18*sgn,0,-6),shin_r=(8,0,0),shin_l=(15,0,0))
a.done()

# New physical attacks: shoulder, rising claws, hooked pick pull and heavy paw.
a=Anim('shoulder_bash',30)
a.pose(7,body=(8,-40,-8),chest=(12,-28,0),head=(-4,30,0),arm_r=(12,0,42),fore_r=(75,0,0),arm_l=(20,0,-18),fore_l=(65,0,0),thigh_r=(-35,0,8),shin_r=(48,0,0));a.pos(7,'hips',(0,-1.4,0))
a.pose(13,body=(34,35,-12),chest=(20,20,0),head=(-25,-22,0),arm_r=(32,0,48),fore_r=(70,0,0),arm_l=(18,0,-28),thigh_l=(-30,0,-8),shin_l=(42,0,0));a.pos(13,'hips',(0,-.5,-1))
a.pose(19,body=(26,42,-9),arm_r=(44,0,30),fore_r=(45,0,0));a.pos(30,'hips',(0,0,0));a.done()
a=Anim('claw_uppercut',34)
a.pose(8,body=(24,32,-7),chest=(12,18,0),head=(-15,-20,0),arm_l=(-30,15,-15),fore_l=(18,0,0),hand_l=(-20,0,0),arm_r=(18,0,26),thigh_l=(-35,0,-8),shin_l=(45,0,0));a.pos(8,'hips',(0,-2.5,0))
a.pose(14,body=(-18,-28,8),chest=(-16,-20,0),head=(-22,14,0),arm_l=(155,-20,-8),fore_l=(20,0,0),hand_l=(25,0,0),arm_r=(-10,0,35),thigh_l=(10,0,-6),shin_l=(0,0,0));a.pos(14,'hips',(0,.5,0))
a.pose(20,body=(-24,-40,10),chest=(-18,-12,0),arm_l=(178,-25,0),fore_l=(35,0,0),head=(-26,20,0));a.pos(30,'hips',(0,0,0));a.done()
a=Anim('pick_hook',40)
a.pose(9,body=(-8,-25,4),chest=(2,-18,0),head=(0,20,0),arm_r=(20,-25,45),fore_r=(65,0,0),arm_l=(25,0,-30),thigh_r=(-18,0,5),shin_r=(25,0,0))
a.pose(14,body=(16,8,-4),chest=(12,12,0),arm_r=(88,15,8),fore_r=(0,0,0),arm_l=(40,0,-18),head=(-8,-8,0))
a.pose(17,body=(8,28,-8),chest=(5,20,0),arm_r=(58,22,16),fore_r=(60,0,0),weapon=(0,25,-28),arm_l=(42,0,-8),fore_l=(55,0,0),head=(-4,-18,0))
a.pose(24,body=(-12,42,-8),chest=(-8,22,0),arm_r=(18,35,24),fore_r=(110,0,0),weapon=(0,35,-30),arm_l=(12,0,-12),fore_l=(85,0,0),head=(2,-22,0));a.pose(32,body=(-8,18,-2),fore_r=(45,0,0));a.done()
a=Anim('paw_stomp',36)
a.pose(9,body=(-8,15,8),chest=(2,-12,0),head=(12,-8,0),thigh_r=(68,0,8),shin_r=(-40,0,0),foot_r=(20,0,0),thigh_l=(-6,0,-10),arm_r=(12,0,42),arm_l=(25,0,-42));a.pos(9,'hips',(-1.4,.8,0))
a.pose(14,body=(-12,12,10),thigh_r=(85,0,6),shin_r=(-65,0,0),foot_r=(25,0,0),head=(18,-8,0))
a.pose(17,body=(25,-12,-4),chest=(18,8,0),head=(-8,6,0),thigh_r=(-15,0,5),shin_r=(10,0,0),foot_r=(-8,0,0),arm_r=(32,0,24),arm_l=(40,0,-26));a.pos(17,'hips',(0,-1.8,-.4))
a.pose(23,body=(18,-8,-2),chest=(10,4,0),head=(-4,0,0));a.pos(32,'hips',(0,0,0));a.done()

# Close left-hand slash followed by a deliberate backward step: hit13, retreat15.
a=Anim('claw_retreat',34)
a.pose(6,body=(5,26,-5),chest=(5,20,0),head=(-3,-22,-2),
       arm_l=(-20,22,-52),fore_l=(48,0,0),hand_l=(-12,0,-8),
       arm_r=(15,0,24),fore_r=(22,0,0),thigh_r=(-10,0,6),thigh_l=(12,0,-6),
       shin_r=(18,0,0),shin_l=(0,0,0))
a.pose(10,body=(9,38,-7),chest=(8,22,0),head=(-4,-28,-2),
       arm_l=(-32,26,-64),fore_l=(55,0,0),hand_l=(-18,0,-12),
       arm_r=(18,0,28),thigh_l=(18,0,-7),shin_r=(22,0,0))
a.pose(13,body=(18,-28,6),chest=(12,-22,0),head=(-8,20,0),
       arm_l=(108,-32,28),fore_l=(10,0,0),hand_l=(28,0,18),
       arm_r=(22,0,22),fore_r=(32,0,0),thigh_r=(8,0,6),thigh_l=(-18,0,-6),
       shin_r=(4,0,0),shin_l=(26,0,0))
a.pose(15,body=(-10,-38,4),chest=(-5,-18,0),head=(2,24,0),
       arm_l=(68,-28,16),fore_l=(58,0,0),hand_l=(18,0,10),
       arm_r=(-8,0,36),fore_r=(28,0,0),thigh_r=(-30,0,7),thigh_l=(30,0,-7),
       shin_r=(26,0,0),shin_l=(-8,0,0),foot_r=(5,0,0),foot_l=(-8,0,0))
a.pos(15,'hips',(0,-.7,0))
a.pose(22,body=(-5,-12,0),chest=(4,-6,0),head=(-2,10,-2),
       arm_l=(28,-10,-15),fore_l=(40,0,0),hand_l=(4,0,0),
       arm_r=(5,0,20),fore_r=(24,0,0),thigh_r=(12,0,6),thigh_l=(-12,0,-6),
       shin_r=(-4,0,0),shin_l=(18,0,0))
a.pos(28,'hips',(0,0,0));a.done()

# Death: stagger, knees buckle, hands release and body collapses sideways.
a=Anim('death',40)
a.pose(5,body=(-22,10,-8),chest=(-20,0,0),head=(-28,0,10),arm_r=(-35,0,55),arm_l=(-45,0,-55),fore_r=(20,0,0),fore_l=(15,0,0))
a.pose(14,body=(28,-12,12),chest=(18,0,0),head=(28,0,-8),thigh_r=(-65,0,10),thigh_l=(-55,0,-12),shin_r=(95,0,0),shin_l=(80,0,0),arm_r=(65,0,18),arm_l=(75,0,-18));a.pos(14,'hips',(0,-10,0))
a.pose(25,body=(38,-20,18),chest=(25,-10,0),head=(35,20,0),arm_r=(90,0,35),arm_l=(35,0,-55),fore_r=(30,0,0),fore_l=(50,0,0),thigh_r=(-50,0,12),thigh_l=(-40,0,-8),shin_r=(70,0,0),shin_l=(75,0,0))
a.key('root','rotation',0,(0,0,0));a.key('root','rotation',15,(0,0,0));a.key('root','rotation',29,(0,0,82));a.key('root','rotation',40,(0,0,87));a.pos(29,'root',(-1,2,0));a.pos(40,'root',(-1,2,0))
# Keep final collapsed pose rather than snapping back to REST on the last frame.
for bone,chans in a.tr.items():
    for channel,keys in chans.items():
        before=[q for q in keys if q[0]<40]
        if before and bone!='root':
            last=max(before,key=lambda q:q[0]);keys[:]=[q for q in keys if q[0]!=40];keys.append((40,*last[1:]))
a.done()

os.makedirs(os.path.dirname(OUT),exist_ok=True)
m.save(OUT)
print('wild_wolf:',len(m.cubes),'elements;',len(m.anims),'animations; height',max(c['to'][1] for c in m.cubes))
