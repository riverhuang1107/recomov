#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import cx_Oracle
import yaml

def dumpActor():
    
    cnxn = cx_Oracle.connect('console20/console20@xe')
    crsr = cnxn.cursor()
    
    try:
        #just offering, not including episode
        crsr.execute("select ast_actors,off_id from t_rs_offering where ast_actors is not null and ast_actors!='无'")
        #print crsr.description
        
        actorList = []
        i = 0
        k = 0
        
        for row in crsr:
            actorStr = row[0]
            offid = row[1]
            actorStr = actorStr.strip()
            aList = actorStr.split('，')
            #print  "hi,", len(aList)
            if len(aList) == 1:
                aList = actorStr.split('、')
                #print len(aList)
                if len(aList) == 1:
                    aList = actorStr.split(',')
                    #print "hell1"
                    if len(aList) == 1:
                        #print "hell2"
                        aList = actorStr.split(' ')
                        if len(aList) == 1:                                                    
                            aList = actorStr.split('　')
                            if len(aList) == 1:
                                print "hell", actorStr, offid
                                aList.append(actorStr)
            
            for actor in aList:
                
                if actor not in actorList and actor != "":
                    actorList.append(actor)
                else:
                    i = i + 1
                    #print i
                    
                k = k + 1
                
        favStream = file('actors.yaml', 'w')
        yaml.dump(actorList, favStream, default_flow_style=False)
            
        print k, i, len(actorList)
                    
    finally:
        crsr.close()
        cnxn.close()
                    
dumpActor()
                    
                        
