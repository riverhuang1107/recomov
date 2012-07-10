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
        crsr.execute("select * from T_RS_OFFERING where SRV_NAME!='%s' and srv_name!='%s'" % ("SHDJ","StartOver"))
        #print crsr.description
                
        i = 0
        
        offMap = {}
        for row in crsr:
            offering = row[0]
            title = row[1].decode('utf-8')
            offMap[offering] = title           
            
            print title
            
            i = i + 1
        
        titleStream = file('offering.yaml', 'w')
        yaml.dump(offMap, titleStream, default_flow_style=False)
        
        print len(offMap)
    finally:
        crsr.close()
        cnxn.close()


dump()
