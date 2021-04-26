import numpy as np
import copy
import time

#ces lignes servent à lire les instances 
fichier = input("Quel fichier dois-je considérer ? ")
try:
    file = open(fichier, "r")
except:
    print("Le fichier", filename, "est introuvable, veuillez réessayer")


r= file.read()

LL1=[]
LL2=[]
car=0
nb=''
S=[]

while r[car] and r[car]!='#':

    if r[car]=='\n':
        if nb!='':
            S.append(int(nb))
        LL1.append(S)
        S=[]
        car+=1
        nb=''

    elif r[car]==' ':
        S.append(int(nb))
        car+=1
        nb=''

    elif r[car]!=' ' and r[car]!='\n':
        nb+=str(r[car])
        car+=1

car+=2

while car<len(r) and r[car]:

    if r[car]=='\n':
        if nb!='':
            S.append(int(nb))
        LL2.append(S)
        S=[]
        car+=1
        nb=''

    elif r[car]==' ':
        S.append(int(nb))
        car+=1
        nb=''

    elif r[car]!=' ' and r[car]!='\n':
        nb+=str(r[car])
        car+=1
    
N=len(LL1)
M=len(LL2)

#on défini des élements fixes pour la suite du code
VIDE = 0
NOIR = 1
BLANC = 2


#création grille
def cree_grille(N,M):
    grille=np.zeros((N,M),dtype=int)
    return grille


#Me retourne si oui ou non je peux placer une séquence sur une ligne i sans prendre en considération les cases déjà coloriées


def Tjl1(grille,i,j,l,LL1):
    
    if l==0:   
        return True


    Sl = LL1[i][l - 1]

    if (j < Sl - 1) :
        return False

    if (j == Sl - 1):
        if (l== 1):
            return True
        return False

    if (j > Sl - 1):
        if (grille[i][j]==BLANC):
            return Tjl(grille,i,j-1,l,LL1)

        elif (grille[i][j]==NOIR):
            return Tjl(grille,i,j-Sl-1,l-1,LL1)
            
    else:
        return Tjl(grille,i,j-Sl-1,l-1,LL1)

#version plus génerale de la fontion précedente: retourne vrai ou faux en prenant en compte les cases déjà coloriées
def Tjl(grille,i,j,l,LL1):

    if j<0:
        if l==0:
            return True
        return False

    if l==0:   
        for y in range(j+1):
            if grille[i][y]==NOIR: 
                return False
        return True

    Sl = LL1[i][l - 1]
    if Sl==0:
        return Tjl(grille,i,j,l-1,LL1)

    if (j < Sl - 1) :
        return False

    if (j == Sl - 1):
        if (l== 1):
            for y in range(0,j+1):
                if grille[i][y]==BLANC:
                    return False
            return True
        return False

    if (j > Sl - 1):
        if (grille[i][j]==BLANC):
            return Tjl(grille,i,j-1,l,LL1)

        elif (grille[i][j]==NOIR):
            if grille[i][j-Sl]==NOIR:
                return False
            if (j-Sl+1>=0 and j-Sl+1<j):
                for y in range(j-Sl+1,j):
                    if grille[i][y]==BLANC:
                        return False

            return Tjl(grille,i,j-Sl-1,l-1,LL1)

        elif (grille[i][j]==VIDE):

            grille2=copy.copy(grille)
            
            grille2[i][j]=NOIR
            return Tjl(grille,i,j-1,l,LL1) or Tjl(grille2,i,j,l,LL1) 
            
    else:
        return False


#colorie chaque ligne de la grille considérée grace à Tjl
def colorligne(grille2,i,l,L1,M,nouveau,ok):

    for j in range(M):
        
        if grille2[i][j]==VIDE:
            
            grille2[i][j]=BLANC
            bool1=Tjl(grille2,i,M-1,l,L1)
            #print("blanc:",bool1, i , j, "SL=",L1[i])

            grille2[i][j]=NOIR 
            bool2=Tjl(grille2,i,M-1,l,L1)
            #print("noir: ",bool2, i , j)
            
            if not bool1 and not bool2:
                print("c'est une abomination")
                ok=False
                return [ok,grille2,nouveau]

            elif bool1 and bool2:
                grille2[i][j]=VIDE
                
            elif bool1 and not bool2:
                grille2[i][j]=BLANC
                nouveau.append(j)
                
            elif not bool1 and bool2:
                grille2[i][j]=NOIR
                nouveau.append(j)


    return [ok,grille2,nouveau]


#considère chacune des lignes puis chacune des colonnes de la grille vide afin de colorier un maximum de cases
def Coloration(grille,N,M,L1,L2,LignesAVoir,ColonnesAVoir):
    
    grille2=copy.copy(grille)
    
    nouveau=[]
    ok=True

    V=[True,grille2,nouveau]

    while LignesAVoir or ColonnesAVoir :

        for i in LignesAVoir:
            l=len(L1[i])

            V=colorligne(grille2,i,l,L1,M,nouveau,ok) #doit colorier un max de case de la ligne i
            ok=V[0]
            grille2=V[1]
            nouveau=V[2]
            
            if ok==False:
                print("OK == FALSE")
                LignesAVoir=[]
                ColonnesAVoir=[]
                nouveau=[]
                return [ok,grille2]
        LignesAVoir=[]
        
        for x in nouveau:
            if x not in ColonnesAVoir:
                ColonnesAVoir.append(x)
        ColonnesAVoir.sort()
        nouveau=[]
        grille2=grille2.T
        
        for i in ColonnesAVoir:
            l=len(L2[i])

            V=colorligne(grille2,i,l,L2,N,nouveau,ok) #doit colorier un max de case de la ligne i
            ok=V[0]
            grille2=V[1]
            nouveau=V[2]

            if ok==False:
                print("OK == FALSE")
                LignesAVoir=[]
                ColonnesAVoir=[]
                nouveau=[]
                return [ok,grille2]

        ColonnesAVoir=[]

        for x in nouveau:
            if x not in LignesAVoir:
                LignesAVoir.append(x)
        LignesAVoir.sort()
        
        nouveau=[]
        grille2=grille2.T 


    if ok==True:
        for i in range(N):
            for j in range(M):
                if grille2[i][j]==VIDE:
                    ok="NeSaitPas"
                    break
    
    return[ok,grille2]

#Dans la partie 2 on ne considère plus une grille vide mais une grille partièlement coloriée, cette fonction complète le coloriage

def Color_propage(grille,i,j,c,L1,L2,N,M):
    
    grille2=copy.copy(grille)
    LignesAVoir=[]
    ColonnesAVoir=[]

    
    LignesAVoir.append(i)
    ColonnesAVoir.append(j)

    nouveau=[]
    ok=True
    V=[True,grille2,nouveau]

    while LignesAVoir or ColonnesAVoir :

        for ligne in LignesAVoir:
            l=len(L1[ligne])
            grille2[i][j]=c
            V=colorligne(grille2,ligne,l,L1,M,nouveau,ok) #doit colorier un max de case de la ligne i
            ok=V[0]
            grille2=V[1]
            nouveau=V[2]
            
            if ok==False:
                print("OK == FALSE")
                LignesAVoir=[]
                ColonnesAVoir=[]
                nouveau=[]
                return [ok,grille2]
        
        LignesAVoir=[]
        for x in nouveau:
            if x not in LignesAVoir:
                ColonnesAVoir.append(x)
        ColonnesAVoir.sort()
        
        ColonnesAVoir.append(j)
        ColonnesAVoir.sort()
        nouveau=[]
        grille2=grille2.T
        
        for col in ColonnesAVoir:
            l=len(L2[col])

            V=colorligne(grille2,col,l,L2,N,nouveau,ok) #doit colorier un max de case de la ligne i
            ok=V[0]
            grille2=V[1]
            nouveau=V[2]

            if ok==False:
                print("OK == FALSE")
                LignesAVoir=[]
                ColonnesAVoir=[]
                nouveau=[]
                return [ok,grille2]

        ColonnesAVoir=[]

        for x in nouveau:
            if x not in LignesAVoir:
                LignesAVoir.append(x)
        LignesAVoir.sort()
        
        nouveau=[]
        grille2=grille2.T 


    if ok==True:
        for i in range(N):
            for j in range(M):
                if grille2[i][j]==VIDE:
                    ok="NeSaitPas"
                    break
    
    return[ok,grille2]

#fonction qui énèmere les potentiels coloriages de la grille
def enum_rec(grilleu,indi_k,couleur,L1,L2,N,M):
    grille2=copy.copy(grilleu)
    if indi_k>=N*M:
        return True

    i=indi_k//N  # quotient de la division euclidienne
    j=indi_k % M  #% (reste de la division euclidienne)

    print(i,j)
    if grille2[i][j]==VIDE:
        Z=Color_propage(grille2,i,j,couleur,L1,L2,N,M)

        if Z[0]==False:
            return False
        if Z[0]==True:
            return [True,Z[1]]
        grille2=Z[1]

       
    indi_k+=1
    i=indi_k//M  # quotient de la division euclidienne
    j=indi_k % M  #% (reste de la division euclidienne)
    while i<N and j<M and grille2[i][j]!=VIDE:
        indi_k+=1
        i=indi_k//M  # quotient de la division euclidienne
        j=indi_k % M  #% (reste de la division euclidienne)
        
    bool1=enum_rec(grille2,indi_k,BLANC,L1,L2,N,M)
    return  bool1 or enum_rec(grille2,indi_k,NOIR,L1,L2,N,M)


#fonction complète de coloration, 
def Enumeration(grille,N,M,L1,L2,LignesAVoir,ColonnesAVoir):
    grille2=copy.copy(grille)

    Z=Coloration(grille2,N,M,L1,L2,LignesAVoir,ColonnesAVoir)

    if Z[0]==False:
        return [False,grille]
    if Z[0]==True:
        return [True,Z[1]]
    grille2=Z[1]

    bool1= enum_rec(grille2,0,BLANC,L1,L2,N,M)
    return bool1 or enum_rec(grille2,0,NOIR,L1,L2,N,M)



grille=cree_grille(N,M)

print(LL1, len(LL1))
print(LL2, len(LL2))

LignesAVoir=[]
ColonnesAVoir=[]


for i in range(N):
    LignesAVoir.append(i)

for i in range(M):
    ColonnesAVoir.append(i)
tps1 = time.time()

[a,b]=Coloration(grille,N,M,LL1,LL2,LignesAVoir,ColonnesAVoir)
#[a,b]=Enumeration(grille,N,M,LL1,LL2,LignesAVoir,ColonnesAVoir)

tps2 = time.time()


s=""
for i in range(N):
    for j in range(M):
        if b[i][j]==NOIR:
            s+='0 ' 
        if b[i][j]==BLANC:
            s+='_ '
        if b[i][j]==VIDE:
            s+='  '
    s+='\n'
 
print(s)
print(a)






print("Temps :",tps2 - tps1)