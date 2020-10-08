#!/usr/bin/env python3.6
import requests
from akamai.edgegrid import EdgeGridAuth, EdgeRc
from urllib.parse import urljoin
import json
import re
import sys
import os
from datetime import datetime,timedelta
from time import strftime
import time
from urllib.parse import urlencode
import texttable as tt
import pandas
from pandas import ExcelWriter
import requests
import http.client
import urllib3
from urllib.parse import urlparse, parse_qs,urljoin
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

http.client._MAXHEADERS = 1000
pandas.options.display.float_format = "{:,.2f}".format


edgerc = EdgeRc('/Users/apadmana/.edgerc')
section = 'default'
baseurl = 'https://%s' % edgerc.get(section, 'host')
s = requests.Session()
s.auth = EdgeGridAuth.from_edgerc(edgerc, section)


headers = {'Content-Type': 'application/json'}

def getStartDay(interval):
    start_day = 0
    if interval == 1:
        start_day = 29
    elif interval == 2:
        start_day = 59
    elif interval == 3:
        start_day = 89

    return start_day

cp_code_list = []

def getAllCPCodes(accountSwitchKey):
    params =    {
                    'accountSwitchKey': accountSwitchKey
                }
    path = "/cprg/v1/cpcodes"
    fullurl = urljoin(baseurl, path)
    result = s.get(fullurl, params=params)
    body = result.json()
    #print("Length:",len(body['cpcodes']))
    for i in body['cpcodes']:
        cp_code_list.append(i['cpcodeId'])

def checkTrafficinCPCodes(writer,accountSwitchKey,interval):
    #get property details
    traffic_cp_code_list = []
    low_traffic_cp_code_list = []
    for cp_code in cp_code_list:
        traffic_cp_code = {}
        low_traffic_cp_code = {}
        data = {}
        data['objectIds'] = cp_code
        data['metrics'] = ['edgeHitsTotal','originHitsTotal']

        json_data = json.dumps(data)

        end = datetime.today().strftime('%Y-%m-%d')
        start = (datetime.today()-timedelta(days=getStartDay(interval))).strftime('%Y-%m-%d')

        params =    {
                        'accountSwitchKey': accountSwitchKey,
                        'start':start,
                        'end':end,
                        'interval':'HOUR'
                    }

        path = "/reporting-api/v1/reports/hits-by-time/versions/1/report-data"
        fullurl = urljoin(baseurl, path)
        result = s.post(fullurl, headers=headers, data = json_data, params=params)
        code = result.status_code
        body = result.json()

        if code == 200:
            traffic_cp_code['CP_Code'] = cp_code
            traffic_cp_code['edgeHitsTotal'] = int(body['summaryStatistics']['edgeHitsTotal']['value'])
            traffic_cp_code['originHitsTotal'] = int(body['summaryStatistics']['originHitsTotal']['value'])
            #print(traffic_cp_code)

            if traffic_cp_code['edgeHitsTotal'] == 0 :
                low_traffic_cp_code['CP_Code'] = cp_code
                low_traffic_cp_code['edgeHitsTotal'] = int(body['summaryStatistics']['edgeHitsTotal']['value'])
                low_traffic_cp_code['originHitsTotal'] = int(body['summaryStatistics']['originHitsTotal']['value'])
                low_traffic_cp_code_list.append(low_traffic_cp_code)

            traffic_cp_code_list.append(traffic_cp_code)
        else:
        	print ("Failed to retrieve configuration details.")
        	print ("Response Code: ",code)

    #print(traffic_cp_code_list)
    #print(low_traffic_cp_code_list)


    df=pandas.json_normalize(traffic_cp_code_list)
    #print(df)
    pandas.set_option('display.max_rows', df.shape[0]+1)
    df.to_excel(writer, sheet_name='Traffic_CpCode',index = False)


    df1=pandas.json_normalize(low_traffic_cp_code_list)
    #print(df1)
    pandas.set_option('display.max_rows', df1.shape[0]+1)
    df1.to_excel(writer, sheet_name='ZeroTraffic_CpCode',index = False)


def main():
    accountSwitchKey = input("Enter the Account Switch Key:")

    interval = 0
    while True:
        interval = input("Enter the interval you want[1/2/3]:")
        if int(interval) in range(1,3):
            break
        else:
            print("Incorrect input. Please enter the correct input")

    file_name = str(accountSwitchKey) + '.xlsx'
    print(file_name)
    print("Fetching the CP Code Traffic and Writing to file")
    print("...............................")
    writer = pandas.ExcelWriter(file_name, engine='xlsxwriter')

    #py report_generator.py www.example.com 266105 1-2RH7J9 1
    #python report_generator.py www.landal.nl 824170 F-AC-2460462 1

    getAllCPCodes(accountSwitchKey)
    checkTrafficinCPCodes(writer,accountSwitchKey,int(interval))


    writer.save()
    print("Done..")


if __name__ == '__main__':
    main()
