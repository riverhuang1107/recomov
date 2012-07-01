#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
"""

"""

import yaml
import urllib2, urllib
import httplib
import xml.dom.minidom
import time
import Queue
import threading
from sys import argv

import Constants
import oAuth


def load():
    
    titleStream = file('movieRate.yaml', 'r')
    movieRateList = yaml.load(titleStream)
    
    authorList = []
    
    movieIdList = movieRateList.keys()
    
    for movieID in movieIdList:
        
        mRateList = movieRateList[movieID]
        
        for mRate in mRateList:
            
            mAuthorID = mRate["authorid"]
            #print mAuthorID
            
            flag = 0
            for author in authorList:
                
                if author == mAuthorID:
                    flag = 1
                    
                    print mAuthorID
                    
                    break
            
            if flag == 0:
                
                authorList.append(mAuthorID)
    
        
        titleStream = file('doubanAuthor.yaml', 'w')
        yaml.dump(authorList, titleStream, default_flow_style=False)        
        #print movieID
        

load()