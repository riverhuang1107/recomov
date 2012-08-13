#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
"""

"""

import yaml
import numpy, scipy.sparse
from sparsesvd import sparsesvd

def generateVector():
    
    offStream = file('titleInfo.yaml', 'r')
    titleMap = yaml.load(offStream)
    titleidList = titleMap.keys()
    
    offStream = file('movieRate.yaml', 'r')
    rateMap = yaml.load(offStream)
    
    offStream = file('doubanAuthor.yaml', 'r')
    authorList = yaml.load(offStream)
    
    vMap = {}
    
    rateList = []
    
    #len:28
    print len(rateMap)
    
    #len:34
    print len(titleidList)
        
    for offeringid in titleidList:
                
        tMap = titleMap[offeringid]
        titleid = tMap["doubanid"]            
        
        rList = []
        
        for dAuthor in authorList:
            
            try:
                
                #map may be not existed, bcs 28<34
                drList = rateMap[titleid]
                    
                flag = 0
                
                for dRate in drList:
                                        
                    dbrate = dRate["rate"]
                    
                    if dRate["authorid"] == dAuthor:
                        
                        rList.append(int(dbrate))
                        
                        flag = 1
                        
                        break
                
                if flag == 0:
                    
                    rList.append(0)
            except:
                
                rList.append(0)
                
                
        print offeringid    
        
        vMap[offeringid] = rList
        
        rateList.append(rList)
    
    mat = scipy.array(rateList)   
    smat = scipy.sparse.csc_matrix(mat) 
    ut, s, vt = sparsesvd(smat, 10)
    
    print s
    
    titleStream = file('titleRateVector.yaml', 'w')
    yaml.dump(vMap, titleStream, default_flow_style=False)
        
generateVector()
        
        
        
        