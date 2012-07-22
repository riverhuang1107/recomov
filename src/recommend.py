#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
"""

"""

from recsys.algorithm.factorize import SVD

def loadSVD():
    
    filename = 'doubanRate.dat'
    svd = SVD()
    svd.load_data(filename=filename, sep='::', format={'col':0, 'row':1, 'value':2, 'ids': int})
    
    svd.save_data("svd.dat", False)
    
    K=20
    svd.compute(k=K, min_values=1, pre_normalize="rows", mean_center=False, post_normalize=True, savefile='.')
    
    
    #svd.recommend(USERID, n=10, only_unknowns=True, is_row=False)
    
    sparse_matrix = svd.get_matrix()
    
    sim_matrix = svd.get_matrix_similarity()
    
    
    
    print sparse_matrix
    
    print sim_matrix
    
    #1173893,1396943
    sim = svd.similar(1396943, 10)
    simi = svd.similarity(1396943, 1429174)
    print sim
    print simi
    print "ok"
    
loadSVD()