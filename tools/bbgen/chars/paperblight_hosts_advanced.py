"""Host Thavel, uninfected AU Claire and Host Zip, from the supplied 2026-11-24 views.

Native Blockbench geometry, painted with stdlib bbgen; no reference-image textures.
Y up, facing -Z, 16 units per block. Rebuild only these three models by running
this script. The twelve ability names and contact ticks match PaperblightHost.
"""
import itertools
import math
from pathlib import Path
import sys
import uuid

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import bbgen
from bbgen import Model, mix

OUT = Path(__file__).resolve().parents[3] / 'src/main/resources/assets/fpe/bbmodels'
PAPER, WHITE, GREY = 0xDCDDE1, 0xF1F0EF, 0xA6A9B2
INK, PURPLE, EDGE = 0x292534, 0x463B59, 0x62516F
SIDES = (('r', 1), ('l', -1))


def rib(m, name, bone, a, b, width, depth, color, **kw):
    dx, dy, dz = (v-u for u, v in zip(a, b))
    length = math.dist(a, b)
    x, y, z = a
    return m.cube(name, bone, (x-width/2, y-.025, z-depth/2),
                  (x+width/2, y+length+.025, z+depth/2), color,
                  origin=a, rot=(math.degrees(math.asin(dz/length)), 0,
                                 -math.degrees(math.atan2(dx, dy))), grain=.012, **kw)


def solid_poly(m, name, bone, points, z, depth, color, step=.35):
    """Extruded paper silhouette: solid thin slices also visible from side/back."""
    low, high = min(y for x,y in points), max(y for x,y in points)
    n = math.ceil((high-low)/step)
    for j in range(n):
        y = low+j*(high-low)/n
        h = (high-low)/n
        mid = y+h/2
        xs=[]
        for (a,b),(c,d) in zip(points,points[1:]+points[:1]):
            if min(b,d)<=mid<max(b,d):
                xs.append(a+(c-a)*(mid-b)/(d-b))
        xs.sort()
        for k,(a,b) in enumerate(zip(xs[::2],xs[1::2])):
            dep = depth(mid) if callable(depth) else depth
            m.cube(f'{name}_{j}_{k}',bone,(a,y,z-dep/2),(b,y+h+.002,z+dep/2),
                   color,grain=.01,res=2)


def card(m, name, bone, bounds, points, z, color, depth=.35, paint=None):
    x0,y0,x1,y1=bounds
    def painter(reverse=False):
        def f(F):
            F.rect(0,0,F.w,F.h,(0,0,0,0))
            def p(v):
                u=(v[0]-x0)/(x1-x0)
                return ((1-u if reverse else u)*F.w,(y1-v[1])/(y1-y0)*F.h)
            F.poly([p(v) for v in points],color)
            if paint and not reverse: paint(F)
        return f
    fs={f:lambda F:F.rect(0,0,F.w,F.h,(0,0,0,0)) for f in bbgen.FACES}
    fs.update(north=painter(),south=painter(True))
    m.cube(name,bone,(x0,y0,z-depth/2),(x1,y1,z+depth/2),color,faces=fs,grain=0,res=7)


def round_head(m,bone,y,width,height,depth,color):
    for j in range(10):
        t=(j+.5)/10
        half=width/2*math.sqrt(max(.03,1-(t*2-1)**2))
        m.cube(f'head_volume_{j}',bone,(-half,y+height*j/10,-depth/2),
               (half,y+height*(j+1)/10+.01,depth/2),color,grain=.008,res=2)


def spine(m,hip=15,shoulder=23,head=26):
    m.group('root')
    m.group('pelvis',(0,hip,0),parent='root')
    m.group('chest',(0,hip+1,0),parent='pelvis')
    m.group('head',(0,head,0),parent='chest')
    m.group('nape',(0,head+4,1),parent='head')
    m.group('ornament',(0,head+4.7,0),parent='head')
    for side,s in SIDES:
        m.group('hair_'+side,(s*1.7,head+4,-.3),parent='head')
        m.group('thigh_'+side,(s*.9,hip,0),parent='pelvis')
        m.group('shin_'+side,(s*1.05,hip*.52,0),parent='thigh_'+side)
        m.group('foot_'+side,(s*1.15,2.3,0),parent='shin_'+side)


def hand(m,tag,wrist,length=4,color=PURPLE,spread=1):
    """A broad palm and five separate two-joint long digits with tapered tips."""
    side,s=tag,1 if tag=='r' else -1
    bone='hand_'+side
    m.group(bone,wrist,parent='fore_'+side)
    m.group('digits_'+side,(wrist[0]+s*.4,wrist[1]-1,wrist[2]),parent=bone)
    x,y,z=wrist
    m.cube('palm_'+side,bone,(x-1.1,y-length*.50,z-.55),(x+1.1,y+.3,z+.55),color,grain=.012)
    for j in range(4):
        rx=x+(-.82+j*.55)
        p=(rx,y-length*.40,z-.08)
        q=(rx+(j-1.5)*.28*spread,y-length*(.80+(.10 if j in (1,2) else 0)),z-.24)
        tip=(q[0]+(j-1.5)*.22*spread,q[1]-length*.23,z-.48)
        rib(m,f'digit_{side}_{j}','digits_'+side,p,q,.43,.48,color)
        rib(m,f'point_{side}_{j}','digits_'+side,q,tip,.24,.30,color)
    a=(x+s*.85,y-.4,z)
    b=(x+s*1.8,y-1.35,z-.3)
    c=(x+s*2.2,y-2.3,z-.55)
    rib(m,'thumb_'+side,'digits_'+side,a,b,.52,.54,color)
    rib(m,'thumb_tip_'+side,'digits_'+side,b,c,.28,.33,color)


def arm(m,side,s,shoulder,elbow,wrist,white_sleeve=True,claire=False,large=4):
    m.group('arm_'+side,shoulder,parent='chest')
    m.group('fore_'+side,elbow,parent='arm_'+side)
    col=PAPER if claire else PURPLE
    rib(m,'upper_arm_'+side,'arm_'+side,shoulder,elbow,1.25,1.25,col)
    rib(m,'long_forearm_'+side,'fore_'+side,elbow,wrist,1.05 if claire else 1.50,1.2,col)
    if white_sleeve:
        end=tuple(a+(b-a)*.42 for a,b in zip(shoulder,elbow))
        rib(m,'puff_sleeve_'+side,'arm_'+side,shoulder,end,2.30,2.1,PAPER)
    hand(m,side,wrist,large,col,1.4 if not claire else .55)
    if claire:
        x,y,z=wrist
        # Black fingertip silhouette continues the pale sleeve and narrow palm.
        for j in range(4):
            xx=x-.82+j*.55
            rib(m,f'ink_fingertip_{side}_{j}','digits_'+side,
                (xx+(j-1.5)*.15,y-large*.77,z-.23),
                (xx+(j-1.5)*.28,y-large*1.12,z-.48),.30,.33,INK)


def alphabet(letter):
    glyphs={'A':['010','101','111','101','101'],
            'B':['110','101','110','101','110'],
            'C':['011','100','100','100','011']}
    def f(F):
        for yy,row in enumerate(glyphs[letter]):
            for xx,v in enumerate(row):
                if v=='1':F.rect((.25+xx*.17)*F.w,(.17+yy*.13)*F.h,.17*F.w,.13*F.h,0x6C626F)
    return f


def spiral(m,bone,y,color=INK):
    p=[(0,y,0),(-1.2,y+.8,0),(-.8,y+2.0,0),(.6,y+2.0,0),(.6,y+1.2,0),(-.1,y+1.2,0)]
    for j,(a,b) in enumerate(zip(p,p[1:])):rib(m,f'spiral_{j}',bone,a,b,.20,.21,color)


def thavel(m):
    spine(m,15.5,23,26)
    m.group('skirt',(0,16,0),parent='pelvis')
    m.cube('blouse','chest',(-1.65,16,-1),(1.65,23.8,1.1),PAPER,grain=.02)
    m.cube('waistband','pelvis',(-1.85,15.6,-1.15),(1.85,16.35,1.2),GREY)
    m.cube('neck','chest',(-.7,23,-.60),(.7,26.8,.65),0xAAA7B2)
    for s in (-1,1):
        rib(m,'collar_'+str(s),'chest',(s*.65,25.6,-.75),(s*1.3,24.0,-1.12),.95,.22,GREY)
    # Full-depth flared skirt, asymmetric torn openings reaching up into the hem.
    outline=[(-1.7,16),(1.7,16),(6.6,1.4),(2.6,1.2),(2.15,3.6),
             (1.5,1.1),(-.1,1.3),(-.5,5.1),(-1.10,3.6),(-.95,1.4),
             (-3.0,1.3),(-3.45,3.4),(-4.1,1.5),(-6.2,1.8)]
    solid_poly(m,'ragged_skirt','skirt',outline,.55,lambda y:2.2+(16-y)*.17,PAPER,.33)
    for j,x in enumerate((-4.1,-1.8,1.2,3.7)):
        rib(m,'skirt_fold_'+str(j),'skirt',(x*.32,15.4,-.65),
            (x,2.2,-1.84),.13,.13,0xB8B9C2)
    for side,s in SIDES:
        rib(m,'leg_'+side,'thigh_'+side,(s*.85,15.5,0),(s*1.1,2.0,0),.84,.88,GREY)
        m.cube('boot_'+side,'foot_'+side,(s*1.1-.65,0,-1.1),(s*1.1+.65,2.4,.65),INK)
    # Purple arms remain purple all the way to the five enormous claws.
    arm(m,'r',1,(1.6,23.8,0),(5.6,16.5,.1),(8.2,6.8,-.2),large=5.7)
    arm(m,'l',-1,(-1.6,23.8,0),(-7.0,12.2,0),(-13.6,11.0,-.4),large=3.6)
    # The low hanging hand is a giant broad claw, wider than the blouse, rather
    # than the narrow human palm used on the smaller opposite hand.
    claw_ids={uid for uid in m.groups['hand_r']['children']+m.groups['digits_r']['children'] if isinstance(uid,str)}
    for c in m.cubes:
        if c['uuid'] in claw_ids:
            for field in ('from','to','origin'):
                c[field][0]=8.2+(c[field][0]-8.2)*1.8
                c[field][2]=-.2+(c[field][2]+.2)*1.35
    m.groups['digits_r']['origin'][0]=8.2+(m.groups['digits_r']['origin'][0]-8.2)*1.8
    round_head(m,'head',26,5.1,4.8,2.3,INK)
    def cluster(F):
        F.rect(0,0,F.w,F.h,(0,0,0,0))
        cx,cy=F.w*.5,F.h*.5
        rr=F.w*.47
        F.disc(cx,cy,rr,0x351725)
        # Hundreds of tiny annular sockets, never a conventional eye pair/grin.
        for row in range(13):
            for col in range(14):
                x=(col+.5+(row%2)*.43)*F.w/14
                y=(row+.6)*F.h/13
                if ((x-cx)/(rr*.96))**2+((y-cy)/(rr*.94))**2<1:
                    r=F.w*(.021+.004*((col*7+row*3)%3))
                    F.disc(x,y,r,0xB08B91)
                    F.disc(x+.15,y+.12,r*.59,0x170C15)
                    if (row+col)%4==0:F.disc(x,y-r*.2,r*.21,0xE2BEC0)
    m.cube('circular_socket_cluster','head',(-2.35,26.1,-1.41),(2.35,30.8,-1.27),
           INK,faces={'north':cluster},res=14,grain=0)
    m.cube('hair_crown','head',(-2.65,29.9,-.95),(2.65,31.2,1.6),INK)
    for side,s in SIDES:
        for j,(y,w) in enumerate(((30.5,4.1),(28.7,4.0),(27.0,3.4))):
            pts=[(s*1.3,y+.8),(s*2.4,y+1.2),(s*w,y-.4),(s*2.15,y-.3)]
            solid_poly(m,f'hair_spike_{side}{j}','hair_'+side,pts,.35,1.65,INK,.24)
        rib(m,'nape_'+side,'nape',(s*1.7,30.4,1.1),(s*2.3,25.0,1.2),1.2,1.3,INK)
        for j in range(2):
            points=[(s*1.7,31.1-j*.7),(s*3.2,31.8-j*.7),
                    (s*4.0,31.3-j*.7),(s*2.8,30.3-j*.7)]
            solid_poly(m,f'headband_petal_{side}{j}','ornament',points,-.7,.28,PAPER,.2)
    for j,l in enumerate('ABC'):
        x=(j-1)*1.6
        m.cube('headband_'+l,'ornament',(x-.73,30.9,-1.55),(x+.73,32.35,-.4),
               PAPER,faces={'north':alphabet(l)},origin=(x,31.7,-.9),rot=(0,0,(j-1)*-10),res=9)
    spiral(m,'ornament',32.2)


def claire_face(F):
    F.rect(0,0,F.w,F.h,PAPER)
    for s in (-1,1):
        cx=F.w*(.5+s*.225)
        cy=F.h*.46
        rx,ry=F.w*.156,F.h*.34
        # Huge U-shaped dark eye and a white crescent along the curved bottom.
        for y in range(F.h):
            for x in range(F.w):
                u,v=(x-cx)/rx,(y-cy)/ry
                if u*u+v*v<1:F.px(x,y,INK)
                if ((x-cx)/(rx*.78))**2+((y-(cy+ry*.14))/(ry*.78))**2<1:
                    F.px(x,y,WHITE)
                if ((x-cx)/(rx*.49))**2+((y-(cy-ry*.21))/(ry*.80))**2<1:
                    F.px(x,y,0x38333F)
        F.line(cx-rx,cy-ry*.25,cx+s*rx*1.55,cy-ry*.45,INK,1.5)
    F.line(F.w*.40,F.h*.88,F.w*.60,F.h*.88,0x73717B,1.1)


def claire(m):
    spine(m,14.4,22.3,24.9)
    m.cube('pale_blouse','chest',(-1.7,14.0,-.95),(1.7,22.7,1.0),PAPER)
    m.cube('neck','chest',(-.67,22.5,-.55),(.67,25.5,.55),PAPER)
    for s in (-1,1):
        card(m,'pointed_collar_'+str(s),'chest',(-1.45,21.8,1.45,23.3),
             [(s*.05,23.2),(s*1.25,23.1),(s*.8,21.8)],-1.04,WHITE)
    for j in range(2):
        m.cube('blouse_button_'+str(j),'chest',(-.15,21.1-j*.85,-1.08),
               (.15,21.4-j*.85,-1.01),0xA3A4AF,res=6)
    rib(m,'blouse_small_crease','chest',(-.35,18.6,-1.03),(.55,18.0,-1.03),.07,.06,GREY)
    m.cube('shorts_waist','pelvis',(-1.72,12.7,-1),(1.72,14.3,1.05),PAPER)
    for side,s in SIDES:
        x=s*.99
        m.cube('short_pant_'+side,'thigh_'+side,(x-.85,10.9,-.94),(x+.85,13.6,1.02),PAPER)
        rib(m,'pale_thigh_'+side,'thigh_'+side,(x,11.4,0),(s*1.1,7.5,0),1.28,1.28,PAPER)
        rib(m,'long_white_calf_'+side,'shin_'+side,(s*1.1,7.6,0),(s*1.24,1.4,0),1.3,1.30,PAPER)
        m.cube('black_boot_'+side,'foot_'+side,(s*1.24-.84,0,-1.15),(s*1.24+.84,3.0,.78),INK)
        m.cube('folded_boot_cuff_'+side,'shin_'+side,(s*1.13-.94,7.0,-.8),(s*1.13+.94,8.0,.9),0xC4C8D1)
        # White flared folded cuff tails are prominent in the reference.
        pts=[(s*1.1-.98,8.0),(s*1.1+1.15,8.0),(s*1.1+.80,6.70),(s*1.1-.8,6.8)]
        solid_poly(m,'cuff_points_'+side,'shin_'+side,pts,0,.84,0xC6CBD5,.2)
        arm(m,side,s,(s*1.65,22.25,0),(s*2.75,17.0,0),
            (s*3.6,13.7,-.1),white_sleeve=False,claire=True,large=2.45)
    round_head(m,'head',24.4,5.9,5.9,2.3,PAPER)
    m.cube('open_visible_eyes','head',(-2.65,24.7,-1.28),(2.65,29.6,-1.17),
           PAPER,faces={'north':claire_face},res=13,grain=0)
    m.cube('bob_hair_crown','head',(-2.75,29.2,-1.0),(2.75,30.8,1.5),0xD7D9DE)
    m.cube('bob_hair_back','nape',(-2.55,25.0,.95),(2.55,30.3,2.0),0xC7CBD3)
    for side,s in SIDES:
        for j in range(3):
            a=(s*(1.5+j*.52),29.8-j*.35,.55)
            b=(s*(2.6+j*.74),24.0+j*.55,.55-j*.25)
            rib(m,'fanned_bob_'+side+str(j),'hair_'+side,a,b,1.18,1.35,0xD9DBDF if j%2 else 0xCDD0D7)
        # Narrow fringe lies above the U eyes; lower iris/crescent remains exposed.
        a=(s*.60,30.6,-1.42)
        b=(s*1.02,28.25,-1.45)
        rib(m,'central_bang_'+side,'head',a,b,1.10,.56,PAPER)
        rib(m,'side_bang_'+side,'head',(s*1.65,30.15,-1.25),(s*2.85,28.65,-1.25),1.12,.65,PAPER)
        pts=[(s*.0,30.5),(s*.70,31.95),(s*1.65,31.10),(s*1.5,30.5)]
        solid_poly(m,'hair_bow_'+side,'ornament',pts,.25,.85,PAPER,.18)


def zip_face(F):
    F.rect(0,0,F.w,F.h,PAPER)
    for s in (-1,1):
        cx,cy=F.w*(.5+s*.235),F.h*.45+s*F.h*.04
        F.disc(cx,cy,F.w*.128,0x948D86)
        F.disc(cx,cy,F.w*.106,WHITE)
        F.disc(cx+s*.6,cy,F.w*.074,0x75503C)
        F.disc(cx+s*.6,cy,F.w*.046,0x32262A)
        F.disc(cx-F.w*.025,cy-F.h*.04,F.w*.025,WHITE)
        F.line(cx-F.w*.13,cy-F.h*.05,cx+F.w*.13,cy-F.h*.12,0x7F7780,1)
    F.line(.43*F.w,.78*F.h,.57*F.w,.76*F.h,0x9A949A,.8)


def doodles(F):
    c=0xA7A7B3
    F.disc(F.w*.22,F.h*.18,F.w*.106,c)
    F.disc(F.w*.22,F.h*.18,F.w*.093,PAPER)
    F.disc(F.w*.195,F.h*.16,.8,c);F.disc(F.w*.247,F.h*.16,.8,c)
    F.line(F.w*.19,F.h*.20,F.w*.22,F.h*.22,c,1)
    F.line(F.w*.22,F.h*.22,F.w*.25,F.h*.20,c,1)
    p=[(.44,.11),(.61,.11),(.67,.23),(.48,.23),(.44,.11),(.44,.27),(.63,.27),(.67,.23)]
    for (a,b),(x,y) in zip(p,p[1:]):F.line(a*F.w,b*F.h,x*F.w,y*F.h,c,1)
    for sx in (-1,1):
        for sy in (-1,1):
            F.disc((.82+sx*.034)*F.w,(.17+sy*.025)*F.h,F.w*.037,c)
            F.disc((.82+sx*.034)*F.w,(.17+sy*.025)*F.h,F.w*.027,PAPER)
    for a,b,x,y in [(.27,.50,.63,.68),(.63,.68,.65,.59),(.65,.59,.27,.50)]:
        F.line(a*F.w,b*F.h,x*F.w,y*F.h,c,1.15)


def equation(F):
    # Readable handwritten 2+2=8 on the projecting white fringe.
    glyph={'2':['111','001','111','100','111'], '+':['000','010','111','010','000'],
           '=':['000','111','000','111','000'],'8':['111','101','111','101','111']}
    for i,ch in enumerate('2+2=8'):
        for y,row in enumerate(glyph[ch]):
            for x,v in enumerate(row):
                if v=='1':F.rect(F.w*(.18+i*.13+x*.027),F.h*(.12+y*.1),max(1,F.w*.026),max(1,F.h*.08),0x77727E)


def zip_host(m):
    spine(m,13.5,22.0,26.0)
    m.group('tunic',(0,14,0),parent='pelvis')
    points=[(-1.5,22.6),(1.5,22.6),(2.0,16),(3.5,11.1),(-3.5,11.1),(-2.0,16)]
    solid_poly(m,'white_tunic_volume','tunic',points,0,2.0,PAPER)
    card(m,'shirt_doodles','chest',(-5.8,12,5.8,24.0),
         [(-5.8,23.5),(-1.6,23.1),(0,23.8),(1.6,23.1),(5.8,23.5),
          (3.5,20.5),(2,20.0),(1.7,17.0),(3.2,12),(-3.2,12),(-1.7,17),(-2,20),(-3.5,20.5)],
         -1.08,PAPER,.22,doodles)
    m.cube('neck','chest',(-.65,22.0,-.6),(.65,26.6,.6),PAPER)
    for side,s in SIDES:
        rib(m,'purple_thigh_'+side,'thigh_'+side,(s*.9,13.6,0),(s*1.3,6.8,0),1.2,1.2,PURPLE)
        m.cube('tall_boot_'+side,'shin_'+side,(s*1.3-.93,1.4,-.88),(s*1.3+.93,7.3,.93),PURPLE)
        m.cube('boot_fold_'+side,'shin_'+side,(s*1.3-1.1,5.3,-1.0),(s*1.3+1.1,6.05,1.05),EDGE)
        m.cube('boot_fold_top_'+side,'shin_'+side,(s*1.3-1.02,7.1,-.98),(s*1.3+1.02,7.8,1.0),0x50465E)
        m.cube('dark_boot_foot_'+side,'foot_'+side,(s*1.3-1.0,0,-1.45),(s*1.3+1.0,2.0,.95),PURPLE)
        arm(m,side,s,(s*2.0,22.0,0),(s*7.5,15.7,0),(s*13.4,12.6,-.1),large=4.6)
        wing='wing_'+side
        m.group(wing,(s*1.6,22.0,1.2),parent='chest')
        # Paired BAT wings, each with three pointed scallops and white inner web.
        outline=[(2.0,22.3),(8.0,29.1),(32.55,28.0),(23.2,24.8),
                 (23.5,19.3),(17.0,21.9),(13.4,17.3),(10.5,22.0),(5.4,19.0)]
        white=[(6.0,23.1),(9.3,27.5),(27.6,27.0),(21.7,24.1),
               (21.6,21.4),(17.0,23.2),(13.8,19.6),(11.4,23.4),(7.0,21.4)]
        solid_poly(m,'purple_bat_wing_'+side,wing,[(s*x,y) for x,y in outline],2.1,.80,PURPLE,.28)
        solid_poly(m,'white_wing_web_'+side,wing,[(s*x,y) for x,y in white],1.62,.15,0xD4D6DF,.25)
        solid_poly(m,'white_wing_back_'+side,wing,[(s*x,y) for x,y in white],2.58,.13,0xC7C9D5,.25)
        rib(m,'wing_structural_rib_'+side,wing,(s*4,22.4,1.55),(s*11.5,27.8,1.55),.85,.55,EDGE)
    round_head(m,'head',25.3,5.6,4.8,2.3,PAPER)
    m.cube('brown_round_eyes','head',(-2.5,25.6,-1.3),(2.5,29.6,-1.2),PAPER,
           faces={'north':zip_face},res=11,grain=0)
    for side,s in SIDES:
        col=PURPLE if s==1 else PAPER
        m.cube('half_crown_'+side,'head',tuple(sorted((s*.02,s*2.65)))[:1]+(29.35,-.85),
               tuple(sorted((s*.02,s*2.65)))[1:]+(31.15,1.55),col)
        for j in range(3):
            rib(m,'split_hair_'+side+str(j),'hair_'+side,
                (s*(1.5+j*.35),30.0-j*.35,.65),(s*(2.7+j*.7),25.2+j*.8,.6),
                1.1,1.35,col)
    solid_poly(m,'black_fringe','head',[(0,31.1),(0,29.4),(2.8,28.4),(3.5,29.8),(2.3,31.4)],-.9,.75,PURPLE,.18)
    points=[(0,31.2),(1.2,30.2),(-7.5,28.2),(-6.0,30.0),(-1.8,31.8)]
    solid_poly(m,'long_white_sideways_fringe','head',points,-1.1,.9,PAPER,.18)
    card(m,'fringe_equation','head',(-6.4,28.9,-.3,31.6),
         [(-6.4,29.5),(-.3,31.6),(-.3,29.4),(-5.8,28.9)],-1.59,PAPER,.12,equation)
    spiral(m,'ornament',31.1,PURPLE)
    # Long rear WHITE arm appendage/tail ends in five clearly separate fingers.
    m.group('tail',(0,14.8,1.3),parent='pelvis')
    m.group('tail_tip',(-4.4,6.2,2.5),parent='tail')
    path=[(0,14.8,1.5),(-2.5,12.3,2.5),(-3.0,8.5,2.8),(-4.4,6.2,2.5)]
    for j,(a,b) in enumerate(zip(path,path[1:])):rib(m,'white_rear_arm_'+str(j),'tail',a,b,1.05,1.00,PAPER)
    rib(m,'rear_hand_palm','tail_tip',path[-1],(-5.6,5.0,2.3),1.50,.9,PAPER)
    for j in range(5):
        a=(-5.3+(j-2)*.32,5.2,2.3)
        b=(-6.3+(j-2)*.65,3.5-(j%2)*.3,2.0)
        c=(b[0]-.7,b[1]-1.1,1.7)
        rib(m,'rear_digit_'+str(j),'tail_tip',a,b,.35,.38,PAPER)
        rib(m,'rear_tip_'+str(j),'tail_tip',b,c,.22,.26,PAPER)


# Body pitch/yaw/roll, face pitch/yaw/roll, drop, stride, and bilateral gestures.
GESTURES={
 'rest':(0,0,0,0,0,0), 'ready':(12,8,9,-10,9,10),
 'wind':(-30,-24,40,-15,-20,8), 'cut':(81,28,-18,22,25,35),
 'open':(-12,-17,4,-15,-25,-18), 'reach':(69,7,-3,12,7,10),
 'clutch':(57,18,33,25,20,72), 'raise':(38,-65,10,-35,8,5),
 'slam':(87,20,-20,25,18,32), 'shield':(55,-42,57,8,-16,35),
 'low':(2,15,-22,10,-12,5), 'upperwind':(-17,20,70,10,-12,28),
 'upper':(80,-47,18,-35,8,30), 'recoil':(-30,-28,22,0,-9,-9),
}
POSES={
 'rest':((0,0,0),(0,0,0),0,0,'rest','rest',0),
 'watch':((-3,6,2),(2,-8,-3),.2,7,'ready','low',0),
 'wind_r':((7,-32,10),(4,22,-8),1.1,22,'ready','wind',-15),
 'cut_r':((-16,35,-9),(6,-22,7),1.0,-22,'low','cut',15),
 'wind_l':((8,29,-10),(4,-20,7),1.1,-22,'wind','ready',-15),
 'cut_l':((-16,-35,9),(6,20,-7),1,22,'cut','low',15),
 'coil':((-14,-8,4),(-4,7,-3),2.4,16,'shield','ready',-28),
 'thrust':((-22,14,-5),(13,-13,2),.8,-30,'low','reach',12),
 'take':((-17,0,1),(7,0,-2),.9,-16,'reach','reach',8),
 'hold':((-8,1,-2),(-4,1,1),1.2,-8,'clutch','clutch',-5),
 'tear':((13,-25,9),(-7,17,-4),1.4,23,'clutch','cut',20),
 'overhead':((13,3,-2),(14,-4,2),1.5,4,'raise','raise',-24),
 'impact':((-31,2,1),(-12,-2,2),2.4,-8,'slam','slam',19),
 'upperwind':((-12,-24,9),(-3,13,-3),2.5,22,'shield','upperwind',-20),
 'upper':((14,30,-5),(-12,-12,6),.2,-20,'low','upper',23),
 'backwind':((6,37,-9),(2,-23,5),1,-18,'ready','shield',-12),
 'backhit':((-12,-39,12),(6,18,-6),.7,22,'low','cut',15),
 'launch':((-15,0,0),(10,0,0),2.5,33,'recoil','raise',-32),
 'air':((9,6,-6),(-3,-6,3),-.7,48,'raise','open',36),
 'land':((-27,0,1),(7,0,1),2.8,-20,'slam','reach',18),
 'fanwind':((5,-16,5),(3,16,-4),1.0,14,'shield','clutch',-16),
 'release':((-7,15,-3),(0,-15,2),.5,-12,'open','cut',31),
 'charge':((-10,0,1),(-14,0,0),1.4,0,'shield','shield',-27),
 'laser':((8,0,0),(-4,0,0),.35,0,'open','open',29),
 'recoil':((12,0,2),(-6,0,-1),.7,-4,'recoil','recoil',22),
 'guard':((-8,0,0),(-8,0,0),1.5,0,'shield','shield',-37),
 'burst':((12,0,0),(5,0,0),.2,0,'open','open',38),
 'spent':((-13,7,5),(-9,-9,-5),2,12,'low','low',-12),
}
ACTIONS={
 'sweep':(34,[(6,'wind_r'),(11,'wind_r'),(14,'cut_r'),(21,'spent'),(28,'watch')]),
 'double_cut':(40,[(6,'wind_r'),(12,'cut_r'),(19,'wind_l'),(26,'cut_l'),(32,'spent')]),
 'lunge':(36,[(6,'coil'),(10,'coil'),(16,'thrust'),(20,'thrust'),(26,'spent')]),
 'grasp':(42,[(6,'coil'),(12,'take'),(16,'hold'),(23,'hold'),(26,'tear'),(34,'spent')]),
 'slam':(40,[(6,'coil'),(13,'overhead'),(17,'overhead'),(20,'impact'),(26,'impact'),(34,'spent')]),
 'uppercut':(32,[(6,'upperwind'),(11,'upperwind'),(14,'upper'),(20,'upper'),(26,'spent')]),
 'backhand':(30,[(5,'backwind'),(9,'backwind'),(12,'backhit'),(17,'backhit'),(24,'spent')]),
 'leap_strike':(44,[(7,'coil'),(12,'launch'),(17,'air'),(21,'air'),(24,'land'),(31,'impact'),(37,'spent')]),
 'shard_fan':(36,[(6,'fanwind'),(13,'fanwind'),(16,'release'),(19,'fanwind'),(22,'release'),(28,'spent')]),
 'eye_ray':(52,[(8,'charge'),(17,'charge'),(23,'charge'),(24,'laser'),(28,'recoil'),(32,'laser'),(38,'recoil'),(45,'spent')]),
 'guard_pulse':(44,[(7,'guard'),(17,'guard'),(21,'guard'),(22,'burst'),(28,'burst'),(36,'spent')]),
 'frenzy':(60,[(5,'wind_r'),(12,'cut_r'),(20,'wind_l'),(28,'cut_l'),(36,'overhead'),(43,'overhead'),(44,'impact'),(51,'spent')]),
}


def full_pose(m,key):
    body,face,drop,stride,left,right,wing=POSES[key]
    pitch,yaw,roll=body
    pose={'chest':body,'head':face,'pelvis':(-drop*2,-yaw*.20,-roll*.25),
          'nape':(-pitch*.5,-yaw*.25,-roll*.5),'ornament':(-pitch*.23,0,-roll*.4)}
    for side,s in SIDES:
        pose['hair_'+side]=(-pitch*.5,-yaw*.25,-roll*.5+s*drop)
        pose['thigh_'+side]=(s*stride+drop*7,0,s*drop)
        pose['shin_'+side]=(-drop*12-max(0,s*stride)*.42,0,0)
        pose['foot_'+side]=(drop*4-s*stride*.4,0,0)
        a,b,c,d,e,f=GESTURES[right if s==1 else left]
        pose['arm_'+side]=(a,s*yaw*.10,s*b)
        pose['fore_'+side]=(c,s*d,s*e)
        pose['hand_'+side]=(-c*.10,s*f*.20,s*e*.5)
        pose['digits_'+side]=(0,s*f,f*.12)
        if 'wing_'+side in m.groups:pose['wing_'+side]=(pitch*.12,s*wing,s*wing*.15)
    if 'skirt' in m.groups:pose['skirt']=(-pitch*.30,-yaw*.12,-roll*.35)
    if 'tunic' in m.groups:pose['tunic']=(-pitch*.3,0,-roll*.3)
    if 'tail' in m.groups:
        pose['tail']=(-pitch*.4,-yaw*.38,-roll*.7)
        pose['tail_tip']=(drop*5,-yaw*.25,roll*.8)
    return pose,(roll*.04,-drop,pitch*.03)


def track(tr,bone,ch,t,v):
    tr.setdefault(bone,{}).setdefault(ch,[]).append((t/20,*(round(x,3) for x in v)))


def animations(m,scale,kind):
    for walking in (False,True):
        tr={};length=28 if walking else 80
        for j in range(9):
            p=math.pi*j/4;t=length*j/8
            w=math.sin(p)
            for bone,value in full_pose(m,'rest')[0].items():
                value=(0,0,0)
                if bone=='chest':value=((-4 if walking else 0)+1.5*math.sin(2*p),3*w,1.5*math.cos(p))
                elif bone=='head':value=(1.7*math.cos(2*p),-2*w,-1.5*math.cos(p))
                elif bone.startswith('thigh_'):value=((1 if bone.endswith('r') else -1)*w*(28 if walking else .5),0,0)
                elif bone.startswith('shin_'):value=(-max(0,(1 if bone.endswith('r') else -1)*w)*(30 if walking else 0),0,0)
                elif bone.startswith('foot_'):value=((1 if bone.endswith('r') else -1)*w*(-15 if walking else 0),0,0)
                elif bone.startswith('arm_'):value=(-w*(9 if walking else 1.5)*(1 if bone.endswith('r') else -1),0,1.5*math.cos(p-.4))
                elif bone.startswith('fore_'):value=(2*math.sin(p-.5),0,1.5*w)
                elif bone.startswith('wing_'):value=(0,(1 if bone.endswith('r') else -1)*3*w,1.4*math.cos(p))
                elif bone.startswith(('hair_','nape','ornament','skirt','tunic','tail')):value=(-1.8*math.sin(p-.5),1.4*w,1.9*math.cos(p-.4))
                elif bone.startswith('hand_'):value=(1.5*math.sin(p-.7),0,1.4*w)
                elif bone.startswith('digits_'):value=(0,2.5*math.sin(p-.9),0)
                track(tr,bone,'rotation',t,value)
            track(tr,'pelvis','position',t,(0,(-.30*(1-math.cos(2*p)) if walking else .10*w)*scale,0))
        m.anim('walk' if walking else 'idle',length/20,tr,True)
    for name,(length,beats) in ACTIONS.items():
        tr={}
        for t,key in [(0,'rest'),*beats,(length,'rest')]:
            pose,move=full_pose(m,key)
            if kind=='claire' and name=='eye_ray':
                # Both enormous U eyes remain visible: no bar, glow, or hand in front.
                pose['head']=(-4 if key in ('laser','recoil') else -11,0,0)
                if key in ('charge','laser','recoil'):
                    pose['arm_r']=(-12,0,-25);pose['arm_l']=(-12,0,25)
                    pose['fore_r']=(5,0,0);pose['fore_l']=(5,0,0)
                    pose['thigh_r']=(8,0,8);pose['thigh_l']=(-8,0,-8)
                    pose['shin_r']=(-10,0,0);pose['shin_l']=(-10,0,0)
            for bone,value in pose.items():
                lag=2 if bone.startswith(('hair_','nape','ornament','skirt','tunic','tail')) and 0<t<length else 0
                track(tr,bone,'rotation',min(length,t+lag),value)
            track(tr,'pelvis','position',t,tuple(v*scale for v in move))
        if name=='leap_strike':
            for t,y in [(0,0),(9,-.7),(12,0),(17,4.7),(21,2.3),(24,0),(29,-.4),(length,0)]:
                track(tr,'root','position',t,(0,y*scale,0))
        m.anim(name,length/20,tr)
    tr={}
    for t,key in [(0,'rest'),(5,'recoil'),(12,'guard'),(20,'spent'),(28,'impact'),(40,'spent')]:
        for bone,v in full_pose(m,key)[0].items():track(tr,bone,'rotation',t,v)
    for t,x,y in [(0,0,0),(10,0,-.7),(17,18,-1.0),(24,61,-.3),(29,86,1.5),(34,80,1.7),(40,83,1.8)]:
        track(tr,'root','rotation',t,(x,0,4))
        track(tr,'root','position',t,(0,y*scale,0))
    m.anim('death',2,tr)


def make(name,builder,height,kind):
    serial=itertools.count()
    bbgen.u=lambda:str(uuid.uuid5(uuid.NAMESPACE_URL,f'fpe/{name}/{next(serial)}'))
    m=Model(name,S=4,atlas=1024)
    builder(m)
    # Highest ornament defines the stated full model height, excluding death poses.
    # Cube rotations are kept; the design heights include the rotated rib ends.
    design={'host_thavel':34.4,'paperblight_claire':31.95,'host_zip':33.15}[name]
    scale=height*16/design
    if name=='host_zip':
        wing_ids={uid for side,s in SIDES for uid in m.groups['wing_'+side]['children']}
        wing_cubes=[c for c in m.cubes if c['uuid'] in wing_ids]
        extent=max(abs(c[field][0]) for c in wing_cubes for field in ('from','to'))
        factor=2.2*16/(2*extent*scale)
        for c in wing_cubes:
            for field in ('from','to','origin'):c[field][0]*=factor
        for side,s in SIDES:m.groups['wing_'+side]['origin'][0]*=factor
    for group in m.groups.values():group['origin']=[round(x*scale,5) for x in group['origin']]
    for cube in m.cubes:
        for field in ('from','to','origin'):cube[field]=[round(x*scale,5) for x in cube[field]]
    animations(m,scale,kind)
    m.save(OUT/(name+'.bbmodel'))
    print(name, len(m.cubes),'cubes;',len(m.groups),'bones;',len(m.anims),'animations;',height,'blocks')


if __name__=='__main__':
    make('host_thavel',thavel,2.7,'thavel')
    make('paperblight_claire',claire,1.8,'claire')
    make('host_zip',zip_host,2.2,'zip')
