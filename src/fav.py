#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import cx_Oracle
import yaml
from sys import argv

def dumpMac():
    
    cnxn = cx_Oracle.connect('console20/console20@xe')
    crsr = cnxn.cursor()
    
    try:
        #just offering, not including episode
        crsr.execute("select distinct mac from t_cs_favorite where off_id is not null")
        #print crsr.description
        
        macList = []
        i = 0
        
        for row in crsr:
            mac = row[0]
            macList.append(mac)
            
            print macList[i]
            
            i = i + 1
        
        macStream = file('favMac.yaml', 'w')
        yaml.dump(macList, macStream, default_flow_style=False)
        
        print len(macList)
    finally:
        crsr.close()
        cnxn.close()

def dumpOffering():
    
    cnxn = cx_Oracle.connect('console20/console20@xe')
    crsr = cnxn.cursor()
    
    try:
        crsr.execute("select distinct off_id from t_cs_favorite where off_id is not null")
        #print crsr.description
        
        offList = []
        i = 0
        
        for row in crsr:
            off = row[0]
            offList.append(off)
            
            print offList[i]
            
            i = i + 1
        
        offStream = file('favOffering.yaml', 'w')
        yaml.dump(offList, offStream, default_flow_style=False)
        
        print len(offList)
    finally:
        crsr.close()
        cnxn.close()
        
def dumpFavByMac():
    
    macStream = file('favMac.yaml', 'r')
    macList = yaml.load(macStream)
    
    cnxn = cx_Oracle.connect('console20/console20@xe')
    crsr = cnxn.cursor()
    
    try:
        macMap = {}
        
        for mac in macList:
            
            offList = []
            crsr.execute("select off_id from t_cs_favorite where mac='%s' and off_id is not null" % (mac))
                
            for row in crsr:
                off = row[0]
                offList.append(off)
                
            print offList
            
            macMap[mac] = offList
        
        favStream = file('favByMac.yaml', 'w')
        yaml.dump(macMap, favStream, default_flow_style=False)
            
    finally:
        crsr.close()
        cnxn.close()
        
def dumpFavByOff():
    
    offStream = file('favOffering.yaml', 'r')
    offList = yaml.load(offStream)
    
    cnxn = cx_Oracle.connect('console20/console20@xe')
    crsr = cnxn.cursor()
    
    try:
        offMap = {}
        
        for off in offList:
            
            macList = []
            crsr.execute("select mac from t_cs_favorite where off_id='%s' and off_id is not null" % (off))
                
            for row in crsr:
                mac = row[0]
                macList.append(mac)
                
            print macList
            
            offMap[off] = macList
        
        favStream = file('favByOff.yaml', 'w')
        yaml.dump(offMap, favStream, default_flow_style=False)
            
    finally:
        crsr.close()
        cnxn.close()
        
def loadFav():

    favStream = file('favByOff.yaml', 'r')
    favMap = yaml.load(favStream)
    
    print favMap
        
script, arg = argv

if arg == "loadFav":    
    loadFav()
elif arg == "dumpMac":
    dumpMac()
elif arg == "dumpOffering":
    dumpOffering()
elif arg == "dumpFavByMac":
    dumpFavByMac()
elif arg == "dumpFavByOff":
    dumpFavByOff()
else:
    print "please type arg!!"