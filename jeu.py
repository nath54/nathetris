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
tac=0.5000

dta=time.time()
taf=0.05

tx,ty=15,20

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
       [ [[2,1],[2,2],[1,2],[1,3]] , [[1,1],[2,1],[2,2],[3,2]] ]
]

def verif_pos(posc,cubes):
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
    def bouger(self,aa,cubes):
        if aa=="bas":
            can=True
            for c in self.cubes:
                if not verif_pos([c.px,c.py+1],cubes): can=False
            if can:
                self.py+=1
                for c in self.cubes:
                    c.py+=1
        elif aa=="gauche":
            can=True
            for c in self.cubes:
                if not verif_pos([c.px-1,c.py],cubes): can=False
            if can:
                self.px-=1
                for c in self.cubes: c.px-=1
        elif aa=="droite":
            can=True
            for c in self.cubes:
                if not verif_pos([c.px+1,c.py],cubes): can=False
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
                if not verif_pos([c.px,c.py],cubes): tch=True
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
                if not verif_pos([c.px,c.py],cubes): tch=True
            if tch:
                self.pa-=1
                if self.pa<0: self.pa=len(self.pcs)-1
                for c in self.cubes:
                    c.px=self.px+self.pcs[self.pa][self.cubes.index(c)][0]
                    c.py=self.py+self.pcs[self.pa][self.cubes.index(c)][1]

def newcenc():
    fig=Fig(int(tx/2),0,random.randint(0,len(figs)-1))
    cl=rcl()
    fig.pa=random.randint(0,len(fig.pcs)-1)
    for p in fig.pcs[fig.pa]:
        fig.cubes.append( Cube(fig.px+p[0],fig.py+p[1],cl) )
    return fig

def detect_rang(cubes,points):
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

def detect_perdu(cubes):
    perdu=False
    for c in cubes:
        if c.py < 4:
            perdu=True
            break
    return perdu

def ccc(cbs,cenc,dtc,tac,points,mode):
    perdu=False
    if time.time()-dtc >= tac:
        dtc=time.time()
        if tac > 0.2: tac-=0.001
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
            cbs,points=detect_rang(cbs,points)
            perdu=detect_perdu(cbs)
            cenc=newcenc()
    return cbs,cenc,dtc,perdu,points,tac


def aff(cbs,cenc,dta,taf,points,mode,tps):
    if time.time()-dta >= taf:
        dta=time.time()
        fenetre.fill((30,30,30))
        #quadrillage
        pdx,pdy=rx(100),ry(200)
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
        fenetre.blit( font.render("score : "+str(points),20,(250,250,250)) , [rx(520),ry(400)] )
        fenetre.blit( font.render("tps tomber : "+str(tac),20,(250,250,250)) , [rx(520),ry(500)] )
        fenetre.blit( font.render("tps : "+str(int(tps))+" sec",20,(250,250,250)) , [rx(520),ry(450)] )
        pygame.display.update()
    return dta
    
def game1(dtc,dta,tac,taf,mode):
    keys=[K_DOWN,K_LEFT,K_RIGHT,K_SPACE,K_b,K_v]
    cubes=[]
    cubeencour=newcenc()
    encourg=True
    perdu=False
    points=0
    tps=0
    while encourg:
        tt=time.time()
        cubes,cubeencour,dtc,perdu,points,tac=ccc(cubes,cubeencour,dtc,tac,points,mode)
        dta=aff(cubes,cubeencour,dta,taf,points,mode,tps)
        for event in pygame.event.get():
            if event.type==QUIT: encourg=False
            elif event.type==KEYDOWN:
                if event.key==K_q: encourg=False
                elif event.key==keys[0]:
                    cubeencour.bouger("bas",cubes)
                elif event.key==keys[1]:
                    cubeencour.bouger("gauche",cubes)
                elif event.key==keys[2]:
                    cubeencour.bouger("droite",cubes)
                elif event.key==keys[3]:
                    cubeencour.bouger("rot gauche",cubes)
                elif event.key==keys[4]:
                    cubeencour.bouger("rot droite",cubes)
        if perdu:
            encourg=False
            break
        tps+=time.time()-tt
    if perdu:
        fenetre.blit( font.render("Vous avez perdu",20,(255,255,255)),[rx(150),ry(50)])
        fenetre.blit( font.render("Veuillez appuyer sur SPACE pour retourner au menu",20,(255,255,255)),[rx(150),ry(100)])
        pygame.display.update()
    while perdu: 
        for event in pygame.event.get():
            if event.type==QUIT: perdu=False
            elif event.type==KEYDOWN:
                if event.key==K_q: perdu=False
                elif event.key==K_SPACE: perdu=False

mode=0
game1(dtc,dta,tac,taf,mode)




