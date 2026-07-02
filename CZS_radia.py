from __future__ import print_function #Python 2.7 compatibility
import radia as rad
import numpy as np
import matplotlib.pyplot as plt


'''General Term Definitions'''
rad.FldUnits()
nseg=50
#rad.FldCmpCrt(10**4)

#all values taken from orignal Mathematica Notebook (look up sources for these values )

hbar=1.054571800*10**-34
h=hbar*2*np.pi
u=1.66051*10**-27
kB=1.380648*10**-23
c=2.9979*10**8
muB=9.274*10**-24
muknot=4*np.pi*10**-7
hbareV=4.13566766*10**-15
heV=hbareV*2*np.pi
kBEv=8.61733034*10**-5
Na=6.022*10**23
eVJ=1.60218*10**-19
mLi=6*u
gammaLi=2*np.pi*5.87*10**6
lambdaLi=671*10**-9
rhoCu=1.7*10**-8
rhoBrass=9*10**-8


'''Zeeman Slower'''


currents=(-195, 195, 10, -10, 0, 0, 261) #(*currents for MOT, MOTH, Bias, BiasH, Curv, CurvH, ZS in A*)

'''
currents=(0, 0, 416, 416, -123, -123, 0) #(*currents for MOT, MOTH, Bias, BiasH, Curv, CurvH, ZS in A*)
currents=(195, 195, 0, 0, 0, 0, 0) #(*currents for MOT, MOTH, Bias, BiasH, Curv, CurvH, ZS in A*)
'''

#count=np.zeros(7)
ZSgrp=rad.ObjCnt([])
IZS=currents[6]
rinZS=13.7
routZS=35


m=10

#unscaled in inches

unscaledZSdisc=np.array([.125, .04, .04, .04, .04, .04, .04, .04, .08, .04, .0400,
.04, .08, .04, .04, .04, .08, .04, .04, .04, .08000,
.04, .08, .04, .08, .04, .08, .04, .08, .04, .08000,
.08, .04, .08, .08, .04, .08, .08, .08, .04, .08000,
.08, .08, .04, .08, .08, .08, .08, .04, .08, .08000,
.08, .08, .08, .04, .08, .08, .08, .08, .08, .08000,
.08, .04, .08, .08, .08, .08, .08, .04, .08, .08000,
.08, .08, .08, .08, .08, .08, .125, .08, .08, .08000,
.08, .08, .125, .08, .08, .08, .08, .125, .08, .08000,
.08, .125, .08, .125, .08, .125, .08, .08, .08, .08000,
.125, .125, .125, .125, .04])

#unscaledZSdisc=np.array([1,2,3])
#converting to mm
scalar=np.full(len(unscaledZSdisc),25.4)

#try this
disczs=scalar*unscaledZSdisc

discZS=scalar*unscaledZSdisc
#print(discZS)
#print('Number of discs:', len(discZS))


#in inches 

unscaledgapsZS= np.array([.025, .025, .025, .025, .025, .025, .025, .025, .025, .025, .025,
.025, .025, .025, .025, .025, .025, .025, .025, .025, .025,
.025, .05, .025, .025, .025, .025, .025, .025, .025, .05000,
.025, .025, .025, .025, .025, .025, .025, .025, .025, .025000,
.025, .025, .05, .025, .025, .025, .025, .025, .025, .05000,
.025, .025, .025, .05, .025, .025, .025, .05, .025, .05000,
.025, .05, .025, .05, .05, .025, .05, .05, .05, .025000,
.05, .05, .05, .025, .05, .025, .05, .05, .05, .025000,
.05, .05, .05, .05, .05, .075, .05, .05, .075, .05000,
.075, .075, .05, .075, .075, .1, .1, .125, .125, .15000,
.175, .175, .175, .175, 20])

#unscaledgapsZS=([0.5,0.6,0.9])
scalar=np.full(len(unscaledgapsZS),25.4)

gapsZS= scalar*unscaledgapsZS
#print('Number of gaps:', len(unscaledgapsZS))


#defining function to find position of each layer along z-axis
# Initialize variables for total sum and index 


#outputs location of the bottom of the layer
def zposZS(layer):
    if layer == 0:
        return 0
    else:
        total_sum = 0
        index = 0
        while index < layer: # Iterate through the list using a while loop 
            total_sum = total_sum + discZS[index] + gapsZS[index]
            index += 1

        return total_sum

print("zpos", zposZS(2))
#Testing zposzs function
'''
TestZSpos= zposZS(1)
print('TestZSpos:',TestZSpos)
'''
#could add in the -1 here
maxlayerZS = len(gapsZS)-1
#print('lengapsZS:', maxlayerZS)
discZSlen=len(discZS)
#print('lendiscZS:', discZSlen)

'''
test2=zposZS(maxlayerZS)
print(test2)

test3 = discZS[maxlayerZS-1]
print(test3) 
#says index 106 is out of bounds but it should be fine as function deals with input-1
#indexing must start at 0 so we  need the -1 to access the final entry
'''

lenZS = zposZS(maxlayerZS)+ discZS[maxlayerZS]
print(lenZS)

'''Now, encode all the separate parts of the two coils and append them 
to the container we just created'''


#defining the even odd functions outside of the list

def copperinitialangle(layer):
    if layer % 2 == 0:
        return 0
    else: 
        return np.pi
    
def copperfinalangle(layer):
    if layer % 2 == 0:
        return np.pi
    else: 
        return 2*np.pi

def plugx(layer):
    if layer % 2 == 0:
        return 1*0.5*(routZS+rinZS)*np.sin(np.pi/2)
    else: 
        return -1*0.5*(routZS+rinZS)*np.sin(np.pi/2)
    
def plugy(layer):
    if layer % 2 == 0:
        return -1*0.5*(routZS+rinZS)*np.cos(np.pi/2)
    else: 
        return 1*0.5*(routZS+rinZS)*np.cos(np.pi/2)
    
def test(layer):
    if layer % 2 == 0:
        return -200
    else:
        return 200


print('maxlayer', maxlayerZS)


#use massive for loop (its not that massive)
ax = plt.figure().add_subplot(projection='3d')

#range automatically does not compute through the right bound so this adds the correct number of layers
for layer in range(0,maxlayerZS):
    
    copper = rad.ObjArcCur([0,0,zposZS(layer)+0.5*discZS[layer]],[rinZS,routZS],[copperinitialangle(layer),copperfinalangle(layer)],discZS[layer],nseg, IZS/(discZS[layer]*(routZS-rinZS)))
    if layer < 1000:
        #plotting by converting the polar information radia takes to rectangular coordinates for matplotlib
        z = np.linspace(zposZS(layer), zposZS(layer), 20) #this z coordinate plots the bottom of the layer
        r = np.linspace(0.5*(rinZS+routZS),0.5*(rinZS+routZS),20)
        theta=np.linspace(copperinitialangle(layer),copperfinalangle(layer),20)
        x = r * np.cos(theta)
        y = r * np.sin(theta)

        ax.plot(x, y, z, label='parametric curve')

    

    copperplug = rad.ObjRecCur([plugx(layer),plugy(layer),zposZS(layer)+discZS[layer]+0.5*gapsZS[layer]],[routZS-rinZS , routZS-rinZS , gapsZS[layer]],[0,0,IZS/((routZS-rinZS)**2)] )
    if layer < 1000:
        zblock = np.linspace(zposZS(layer)+discZS[layer]+gapsZS[layer],zposZS(layer)+discZS[layer]+gapsZS[layer],20) #plots top of spacer so I can check if it makes cintact with bottom of ring as plotted 
        xblock = np.linspace(plugx(layer),plugx(layer),20)
        yblock = np.linspace(plugy(layer),plugy(layer),20)

        ax.plot(xblock, yblock, zblock, marker='_')
    print('gaps',gapsZS[layer])
    print('disc',discZS[layer])
    print('layer',layer)
    #put everything into the container

    rad.ObjAddToCnt(ZSgrp , [copper,copperplug])

#create geometry for final top ring with out a corresonding spacer
copper = rad.ObjArcCur([0,0,zposZS(maxlayerZS)+0.5*discZS[maxlayerZS]],[rinZS,routZS], [copperinitialangle(maxlayerZS),copperfinalangle(maxlayerZS)],discZS[maxlayerZS], nseg, IZS/(discZS[maxlayerZS]*(routZS-rinZS)))
print('disc', discZS[maxlayerZS])
print('maxlayer', maxlayerZS)

z = np.linspace(zposZS(maxlayerZS), zposZS(maxlayerZS), 20)
r = np.linspace(0.5*(rinZS+routZS),0.5*(rinZS+routZS),20)
theta=np.linspace(copperinitialangle(maxlayerZS),copperfinalangle(maxlayerZS),20)
x = r * np.cos(theta)
y = r * np.sin(theta)
ax.plot(x, y, z, label='parametric curve')

plt.xlabel(r'x')
plt.ylabel(r'y')

plt.show()


#add final copper ring to container holding rest of geometry
rad.ObjAddToCnt(ZSgrp,[copper])



RCuZS = sum(rhoCu*(2*np.pi)/(10**(-3)*discZS*np.log(routZS/rinZS)))  #resistance of all ZS coils

RspacerZS = sum(rhoCu*(gapsZS*10**(-3))/(10**(-6)*(routZS-rinZS)**2))  #reistance of all ZS spacers

RZS = RCuZS+RspacerZS  #resistance of entire ZS coil
VZS = IZS*RZS  #voltage drop for both curvature coils
PZS=IZS**2*RZS  #power dissipated in both curvature coils
LZS=muknot/(4*np.pi)*(maxlayerZS**2)*rinZS*0.001*10  #Self inductance of ZS coils
tauZS=LZS/RZS  #time constant 
#flowZS=3.8*(10**(-3))/60  #flow rate in gpm -> m^3/sec
#dTZS=PZS/(998*flowZS*4186)  #change in water temperature flowing through curvature coils

print('resistance:', RZS)
print('LZS:', LZS)
print('tauZS:', tauZS)
print('IZS:', IZS)
print('voltage drop:', VZS)
print('PZS:', PZS)
#print('flowZS:', flowZS)
#print('dTZS:', dTZS)

Steps=106
leftbound= -100
rightbound=lenZS+60
zpos= np.linspace(leftbound,rightbound,Steps)

Bz=rad.FldLst(ZSgrp,'bz',[0,0,leftbound],[0,0,rightbound],Steps,'noarg')
By=rad.FldLst(ZSgrp,'by',[0,0,leftbound],[0,0,rightbound],Steps,'noarg')
Bx=rad.FldLst(ZSgrp,'bx',[0,0,leftbound],[0,0,rightbound],Steps,'noarg')
#Bmag=rad.FldLst(ZSgrp,'',[0,0,leftbound],[0,0,rightbound],Steps,'noarg')


plt.plot(zpos,Bz, label=r'$B_z$')
plt.plot(zpos,By, label=r'$B_y$')
plt.plot(zpos,Bx, label=r'$B_x$')

#plt.plot(zpos,Bmag, label=r'$B Magnitude$')
plt.xlabel(r'Position $z$ (mm)')
plt.ylabel(r'Axial Field  (T)')
plt.title(r'Zeeman Slower $I=261$ A')
plt.legend()
plt.show()


'''TOLERENCING'''

'''changing angle about center'''

#check to make sure theta starts at zero at the same place in radia and matplotlib

raveZS= (rinZS+routZS)/2

#creating functions that alter the splay of the rings in the odd ring based on a loop with a counter that serves as an input in radians for this splay

def centerx(s,layer):
    if layer % 2 == 0:
        return 0
    else: 
        return raveZS-raveZS*np.cos(s)  
    
def centery(s,layer):
    if layer % 2 == 0:
        return 0
    else: 
        return -raveZS*np.sin(s)

def copperinitialangletol(s,layer):
    if layer % 2 == 0:
        return 0
    else: 
        return np.pi+s
    
def copperfinalangletol(s,layer):
    if layer % 2 == 0:
        return np.pi
    else: 
        return 2*np.pi+s


maxang = 0.05
steps=10
#print(np.linspace(-maxang,maxang,steps))
sdistr = np.array(np.linspace(-maxang,maxang,steps))




#empty list to eventually add residual sums to
diffzcont=[]
diffycont=[]
diffxcont=[]




for s in sdistr:
    ZSgrpang=rad.ObjCnt([])
    #bx = plt.figure().add_subplot(projection='3d')
    for layer in range(0,maxlayerZS):
    
        copper = rad.ObjArcCur([centerx(s,layer),centery(s,layer),zposZS(layer)+0.5*discZS[layer]],[rinZS,routZS],[copperinitialangletol(s,layer),copperfinalangletol(s,layer)],discZS[layer],nseg, IZS/(discZS[layer]*(routZS-rinZS)))
        #if layer < 1000:
         #   z = np.linspace(zposZS(layer), zposZS(layer), 20)
          #  r = np.linspace(0.5*(rinZS+routZS),0.5*(rinZS+routZS),20)
           # theta=np.linspace(copperinitialangletol(s,layer),copperfinalangletol(s,layer),20)
            #x = r * np.cos(theta)+centerx(s,layer)
            #y = r * np.sin(theta)+centery(s,layer)

            #bx.plot(x, y, z, label='parametric curve')

    

        copperplug = rad.ObjRecCur([plugx(layer),plugy(layer),zposZS(layer)+discZS[layer]+0.5*gapsZS[layer]],[routZS-rinZS , routZS-rinZS , gapsZS[layer]],[0,0,IZS/((routZS-rinZS)**2)] )
       # if layer < 1000:
        #    zblock = np.linspace(zposZS(layer)+discZS[layer]+gapsZS[layer],zposZS(layer)+discZS[layer]+gapsZS[layer],20)
         #   xblock = np.linspace(plugx(layer),plugx(layer),20)
          #  yblock = np.linspace(plugy(layer),plugy(layer),20)

           # bx.plot(xblock, yblock, zblock, marker='_')
        #print('gaps',gapsZS[layer])
        #print('disc',discZS[layer])
        #print('layer',layer)
        #put everything into the container

        rad.ObjAddToCnt(ZSgrpang , [copper,copperplug])

    #create geometry for final top ring with out a corresonding spacer
    copperlid = rad.ObjArcCur([centerx(s,maxlayerZS),centery(s,maxlayerZS),zposZS(maxlayerZS)+0.5*discZS[maxlayerZS]],[rinZS,routZS], [copperinitialangletol(s,maxlayerZS),copperfinalangletol(s,maxlayerZS)],discZS[maxlayerZS], nseg, IZS/(discZS[maxlayerZS]*(routZS-rinZS)))
    #print('disc', discZS[maxlayerZS])
    #print('maxlayer', maxlayerZS)

    #z = np.linspace(zposZS(maxlayerZS), zposZS(maxlayerZS), 20)
    #r = np.linspace(0.5*(rinZS+routZS),0.5*(rinZS+routZS),20)
    #theta=np.linspace(copperinitialangletol(s,maxlayerZS),copperfinalangletol(s,maxlayerZS),20)
    #x = r * np.cos(theta)+centerx(s,maxlayerZS)
    #y = r * np.sin(theta)+centery(s,maxlayerZS)
    #bx.plot(x, y, z, label='parametric curve')
    #plt.xlabel(r'x')
    #plt.ylabel(r'y')
   
    #plt.show()
    #exit()

    #add final copper ring to container holding rest of geometry
    rad.ObjAddToCnt(ZSgrpang,[copperlid])

    Steps=106
    leftbound= -100
    rightbound=lenZS+60
    zpos= np.linspace(leftbound,rightbound,Steps)

    Bzang=rad.FldLst(ZSgrpang,'bz',[0,0,leftbound],[0,0,rightbound],Steps,'noarg')
    Byang=rad.FldLst(ZSgrpang,'by',[0,0,leftbound],[0,0,rightbound],Steps,'noarg')
    Bxang=rad.FldLst(ZSgrpang,'bx',[0,0,leftbound],[0,0,rightbound],Steps,'noarg')
    '''
    plt.plot(zpos,Bz)
    plt.plot(zpos,Bzang)
    plt.plot(zpos,Byang)
    plt.plot(zpos,Bxang)
    plt.xlabel(r'Position $z$ (mm)')
    plt.ylabel(r'Axial Field $B_z$ (T)')
    plt.title(r'Zeeman Slower $I=261$ A')
    plt.show()
    '''

    diffz=sum(np.array(Bz)-np.array(Bzang))
    diffzsq=diffz**2
    diffzcont.append(diffzsq)
    diffy=sum(np.array(By)-np.array(Byang))
    diffysq=diffy**2
    diffycont.append(diffysq)
    diffx=sum(np.array(Bx)-np.array(Bxang))
    diffxsq=diffx**2
    diffxcont.append(diffxsq)

plt.plot(sdistr,diffzcont,'o', label=r'z component')
plt.show()
plt.plot(sdistr,diffycont,'o', label=r'y component')
plt.plot(sdistr,diffxcont,'o', label=r'x component')
plt.legend()
plt.title('Sqaure Residual')
plt.xlabel('Angle of Odd Layer Center Deviation from Origin (rad)')
plt.show()
    

    


#ignore everyting below this point (created before fixing the geometry in my original loop)
'''
for s in sdistr:
    
    
    for layer in range(0,maxlayerZS-1):
        #print(copperinitialangletol(s,layer),copperfinalangletol(s,layer))
        #print(center(s,layer),zposZS(layer)+0.5*discZS[layer],rinZS,routZS,copperinitialangletol(s,layer),copperfinalangletol(s,layer),discZS[layer])
        copper = rad.ObjArcCur([centerx(s,layer),centery(s,layer),zposZS(layer)+0.5*discZS[layer]],[rinZS,routZS],[copperinitialangletol(s,layer),copperfinalangletol(s,layer)],discZS[layer],nseg, IZS/(discZS[layer]*(routZS-rinZS)))
        #print(routZS-rinZS , routZS-rinZS , gapsZS[layer])
        copperplug = rad.ObjRecCur([plugx(layer),plugy(layer),zposZS(layer)+discZS[layer]+0.5*gapsZS[layer]],[routZS-rinZS , routZS-rinZS , gapsZS[layer]],[0,0,IZS/((routZS-rinZS)**2)] )

        #put everything into the container

        rad.ObjAddToCnt(ZSgrpang , [copper,copperplug])

    #create geometry for final top ring with out a corresonding spacerplt.plot(sdistr,diffzcont,'o', label=r'z component')
    copper_lid = rad.ObjArcCur([centerx(s,maxlayerZS),centery(s,maxlayerZS),zposZS(maxlayerZS)+0.5*discZS[maxlayerZS-1]],[rinZS,routZS], [copperinitialangletol(s,maxlayerZS),copperfinalangletol(s,maxlayerZS)],discZS[maxlayerZS-1], nseg, IZS/(discZS[maxlayerZS-1]*(routZS-rinZS)))

    #add final copper ring to container holding rest of geometry
    rad.ObjAddToCnt(ZSgrpang,[copper_lid])     

    
    Steps=106
    zpos= np.linspace(0,maxlayerZS,Steps)
    
    Bztol=rad.FldLst(ZSgrpang,'bz',[0,0,0],[0,0,maxlayerZS],Steps,'noarg')
    
    
    
    diffsum=(sum(np.array(Bz)-np.array(Bztol))**2)
    diff=np.array(Bz)-np.array(Bztol)
    difftol.append(diffsum)
    standdevog=np.std(diff**2)
    standdev.append(standdevog)
    
    plt.plot(zpos,Bz)
    plt.plot(zpos,Bztol,'o')
    plt.show()
    '''
'''
print ('standdev list:',standdev)


plt.plot(sdistr,standdev,'o')
plt.show()
plt.plot(sdistr,difftol,'o',label='diff')
plt.legend()
plt.show()
'''

'''changing thickness uniformly'''
'''
ZSgrpthk=rad.ObjCnt([])

addit=1
steps=4

scalar=np.full(len(unscaledZSdisc),addit)
discZSthk=scalar+discZS
gapsZSthk= scalar+gapsZS

def zposZSthk(layer):
    if layer == 0:
        return 0
    else:
        total_sum = 0
        index = 0
        while index < layer-1: # Iterate through the list using a while loop 
            total_sum = total_sum + discZSthk[index] + gapsZSthk[index]
            index += 1

        return total_sum


for t in np.linspace(0,addit,steps):
    for layer in range(0,maxlayerZS):
    
        copper = rad.ObjArcCur([0,0,zposZSthk(layer)+0.5*discZSthk[layer]],[rinZS,routZS],[copperinitialangle(layer),copperfinalangle(layer)],discZSthk[layer],nseg, IZS/(discZSthk[layer]*(routZS-rinZS)))

        copperplug = rad.ObjRecCur([plugx(layer),plugy(layer),zposZSthk(layer)+discZSthk[layer]+0.5*gapsZSthk[layer]],[routZS-rinZS , routZS-rinZS , gapsZSthk[layer-1]],[0,0,IZS/((routZS-rinZS)**2)] )

        #put everything into the container

        rad.ObjAddToCnt(ZSgrpthk , [copper,copperplug])

    #create geometry for final top ring with out a corresonding spacer
    copper = rad.ObjArcCur([0,0,zposZSthk(maxlayerZS)+0.5*discZSthk[maxlayerZS-1]],[rinZS,routZS], [copperinitialangle(maxlayerZS),copperfinalangle(maxlayerZS)],discZSthk[maxlayerZS-1], nseg, IZS/(discZSthk[maxlayerZS-1]*(routZS-rinZS)))

    #add final copper ring to container holding rest of geometry
    rad.ObjAddToCnt(ZSgrpthk,[copper])

    Steps=106
    zpos= np.linspace(0,maxlayerZS,Steps)

    Bzthk=rad.FldLst(ZSgrpthk,'bz',[0,0,0],[0,0,maxlayerZS],Steps,'noarg')
    plt.plot(zpos,Bz)
    plt.plot(zpos,Bzthk,'o')
    plt.show()

'''
