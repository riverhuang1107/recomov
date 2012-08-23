#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
"""

"""

import yaml
import time


def load():
    
    titleStream = file('offering.yaml', 'r')
    titleList = yaml.load(titleStream)
    
    nOfferingList = titleList.keys()
    
    #produce a list contains unfetched offering
    try:
        titleStream = file('fetchedOffering2.yaml', 'r')
        fetchedOffMap = yaml.load(titleStream)
        
        fetchedOffList = fetchedOffMap.keys()
        print len(fetchedOffList)
        
        offMap = {}
        for off in nOfferingList:
            try:
                result = fetchedOffMap[off]                
            except:
                offMap[off] = titleList[off]
                
        titleList = offMap        
        nOfferingList = titleList.keys()
        nTList = nOfferingList
    except:
        nTList = nOfferingList
            
    
    print len(nTList)
    
    start = time.time()
    print start    
        
    k = 0    
    
    list1 = []
    list2 = []    
    #populate queue with data   
    for off in nTList:
                                        
        if k % 2 == 0:
            list1.append(off)            
        else:
            list2.append(off)
        k = k + 1
        
    
    #write the console20's title relationship with douban's title and douban's id into titleInfo.yaml
    titleStream = file('off434.yaml', 'w')
    yaml.dump(list1, titleStream, default_flow_style=False)
    
    #write the fetched offering info into yaml
    titleStream = file('off4111.yaml', 'w')
    yaml.dump(list2, titleStream, default_flow_style=False)
        
    #cal the time for request
    current = time.time()
    print "Elapsed Time: %s" % (current - start)
    
    print len(titleList)        
    
    
load()