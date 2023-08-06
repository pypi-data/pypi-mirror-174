# -*- coding: utf-8 -*-
"""
Created on Mon Feb 21 19:00:30 2022

@author: lidon
"""

import numpy as np
from .HMM import*
from .SeqSampling import*
import time
from multiprocessing import Pool
import scipy.stats as stats
import math
import os
import multiprocessing as mp


#!!!!!!!!!!!!!!!
# inner testing function, should not be exposed to the user
#!!!!!!!!!!!!!!!
# initialize data, transition matrix and obs_matrix
# ignore this function while inference
# just for testing
def data_initializer(transition,obs_prob,pi,hidden_state,obs_state,rate):
    #print('Data Preprocessing and Initializing Parameters...')
    #data=Sampling.data
    
    # Generate the HMM object
    MC=HMM(hidden_state,obs_state,transition,obs_prob,pi)


    # Construct Data
    hidden_data=Hidden_Generator(MC,20,5000)
    data=Obs_Generator(MC,hidden_data)

    # Missing at random
    data=Missing(data,p=rate)
    
    # Initialize transition matrix A
    
    A=np.array([[1/transition.shape[1] for i in range(0,transition.shape[1])] for j in range(0,transition.shape[0])])
    for i in range(0,A.shape[0]):
        A[i,:]=A[i,:]/sum(A[i,:])
    
    # Initialize observation matrix B and pi
    # Dirichlet parameter of B
    
    #A=np.random.dirichlet(np.ones(transition.shape[1]),transition.shape[0])
    
    #alpha_B=np.array([1 for i in range(0,obs_prob.shape[1])])
    #B=np.random.dirichlet(alpha_B,obs_prob.shape[0])
        
    B=np.array([[1/obs_prob.shape[1] for i in range(0,obs_prob.shape[1])] for j in range(0,obs_prob.shape[0])])
    for i in range(0,B.shape[0]):
        B[i,:]=B[i,:]/sum(B[i,:])
    
    
    pi=np.array([1/len(pi) for i in range(0,len(pi))])
    pi=pi/sum(pi)
    return A,B,pi,data,hidden_data

# in our algorithm, missing entries are tagged with None
# however, other dataset may not follow this standard
# miss_indicator is the indicator for missing in the data dataset
# after calling data parser, the output dataset
# will be a string array, with missing indicator substituted by None
def data_parser(data,miss_indicator):
    #data=data.astype(str)
    for i in range(0,data.shape[0]):
        for j in range(0,len(data[i])):
            if data[i][j]==str(miss_indicator):
                data[i][j]=None
    return data

# compute alpha and beta, unscaled
def us_alpha_and_beta(obs,A,B,pi,hidden_state,obs_state):
    T=len(obs)
    alpha=np.zeros((T,len(hidden_state)))
    
    # acquire the index that correspond to observations that are not missing
    indexer=np.where(obs!='None')[0]

    # Handle the boundary case: the first line of alpha
    if obs[0]!='None':
        y=np.where(obs_state==obs[0])[0][0]
        
        alpha[0,:]=pi*B[:,y]
    else:
        alpha[0,:]=pi
    
    # scaling
    #alpha[0,:]=alpha[0,:]/sum(alpha[0,:])
    
    
    for i in range(1,T):
        # The case when i is an observable data
        if i in indexer:
            #print('hurray!')
            y=np.where(obs_state==obs[i])[0][0]
            alpha[i,:]=np.dot(alpha[i-1,:],A)*B[:,y]
            #alpha[i,:]=alpha[i,:]/sum(alpha[i,:])
        else:
            alpha[i,:]=np.dot(alpha[i-1,:],A)
            #alpha[i,:]=alpha[i,:]/sum(alpha[i,:])
    
    T=len(obs)
    beta=np.zeros((T,len(hidden_state)))
    
    # acquire the index that correspond to observations that are not missing
    indexer=np.where(obs!='None')[0]
    beta[T-1,:]=[1 for i in range(0,len(hidden_state))]
    #beta[T-1,:]=beta[T-1]/sum(alpha[T-1,:])
    for i in range(T-2,-1,-1):
        if (i+1) in indexer:
            
            y=np.where(obs_state==obs[i+1])[0][0]
            #beta[i,:]=[np.sum(beta[i+1,:]*A[j,:]*B[:,y]) for j in range(0,len(hidden_state))]
            #beta[i,:]=beta[i,:]/sum(alpha[i,:])
            beta[i,:]=np.dot(beta[i+1,:]*A,B[:,y])
            #beta[i,:]=np.dot((A.T*B[:,y]).T,beta[i+1,:])
        else:
            beta[i,:]=np.dot(beta[i+1,:],A.T)
            #beta[i,:]=beta[i+1,:]*A
            #beta[i,:]=beta[i,:]/sum(alpha[i,:])
    return alpha,beta

    

# calculate alpha_t(z_t) in HMM models, scaled
def alpha_and_beta(obs,A,B,pi,hidden_state,obs_state):
    T=len(obs)
    alpha=np.zeros((T,len(hidden_state)))
    
    # acquire the index that correspond to observations that are not missing
    indexer=np.where(obs!='None')[0]

    # Handle the boundary case: the first line of alpha
    if obs[0]!='None':
        y=np.where(obs_state==obs[0])[0][0]
        
        alpha[0,:]=pi*B[:,y]
    else:
        alpha[0,:]=pi
    
    # scaling
    alpha[0,:]=alpha[0,:]/sum(alpha[0,:])
    
    
    for i in range(1,T):
        # The case when i is an observable data
        if i in indexer:
            y=np.where(obs_state==obs[i])[0][0]
            alpha[i,:]=np.dot(alpha[i-1,:],A)*B[:,y]
            alpha[i,:]=alpha[i,:]/sum(alpha[i,:])
        else:
            alpha[i,:]=np.dot(alpha[i-1,:],A)
            alpha[i,:]=alpha[i,:]/sum(alpha[i,:])
    
    T=len(obs)
    beta=np.zeros((T,len(hidden_state)))
    
    # acquire the index that correspond to observations that are not missing
    indexer=np.where(obs!='None')[0]
    beta[T-1,:]=[1 for i in range(0,len(hidden_state))]
    beta[T-1,:]=beta[T-1]/sum(alpha[T-1,:])
    for i in range(T-2,-1,-1):
        if (i+1) in indexer:
            y=np.where(obs_state==obs[i+1])[0][0]
            #beta[i,:]=[np.sum(beta[i+1,:]*A[j,:]*B[:,y]) for j in range(0,len(hidden_state))]
            beta[i,:]=np.dot((A.T*B[:,y]).T,beta[i+1,:])
            beta[i,:]=beta[i,:]/sum(alpha[i,:])
        else:
            beta[i,:]=np.dot(beta[i+1,:],A)
            beta[i,:]=beta[i,:]/sum(alpha[i,:])
    return alpha,beta

# calculate the probability that p(y_o,z_t,z_{t+1})
# z1,z2 is the respective hidden state
# t1,t2 is the position of z1 and z2, note that t2=t1+1
# alph, bet is the respective alpha and beta form of obs
# def ksi(obs,A,B,pi,z1,z2,t1,t2,hidden_state,obs_state):
#     z1_pos=np.where(hidden_state==z1)[0][0]
#     z2_pos=np.where(hidden_state==z2)[0][0]
    
#     alph,bet=us_alpha_and_beta(obs,A,B,pi,hidden_state,obs_state)
    
#     indexer=np.where(obs!='None')[0]
    
#     if t2 in indexer:
#         y=np.where(obs_state==obs[t2])[0][0]
#         return alph[t1,z1_pos]*A[z1_pos,z2_pos]*B[z2_pos,y]*bet[t2,z2_pos]
#     else:
        
#         return alph[t1,z1_pos]*A[z1_pos,z2_pos]*bet[t2,z2_pos]

# calculate (y_o,z_t,z_{t+1}) for all z_{t+1}
def ksi(obs,A,B,pi,zt,t,hidden_state,obs_state):
    zt_pos=np.where(hidden_state==zt)[0][0]
    alph,bet=us_alpha_and_beta(obs,A,B,pi,hidden_state,obs_state)
    indexer=np.where(obs!='None')[0]
    
    if t+1 in indexer:
        
        y=np.where(obs_state==obs[t+1])[0][0]
        output=alph[t,zt_pos]*A[zt_pos,:]*B[:,y]*bet[t+1]
        #output=(alph[t]*A*B[:,y])*bet[t+1]
        #output=output.T
        #output=output/np.sum(np.sum(output))
        #output=output/np.sum(output)
        #return output[zt_pos]
        return output
    else:
        
        output=alph[t,zt_pos]*A[zt_pos,:]*bet[t+1]
        #output=output/np.sum(output)
        return output

# calculate ksi of the whole sequence given z1 and z2
# def seq_ksi(obs,A,B,pi,z1,z2,hidden_state,obs_state):
#     h=hidden_state
#     o=obs_state
#     ks=sum([ksi(obs,A,B,pi,z1,z2,t,t+1,h,o) for t in range(0,len(obs)-1)])
#     return ks


# calculate ksi of the whole sequence given z1 and return a vector
def seq_ksi(obs,A,B,pi,z,hidden_state,obs_state):
    h=hidden_state
    o=obs_state
    ks=[ksi(obs,A,B,pi,z,r,h,o)[:] for r in range(0,len(obs)-1)]
    # note that ks is a vector, indicating the new reestimation of A
    return sum(ks)

# compute the probability of p(z_t|y)
# t: position of z
# z: latent sequence
def gamma(t,alph,bet,z,hidden_state):
    z_pos=np.where(hidden_state==z)[0][0]
    return alph[t,z_pos]*bet[t,z_pos]/np.dot(alph[t,:],bet[t,:])


# compute p(y_o,z_t) wrt all values of z_t
# return a vector
def ph(obs,A,B,pi,t,hidden_state,obs_state):
    alph,bet=us_alpha_and_beta(obs,A,B,pi,hidden_state,obs_state)
    #bet=beta(obs,A,B,pi,hidden_state,obs_state)
    
    return alph[t,:]*bet[t,:]
    
# a specifically designed parallel function for updating B
# compute p(y_o,z_t)*I(y_o_t==y_t), return a vector indicating each y
# j: the index of z
def ph_seq_obs(obs,A,B,pi,j,hidden_state,obs_state):
    h=hidden_state
    o=obs_state
    #out=sum([ph(obs,A,B,pi,t,h,o)*((o==obs[t]).astype(np.int32)) for t in range(0,len(obs))])
    out1=[ph(obs,A,B,pi,t,h,o)[j] for t in range(0,len(obs))]
    out1=np.array(out1)
    out2=np.array([obs==obs_state[i] for i in range(0,len(obs_state))])
    out2=out2.astype(np.int)
    out=np.dot(out1,out2.T)
    return out


# a function for updating B
# compute summation of p(y_o,z_t=z,y_t=y) for all t
# return a vector indicating the value for each y
# j: index of z
def ph_seq_mis(obs,A,B,pi,j,hidden_state,obs_state):
    indexer=np.where(obs=='None')[0]
    alph,bet=us_alpha_and_beta(obs,A,B,pi,hidden_state,obs_state)
    temp=alph[indexer,j]*bet[indexer,j]
    out=sum(temp)*B[j,:]
    
    return out
    


# evaluate p(y_o|theta)
def p_obs(obs,A,B,pi,hidden_state,obs_state):
    h=hidden_state
    o=obs_state
    alph,bet=us_alpha_and_beta(obs,A,B,pi,h,o)
    return sum(alph[len(obs)-1,:])

def step(A,B,pi,new_A,new_B,new_pi):
    length_A=np.linalg.norm(A-new_A)
    length_B=np.linalg.norm(B-new_B)
    length_pi=np.linalg.norm(pi-new_pi)
    out=max(length_A,length_B,length_pi)
    return out

# calculate the observational probability of all data
def y_prob(data,A,B,pi,hidden_state,obs_state,p):
    h=hidden_state
    o=obs_state
    prob=p.starmap(p_obs,[(data[r],A,B,pi,h,o) for r in range(0,data.shape[0]) ])
    prob=np.array(prob)
    return prob

# update A
# Notice that prob is the observational prob of all data
# returned by obs_prob
def update_A(A,B,pi,data,hidden_state,obs_state,prob,p):
    h=hidden_state
    o=obs_state
    new_A=A.copy()
    
    
    #prob=p.starmap(p_obs,[(data[r],A,B,pi,h,o) for r in range(0,data.shape[0]) ])
    #prob=np.array(prob)
    new_A=A.copy()
    for j in range(0,A.shape[0]):
        propose=p.starmap(seq_ksi,[(data[r],A,B,pi,h[j],h,o) 
                                   for r in range(0,data.shape[0])])
        propose=np.array(propose)
        propose=propose.T/prob
        propose=propose.T
        new_A[j,:]=sum(propose)
        new_A[j,:]=new_A[j,:]/np.sum(new_A[j,:])
        
      
    return new_A

def update_pi(A,B,pi,data,hidden_state,obs_state,prob,p):
    
    h=hidden_state
    o=obs_state
    # for testing pi
    new_pi=pi
    
    #Test code
    #prob=1
    
    
    pi_propose=p.starmap(ph,[(data[k],A,B,pi,0,h,o) for k in range(0,data.shape[0])])
    
    
    pi_propose=np.array(pi_propose)
    pi_propose=pi_propose.T/prob
    pi_propose=pi_propose.T
    
    new_pi=sum(pi_propose)
    
    new_pi=new_pi/sum(new_pi)
    
    return new_pi

def update_B(A,B,pi,data,hidden_state,obs_state,prob,p):
    h=hidden_state
    o=obs_state
    new_B=B.copy()
    
    #Test code
    #prob=1
    
    for j in range(0,B.shape[0]):
        propose1=p.starmap(ph_seq_obs,[(data[r],A,B,pi,j,h,o) for r in range(0,data.shape[0])])
        propose2=p.starmap(ph_seq_mis,[(data[r],A,B,pi,j,h,o) for r in range(0,data.shape[0])])
        #prob=p.starmap(p_obs,[(data[r],A,B,pi,h,o) for r in range(0,data.shape[0]) ])
        propose1=np.array(propose1)
        propose2=np.array(propose2)
        propose=propose1+propose2
        #prob=np.array(prob)
        propose=propose.T/prob
        propose=propose.T
        new_B[j,:]=sum(propose)
        # normalize
        new_B[j,:]=new_B[j,:]/np.sum(new_B[j,:])
     
    return new_B

# traning, start from arbitrary A,B and pi, don't report anything
# e is the stopping rule
# n is the number of iteration
# p: multiprocessing core
# private API, not exposed to the user
def EMTrain(A,B,pi,data,e,hidden_state,obs_state,p):
    pi=pi
    A=A
    B=B
    h=hidden_state
    o=obs_state
    size=data.shape[0]
    
    A_trace=[]
    B_trace=[]
    pi_trace=[]
    obj_func=[]
    
    prob=y_prob(data,A,B,pi,h,o,p)
    new_A=update_A(A,B,pi,data,h,o,prob,p)
    new_B=update_B(A,B,pi,data,h,o,prob,p)
    new_pi=update_pi(A,B,pi,data,h,o,prob,p)

    # test code
    #print(new_pi)
    #print(new_A)
    #print(new_B)
    
    iterator=0
    #log_prob=sum(np.log(prob))
    log_prob=sum(np.log(prob))/size
    #print('ObjectiveFunc',log_prob)
    obj_func.append(log_prob)
    A_trace.append(new_A)
    B_trace.append(new_B)
    pi_trace.append(new_pi)
    
    # Start while loop
    switcher=True
    while switcher or obj_func[len(obj_func)-1]-obj_func[len(obj_func)-2]>e:
        switcher=False
        iterator+=1
        #print('Step:',obj_func[len(obj_func)-1]-obj_func[len(obj_func)-2])
        #print('Iteration',iterator)
        pi=new_pi.copy()
        B=new_B.copy()
        A=new_A.copy()
        start=time.time()
        prob=y_prob(data,A,B,pi,h,o,p)
        new_pi=update_pi(A,B,pi,data,h,o,prob,p)
        new_A=update_A(A,B,pi,data,h,o,prob,p)
        new_B=update_B(A,B,pi,data,h,o,prob,p)
        #print(new_pi)
        #print(new_A)
        #print(new_B)
        end=time.time()
        #print('Use Time',end-start)
        #log_prob=sum(np.log(prob))
        log_prob=sum(np.log(prob))/size
        #print('ObjectiveFunc:',log_prob)
        obj_func.append(log_prob)
        A_trace.append(new_A)
        B_trace.append(new_B)
        pi_trace.append(new_pi)
        
    A_trace=np.array(A_trace)
    B_trace=np.array(B_trace)
    pi_trace=np.array(pi_trace)
    
    return A_trace,B_trace,pi_trace,obj_func


# traning, start from arbitrary A,B and pi, report every several steps
# e is the stopping rule
# n is the number of iteration
# p: multiprocessing core
# private API, not exposed to the user
# step: report the result every step steps
def EMTrain1(A,B,pi,data,e,step,hidden_state,obs_state,p):
    pi=pi
    A=A
    B=B
    h=hidden_state
    o=obs_state
    size=data.shape[0]
    
    A_trace=[]
    B_trace=[]
    pi_trace=[]
    obj_func=[]
    
    prob=y_prob(data,A,B,pi,h,o,p)
    new_A=update_A(A,B,pi,data,h,o,prob,p)
    new_B=update_B(A,B,pi,data,h,o,prob,p)
    new_pi=update_pi(A,B,pi,data,h,o,prob,p)

    # test code
    #print(new_pi)
    #print(new_A)
    #print(new_B)
    
    # initialize training log
    log=[]
    
    iterator=0
    #log_prob=sum(np.log(prob))
    log_prob=sum(np.log(prob))
    #print('ObjectiveFunc',log_prob)
    obj_func.append(log_prob)
    A_trace.append(new_A)
    B_trace.append(new_B)
    pi_trace.append(new_pi)
    
    # Start while loop
    switcher=True
    while switcher or obj_func[len(obj_func)-1]-obj_func[len(obj_func)-2]>e:
        switcher=False
        iterator+=1
        #print('Step:',obj_func[len(obj_func)-1]-obj_func[len(obj_func)-2])
        #print('Iteration',iterator)
        # report result
        
        pi=new_pi.copy()
        B=new_B.copy()
        A=new_A.copy()
        start=time.time()
        prob=y_prob(data,A,B,pi,h,o,p)
        new_pi=update_pi(A,B,pi,data,h,o,prob,p)
        new_A=update_A(A,B,pi,data,h,o,prob,p)
        new_B=update_B(A,B,pi,data,h,o,prob,p)
        #print(new_pi)
        #print(new_A)
        #print(new_B)
        end=time.time()
        #print('Use Time',end-start)
        #log_prob=sum(np.log(prob))
        log_prob=sum(np.log(prob))
        #print('ObjectiveFunc:',log_prob)
        obj_func.append(log_prob)
        A_trace.append(new_A)
        B_trace.append(new_B)
        pi_trace.append(new_pi)
        
        if iterator%step==0:
            print('-----------------')
            log.append('-----------------')
            print(f'Iteration: {iterator}')
            log.append(f'Iteration: {iterator}')
            print(f'Pi estimate: {new_pi}')
            log.append(f'Pi estimate: {new_pi}')
            print(f'Transition Estimate: {new_A}')
            log.append(f'Transition Estimate: {new_A}')
            print(f'Emission estimate: {new_B}')
            log.append(f'Emission estimate: {new_B}')
            print(f'Objective Function: {log_prob}')
            log.append(f'Objective Function: {log_prob}')
            print(f'Time per iteration: {end-start}')
            log.append(f'Time per iteration: {end-start}')
            print('-----------------')
            log.append('-----------------')
            
        
    A_trace=np.array(A_trace)
    B_trace=np.array(B_trace)
    pi_trace=np.array(pi_trace)
    
    return A_trace,B_trace,pi_trace,obj_func,log

# train parameter with data, hidden state and obs state
# core specifies the number of multiprocessing cores to use
# if core=None(don't specify the core), use all cores by default
# report every step iterations
# won't report by default (step=0)
# e: stopping threshold
# a0,b0,pi0: initial values
def train(data,hidden_state,obs_state,a0=0,b0=0,pi0=0,step=0,e=0.001,core=None):
    if not core:
        p=Pool(mp.cpu_count())
    else:
        p=Pool(core)
    
    # if not specify intial value, initialize randomly
    if type(a0)!=np.ndarray and type(b0)!=np.ndarray and type(pi0)!=np.ndarray:
        # initialize with dirichlet distribution
        # M is size of hidden space, N is size of observed space
        M=len(hidden_state)
        N=len(obs_state)
        
        # MXM
        A=np.random.dirichlet([8 for i in range(0,M)],M)
        B=np.random.dirichlet([8 for i in range(0,N)],M)
        pi=np.random.dirichlet([8 for i in range(0,M)])
    else:
        A=a0
        B=b0
        pi=pi0
    
    if step==0:
        a_trace,b_trace,pi_trace,f=EMTrain(A,B,pi,data,e,hidden_state,obs_state,p)
        return a_trace,b_trace,pi_trace,f
    else:
        a_trace,b_trace,pi_trace,f,log=EMTrain1(A,B,pi,data,e,step,hidden_state,obs_state,p)
        return a_trace,b_trace,pi_trace,f,log
    
    
    



# traning, start from arbitrary A,B and pi with fixed iteration
# e is the stopping rule
# n is the number of iterations
# p: multiprocessing core
def EMTrain2(A,B,pi,data,n,hidden_state,obs_state,p):
    pi=pi
    A=A
    B=B
    h=hidden_state
    o=obs_state
    size=data.shape[0]
    
    A_trace=[]
    B_trace=[]
    pi_trace=[]
    obj_func=[]
    
    prob=y_prob(data,A,B,pi,h,o,p)
    new_A=update_A(A,B,pi,data,h,o,prob,p)
    new_B=update_B(A,B,pi,data,h,o,prob,p)
    new_pi=update_pi(A,B,pi,data,h,o,prob,p)

    # test code
    print(new_pi)
    print(new_A)
    print(new_B)
    
    iterator=0
    #log_prob=sum(np.log(prob))
    log_prob=sum(np.log(prob))/size
    print('ObjectiveFunc',log_prob)
    obj_func.append(log_prob)
    A_trace.append(new_A)
    B_trace.append(new_B)
    pi_trace.append(new_pi)
    
    # Start while loop
    switcher=True
    k=0
    while k<n:
        switcher=False
        iterator+=1
        print('Step:',obj_func[len(obj_func)-1]-obj_func[len(obj_func)-2])
        print('Iteration',iterator)
        pi=new_pi.copy()
        B=new_B.copy()
        A=new_A.copy()
        start=time.time()
        prob=y_prob(data,A,B,pi,h,o,p)
        new_pi=update_pi(A,B,pi,data,h,o,prob,p)
        new_A=update_A(A,B,pi,data,h,o,prob,p)
        new_B=update_B(A,B,pi,data,h,o,prob,p)
        print(new_pi)
        print(new_A)
        print(new_B)
        end=time.time()
        print('Use Time',end-start)
        #log_prob=sum(np.log(prob))
        log_prob=sum(np.log(prob))/size
        print('ObjectiveFunc:',log_prob)
        obj_func.append(log_prob)
        A_trace.append(new_A)
        B_trace.append(new_B)
        pi_trace.append(new_pi)
        k+=1
        
    A_trace=np.array(A_trace)
    B_trace=np.array(B_trace)
    pi_trace=np.array(pi_trace)
    
    return A_trace,B_trace,pi_trace,obj_func

# define the output class of the experiments
class Out:
    def __init__(self,data,post_A,post_B,post_pi,latent_seq, log_prob,true_hidden):
        self.data=data
        self.post_A=post_A
        self.post_B=post_B
        self.post_pi=post_pi
        self.latent_seq=latent_seq
        self.log_prob=log_prob
        self.true_hidden=true_hidden 



