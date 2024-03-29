#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
"""
titleInfo.yaml:key(offeringid)
"""

import yaml
import httplib
import xml.dom.minidom
import time
import Queue
import threading


queue = Queue.Queue()

titleInfoDict = {}

#the fetched offering by douban api
fetchedOff = {}
          
class ThreadUrl(threading.Thread):
    """Threaded Url Grab"""
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
    
    def run(self):
        num = 0

        num2 = 0
        
        k = 0
        
        while True:
            #grabs host from queue
            (title, offingid, host, sttime) = self.queue.get()
            
            #grabs urls of hosts and prints first 1024 bytes of page
            #url = urllib2.urlopen(host)
            #print url.read(1024)
            print "start: %s"% sttime
            while True:
                crt = time.time()
                print crt
                period = crt  - sttime
                if period == 0:
                    period = 1
                pulse = k / period
                print "pulse: %s"% pulse
                if pulse > 0.6:
                    print pulse
                    time.sleep(1)                    
                    continue
                else:
                    break
            
            try:
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
                        
                        id = entry.getElementsByTagName("id")[0].childNodes[0].data
                        idList = id.split("/")
                        idListLen = len(idList)
                        idNum = idList[idListLen-1]
                        
                        titleDict = {}
                        titleDict["doubanTitle"] = mTitle
                        titleDict["catalogTitle"] = title
                        titleDict["doubanid"] = idNum
                        
                        titleInfoDict[offingid] = titleDict
                        
                        #the status is ok if entry is existed
                        fetchedOff[offingid] = "ok"
                        
                        #show the title in console20 and title in douban
                        #print title, mTitle, idNum
                        print offingid, idNum
                    else:
                        num2 = num2 + 1
                        fetchedOff[offingid] = "notquery"
                        print "not exist:" + str(num2)                    
                else:
                    num = num + 1
                    print "conn err:" + str(num)
            except:
                
                if len(titleInfoDict) != 0: 
                    #write the console20's title relationship with douban's title and douban's id into titleInfo.yaml
                    titleStream = file('swtitleInfo.yaml', 'a')
                    yaml.dump(titleInfoDict, titleStream, default_flow_style=False)
                
                if len(fetchedOff) != 0: 
                    #write the fetched offering info into yaml
                    titleStream = file('swfetchedOffering.yaml', 'a')
                    yaml.dump(fetchedOff, titleStream, default_flow_style=False)
                
                
                
            
            k = k + 1
            
            #signals to queue job is done
            self.queue.task_done()


def load():
    
    titleStream = file('swoffering.yaml', 'r')
    titleList = yaml.load(titleStream)
    
    nOfferingList = titleList.keys()
    
    #produce a list contains unfetched offering
    try:
        titleStream = file('swfetchedOffering.yaml', 'r')
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
    
    #choose 40 movies for douban api
    
    
    num = 0

    num2 = 0
    
    k = 0        
    
    print len(nTList)
    
    start = time.time()
    print start        
    
    #spawn a pool of threads, and pass them queue instance, set 6 threads 
    for i in range(1):
        t = ThreadUrl(queue)
        t.setDaemon(True)
        t.start()
        
    #populate queue with data   
    for off in nTList:
        
        row = titleList[off]
        
        #add apikey for 40 request/sec in douban
        searchUrlList = ["http://api.douban.com/movie/subjects?q=",
                        row,
                        "&amp;start-index=1&amp;max-results=1&amp;apikey=047c58ac95bc67810d750a05c1353683"
                        ]
        sUrl = "".join(searchUrlList).encode("utf8")
        
        print sUrl
        queue.put((row, off, sUrl, start))
    
    #wait on the queue until everything has been processed     
    queue.join()
    
    #write the console20's title relationship with douban's title and douban's id into titleInfo.yaml
    titleStream = file('swtitleInfo.yaml', 'a')
    yaml.dump(titleInfoDict, titleStream, default_flow_style=False)
    
    #write the fetched offering info into yaml
    titleStream = file('swfetchedOffering.yaml', 'a+')
    yaml.dump(fetchedOff, titleStream, default_flow_style=False)
        
    #cal the time for request
    current = time.time()
    print "Elapsed Time: %s" % (current - start)
    
    print len(titleList)
    
    print len(fetchedOff.keys())
    
        
load()
    
