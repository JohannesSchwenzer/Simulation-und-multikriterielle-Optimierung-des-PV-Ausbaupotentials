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


####################   Simulationseinstellungen

Simulationsschritte = 10        # paralell simulierte PV Kapazitäten in %
                                # Dachausnutzung
                                
timesteps =  52560              # simulierte Zeitschritte
Batteriekapazitäten = 3         # Anzahl simulierter Batteriekapazitäten pro 
                                # Haushalt in (1 kWh Kapazität/ Schritt)-1
Batrange = range(Batteriekapazitäten)                                
Haushalte =  91                 # Anzahl simulierter Haushalte

####################   Systemkennwerte etc. 
n_pv=0.2                        # Modulwirkungsgras
nsys_pv = 0.85                  # Systemwirkungsgrad
Startkapazität=0                # Starkapazität Berlin 
nsys_bat = 0.921                # Batteriewirkungsgrad
Einspeisevergütung= 0.1075      # in €
Einspeisevergütung10kw= 0.105        
Strompreis_Anbieter= 0.3         
Strompreis_EEG= 0.273
co2_Emmission_PV_pro_kWh= 0.04  # in kg/kWh


####################   Einlesen der Daten            
df=pd.read_csv('QuartierHH.csv',nrows=timesteps)
df2=pd.read_csv('Last_einzeln.csv',nrows=timesteps)
df3=pd.read_csv('Dachflaechen.csv',nrows=Haushalte)

Isued= df['sued']          
Iost= df['ost']
Iwest= df['west']
Kapazität1=df3['Bat']
Dach=df3['Dach']             # Dachfläche Süd       
Dachow=df3['Dachow']         # Dachfläche Ost West
co2reihe=df['co2']           # CO2 Emmissionen Strommix 
Wind= df['Wind']             # Abregelung Windeinspeisung 
Preis=df['Strompreis']       # Strompreis


##################### Erstellen leerer Matrizen und Listen

Last = np.zeros(shape=(timesteps,Simulationsschritte))    
PVgen = np.zeros(shape=(timesteps,Simulationsschritte))
list=[]



# Codeblock 1 - Simulation des Energiesystems: k Haushalte werden nacheinander 
# über i Zeitschritte mit j Dachausnutzungsgraden simuliert                       
                                                                               

for k in range (2): 
    matco=pd.DataFrame()
    matwind = pd.DataFrame()
    matrendite = pd.DataFrame()
    mataut = pd.DataFrame()
    matgsc = pd.DataFrame()
    matzukunft = pd.DataFrame()  

    for i in range(Last.shape[0]):
     for j in range(Last.shape[1]):  
        tess= df2[df2.columns[k]]
        Last[i,j]=tess[i]
    
      
    einfach= np.zeros(shape=(timesteps))
    einfachost= np.zeros(shape=(timesteps))
    einfachwest= np.zeros(shape=(timesteps))
    
    for i in range(PVgen.shape[0]):
             einfach[i]= Isued[i] *  Dach[k]/10 *n_pv*nsys_pv
             einfachost[i] = Iost[i] * Dachow[k]/10*0.5 *n_pv*nsys_pv
             einfachwest[i] = Iwest[i] * Dachow[k]/10*0.5 *n_pv*nsys_pv
    for i in range(PVgen.shape[0]):         
      for j in range(PVgen.shape[1]):
             
          PVgen[i,j] = (einfach[i]+einfachost[i]+einfachwest[i]) *(j+1)                                         
                                      
       
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
                 
    for m in range (Batteriekapazitäten):  
        Kapazität= 1 * m 
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
            siebzig[i]= (Dach[k]/10+ Dachow[k]/10)*(i+1)*n_pv *0.7 
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
              
        
        # Codeblock 2 - Berechnung der Optimierungsparameter: Aus den Ergebnissen                        
        # von Codeblock 1 werden die 6 Optimierungsparameter Autarkie, Grid Support Coefficient,       
        # Konfliktfreiheit mit Windeinspeisung, CO² Einsparung, Wirtschaftlichkeit, Zukunftsfähigkeit
        
        ### CO2 
        
        co2sparung= np.zeros(shape=(timesteps,Simulationsschritte))
        
        
        for i in range(co2sparung.shape[0]):
          for j in range(co2sparung.shape[1]):
             co2sparung[i,j]= (Last[i,j] - Netzbezug[i,j])*co2reihe[i]
        
        
        co2speisung= np.zeros(shape=(timesteps,Simulationsschritte))
        
        for i in range(co2speisung.shape[0]):
          for j in range(co2speisung.shape[1]):
            if Netzeinspeisung[i,j] > 0 and Wind[i] < 1 :
                co2speisung[i,j]= Netzeinspeisung[i,j]*co2reihe[i]
          
        
        
        co2= np.zeros(shape=(Simulationsschritte))
        
        for i in range(co2.shape[0]):     
               co2[i]= (np.sum(co2sparung, axis=0)[i]- co2_Emmission_PV_pro_kWh* np.sum(PVgen, axis=0)[i]- Kapazität * 3.75+ np.sum(co2speisung, axis=0)[i])/1000
        
        
        ### Konflikte mit Windenergie
        
        Konflikt=np.zeros(shape=(timesteps,Simulationsschritte))
        
        for i in range(Netzeinspeisung.shape[0]):
          for j in range(Netzeinspeisung.shape[1]):
            if Netzeinspeisung[i,j] > 0:
                if Wind[i] == 1:
                    Konflikt[i,j] = 1
                
                else: Konflikt[i,j] = 0
            
            else: Konflikt[i,j] = 0
        
        Konflikt_sum = timesteps - np.sum(Konflikt, axis =0)
        
        ### Netzdienlichkeitskoeffizient
      
        GSC_top = np.zeros(shape=(timesteps,Simulationsschritte))
        GSC_top2 = np.zeros(shape=(timesteps,Simulationsschritte))
        
        for i in range(GSC_top.shape[0]):
            for j in range(GSC_top.shape[1]):
               GSC_top[i,j] = Netzeinspeisung[i,j]*Preis[i] 
               
        GSC_Einspeisung=np.around(np.sum(GSC_top, axis=0)/(np.sum(Netzeinspeisung,axis=0)*np.sum(Preis,axis=0)/timesteps) , decimals=3)      
            
        for i in range(GSC_top.shape[0]):
            for j in range(GSC_top.shape[1]):
               GSC_top2[i,j] = (Last[i,j]-Netzbezug[i,j])*Preis[i]        
        
        GSC_Eigenverbrauch = np.around(np.sum(GSC_top2, axis=0)/(np.sum((Last-Netzbezug),axis=0)*np.sum(Preis,axis=0)/timesteps) , decimals=3)      
        
        GSC= (GSC_Einspeisung+GSC_Eigenverbrauch)/2
        
        ### Wirtschaftlichkeit
        
        Ersparniss= np.zeros(shape=(Simulationsschritte))
        
        EinspeisevergütungEEG= np.zeros(shape=(Simulationsschritte)) 
        for i in range(EinspeisevergütungEEG.shape[0]):
             if (i+1 )* (Dach[k]/10+Dachow[k]/10)*0.2 < 10 : 
                 EinspeisevergütungEEG[i]= Einspeisevergütung
             else:
                 EinspeisevergütungEEG[i]= ((((i+1)*(Dach[k]/10+Dachow[k]/10)*0.2)-10)* Einspeisevergütung10kw + 10 * Einspeisevergütung)/((i+1)*(Dach[k]/10+Dachow[k]/10)*0.2)
            
        
      
        
        for i in range(Ersparniss.shape[0]):
             if (i+1 )* (Dach[k]/10+Dachow[k]/10)*0.2 < 10 :  
               Ersparniss[i]= (np.sum(Last, axis=0)[i] -  (np.sum(Netzbezug, axis=0)[i])) *Strompreis_Anbieter + (np.sum(Netzeinspeisung, axis=0)[i]) * EinspeisevergütungEEG[i]
             else:
               Ersparniss[i]= (np.sum(Last, axis=0)[i] -  (np.sum(Netzbezug, axis=0)[i])) *Strompreis_EEG + (np.sum(Netzeinspeisung, axis=0)[i]) * EinspeisevergütungEEG[i]  
        ##
    
        Installationskosten = np.zeros(shape=(1,Simulationsschritte))
        for i in range(1):
           for j in range(Simulationsschritte):
             if (j+1 )* (Dach[k]/10+Dachow[k]/10)*0.2 < 4 :  
               Installationskosten[i,j]= (j+1)*350 * (Dach[k]/10 +  Dachow[k]/10)  + Kapazität*700             
             if 4 <= (j+1 )* (Dach[k]/10+Dachow[k]/10)*0.2 < 6 :
              Installationskosten[i,j]= (j+1)*330 * (Dach[k]/10 + Dachow[k]/10)  + Kapazität*700
             if 6 <= (j+1 )* (Dach[k]/10+Dachow[k]/10)*0.2 <= 10 :
              Installationskosten[i,j]= (j+1)*310 * (Dach[k]/10 +  Dachow[k]/10)  + Kapazität*700 
             if (j+1 )* (Dach[k]/10+Dachow[k]/10)*0.2 > 10 :
              Installationskosten[i,j]= (j+1)*280 * (Dach[k]/10 +  Dachow[k]/10)  + Kapazität*700 
               
        Installationskosten20 = np.zeros(shape=(1,Simulationsschritte))
        for i in range(1):
           for j in range(Simulationsschritte):
               if (j+1 )* (Dach[k]/10+Dachow[k]/10)*0.2 < 8 :
                Installationskosten20[i,j]= Installationskosten[i,j]+(148+5*(j+1 )* (Dach[k]/10+Dachow[k]/10)*0.2)*20   
               else:   
                Installationskosten20[i,j]= Installationskosten[i,j]+(148+21+5*(j+1 )* (Dach[k]/10+Dachow[k]/10)*0.2)*20    
       
        anual= ((Ersparniss*20 /Installationskosten20) ** (1/20) -1)*100
        
        ##############################################################
        
        Dachausnutzung_sqm = np.zeros(shape=(Simulationsschritte))
        for i in range(Dachausnutzung_sqm.shape[0]):           
                   Dachausnutzung_sqm[i] = (i+1 )* (Dach[k]/10+Dachow[k]/10)  
                              
        Dachausnutzung_per = np.zeros(shape=(Simulationsschritte))
        for i in range(Dachausnutzung_per.shape[0]):
                   Dachausnutzung_per[i] = Dachausnutzung_sqm[i]/(Dach[k]+Dachow[k]) *100  
                
        ### Autarkie
        
        Aut = np.zeros(shape=(Simulationsschritte))
        for i in range(Aut.shape[0]):
               Aut[i] = ((np.sum(Last, axis=0)[i] -  (np.sum(Netzbezug, axis=0)[i]))/np.sum(Last, axis=0)[i])*100 
                  
        
        
        ### Zukunftsfähigkeit
        
        zukunft= np.zeros(shape=(Simulationsschritte))            
        for i in range(zukunft.shape[0]):
         
               zukunft[i]=np.sum(PVgen, axis=0)[i]
      
        ##################################################################
        print(' ')
        print('****                 Ergebnisse                  ****        ')
        print(' ')
        print('Haushalt                  ', (k+1))
        print('PV Fläche in m²           ', Dachausnutzung_sqm )
        print('Kapazität                 ', Kapazität )
        print('Autarkiegrad in %         ',np.around(Aut, decimals=2))    
        print('CO2 Einsparung [t/a]:     ',np.around(co2, decimals=2))
        print('jährl. Rendite            ',np.around(anual, decimals=2))
        print('Grid support coefficient  ',GSC )
        print('Konfliktfreiheit Wind     ',Konflikt_sum )        
       ######################################################################
       
        
       
       ## Codeblock 3 - Optimierung: Durch TOPSIS Optimierung wird die optimale
       #PV-Anlagengröße und Batteriegröße errechnet und ausgegeben                                       #
                                                                                   
        # Erstellen der Entscheidungssmatrix
        aa=pd.DataFrame(Aut)    
        mataut= mataut.append(aa, ignore_index=True)  
        bb=pd.DataFrame(co2)
        matco= matco.append(bb, ignore_index=True)  
        cc=pd.DataFrame(anual)
        cc=cc.T
        cc[cc < 0] = 0
        matrendite= matrendite.append(cc, ignore_index=True)  
        dd=pd.DataFrame(GSC) 
        matgsc= matgsc.append(dd, ignore_index=True)  
        ee=pd.DataFrame(Konflikt_sum)  
        matwind= matwind.append(ee, ignore_index=True)                  
        ff=pd.DataFrame(zukunft)
        matzukunft= matzukunft.append(ff, ignore_index=True)
        
      #sind alle Möglichkeiten simuliert, wird das optimale Ergebnis berechnet:
        if m+1 == len(Batrange):
            #Entscheidungsmatrix
            opt=pd.concat([mataut, matco,matrendite,matgsc,matwind,matzukunft], axis=1)  
                 
            opt.columns = ['Aut', 'co2', 'anual','GSC', 'Konfliktfreiheit','Zukunft']     
            col_sums = np.cumsum(opt**2,axis=0)
            wurzel= np.sqrt(col_sums)
            max1=wurzel.max()
            weight = np.array([0.1,0.3,0.3,0.1,0.1,0.1]) #Gewichtungsvektor
            Decision=opt/max1*weight #normalisierte gewichtete Entscheidungsmatrix  
            max2=Decision.max()
            min1=Decision.min()
            Ideal=np.sqrt(np.cumsum((Decision-max2)**2,axis=1)) #Ideallösung
            max3=Ideal['Zukunft']
            nonIdeal=np.sqrt(np.cumsum((Decision-min1)**2,axis=1)) #Antiideallösung
            min2=nonIdeal['Zukunft']
         
            relDist=min2/(max3+min2) #relative Distanz
           
            final=relDist.idxmax()  # Optimalergebnis
            list.append(final)
            #print(final , relDist.max())
            optpv=int(str(final)[1:2])
            optbat=int(str(final)[0:1])
            print('optimale Anlagengröße:     ',(optpv+1)*(Dach[k]/10+Dachow[k]/10)*0.2,'kWp')
            print('optimale Batteriegröße:    ', optbat, 'kWh' )
    
