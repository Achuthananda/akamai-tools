import requests
import http.client
from urllib.parse import urlparse, parse_qs,urljoin
import json
import re
import sys
import urllib3
import texttable as tt

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

http.client._MAXHEADERS = 1000

class bcolors:
    PURPLE = '\x1b[95m'
    BLUE = '\x1b[94m'
    GREEN = '\x1b[92m'
    YELLOW = '\x1b[93m'
    RED = '\x1b[91m'
    ENDC = '\x1b[0m'
    WHITE = ''
    BOLD = '\x1b[1m'
    UNDERLINE = '\x1b[4m'

def get_color_string(type, string):
    end = bcolors.ENDC
    if type == bcolors.WHITE:
        end = ''
    return '%s%s%s' % (type, string, end)



def parseSessionInfo(session_values):
    session_dict = {}
    for str in session_values.split(','):
        if len(str.split(';')) == 2:
            name_value = str.split(';')
            name = name_value[0]
            value = name_value[1]
            session_dict[name.split('=')[1]] = value.split('=')[1]
            #print(name.split('=')[1],"=",value.split('=')[1])
    return session_dict



if(len(sys.argv) != 3):
    print("Incorrect arguments: Correct format is python comparitive_testing.py <URL> <ff/essl> <version_to_activate> <network:1 for production>")
    sys.exit()

url = sys.argv[1]
network = sys.argv[2]

parsed_components = urlparse(url)
hostname = parsed_components.netloc
if network == 'essl':
    staging_hostname = 'e1.a.akamaiedge-staging.net'
    production_hostname = 'e1.a.akamaiedge.net'
else:
    staging_hostname = 'a1.g.akamai-staging.net'
    production_hostname = 'a1.g.akamai.net'

path = parsed_components.path
scheme = parsed_components.scheme

params = ' '

if len(url.split('?')) == 2:
    params = dict(a.split('=') for a in url.split('?')[1].split('&'))

pragma_headers = {'Pragma':'akamai-x-get-client-ip, akamai-x-cache-on, akamai-x-cache-remote-on, akamai-x-check-cacheable, akamai-x-get-cache-key, akamai-x-get-extracted-values, akamai-x-get-nonces, akamai-x-get-ssl-client-session-id, akamai-x-get-true-cache-key, akamai-x-serial-no, akamai-x-feo-trace, akamai-x-get-request-id, x-akamai-a2-trace,x-akamai-rua-debug,x-akamai-a2-enable, x-akamai-cpi-trace, akamai-x-get-brotli-status',
                  'Host': hostname}

#Staging Test:

full_path = scheme + '://' + staging_hostname + path
staging_response = requests.get(full_path,headers=pragma_headers,params=params,verify=False)
#response = requests.head(full_path,params=params)
'''
print("---------------Staging------------------------")
print('Status:',staging_response.status_code)
for temp in staging_response.headers:
    print(temp,':',staging_response.headers[temp])
print("----------------------------------------------")
'''

#Production Test:
full_path = scheme + '://' + production_hostname + path
prod_response = requests.get(full_path,headers=pragma_headers,params=params,verify=False)
#response = requests.head(full_path,params=params)

'''
print("---------------Production------------------------")
print('Status:',prod_response.status_code)
for temp in prod_response.headers:
    print(temp,':',prod_response.headers[temp])
print("----------------------------------------------")
'''

ParentTable = tt.Texttable()
ParentTable.set_cols_width([25,55,55])
ParentTable.set_cols_align(['c','c','c'])
ParentTable.set_cols_valign(['m','m','m'])
Parentheader = ['Header','Staging','Production']
ParentTable.header(Parentheader)
Parentrow = ['Status',staging_response.status_code,prod_response.status_code]
ParentTable.add_row(Parentrow)

for temp in staging_response.headers:
    if temp in prod_response.headers:
        if temp == 'Set-Cookie':
            continue
        if temp == 'X-Akamai-Session-Info':
            staging_session_dict = parseSessionInfo(staging_response.headers[temp])
            production_session_dict = parseSessionInfo(prod_response.headers[temp])
            for key in staging_session_dict:
                if key in production_session_dict.keys():
                    if staging_session_dict[key] != production_session_dict[key]:
                        Parentrow = [key,get_color_string(bcolors.RED,staging_session_dict[key]),get_color_string(bcolors.RED,production_session_dict[key])]
                    else:
                        Parentrow = [key,staging_session_dict[key],production_session_dict[key]]
                    ParentTable.add_row(Parentrow)
        else:
            if staging_response.headers[temp] != prod_response.headers[temp]:
                #staging_response.headers[temp] = '\x1b[0;30;41m' + staging_response.headers[temp] + '\x1b[0m'
                #prod_response.headers[temp] = '\x1b[0;30;41m' + prod_response.headers[temp] + '\x1b[0m'
                #Parentrow = [temp,staging_response.headers[temp],prod_response.headers[temp]]
                Parentrow = [temp,get_color_string(bcolors.RED,staging_response.headers[temp]),get_color_string(bcolors.RED,prod_response.headers[temp])]
            else:
                Parentrow = [temp,staging_response.headers[temp],prod_response.headers[temp]]
            ParentTable.add_row(Parentrow)

'''
for temp in prod_response.headers:
    if temp not in staging_response.headers:
        empty_string = ''
        Parentrow = [temp,empty_string,get_color_string(bcolors.RED,prod_response.headers[temp])]
        ParentTable.add_row(Parentrow)
'''

MainParentTable = ParentTable.draw()
print(MainParentTable)
print('--------------------------------------------------------------------------------------------------')
print("Staging Headers for Logs:")
print('X-Cache:',staging_response.headers['X-Cache'])
print('X-Akamai-Request-ID:',staging_response.headers['X-Akamai-Request-ID'])
print('--------------------------------------------------------------------------------------------------')
print("Production Headers for Logs:")
print('X-Cache:',prod_response.headers['X-Cache'])
print('X-Akamai-Request-ID:',prod_response.headers['X-Akamai-Request-ID'])
print('--------------------------------------------------------------------------------------------------')


#Coloring Info: https://stackoverflow.com/questions/287871/how-to-print-colored-text-in-python
