#!/usr/bin/env python3
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import requests
import time

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def GenFileName(hostname):
    #
    file_name = hostname+"_"
    #
    timestamp = time.ctime()
    #
    replace_colons = timestamp.replace(":",'_')
    #
    final_timestamp = replace_colons.replace(" ","_")
    #
    final_timestamp += ".conf"
    #
    file_name += final_timestamp
    #
    return file_name

def BackupConfiguration(addr,key):
    #
    device_url = "https://"+addr+"/api/v2/cmdb/system/global?access_token={0}".format(key) 
    #
    headers = {'Authorization': 'Bearer {}'.format(key)}
    #
    response = requests.get(device_url, headers=headers, timeout=3, verify=False)
    #
    if(response.status_code == 200):
        #
        host_data = response.json()
        #
        appliance_hostname = host_data['results']['hostname']
        #
        conf_filename = GenFileName(appliance_hostname) ; print(conf_filename)
        #
        configuration_url = "https://{0}/api/v2/monitor/system/config/backup/?scope=global&amp;access_token={1}".format(addr,key)
        #
        configuration_request = requests.get(configuration_url, headers=headers, timeout=3, verify=False) 
        #
        if(configuration_request.status_code == 200):
            #
            config_data = configuration_request.text
            #
            configuration_file = open(conf_filename,'w')
            #
            configuration_file.write(config_data)
            #
            configuration_file.close()
            #
        else:
            return
    else:
        #
        return

BackupConfiguration("<addr>","<key>")