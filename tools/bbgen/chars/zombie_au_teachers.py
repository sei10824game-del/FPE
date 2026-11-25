"""Seven survivors from the supplied FPE Zombie AU lineup.

Rebuild with python tools/bbgen/chars/zombie_au_teachers.py. Painted atlas and
solid native 3D geometry only; reference pixels are never imported.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from zombie_au_common import *

def poly(m,n,b,pts,z,depth,c):solid_poly(m,n,b,pts,z,depth,c,step=.35)

def cross(m,name,b,x,y,z,c=GOLD,size=1):
    m.cube(name+'_upright',b,(x-size*.25,y-size,z-.08),(x+size*.25,y+size,z+.08),c,grain=0)
    m.cube(name+'_crossbar',b,(x-size,y-size*.25,z-.09),(x+size,y+size*.25,z+.09),c,grain=0)

def seam(m,name,b,a,bp,c=DARK,w=.09):rib(m,name,b,a,bp,w,.08,c)

def collar(m,c=PAPER):
    for s in [-1,1]:
        poly(m,'pointed_collar_'+str(s),'chest',[(s*.45,24.7),(s*2.25,23.2),(s*.85,21.5)],-1.27,.35,c)
    m.cube('black_necktie','chest',(-.32,19.8,-1.52),(.32,23.5,-1.33),INK,grain=.01)
    poly(m,'tie_tip','chest',[(-.32,20.1),(.32,20.1),(0,19.3)],-1.43,.2,INK)

def buttons(m,start=17,end=22,c=GOLD):
    for i in range(start,end,2):m.cube('front_button_'+str(i),'chest',(-.12,i,-1.39),(.12,i+.25,-1.22),c,grain=0)

def hair(m,color=INK,length=24,spiky=False):
    # Round, volumetric scalp; locks overlap in depth and break the silhouette.
    m.cube('rear_hair_mass','hair',(-2.55,26.4,.65),(2.55,30.6,2.0),color,grain=.014)
    m.cube('hair_crown','hair',(-2.35,29.4,-1.1),(2.35,31.4,1.6),color,grain=.014)
    for s in [-1,1]:
        pts=[(s*.65,31.1),(s*2.8,30.6),(s*3.35,28.0),(s*2.7,length),(s*1.8,length+1.9),(s*2,28.7)]
        poly(m,'side_hair_'+str(s),'hair_r' if s>0 else 'hair_l',pts,.55,2.5,color)
    for i,(x,end) in enumerate([(-2.1,27.5),(-1.2,28.0),(-.3,27.2),(.65,28.2),(1.6,28.4)]):
        poly(m,'pointed_fringe_'+str(i),'hair',[(x-.7,30.8),(x+.9,30.8),(x+.2,end)],-1.57,.6,color)
    if spiky:
        for i,(a,b,c) in enumerate([((-2,30),(-4,31),(-2.4,28.3)),((-1.5,30.3),(-2.1,32),(0,30.2)),((.1,30.5),(1.7,32),(1.8,29.9)),((1.7,30),(4,30.8),(2.4,28.4)),((-2.2,28),(-4,27.4),(-2.1,26.3))]):poly(m,'hair_spike_'+str(i),'hair',[a,b,c],.25,2.4,color)

def coat(m,c=PAPER,length=7,width=3.6):
    for side,s in [('r',1),('l',-1)]:
        pts=[(s*.5,18.7),(s*2.35,19),(s*width,length+1),(s*1.8,length),(s*.5,length+2)]
        poly(m,'coat_tail_'+side,'coat_'+side,pts,.6,1.85,c)
        seam(m,'coat_seam_'+side,'coat_'+side,(s*1.1,18,-.39),(s*(width-.4),length+1.6,-.39),GREY)
        m.cube('coat_pocket_'+side,'chest',(s*1.55-.52,17.9,-1.34),(s*1.55+.52,19.1,-1.22),GREY,grain=.015)

def wrap(m,b,x,y,length=3,width=1.6):
    for j in range(5):
        yy=y-j*length/5
        m.cube('wrap_'+b+'_'+str(j),b,(x-width/2,yy-.35,-.83),(x+width/2,yy+.13,.83),GREY,grain=.018)
        seam(m,'wrap_seam_'+b+'_'+str(j),b,(x-width/2,yy-.19,-.90),(x+width/2,yy-.19,-.90),DARK,.05)

def medkit(m,b='hand_l',x=-4,y=11):
    m.cube('medical_case',b,(x-1.65,y-1.2,-.8),(x+1.65,y+1.2,.85),GREY,grain=.015)
    m.cube('case_front',b,(x-1.45,y-1,-.94),(x+1.45,y+1,-.81),PAPER,grain=.01)
    m.cube('case_handle_top',b,(x-.6,y+1.7,-.2),(x+.6,y+1.9,.25),INK,grain=0)
    for s in [-1,1]:m.cube('case_handle_'+str(s),b,(x+s*.55-.1,y+1.1,-.2),(x+s*.55+.1,y+1.8,.25),INK,grain=0)
    cross(m,'medical_case_mark',b,x,y,-1.0,GOLD,.72)
    for s in [-1,1]:m.cube('case_latch_'+str(s),b,(x+s*1.05-.12,y+.8,-1.04),(x+s*1.05+.12,y+1.2,-.88),DARK,grain=0)

def grace():
    m=Rig('survivor_grace',2.4,'gun');limbs(m,shirt=DARK,pants=INK,boots=INK)
    m.gun_axis=(0,1,0)  # Raised barrel in the authored rest geometry.
    head(m);face(m,bandage=True);hair(m,GREY,length=22.5,spiky=True)
    # Leave room for the officer cap above the sharp fringe.
    for e in m.cubes:
        if e['name'].startswith('hair_spike_'):
            for key in ['from','to','origin']:e[key][1]-=.8*m.unit
    # Sweeping grey jacket, open dark centre and pointed gold lapel badges.
    for s in [-1,1]:
        poly(m,'jacket_lapel_'+str(s),'chest',[(s*.4,24.3),(s*2.9,23.5),(s*2.2,18.1),(s*.5,19.8)],-1.36,.50,GREY)
        poly(m,'shoulder_panel_'+str(s),'arm_r' if s>0 else 'arm_l',[(s*2.5,23.8),(s*4.3,22.9),(s*4.6,20),(s*3.1,20.5)],0,2.1,GREY)
    coat(m,DARK,7,4.1);collar(m,PAPER)
    for x,y in [(1.7,22),(-3.45,21)]:
        poly(m,'gold_authority_badge_'+str(x),'chest' if x>0 else 'arm_l',[(x-.6,y+.8),(x+.7,y+.5),(x+.35,y-.9),(x-.55,y-.5)],-1.75,.25,GOLD)
        seam(m,'badge_ink_'+str(x),'chest' if x>0 else 'arm_l',(x,y-.45,-1.94),(x,y+.48,-1.94),DARK,.12)
    m.cube('officer_hat_brim','head',(-3,30.55,-1.9),(3,30.9,1.9),DARK,grain=.01)
    poly(m,'officer_hat_crown','head',[(-2.3,30.8),(-2,32),(1.9,32),(2.4,30.8)],.1,2.9,INK)
    m.cube('hat_band','head',(-2.2,30.95,-1.49),(2.2,31.35,-1.34),MINT,grain=.01)
    poly(m,'hat_badge','head',[(-.5,31.9),(.5,31.9),(.3,31.3),(0,31.1),(-.3,31.3)],-1.57,.2,GREY)
    # Solid pistol: receiver, thick barrel, sight, trigger guard and grip.
    m.cube('pistol_grip','weapon',(3.5,14.2,-.6),(4.4,16.6,.55),INK,rot=(0,0,-12),origin=(4,15,0),grain=.015)
    m.cube('pistol_receiver','weapon',(3.25,16,-1),(4.65,18.8,.65),DARK,grain=.012)
    m.cube('pistol_barrel','weapon',(3.65,18.4,-.75),(4.25,21.7,.1),MINT,grain=.01)
    m.cube('barrel_muzzle','weapon',(3.78,21.68,-.62),(4.12,21.85,-.02),INK,grain=0)
    m.cube('pistol_front_sight','weapon',(3.8,21,-.98),(4.1,21.5,-.7),INK,grain=0)
    for x in [3.1,4.55]:m.cube('trigger_guard_'+str(x),'weapon',(x,15.8,-1.25),(x+.25,17,-.9),INK,grain=0)
    m.cube('trigger_guard_base','weapon',(3.1,15.7,-1.25),(4.8,16,-.9),INK,grain=0)
    # Present the gun outside the forearm silhouette, connected to the hand.
    weapon_ids=set(m.groups['weapon']['children'])
    for e in m.cubes:
        if e['uuid'] in weapon_ids:
            for key in ['from','to','origin']:
                e[key][0]+=1.7*m.unit;e[key][2]-=.5*m.unit
    rib(m,'pistol_grip_bridge','weapon',(4,14.6,-.2),(5.7,15.1,-.5),.8,1.05,INK)
    return m

def demi():
    m=Rig('survivor_demi',2.1,'medic');limbs(m,shirt=PAPER,pants=INK,boots=INK)
    head(m);face(m);hair(m,PAPER,length=24,spiky=True);coat(m,PAPER,7.4,4)
    for e in m.cubes:
        if e['name'].startswith('hair_spike_'):
            for key in ['from','to','origin']:e[key][1]-=.8*m.unit
        elif e['name']=='hair_crown':e['to'][1]-=.6*m.unit
    collar(m,WHITE);buttons(m,c=GREY)
    # Distinct gold rectangular glasses and white crossed hair ornaments.
    for s in [-1,1]:
        x=s*1.05
        for y in [27.35,28.45]:m.cube('glasses_h_'+str(s)+str(y),'head',(x-.85,y,-1.91),(x+.85,y+.17,-1.71),GOLD,grain=0)
        for xx in [x-.85,x+.68]:m.cube('glasses_v_'+str(xx),'head',(xx,27.35,-1.91),(xx+.17,28.6,-1.71),GOLD,grain=0)
        poly(m,'hair_rod_'+str(s),'head',[(s*.9,30.3),(s*2.3,32),(s*2.6,32),(s*1.2,30.2)],.1,.45,GREY)
        rib(m,'hair_rod_cross_'+str(s),'head',(s*1.6,30.7,-.15),(s*2.3,31.4,.5),.35,.35,PAPER)
    m.cube('glasses_bridge','head',(-.25,27.9,-1.92),(.25,28.06,-1.7),GOLD,grain=0)
    m.cube('doctor_face_mask','head',(-1.65,25.7,-1.82),(1.65,27,-1.61),MINT,grain=.015)
    for i in range(3):seam(m,'mask_pleat_'+str(i),'head',(-1.45,25.9+i*.35,-1.9),(1.45,25.9+i*.35,-1.9),GREY,.06)
    medkit(m);wrap(m,'fore_r',4,18.2,2.8,1.55)
    cross(m,'coat_medical_mark','chest',1.5,21,-1.3,MINT,.42)
    return m

def sasha():
    m=Rig('survivor_sasha',2,'medic');limbs(m,shirt=GREY,pants=INK,boots=GREY,boot_height=7.4)
    head(m);face(m);hair(m,INK,length=24,spiky=False)
    collar(m,PAPER);buttons(m,c=DARK)
    m.cube('medical_waistband','body',(-2.6,14.8,-1.25),(2.6,15.5,1.3),MINT,grain=.01)
    poly(m,'medical_apron','coat',[(-1.85,16),(1.85,16),(2.1,12.7),(0,13.7),(-2.1,12.7)],-.4,1.8,PAPER)
    # Left-eye medical plus is a silhouette feature, raised above the face.
    cross(m,'large_eye_patch','head',-1,27.9,-2.05,GOLD,1.25)
    m.cube('eye_patch_strap','head',(-2.5,27.7,-1.65),(2.5,28.05,1.61),DARK,grain=0)
    cross(m,'large_eye_patch_front','head',-1,27.9,-2.2,GOLD,1.2)
    m.cube('nurse_cap_base','head',(-2.6,30,-1.5),(2.6,30.65,1.5),DARK,grain=.01)
    poly(m,'nurse_cap','head',[(-2.5,30.5),(-1.3,32),(1.8,31.65),(2.6,30.5)],-.1,2.8,MINT)
    cross(m,'cap_cross','head',.7,31.1,-1.58,GOLD,.37)
    # Segment the high armour boots and add rigid front/shin plates.
    for side,s in [('r',1),('l',-1)]:
        x=s*1.25
        for j in range(3):
            m.cube('armour_plate_'+side+str(j),'shin_'+side,(x-.78,1.3+j*1.9,-.94),(x+.78,2.9+j*1.9,-.75),MINT,grain=.01)
        for xx in [x-.83,x+.68]:m.cube('boot_vertical_trim_'+str(xx),'shin_'+side,(xx,.7,-.99),(xx+.15,7.5,-.83),DARK,grain=0)
    medkit(m,x=-4,y=11.5)
    return m

def thavel():
    m=Rig('survivor_thavel',2.6,'claw');limbs(m,shirt=GREY,pants=INK,boots=INK,skin=PAPER)
    head(m);face(m,bandage=True);hair(m,INK,length=24,spiky=True)
    # Grey hood/eye mask and a wide mint-grey poncho over a ragged skirt.
    m.cube('eye_mask','head',(-2.2,27,-1.87),(2.2,28.55,-1.65),DARK,grain=.012)
    for s in [-1,1]:seam(m,'mask_eye_'+str(s),'head',(s*.5,27.8,-1.95),(s*1.55,27.85,-1.95),PAPER,.13)
    for s in [-1,1]:poly(m,'hood_fold_'+str(s),'head',[(s*.3,31.8),(s*2.7,30.5),(s*2.7,28.6),(s*1.3,30.2)],.05,3.3,GREY)
    poly(m,'broad_poncho','coat',[(-1.3,24.8),(1.3,24.8),(4.4,20.8),(3.2,16.2),(0,17.5),(-3.3,16.1),(-4.5,20.8)],0,2.6,MINT)
    poly(m,'neckline','chest',[(-1.3,24.8),(1.3,24.8),(.9,22.5),(0,21.6),(-.9,22.5)],-1.55,.35,GREY)
    poly(m,'ragged_skirt','coat',[(-2.6,16.7),(2.6,16.7),(5.2,4.3),(3.8,4.5),(3.2,6),(2.6,3.8),(1.4,4),(1.1,6),(.1,4.3),(-1.2,4.6),(-1.8,3.9),(-2.8,4.2),(-3.4,6),(-4.1,4.6),(-4.9,4.2)],.25,3.5,GREY)
    m.cube('waist_belt','body',(-2.8,15.9,-1.75),(2.8,16.7,1.8),DARK,grain=.01)
    m.cube('belt_buckle','body',(-.65,15.85,-1.95),(.65,16.8,-1.76),GOLD,grain=0)
    # One enormous black skeletal claw. Palm and five separate hooked digits.
    m.cube('giant_claw_palm','hand_r',(3.0,12.8,-1.0),(6.1,16.5,1.0),INK,grain=.014)
    for i in range(4):
        x=3.3+i*.82;tipx=x+(i-1.5)*.55
        rib(m,'claw_digit_'+str(i),'hand_r',(x,13.7,-.15),(tipx,10.2-(1 if i in [1,2] else 0),-.4),.62,.68,INK)
        rib(m,'claw_hook_'+str(i),'hand_r',(tipx,10.2-(1 if i in [1,2] else 0),-.4),(tipx-.15,9.5-(1 if i in [1,2] else 0),-1.35),.35,.4,INK)
    rib(m,'claw_thumb','hand_r',(5.8,15.8,0),(7,14.3,-.5),.85,.85,INK)
    rib(m,'claw_thumb_hook','hand_r',(7,14.3,-.5),(6.6,12.7,-1),.5,.55,INK)
    wrap(m,'fore_r',4,20,4.7,1.85);wrap(m,'fore_l',-4,18.5,3.6,1.55)
    return m

def circle():
    m=Rig('survivor_circle',3,'chainsaw');limbs(m,shirt=PAPER,pants=PAPER,boots=INK,skin=PAPER,boot_height=3.3)
    head(m);face(m,bandage=True);coat(m,PAPER,8.6,4.7);collar(m,GREY)
    # Long, saw-tooth black mane is a thick rear volume with separate layered locks.
    mane=[(-1.7,31),(-3,30.1),(-4.5,28.6),(-3.6,27.4),(-5.4,25.4),(-4.2,25.2),(-6.1,22.1),(-4.6,22.6),(-6.4,18.3),(-4.8,19),(-6.1,14.9),(-4.3,15.2),(-5.4,11),(-3.8,11.5),(-4.3,7.4),(-1.8,8.4),(0,10.2),(1.8,8.4),(4.3,7.4),(3.8,11.5),(5.4,11),(4.3,15.2),(6.1,14.9),(4.8,19),(6.4,18.3),(4.6,22.6),(6.1,22.1),(4.2,25.2),(5.4,25.4),(3.6,27.4),(4.5,28.6),(3,30.1),(1.7,31)]
    poly(m,'large_jagged_mane','hair',mane,2.2,2.1,INK)
    hair(m,INK,length=24.4,spiky=False)
    for s in [-1,1]:
        poly(m,'wolf_ear_'+str(s),'head',[(s*.9,29.8),(s*2.25,32),(s*2.6,29.2)],.3,2.15,INK)
        poly(m,'ear_inner_'+str(s),'head',[(s*1.45,30),(s*2.16,31.5),(s*2.32,29.8)],-.86,.15,PAPER)
    m.cube('mint_scarf_collar','chest',(-2.3,23.3,-1.6),(2.3,25.2,1.4),MINT,grain=.015)
    poly(m,'scarf_front','chest',[(-2.1,24),(2,24),(1.4,20.4),(-.3,21),(-1.7,22)],-1.68,.6,MINT)
    poly(m,'scarf_tail','coat',[(1.1,24),(2.6,23),(3.5,17.5),(1.8,18.3)],-.2,1,MINT)
    wrap(m,'fore_l',-4,18.4,3.4,1.5)
    # A real vertical chainsaw: thick central steel guide, dark rim, 30 teeth,
    # powered housing and forward/side handles. It replaces the right hand.
    m.cube('chainsaw_power_housing','weapon',(3.45,14,-1),(6.4,18.3,1.4),DARK,grain=.02)
    m.cube('chainsaw_engine_panel','weapon',(3.65,14.4,-1.15),(6.2,17.8,-1.01),GREY,grain=.01)
    for j in range(4):m.cube('engine_vent_'+str(j),'weapon',(4.1,15+j*.5,-1.24),(5.8,15.17+j*.5,-1.13),INK,grain=0)
    poly(m,'chain_outer_track','weapon',[(3.7,15),(6.1,15),(6.1,2),(5.75,.6),(4.9,.25),(4.05,.6),(3.7,2)],.1,1.5,INK)
    poly(m,'steel_guide_bar','weapon',[(4.08,14.7),(5.72,14.7),(5.72,2.2),(5.5,1.05),(4.9,.75),(4.3,1.05),(4.08,2.2)],-.05,1.6,GREY)
    m.cube('guide_centre','weapon',(4.65,1.5,-.92),(5.1,14.9,-.78),MINT,grain=.01)
    for j in range(15):
        y=1.25+j*.88
        for s in [-1,1]:
            x=4.9+s*1.24
            poly(m,'chain_tooth_'+str(s)+'_'+str(j),'weapon',[(x-s*.22,y-.26),(x+s*.36,y+.02),(x-s*.22,y+.42)],.1,1.7,PAPER)
    rib(m,'chainsaw_front_handle','weapon',(3.4,17.8,-.2),(6.5,17.8,-.2),.42,.46,INK)
    rib(m,'chainsaw_rear_handle','weapon',(3.45,16.5,.5),(2.9,18.4,.5),.5,.5,INK)
    m.cube('chainsaw_rivet','weapon',(4.6,15.4,-1.32),(5.1,15.9,-1.15),GOLD,grain=0)
    for side,s in [('r',1),('l',-1)]:wrap(m,'shin_'+side,s*1.25,5.3,2.4,1.7)
    return m

def bloomie():
    m=Rig('survivor_bloomie',2.25,'claw');limbs(m,shirt=MINT,pants=PAPER,boots=INK,skin=PAPER)
    head(m);face(m,bandage=True);hair(m,INK,length=25.5,spiky=True);collar(m,PAPER)
    coat(m,PAPER,11.2,3.5)
    m.cube('mint_shirt_waist','body',(-2.5,14.4,-1.2),(2.5,16,1.25),MINT,grain=.015)
    # Heavy cleaver arm, with a broad curved steel blade and deep dark tang.
    m.cube('cleaver_arm_socket','fore_r',(3.2,14,-.85),(5.25,19.5,.85),INK,grain=.012)
    poly(m,'massive_cleaver_blade','weapon',[(4.1,17),(7,18),(8.65,21.4),(8.3,26.4),(6.5,29),(5.7,25.5),(5,21)],.1,1.0,GREY)
    poly(m,'cleaver_polished_edge','weapon',[(7,18),(8.65,21.4),(8.3,26.4),(7.9,25.8),(8.05,21.6),(6.6,18.6)],-.47,.16,PAPER)
    seam(m,'cleaver_spine','weapon',(5,21,-.49),(6.5,29,-.49),DARK,.18)
    for j in range(3):m.cube('cleaver_rivet_'+str(j),'weapon',(4.1,17.1+j*.7,-.99),(4.45,17.45+j*.7,-.85),GOLD,grain=0)
    m.cube('cut_blade_hole','weapon',(7.08,25.2,-.55),(7.62,25.8,-.49),INK,grain=0)
    wrap(m,'fore_l',-4,18,3.5,1.5)
    return m

def alice():
    m=Rig('survivor_alice',2.5,'claw');limbs(m,shirt=PAPER,pants=INK,boots=INK,skin=GREY)
    head(m,GREY);face(m,eyes=0xD85B65,angry=True);hair(m,0x704E53,length=22.8,spiky=True)
    coat(m,PAPER,6.5,4.3);collar(m,PAPER);buttons(m,c=DARK)
    m.cube('shadow_face','head',(-1.8,26.7,-1.7),(1.8,28.9,-1.55),INK,grain=.01)
    for s in [-1,1]:
        poly(m,'glowing_red_eye_'+str(s),'head',[(s*.45,28.2),(s*1.5,28.5),(s*1.1,27.7)],-1.83,.17,0xD75C65)
        seam(m,'eye_scar_'+str(s),'head',(s*1,27.8,-1.94),(s*1.45,26.3,-1.94),BLOOD,.16)
    # Tilted three-point crown, built from solid gold plates.
    poly(m,'tilted_crown','head',[(-2.6,30.2),(-2.5,31.5),(-1.8,31),(-1.2,32),(-.6,31.15),(.25,31.65),(.15,30.2)],-1.38,.52,GOLD)
    poly(m,'crown_inside','head',[(-2.2,30.4),(-2.15,31),(-1.8,30.7),(-1.2,31.4),(-.8,30.7),(-.25,31.05),(-.3,30.4)],-1.68,.12,DARK)
    for i,(a,b) in enumerate([((-1.8,22),(-.5,20.2)),((.8,18),(2,16)),((-2,12),(-.8,10.8)),((1.6,9.8),(2.7,8.4))]):
        bone='chest' if a[1]>16 else ('coat_r' if a[0]>0 else 'coat_l')
        zz=-1.25 if a[1]>16 else -.45
        seam(m,'coat_scar_'+str(i),bone,(*a,zz),(*b,zz),BLOOD,.16)
        for j in range(3):
            x=a[0]+(b[0]-a[0])*(j+.4)/3;y=a[1]+(b[1]-a[1])*(j+.4)/3
            seam(m,'scar_stitch_'+str(i)+'_'+str(j),bone,(x-.20,y-.12,zz-.09),(x+.2,y+.12,zz-.09),INK,.07)
    wrap(m,'fore_r',4,18,3.3,1.5)
    # Long black fingers give her unarmed silhouette the dangerous reference pose.
    for side,s in [('r',1),('l',-1)]:
        for j in range(4):
            x=s*4-.6+j*.4
            rib(m,'black_digit_'+side+str(j),'hand_'+side,(x,13.8,0),(x+(j-1.5)*.13,11.6+(j%2)*.3,-.4),.23,.32,INK)
    return m

if __name__=='__main__':
    for builder in [grace,demi,sasha,thavel,circle,bloomie,alice]:
        m=builder().finish();print(m.name,len(m.cubes),'native cubes;',len(m.anims),'animations')
