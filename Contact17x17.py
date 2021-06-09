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
        combined31= pd.read_excel('covidmatrix.xlsx',sheet_name='normal')
        combined3=combined31.values
        prop= np.dot(55.98e6/66.27,[3.86,4.15,3.95,3.66,4.15,4.51,4,4.4,4.02,4.4,4.66,4.41,3.76,3.37,3.32,5.7-0.376200,0.418000])
        store=np.zeros(shape=(17,17))
        for i in range(0,17):
            for j in range(0,17):
                store[i][j]=(1/(2*prop[i]))*(combined3[i][j]*prop[j]+combined3[j][i]*prop[i])
        dett=np.linalg.eigvals(store)
        return store/max(dett)
    
