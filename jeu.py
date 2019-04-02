#coding:utf-8
import random,time,pygame,numpy
from pygame.locals import *

tex,tey=700,900

pygame.init()
fenetre=pygame.display.set_mode([tex,tey])
pygame.display.set_caption("NATHETRIS")
#pygame.key.set_repeat(40,30)
font=pygame.font.SysFont("Serif",20)

dtc=time.time()
dta=time.time()


def rx(x): return int(x/700.0*tex)
def ry(y): return int(y/800.0*tey)

def rcl(): return (random.randint(0,255),random.randint(0,255),random.randint(0,255))

class Cube:
    def __init__(self,x,y,cl):
        self.px=x
        self.py=y
        self.cl=cl

figs=[ [ [[0,1],[1,1],[2,1],[3,1]] , [[2,0],[2,1],[2,2],[2,3]] ],
       [ [[1,1],[1,2],[2,1],[2,2]] ],
       [ [[1,1],[1,2],[1,3],[2,3]] , [[0,2],[1,2],[2,2],[2,1]] , [[1,1],[2,1],[2,2],[2,3]] , [[0,1],[1,1],[2,1],[0,2]] ],
       [ [[2,1],[2,2],[2,3],[1,3]] , [[0,1],[0,2],[1,2],[2,2]] , [[1,1],[1,2],[1,3],[2,1]] , [[0,1],[1,1],[2,1],[2,2]] ],
       [ [[1,1],[0,2],[1,2],[2,2]] , [[1,1],[1,2],[1,3],[2,2]] , [[0,1],[1,1],[2,1],[1,2]] , [[2,1],[2,2],[2,3],[1,2]] ],
       [ [[1,1],[1,2],[2,2],[2,3]] , [[1,2],[2,2],[2,1],[3,1]] ],
       [ [[2,1],[2,2],[1,2],[1,3]] , [[1,1],[2,1],[2,2],[3,2]] ],
       [ [[1,1],[1,2],[2,1]] , [[1,1],[2,1],[2,2]] , [[2,1],[2,2],[1,2]] , [[1,1],[1,2],[2,2]] ],
       [ [[1,1],[2,1],[3,1],[1,2],[3,2]] , [[1,1],[2,1],[2,2],[2,3],[1,3]] , [[1,1],[3,1],[1,2],[2,2],[3,2]] , [[1,1],[2,1],[1,2],[1,3],[2,3]] ],
       [ [[2,2]] ],
       [ [[2,2],[2,1],[1,2],[2,3],[3,2]] ],
       [ [[2,1],[2,2],[2,3]] , [[1,2],[2,2],[3,2]] ],
       [ [[2,0],[2,1]] , [[0,2],[1,2]] ]
]

clfs=[]
for f in figs: clfs.append(rcl())

def verif_pos(posc,cubes,tx,ty):
    pastch=True
    if posc[0] >= tx: pastch=False
    if posc[0] < 0: pastch=False
    if posc[1] >= ty: pastch=False
    if posc[1] < 0: pastch=False
    if pastch:
        for c in cubes:
            if posc[0]==c.px and posc[1]==c.py:
                pastch=False
                break
    return pastch
    

class Fig:
    def __init__(self,x,y,f):
        self.px=x
        self.py=y
        self.f=f
        self.pa=0
        self.pcs=figs[f]
        self.cubes=[]
    def bouger(self,aa,cubes,tx,ty):
        if aa=="bas":
            can=True
            for c in self.cubes:
                if not verif_pos([c.px,c.py+1],cubes,tx,ty): can=False
            if can:
                self.py+=1
                for c in self.cubes:
                    c.py+=1
        elif aa=="gauche":
            can=True
            for c in self.cubes:
                if not verif_pos([c.px-1,c.py],cubes,tx,ty): can=False
            if can:
                self.px-=1
                for c in self.cubes: c.px-=1
        elif aa=="droite":
            can=True
            for c in self.cubes:
                if not verif_pos([c.px+1,c.py],cubes,tx,ty): can=False
            if can:
                self.px+=1
                for c in self.cubes: c.px+=1
        elif aa=="rot gauche":
            self.pa-=1
            if self.pa<0: self.pa=len(self.pcs)-1
            for c in self.cubes:
                c.px=self.px+self.pcs[self.pa][self.cubes.index(c)][0]
                c.py=self.py+self.pcs[self.pa][self.cubes.index(c)][1]
            tch=False
            for c in self.cubes:
                if not verif_pos([c.px,c.py],cubes,tx,ty): tch=True
            if tch:
                self.pa+=1
                if self.pa>len(self.pcs)-1: self.pa=0
                for c in self.cubes:
                    c.px=self.px+self.pcs[self.pa][self.cubes.index(c)][0]
                    c.py=self.py+self.pcs[self.pa][self.cubes.index(c)][1]
        elif aa=="rot droite":
            self.pa+=1
            if self.pa>len(self.pcs)-1: self.pa=0
            for c in self.cubes:
                c.px=self.px+self.pcs[self.pa][self.cubes.index(c)][0]
                c.py=self.py+self.pcs[self.pa][self.cubes.index(c)][1]
            tch=False
            for c in self.cubes:
                if not verif_pos([c.px,c.py],cubes,tx,ty): tch=True
            if tch:
                self.pa-=1
                if self.pa<0: self.pa=len(self.pcs)-1
                for c in self.cubes:
                    c.px=self.px+self.pcs[self.pa][self.cubes.index(c)][0]
                    c.py=self.py+self.pcs[self.pa][self.cubes.index(c)][1]

def newcenc(tx,ty,modcl):
    f=random.randint(0,len(figs)-1)
    fig=Fig(int(tx/2),0,f)
    if modcl == 0 : cl=rcl()
    elif modcl == 1 : cl=clfs[f]
    elif modcl == 2 : cl=(255,255,255)
    fig.pa=random.randint(0,len(fig.pcs)-1)
    for p in fig.pcs[fig.pa]:
        fig.cubes.append( Cube(fig.px+p[0],fig.py+p[1],cl) )
    return fig

def detect_rang(cubes,points,tx,ty):
    j=numpy.zeros([tx,ty])
    for c in cubes: j[c.px,c.py]=1
    rt=[]
    adel=[]
    nbrmt=0
    for y in range(ty):
        rang=True
        for x in range(tx):
            if j[x,y]==0:
                rang=False
                break
        if rang :
            nbrmt+=1
            for c in cubes:
                if c.py==y:
                    adel.append(c)
                    j[c.px,c.py]=0
                    points+=1*nbrmt
            for c in cubes:
                if c.py<y:
                    c.py+=1
    for c in adel:
        del(cubes[cubes.index(c)])
    return cubes,points

def detect_perdu(cubes,tx,ty):
    perdu=False
    for c in cubes:
        if c.py < 4:
            perdu=True
            break
    return perdu

def ccc(cbs,cenc,dtc,tac,points,mode,tx,ty,mintac,dimtac,modecl):
    perdu=False
    if time.time()-dtc >= tac:
        dtc=time.time()
        if tac > mintac: tac-=dimtac
        j=numpy.zeros([tx,ty])
        for c in cbs:
            j[c.px,c.py]=1
        tf=False
        for c in cenc.cubes:
            if c.py+1==ty or j[c.px,c.py+1]==1:
                tf=True
        if not tf:
            for c in cenc.cubes:
                c.py+=1
            cenc.py+=1
        else:
            for c in cenc.cubes:
                cbs.append(c)
            cbs,points=detect_rang(cbs,points,tx,ty)
            perdu=detect_perdu(cbs,tx,ty)
            cenc=newcenc(tx,ty,modecl)
    return cbs,cenc,dtc,perdu,points,tac


def aff(cbs,cenc,dta,taf,points,mode,tps,tx,ty):
    if time.time()-dta >= taf:
        dta=time.time()
        fenetre.fill((30,30,30))
        #quadrillage
        pdx,pdy=rx(100),ry(100)
        tc=rx(25)
        pygame.draw.rect(fenetre,(10,10,10),(pdx,pdy,(tx*tc),(ty*tc)),0)
        cll=(150,150,150)
        for x in range(tx+1): pygame.draw.line(fenetre,cll,(pdx+(x*tc),pdy),(pdx+(x*tc),pdy+(ty*tc)),1)
        for y in range(ty+1):
            if y==4: cll=(250,0,0)
            else: cll=(150,150,150)
            pygame.draw.line(fenetre,cll,(pdx,pdy+(y*tc)),(pdx+(tx*tc),pdy+(y*tc)),1)
        #cubes
        for c in cbs+cenc.cubes: pygame.draw.rect(fenetre,c.cl,(pdx+(c.px*tc),pdy+(c.py*tc),tc,tc),0)
        #points
        fenetre.blit( font.render("score : "+str(points),20,(250,250,250)) , [rx(300),ry(700)] )
        fenetre.blit( font.render("tps : "+str(int(tps))+" sec",20,(250,250,250)) , [rx(300),ry(750)] )
        pygame.display.update()
    return dta
    
def game1(dtc,dta,tac,taf,mode,tx,ty,modecl,menu,mintac,dimtac):
    keys=[K_DOWN,K_LEFT,K_RIGHT,K_SPACE,K_b,K_v]
    cubes=[]
    cubeencour=newcenc(tx,ty,modecl)
    encourg=True
    perdu=False
    points=0
    tps=0
    while encourg:
        tt=time.time()
        cubes,cubeencour,dtc,perdu,points,tac=ccc(cubes,cubeencour,dtc,tac,points,mode,tx,ty,mintac,dimtac,modecl)
        dta=aff(cubes,cubeencour,dta,taf,points,mode,tps,tx,ty)
        for event in pygame.event.get():
            if event.type==QUIT: encourg=False
            elif event.type==KEYDOWN:
                if event.key==K_q: encourg=False
                elif event.key==keys[0]:
                    cubeencour.bouger("bas",cubes,tx,ty)
                elif event.key==keys[1]:
                    cubeencour.bouger("gauche",cubes,tx,ty)
                elif event.key==keys[2]:
                    cubeencour.bouger("droite",cubes,tx,ty)
                elif event.key==keys[3]:
                    cubeencour.bouger("rot gauche",cubes,tx,ty)
                elif event.key==keys[4]:
                    cubeencour.bouger("rot droite",cubes,tx,ty)
        if perdu:
            encourg=False
            break
        tps+=time.time()-tt
    if perdu:
        fenetre.blit( font.render("Vous avez perdu",20,(255,255,255)),[rx(150),ry(20)])
        fenetre.blit( font.render("Veuillez appuyer sur SPACE pour retourner au menu",20,(255,255,255)),[rx(150),ry(60)])
        pygame.display.update()
    while perdu: 
        for event in pygame.event.get():
            if event.type==QUIT: perdu=False
            elif event.type==KEYDOWN:
                if event.key==K_q: perdu=False
                elif event.key==K_SPACE: perdu=False
    menu()

########menu

def texte(txt,x,y,t,cl): fenetre.blit( pygame.font.SysFont("Serif",rx(t)).render(txt,rx(t),cl) , [rx(x),ry(y)] )

def boutton(x,y,tx,ty,cl):
    b=pygame.draw.rect(fenetre,cl,(rx(x),ry(y),rx(tx),ry(ty)),0)
    pygame.draw.rect(fenetre,(0,0,0),(rx(x),ry(y),rx(tx),ry(ty)),2)
    return b

def affmenu(modecl,mode,tx,tac,dimtac):
    bts=[]
    for x in range(20): bts.append(None)
    fenetre.fill(clf)
    texte("N",100,80,80,rcl())
    texte("A",150,80,80,rcl())
    texte("T",200,80,80,rcl())
    texte("H",250,80,80,rcl())
    texte("E",300,80,80,rcl())
    texte("T",350,80,80,rcl())
    texte("R",400,80,80,rcl())
    texte("I",450,80,80,rcl())
    texte("S",480,80,80,rcl())
    a=(50,50,50)
    b=(50,250,50)
    clbs=[]
    for x in range(16): clbs.append(a)
    #
    bts[0]=boutton(200,550,200,100,(150,150,0))
    texte("jouer",240,570,30,(150,0,0))
    #
    if modecl==0: clbs[0]=b
    elif modecl==1: clbs[1]=b
    elif modecl==2: clbs[2]=b
    texte("mode couleur",20,200,20,(250,250,250))
    bts[1]=boutton(20,240,100,30,clbs[0])
    bts[2]=boutton(20,280,100,30,clbs[1])
    bts[3]=boutton(20,320,100,30,clbs[2])
    texte("normal",25,245,15,(255,255,255))
    texte("uniques",25,285,15,(255,255,255))
    texte("noir et blanc",25,325,15,(255,255,255))
    #
    if tac==0.5: clbs[4]=b
    elif tac==0.4: clbs[5]=b
    elif tac==0.3: clbs[6]=b
    elif tac==0.2: clbs[7]=b
    texte("difficulté",150,200,20,(250,250,250))
    bts[4]=boutton(150,240,100,30,clbs[4])
    bts[5]=boutton(150,280,100,30,clbs[5])
    bts[6]=boutton(150,320,100,30,clbs[6])
    bts[7]=boutton(150,360,100,30,clbs[7])
    texte("facile",155,245,15,(255,255,255))
    texte("moyen",155,285,15,(255,255,255))
    texte("difficile",155,325,15,(255,255,255))
    texte("hardcore",155,365,15,(255,255,255))
    #
    if dimtac==0: clbs[8]=b
    elif dimtac==0.0001: clbs[9]=b
    elif dimtac==0.001: clbs[10]=b
    elif dimtac==0.01: clbs[11]=b
    texte("accélération",280,200,20,(250,250,250))
    bts[8]=boutton(280,240,100,30,clbs[8])
    bts[9]=boutton(280,280,100,30,clbs[9])
    bts[10]=boutton(280,320,100,30,clbs[10])
    bts[11]=boutton(280,360,100,30,clbs[11])
    texte("-",305,245,15,(255,255,255))
    texte(">",305,285,15,(255,255,255))
    texte(">>",305,325,15,(255,255,255))
    texte(">>>",305,365,15,(255,255,255))
    #
    if mode==0: clbs[15]=b
    texte("mode jeu",420,200,20,(250,250,250))
    bts[16]=boutton(400,240,100,30,clbs[15])
    texte("standar",405,245,15,(255,255,255))
    #
    if tx==10: clbs[12]=b
    elif tx==15: clbs[13]=b
    elif tx==20: clbs[14]=b
    texte("taille plateau",520,200,20,(250,250,250))
    bts[12]=boutton(520,240,100,30,clbs[12])
    bts[13]=boutton(520,280,100,30,clbs[13])
    bts[14]=boutton(520,320,100,30,clbs[14])
    texte("10*18",525,245,15,(255,255,255))
    texte("15*20",525,285,15,(255,255,255))
    texte("20*25",525,325,15,(255,255,255))
    #
    bts[15]=boutton(10,10,30,30,(200,0,0))
    texte("X",12,10,32,(0,0,0))
    pygame.display.update()
    return bts

clf=(50,16,80)

def menu():
    taf=0.05
    tac=0.5000
    mintac=0.3
    dimtac=0.001
    tx,ty=15,20
    needtoaff=True
    encourmenu=True
    playgame=False
    mode=0
    modecl=0
    bts=[]
    while encourmenu:
        if needtoaff:
            bts=affmenu(modecl,mode,tx,tac,dimtac)
            needtoaff=False
        for event in pygame.event.get():
            if event.type==QUIT: encourmenu=False
            elif event.type==KEYDOWN:
                if event.key==K_q: encourmenu=False
            elif event.type==MOUSEBUTTONUP:
                needtoaff=True
                pos=pygame.mouse.get_pos()
                rpos=pygame.Rect(pos[0],pos[1],1,1)
                for b in bts:
                    if b!=None and rpos.colliderect(b):
                        di=bts.index(b)
                        if di==0: encourmenu,playgame=False,True
                        elif di==1: modecl=0
                        elif di==2: modecl=1
                        elif di==3: modecl=2
                        elif di==4: tac,mintac=0.5,0.4
                        elif di==5: tac,mintac=0.4,0.3
                        elif di==6: tac,mintac=0.3,0.2
                        elif di==7: tac,mintac=0.2,0.1
                        elif di==8: dimtac=0
                        elif di==9: dimtac=0.0001
                        elif di==10: dimtac=0.001
                        elif di==11: dimtac=0.01
                        elif di==12: tx,ty=10,18
                        elif di==13: tx,ty=15,20
                        elif di==14: tx,ty=20,25
                        elif di==15: exit()
                        elif di==16: mode=0
    if playgame :
        playgame=False
        game1(dtc,dta,tac,taf,mode,tx,ty,modecl,menu,mintac,dimtac)

#########

menu()


