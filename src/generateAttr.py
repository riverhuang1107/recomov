#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
"""
* Dump:Import movie title into offering.yaml from console db

"""

import cx_Oracle
import yaml


#Import movie title into title.xml from console db
def dump():
        
    cnxn = cx_Oracle.connect('console20/console20@xe')
    crsr = cnxn.cursor()    
    #print "%s" % cnxn.version
    
    try:
        
        crsr.execute("select off_id,ast_genre,ast_actors,ast_director from t_rs_offering")
        #print crsr.description                                
        
        offList=[]
        for row in crsr:
            offeringid = row[0]
            genre = row[1]
            actorStr = row[2]
            directorStr = row[3]
            
            if genre and genre != "无":
                rateValue = 1
                strList = [genre, "::", offeringid, "::", str(rateValue), "\n"]
                rateStr = "".join(strList)                        
                offList.append(rateStr)
            
            dList=[]
            if directorStr and directorStr != "无":
                directorStr = directorStr.strip()
                dList = directorStr.split('，')
                #print  "hi,", len(aList)
                if len(dList) == 1:
                    dList = directorStr.split('、')
                    #print len(aList)
                    if len(dList) == 1:
                        dList = directorStr.split(',')
                        #print "hell1"
                        if len(dList) == 1:
                            #print "hell2"
                            dList = directorStr.split(' ')
                            if len(dList) == 1:                                                    
                                dList = directorStr.split('　')
                                     
                
                for director in dList:
                    if director:                        
                        rateValue = 1
                        strList = [director, "::", offeringid, "::", str(rateValue), "\n"]
                        rateStr = "".join(strList)                        
                        offList.append(rateStr)
            
            aList=[]
            if actorStr and actorStr != "无":
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
                
                for act in aList:
                    
                    if act:
                        rateValue = 1
                        strList = [act, "::", offeringid, "::", str(rateValue), "\n"]
                        rateStr = "".join(strList)                        
                        offList.append(rateStr)
                
        
        if len(offList) != 0:
            f = open("attrRate.dat", "w")
            f.writelines(offList)
            f.close()
        
        print len(offList)
    finally:
        crsr.close()
        cnxn.close()


dump()