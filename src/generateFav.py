#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import cx_Oracle
import yaml

def load():
    
    cnxn = cx_Oracle.connect('console20/console20@xe')
    crsr = cnxn.cursor()
    
    try:
        #just offering, not including episode
        crsr.execute("select mac, off_id from t_cs_favorite where off_id is not null")
        #print crsr.description
        
        macList = []
        i = 0
        
        for row in crsr:
            mac = row[0]
            
            offeringid = row[1]
            rateValue = 1                                            
            
            strList = [mac, "::", offeringid, "::", str(rateValue), "\n"]
            rateStr = "".join(strList)                        
            macList.append(rateStr)
        
        if len(macList) != 0:
            f = open("favRate.dat", "a")
            f.writelines(macList)
            f.close()
        
        print len(macList)
    finally:
        crsr.close()
        cnxn.close()
        
load()