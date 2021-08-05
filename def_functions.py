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

df=pd.read_csv('QuartierHH.csv',nrows=timesteps)
df2=pd.read_csv('Last_einzeln.csv',nrows=timesteps)
df3=pd.read_csv('Dachflaechen.csv',nrows=Haushalte)
####################
n_pv=0.2                
nsys_pv = 0.85            
Startkapazitaet=0
nsys_bat = 0.921

Isued= df['sued']          
Iost= df['ost']
Iwest= df['west']
####################
Dach=df3['Dach']             #Dach Süd       
Dachow=df3['Dachow']         #Dach Ost West
co2reihe=df['co2']
Wind= df['Wind']             #Abregelung Windeinspeisung 
Preis=df['Strompreis']
##################


PVgen = np.zeros(shape=(timesteps))
Last  = np.zeros(shape=(timesteps))
batkap  = np.zeros(shape=(timesteps))
def PVgenerated(k):
  print('Haushalt:',k) 
  
  einfach= [Isued[i] *  Dach[k] *n_pv*nsys_pv for i in range(timesteps)]
  einfachost = [Iost[i] * Dachow[k]*0.5 *n_pv*nsys_pv for i in range(timesteps)]
  einfachwest = [Iwest[i] * Dachow[k]*0.5 *n_pv*nsys_pv for i in range(timesteps)]
  PVgen = [(einfach[i]+einfachost[i]+einfachwest[i]) for i in range(timesteps)] 
  
  print('PVgen   :',np.sum(PVgen))
  return PVgen
def Lastfct(k):
 
  
  tess= df2[df2.columns[k]]
  Last=tess
  
  
  print("Last  :",np.sum(Last))
  
  

  return Last


class cl1():
  def __init__(self,k):  
   self.PVgen= PVgenerated(k)
   self.Last= Lastfct(k)  
   self.siebzig= Dach[k]+ Dachow[k]*n_pv *0.7 

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


for k in range (0,3):
 p1 = cl1(k)    
 p2 = cl2(k)
 p3 = cl3(k)
 p4 = cl4(k) 
 print(np.sum(p2.bataus),'    ',np.sum(p2.batein))
 print(np.sum(p4.Netzbezug),'    ',np.sum(p4.Netzeinspeisung)) 
 print('  ')

