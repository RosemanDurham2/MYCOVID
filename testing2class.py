#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 10:37:45 2021

@author: meg
"""
import sys
import math
import matplotlib.pyplot as plt
import numpy as np
from metromin import metromin
from Contact17x17 import Contactclass17
from Contact17x17Q import Contactclass17Q
import datetime
from scipy.stats import gamma
import scipy as scipy
import pandas as pd
import matplotlib.dates as dates

class MY_COVID2(metromin,Contactclass17) :
    def __init__(self,Tmax,R,nP,Vdelay,Vorder,Vgap,Vprop1,Vprop2):
        self.TotPop = np.dot(55.98e6/66.27,[3.86,4.15,3.95,3.66,4.15,4.51,4,4.4,4.02,4.4,4.66,4.41,3.76,3.37,3.32,5.7-0.376200,0.418000])
        self.Tmax = Tmax
        self.asize=Tmax+1
        self.Rpar = R
        self.Ac=0.4
        self.avred=0.3007
        self.Cf= np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0.5975])
        self.Hf = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        self.Hc = np.array([0.0,0.0026,0.00084,0.00042,0.0008,0.0026,0.0040,0.0063,0.012,0.019,0.023,0.040,0.096,0.10,0.24,0.50,0.2])
        self.Kf = np.array([0.00031,0.00003,0.00001,0.000001,0.00001,0.00004,0.00006,0.00013,0.00031,0.0007,0.00116,0.00276,0.00867,0.01215,0.03512,0.09063,0.60*0.2])
        self.Hf=self.Kf/self.Hc
        self.Hf[0]=0
        self.nP=nP
        self.nPad = nP+1
        self.Vorder=Vorder
        self.Vrateweek=0
        self.storeVrate=np.zeros((17,self.asize))
        self.storefVrate=np.zeros((17,self.asize))
        self.storefVrate2=np.zeros((17,self.asize))
        self.storeVrate2=np.zeros((17,self.asize))
        self.Vrate=np.zeros((17,))
        self.Vrateweek2=0
        self.Vrate2=np.zeros((17,))
        self.Vprop1=Vprop1
        self.Vprop2=Vprop2
        self.sigmai1=0.28
        self.sigmah1=0.15
        self.sigmaa1=0.43
        self.sigmai2=0.10
        self.sigmah2=0.06
        self.sigmaa2=0.30
        self.lnP=249
        self.lnPad=250
        self.uptake=np.array(np.full(shape=(17,),fill_value=0.9))
        self.dose=Vgap
        self.amount=Vdelay
      
            
            #0,0,0.85,0.85,0.85,0.85,0.85,0.85,0.85,0.85,0.85,0.85,0.85,0.85,0.85,0.85,0.902,0.85]

        
       # self.contact=[[0.16911964,0.09572051,0.055995, 0.00372662,0.00372662],[0.09623008, 0.15657723, 0.07461365, 0.00969354,0.00969354],[0.07703133, 0.10096069, 0.11584768, 0.01817469,0.01817469],[0.02226108, 0.04303201, 0.06305222, 0.06045816,0.06045816],[0.02226108, 0.04303201, 0.06305222, 0.06045816,0.06045816]]
        self.contact=Contactclass17.contactmatrix()
        self.contactQ=Contactclass17Q.contactmatrix()
        
        casesinf=pd.read_excel('hospdata.xlsx',sheet_name='cases',names=["case1"])

        self.S=np.zeros((17,self.asize))
        self.I=np.zeros((17,self.asize))
        self.R=np.zeros((17,self.asize))
        self.F=np.zeros((17,self.asize))
        self.A=np.zeros((17,self.asize))
        self.H=np.zeros((17,self.asize))
        
        
        self.SV1=np.zeros((17,self.asize))
        self.IV1=np.zeros((17,self.asize))
        self.RV1=np.zeros((17,self.asize))
        self.FV1=np.zeros((17,self.asize))
        self.AV1=np.zeros((17,self.asize))
        self.HV1=np.zeros((17,self.asize))
        
         
        self.SV2=np.zeros((17,self.asize))
        self.IV2=np.zeros((17,self.asize))
        self.RV2=np.zeros((17,self.asize))
        self.FV2=np.zeros((17,self.asize))
        self.AV2=np.zeros((17,self.asize))
        self.HV2=np.zeros((17,self.asize))
        
        
        self.V1=np.zeros((17,self.asize+21))
        self.Vcount=np.zeros((17,self.asize+21))
        self.Vcount2=np.zeros((17,self.asize+21))
        self.V2=np.zeros((16,self.asize+21))
        self.Vac=np.zeros((16,self.asize))
        self.Vac2=np.zeros((16,self.asize))
      #number of people in hospital
        self.Dh=np.zeros((17,self.asize+self.nPad)) #no. transferrred from infected to hospitalised
        self.DRh=np.zeros((17,self.asize)) #no. of those in hosipital who are moved to recovered
        self.Di=np.zeros((17,self.asize+self.nPad))
        self.Da=np.zeros((17,self.asize+self.nPad))
        self.Dr=np.zeros((17,self.asize))
        self.Df=np.zeros((17,self.asize))
        self.DRa=np.zeros((17,self.asize))
        
        self.DhV1=np.zeros((17,self.asize+self.nPad)) #no. transferrred from infected to hospitalised
        self.DRhV1=np.zeros((17,self.asize)) #no. of those in hosipital who are moved to recovered
        self.DiV1=np.zeros((17,self.asize+self.nPad))
        self.DaV1=np.zeros((17,self.asize+self.nPad))
        self.DrV1=np.zeros((17,self.asize))
        self.DfV1=np.zeros((17,self.asize))
        self.DRaV1=np.zeros((17,self.asize))
        
        self.DhV2=np.zeros((17,self.asize+self.nPad)) #no. transferrred from infected to hospitalised
        self.DRhV2=np.zeros((17,self.asize)) #no. of those in hosipital who are moved to recovered
        self.DiV2=np.zeros((17,self.asize+self.nPad))
        self.DaV2=np.zeros((17,self.asize+self.nPad))
        self.DrV2=np.zeros((17,self.asize))
        self.DfV2=np.zeros((17,self.asize))
        self.DRaV2=np.zeros((17,self.asize))
        
        self.CHF=np.zeros((17,self.asize+self.nPad))
        self.t=np.linspace(0,self.Tmax,num=self.Tmax+1)
        
        
        
        
        self.lPinf=self.mk_gammalong(self.t,6.5,0.62)
        self.lPinc=self.mk_gammalong(self.t,5.1,0.86) 
        self.lPrinc=self.mk_gammalong(self.t,17.8,0.45) 
        
        self.mildsymprecover=self.mk_gammalong(self.t,11.94,0.48)
        self.symphosp=self.log_normallong(self.t,0.845,5.506)
        self.exphosp=self.evalexphosp()
        plt.plot(self.mildsymprecover)
        plt.show()
        self.mildfull=self.evalmildfull()
        self.fullhosp=self.evalfullhosp()
        
        self.truPinf=self.truePinf()
        self.mildcase=self.normalpinf()
        self.HPinf=self.evalHPinf()
        self.HPinfIso=self.evalHPinfIso(1,0.95)
        self.averHPinf=self.evalHPinfIso(1,0.6667)
        
        
        self.PinfIso=self.evalisoPinf(1,0.95)
        self.averPinf=self.evalisoPinf(1,0.666667)
        self.AsPinf=self.asympPinf(0,0)
        
        self.presymp1=self.evalisoPinf(0,1)
        self.asymprec=self.evalasympfull()
        #self.mildfull=np.delete(self.mildfull,-1)
      #  self.mildfull=5*np.mean(self.mildfull.reshape(-1,5),axis=1)
      #  self.mildfull=np.insert(self.mildfull,-1,0)
        self.lPinf=self.shorten(self.lPinf)
        self.averPinf=self.shorten(self.averPinf)
        self.truPinf=self.shorten(self.truPinf)
        self.lPinc=self.shorten(self.lPinc)
        self.lPrinc=self.shorten(self.lPrinc)
        self.mildfull=self.shorten(self.mildfull)
        self.fullhosp=self.shorten(self.fullhosp)
        self.HPinf=self.shorten(self.HPinf)
        self.HPinfIso=self.shorten(self.HPinfIso)
        self.averHPinf=self.shorten(self.averHPinf)
        self.presymp1=self.shorten(self.presymp1)
        self.PinfIso=self.shorten(self.PinfIso)
        self.AsPinf=self.shorten(self.AsPinf)
        self.mildcase=self.shorten(self.mildcase)
        self.asymprec=self.shorten(self.asymprec)
        twat=np.zeros((16,))
        twat2=0
        
        for i in range(0,self.nPad):
            for j in range(0,16):
                self.Da[j][self.nPad-i]=0.4*sum(self.contactQ[j])/sum(sum(self.contactQ))*(1/0.6)*(self.TotPop[j]/sum(self.TotPop))*(1/0.057721729012579985)*25000
                self.Di[j][self.nPad-i]=(1-self.Hc[j]-0.4)*sum(self.contactQ[j])/sum(sum(self.contactQ))*(1/0.6)*(self.TotPop[j]/sum(self.TotPop))*(1/0.057721729012579985)*25000
                self.Dh[j][self.nPad-i]=self.Hc[j]*sum(self.contactQ[j])/sum(sum(self.contactQ))*(1/0.6)*(self.TotPop[j]/sum(self.TotPop))*(1/0.057721729012579985)*25000
                twat[j]=sum(self.contactQ[j])/sum(sum(self.contactQ))*(self.TotPop[j]/sum(self.TotPop))
        for i in range(0,self.nPad):
            self.Da[16][self.nPad-i]=0.4*sum(self.contactQ[16])/sum(sum(self.contactQ))*(1/0.6)*(self.TotPop[16]/sum(self.TotPop))*(1/(0.057721729012579985+0.00046759425727457225))*25000
            self.Di[16][self.nPad-i]=(1-self.Hc[16]-0.4)*sum(self.contactQ[16])/sum(sum(self.contactQ))*(1/0.6)*(self.TotPop[16]/sum(self.TotPop))*(1/(0.057721729012579985+0.00046759425727457225))*25000
            self.Dh[16][self.nPad-i]=self.Hc[16]*sum(self.contactQ[16])/sum(sum(self.contactQ))*(1/0.6)*(self.TotPop[16]/sum(self.TotPop))*(1/(0.057721729012579985+0.00046759425727457225))*25000
            twat2=+sum(self.contactQ[16])/sum(sum(self.contactQ))*(self.TotPop[16]/sum(self.TotPop))
      #  print("WHATIDO",sum(twat),twat2,twat2/(sum(twat)+twat2))
        
        
        cum=1-np.cumsum(self.mildfull)
        cum2=1-np.cumsum(self.fullhosp)
        cum3=1-np.cumsum(self.asymprec)
 
        for i in range(0,17):
            self.A[i][0]=np.sum(self.Da[i][0:self.nPad]*cum3[::-1])
            self.I[i][0]=np.sum(self.Di[i][0:self.nPad]*cum[::-1])
            self.H[i][0]=np.sum(self.Dh[i][0:self.nPad]*cum2[::-1])
        #print(self.A[5][0],"BOOOM BOOM READ THIS FUCKER")
        for i in range(0,17):
            self.R[i][0]=self.TotPop[i]*0.15
            self.S[i][0]=self.TotPop[i]*(1-self.Vprop1[i]-self.Vprop2[i])-self.I[i][0]-self.H[i][0]-self.A[i][0]-self.R[i][0]
            self.SV1[i][0]=self.TotPop[i]*self.Vprop1[i]+1e-9
            self.SV2[i][0]=self.TotPop[i]*self.Vprop2[i]+1e-9

            
    def mk_gamma(self,t, mu, var_coef):
        """ Create and return a varience distribution
            : param t : range of values
            : param mu : average
            : param var_coef : coefficient of variation (=sigma/mu)
        """
        lambda_p = np.sqrt(1/(mu*var_coef**2)) # lambda=alpha/mu=1/(mu V^2)
        alpha_p = mu*lambda_p 
        Pi = gamma.pdf(t[:self.nPad], alpha_p, 0, 1/lambda_p)
        x=np.linspace(0,50,51)
        Pi=Pi/sum(Pi)

        Pi2=np.roll(Pi,1)
        Pi3=(Pi+Pi2)/2
        return(Pi3)
    def mk_gammalong(self,t, mu, var_coef):
        """ Create and return a varience distribution
            : param t : range of values
            : param mu : average
            : param var_coef : coefficient of variation (=sigma/mu)
        """
        lambda_p = np.sqrt(1/(mu*var_coef**2)) # lambda=alpha/mu=1/(mu V^2)
        alpha_p = mu*lambda_p
        x=np.linspace(0,50,self.lnPad)
        Pi = gamma.pdf(x, alpha_p, 0, 1/lambda_p)
        Pi=Pi/sum(Pi)
        return(Pi)
    
    
    
    def log_normallong(self,t, mu, var_coef):
        """ Create and return a varience distribution
            : param t : range of values
            : param mu : average
            : param var_coef : coefficient of variation (=sigma/mu)
        """
        x=np.linspace(0,50,self.lnPad+2)
        Pi = (scipy.stats.weibull_min.pdf(x,mu,0,var_coef))
        Pi=Pi[1:self.lnPad+1]
       # plt.show()
      #  print(sum(Pi))
        Pi = Pi/sum(Pi) # normalise
        return(Pi)
       
        
    def evalPrd(self):
        Pr=np.zeros(self.lnPad)
        for d in range(len(Pr)):
            for n in range(0,self.lnP):
                Pr[d] += self.lPinc[n]*self.lPrinc[d-n]
        Pr = Pr/sum(Pr)     # normalise the probability    
        return Pr
    
    def evalPhd(self):
        Phrd=np.zeros(self.lnPad)
        for d in range(len(Phrd)):
            for n in range(0,self.lnP):
                Phrd[d] += self.lPinc[n]*self.Phrinc[d-n]
        Phrd = Phrd/sum(Phrd)     # normalise the probability    
        return Phrd  
        
    def evalmildfull(self):
        Pr=np.zeros(self.lnPad)
        for d in range(len(Pr)):
            for n in range(0,self.lnP):
                Pr[d] += self.lPinc[n]*self.mildsymprecover[d-n]
        Pr = Pr/sum(Pr) # normalise the probability    
        return Pr
    
    def evalasympfull(self):
        Pr=np.zeros(self.lnPad)
        for d in range(len(Pr)):
            for n in range(0,self.lnP):
                Pr[d] += self.lPinc[n]*self.truPinf[d-n]
        Pr = Pr/sum(Pr) # normalise the probability    
        return Pr
    
    
    def evalHPinf(self): #No isolation Hpinf
        cumn=1-np.cumsum(np.roll(self.exphosp,0))
        Phrd=np.zeros(self.lnPad)
        for d in range(len(Phrd)):
            for n in range(0,self.lnP):
                Phrd[d] += self.truPinf[d]*cumn[d]
        Phrd = Phrd/self.lnP
       # print(sum(Phrd),"L Hpinf reduction")
        return Phrd
    
    def evalHPinfIso(self,d,p): #variable isolation Hpinf
        cumn=1-np.cumsum(np.roll(self.lPinc,d*5)*p)
        Phrd=np.zeros(self.lnPad)
        for d in range(len(Phrd)):
            for n in range(0,self.lnP):
                Phrd[d] += self.HPinf[d]*cumn[d]
        Phrd = Phrd/self.lnP
      #  print(sum(Phrd),"L Hpinfiso reduction")
        return Phrd
    
    def normalpinf(self): #normalised mild case = 1
        cumn=1-np.cumsum(np.roll(self.mildfull,0))
        Phrd=np.zeros(self.lnPad)
        for d in range(len(Phrd)):
            for n in range(0,self.lnP):
                Phrd[d] += self.truPinf[d]*cumn[d]
        Phrd = Phrd/self.lnP
       # print(sum(Phrd),"noramlpinf reduction")
        return Phrd

    def truePinf(self): #maximum potential infectvity
        cumn=1-np.cumsum(np.roll(self.lPinc,5)*(6/7))
        Phrd=np.zeros(self.lnPad)
        for d in range(len(Phrd)):
            for n in range(0,self.lnP):
                Phrd[d] += self.lPinf[d]/cumn[d]
        Phrd = Phrd/(sum(Phrd))
    #    for d in range(len(Phrd)):
    #        for n in range(0,self.lnP):
       #         Phrd[d] += Phrd[d]*cumn2[d]
       # Phrd = Phrd/(sum(Phrd))
        return Phrd

    def asympPinf(self,d,p): #Asymptomatic infectvity with possible pre-incubation testing
        cumn=1-np.cumsum(np.roll(self.lPinc,d*5)*p)
        Phrd=np.zeros(self.lnPad)
        for d in range(len(Phrd)):
            for n in range(0,self.lnP):
                Phrd[d] += self.truPinf[d]*0.3007
        Phrd = Phrd/self.lnP
       # print(sum(Phrd),"L asymp reduction")
        return Phrd
    
    def evalisoPinf(self,d,p): #mild case isolation infectivity
        cumn=1-np.cumsum(np.roll(self.lPinc,5*d)*p)
        Phrd=np.zeros(self.lnPad)
        for d in range(len(Phrd)):
            for n in range(0,self.lnP):
                Phrd[d] += self.truPinf[d]*cumn[d]
        Phrd = Phrd/self.lnP
       # print(sum(Phrd),"L pinfiso reduction")
        return Phrd
    
    def evalexphosp(self): #Duration from infection to hospitalisation
        Phrd=np.zeros(self.lnPad)
        for d in range(len(Phrd)):
            for n in range(0,self.lnP):
                Phrd[d] += self.lPinc[n]*self.symphosp[d-n]
        Phrd = Phrd/sum(Phrd)   
        return Phrd
    
    def evalfullhosp(self): #Full hospital duration
        Phrd=np.zeros(self.lnPad)
        for d in range(len(Phrd)):
            for n in range(0,self.lnP):
                Phrd[d] += self.lPinc[n]*self.lPrinc[d-n]
        Phrd = Phrd/sum(Phrd)
        #print(sum(Phrd))   
        return Phrd
        
    def shorten(self,func):
        func=5*np.mean(func.reshape(-1,5),axis=1)
        func=np.insert(func,-1,0)
        return func
   
    def my_covid2(self):
        SumDi=np.zeros(shape=(17,))
        SumRi=np.zeros(shape=(17,))
        SumRh=np.zeros(shape=(17,))
        SumRa=np.zeros(shape=(17,))
        SumRiV1=np.zeros(shape=(17,))
        SumRhV1=np.zeros(shape=(17,))
        SumRaV1=np.zeros(shape=(17,))
        SumRiV2=np.zeros(shape=(17,))
        SumRhV2=np.zeros(shape=(17,))
        SumRaV2=np.zeros(shape=(17,))
        SumDiA=np.zeros(shape=(17,))
        SumDiH=np.zeros(shape=(17,))
        SumDiHV1=np.zeros(shape=(17,))
        SumDiHV2=np.zeros(shape=(17,))
        SumVi=np.zeros(shape=(17,))
        SumRaV=np.zeros(shape=(17,))
        SumDiH=np.zeros(shape=(17,))
        SumDiAV1=np.zeros(shape=(17,))
        SumDiAV2=np.zeros(shape=(17,))
        SumDiA=np.zeros(shape=(17,))
        SumDiV1=np.zeros(shape=(17,))
        SumDiV2=np.zeros(shape=(17,))
        count=0
        count2=0
     #   print("population",self.S[0:-1][0],self.SV1[0:-1][0])
        zeros=np.zeros(shape=(3,))
        zeros2=np.zeros(shape=(3,))
       # self.Vrateweeka=np.concatenate((zeros,self.Vrateweek))
       # self.Vrateweek2a=np.concatenate((zeros,self.Vrateweek2))
        self.Vrate=np.zeros(shape=(17,))
        self.Vrate2=np.zeros(shape=(17,))        
        for d in range(self.Tmax): 
             #   print(d,"fur",self.storefVrate[self.Vorder[count2]][d-21],self.storeVrate[self.Vorder[count2]][d-21])
             #   print("i wanna die",self.Vrate2[Vorder[count2]])
             
            if d>=21 and d<self.dose:
                self.Vrate=np.zeros(shape=(17,))
                self.Vrate[self.Vorder[count]]=(self.amount*2)/7
                self.storeVrate[:,d]=self.Vrate
                self.Vrate=self.Vrate#*((self.S[:,d-21]+self.SV1[:,d-21]+self.SV2[:,d-21])/(self.R[:,d-21]+self.S[:,d-21]+self.SV1[:,d-21]+self.SV2[:,d-21]))
                
                self.storefVrate[:,d]=self.Vrate
              #  print(d,"vaccine",self.Vrate[Vorder[count]],Vorder[count],self.S[Vorder[count]][d],self.SV1[Vorder[count]][d])
            if d>=self.dose:
                self.Vrate=np.zeros(shape=(17,))
                self.Vrate[self.Vorder[count]]=self.amount/7
                self.storeVrate[:,d]=self.Vrate
                self.Vrate=self.Vrate#*((self.S[:,d-21]+self.SV1[:,d-21]+self.SV2[:,d-21])/(self.R[:,d-21]+self.S[:,d-21]+self.SV1[:,d-21]+self.SV2[:,d-21]))
               # print(self.S[:,d-21],"dwajf")
                #((self.S[:,d-21]+self.SV1[:,d-21]+self.SV2[:,d-21])/(self.R[:,d-21]+self.S[:,d-21]+self.SV1[:,d-21]+self.SV2[:,d-21]))
                self.storefVrate[:,d]=self.Vrate
                #print(d,"shouldmtbe mucg",self.storefVrate2[:,(d-1)],np.transpose(np.cumsum(self.storefVrate2,axis=0))[d][i])
               # print("plsbezeros",self.storeVrate2[:,d])
                #print(d,"for all that is holty",
                self.Vrate2=np.zeros(shape=(17,))
                self.Vrate2[self.Vorder[count2]]=self.amount/7
             #   print("plsease",sum(np.transpose(np.cumsum(self.storefVrate,axis=0))[0:d-21]))
             #   print("killme",np.sum(self.storefVrate,axis=0)[0:d-21])
                self.Vrate2=self.Vrate2#*((sum(np.sum(self.storefVrate,axis=0)[0:d-21])/sum(np.sum(self.storeVrate,axis=0)[0:d-21])))
               # print(d,"vaccine",self.Vrate[Vorder[count]],Vorder[count],self.S[Vorder[count]][d],self.SV1[Vorder[count]][d])
                #self.storeVrate2[:,d]+np.concatenate((np.zeros(shape=(16,)),np.full(shape=(1,),fill_value=1000000/7)))#(sum(np.transpose(np.cumsum(self.storefVrate,axis=0))[0:d-21])/sum(np.transpose(np.cumsum(self.storeVrate,axis=0))[0:d-21]))
                self.storefVrate2[:,d]=self.Vrate2
               # print(d,"vaccine2",self.Vrate2[Vorder[count2]],Vorder[count2],self.SV1[Vorder[count2]][d],self.SV2[Vorder[count2]][d])
               # print("vac 2",d,self.Vrate2,self.storefVrate2[:,d])

            totalinfect=np.zeros(shape=(17,))
            suminfect=np.zeros(shape=(17,))
            suminfectV1=np.zeros(shape=(17,))
            suminfectV2=np.zeros(shape=(17,))
            for i in range(16,-1,-1):   
                for j in range(0,17):
                    if d>0 and d<=0:
                        suminfect[i]+=(self.contact[i][j])*(sum(self.PinfIso*self.Di[j][self.nPad+d:self.nPad+d-self.nP-1:-1]/(self.TotPop[j]-self.F[j][d]))+sum(self.HPinfIso*self.Dh[j][self.nPad+d:self.nPad+d-self.nP-1:-1]/(self.TotPop[j]-self.F[j][d]))+sum(self.AsPinf*self.Da[j][self.nPad+d:self.nPad+d-self.nP-1:-1]/(self.TotPop[j]-self.F[j][d])))
                        suminfectV1[i]+=(self.contact[i][j])*(sum(self.PinfIso*self.DiV1[j][self.nPad+d:self.nPad+d-self.nP-1:-1]/(self.TotPop[j]-self.F[j][d]))+sum(self.HPinfIso*self.DhV1[j][self.nPad+d:self.nPad+d-self.nP-1:-1]/(self.TotPop[j]-self.F[j][d]))+sum(self.AsPinf*self.DaV1[j][self.nPad+d:self.nPad+d-self.nP-1:-1]/(self.TotPop[j]-self.F[j][d])))
                        suminfectV2[i]+=(self.contact[i][j])*(sum(self.PinfIso*self.DiV2[j][self.nPad+d:self.nPad+d-self.nP-1:-1]/(self.TotPop[j]-self.F[j][d]))+sum(self.HPinfIso*self.DhV2[j][self.nPad+d:self.nPad+d-self.nP-1:-1]/(self.TotPop[j]-self.F[j][d]))+sum(self.AsPinf*self.DaV2[j][self.nPad+d:self.nPad+d-self.nP-1:-1]/(self.TotPop[j]-self.F[j][d])))
                    else:
                        suminfect[i]+=(self.contactQ[i][j])*(sum(self.PinfIso*self.Di[j][self.nPad+d:self.nPad+d-self.nP-1:-1]/(self.TotPop[j]-self.F[j][d]))+sum(self.HPinfIso*self.Dh[j][self.nPad+d:self.nPad+d-self.nP-1:-1]/(self.TotPop[j]-self.F[j][d]))+sum(self.AsPinf*self.Da[j][self.nPad+d:self.nPad+d-self.nP-1:-1]/(self.TotPop[j]-self.F[j][d])))
                        suminfectV1[i]+=(self.contactQ[i][j])*(sum(self.PinfIso*self.DiV1[j][self.nPad+d:self.nPad+d-self.nP-1:-1]/(self.TotPop[j]-self.F[j][d]))+sum(self.HPinfIso*self.DhV1[j][self.nPad+d:self.nPad+d-self.nP-1:-1]/(self.TotPop[j]-self.F[j][d]))+sum(self.AsPinf*self.DaV1[j][self.nPad+d:self.nPad+d-self.nP-1:-1]/(self.TotPop[j]-self.F[j][d])))
                        suminfectV2[i]+=(self.contactQ[i][j])*(sum(self.PinfIso*self.DiV2[j][self.nPad+d:self.nPad+d-self.nP-1:-1]/(self.TotPop[j]-self.F[j][d]))+sum(self.HPinfIso*self.DhV2[j][self.nPad+d:self.nPad+d-self.nP-1:-1]/(self.TotPop[j]-self.F[j][d]))+sum(self.AsPinf*self.DaV2[j][self.nPad+d:self.nPad+d-self.nP-1:-1]/(self.TotPop[j]-self.F[j][d])))
                        
                totalinfect[i]=suminfect[i]+suminfectV1[i]+suminfectV2[i]
                if self.S[i][d]<=0:
                    self.S[i][d]=0
                if self.SV1[i][d]<=0:
                    self.SV1[i][d]=0   
                
                SumDi[i]= (1-self.Hc[i]-self.Ac)*totalinfect[i]
                SumDiA[i]= self.Ac*totalinfect[i]
                SumDiH[i]= self.Hc[i]*totalinfect[i]
         
                SumDiV1[i]= self.sigmai1*(1-self.Hc[i]-self.Ac)*totalinfect[i]
                SumDiAV1[i]=self.sigmaa1*self.Ac*totalinfect[i]
                SumDiHV1[i]=self.sigmah1*self.Hc[i]*totalinfect[i]
                
                SumDiV2[i]= self.sigmai2*(1-self.Hc[i]-self.Ac)*totalinfect[i]
                SumDiAV2[i]=self.sigmaa2*self.Ac*totalinfect[i]
                SumDiHV2[i]=self.sigmah2*self.Hc[i]*totalinfect[i]
                
                SumRi[i] =sum(self.mildfull*self.Di[i][self.nPad+d:self.nPad+d-self.nP-1:-1])
                SumRh[i]=sum(self.fullhosp*self.Dh[i][self.nPad+d:self.nPad+d-self.nP-1:-1])
                SumRa[i]=sum(self.asymprec*self.Da[i][self.nPad+d:self.nPad+d-self.nP-1:-1])
                
                SumRiV1[i] =sum(self.mildfull*self.DiV1[i][self.nPad+d:self.nPad+d-self.nP-1:-1])
                SumRhV1[i]=sum(self.fullhosp*self.DhV1[i][self.nPad+d:self.nPad+d-self.nP-1:-1])
                SumRaV1[i]=sum(self.asymprec*self.DaV1[i][self.nPad+d:self.nPad+d-self.nP-1:-1])
                
                SumRiV2[i] =sum(self.mildfull*self.DiV2[i][self.nPad+d:self.nPad+d-self.nP-1:-1])
                SumRhV2[i]=sum(self.fullhosp*self.DhV2[i][self.nPad+d:self.nPad+d-self.nP-1:-1])
                SumRaV2[i]=sum(self.asymprec*self.DaV2[i][self.nPad+d:self.nPad+d-self.nP-1:-1])
               
                self.Di[i][self.nPad+d]=self.Rpar[d]*self.S[i][d]*(SumDi[i])
                self.Dh[i][self.nPad+d]=self.Rpar[d]*self.S[i][d]*(SumDiH[i])
                self.Da[i][self.nPad+d]=self.Rpar[d]*self.S[i][d]*(SumDiA[i])
                
                self.DiV1[i][self.nPad+d]=self.Rpar[d]*self.SV1[i][d]*(SumDiV1[i])
                self.DhV1[i][self.nPad+d]=self.Rpar[d]*self.SV1[i][d]*(SumDiHV1[i])
                self.DaV1[i][self.nPad+d]=self.Rpar[d]*self.SV1[i][d]*(SumDiAV1[i])
                
                self.DiV2[i][self.nPad+d]=self.Rpar[d]*self.SV2[i][d]*(SumDiV2[i])
                self.DhV2[i][self.nPad+d]=self.Rpar[d]*self.SV2[i][d]*(SumDiHV2[i])
                self.DaV2[i][self.nPad+d]=self.Rpar[d]*self.SV2[i][d]*(SumDiAV2[i])

                self.CHF[i][self.nPad+d]=(self.Cf[i])*SumRi[i]
                
                self.Df[i][d]=self.Hf[i]*SumRh[i]+self.Cf[i]*SumRi[i]
                #+sum(self.CareHF*self.CHF[i][self.nPad+d:self.nPad+d-self.nP-1:-1])
                self.Dr[i][d]=SumRi[i]*(1-self.Cf[i])
                self.DRh[i][d]=(1-self.Hf[i])*SumRh[i]
                self.DRa[i][d]=SumRa[i]
                
                self.DfV1[i][d]=self.Hf[i]*SumRhV1[i]+self.Cf[i]*SumRiV1[i]*self.sigmai1
                #+sum(self.CareHF*self.CHF[i][self.nPad+d:self.nPad+d-self.nP-1:-1])
                self.DrV1[i][d]=SumRiV1[i]*(1-self.Cf[i])*(1-self.sigmai1)
                self.DRhV1[i][d]=(1-self.Hf[i])*SumRhV1[i]
                self.DRaV1[i][d]=SumRaV1[i]
                 
                self.DfV2[i][d]=self.Hf[i]*SumRhV2[i]+self.Cf[i]*SumRiV2[i]*self.sigmai2
                #+sum(self.CareHF*self.CHF[i][self.nPad+d:self.nPad+d-self.nP-1:-1])
                self.DrV2[i][d]=SumRiV2[i]*(1-self.Cf[i])*(1-self.sigmai2)
                self.DRhV2[i][d]=(1-self.Hf[i])*SumRhV2[i]
                self.DRaV2[i][d]=SumRaV2[i]
                
                
                self.S[i][d+1]=self.S[i][d]-self.Di[i][self.nPad+d]-self.Dh[i][self.nPad+d]-self.Vrate[i]
                if self.S[i][d+1]<0 and (i==self.Vorder[count]):
                #    print(d,i,"fuck you")
                    self.Vrate[i]=self.Vrate[i]+self.S[i][d+1]
                    self.S[i][d+1]=0
                    count+=1
                    self.Vrate[self.Vorder[count]]=-self.S[i][d+1]
                if self.S[i][d]<0 and i!=self.Vorder[count]:
                #    print(d,i,"fuck you and part2")
                    self.Vrate[self.Vorder[count]]=self.Vrate[i]
                    self.Vrate[i]=0
                    self.S[i][d]=0
                self.I[i][d+1]=self.Di[i][self.nPad+d]-self.Dr[i][d]+self.I[i][d]
                self.R[i][d+1]=self.R[i][d]+self.Dr[i][d]+self.DRh[i][d]
                self.F[i][d+1]=self.F[i][d]+self.Df[i][d]
                self.H[i][d+1]=self.H[i][d]-self.Df[i][d]+self.Dh[i][self.nPad+d]-self.DRh[i][d]+self.Cf[i]*SumRi[i]
                self.A[i][d+1]=self.A[i][d]+self.Da[i][self.nPad+d]-self.DRa[i][d]

                self.SV1[i][d+1]=self.SV1[i][d]-self.DiV1[i][self.nPad+d]-self.DhV1[i][self.nPad+d]+self.Vrate[i]-self.Vrate2[i]
                if self.SV1[i][d+1]<0 and (i==self.Vorder[count2]):
                #    print(d,i,"fuck you2")
                    self.Vrate2[i]=self.Vrate2[i]+self.SV1[i][d+1]
                    self.SV1[i][d+1]=0
                    count2+=1
                    self.Vrate2[self.Vorder[count2]]=-self.SV1[i][d+1]
                if self.SV1[i][d]<0 and i!=self.Vorder[count2]:
                #    print(d,i,"fuck you2 and part2")
                    self.Vrate2[self.Vorder[count2]]=self.Vrate2[i]
                    self.Vrate2[i]=0
                    self.SV1[i][d]=0
                    
                self.IV1[i][d+1]=self.DiV1[i][self.nPad+d]-self.DrV1[i][d]+self.IV1[i][d]
                self.RV1[i][d+1]=self.RV1[i][d]+self.DrV1[i][d]+self.DRhV1[i][d]
                self.FV1[i][d+1]=self.FV1[i][d]+self.DfV1[i][d]
                self.HV1[i][d+1]=self.HV1[i][d]-self.DfV1[i][d]+self.DhV1[i][self.nPad+d]-self.DRhV1[i][d]+self.Cf[i]*SumRiV1[i]
                self.AV1[i][d+1]=self.AV1[i][d]+self.DaV1[i][self.nPad+d]-self.DRaV1[i][d]
                
                self.SV2[i][d+1]=self.SV2[i][d]-self.DiV2[i][self.nPad+d]-self.DhV2[i][self.nPad+d]+self.Vrate2[i]
                self.IV2[i][d+1]=self.DiV2[i][self.nPad+d]-self.DrV2[i][d]+self.IV2[i][d]
                self.RV2[i][d+1]=self.RV2[i][d]+self.DrV2[i][d]+self.DRhV2[i][d]
                self.FV2[i][d+1]=self.FV2[i][d]+self.DfV2[i][d]
                self.HV2[i][d+1]=self.HV2[i][d]-self.DfV2[i][d]+self.DhV2[i][self.nPad+d]-self.DRhV2[i][d]+self.Cf[i]*SumRiV2[i]
                self.AV2[i][d+1]=self.AV2[i][d]+self.DaV2[i][self.nPad+d]-self.DRaV2[i][d]
        #        print(self.H[0][i]+self.F[0][i]+self.R[0][i]+self.S[0][i])
        #print(d,"sumcontact",sumcontact)
        



           
#        plt.semilogy(*self.larger_than(self.t,self.I),'r',label='I')
 #       plt.semilogy(*self.larger_than(self.t,self.R),'g', label='R')
 #       plt.semilogy(*self.larger_than(self.t,self.F),'k',label='F')
 #       plt.semilogy(*self.larger_than(self.t,self.Di[nP+1:]),'b',label='Di')
  #      plt.xlabel("t")
  #      plt.ylabel("P")
  #      plt.legend()
  #      plt.show()
  
    def Rweek(self,weekR):
        emptyR=[]
        for i in range(0,len(weekR)):
            n=0
            while n<7:
                emptyR.append(weekR[i])
                n=n+1
        return emptyR
   
""""
       
deaths=[90,125,128,110,123,134,155,168,135,126,163,186,217,196,213,201,196,220,223,238,268]
deaths=[818,844,878,858,896,958,955,944,1000,1075,999,895,917,907,840,807,769,660,591,506,436,398,362,303,237,186,164,130,109,74,68,52,47,32,22,16,13,8,3,5,3,0,0,3,0,2,1]

fatal=pd.read_excel('hospdata.xlsx',sheet_name='Deathage',names=['a','b','a1','b2','a3','b4','a5','b6','a7','b8','a9','b12','b61','a71','14','group15','care'])

deaths=fatal['a']+fatal['b']+fatal['a1']+fatal['b2']+fatal['a3']+fatal['b4']+fatal['a5']+fatal['b6']+fatal['a7']+fatal['b8']+fatal['a9']+fatal['b12']+fatal['b61']+fatal['a71']+fatal['14']+fatal['group15']


TotPop=np.dot(55.98/66.65,[3451560,3556732,3823503,3957013,3903430,3752013,4166962,4692543,4651991,3986480,3612537,3900381,3125098,2704065-20900,2337939-20900,4587765-376200,418000])
I0 = np.full(shape=(17,),fill_value=1)

Tmax = 100
asize=Tmax+1
d= 14
Kf = 0
nP=50
Vdelay=1000000
Vorder=[16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0]
Vprop1=np.full(shape=(17,),fill_value=0)
Vprop2=np.full(shape=(17,),fill_value=0)
#Vnum=np.array([0,0,0,0,340000/6,340000/6,340000/6,340000/6,340000/6,340000/6,90000,90000,65000,20000,20000,60000+800000*0.9,60000+800000*0.1])
#Vprop1=Vnum/TotPop    
#print(Vprop1)
Vrate0=np.zeros(shape=(17,146))
Vrate0[16][0]=200000
Vrate0[16][1]=200000
Vrate0[16][2]=200000
Vrate0[16][3]=200000
Vrate0[16][4]=200000
Vrate=Vrate0
Vrate12=np.zeros(shape=(17,))
Vrate12[16]=200000
Vrate=np.concatenate((np.full(shape=(200,),fill_value=0),np.full(shape=(5,),fill_value=1000000)))
Vrate2=np.concatenate((np.array(np.full(shape=(200,),fill_value=0)),np.array(np.full(shape=(20,),fill_value=1000000))))


weekR1=np.concatenate(((np.full(shape=(1,),fill_value=1/0.315469)),np.full(shape=(40,),fill_value=0.95/0.315469),np.full(shape=(42,),fill_value=1.2/0.315469),np.full(shape=(34,),fill_value=1.25/0.315469),np.full(shape=(60,),fill_value=1.4/0.315469)))
weekR=np.full(shape=(257,),fill_value=1.35/0.31549)
weekRearly=np.concatenate((np.full(shape=(33,),fill_value=(4.45/0.42917)),np.full(shape=(7,),fill_value=(3.65/0.3134511511)),np.full(shape=(16-7-7,),fill_value=3.65/0.3134511511),np.full(shape=(5,),fill_value=1.03/0.315469),np.full(shape=(130,),fill_value=0.81/0.315469)))
weekRlate=np.concatenate((np.full(shape=(33,),fill_value=(4.45/0.42917)),np.full(shape=(7,),fill_value=(4.45/0.42917)),np.full(shape=(16,),fill_value=3.65/0.3134511511),np.full(shape=(5,),fill_value=1.03/0.315469),np.full(shape=(130,),fill_value=0.81/0.315469)))
weekRhigh=weekR*1.1
weekRlow=weekR*0.9
dose=43

blupalette=["#1659C6",'#1C6FF8','#27BBE0','#31DB92','#1BF118','#9BFA24','#FEF720']

infectpal=['#F4BB00','#FEDE3A','#FEF247','FFFCA1']
deadpal=['#FF4D50','#EE1B10','#C6230F','#AD1F0A']
recoverpal=['#D6FA8C','#BEED53','#A5D721','#82B300']
suspal=['#00B9D3','#57C7DB','#90D6E2','#B8E3EA']

from matplotlib.colors import DivergingNorm
trueweekR=np.concatenate((np.full(shape=(33,),fill_value=(4.45)),np.full(shape=(16,),fill_value=3.65),np.full(shape=(5,),fill_value=1.03),np.full(shape=(120,),fill_value=0.81)))
#C19 = MY_COVID(TotPop,I0,Tmax,d,weekR,Kf,nP,Vdelay,Vorder,Vrate,Vrate2,dose,Vprop1,Vprop2)
#C19.Rweek(weekR)
#C19.my_covid()

fig, ax = plt.subplots()
fig.set_size_inches(18.5/2, 10.5/2)

im=ax.plot(C19.t,trueweekR[0:121],color='black',ls="dashed",label="$R_{1}$ value")
plt.axvline(33,color='r',label='02/03: First UK death')
plt.axvline(47,color='yellow',label="16/03: Lockdown Announced, partial measures")
plt.axvline(49,color='orange',label="18/03: Peak daily infections")
plt.axvline(54,color='green',label="23/03: Official Lockdown starts")
plt.axvline(70,color='blue',label="08/04: Peak daily deaths")
plt.xlim(0,120)
plt.xlabel("Day of the simulation")
plt.ylabel("$R_{1}$")
plt.title("$R_{1}$ of the model")
plt.legend(title='Key dates',bbox_to_anchor=(0,0,0.5,-0.15))

plt.show()

#print(C19.contact)

matrixx=C19.contact
#fig, ax = plt.subplots()
#im = ax.imshow(matrixx, cmap='cividis', interpolation='none')
#fig.colorbar(im)
#plt.show()

peakdath1 = pd.read_excel('peakdeath.xlsx',sheet_name='peakdeath',names=["death","cumdeath"])
fat=peakdath1['death']


agedeath= pd.read_excel('Book2.xlsx',sheet_name='deaths',names=["death"])

agedeath1=agedeath['death']
agedeath3=agedeath1.values
agedeath2=agedeath3[::-1]

plt.plot(C19.t,np.cumsum(np.sum(C19.storeVrate,axis=0)),label="storeVrate")
plt.plot(C19.t,np.cumsum(np.sum(C19.storefVrate,axis=0)),label="storefVrate")
plt.plot(np.sum(C19.S,axis=0),label="Sus")
plt.plot(np.sum(C19.SV1,axis=0),label="Vac1stdose")
plt.xlim(0,100)
plt.ylim(0)
plt.legend()
plt.show()

under301=agedeath1['g1'][0:146]+agedeath1['g2'][0:146]+agedeath1['g3'][0:146]+agedeath1['g4'][0:146]+agedeath1['g5'][0:146]+agedeath1['g6'][0:146]
forty1=agedeath1['g8'][0:146]+agedeath1['g7'][0:146]
fifty1=agedeath1['g10'][0:146]+agedeath1['g9'][0:146]
sixty1=agedeath1['g12'][0:146]+agedeath1['g11'][0:146]
seventy1=agedeath1['g14'][0:146]+agedeath1['g13'][0:146]+agedeath1['g15'][0:146]
eighty1=agedeath1['g16'][0:146]

under30=np.concatenate((nill,under301))
forty=np.concatenate((nill,forty1))
fifty=np.concatenate((nill,fifty1))
sixty=np.concatenate((nill,sixty1))
seventy=np.concatenate((nill,seventy1))
eighty=np.concatenate((nill,eighty1))

newdeath3=np.concatenate((nill,newdeath2))

fig, ax = plt.subplots()
fig.set_size_inches(18.5/2, 10.5/2)

im=ax.stackplot(C19.t,under30[0:146],forty[0:146],fifty[0:146],sixty[0:146],seventy[0:146],eighty[0:146],labels=['[0-29]','[30-39]','[40-49]','[50-59]','[60-69]','[70+]'],alpha=0.4,colors=blupalette)
#ax.plot(C19.t,newdeath3[0:146],'.',color='orange',label="Daily deaths data")
#ax.plot(C19.t,under30[0:146]+forty[0:146]+fifty[0:146]+sixty[0:146]+seventy[0:146],'.',color='orange')
#ax.plot(C19.t,under30[0:146]+forty[0:146]+fifty[0:146]+sixty[0:146],'.',color='orange')
ax.plot(np.sum(C19.Df,axis=0)[0:146],color='blue',ls='dotted',label="Model daily deaths")
ax.plot(np.sum(C19.Df,axis=0)[0:146]-np.sum([C19.Df[16]*0.7+C19.Df[15]],axis=0)[0:146],color='blue',ls='dotted')
ax.plot(np.sum(C19.Df,axis=0)[0:146]-np.sum([C19.Df[16]*0.95+C19.Df[15]],axis=0)[0:146]-np.sum([C19.Df[16]*0.05+C19.Df[14]],axis=0)[0:146],color='blue',ls='dotted')
plt.legend(title="Key")
plt.xlabel("Day of the simulation")
plt.ylabel("Number of daily deaths")
plt.title("Daily deaths by age interval")
plt.xlim(0,C19.Tmax)

plt.show()


C23 = MY_COVID(TotPop,I0,Tmax,d,weekR,Kf,nP,Vdelay,Vorder,Vrate,Vrate2,Vgap)
C23.my_covid()



newfat=fat[::-1]

newfat2=newfat.values
nill=np.zeros((33))
print(newfat2)
newfat3=np.concatenate((nill,newfat2))
print(newfat3)

#print(newfat3[47],"BOOP")
#print(newfat3[33],"BEEP")

plt.plot(np.sum(C19.I,axis=0)+np.sum(C19.H,axis=0)+np.sum(C19.A,axis=0),'g',label='Infected')

#plt.plot(np.sum(C19.H,axis=0),'r',label='death')
#plt.plot(np.sum(C19.A,axis=0),'c',label='death')
plt.show()


#plt.plot(np.sum(C19.Di,axis=0)+np.sum(C19.Dh,axis=0)+np.sum(C19.Da,axis=0))
#plt.title("peak daily infections")
#plt.show()


#plt.plot(np.sum(C19.Di,axis=0)+np.sum(C19.Dh,axis=0)+np.sum(C19.Da,axis=0))
#plt.plot(C19.Di[5]+C19.Dh[5]+C19.Da[5])
#plt.plot(C19.Di[16]+C19.Dh[16]+C19.Da[16])
#plt.title("peak daily infections")
#plt.show()


plt.plot(np.sum(C19.I,axis=0)+np.sum(C19.A,axis=0)+np.sum(C19.H,axis=0),'g',label='Infected')
plt.plot(np.sum(C19.IV1,axis=0)+np.sum(C19.AV1,axis=0)+np.sum(C19.HV1,axis=0),'r',label='VaccInfected')
plt.plot(np.sum(C19.IV2,axis=0)+np.sum(C19.AV2,axis=0)+np.sum(C19.HV2,axis=0),'r',label='VaccInfected')
plt.legend()
plt.title("peak daily infections")
plt.show()

plt.plot(np.sum(C19.IV1,axis=0)+np.sum(C19.AV1,axis=0)+np.sum(C19.HV1,axis=0),'r',label='VaccInfected')
plt.plot(np.sum(C19.IV2,axis=0)+np.sum(C19.AV2,axis=0)+np.sum(C19.HV2,axis=0),'r',label='VaccInfected')
plt.legend()
plt.title("peak daily infections")
plt.show()

plt.plot(np.sum(C19.Di,axis=0))
plt.plot(np.sum(C19.DiV1,axis=0))
plt.plot(np.sum(C19.DiV2,axis=0))
plt.title("peak s infections")
plt.show()

plt.plot(np.sum(C19.Df,axis=0)+np.sum(C19.DfV1,axis=0)+np.sum(C19.DfV2,axis=0))
plt.plot(C19.Df[16])
plt.plot(agedeath2[0:C19.Tmax],'.',color='orange')
plt.ylim(1)
plt.title("peak deaths infections")
plt.show()


plt.plot(C19.CHF[16])
plt.plot(C19.DiV1[16])
plt.title("peak deaths infections")
plt.show()

plt.plot(np.sum(C19.FV2,axis=0))
plt.plot(np.sum(C19.FV1,axis=0))
plt.title("peak deaths infections")
plt.show()


plt.plot(np.sum(C19.Dh,axis=0))
plt.plot(C19.Dh[16])
plt.title("peak hospp infections")
plt.show()


plt.plot(C19.Df[16])
plt.plot(C19.DfV1[15])
plt.plot(C19.SV1[14])
plt.show()

plt.plot(np.sum(C19.S,axis=0))
plt.plot(np.sum(C19.SV1,axis=0))
plt.plot(np.sum(C19.SV2,axis=0))
plt.title("vaccine proprotioj")
plt.show()



plt.plot(np.sum(C19.Dh,axis=0))
plt.plot(np.sum(C19.DhV1,axis=0))
plt.plot(np.sum(C19.DhV2,axis=0))
plt.title("peak deaths infections")
plt.show()

plt.plot(np.sum(C19.S,axis=0))
plt.plot(np.sum(C19.SV1,axis=0))
plt.plot(np.sum(C19.SV2,axis=0))
plt.title("susceptible")
plt.show()


print("DEATHS IN CAREHOME",sum(sum(C19.CHF)))
print("DEATHS HOSPITAL CAREHOME",(sum(C19.Df[16])-sum(sum(C19.CHF))))
print("DEATHS TOTAL CAREHOME",(sum(C19.Df[16])+sum(C19.DfV1[16])+sum(C19.DfV2[16])))

print("TOTAL INFECTIONS", sum(np.sum(C19.Dh,axis=0)[51:51+90])+sum(np.sum(C19.Di,axis=0)[51:51+C19.Tmax]))
print("TOTAL ASYMP INFECTIONS",sum(np.sum(C19.Da,axis=0)[51:51+C19.Tmax]))
print("TOTAL NEW HOSPITAL INFECTIONS",sum(np.sum(C19.Dh,axis=0)[51:51+C19.Tmax]))

print("TOTAL DEATHS",sum(sum(C19.Df))+sum(sum(C19.DfV1))+sum(sum(C19.DfV2)))
print("TOTAL GIVEN OUT VACCINE 1 st doses",sum(sum(C19.storeVrate)))
print("TOTAL EFFECTIVE VACCINE 1 st doses",sum(sum(C19.storefVrate)))
print("TOTAL EFFECTIVET VACCINE 2 nd doses",sum(sum(C19.storefVrate2)))


print(np.sum(C19.S,axis=0)+np.sum(C19.F,axis=0)+np.sum(C19.R,axis=0)+np.sum(C19.SV1,axis=0)+np.sum(C19.SV2,axis=0)+np.sum(C19.I,axis=0)+np.sum(C19.H,axis=0)+np.sum(C19.A,axis=0)+np.sum(C19.SV1,axis=0)+np.sum(C19.IV1,axis=0)+np.sum(C19.IV2,axis=0)+np.sum(C19.AV1,axis=0)+np.sum(C19.AV2,axis=0))
print("groups vaccinated", np.sum(C19.storeVrate,axis=1))
print(C19.TotPop)
#print("SUS",np.sum(C19.S,axis=0),np.sum(C19.SV1,axis=0),np.sum(C19.SV2,axis=0))

print(C19.SV2[16]+C19.SV1[16]+C19.S[16]+C19.R[16]+C19.F[16]+C19.A[16]+C19.H[16])
print("I WANNA CRY",C19.SV1[16],C19.SV1[15],C19.SV1[0])

#plt.plot(C19.F[15])
#plt.plot(C19.I[15]+C19.H[15]+C19.A[15])
#plt.plot(C19.H[15])
#plt.title("Di,Dh")
#plt.show()

#plt.plot(C19.Di[16][50:])
#plt.plot(C19.CHF[16][50:])
#plt.plot(C19.Df[16])
#plt.plot()
#plt.title("CHF,Df")
#plt.show()

#plt.plot(C19.Di[5][50:])
#plt.plot(C19.Df[5])
#plt.plot()
#plt.title("CHF,Df")
#plt.show()


#plt.plot(C19.t,np.sum(C19.Dh,axis=0)[51:])
#plt.plot(np.sum(C19.CHF,axis=0))
#plt.show()


#p=deaths[116:317]
#q=p[::-1]
#nill=np.zeros((37))
#r=np.concatenate((nill,q))
#plt.plot(np.sum(C19.Df,axis=0),'g',label='Infected')
#plt.plot(C19.t,newfat3[0:146])
#plt.show()


#plt.plot(np.sum(C19.Df,axis=0),'b',label='death')
#plt.plot(newfat3[0:146],'.',color='r')
#plt.show()
#print("PEAKDEATH,DF",max(np.sum(C19.Df,axis=0)),np.sum(C19.Df,axis=0)[70:80])
#print("PEAKINFECT,Di",max(np.sum(C19.Di,axis=0)),np.sum(C19.Di,axis=0)[40+51:50+51])
#fatal=np.array(deaths[::-1])
#print(np.cumsum(fatal))
#print(np.zeros((20)))
#print(fatal)
#nill=np.zeros((37))
#newdeath=np.concatenate((nill,fatal))

fig, ax = plt.subplots()
fig.set_size_inches(18.5/2, 10.5/2)



under30=C19.S[0]+C19.S[1]+C19.S[2]+C19.S[3]+C19.S[4]+C19.S[5]
forty=C19.S[6]+C19.S[7]
fifty=C19.S[8]+C19.S[9]
sixty=C19.S[10]+C19.S[11]
seventy=C19.S[12]+C19.S[13]
eighty=C19.S[14]+C19.S[15]
carehome=C19.S[16]
plt.stackplot(C19.t,under30,forty,fifty,sixty,seventy,eighty,carehome,labels=['Under 30','30-39','40-49','50-59','60-69','70-79','Carehome'],alpha=0.7,colors=blupalette)
#plt.plot(np.cumsum(newfat3[0:200]),'.',color='r')

plt.legend()
plt.show()



Vdelay=1000000
dose=43
C19 = MY_COVID(TotPop,I0,Tmax,d,weekR,Kf,nP,Vdelay,Vorder,Vrate,Vrate2,dose,Vprop1,Vprop2)
C19.my_covid()

midR=np.sum(C19.Df,axis=0)+np.sum(C19.DfV1,axis=0)+np.sum(C19.DfV2,axis=0)
Vdelay=1000000
dose=100
C20 = MY_COVID(TotPop,I0,Tmax,d,weekR,Kf,nP,Vdelay,Vorder,Vrate,Vrate2,dose,Vprop1,Vprop2)
C20.my_covid()

midR2=np.sum(C20.Df,axis=0)+np.sum(C20.DfV1,axis=0)+np.sum(C20.DfV2,axis=0)
midRinf=np.sum(C19.Di,axis=0)+np.sum(C19.Da,axis=0)+np.sum(C19.Dh,axis=0)+np.sum(C19.DiV1,axis=0)+np.sum(C19.DaV1,axis=0)+np.sum(C19.DhV1,axis=0)+np.sum(C19.DiV2,axis=0)+np.sum(C19.DaV2,axis=0)+np.sum(C19.DhV2,axis=0)

fig, ax = plt.subplots()
fig.set_size_inches(18.5/2, 10.5/2)
plt.plot(C19.t,midR,color='blue')
#plt.plot(C19.t,np.sum(C19.DfV1,axis=0),color='blue',label="1st dose vaccinated fatalities")
#plt.plot(C19.t,np.sum(C19.DfV2,axis=0),color='green',label="2nd dose vaccinated fatalities")
plt.plot(C19.t,midR2,color='blue',ls="dashdot")
#lt.plot(C19.t,np.sum(C20.DfV1,axis=0),color='blue',ls="dashdot")
#plt.plot(C19.t,np.sum(C20.DfV2,axis=0),color='green',ls="dashdot")
Vdelay=500000
dose=43
C19 = MY_COVID(TotPop,I0,Tmax,d,weekR,Kf,nP,Vdelay,Vorder,Vrate,Vrate2,dose,Vprop1,Vprop2)
C19.my_covid()


midR=np.sum(C19.Df,axis=0)+np.sum(C19.DfV1,axis=0)+np.sum(C19.DfV2,axis=0)
Vdelay=500000
dose=100
C20 = MY_COVID(TotPop,I0,Tmax,d,weekR,Kf,nP,Vdelay,Vorder,Vrate,Vrate2,dose,Vprop1,Vprop2)
C20.my_covid()

midR2=np.sum(C20.Df,axis=0)+np.sum(C20.DfV1,axis=0)+np.sum(C20.DfV2,axis=0)

plt.plot(C19.t,midR,color='skyblue')
plt.plot(C19.t,midR2,color='skyblue',ls="dashdot")

Vdelay=2000000
dose=43
C19 = MY_COVID(TotPop,I0,Tmax,d,weekR,Kf,nP,Vdelay,Vorder,Vrate,Vrate2,dose,Vprop1,Vprop2)
C19.my_covid()

midR=np.sum(C19.Df,axis=0)+np.sum(C19.DfV1,axis=0)+np.sum(C19.DfV2,axis=0)
Vdelay=2000000
dose=100
C20 = MY_COVID(TotPop,I0,Tmax,d,weekR,Kf,nP,Vdelay,Vorder,Vrate,Vrate2,dose,Vprop1,Vprop2)
C20.my_covid()

midR2=np.sum(C20.Df,axis=0)+np.sum(C20.DfV1,axis=0)+np.sum(C20.DfV2,axis=0)


plt.plot(C19.t,midR,color='red')
plt.plot(C19.t,midR2,color='red',ls="dashdot")


plt.legend(fontsize=12)
plt.xlim(42,C19.Tmax-1)
plt.ylim(0)
plt.xlabel("Day of simulation",fontsize=14)
plt.ylabel("Number of daily deaths",fontsize=14)
plt.show()

fig, ax = plt.subplots()
fig.set_size_inches(18.5/2, 10.5/2)
plt.plot(C19.t,np.cumsum(np.sum(C19.Df,axis=0)),color='red',label="Non-vaccinated fatalities")
plt.plot(C19.t,np.cumsum(np.sum(C19.DfV1,axis=0)),color='blue',label="1st dose vaccinated fatalities")
plt.plot(C19.t,np.cumsum(np.sum(C19.DfV2,axis=0)),color='green',label="2nd dose vaccinated fatalities")
plt.plot(C19.t,np.cumsum(np.sum(C20.Df,axis=0)),color='red',ls="dashdot")
plt.plot(C19.t,np.cumsum(np.sum(C20.DfV1,axis=0)),color='blue',ls="dashdot")
plt.plot(C19.t,np.cumsum(np.sum(C20.DfV2,axis=0)),color='green',ls="dashdot")
plt.legend(fontsize=12)
plt.xlim(42,C19.Tmax-1)
plt.ylim(0)
plt.xlabel("Day of simulation",fontsize=14)
plt.ylabel("Number of daily deaths",fontsize=14)
plt.show()


fig, ax = plt.subplots()
fig.set_size_inches(18.5/2, 10.5/2)
plt.plot(C19.t[0:100],np.sum(C19.DiV1,axis=0)[51:100+51],color='blue')
plt.plot(C19.t[0:100],np.sum(C19.DiV2,axis=0)[51:100+51],color='green')
plt.plot(C20.t[0:100],np.sum(C20.DiV1,axis=0)[51:100+51],color='blue',ls="dashdot")
plt.plot(C20.t[0:100],np.sum(C20.DiV2,axis=0)[51:100+51],color='green',ls="dashdot")
plt.legend(fontsize=12)
plt.xlim(42,C19.Tmax-1)
plt.ylim(0)
plt.xlabel("Day of simulation",fontsize=14)
plt.ylabel("Number of daily deaths",fontsize=14)
plt.show()




fig, ax = plt.subplots()
fig.set_size_inches(18.5/2, 10.5/2)
under30=C19.Df[0]+C19.Df[1]+C19.Df[2]+C19.Df[3]+C19.Df[4]+C19.Df[5]
forty=C19.Df[6]+C19.Df[7]
fifty=C19.Df[8]+C19.Df[9]
sixty=C19.Df[10]+C19.Df[11]
seventy=C19.Df[12]+C19.Df[13]
eighty=C19.Df[14]+C19.Df[15]
carehome=C19.Df[16]
#ax.plot(agedeath2[0:C19.Tmax],'.',color='orange')
#ax.plot(agedeath2[0:C19.Tmax],ls='dotted',color='blue')
ax.stackplot(C19.t,under30,forty,fifty,sixty,seventy,eighty,carehome,labels=['Under 30','[30-39]','[40-49]','[50-59]','[60-69]','[70-79]','Carehomes'],alpha=0.7,colors=blupalette)
#plt.plot(np.cumsum(newfat3[0:200]),'.',color='r')
plt.legend(loc="upper left",fontsize=12)
plt.xlim(0,C19.Tmax-1)
plt.ylim(0)
plt.xlabel("Day of simulation",fontsize=14)
plt.ylabel("Number of daily deaths",fontsize=14)
plt.show()

fig, ax = plt.subplots()
fig.set_size_inches(18.5/2, 10.5/2)
under30=C19.DfV1[0]+C19.DfV1[1]+C19.DfV1[2]+C19.DfV1[3]+C19.DfV1[4]+C19.DfV1[5]
forty=C19.DfV1[6]+C19.DfV1[7]
fifty=C19.DfV1[8]+C19.DfV1[9]
sixty=C19.DfV1[10]+C19.DfV1[11]
seventy=C19.DfV1[12]+C19.DfV1[13]
eighty=C19.DfV1[14]+C19.DfV1[15]
carehome=C19.DfV1[16]
#ax.plot(agedeath2[0:C19.Tmax],'.',color='orange')
#ax.plot(agedeath2[0:C19.Tmax],ls='dotted',color='blue')
ax.stackplot(C19.t,under30,forty,fifty,sixty,seventy,eighty,carehome,labels=['Under 30','[30-39]','[40-49]','[50-59]','[60-69]','[70-79]','Carehomes'],alpha=0.7,colors=blupalette)
#plt.plot(np.cumsum(newfat3[0:200]),'.',color='r')
plt.legend(loc="upper left",fontsize=12)
plt.xlim(0,C19.Tmax-1)
plt.ylim(0)
plt.xlabel("Day of simulation",fontsize=14)
plt.ylabel("Number of daily deaths",fontsize=14)
plt.show()




#i#m = ax.imshow(combined3, norm=DivergingNorm(0), cmap='seismic_r', interpolation='none')
#fig.colorbar(im)
#plt.yticks(np.arange(0, 17, 1.0),labels=['[0,5]','[5,10]','[10,15]','[15,20]','[20,25]','[25,30]','[30,35]','[35,40]','[40,45]','[45,50]','[50,55]','[55,60]','[60,65]','[65,70]','[70,75]','[75+]','Carehomes'])
#plt.xticks(np.arange(0, 17, 1.0),labels=['[0,5]','[5,10]','[10,15]','[15,20]','[20,25]','[25,30]','[30,35]','[35,40]','[40,45]','[45,50]','[50,55]','[55,60]','[60,65]','[65,70]','[70,75]','[75+]','Carehomes'])
#plt.setp(ax.get_xticklabels(), rotation=50, ha="right",rotation_mode="anchor",fontsize=11)

#plt.show()

fig, ax = plt.subplots()
fig.set_size_inches(18.5/2, 10.5/2)
dose=43
Vorder=[12,11,10,9,8,7,6,5,4,3,2,1,0]
C19 = MY_COVID(TotPop,I0,Tmax,d,weekR,Kf,nP,Vdelay,Vorder,Vrate,Vrate2,dose,Vprop1,Vprop2)
C19.my_covid()

midR=np.sum(C19.Df,axis=0)+np.sum(C19.DfV1,axis=0)+np.sum(C19.DfV2,axis=0)
midRinf=np.sum(C19.Di,axis=0)+np.sum(C19.Da,axis=0)+np.sum(C19.Dh,axis=0)+np.sum(C19.DiV1,axis=0)+np.sum(C19.DaV1,axis=0)+np.sum(C19.DhV1,axis=0)+np.sum(C19.DiV2,axis=0)+np.sum(C19.DaV2,axis=0)+np.sum(C19.DhV2,axis=0)
print("vac doses working 43",sum(sum(C19.storeVrate)),sum(sum(C19.storefVrate2)))
print(sum(sum(C19.storefVrate)))
Vorder=[16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0]
C20 = MY_COVID(TotPop,I0,Tmax,d,weekR,Kf,nP,Vdelay,Vorder,Vrate,Vrate2,dose,Vprop1,Vprop2)
C20.my_covid()


lowR=np.sum(C20.Df,axis=0)+np.sum(C20.DfV1,axis=0)+np.sum(C20.DfV2,axis=0)
lowRinf=np.sum(C20.Di,axis=0)+np.sum(C20.Da,axis=0)+np.sum(C20.Dh,axis=0)+np.sum(C20.DiV1,axis=0)+np.sum(C20.DaV1,axis=0)+np.sum(C20.DhV1,axis=0)+np.sum(C20.DiV2,axis=0)+np.sum(C20.DaV2,axis=0)+np.sum(C20.DhV2,axis=0)
print("vac doses old t young dose 43",sum(sum(C20.storeVrate)),sum(sum(C20.storefVrate2)))
print(sum(sum(C20.storefVrate)))

im=ax.plot(midR[0:250],zorder=7,color='blue',label="Working population vaccinated first, 3 week gap")
ax.plot(lowR[0:250],zorder=7,color='orange',label="Oldest to youngest vaccinated first, 3 week gap")

dose=105
Vorder=[12,11,10,9,8,7,6,5,4,3,2,1,0]
C19 = MY_COVID(TotPop,I0,Tmax,d,weekR,Kf,nP,Vdelay,Vorder,Vrate,Vrate2,dose,Vprop1,Vprop2)
C19.my_covid()

midR2=np.sum(C19.Df,axis=0)+np.sum(C19.DfV1,axis=0)+np.sum(C19.DfV2,axis=0)
midRinf2=np.sum(C19.Di,axis=0)+np.sum(C19.Da,axis=0)+np.sum(C19.Dh,axis=0)+np.sum(C19.DiV1,axis=0)+np.sum(C19.DaV1,axis=0)+np.sum(C19.DhV1,axis=0)+np.sum(C19.DiV2,axis=0)+np.sum(C19.DaV2,axis=0)+np.sum(C19.DhV2,axis=0)
print("vac doses working dose 105",sum(sum(C19.storeVrate)),sum(sum(C19.storefVrate2)))
print(sum(sum(C19.storefVrate)))
Vorder=[16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0]
C20 = MY_COVID(TotPop,I0,Tmax,d,weekR,Kf,nP,Vdelay,Vorder,Vrate,Vrate2,dose,Vprop1,Vprop2)
C20.my_covid()
print("vac doses old t young dose 105",sum(sum(C20.storeVrate)),sum(sum(C20.storefVrate2)))
print(sum(sum(C20.storefVrate)))

lowR2=np.sum(C20.Df,axis=0)+np.sum(C20.DfV1,axis=0)+np.sum(C20.DfV2,axis=0)
lowRinf2=np.sum(C20.Di,axis=0)+np.sum(C20.Da,axis=0)+np.sum(C20.Dh,axis=0)+np.sum(C20.DiV1,axis=0)+np.sum(C20.DaV1,axis=0)+np.sum(C20.DhV1,axis=0)+np.sum(C20.DiV2,axis=0)+np.sum(C20.DaV2,axis=0)+np.sum(C20.DhV2,axis=0)


im=ax.plot(midR2[0:250],zorder=7,color='blue',ls='dashdot',label="Working population vaccinated first, 12 week gap")
ax.plot(lowR2[0:250],zorder=7,color='orange',ls='dashdot',label="Oldest to youngest vaccinated first, 12 week gap")

C21 = MY_COVID(TotPop,I0,Tmax,d,weekR,Kf,nP,Vdelay,Vorder,Vrate,Vrate2,Vgap)
C21.my_covid()

midR=np.sum(C21.Df,axis=0)
midRinf=np.sum(C21.Di,axis=0)+np.sum(C21.Da,axis=0)+np.sum(C21.Dh,axis=0)


#ax.fill_between(C19.t,midR[0:146],highR[0:146],alpha=0.1,color='blue',zorder=0)
#ax.fill_between(C19.t,lowR[0:146],midR[0:146],alpha=0.1,color='blue',zorder=0)
#plt.plot(newfat3[0:146],'.',zorder=3,label="Daily death data")
#plt.axvline(33,color='red')#,label='02/03: First UK death')
#plt.axvline(47,color='yellow')#,label="16/03: Lockdown Announced, partial measures introduced")
#plt.axvline(49,color='orange')#,label="18/03: Peak daily infections")
##plt.axvline(54,color='green')#,label="23/03: Official Lockdown starts")
#plt.axvline(70,color='blue')#,label="08/04: Peak daily deaths")
plt.xlim(0,249)
plt.ylim(0)
plt.grid(linestyle="--",zorder=0)
plt.xlabel("Day of simulation",fontsize=14)
plt.ylabel("Number of daily deaths",fontsize=14)
#plt.legend()
#plt.legend(title="Key dates",bbox_to_anchor=(0,0,0.5,-0.15))
plt.show()

fig, ax = plt.subplots()
fig.set_size_inches(18.5/2, 10.5/2)
im=ax.plot(midRinf[51:250+51],zorder=7,color='blue',label="Working population vaccinated first, 3 week gap")
ax.plot(lowRinf[51:250+51],zorder=7,color='orange',label="Oldest to youngest vaccinated first, 3 week gap")
im=ax.plot(midRinf2[51:250+51],zorder=7,color='blue',ls='dashdot',label="Working population vaccinated first, 12 week gap")
ax.plot(lowRinf2[51:250+51],zorder=7,color='orange',ls='dashdot',label="Oldest to youngest vaccinated first, 12 week gap")
plt.xlim(0,249)
plt.grid(linestyle="--",zorder=0)
plt.xlabel("Day of simulation",fontsize=14)
plt.ylabel("Number of new daily infections",fontsize=14)
plt.show()

fig, ax = plt.subplots()
fig.set_size_inches(18.5, 10.5)
Vorder=[16,15,14,13,12,11,10,9,8,7,6,5,4,3,2,1,0]
C19 = MY_COVID(TotPop,I0,Tmax,d,weekR,Kf,nP,Vdelay,Vorder,Vrate,Vrate2,Vgap,Vprop1,Vprop2)
C19.my_covid()
midR=np.sum(C19.Df,axis=0)
midRinf=np.sum(C19.Di,axis=0)+np.sum(C19.Da,axis=0)+np.sum(C19.Dh,axis=0)
im=ax.plot(midR[0:100],zorder=7,label="Oldest to youngest")
Vorder=[16,12,11,10,9,8,7,6,5,4,3,2,1,0]
C19 = MY_COVID(TotPop,I0,Tmax,d,weekR,Kf,nP,Vdelay,Vorder,Vrate,Vrate2,Vgap,Vprop1,Vprop2)
C19.my_covid()
midR=np.sum(C19.Df,axis=0)
midRinf=np.sum(C19.Di,axis=0)+np.sum(C19.Da,axis=0)+np.sum(C19.Dh,axis=0)
im=ax.plot(midR[0:100],zorder=7,label="[16,12,11,10,9,8,7,6,5,4,3,2,1,0,15,14]")
Vorder=[16,15,12,11,10,9,8,7,6,5,4,3,2,1,0]
C19 = MY_COVID(TotPop,I0,Tmax,d,weekR,Kf,nP,Vdelay,Vorder,Vrate,Vrate2,Vgap,Vprop1,Vprop2)
C19.my_covid()
midR=np.sum(C19.Df,axis=0)
midRinf=np.sum(C19.Di,axis=0)+np.sum(C19.Da,axis=0)+np.sum(C19.Dh,axis=0)
im=ax.plot(midR[0:100],zorder=7,label="[16,15,12,11,10,9,8,7,6,5,4,3,2,1,0,14]")
Vorder=[16,15,14,12,11,10,9,8,7,6,5,4,3,2,1,0]
C19 = MY_COVID(TotPop,I0,Tmax,d,weekR,Kf,nP,Vdelay,Vorder,Vrate,Vrate2,Vgap,Vprop1,Vprop2)
C19.my_covid()
midR=np.sum(C19.Df,axis=0)
midRinf=np.sum(C19.Di,axis=0)+np.sum(C19.Da,axis=0)+np.sum(C19.Dh,axis=0)
im=ax.plot(midR[0:100],zorder=7,label="[16,15,14,12,11,10,9,8,7,6,5,4,3,2,1,0]")
Vorder=[16,6,5,4,3,2,1,0]
C19 = MY_COVID(TotPop,I0,Tmax,d,weekR,Kf,nP,Vdelay,Vorder,Vrate,Vrate2,Vgap,Vprop1,Vprop2)
C19.my_covid()
midR=np.sum(C19.Df,axis=0)
midRinf=np.sum(C19.Di,axis=0)+np.sum(C19.Da,axis=0)+np.sum(C19.Dh,axis=0)
im=ax.plot(midR[0:100],zorder=7,label="[16,5,6,7,8,9,10,11,12,13,14,15]")
Vorder=[16,15,6,5,4,3,2,1,0]
C19 = MY_COVID(TotPop,I0,Tmax,d,weekR,Kf,nP,Vdelay,Vorder,Vrate,Vrate2,Vgap,Vprop1,Vprop2)
C19.my_covid()
midR=np.sum(C19.Df,axis=0)
midRinf=np.sum(C19.Di,axis=0)+np.sum(C19.Da,axis=0)+np.sum(C19.Dh,axis=0)
im=ax.plot(midR[0:100],zorder=7,label="[16,15,5,6,7,8,9,10,11,12,13,14]")
Vorder=[16,15,14,6,5,4,3,2,1,0]
C19 = MY_COVID(TotPop,I0,Tmax,d,weekR,Kf,nP,Vdelay,Vorder,Vrate,Vrate2,Vgap,Vprop1,Vprop2)
C19.my_covid()
midR=np.sum(C19.Df,axis=0)
midRinf=np.sum(C19.Di,axis=0)+np.sum(C19.Da,axis=0)+np.sum(C19.Dh,axis=0)
im=ax.plot(midR[0:100],zorder=7,label="[16,15,14,6,7,8,9,10,11,12,13]")


plt.xlim(0,99)
plt.ylim(0)
plt.legend()
plt.xlabel("Day of simulation",fontsize=14)
plt.ylabel("Number of daily deaths",fontsize=14)
plt.show()




fig, ax = plt.subplots()
fig.set_size_inches(18.5/2, 10.5/2)

ax.fill_between(C19.t,midR[0:146],highR[0:146],alpha=0.2,color='blue',zorder=0)
ax.fill_between(C19.t,lowR[0:146],midR[0:146],alpha=0.1,color='blue',zorder=0)
im=ax.plot(midR[0:146],ls="dotted",zorder=5)
plt.plot(newfat3[0:146],'.',zorder=3)
plt.axvline(33,color='r',label='02/03: First UK death')
plt.axvline(47,color='yellow',label="16/03: Lockdown Announced, partial measures introduced")
plt.axvline(49,color='orange',label="18/03: Peak daily infections")
plt.axvline(54,color='green',label="23/03: Official Lockdown starts")
plt.axvline(70,color='blue',label="08/04: Peak daily deaths")
plt.xlim(20,144)
plt.xlabel("Day of simulation")
plt.ylabel("Daily deaths")
plt.title("Modelling daily deaths in England during Covid-19 first wave")
#plt.legend(title="Key dates",bbox_to_anchor=(0,0,0.7,-0.15))
plt.show()



C19 = MY_COVID(TotPop,I0,Tmax,d,weekRlate,Kf,nP,Vdelay,Vorder,Vrate,Vrate2,Vgap)
C19.my_covid()
highR=np.sum(C19.Df,axis=0)
print("FUCKIN READ LATE LOCKDEATHS",sum(highR))
highRinf=np.array(np.sum(C19.Di,axis=0)+np.sum(C19.Da,axis=0)+np.sum(C19.Dh,axis=0))[51:51+146]
C20 = MY_COVID(TotPop,I0,Tmax,d,weekRearly,Kf,nP,Vdelay,Vorder,Vrate,Vrate2,Vgap)
C20.my_covid()
lowR=np.sum(C20.Df,axis=0)
lowRinf=np.array(np.sum(C20.Di,axis=0)+np.sum(C20.Da,axis=0)+np.sum(C20.Dh,axis=0))[51:51+146]
print("FUCKIN READ EARLY LOCKDEATHS",sum(lowR))
C21 = MY_COVID(TotPop,I0,Tmax,d,weekR,Kf,nP,Vdelay,Vorder,Vrate,Vrate2,Vgap)
C21.my_covid()
midR=np.sum(C21.Df,axis=0)
midRinf=np.array(np.sum(C21.Di,axis=0)+np.sum(C21.Da,axis=0)+np.sum(C21.Dh,axis=0))[51:51+146]
print("FUCKIN LOCKDEATHS",sum(midR))
fig, ax = plt.subplots()
fig.set_size_inches(18.5/2, 10.5/2)

ax.fill_between(C19.t,midR[0:146],highR[0:146],alpha=0.1,color='red',zorder=0)
ax.fill_between(C19.t,lowR[0:146],midR[0:146],alpha=0.1,color='green',zorder=0)
ax.plot(lowR[0:146],color='green',ls="dotted",label="Model deaths: 09/03 early Lockdown")
im=ax.plot(midR[0:146],color='blue',ls="dotted",label="Model deaths: 16/03 Lockdown",zorder=5)
ax.plot(highR[0:146],color='red',ls="dotted",label="Model deaths: 23/03 late Lockdown")

plt.plot(newfat3[0:146],'.',color='orange',label="Daily deaths data",zorder=3)
plt.axvline(47-7,color='green',label="09/03: Lockdown Announced 1 week earlier")
plt.axvline(47,color='blue',label="16/03: Lockdown Announced")
plt.axvline(47+7,color='red',label="23/03: Lockdown Announced 1 week later")
plt.xlim(20,144)
plt.ylim(1)
plt.xlabel("Day of simulation")
plt.ylabel("Log-scale daily deaths")
plt.title("Modelling potential daily deaths with varying dates of Lockdown")
plt.legend(bbox_to_anchor=(0,0,0.5,-0.15))
plt.show()

fig, ax = plt.subplots()
fig.set_size_inches(18.5/2, 10.5/2)

ax.fill_between(C19.t,midRinf[0:146],highRinf[0:146],alpha=0.2,color='red',zorder=0)
ax.fill_between(C19.t,lowRinf[0:146],midRinf[0:146],alpha=0.2,color='green',zorder=0)
ax.plot(lowRinf[0:146],color='green',ls="dotted",label="Model deaths: 09/03 early Lockdown")
im=ax.plot(midRinf[0:146],color='blue',ls="dotted",label="Model deaths: 16/03 Lockdown",zorder=5)
ax.plot(highRinf[0:146],color='red',ls="dotted",label="Model deaths: 23/03 late Lockdown")
plt.axvline(47-7,color='green',label="09/03: Lockdown Announced 1 week earlier")
plt.axvline(47,color='blue',label="16/03: Lockdown Announced")
plt.axvline(47+7,color='red',label="23/03: Lockdown Announced 1 week later")
plt.xlim(20,100)
plt.ylim(100,500000)
plt.yscale("log")
plt.xlabel("Day of simulation")
plt.ylabel("Log-scale daily infections")
plt.title("Modelling potential daily infections with varying dates of Lockdown")
plt.legend(bbox_to_anchor=(0,0,0.5,-0.15))
plt.show()

fig, ax = plt.subplots()
fig.set_size_inches(18.5/2, 10.5/2)

ax.fill_between(C19.t,midRinf[0:146],highRinf[0:146],alpha=0.2,color='red',zorder=0)
ax.fill_between(C19.t,lowRinf[0:146],midRinf[0:146],alpha=0.2,color='green',zorder=0)
ax.plot(lowRinf[0:146],color='green',ls="dotted",label="Model deaths: 09/03 early Lockdown")
im=ax.plot(midRinf[0:146],color='blue',ls="dotted",label="Model deaths: 16/03 Lockdown",zorder=5)
ax.plot(highRinf[0:146],color='red',ls="dotted",label="Model deaths: 23/03 late Lockdown")
plt.axvline(47-7,color='green',label="09/03: Lockdown Announced 1 week earlier")
plt.axvline(47,color='blue',label="16/03: Lockdown Announced")
plt.axvline(47+7,color='red',label="23/03: Lockdown Announced 1 week later")
plt.xlim(20,100)
plt.ylim(100,500000)
plt.xlabel("Day of simulation")
plt.ylabel("Log-scale daily infections")
plt.title("Modelling potential daily infections with varying dates of Lockdown")
plt.legend(bbox_to_anchor=(0,0,0.5,-0.15))
plt.show()



under30=C19.Di[0]+C19.Di[1]+C19.Di[2]+C19.Di[3]+C19.Di[4]+C19.Di[5]+C19.Di[0]
forty=C19.Di[6]+C19.Di[7]
fifty=C19.Di[8]+C19.Di[9]
sixty=C19.Di[10]+C19.Di[11]
seventy=C19.Di[12]+C19.Di[13]
eighty=C19.Di[14]+C19.Di[15]
carehome=C19.Di[16]
plt.stackplot(C19.t,under30[51:],forty[51:],fifty[51:],sixty[51:],seventy[51:],eighty[51:],carehome[51:],labels=['Under 30','30-39','40-49','50-59','60-69','70-79','Carehome'],colors=blupalette)
plt.legend()
plt.show()

fig, ax = plt.subplots()
fig.set_size_inches(18.5/2, 10.5/2)

under30=C19.I[0]+C19.I[1]+C19.I[2]+C19.I[3]+C19.I[4]+C19.I[5]+C19.H[0]+C19.H[1]+C19.H[2]+C19.H[3]+C19.H[4]+C19.H[5]
forty=C19.I[6]+C19.I[7]+C19.H[6]+C19.H[7]
fifty=C19.I[8]+C19.I[9]+C19.H[8]+C19.H[9]
sixty=C19.I[10]+C19.I[11]+C19.H[10]+C19.H[11]
seventy=C19.I[12]+C19.I[13]+C19.H[12]+C19.H[13]
eighty=C19.I[14]+C19.I[15]+C19.H[14]+C19.H[15]
carehome=C19.I[16]+C19.H[16]

#ax.plot(agedeath2[0:C19.Tmax],ls='dotted',color='blue')
ax.stackplot(C19.t,under30,forty,fifty,sixty,seventy,eighty,carehome,labels=['Under 30','[30-39]','[40-49]','[50-59]','[60-69]','[70-79]','Carehomes'],alpha=0.7,colors=blupalette)
#plt.plot(np.cumsum(newfat3[0:200]),'.',color='r')
plt.legend(loc="upper left",fontsize=12)
plt.xlim(0,99)
plt.ylim(0)
plt.xlabel("Day of simulation",fontsize=14)
plt.ylabel("Number of current symptomatic infections",fontsize=14)
plt.show()




under30=C19.H[0]+C19.H[1]+C19.H[2]+C19.H[3]+C19.H[4]+C19.H[5]+C19.H[0]
forty=C19.H[6]+C19.H[7]
fifty=C19.H[8]+C19.H[9]
sixty=C19.H[10]+C19.H[11]
seventy=C19.H[12]+C19.H[13]
eighty=C19.H[14]+C19.H[15]
carehome=C19.H[16]
plt.stackplot(C19.t,under30,forty,fifty,sixty,seventy,eighty,carehome,labels=['Under 30','30-39','40-49','50-59','60-69','70-79','80+'],colors=blupalette)
plt.legend()
plt.show()

#plt.plot(Pr)
#plt.show()
#print("Sum Pr =",sum(Pr))
#print("Sum Pinf =",sum(Pinf))

print(min(C21.Di[16]),min(C21.Di[16]),min(C21.Da[16]))
print("Total infections:",sum(np.sum(C21.Di,axis=0))+sum(np.sum(C21.Dh,axis=0))+sum(np.sum(C21.Da,axis=0)))
print("Infections By Group:",(np.sum(C21.Di,axis=1)+np.sum(C21.Dh,axis=1)+np.sum(C21.Da,axis=1)))

print("Total Deaths:",sum(np.sum(C21.Df,axis=0)))
print("Deaths By Group:",(np.sum(C21.Df,axis=1)))

print("Total Hosps:",sum(np.sum(C21.Dh,axis=0)))
print("Hosp By Group:",(np.sum(C21.Dh,axis=1)))

print("Hosp Death By Group:",(np.sum(C21.Dh,axis=1)*C21.Hf))

print("Total Care home non-hosp Death:",sum(np.sum(C21.CHF,axis=0)))
print(C21.Hf)

Di=C19.Di
Dr=C19.Dr
Infe=C19.I
sumcon=0
sumcd=0
for i in range(0,17):
    print(i)
    for j in range(0,17):
        sumcon+=(C19.contact[i][j]/(sum(C19.contact[j])))
    print("the sumcontact of group",i,"used to calculate infections created in group",i,"from other groups",sumcon)
    sumcd+=sumcon
    sumcon=0
print(sumcd,"total influence of infections on each group by others")
sumcd2=0
for j in range(0,17):
    print(j)
    for i in range(0,17):
        sumcon+=(C19.contact[i][j]/(sum(C19.contact[j])))
    print("the sumcontact of produced by group",j,"used to calculate infections created by group",j,"in other groups",sumcon)
    sumcd2+=sumcon
    sumcon=0
print(sumcd,"total influence of infections of each group")
  
    
sumc=[0.76418094361674,0.8796718372911431,0.9489493440069919,1.0386007518837457,1.0620359989638846,1.1737508675133215,1.064023438568784,1.1475576586854337,1.0810414900703413,1.0775608625098698,0.9691229540844309,1.0378652205732475,0.676970208388224,0.7861349074384673,0.9857911792890166,0.7361670905538034,0.7361670905538034]

print(C19.I[15])
print(C19.I[14])

print(C19.I[16])
"""
