#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 17:28:30 2021

@author: meg
"""
import numpy as np
import pandas as pd

class Contactclass17:
    
    def __init__(self, trace_n=10):
        self.a0 = [0]
        self.trace_n = trace_n # tracing step no
        self.min = None
        self.max = None

    def contactmatrix():
        school2 = pd.read_excel('covidmatrix.xlsx',sheet_name='School')
        school2=school2.values
        work2 = pd.read_excel('covidmatrix.xlsx',sheet_name='Work')
        work2=work2.values
        other2 = pd.read_excel('covidmatrix.xlsx',sheet_name='Other')
        other2=other2.values
        home2 = pd.read_excel('covidmatrix.xlsx',sheet_name='Home')
        home2=home2.values
        full=pd.read_excel('covidmatrix.xlsx',sheet_name='normal')
        full2=full.values
        home2=np.delete(home2,0,1)
        other2=np.delete(other2,0,1)
        work2=np.delete(work2,0,1)
        school2=np.delete(school2,0,1)
        combined31= pd.read_excel('covidmatrix.xlsx',sheet_name='normal')
        combined31=combined31.values
        prop= np.dot(55.98e6/66.27,[3.86,4.15,3.95,3.66,4.15,4.51,4,4.4,4.02,4.4,4.66,4.41,3.76,3.37,3.32,5.7-0.376200,0.418000])
        store=np.zeros(shape=(17,17))
        for i in range(0,17):
            for j in range(0,17):
                store[i][j]=(1/(2*prop[i]))*(combined3[i][j]*prop[j]+combined3[j][i]*prop[i])
        dett=np.linalg.eigvals(store)
        return store/max(dett)
    


school=[[0.815589,0.066048688,0.039809875,0.001824188],[0.063834875,0.040088688,0.015466813,0.001404],[0.042693625,0.017459125,0.036170875,0.000462938],[0.018119625,0.015920563,0.006469125,0.000295938]]
work=[[0.069437698,0.10229876,	0.066092578,	0.001067727],[0.090440398,0.660674776,0.433904061,0.004201923],[0.054352773,	0.47738693,	0.486605976,	0.007610283],[2.36736E-06,0.01373065,0.014285468,0.000134875]]
other=[[0.377628002,	0.200896461,	0.159691956,	0.039335821],[0.193632127	,0.466123017,0.227936182,0.062451804],[0.099835386	,0.340819111,0.376441602,0.11669539],[0.064191556,	0.264398061,	0.351792739	,0.24367375]]
home=[[0.446055359,	0.24227306,	0.131888211,	0.003621577],[0.284229361	,0.236494806	,0.076484679	,0.006193877],[0.263090124	,0.115944057	,0.158096849	,0.011907469],[0.060798328	,0.03597532	,0.074062669,0.126663579]]

#If schools shut, set school=0, increase 0-19 home interaction by 50%
A=np.diag((1.5,1.5,1.5,1.5,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1,1.1))
B=np.diag((0.5,0.5,0.5,0.5,1,1,1,1,1,1,1,1,1,1,1,1,1))
C=np.diag((0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5,0.5))
E=np.diag((1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1))
#print(A,B,C)


school2 = pd.read_excel('covidmatrix.xlsx',sheet_name='School')
school2.to_numpy()
full=pd.read_excel('covidmatrix.xlsx',sheet_name='normal')
full2=full.values
work2 = pd.read_excel('covidmatrix.xlsx',sheet_name='Work')
work2.to_numpy()
other2 = pd.read_excel('covidmatrix.xlsx',sheet_name='Other')
other2.to_numpy()
home2 = pd.read_excel('covidmatrix.xlsx',sheet_name='Home')
home2.to_numpy()
school2 = pd.read_excel('covidmatrix.xlsx',sheet_name='School')
school2=school2.values
work2 = pd.read_excel('covidmatrix.xlsx',sheet_name='Work')
work2=work2.values
other2 = pd.read_excel('covidmatrix.xlsx',sheet_name='Other')
other2=other2.values
home2 = pd.read_excel('covidmatrix.xlsx',sheet_name='Home')
home2=home2.values
home2=np.delete(home2,0,1)
other2=np.delete(other2,0,1)
work2=np.delete(work2,0,1)
school2=np.delete(school2,0,1)
combined3=np.dot(A,home2)+np.dot(B,other2)+np.dot(C,work2)

#print(combined3)

combined31= pd.read_excel('covidmatrix.xlsx',sheet_name='normal')
combined3=combined31.values
prop= np.dot(55.98e6/66.27,[3.86,4.15,3.95,3.66,4.15,4.51,4,4.4,4.02,4.4,4.66,4.41,3.76,3.37,3.32,5.7-0.376200,0.418000])
store=np.zeros(shape=(17,17))
for i in range(0,17):
    for j in range(0,17):
        store[i][j]=(1/(2*prop[i]))*(combined3[i][j]*prop[j]+combined3[j][i]*prop[i])
dett=np.linalg.eigvals(store)
store=store/max(dett)
hosp=np.array([0,0.0026,0.00084,0.00042,0.0008,0.0026,0.004,0.0063,0.012,0.019,0.023,0.04,0.096,0.1,0.24,0.5,0.2])
print(max(dett),"dett")
poop3=hosp*store
poop1=np.dot(0.6-hosp,store,)*0.33877
poop2=(0.4*0.3007*store)
rnumber=np.linalg.eigvals(store*(hosp*0.24787)+0.33877*(store*(0.6-hosp))+(0.4*0.3007*(store)))
print(max(rnumber))
rnumber=np.linalg.eigvals(store*(hosp*0.38457)+0.590669*(store*(0.6-hosp))+(0.4*0.3007*(store)))
print(max(rnumber))



