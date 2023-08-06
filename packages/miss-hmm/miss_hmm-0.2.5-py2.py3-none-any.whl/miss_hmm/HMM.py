# -*- coding: utf-8 -*-
"""
Created on Thu Jan 27 15:26:23 2022

@author: lidon
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Aug 13 14:57:16 2021

@author: a
"""

import numpy as np
import scipy.stats
import math

# Markov chain class
class Markov:
    # state: states of a Markov Chain
    # transition: transition matrix
    # pi: original distribution
    def __init__(self,state,transition,pi=None):
        self.state=state
        self.transition=transition
        if pi:
            self.pi=pi
        # if pi not specified, start from a uniform distribution
        else:
            self.pi=np.array([1 for i in range(0,len(state))])
            self.pi=self.pi/len(self.state)
    
    # start: the state that starts
    # length: number of the path length
    def sample(self,length):
        start=np.random.choice(self.state,1,p=self.pi)[0]
        path=[start]
        for i in range(0,length-1):
            index=np.where(self.state==start)[0][0]
            start=np.random.choice(self.state,1,p=self.transition[index,:])[0]
            path.append(start)
        path=np.array(path)
        return path

# hidden markov model class
# this class is capable of generating simulated paths with missing observations
class HMM(Markov):
    # h_state, o_state: a list of hidden state and observable state
    # trans_prob, obs_prob: transition matrix 
    # obs_prob: matrix that transform hidden state to obs state
    # pi: initial distribution
    def __init__(self,h_state,o_state,trans_prob,obs_prob,pi):
        self.h_state=h_state
        self.state=h_state
        self.o_state=o_state
        self.transition=trans_prob
        self.obs_prob=obs_prob
        self.pi=pi
            
    
    
    # sample the observable path
    def sample_obs(self,hidden_path):
        obs=[]
        for i in range(0,len(hidden_path)):
            index=np.where(self.state==hidden_path[i])[0][0]
            new_obs=np.random.choice(self.o_state,1,p=self.obs_prob[index,:])[0]
            obs.append(new_obs)
        obs=np.array(obs)
        return obs
    
    # return the index of a hidden variable in the hidden_state list
    def hidden_index(self, h_var):
        index=np.where(self.h_state==h_var)[0][0]
        return index
    
    # return the index of an observed variable in the observe state list
    def obs_index(self,o_var):
        index=np.where(self.o_state==o_var)[0][0]
        return index
    
    # generate size sequences, each of length length
    # return observation path and hidden path
    def generate_seq(self,size,length):
        hidden_data=[]
        observe_data=[]
        for i in range(0,size):
            h=self.sample(length)
            o=self.sample_obs(h)
            hidden_data.append(h)
            observe_data.append(o)
        hidden_data=np.array(hidden_data)
        observe_data=np.array(observe_data)
        return hidden_data,observe_data
    
    # generate a sequences with missing observations
    # full data is the data withour missing
    def generate_partial_seq(self,size,length,p=0.3):
        hidden_data=[]
        observe_data=[]
        for i in range(0,size):
            h=self.sample(length)
            o=self.sample_obs(h)
            hidden_data.append(h)
            observe_data.append(o)
        
        observe_data=np.array(observe_data)
        hidden_data=np.array(hidden_data)
        full_data=observe_data.copy()
        
        for i in range(0,len(observe_data)):
            for j in range(0,len(observe_data[0])):
                if np.random.binomial(1,p):
                    observe_data[i][j]=None
            # if a whole sequence is missing, delete it
            if sum(observe_data[i]==None)==len(observe_data[i]):
                observe_data[i]=observe_data[i-1]
        
        hidden_data=np.array(hidden_data)
        observe_data=np.array(observe_data)
        full_data=np.array(full_data)
        return hidden_data,full_data,observe_data
    
    # generate missing data according to missing rate p
    def generate_missing_data(self,full_data,p):
        full_data=np.array(full_data)
        data=full_data.copy()
        data=np.array(data)
        
        for i in range(0,len(data)):
            for j in range(0,len(data[i])):
                if np.random.binomial(1,p):
                    data[i][j]=None
            # if a whole sequence is missing, delete it
            if sum(data[i]==None)==len(data[i]):
                data[i]=data[i-1]
        return data


'''
# HMM construction
transition=np.array(
        [[0.6,0.2,0.1,0.05,0.05],[0.05,0.6,0.2,0.1,0.05],[0.05,0.05,0.6,0.2,0.1],[0.05,0.05,0.1,0.6,0.2],
         [0.05,0.05,0.1,0.2,0.6]]
        )           

state=np.array(['A','B','C','D','E'])
hidden_state=state
obs_state=np.array(['Blue','Red','Green','Purple','Grey'])

    
obs_prob=np.array([[0.5,0.3,0.05,0.05,0.1],[0.1,0.5,0.3,0.05,0.05],[0.05,0.1,0.5,0.3,0.05],
                   [0.05,0.05,0.1,0.5,0.3],[0.3,0.05,0.05,0.1,0.5]
        ])

pi=[0.5,0.2,0.2,0.1,0]

MC=HMM(hidden_state,obs_state,transition,obs_prob,pi)
'''



          

    