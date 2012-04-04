#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import cx_Oracle
import yaml
import urllib2, urllib
import httplib
import xml.dom.minidom
import Queue
import threading
import math
from sys import argv

def generateVector():
    
    offStream = file('favByOff.yaml', 'r')
    offMap = yaml.load(offStream)
    
    offStream = file('favOffering.yaml', 'r')
    offList = yaml.load(offStream)
    
    macStream = file('favMac.yaml', 'r')
    macList = yaml.load(macStream)
    
    vMap = {}
    
    for off in offList:
                
        fMacList = offMap[off]
        
        print fMacList
        
        vList = []
        
        for mac in macList:
            
            if mac in fMacList:
                vList.append(1)                            
            else:
                vList.append(0)
        
        vMap[off] = vList
        
        #print vList                
        
    cosine(vMap, offList)
    
    #favStream = file('favOffVector.yaml', 'w')
    #yaml.dump(vMap, favStream, default_flow_style=False)

#1005130,704332
def cosine(vMap, offList, off_id='704332'):
    
    recoList = vMap[off_id]
    
    num = len(recoList)
    
    for off in offList:
        
        vList = vMap[off]        
        
        productDot = 0
        sum1 = 0
        sum2 = 0
        
        for i in range(num):
            
            k = recoList[i]
            j = vList[i]
            productDot = productDot + k * j
            
            if k != 0:
                sum1 += k
            
            if j != 0:
                sum2 += j
        
        cosineAngle = productDot / (math.sqrt(sum1) * math.sqrt(sum2))
        
        if productDot != 0:
            print off, productDot, sum1, sum2, cosineAngle
            
            
            

generateVector()