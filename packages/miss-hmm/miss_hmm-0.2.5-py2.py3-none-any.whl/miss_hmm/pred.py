# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 16:41:20 2022

@author: lidon
"""

# state classification algorithm (i.e. MAP, MMAP) are implemented in this file
import numpy as np
#from ZMARGibbs import*
from .HMM import*
from .learn import*
#from SeqSampling import*

# viterbi decoding

# Return the MAP estimate of state trajectory of Hidden Markov Model.
# Parameters
# ----------
# y : array (T,)
#     Observation state sequence. int dtype.
# A : array (K, K)
#     State transition matrix. See HiddenMarkovModel.state_transition  for
#     details.
# B : array (K, M)
#     Emission matrix. See HiddenMarkovModel.emission for details.
# Pi: optional, (K,)
#     Initial state probabilities: Pi[i] is the probability x[0] == i. If
#     None, uniform initial distribution is assumed (Pi[:] == 1/K).
# Returns
# -------
# x : array (T,)
#     Maximum a posteriori probability estimate of hidden state trajectory,
#     conditioned on observation sequence y under the model parameters A, B,
#     Pi.
# T1: array (K, T)
#     the probability of the most likely path so far
# T2: array (K, T)
#     the x_j-1 of the most likely path so far
def viterbi(y, A, B, Pi,hidden_state,obs_state):
    
    # Cardinality of the state space
    K = A.shape[0]
    # Initialize the priors with default (uniform dist) if not given by caller
    Pi = Pi if Pi is not None else np.full(K, 1 / K)
    T = len(y)
    indexer=np.where(y!='None')[0]
    T1 = np.empty((K, T), 'd')
    T2 = np.empty((K, T), 'B')

    # Initilaize the tracking tables from first observation
    
    if y[0]!='None':
        T1[:, 0] = Pi * B[:, np.where(obs_state==y[0])[0][0]]
        T2[:, 0] = 0
    if y[0]=='None':
        T1[:, 0] = Pi
        T2[:, 0] = 0
    
    # Iterate throught the observations updating the tracking tables
    for i in range(1, T):
        if i in indexer:
            T1[:, i] = np.max(T1[:, i - 1] * A.T * B[np.newaxis, :, np.where(obs_state==y[i])[0][0]].T, 1)
            T2[:, i] = np.argmax(T1[:, i - 1] * A.T, 1)
        else:
            T1[:, i] = np.max(T1[:, i - 1] * A.T,1)
            T2[:, i] = np.argmax(T1[:, i - 1] * A.T, 1)

    # Build the output, optimal model trajectory
    x = np.empty(T,'B')
    x[-1] = np.argmax(T1[:, T - 1])
    for i in reversed(range(1, T)):
        x[i - 1] = T2[x[i], i]
    
    
    x=np.array([hidden_state[i] for i in x])
    
    return x

# pointwise MAP implementation
# inside API, should not be exposed to users
def PMAP(obs,A,B,pi,hidden_state,obs_state):
    alph,bet=us_alpha_and_beta(obs,A,B,pi,hidden_state,obs_state)
    
    # compute p(z_t|y_o)
    cond_prob=[alph[t,:]*bet[t,:]/np.sum(alph[t,:]*bet[t,:]) for t in range(0,len(obs))]
    cond_prob=np.array(cond_prob)
    # find the index of the PMAP estimate of z
    out=[]
    for i in range(0,len(obs)):
        out.append(hidden_state[np.argmax(cond_prob[i,:])])
    out=np.array(out)
    return out

# random guess
# inside api, should not be exposed to users
def random_guesser(data,hidden_state,pi,A,B):
    n=data.shape[0]
    t=data.shape[1]
    guess=[]
    for i in range(0,n):
        #new_guess=np.random.choice(hidden_state,t)
        new_guess=np.array(
            [np.random.choice(hidden_state,1,p=np.dot(pi,np.linalg.matrix_power(A,k)))[0] for k in range(0,t)])
        guess.append(new_guess)
    
    guess=np.array(guess)
    
    return guess

# predict according to incomplete observations
# use viterbi in default
# can choose from: marginalized (obtai marginalized MAP) or random (random guess)
def predict(data,A,B,pi,hidden_state,obs_state,method='Viterbi'):
    n=data.shape[0]
    z=[]
    if method=='marginalized':
        for i in range(0,n):
            new_z=PMAP(data[i],A,B,pi,hidden_state,obs_state)
            z.append(new_z)
    elif method=='Viterbi':
        for i in range(0,n):
            new_z=viterbi(data[i],A,B,pi,hidden_state,obs_state)
            z.append(new_z)
    elif method=='random':
        for i in range(0,n):
            new_z=[np.random.choice(hidden_state,1,p=np.dot(pi,np.linalg.matrix_power(A,k)))[0] for k in range(0,len(data[0]))]
            z.append(new_z)
    z=np.array(z)
    return z