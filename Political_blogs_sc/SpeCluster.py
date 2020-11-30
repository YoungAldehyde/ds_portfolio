#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: Young Cho

Spectral clustering algorithm on the political blogs data

"""

import numpy as np
from matplotlib import pyplot as plt
from scipy.stats import mode
from sklearn.cluster import KMeans
import random


#open the files and assign them to variables for nodes and edges
def open_files():
    with open('nodes.txt') as f1:
        nodes = np.array([i.split() for i in f1])
    with open('edges.txt') as f2:
        edges = np.array([j.split() for j in f2]).astype('int')
    return nodes, edges

nodes, edges = open_files()

# nodes[110,2] = '0' # fix the issue with a strange entry in the raw data file
    
# build adjacency matrix
A = np.full((len(nodes), len(nodes)), fill_value = 0)
for item in edges:
    if item[0]!=item[1]:
        A[item[0]-1, item[1]-1] = 1
        A[item[1]-1, item[0]-1] = 1
    
A_bak = A.copy()    

label = np.array(nodes[:,2])
label_bak = label.copy()

degrees = np.sum(A, axis=0)
degrees_bak = degrees.copy()

'''
the degree of the node in a graph is defined as the 
total number of other nodes connected to this node.
In the hw description we suggest to remove the isolated node, i.e., the node with degree 0
In this implmementation, we test with removing node with higher degree
We can see that when remove degree >= 1, the results are better than degree =0

meanwhile, to search for best minimum mismatch rate,
we incease the total number of eign K to 30

'''
random.seed(0) # fix random seed

degree_choice = [0,1,2,3,5,10]
# degree_choice = [1,0]
best_rate = []

plt.figure()
fig, axs = plt.subplots(3,2)
fig.subplots_adjust(hspace = .8, wspace=.5)
axs = axs.ravel()

for jj in range(len(degree_choice)):
    
    A = A_bak.copy()
    label = label_bak.copy()
    degrees = degrees_bak.copy()
    
    # to answer hw Q3-2), 3)
    
    if jj ==0:
        print('when removing only the isolated nodes: ---- for Q3 (2) & (3)')
    
    min_degree = degree_choice[jj] # level for thresholding graph degree
    idx_remove = []
    for ii in range(min_degree+1):
        idx_remove = np.concatenate((np.where(degrees==ii), idx_remove), axis=None).astype(int)
        
    label = np.delete(label, idx_remove, 0)
    A = np.delete(A, idx_remove, 0)
    A = np.delete(A, idx_remove, 1)
    degrees = np.delete(degrees, idx_remove, 0)
    
    
    D = np.diag(degrees)
    
    
    # graph Laplacian
    L = D-A
    
    # svd
    u, s, _ = np.linalg.svd(L)
    u = np.flip(u, 1)
    
    # K is the total number of eigencomponent, 
    K = 31
    K_mesh = range(2,K)
    mismatch_rate_dd = [] # store the mismatch rate over choice of k
    
    m = len(label)
    for k in K_mesh:
        ut = u[:,:k]
        
        # kmeans, increase n_init to achieve less noisy result, running time will be longer
        km = KMeans(n_clusters=k, init='random', n_init=50).fit(ut) 
        
        y_pred = km.labels_
        
        mismatch = 0
        
        # # for a given cluster number k, the record for mismatch and voted label for each cluster
        mis_k =[]
        vote_k =[]
        
        for ii in np.unique(y_pred): # iterate each cluster
            idx_ii = np.where(y_pred == ii) 
            label_ii = label[idx_ii] # the label in group ii
            vote_ii = mode(label_ii).mode[0] # 'voted' label in cluster ii            
            vote_k.append(vote_ii)
            
            mismatch_ii = np.sum(label_ii != vote_ii)
            mis_k.append(np.float(mismatch_ii) / np.size(idx_ii))
            
            mismatch = mismatch + mismatch_ii
        
        mismatch_rate_dd.append(float(mismatch)/m)
        
        # to answer Q3 part (2) & (3)
        if (jj==0) & (k<=4):
            print('d='+str(jj)+' k='+str(k))
            for kk in range(k):
                print('cluster '+str(kk)+', voted label: '+str(vote_k[kk]))
                print('mismatch rate for cluster '+str(kk)+': ',round(mis_k[kk], 4))
            # print('the mismatch rate: ', round(mismatch_rate_dd[-1],4))
            print('\n')
        
    print('current degree threshold: ', degree_choice[jj])
    print('best mismatach rate: ', round(np.min(mismatch_rate_dd),4),'\n')
    best_rate.append(np.min(mismatch_rate_dd))

    # axs[jj].plot(K_mesh, mismatch_rate_dd)
    axs[jj].plot(K_mesh, np.log10(mismatch_rate_dd))
    axs[jj].set_title('d='+str(min_degree)+', best rate: '\
                      +str(round(np.min(mismatch_rate_dd),4)), fontsize = 8)
    # axs[jj].set(xlabel='K',\
    #             ylabel='mismatch rate')
    axs[jj].set_ylim([-2, 0])
    
fig.text(0.5, 0.01, 'number of clusters k', ha='center')       
fig.text(0.03, 0.5, 'log - mismatch rate : log(y)', va='center', rotation='vertical') 
fig.savefig('SPEcluster_kmeans30.pdf',dpi=300)
