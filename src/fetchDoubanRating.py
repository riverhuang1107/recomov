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

queue = Queue.Queue()

movieRateDict = {}
          
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
            (title, id, doubanTitle, host) = self.queue.get()
            
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
                entryList = dom.getElementsByTagName("entry")
                if entryList:
                    
                    rateList = []
                    for entry in entryList:
                        
                        rating = entry.getElementsByTagName("gd:rating")
                        if rating:
                            rateValue = rating[0].getAttribute("value")
                        else:
                            rateValue = 3
                        
                        author = entry.getElementsByTagName("author")[0]
                        uri = author.getElementsByTagName("uri")[0].childNodes[0].data
                        uriList = uri.split("/")
                        uriListLen = len(uriList)
                        authorid = uriList[uriListLen-1]
                        
                        rateDict = {}
                        rateDict["authorid"] = authorid
                        rateDict["rate"] = rateValue
                        
                        rateList.append(rateDict)
                    
                    movieRateDict[id] = rateList
                    
                    #show the title in console20 and title in douban
                    print doubanTitle, rateValue, authorid
                else:
                    num2 = num2 + 1
                    print "not exist:" + str(num2)                    
            else:
                num = num + 1
                print "conn err:" + str(num)
    
            #signals to queue job is done
            self.queue.task_done()


def load():
    
    #titleStream = file('title.yaml', 'r')
    #titleList = yaml.load(titleStream)
    
    titleInfoStream = file('titleInfo.yaml', 'r')
    titleInfoDict = yaml.load(titleInfoStream)                
    
    num = 0

    num2 = 0
    
    k = 0
    
    #choose 40 movies for douban api
    #nTList = titleList[:40]
    nTList = titleInfoDict.keys()
    
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
    for i in range(1):
        t = ThreadUrl(queue)
        t.setDaemon(True)
        t.start()
        
    #populate queue with data   
    for row in nTList:
        
        print row
                
        id = row
        
        titleKey = titleInfoDict[row]
        catalogTitle = titleKey["catalogTitle"]
        doubanTitle = titleKey["doubanTitle"]
        
        #add apikey for 40 request/min in douban, by default, result contains 10 records
        searchUrlList = ["http://api.douban.com/movie/subject/",
                        id,
                        "/reviews?apikey=047c58ac95bc67810d750a05c1353683"
                        ]
        sUrl = "".join(searchUrlList).encode("utf8")
        
        print sUrl
        queue.put((catalogTitle,id,doubanTitle,sUrl))
    
    #wait on the queue until everything has been processed     
    queue.join()
    
    #write the console20's title relationship with douban's title and douban's id into titleInfo.yaml
    titleStream = file('movieRate.yaml', 'w')
    yaml.dump(movieRateDict, titleStream, default_flow_style=False)
        
    #cal the time for request
    current = time.time()
    print "Elapsed Time: %s" % (current - start)
        
    
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
    
    
        
load()
    