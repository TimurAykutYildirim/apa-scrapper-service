#!/usr/bin/env python
# -*- coding: ISO-8859-1 -*-

import  urllib, json, datetime, math, time, sqlite3, io, os

key = "5359f98af2e4d8f738170b82b8eeaece"
myDict=[]
query = ""
page = "1"
totalNewsAmount = 0
von = "1199142000"
bis = "1388530800"

serviceURL="http://78.46.106.130:83/get_init_db_table_data2"

requestCounter = 2000 # APA'nın api'sinden kaç tane istek hakkımız olduğunu takip edecek


#---------
APIID = key
SERVICE_URL = serviceURL
API_URL= u"http://www.ots.at/api/liste?app=$apiid&query=%28$queryKey%29&inhalt=alle&von=$von&bis=$bis&anz=500&format=json&page=$pagenum"
API_URL = API_URL.replace('$apiid', APIID)
File_Mode = "w"
#---------


#time.sleep(50)

#json gönderiyor
def getDecodedKeys(SERVICE_URL):
    url = urllib.urlopen(SERVICE_URL)
    data = url.read()
    url.close()
    decoded_data = json.loads(data)
    return decoded_data

def timetoEpoch(date):
    epoch = datetime.datetime.strptime(str(date), "%d/%m/%Y")
    epoch = str(int(time.mktime(epoch.timetuple()) * 1000))[:10]
    return epoch

def createTextFile(value, filename, FileMode):
    filename = os.path.abspath('')+'/'+filename
    if os.path.exists(filename):
        FileMode = "a+"
    text_file = io.open(filename, FileMode, encoding="utf-8")
    text_file.write(value+'\n')
    text_file.close()

def getAPIResult(API_URL, queryKey, von, bis, pagenum):
    #URL Encode
    queryKey = u''+queryKey+'' # AstraZeneca vs bu
    queryKey = urllib.quote(queryKey.encode('utf8'))
    print queryKey
    API_URL = API_URL.replace('$von', timetoEpoch(von)).replace('$queryKey', queryKey).replace('$bis', timetoEpoch(bis)).replace('$pagenum', pagenum)
    fileName = "from_"+str(von).replace("/", "_")+"_to_"+str(bis).replace("/", "_")+"_URL.txt"


    createTextFile(API_URL, str(fileName).replace('URL.txt','list_OF_request_URLs.txt'), File_Mode)
    for item in getDecodedKeys(API_URL)['ergebnisse']:
        #Create URL List Solr
        createTextFile(item['WEBLINK'], str(fileName), File_Mode)
        #time.sleep(20)

    return API_URL

def runJobs(von, bis):
    fileName = "from_"+str(von).replace("/", "_")+"_to_"+str(bis).replace("/", "_")+"_manufacture.txt"
    for item in getDecodedKeys(SERVICE_URL)['result']:
        #Create Manufacture List
        createTextFile(item['title'].replace(' ', '+'), str(fileName), File_Mode)
        #Create API URL List
        createTextFile(getAPIResult(API_URL, item['title'].replace(' ', '+'), von, bis, '1'), str(fileName).replace('manufacture','APIURL'), File_Mode)

if __name__ == "__main__":
    try:
        von = raw_input("From Date (d/m/Y) :")
        datetime.datetime.strptime(str(von), "%d/%m/%Y")
    except:
        von = raw_input("Wrong Format Try Again From Date (d/m/Y) :")

    try:
        bis = raw_input("To Date (d/m/Y) :")
        datetime.datetime.strptime(str(bis), "%d/%m/%Y")
    except:
        bis = raw_input("Wrong Format Try Again To Date (d/m/Y) :")
    runJobs(von, bis)