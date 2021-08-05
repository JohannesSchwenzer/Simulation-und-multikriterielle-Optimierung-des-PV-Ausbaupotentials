# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 23:00:16 2020

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



timesteps=52560
Haushalte =  91
Batrange = range(6)           # Anzahl simulierter Batteriekapazitaeten in kWh-1


df=pd.read_csv('QuartierHH.csv',nrows=timesteps)
df2=pd.read_csv('Last_einzeln.csv',nrows=timesteps)
df3=pd.read_csv('Dachflaechen.csv',nrows=Haushalte)
####################
n_pv=0.2                
nsys_pv = 0.85            
Startkapazitaet=0
nsys_bat = 0.921
##################
Einspeiseverguetung= 0.1075        #in €
Einspeiseverguetung10kw= 0.105        
Strompreis_Anbieter= 0.3 
Strompreis_EEG= 0.273
###################
co2_Emmission_PV_pro_kWh= 0.04



Isued= df['sued']          
Iost= df['ost']
Iwest= df['west']
####################
Dach=df3['Dach']             #Dach Sued       
Dachow=df3['Dachow']         #Dach Ost West
co2reihe=df['co2']
Wind= df['Wind']             #Abregelung Windeinspeisung 
Preis=df['Strompreis']
Kapazitaet1=df3['Bat']
##################


PVgen = np.zeros(shape=(timesteps))
Last  = np.zeros(shape=(timesteps))
batkap  = np.zeros(shape=(timesteps))

alle_werte =pd.DataFrame()
optimalwerte=pd.DataFrame()

def PVgenerated(k):
  print('Haushalt:',k) 
  
  einfach= [Isued[i] *  Dach[k] *n_pv*nsys_pv for i in range(timesteps)]
  einfachost = [Iost[i] * Dachow[k]*0.5 *n_pv*nsys_pv for i in range(timesteps)]
  einfachwest = [Iwest[i] * Dachow[k]*0.5 *n_pv*nsys_pv for i in range(timesteps)]
  PVgen = [(einfach[i]+einfachost[i]+einfachwest[i]) for i in range(timesteps)] 
  return PVgen

def Lastfct(k):
  tess= df2[df2.columns[k]]
  Last=tess  
  return Last


class cl1():
  def __init__(self,k):  
   self.PVgen= PVgenerated(k)
   self.zukunft=np.sum(self.PVgen)
   self.Last= Lastfct(k)  
   self.siebzig= Dach[k]+ Dachow[k]*n_pv *0.7 
   self.Kapazitaet= Kapazitaet1[k]
   self.Anlage = (Dach[k]+Dachow[k])*0.2
   self.preisavg= np.sum(Preis)/timesteps
class cl2:
  def __init__(self,k): 
   self.bataus=[p1.PVgen[i]-p1.Last[i] if p1.PVgen[i]-p1.Last[i]<0 else 0 for i in range(timesteps) ]
   self.batein=[p1.PVgen[i]-p1.Last[i] if p1.PVgen[i]-p1.Last[i]>0 else 0 for i in range(timesteps) ]

class cl3:
  def __init__(self,k): 
   self.batkap= np.zeros(shape=(timesteps))   
   for i in range(timesteps):
  
    if p2.batein[i]+p2.bataus[i]+self.batkap[i-1]>0 :
        if p2.batein[i]+p2.bataus[i]+self.batkap[i-1]> Kapazitaet :
                    self.batkap[i]= Kapazitaet
        else: self.batkap[i]=(p2.batein[i]+p2.bataus[i])*(1-(1-nsys_bat)/2)+self.batkap[i-1]
                    
    else:
       self.batkap[i]=0     

class cl4:
  def __init__(self,k):        
      diff= p1.PVgen-p1.Last
      self.Netzbezug= np.zeros(shape=(timesteps))   
      for i in range(timesteps):   
            if i < timesteps-1:
                if diff[i+1]+p3.batkap[i]<0:
                    self.Netzbezug[i]= abs(diff[i+1]+p3.batkap[i]*(1-(1-nsys_bat)/2))
                else: self.Netzbezug[i]= 0    
            else: self.Netzbezug[i]= abs(diff[i])    
            
      self.Netzeinspeisung= np.zeros(shape=(timesteps))      
      for i in range(timesteps):        
        if self.Netzbezug[i] == 0 :
           if p3.batkap[i-1] == Kapazitaet :
             if p2.batein[i] < p1.siebzig:
               self.Netzeinspeisung[i]= p2.batein[i]
             if p2.batein[i] > p1.siebzig:  
               self.Netzeinspeisung[i]= p1.siebzig  
           else: self.Netzeinspeisung[i]= 0
                
        else:
            self.Netzeinspeisung[i]= 0
      
      self.Eigenverbrauch = p1.Last -  self.Netzbezug
        
class co2calc:
  def __init__(self,k):  
     self.co2sparung=[(p1.Last[i] - p4.Netzbezug[i])*co2reihe[i] for i in range (timesteps)]
     self.co2speisung= [p4.Netzeinspeisung[i]*co2reihe[i] if p4.Netzeinspeisung[i] > 0 and Wind[i] < 1 else 0 for i in range (timesteps)] 
     self.co2=(np.sum(self.co2sparung)+np.sum(self.co2speisung)- co2_Emmission_PV_pro_kWh* np.sum(p1.PVgen)- Kapazitaet * 3.75)/1000 


class Konfliktcalc:
 def __init__(self,k):
   self.Konflikt=[1 if p4.Netzeinspeisung[i] > 0 and Wind[i]==1 else 0 for i in range (timesteps)]
   self.Konflikt_sum = timesteps - np.sum(self.Konflikt)


class Renditecalc:
 def __init__(self,k):
    if p1.Anlage  < 10 : 
        self.EinspeiseverguetungEEG= Einspeiseverguetung
        self.Ersparniss= (np.sum(p1.Last) -  np.sum(p4.Netzbezug)) *Strompreis_Anbieter + np.sum(p4.Netzeinspeisung) * self.EinspeiseverguetungEEG
    else:
        self.EinspeiseverguetungEEG= ((p1.Anlage-10)* Einspeiseverguetung10kw + 10 * Einspeiseverguetung)/(p1.Anlage)
        self.Ersparniss= (np.sum(p1.Last) - np.sum(p4.Netzbezug)) *Strompreis_EEG + np.sum(p4.Netzeinspeisung) * self.EinspeiseverguetungEEG  

    if p1.Anlage < 4 :  
        self.Installationskosten= 1750 * p1.Anlage + Kapazitaet*700             
    elif 4 <= p1.Anlage < 6 :
        self.Installationskosten= 1650 * p1.Anlage + Kapazitaet*700
    elif 6 <= p1.Anlage <= 10 :
        self.Installationskosten= 1550 * p1.Anlage + Kapazitaet*700 
    else :
        self.Installationskosten= 1400 * p1.Anlage + Kapazitaet*700 
    

    if p1.Anlage < 8 :
        self.Installationskosten20= self.Installationskosten+(148+5* p1.Anlage) *20   
    else:   
        self.Installationskosten20= self.Installationskosten+(148+21+5* p1.Anlage) *20    
    
    self.anual= ((self.Ersparniss*20 /self.Installationskosten20) ** (1/20) -1)*100

class Autcalc:
 def __init__(self,k):           

    self.Aut = np.sum(p4.Eigenverbrauch)/np.sum(p1.Last)*100 
     

class GSCcalc:
 def __init__(self,k):  

     self.GSC_top= np.sum(p4.Netzeinspeisung*Preis)             
     self.GSCein=np.around(np.sum(self.GSC_top)/(np.sum(p4.Netzeinspeisung)*p1.preisavg),decimals=3)    

     self.GSC_bot=np.sum(p4.Eigenverbrauch*Preis) 
     self.GSCev=np.around(np.sum(self.GSC_bot)/(np.sum(p4.Eigenverbrauch)*p1.preisavg),decimals=3)    

     self.GSC = (self.GSCein+self.GSCev)/2
     
for k in range (Haushalte):
  p1 = cl1(k)    
  p2 = cl2(k)  
  matco=pd.DataFrame()
  matwind = pd.DataFrame()
  matrendite = pd.DataFrame()
  mataut = pd.DataFrame()
  matgsc = pd.DataFrame()
  matzukunft = pd.DataFrame()
  for m in Batrange:
     Kapazitaet = m * 1   
       

     p3 = cl3(k)
     p4 = cl4(k) 
     pco = co2calc(k)   
     pwind= Konfliktcalc(k)
     panual= Renditecalc(k)
     paut= Autcalc(k)
     pgsc= GSCcalc(k)
     print('anlage:',np.around(p1.Anlage,decimals=2) , 'kWp')
     print('Kapazitaet:',Kapazitaet, 'kWh')
     print('co2:   ',np.around(np.sum(pco.co2),decimals=2),  't/a')
     print('wind:  ',pwind.Konflikt_sum , 'konfliktfreie Zeitpunkte')
     print('Rendite:',np.around(panual.anual,decimals=3), '%/a')
     print('Aut:',np.around(paut.Aut,decimals=2) , '%')
     print('GSC:',np.around(pgsc.GSC,decimals=2))
     print('  ')
    
   


     matco = matco.append({'co2':pco.co2}, ignore_index=True)
     matwind = matwind.append({'wind':pwind.Konflikt_sum}, ignore_index=True)
     matrendite = matrendite.append({'rendite':panual.anual}, ignore_index=True)
     mataut = mataut.append({'autarkie':paut.Aut}, ignore_index=True)
     matgsc=matgsc.append({'gsc':pgsc.GSC}, ignore_index=True)
     matzukunft = matzukunft.append({'zukunft':1}, ignore_index=True)
     
     #Optimization starts here (optimale Lösung wird ermittelt)
     if m+1 == len(Batrange):
          opt=pd.concat([matco, matwind,matrendite,mataut,matgsc,matzukunft], axis=1) 
          col_sums = np.cumsum(opt**2,axis=0)
          wurzel= np.sqrt(col_sums)
          max1=wurzel.max()
          weight = np.array([0.1,0.3,0.3,0.1,0.1,0.1])
          Decision=opt/max1*weight
          max2=Decision.max()
          min1=Decision.min()
          Ideal=np.sqrt(np.cumsum((Decision-max2)**2,axis=1))
          max3=Ideal['zukunft']
          nonIdeal=np.sqrt(np.cumsum((Decision-min1)**2,axis=1))
          min2=nonIdeal['zukunft']
          relDist=min2/(max3+min2) 
          final=relDist.idxmax()
          print('Optimale Batteriekapazitaet:',final, 'kWh')
          








  

 