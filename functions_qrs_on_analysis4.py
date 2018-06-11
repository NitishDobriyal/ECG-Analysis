# -*- coding: utf-8 -*-
"""
Created on Tue Jun  5 12:08:00 2018

@author: Nitish
"""

'''
WE FOUND OUT THE HEARTBEATS BY THE ABOVE CODE,NOW WE HAVE TO FIND THE QRS COMPLEX,JUST BY PEAKS THAT TOO
FROM OUR ORIGINAL ARRAY

T=(S(LOC)+x) - (Q(LOC)-x)/t(S) = QRS COMPLEX

'''
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from numpy import inf

colnames=['Time','Lead2']

#ds1=pd.read_csv('4.csv',names=colnames,header=None).tail(5000)

ds1=pd.read_csv('9.csv',names=colnames,header=None)

x=ds1.iloc[75000:80000,1]


class ECG:                                        
    def peakfinder(self,derivative_arr,peaks):    #To calculate peaks when you have more peaks in one crest(Ist peak logic)

        i=0
        Lower_B=[]
        Upper_B=[]
        #calculation of main peaks
        while(i<len(derivative_arr)):    
            currentMax = derivative_arr[i]
            maxIndex=i
            i=i+1
            maxm=False
            while(i<len(derivative_arr) and derivative_arr[i]>=threshold ):      
                maxm=True
                if(derivative_arr[i]>currentMax):       
                    currentMax = derivative_arr[i]
                    maxIndex = i    
                i=i+1
            if (maxm == True):
                peaks.append(maxIndex)#peaks is an list containing x-indices of main pulse peaks
                Upper_B.append(maxIndex+20)
                Lower_B.append(maxIndex-20)
                i=i+1
                
        return peaks
    
    def peaks_deriv_to_orig(self,derivative_arr,peaks):
        minIndex=0
        for i in range(0,len(peaks)-1):
            m=peaks[i]
            while(derivative_arr[m]>=0): #i.e the derivative curve can't be zero,while slope is decreasing
                min=derivative_arr[m]
                minIndex=m
                m=m+1
            R_peaks.append(minIndex)
        return R_peaks
    
    def heartbeat_calc(self,R_peaks,heartbeat):
        diff=[]
        time=[]
        for i in range(0,len(R_peaks)-1):
            diff.append(R_peaks[i+1]-R_peaks[i])
            time.append(diff[i]*2)
            
        #Calculating the heartbeats
        for i in range(0,len(time)-1):
            heartbeat.append(60000/time[i])
        
        return heartbeat
    
    def Q_peaks_calc(self,orig_arr,Q_peaks): 
        minINDEX=0
        for i in range(1,len(R_peaks)-1): #Excluding 1st and final waveform result
            minimum=inf
            LB=R_peaks[i]-40
            #UB=R_peaks[i]+20
            
            while(LB<R_peaks[i]):
                if(orig_arr[LB]<minimum):
                    minimum=orig_arr[LB]
                    minINDEX=LB
                LB=LB+1
            Q_peaks.append(minINDEX)  
            
        return Q_peaks
    
    def S_peaks_calc(self,orig_arr,S_peaks):
        
        for i in range(1,len(R_peaks)-1): #Excluding 1st and final waveform result
            mini=inf
            UB=R_peaks[i]+40   
            while(R_peaks[i]<UB):
                if(orig_arr[R_peaks[i]]<mini): 
                    mini=orig_arr[R_peaks[i]]
                    mIX=R_peaks[i]
                R_peaks[i]=R_peaks[i]+1
            S_peaks.append(mIX)   
        
        return S_peaks   

    def calcQRS(self,Q_peaks,S_peaks,TQRS): #Function to calculate TQRS
        sampling_fqcy=1
        x1=2.5
        for i in range(0,len(Q_peaks)):
            TQRS.append(2*((S_peaks[i]+x1) - (Q_peaks[i]-x1))/sampling_fqcy)
    
        #TQRS=sum(TQRS)/len(TQRS)
        return TQRS 
       

if __name__=="__main__":           #Our main function
    x.plot() #PLotting the dataset's column on graph
    
    #Converting dataframes to array
    orig_arr=np.array(x)    # our original array
    derivative_arr=np.zeros(len(orig_arr))    #derivative array
    for i in range(0,len(orig_arr)-1):
        derivative_arr[i]=orig_arr[i+1]-orig_arr[i]
    
    #Now plotting the derivative array,but first converting array to series
    s1=pd.Series(derivative_arr) 
    
    plt.plot(s1)#Plotting the derivative array
    
    #To find the maximum of the peaks value generated in our graph
    max=np.max(derivative_arr)
    
    #Fixing a threshold value on the basis of maximum peak generated in a peak
    threshold=max*(0.65)
    
    #Now we'll find peaks in th graph
    peaks=[]
    obj = ECG() #Creating instance of class ECG
    peaks=obj.peakfinder(derivative_arr,peaks)


    '''
    *************************************************************************
    FIRST OF ALL WE WILL FIND RPEAKS,CORRESPONDING DERIVATIVE CURVE PEAKS
    *************************************************************************
    '''
    R_peaks=[]
    obj1 = ECG()    
    
    R_peaks = obj1.peaks_deriv_to_orig(derivative_arr,peaks)



    '''
    AS WE HAVE CALCULATED,THE PEAKS(R_peaks),NOW WE WILL BE
    CALCULATING HEARTBEATS WITH RPEAKS i.e with our Original set of values,BY
    CALLING A SUITABLE FUNCTION
    '''
    heartbeat=[]
    obj2 = ECG()
    heartbeat = obj2.heartbeat_calc(R_peaks,heartbeat)
        
            
    plt.plot(heartbeat)
    
    try:
        average_heartbeat=sum(heartbeat)/len(heartbeat) 
    except ZeroDivisionError:
        average_heartbeat = 0
    print()
    print("Average heartbeat {}".format(np.ceil(average_heartbeat))) #around 96.0 again




    '''
    Calculating QRS Complex for original array
    So far we have calcualated RPeaks,now we'll find S_Peaks and Q_Peaks
    '''
    #First finding Q_peaks
    Q_peaks=[]
    obj3=ECG()
    Q_peaks = obj3.Q_peaks_calc(orig_arr,Q_peaks)
  
                                 
    #Now finding the S_peaks
    S_peaks=[]
    obj4=ECG()
    S_peaks = obj4.S_peaks_calc(orig_arr,S_peaks)
 

    '''   
    NOW WE'LL CALCULATE TQRS VALUES WITH THE HELP OF S_peaks AND Q_peaks
    '''
    TQRS=[]
    obj6 = ECG()
    print("Average QRS {}".format(np.mean(obj6.calcQRS(Q_peaks,S_peaks,TQRS))))
    
    print("Min QRS: {} ".format(np.min(TQRS)))
    
    print("Max QRS: {} ".format(np.max(TQRS)))

    #print("Average QRS: {} ".format(np.mean(TQRS)))



        





























































    
    
    
    
    

    
    






    
    
    
