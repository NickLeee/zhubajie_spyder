# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 15:56:18 2016

@author: lenovo
"""

import urllib2
from bs4 import BeautifulSoup
import re
import MySQLdb
import time
import random
import datetime
import requests

def getpage(url):
    trytimes = 0
    while trytimes <5 :
        
        try:
            user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
            headers = { 'User-Agent' : user_agent }
            request = urllib2.Request(url,headers = headers)
            response = urllib2.urlopen(request)
            content = response.read()
            soup = BeautifulSoup(content)
            trytimes = 6
        except urllib2.URLError, e:
            if hasattr(e,"code"):
                print e.code
            if hasattr(e,"reason"):
                print e.reason
            trytimes = trytimes + 1
            print('error trying %s times'%trytimes)
    return soup

def getmenulist():
    soup = getpage('http://home.zbj.com/')
    ul = soup.find('div',class_="ui-dropdown ui-dropdown-level1")
    urllist = []
    for i in ul.contents[1].find_all('a'):
        url = i.attrs['href'][:-6:]
        urllist.append(url)
    return urllist
    
def geturllist(alist):
    soup = getpage(alist+'px1s9mb1.html')
    pagenumber = int(soup.find_all('a',attrs={"href":re.compile('.*?px1s9mb1.*?')})[-2].text)
    urllist = []
    for i in range(pagenumber):
        tempurl = alist + 'px1s9mb1p'+str(i+1)+'.html'
        urllist.append([tempurl,alist[19:len(alist)-1]])
    return urllist

def writeSQL(url):
    conn = MySQLdb.Connect(host='localhost', user='root', passwd='123456', db='weike',charset='utf8')
    cur=conn.cursor()
    for item in url:
        cur.execute('insert ignore into urllist values(%s,%s)',item)
    conn.commit()
    cur.close()
    return

menulist = getmenulist()
n = 1
for i in menulist:
    print 'getting '+i
    urllist = geturllist(i)
    print 'writing sql'
    writeSQL(urllist)
    print 'remaining %d'%(len(menulist)-n)
    n = n+1
    print '----'
    print ' '
    







