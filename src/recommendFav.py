#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
"""

"""

from recsys.algorithm.factorize import SVD
from recsys import algorithm

import yaml

algorithm.VERBOSE = True

def loadSVD():        
    
    filename = 'favRate.dat'
    svd = SVD()
    svd.load_data(filename=filename, sep='::', format={'col':0, 'row':1, 'value':2})
    
    svd.save_data("svd.dat", False)
    
    K=20
    svd.compute(k=K, min_values=1, pre_normalize="rows", mean_center=False, post_normalize=True, savefile='.')
    
    
    #svd.recommend(USERID, n=10, only_unknowns=True, is_row=False)
    
    sparse_matrix = svd.get_matrix()
    
    sim_matrix = svd.get_matrix_similarity()
    
    
    
    print sparse_matrix
    
    print sim_matrix
    
    #1173893,1396943
    sim = svd.similar(1251131, 10)
    
    filename = 'swoffering.yaml'
    titleStream = file(filename, 'r')
    titleList = yaml.load(titleStream)
    
    for row in sim:
        
        (offid, simiilar) = row
        
        print offid, titleList[str(offid)]
    
    print sim
    
    print "ok"
    
loadSVD()