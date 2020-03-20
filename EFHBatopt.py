# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 18:23:17 2020

@author: s0536
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 13:46:29 2020

@author: s0536
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Nov 30 20:26:28 2019

@author: s0536
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 19:49:39 2019

@author: s0536
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 17:04:36 2019

@author: s0536
"""


import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from mpl_toolkits.mplot3d import Axes3D
import time
from pathlib import Path


####################   Systemkennwerte 
n_pv=0.2                
nsys_pv = 0.85            
Startkapazität=0
nsys_bat = 0.921
Kapazität=0

####################

Einspeisevergütung= 0.1048        #in €
Einspeisevergütung10kw= 0.1019          
Strompreis_Anbieter= 0.3          #0.3 
Strompreis_EEG=0.273                #0.273
####################

Simulationsschritte = 1        # paralell simulierte PV Kapazitäten       
plot = False
####################


timesteps =  52560 
Haushalte =  91#40    #91
###################

co2_Emmission_PV_pro_kWh= 0.04

####################              
# =============================================================================
# df=pd.read_csv('QuartierHH.csv',nrows=timesteps)
# # =============================================================================
# df2=pd.read_csv('Last_einzeln.csv',nrows=timesteps)
# df3=pd.read_csv('Dachflaechen.csv',nrows=Haushalte)
# =============================================================================
# =============================================================================
data_folder = Path(r"C:\Users\s0536\Downloads\Code") 
df=pd.read_csv(data_folder /'QuartierHH.csv',nrows=timesteps)
df2=pd.read_csv(data_folder /'Last_einzeln.csv',nrows=timesteps)
df3=pd.read_csv(data_folder / "Dachflaechen.csv",nrows=Haushalte)

#==========================
# df2=pd.read_csv(data_folder /"LAST_MFH.csv",nrows=timesteps)
# df3=pd.read_csv(data_folder / "DachflaechenMFH.csv",nrows=41)
# =============================================================================
np.sum(df2)
#Lastttt=np.sum(df2)
#Lastttt.to_csv('LastGW')

####################


Isued= df['sued']          
Iost= df['ost']
Iwest= df['west']
####################
Last = np.zeros(shape=(timesteps,Simulationsschritte))    #Erstellen leerer Matrizen
PVgen = np.zeros(shape=(timesteps,Simulationsschritte))
Bezug = np.zeros(shape=(timesteps,1))
Nsp = np.zeros(shape=(timesteps,1))
Renditeeo=np.zeros(shape=(1,4))
Rendite= pd.DataFrame()
RenditeVergleich=pd.DataFrame( np.zeros(shape=(1,4)))
install=pd.DataFrame()
aaa=pd.DataFrame()
bbb=pd.DataFrame()
ccc=pd.DataFrame()
ddd=pd.DataFrame()
eee=pd.DataFrame()
fff=pd.DataFrame()
Autarrrkie=pd.DataFrame()
Wiind=pd.DataFrame()
Griid=pd.DataFrame()
Solaar=pd.DataFrame()
####################
Dach=df3['Dach']             #Dach Süd       
Dachow=df3['Dachow']         #Dach Ost West
co2reihe=df['co2']
Wind= df['Wind']             #Abregelung Windeinspeisung 
Preis=df['Strompreis']
#Kapazität1=df3['Bat']
########### leere Listen für den Optimierungsblock
list=[]
listan=[]
listco=[]

plt.close()
############
batt=8
coanalyse=6
## Codeblock 1 - Simulation des Energiesystems:  k Haushalte werden nacheinander ##
#  über i Zeitschritte mit j Dachausnutzungsgraden simuliert                      # 
##                                                                               ##



for k in range (Haushalte):
  print('***    Haushalt:       ',k,'     ***')  
  for i in range(Last.shape[0]):
      for j in range(Last.shape[1]):  
            tess= df2[df2.columns[k]]
            Last[i,j]=tess[i]
        
  Dachausnutzung_sqm= (Dach[k]+Dachow[k])   
  einfach= np.zeros(shape=(timesteps))
  einfachost= np.zeros(shape=(timesteps))
  einfachwest= np.zeros(shape=(timesteps))
    
  for i in range(PVgen.shape[0]):
            einfach[i]= Isued[i] *  Dach[k] *n_pv*nsys_pv
            einfachost[i] = Iost[i] * Dachow[k]*0.5 *n_pv*nsys_pv
            einfachwest[i] = Iwest[i] * Dachow[k]*0.5 *n_pv*nsys_pv
  for i in range(PVgen.shape[0]):         
    for j in range(PVgen.shape[1]):
             
                   PVgen[i,j] = (einfach[i]+einfachost[i]+einfachwest[i])  
                   
  for m in range (coanalyse):
   cobat=700-(m*100)
   aaa=pd.DataFrame()
   bbb=pd.DataFrame()
   ccc=pd.DataFrame()
   ddd=pd.DataFrame()
   eee=pd.DataFrame()
   fff=pd.DataFrame()  
   ggg=pd.DataFrame()
   for l in range (batt): 
    Kapazität=2*l
                                       

                                           
       
    bataus = PVgen-Last
    
    for i in range(bataus.shape[0]):
        for j in range(bataus.shape[1]):
            if bataus[i,j]>0:
                bataus[i,j]=0
            elif bataus[i,j]<0:
                 bataus[i,j]=bataus[i,j]
                 
    batein = PVgen-Last
    
    
    for i in range(batein.shape[0]):
        for j in range(batein.shape[1]):
            if batein[i,j]<0:
                batein[i,j]=0
            elif batein[i,j]>0:
                 batein[i,j]=batein[i,j]  
    
    batkap=PVgen-Last
    
    for i in range(batkap.shape[0]):
        for j in range(batkap.shape[1]):
        
                if i in (0,1):
                 if batein[i,j]+bataus[i,j]+Startkapazität>0 :
               
            
                    batkap[i,j]=batein[i,j]+bataus[i,j]+Startkapazität    
                 else: batkap[i,j]=0
            
        
                else:    
                 if batein[i,j]+bataus[i,j]+batkap[i-1,j]>0 :
                     if batein[i,j]+bataus[i,j]+batkap[i-1,j]> Kapazität :
                        batkap[i,j]= Kapazität
                     else: batkap[i,j]=(batein[i,j]+bataus[i,j])*(1-(1-nsys_bat)/2)+batkap[i-1,j]
                        
                 else:
                    batkap[i,j]=0   
    
    ##############################################################
    
    
    diff= PVgen-Last
    Netzbezug= PVgen-Last
    
    for i in range(Netzbezug.shape[0]):
        for j in range(Netzbezug.shape[1]):
            if i < timesteps-1:
                if diff[i+1,j]+batkap[i,j]<0:
                    Netzbezug[i,j]= abs(diff[i+1,j]+batkap[i,j]*(1-(1-nsys_bat)/2))
                else: Netzbezug[i,j]= 0    
            else: Netzbezug[i,j]= abs(diff[i,j])                
    
    Netzbezug1 = np.zeros(shape=(Simulationsschritte))
    for i in range(Netzbezug1.shape[0]):
           Netzbezug1[i] = np.around(np.sum(Netzbezug, axis=0), decimals=2)[i]
           
    
    ####
    Netzeinspeisung= PVgen-Last
    
    siebzig = np.zeros(shape=(Simulationsschritte))
    for i in range(Netzbezug1.shape[0]):
        siebzig[i]= (Dach[k]+ Dachow[k])*(i+1)*n_pv *0.7 
    for i in range(Netzeinspeisung.shape[0]):
       for j in range(Netzeinspeisung.shape[1]): 
        if i in (0,1):
            Netzeinspeisung[i,j]=0
               
               
        else:    
            if Netzbezug[i,j] == 0 :
               if batkap[i-1,j] == Kapazität :
                 if batein[i,j] < siebzig[j]:
                   Netzeinspeisung[i,j]= batein[i,j]
                 if batein[i,j] > siebzig[j]:  
                   Netzeinspeisung[i,j]= siebzig[j]  
               else: Netzeinspeisung[i,j]= 0
                    
            else:
                Netzeinspeisung[i,j]= 0
    
    Netzeinspeisung1 = np.zeros(shape=(Simulationsschritte))
    for i in range(Netzeinspeisung1.shape[0]):
           Netzeinspeisung1[i] = np.around(np.sum(Netzeinspeisung, axis=0), decimals=2)[i]            
    
    
    #####
          
    
    ## Codeblock 2 - Berechnung der Optimierungsparameter: Aus den Ergebnissen                    ##   
    #  von Codeblock 1 werden die 7 Optimierungsparameter Autarkie, Grid Support Coefficient,      #
    #  Konfliktfreiheit mit Windeinspeisung, CO² Einsparung, Wirtschaftlichkeit, Zukunftsfähigkeit,#
    ## Speicherpotential (Speicherpotential ist hier nicht implementiert) berechnet.              ##
    
    co2sparung= np.zeros(shape=(timesteps,Simulationsschritte))
    
    
    for i in range(co2sparung.shape[0]):
      for j in range(co2sparung.shape[1]):
         co2sparung[i,j]= (Last[i,j] - Netzbezug[i,j])*co2reihe[i]
    
    
    co2speisung= np.zeros(shape=(timesteps,Simulationsschritte))
    
    for i in range(co2speisung.shape[0]):
      for j in range(co2speisung.shape[1]):
        if Netzeinspeisung[i,j] > 0 and Wind[i]<1:
            co2speisung[i,j]= Netzeinspeisung[i,j]*co2reihe[i]
        else: co2speisung[i,j]=0
    
    
    co2= np.zeros(shape=(Simulationsschritte))
    
    for i in range(co2.shape[0]):     
           co2[i]= (np.sum(co2sparung, axis=0)[i]- co2_Emmission_PV_pro_kWh* np.sum(PVgen, axis=0)[i]- Kapazität * 3.75+ np.sum(co2speisung, axis=0)[i])/1000
    
    
    ##############################################################
    Konflikt=np.zeros(shape=(timesteps,Simulationsschritte))
    
    for i in range(Netzeinspeisung.shape[0]):
      for j in range(Netzeinspeisung.shape[1]):
        if Netzeinspeisung[i,j] > 0:
            if Wind[i] == 1:
                Konflikt[i,j] = 1
            
            else: Konflikt[i,j] = 0
        
        else: Konflikt[i,j] = 0
    
    Konflikt_sum = timesteps - np.sum(Konflikt, axis =0)
    #################################################################
  
    GSC_top = np.zeros(shape=(timesteps,Simulationsschritte))
    GSC_top2 = np.zeros(shape=(timesteps,Simulationsschritte))
    
    for i in range(GSC_top.shape[0]):
            for j in range(GSC_top.shape[1]):
               GSC_top[i,j] = (Netzeinspeisung[i,j]+Last[i,j]-Netzbezug[i,j])*Preis[i] 
               
    GSC=np.around(np.sum(GSC_top, axis=0)/((np.sum(Netzeinspeisung,axis=0)+np.sum(Last-Netzbezug,axis=0))*np.sum(Preis,axis=0)/timesteps) , decimals=3)      
         
# =============================================================================
#     for i in range(GSC_top.shape[0]):
#         for j in range(GSC_top.shape[1]):
#            GSC_top[i,j] = Netzeinspeisung[i,j]*Preis[i] 
#            
#     GSC_Einspeisung=np.around(np.sum(GSC_top, axis=0)/(np.sum(Netzeinspeisung,axis=0)*np.sum(Preis,axis=0)/timesteps) , decimals=3)      
#         
#     for i in range(GSC_top.shape[0]):
#         for j in range(GSC_top.shape[1]):
#            GSC_top2[i,j] = (Last[i,j]-Netzbezug[i,j])*Preis[i]        
#     
#     GSC_Eigenverbrauch = np.around(np.sum(GSC_top2, axis=0)/(np.sum((Last-Netzbezug),axis=0)*np.sum(Preis,axis=0)/timesteps) , decimals=3)      
#     
#     GSC= (GSC_Einspeisung+GSC_Eigenverbrauch)/2
# =============================================================================
    
    #################################################################
    
    Ersparniss= np.zeros(shape=(Simulationsschritte))
    
    EinspeisevergütungEEG= np.zeros(shape=(Simulationsschritte)) 
    for i in range(EinspeisevergütungEEG.shape[0]):
         if (i+1 )* (Dach[k]+Dachow[k])*0.2 < 10 : 
             EinspeisevergütungEEG[i]= Einspeisevergütung
         else:
             EinspeisevergütungEEG[i]= ((((i+1)*(Dach[k]+Dachow[k])*0.2)-10)* Einspeisevergütung10kw + 10 * Einspeisevergütung)/((i+1)*(Dach[k]+Dachow[k])*0.2)
        
    
  
    
    for i in range(Ersparniss.shape[0]):
         if (i+1 )* (Dach[k]+Dachow[k])*0.2 < 10 :  
           Ersparniss[i]= (np.sum(Last, axis=0)[i] -  (np.sum(Netzbezug, axis=0)[i])) *Strompreis_Anbieter + (np.sum(Netzeinspeisung, axis=0)[i]) * EinspeisevergütungEEG[i]
         else:
           Ersparniss[i]= (np.sum(Last, axis=0)[i] -  (np.sum(Netzbezug, axis=0)[i])) *Strompreis_EEG + (np.sum(Netzeinspeisung, axis=0)[i]) * EinspeisevergütungEEG[i]  
    ##

   
    Installationskosten = np.zeros(shape=(1,Simulationsschritte))
    for i in range(1):
       for j in range(Simulationsschritte):
         if  (Dach[k]+Dachow[k])*0.2 < 4 :  
           Installationskosten[i,j]= 350* (Dach[k] +  Dachow[k])  + Kapazität*cobat             
         if 4 <=  (Dach[k]+Dachow[k])*0.2 < 6 :
          Installationskosten[i,j]= 330 * (Dach[k] + Dachow[k])  + Kapazität*cobat
         if 6 <=  (Dach[k]+Dachow[k])*0.2 <= 10 :
          Installationskosten[i,j]= 310 * (Dach[k] +  Dachow[k])  + Kapazität*cobat 
         if  (Dach[k]+Dachow[k])*0.2 > 10 :
          Installationskosten[i,j]= 280 * (Dach[k] +  Dachow[k])  + Kapazität*cobat
         if (Dach[k]+Dachow[k])*0.2 > 18 :
          Installationskosten[i,j]= 240 * (Dach[k] +  Dachow[k]) + Kapazität*cobat           
  
    
        
    #ROI= Installationskosten/Ersparniss
    
    ##
    Installationskosten20 = np.zeros(shape=(1,Simulationsschritte))
    for i in range(1):
       for j in range(Simulationsschritte):
           if  (Dach[k]+Dachow[k])*0.2 < 8 :
            Installationskosten20[i,j]= Installationskosten[i,j]+(148+5* (Dach[k]+Dachow[k])*0.2)*20   
           else:   
            Installationskosten20[i,j]= Installationskosten[i,j]+(148+21+5* (Dach[k]+Dachow[k])*0.2)*20    
   
    anual= ((Ersparniss*20 /Installationskosten20) ** (1/20) -1)*100
    
    ##############################################################
    
# =============================================================================
#     Dachausnutzung_sqm = np.zeros(shape=(Simulationsschritte))
#     for i in range(Dachausnutzung_sqm.shape[0]):           
#                Dachausnutzung_sqm[i] = (i+1 )* (Dach[k]+Dachow[k])  
# =============================================================================
                      
# =============================================================================
#     Dachausnutzung_per = np.zeros(shape=(Simulationsschritte))
#     for i in range(Dachausnutzung_per.shape[0]):
#                Dachausnutzung_per[i] = Dachausnutzung_sqm[i]/(Dach[k]+Dachow[k]) *100  
#     
# =============================================================================
        
    ###############################################################
    
    Aut = np.zeros(shape=(Simulationsschritte))
    for i in range(Aut.shape[0]):
           Aut[i] = ((np.sum(Last, axis=0)[i] -  (np.sum(Netzbezug, axis=0)[i]))/np.sum(Last, axis=0)[i])*100 
              
    
    
    #################################################################
    
    zukunft= np.zeros(shape=(Simulationsschritte))            
    for i in range(zukunft.shape[0]):
     
           zukunft[i]=np.sum(PVgen, axis=0)[i]
  
    ##################################################################
    batterieopt= np.zeros(shape=(Simulationsschritte))            
    for i in range(batterieopt.shape[0]):
     
           batterieopt[i]=Kapazität/(Dachausnutzung_sqm/5)
    
    print(' ')
    print('****                 Ergebnisse                  ****        ')
    print(' ')
    print('Haushalt                  ', (k+1))
    print('PV Fläche in m²           ', Dachausnutzung_sqm )
    print('Autarkiegrad in %         ',np.around(Aut, decimals=2))
    print('CO2 Einsparung [t/a]:     ',np.around(co2, decimals=2))
    print('jährl. Rendite            ',np.around(anual, decimals=2))
    print('Grid support coefficient  ',GSC )
    print('Konfliktfreiheit Wind     ',Konflikt_sum )
    print('Kap',Kapazität)
    
   ###################################################################

    
   ######################################################################
   
   ## Codeblock 3 - Optimierung: Durch TOPSIS Optimierung wird die optimale PV-  ##
   #  Anlagengröße errechnet und ausgegeben                                       #
   ##                                                                            ##
   
    aa=pd.DataFrame(Aut)        
    aaa= aaa.append(pd.DataFrame(aa))
    bb=pd.DataFrame(co2)  
    bbb= bbb.append(pd.DataFrame(bb))
    anual[anual < 0] = 0
    cc=pd.DataFrame(anual)
    ccc= ccc.append(pd.DataFrame(cc))
    dd=pd.DataFrame(GSC)    
    ddd= ddd.append(pd.DataFrame(dd))
    cc=cc.T   
    cc[cc < 0] = 0
    
    ee=pd.DataFrame(Konflikt_sum)  
    eee= eee.append(pd.DataFrame(ee))
    ff=pd.DataFrame(zukunft)
    fff= fff.append(pd.DataFrame(ff))
    gg=pd.DataFrame(batterieopt)
    ggg= ggg.append(pd.DataFrame(gg))
    #index=['0','2','4','6','8','10' ]   #,'4','6','8','10'     
    index=['0','2','4','6','8','10','12','14' ] 
    #print('optimale Anlagengröße:     ',(Dach[k]+Dachow[k])*0.2,'kWp')
    #listan.append(anual)
    #listco.append(co2)
    #nb1= Netzbezug
    #ne1= Netzeinspeisung
    #print(np.sum(nb1))
    #print(np.sum(ne1))
    #Bezuggesamt = Bezug+nb1
    #Nspgesamt = Nsp+ne1 
    #print(np.sum(Bezuggesamt))
    #print(np.sum(Nspgesamt))
    #Bezug=Bezuggesamt
    #Nsp=Nspgesamt
    ####
    
    #anual[anual < 0] = 0
    #if    anual==0: 
    #     anual=0.2
    #Renditeeo=[[float(np.around(anual.max(axis=1),3)),float(np.where(anual == np.amax(anual))[1]),float(final),float(np.around(anual,3))]]    
    #Rendite= Rendite.append(pd.DataFrame(anual))
    #RenditeVergleich=RenditeVergleich.append(pd.DataFrame(Renditeeo))
    ####
    #PVgensum=np.sum(PVgen, axis =0)
    #installP= [(final+1)*(Dach[k]+Dachow[k])*0.2]
    #install= install.append(pd.DataFrame(installP))
    #Autarrrkie=Autarrrkie.append(pd.DataFrame(Aut))
    #Wiind=Wiind.append(pd.DataFrame(Konflikt_sum))
    #Griid=Griid.append(pd.DataFrame(GSC))
    #Solaar=Solaar.append(pd.DataFrame(PVgensum)) 
##############################################     
     
##############################################
# =============================================================================
# =============================================================================
# =============================================================================
   opt=pd.concat([aaa, bbb,ccc,ddd,eee,fff,ggg], axis=1) 
   opt=opt.set_index([index])
   opt.columns = ['Aut', 'co2', 'anual','GSC', 'Konfliktfreiheit','Zukunft','Bat']     
   col_sums = np.cumsum(opt**2,axis=0)
   wurzel= np.sqrt(col_sums)
   max1=wurzel.max()
   weight = np.array([0.1,0.3,0.3,0.1,0.1,0.1,0.0])
   Decision=opt/max1*weight
   max2=Decision.max()
   min1=Decision.min()
   Ideal=np.sqrt(np.cumsum((Decision-max2)**2,axis=1))
   max3=Ideal['Bat']
   nonIdeal=np.sqrt(np.cumsum((Decision-min1)**2,axis=1))
   min2=nonIdeal['Bat']
     
   relDist=min2/(max3+min2) 
       
   final=relDist.idxmax()
   list.append(final)
   print(cobat)
   print(final , relDist.max())        
# =============================================================================
# tt = pd.DataFrame(Bezuggesamt)    
# tt.to_csv('Bezuggesamt')
# st = pd.DataFrame(Nspgesamt)    
# st.to_csv('Einspeisunggesamt')  
# rt = pd.DataFrame(listco)    
# rt.to_csv('co2')
# =============================================================================
qt = pd.DataFrame(list)    
qt.to_csv('Optimallösung')


#RenditeVergleich.to_csv('VergleichRendite')  

# =============================================================================
# Rendite.to_csv('Rendite')  
# install.to_csv('instLeistung')
# Autarrrkie.to_csv('Autarkie')
# Wiind.to_csv('Wind')
# Griid.to_csv('GSC')
# Solaar.to_csv('PVSTROM')
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# =============================================================================
# np.sum(Last)
# np.sum(Netzbezug)
# np.sum(Netzeinspeisung)
# 
# eigenverbrrr=np.sum(Last)-np.sum(Netzbezug)
# 
# eigenverbrrr/np.sum(PVgen)
# 
# =============================================================================








