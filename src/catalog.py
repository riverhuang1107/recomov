#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import cx_Oracle
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

queue = Queue.Queue()
          
class ThreadUrl(threading.Thread):
    """Threaded Url Grab"""
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
    
    def run(self):
        num = 0

        num2 = 0
        
        while True:
            #grabs host from queue
            (title, host) = self.queue.get()
            
            #grabs urls of hosts and prints first 1024 bytes of page
            #url = urllib2.urlopen(host)
            #print url.read(1024)
            
            conn = httplib.HTTPConnection("api.douban.com")
            conn.request("GET",host)
            res = conn.getresponse()
            if res.status == 200:
                xmlStr = res.read()
                
                dom = xml.dom.minidom.parseString(xmlStr)        
                #print dom
                entry = dom.getElementsByTagName("entry")
                if entry:
                    entry = dom.getElementsByTagName("entry")[0]
                    mTitle = entry.getElementsByTagName("title")[0].childNodes[0].data
                    
                    #show the title in console20 and title in douban
                    print title, mTitle                    
                else:
                    num2 = num2 + 1
                    print "not exist:" + str(num2)                    
            else:
                num = num + 1
                print "conn err:" + str(num)
    
            #signals to queue job is done
            self.queue.task_done()

def dump():
    
    cnxn = cx_Oracle.connect('console20/console20@xe')
    crsr = cnxn.cursor()    
    #print "%s" % cnxn.version
    
    try:
        crsr.execute("select * from T_RS_OFFERING where SRV_NAME!='%s' and srv_name!='%s'" % ("SHDJ","StartOver"))
        #print crsr.description
        
        titleList = []
        i = 0
        
        for row in crsr:
            title = row[1].decode('utf-8')
            titleList.append(title)
            
            print titleList[i]
            
            i = i + 1
        
        titleStream = file('title.yaml', 'w')
        yaml.dump(titleList, titleStream, default_flow_style=False)
        
        print len(titleList)
    finally:
        crsr.close()
        cnxn.close()

def load():
    
    titleStream = file('title.yaml', 'r')
    titleList = yaml.load(titleStream)
    
    num = 0

    num2 = 0
    
    k = 0
    
    #choose 40 movies for douban api
    nTList = titleList[:40]
    
    print len(nTList)
    
    start = time.time()
    print start
    
    #for row in nTList:
    #    #print row
    #    code = fetchMovie(row)
    #    
    #    if code == 1:
    #        num2 = num2 + 1
    #        print "not exist:" + str(num2)
    #    elif code == 2:
    #        num = num + 1
    #        print "conn err:" + str(num)
    #        
    #    print k
    #    
    #    k += 1
    #    
    #    current = time.time()
    #    print "Elapsed Time: %s" % (current - start)
    
    #spawn a pool of threads, and pass them queue instance, set 6 threads 
    for i in range(6):
        t = ThreadUrl(queue)
        t.setDaemon(True)
        t.start()
        
    #populate queue with data   
    for row in nTList:
        
        #add apikey for 40 request/sec in douban
        searchUrlList = ["http://api.douban.com/movie/subjects?q=",
                        row,
                        "&amp;start-index=1&amp;max-results=1&amp;apikey=047c58ac95bc67810d750a05c1353683"
                        ]
        sUrl = "".join(searchUrlList).encode("utf8")
        
        print sUrl
        queue.put((row,sUrl))
    
    #wait on the queue until everything has been processed     
    queue.join()
    
    #cal the time for request
    current = time.time()
    print "Elapsed Time: %s" % (current - start)
    
    print len(titleList)
    
def fetchMovie(title):
    
    searchUrlList = ["http://api.douban.com/movie/subjects?q=",
                     title,
                     "&amp;start-index=1&amp;max-results=1&amp;apikey=047c58ac95bc67810d750a05c1353683"
                     ]
    sUrl = "".join(searchUrlList).encode("utf8")
    
    print sUrl
    
    #sUrl = urllib.urlencode(sUrl)    
    
    conn = httplib.HTTPConnection("api.douban.com")
    conn.request("GET",sUrl, headers = {"User-Agent": "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.1) Gecko/20090624 Firefox/3.5"})
    res = conn.getresponse()
    if res.status == 200:
        xmlStr = res.read()
        
        dom = xml.dom.minidom.parseString(xmlStr)        
        #print dom
        entry = dom.getElementsByTagName("entry")
        if entry:
            entry = dom.getElementsByTagName("entry")[0]
            mTitle = entry.getElementsByTagName("title")[0].childNodes[0].data
            print title, mTitle
            return 0
        else:
            return 1
            
    else:
        print res.status, res.reason
        return 2
        
    #result = urllib2.Request(sUrl)
    #f = urllib2.urlopen(sUrl)
    #print f
    
    
        
script, arg = argv



if arg == "load":    
    load()
elif arg == "dump":
    dump()
elif arg == "fetch":
    fetchMovie()
else:
    print "please type arg!!"
    