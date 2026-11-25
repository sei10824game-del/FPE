"""FPE Zombie AU native geometry and shared, contact-timed animation rig.

Geometry authoring coordinates use a 32-unit-tall figure; Rig scales all cubes,
pivots and animation translations to height_blocks * 16 at export. No image data.
"""
import math
from pathlib import Path
from bbgen import Model

OUT = Path(__file__).resolve().parents[2] / 'src/main/resources/assets/fpe/bbmodels'
INK=0x142C2A; BLACK=0x102724; PAPER=0xE0E8E1; WHITE=0xEDF0E8
GREY=0xA9BBB3; MINT=0x88B0A2; DARK=0x32534A; GOLD=0xD7CE86
GREEN=0x8FE440; BLOOD=0x823D43

class Rig(Model):
    """Model with standard bones and normalized geometry coordinates.

    Use ordinary Model cube/group API. All positions are in 32-unit space.
    Bones: root/body/chest/head/hair, arms/forearms/hands, legs/shins/feet,
    coat/weapon/tail/wing_r/wing_l; hair_l/r and coat_l/r for secondary motion.
    """
    def __init__(self,name,height=2.0,style='claw',atlas=2048):
        super().__init__(name,S=3,atlas=atlas)
        self.height,self.unit,self.style=height,height*.5,style
        for n,p,parent in [
            ('root',(0,0,0),None),('body',(0,14,0),'root'),
            ('chest',(0,20,0),'body'),('head',(0,26,0),'chest'),
            ('hair',(0,29,1),'head'),('hair_r',(2,29,1),'hair'),('hair_l',(-2,29,1),'hair'),
            ('coat',(0,18,1),'body'),('coat_r',(1.5,17,1),'coat'),('coat_l',(-1.5,17,1),'coat'),
            ('tail',(0,14,1),'body'),('wing_r',(2,23,1),'chest'),('wing_l',(-2,23,1),'chest')]:
            self.group(n,p,parent=parent)
        for side,sgn in [('r',1),('l',-1)]:
            for n,p,parent in [
                ('arm',(sgn*3.2,23,0),'chest'),('fore',(sgn*4,18.5,0),'arm_'+side),
                ('hand',(sgn*4,14.5,0),'fore_'+side),
                ('leg',(sgn*1.25,14,0),'body'),('shin',(sgn*1.25,7.5,0),'leg_'+side),
                ('foot',(sgn*1.25,2,0),'shin_'+side)]:self.group(n+'_'+side,p,parent=parent)
        self.group('weapon',(4,14.5,0),parent='hand_r')
    def group(self,name,origin=(0,0,0),rot=(0,0,0),parent=None):
        return super().group(name,tuple(v*self.unit for v in origin),rot,parent)
    def cube(self,name,parent,frm,to,color=0x808080,origin=None,**kw):
        if 'inflate' in kw:kw['inflate']*=self.unit
        return super().cube(name,parent,[v*self.unit for v in frm],[v*self.unit for v in to],color,
                            origin=[v*self.unit for v in origin] if origin is not None else None,**kw)
    def finish(self):
        author_animations(self,self.height,self.style)
        OUT.mkdir(parents=True,exist_ok=True)
        self.save(OUT/(self.name+'.bbmodel'))
        return self

def cube(m,*a,**k):return m.cube(*a,**k)

def inverse_rotation(v,rotation):
    """Inverse of Blockbench/ModelPart Rz*Ry*Rx, without external packages."""
    x,y,z=[math.radians(-a) for a in rotation];px,py,pz=v
    px,py=px*math.cos(z)-py*math.sin(z),px*math.sin(z)+py*math.cos(z)
    px,pz=px*math.cos(y)+pz*math.sin(y),-px*math.sin(y)+pz*math.cos(y)
    py,pz=py*math.cos(x)-pz*math.sin(x),py*math.sin(x)+pz*math.cos(x)
    return px,py,pz

def aim_weapon(pose,axis=(0,0,-1)):
    """Counter-rotate the actual barrel axis to entity forward (-Z).

    Grace's upward rest barrel and Lizzy's forward rest barrel have different
    local axes. Invert the entire animated parent chain rather than guessing a
    wrist angle; torso turns and forearm bend are included in the solution.
    """
    d=(0,0,-1)
    for b in ('root','body','chest','arm_r','fore_r','hand_r'):
        d=inverse_rotation(d,pose.get(b,(0,0,0)))
    dx,dy,dz=d;dy=max(-1,min(1,dy))
    if tuple(axis)==(0,1,0):
        return (-math.degrees(math.acos(dy)),math.degrees(math.atan2(-dx,-dz)),0)
    if tuple(axis)==(0,0,-1):
        return (math.degrees(math.asin(dy)),math.degrees(math.atan2(-dx,-dz)),0)
    raise ValueError('gun_axis must be up (0,1,0) or forward (0,0,-1)')

def rib(m,name,bone,a,b,width,depth,color,**kw):
    dx,dy,dz=(v-u for u,v in zip(a,b));length=math.dist(a,b)
    if length<.001:raise ValueError(name+' has zero length')
    x,y,z=a
    return m.cube(name,bone,(x-width/2,y-.015,z-depth/2),(x+width/2,y+length+.015,z+depth/2),
        color,origin=a,rot=(math.degrees(math.asin(dz/length)),0,-math.degrees(math.atan2(dx,dy))),grain=.012,**kw)

def solid_poly(m,name,bone,points,z,depth,color,step=.45):
    lo,hi=min(y for x,y in points),max(y for x,y in points)
    n=max(1,math.ceil((hi-lo)/step))
    for j in range(n):
        y=lo+(hi-lo)*j/n;h=(hi-lo)/n;mid=y+h/2;xs=[]
        for (a,b),(c,d) in zip(points,points[1:]+points[:1]):
            if min(b,d)<=mid<max(b,d):xs.append(a+(c-a)*(mid-b)/(d-b))
        xs.sort()
        for k in range(0,len(xs)-1,2):
            if xs[k+1]-xs[k]>.001:
                dep=depth(mid) if callable(depth) else depth
                m.cube(f'{name}_{j}_{k}',bone,(xs[k],y,z-dep/2),(xs[k+1],y+h+.008,z+dep/2),color,grain=.012,res=2)

def card(m,name,bone,bounds,points,z,color,depth=.3,paint=None):
    # Solid extrusion instead of a camera-facing alpha plane.
    return solid_poly(m,name,bone,points,z,depth,color)

def head(m,color=PAPER,y=25,width=5,height=5.6,depth=3):
    for j in range(8):
        t=(j+.5)/8;w=width*.5*math.sqrt(max(.12,1-(2*t-1)**2))
        m.cube('head_volume_'+str(j),'head',(-w,y+j*height/8,-depth/2),(w,y+(j+1)*height/8+.012,depth/2),color,grain=.01,res=4)

def face(m,bandage=False,eyes=INK,angry=False):
    for s in [-1,1]:
        m.cube('eye_'+str(s),'head',(s*1.05-.32,27.6,-1.62),(s*1.05+.32,28.15,-1.49),eyes,grain=0)
        if angry:rib(m,'brow_'+str(s),'head',(s*.45,28.5,-1.67),(s*1.5,28.8,-1.67),.20,.12,INK)
    rib(m,'mouth','head',(-.6,26.4,-1.64),(.65,26.5,-1.64),.13,.14,INK)
    if bandage:
        for i in range(4):
            m.cube('facial_bandage_'+str(i),'head',(-2.1,25.5+i*.58,-1.72),(2.1,25.94+i*.58,-1.58),GREY,rot=(0,0,-8),origin=(0,27,-1.6),grain=.02)
            rib(m,'bandage_seam_'+str(i),'head',(-1.8,25.72+i*.58,-1.79),(1.7,25.72+i*.58,-1.79),.045,.04,DARK)

def limbs(m,shirt=PAPER,pants=INK,boots=INK,skin=PAPER,boot_height=3):
    m.cube('torso','chest',(-2.4,15,-1.1),(2.4,23.5,1.2),shirt,grain=.018)
    m.cube('neck','chest',(-.7,23,-.6),(.7,25.7,.6),skin,grain=.012)
    for side,s in [('r',1),('l',-1)]:
        rib(m,'sleeve_'+side,'arm_'+side,(s*2.8,23,0),(s*4,18.6,0),1.65,1.7,shirt)
        rib(m,'forearm_'+side,'fore_'+side,(s*4,18.7,0),(s*4,14.6,0),1.18,1.3,shirt)
        m.cube('hand_'+side,'hand_'+side,(s*4-.67,13.3,-.7),(s*4+.67,15,.7),skin,grain=.01)
        m.cube('trouser_'+side,'leg_'+side,(s*1.25-.84,7.3,-.77),(s*1.25+.84,15,.83),pants,grain=.018)
        m.cube('lower_leg_'+side,'shin_'+side,(s*1.25-.73,boot_height,-.7),(s*1.25+.73,7.7,.76),pants,grain=.018)
        m.cube('boot_'+side,'foot_'+side,(s*1.25-.90,0,-1.5),(s*1.25+.90,boot_height,.9),boots,grain=.012)
        m.cube('boot_sole_'+side,'foot_'+side,(s*1.25-.95,0,-1.56),(s*1.25+.95,.40,.94),BLACK,grain=.01)

# Shared runtime contract: ticks/contact instants supplied by ZombieAuSpec.
ABILITY_CONTRACT = {
 'sweep':(34,[14]),'double_strike':(42,[12,26]),'lunge':(36,[16]),
 'grab':(42,[12,26]),'slam':(44,[22]),'uppercut':(32,[14]),
 'backstep':(36,[12]),'leap':(46,[26]),'volley':(42,[18,24,30]),
 'signature':(54,[24,32]),'rally':(44,[20]),'frenzy':(66,[14,30,46])}

def author_animations(m,height=None,style='claw'):
    """15 native animations. Every ability keys all major joints and secondaries.

    Contract values are ticks; animation seconds = ticks/20. Attack contact keys
    are exact (linear adjacent contact keys avoid Catmull-Rom strike overshoot).
    """
    if m.anims:return
    unit=getattr(m,'unit',(height or 2)/2)
    bones=[n for n in m.groups if n in ('root','body','chest','head','hair','hair_r','hair_l','coat','coat_r','coat_l','arm_r','arm_l','fore_r','fore_l','hand_r','hand_l','leg_r','leg_l','shin_r','shin_l','foot_r','foot_l','weapon','tail','wing_r','wing_l')]
    def pose(kind,strength=1,direction=1):
        d=direction;s=strength
        p={b:(0,0,0) for b in bones}
        if kind=='wind':
            p.update(body=(-9*s,-17*d,4*d),chest=(-12*s,-22*d,5*d),head=(7*s,20*d,-3*d),arm_r=(-45*s,-22*d,-48*s),fore_r=(-48*s,0,-9*s),arm_l=(-25*s,22*d,25*s),fore_l=(-42*s,0,12*s),leg_r=(-21*s,0,8*s),leg_l=(22*s,0,-6*s),shin_r=(35*s,0,0),shin_l=(10*s,0,0),weapon=(-12*s,0,-8*d))
        else:
            p.update(body=(17*s,22*d,-6*d),chest=(22*s,30*d,-9*d),head=(-12*s,-21*d,4*d),arm_r=(92*s,25*d,36*d),fore_r=(-17*s,0,19*d),arm_l=(35*s,-20*d,-35*d),fore_l=(-50*s,0,-8*d),leg_r=(30*s,0,9*s),leg_l=(-28*s,0,-7*s),shin_r=(10*s,0,0),shin_l=(42*s,0,0),foot_l=(-18*s,0,0),weapon=(16*s,0,14*d))
        return p
    def apply_style(p,ability,phase):
        hit=phase=='hit'
        if style in ('gun','medic') and ability in ('volley','signature'):
            p.update(arm_r=(90 if hit else 65,-8,-9),fore_r=(-9 if hit else -28,0,0),arm_l=(75,12,30),fore_l=(-50,0,-27),head=(-3,0,0),weapon=(-8 if hit else 1,0,0),chest=(-5 if hit else 2,0,0))
        if style=='medic' and ability=='rally':p.update(body=(16,0,0),chest=(16,0,0),head=(24,0,0),arm_r=(48,-13,-8),fore_r=(-52,0,0),arm_l=(46,13,8),fore_l=(-63,0,0),leg_r=(-32,0,0),shin_r=(72,0,0))
        if style=='chainsaw':p['weapon']=(9 if hit else -15,0,9 if hit else -8);p['arm_r']=(65 if hit else -42,28 if hit else -15,27 if hit else -24)
        if style=='shield' and ability=='signature':p.update(arm_l=(63,24,34),fore_l=(-112,0,-32),hand_l=(0,0,-10),arm_r=(103 if hit else 34,-16,-15),fore_r=(-20 if hit else -88,0,0),chest=(18 if hit else -8,18 if hit else -16,0),head=(-7,-12,0),weapon=(0,0,0))
        if ability in ('slam','leap'):
            p['arm_r']=(125 if hit else -145,0,-12);p['arm_l']=(95 if hit else -110,0,15);p['chest']=(34 if hit else -22,0,0)
        if ability=='uppercut':p.update(arm_r=(-155 if hit else 15,0,-12),fore_r=(-70 if hit else -100,0,0),chest=(-18 if hit else 25,20 if hit else -12,0),head=(-12 if hit else 10,0,0))
        if ability=='backstep':p.update(chest=(-16 if hit else 15,-14,0),arm_l=(65 if hit else 35,0,42),fore_l=(-100,0,-15),leg_r=(-32,0,0),leg_l=(29,0,0))
        if ability=='grab':p['arm_l']=(105 if hit else 27,20,-15);p['hand_l']=(35 if hit else -20,0,0)
        if ability=='rally' and style!='medic':p.update(arm_l=(-20,0,45),fore_l=(-120,0,-30),head=(12,0,0),body=(8,0,0))
        if style=='gun' and ability in ('volley','signature'):
            p['weapon']=aim_weapon(p,getattr(m,'gun_axis',(0,0,-1)))
        return p
    def make(name,ticks,frames,loop=False):
        tracks={}
        for b in bones:
            keys=[]
            for t,p in frames:keys.append((t/20,*p.get(b,(0,0,0))))
            tracks[b]={'rotation':keys}
        # Root/body translation is actual weight transfer; feet flex around pivots.
        tracks['root']['position']=[(t/20,0, p.get('_pos',(0,0,0))[1]*unit,p.get('_pos',(0,0,0))[2]*unit) for t,p in frames]
        # Cloth/hair drag the prior torso motion rather than moving rigidly.
        for b,factor in [('hair',-.55),('hair_r',-.38),('hair_l',-.45),('coat',-.45),('coat_r',-.35),('coat_l',-.4),('tail',-.6),('wing_r',-.35),('wing_l',-.35)]:
            if b in tracks:
                tracks[b]['rotation']=[(min(ticks,t+1.5)/20,p.get('chest',(0,0,0))[0]*factor,p.get('chest',(0,0,0))[1]*factor, p.get('chest',(0,0,0))[2]*factor) for t,p in frames]
                tracks[b]['rotation'][0]=(0,0,0,0)
        m.anim(name,ticks/20,tracks,loop)
        # Fast strikes use linear interpolation for exact readable contacts.
        for a in m.anims[-1]['animators'].values():
            for k in a['keyframes']:k['interpolation']='linear'
    rest={b:(0,0,0) for b in bones}
    idle=[]
    for i in range(9):
        t=i*10;q=dict(rest);wave=math.sin(i*math.pi/4)
        q.update(chest=(1.6*wave,0,0),head=(-1.2*wave,1.2*wave,0),arm_r=(1.8*wave,0,1),arm_l=(-1.8*wave,0,-1),_pos=(0,.12*wave,0));idle.append((t,q))
    make('idle',80,idle,True)
    walk=[]
    for i in range(9):
        q=dict(rest);v=math.sin(i*math.pi/4);q.update(body=(3,0,2*v),chest=(-2,3*v,0),head=(-2,-3*v,-v),leg_r=(28*v,0,0),leg_l=(-28*v,0,0),shin_r=(max(0,-v)*35,0,0),shin_l=(max(0,v)*35,0,0),foot_r=(-max(0,v)*15,0,0),foot_l=(-max(0,-v)*15,0,0),arm_r=(-18*v,0,-5),arm_l=(18*v,0,5),fore_r=(-10-8*max(0,v),0,0),fore_l=(-10-8*max(0,-v),0,0),_pos=(0,.25*abs(v),0));walk.append((i*3,q))
    make('walk',24,walk,True)
    for index,(name,(duration,contacts)) in enumerate(ABILITY_CONTRACT.items()):
        frames=[(0,rest)]
        for j,t in enumerate(contacts):
            direction=(-1 if j%2 else 1)
            wind=apply_style(pose('wind',1,direction),name,'wind');wind['_pos']=(0,-.8,.25)
            hit=apply_style(pose('hit',1,direction),name,'hit');hit['_pos']=(0,-1.1,-.65)
            if name=='leap':wind['_pos']=(0,3.5,.2);hit['_pos']=(0,-1.4,-1)
            if name=='lunge':hit['_pos']=(0,-.7,-2.1)
            frames.extend([(max(frames[-1][0]+.5,t-7),wind),(t-1,wind),(t,hit),(min(duration-3,t+3),apply_style(pose('hit',.7,direction),name,'hit'))])
        if name=='lunge':
            dash=apply_style(pose('wind',.7),name,'wind');dash['_pos']=(0,-.65,-.5);frames.append((10,dash))
        if name=='leap':
            takeoff=pose('wind',.8);takeoff['_pos']=(0,2,-.5);frames.append((12,takeoff))
        if name=='grab':
            pull=apply_style(pose('hit',.65,-1),name,'hit');pull.update(fore_l=(-110,0,-8),chest=(-14,-20,0),_pos=(0,-.6,.3));frames.extend([(17,pull),(23,pull)])
        if name=='backstep':
            retreat=apply_style(pose('wind',.65),name,'wind');retreat['_pos']=(0,-.3,1.5);frames.extend([(16,retreat),(24,retreat)])
        frames.extend([(duration-4,pose('wind',.22)),(duration,rest)])
        frames=sorted({t:p for t,p in frames}.items())
        make(name,duration,frames)
    fall=pose('hit',.6);fall.update(body=(35,12,18),chest=(37,-8,12),head=(28,0,15),arm_l=(35,0,42),arm_r=(60,0,-25),leg_l=(-40,0,-12),shin_l=(70,0,0),_pos=(0,-5,0))
    down=dict(fall);down.update(root=(0,0,78),body=(38,0,12),head=(24,0,18),_pos=(0,-10,0))
    make('death',40,[(0,rest),(9,fall),(24,down),(40,down)])
