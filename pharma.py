#!/usr/bin/env python
# -*- coding: utf-8 -*-

import  urllib2, json, datetime, math, time

key = "5359f98af2e4d8f738170b82b8eeaece"

query = ""

page = "1"
totalNewsAmount = 0

von = "1199142000"
bis = "1388530800"

serviceURL="http://78.46.106.130:83/get_init_db_table_data2"

requestCounter = 2000 # APA'nın api'sinden kaç tane istek hakkımız olduğunu takip edecek


myDict = ["pharma"]
# myDict = ["novartis","glivec","lucentis","tasigna","mono embolex","sandostatin lar","pfizer","lyrica","enbrel pfz","prevenar pfz","sutent","genotropin","bayer vital","xarelto","betaferon","eylea","contour next","contour sensoren","sanofi","lantus","clexane","apidra","insuman rapid","insuman comb","abbvie","humira","synagis","duodopa","kaletra","zemplar","gliead sciences","sovaldi","truvada","atripla","viread","hepsera","hexal","gingium","acc akut","metohexal succinat","fentanyl hexal mat","filgastim hexal","glaxosmithkline","viani","infanix hexa","atmadisc gsk","priorix tetra","twinrix","zentiva pharma","ibuflam lichtenstein","novaminsulfan lichtenstein","leflunomide winthrop","ramilich","glimepirid winthrop"]

def apa_ots_news_scrapper(myURL):
    try:
        response = urllib2.urlopen(myURL)

        str(response).decode('string-escape')

        data = json.loads(response.read())
        totalNewsAmount = int(data["meta"]["treffer"])

        text_file = open("apa_ots_pharma_links.txt", "a")
        for index in range(len(data['ergebnisse'])):
            if index < len(data['ergebnisse']) - 1:
                text_file.writelines(data['ergebnisse'][index]['WEBLINK'] + "\n")
                #print (data['ergebnisse'][index]['WEBLINK'])
            else:
                text_file.writelines(data['ergebnisse'][index]['WEBLINK'])
                #print (data['ergebnisse'][index]['WEBLINK'])
        text_file.close()
    except urllib2.URLError, e:
        print ("something went wrong" + e)

    return totalNewsAmount

def logger(x):
    text_file = open("pharma_logs.txt", "a")
    text_file.writelines("from: " + millisecondConverter(von) + "\n")
    text_file.writelines("to: " + millisecondConverter(bis) + "\n")
    text_file.writelines(x + "\n")
    text_file.close()

def millisecondConverter(x):
    s = datetime.datetime.fromtimestamp(int(x)).strftime("%Y-%m-%d %H:%M:%S")
    return s


def urlGenerator(pageNum):
    for item in myDict:
        if ' ' in item:
            item = item.replace(' ', '%20')
        query=item
        url = "http://www.ots.at/api/liste?app=" + key + "&query=%28" + query + "%29&inhalt=alle&von=" + von + "&bis=" + bis + "&anz=500&format=json&page=" + str(pageNum)
        #print (item+"\n")
        logger("search term: " + item + " page: " + page)
        logger(url+"\n")
        #print item + " ile yapılan istekten gelen haber sayısı: " + str(apa_ots_news_scrapper(url))
        return url



totalNewsAmount=apa_ots_news_scrapper(urlGenerator(page))
print "total news amount:" + str(totalNewsAmount)
if totalNewsAmount > 500:
    lastPageNum= math.ceil(float(totalNewsAmount)/float(500))
    print (lastPageNum)
    while int(lastPageNum) >= 2:
        text_file = open("apa_ots_pharma_links.txt", "a")
        text_file.writelines("\n")
        text_file.close()
        apa_ots_news_scrapper(urlGenerator(int(lastPageNum)))
        lastPageNum = int(lastPageNum)-1
