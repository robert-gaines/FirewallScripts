#!/usr/bin/env python3

_AUTH_ = 'RWG' # 02102022

try:
    from cmath import sin
    from turtle import back
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    import xlsxwriter
    import requests
    import shutil
    import time
    import sys
    import os
except Exception as e:
    print("[!] Library import error: %s " % e)

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

def GenFileName(hostname):
    #
    file_name = hostname+"_Sessions_"
    #
    timestamp = time.ctime()
    #
    replace_colons = timestamp.replace(":",'_')
    #
    final_timestamp = replace_colons.replace(" ","_")
    #
    final_timestamp += ".txt"
    #
    file_name += final_timestamp
    #
    return file_name

def CollectHostname(addr,port,key):
    #
    try:
        #
        print("[~] Collecting the appliance's hostname...")
        #
        device_url = "https://"+addr+":{0}/api/v2/cmdb/system/global?access_token={1}".format(port,key)
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
            print("[*] Device claims to be: %s " % appliance_hostname)
            #
            return appliance_hostname
            #
        else:
            #
            print("[!] Device refused to identify itself ")
            #
            return "Unidentified_Firewall"
            #
    except Exception as e:
        #
        print("[!] Failed to contact the appliance ")
        #
        sys.exit()

def CollectSessionTable(addr,port,key,hostname):
    #
    try:
        #
        print("[~] Collecting the appliance's session table...")
        #
        device_url = "https://"+addr+":{0}/api/v2/monitor/firewall/session?count=1000&access_token={1}".format(port,key)
        #
        headers = {'Authorization': 'Bearer {}'.format(key)}
        #
        response = requests.get(device_url, headers=headers, timeout=3, verify=False)
        #
        if(response.status_code == 200):
            #
            fileName = GenFileName(hostname)
            #
            fileObject = open(fileName,'w')
            #
            fileObject.write(response.text)
            #
            print("[*] Session table can be located at: %s " % os.path.abspath(fileName))
            #
            fileObject.close()
            #
    except Exception as e:
        #
        print("[!] Communication error: %s " % e)

def main():
    #
    print("[*] Fortigate Session Table Collection Script ")
    #
    print("---------------------------------------------")
    #
    addr = input("[+] Enter the appliance's IP address-> ")
    #
    key =  input("[+] Enter the API key-> ")
    #
    port = input("[+] Enter the administrative interface port number-> ")
    #
    hostname = CollectHostname(addr,port,key)
    #
    sessions = CollectSessionTable(addr,port,key,hostname)

if(__name__ == '__main__'):
    #
    main()
