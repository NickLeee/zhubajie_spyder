# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 13:01:44 2016

@author: lenovo
"""


import urllib2
from bs4 import BeautifulSoup
import re
import MySQLdb
import time
import datetime


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
    
    
def getoneurl():
    conn = MySQLdb.Connect(host='localhost', user='root', passwd='123456', db='weike',charset='utf8')
    cur=conn.cursor()
    query = 'select * from urllist limit 1;'
    cur.execute(query)
    urlinfo = cur.fetchone()
    cur.close()
    conn.close()
    return urlinfo
    
    
def getpageinfo(soup):
    category = soup.find('a',class_= 'active').text
    fwsh5 = soup.find_all('div',class_='fws-item-hd clearfix')
    items = []
    for onefws in fwsh5:
        item = ['shopid_0',
                'shopname_1',
                'shopurl_2',
                'province_3',
                'city_4',
                'servicetype_5',
                'level value_6',
                'three month money_7',
                'three month deal_8',
                'quality score_9',
                'speed score_10',
                'attitude score_11',
                'vip_12',
                category
                ]
        h5 = onefws.find('h5', class_="fws-detail-hd")
        item[0] = h5.contents[0].attrs['href'].split('/')[-1::][0]
        item[1] = h5.contents[0].attrs['title']
        item[2] = h5.contents[0].attrs['href']
        try:
            location = onefws.find('span', class_="witkey-item-province").contents[1].text.split(' ')
        except:
            location = ['None','None']
        item[3] = location[0]
        item[4] = location[1]
        service = onefws.find('p',class_='like').find_all('a')
        servicetype = []
        for i in service:
            servicetype.append(i.text)
        item[5] = ','.join(servicetype)
        try:
            item[6] = int(h5.contents[2].attrs['title'].split(u'\uff1a')[2])
        except:
            item[6] = 0
        item[7] = float(onefws.find('div', class_="threemonth-money").contents[1].text)
        item[8] = int(onefws.find('div', class_="threemonth-count").contents[1].text)
        item[9] = onefws.find('div', class_="extend-pop").find('tbody').contents[0].contents[0].text.split(u'\uff1a')[1]
        item[10] = onefws.find('div', class_="extend-pop").find('tbody').contents[1].contents[0].text.split(u'\uff1a')[1]
        item[11] = onefws.find('div', class_="extend-pop").find('tbody').contents[2].contents[0].text.split(u'\uff1a')[1]
        try:        
            item[12] = h5.find('i', class_=re.compile("ui-icosmember.*?")).attrs['title']
        except:
            item[12] = 'Not VIP'
        items.append(item)
    return items

def writeSQL(items):
    conn = MySQLdb.Connect(host='localhost', user='root', passwd='123456', db='weike',charset='utf8')
    cur=conn.cursor()
#    n = 0
    for item in items:
#        print n        
        cur.execute("insert ignore into zhubajieshop values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",item)
#        n = n+1
    conn.commit()
    cur.close()
    return   
    
def deleteurl(url):
    conn = MySQLdb.Connect(host='localhost', user='root', passwd='123456', db='weike',charset='utf8')
    cur=conn.cursor()
    delete = "delete from urllist where  url = '%s'"%(url)
    cur.execute(delete)
    conn.commit()
    print('url %s delete'%(url))

    cur.execute("select count(1) from urllist;")
    remainning = cur.fetchone()
    print('remaining %d pages to get'%(remainning[0]))
    cur.close()
    conn.close()
    return
def main():
    while True:
        print 'getting url'
        urlinfo = getoneurl()
        print 'download page %s'%urlinfo[0]
        soup = getpage(urlinfo[0])
        print 'getinfo'
        items = getpageinfo(soup)
        print 'writing to sql'
        writeSQL(items)
        print 'delete url' 
        deleteurl(urlinfo[0])
        print '----------'
        print ' '
if __name__ == '__main__':
    main()
                
    
    
    
    
    
    
    
    
    
