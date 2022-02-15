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

def GenFileName(hostname):
    #
    file_name = hostname+"_Policies_"
    #
    timestamp = time.ctime()
    #
    replace_colons = timestamp.replace(":",'_')
    #
    final_timestamp = replace_colons.replace(" ","_")
    #
    final_timestamp += ".xlsx"
    #
    file_name += final_timestamp
    #
    return file_name

def ParsePolicies(policies,hostname):
    #
    print("[~] Parsing policies....")
    #
    try:
        #
        fileName = GenFileName(hostname)
        #
        workbook = xlsxwriter.Workbook(fileName)
        #
        current_worksheet = workbook.add_worksheet('Policies')
        #
        col_header_list = []
        #
        column_headers = policies[0]
        #
        for c in column_headers.keys():
            #
            col_header_list.append(c)
            #
        limit = len(col_header_list)
        #
        chars = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        #
        current_iter = 0
        #
        alpha_iter = 0
        #
        secondary_iter = 0
        #
        col_index = 1
        #
        secondary_index = 0
        #
        while(current_iter < limit-1):
            #
            char_index = 0
            #
            if(current_iter == limit):
                #
                break
                #
            while(alpha_iter <= 25):
                #
                if(current_iter == limit):
                    #
                    break
                    #
                if(current_iter > 25):
                    #
                    write_index = chars[secondary_index]+chars[alpha_iter]+str(col_index)
                    #
                    current_worksheet.write(write_index,col_header_list[current_iter])
                    #
                if(current_iter < 25):
                    #
                    write_index = chars[char_index]+str(col_index)
                    #
                    current_worksheet.write(write_index,col_header_list[current_iter])
                    #
                current_iter += 1 ; char_index += 1 ; alpha_iter += 1
                #
            if(current_iter > 50):
                #
                secondary_index += 1
                #
            char_index = 0
            alpha_iter = 0
            #
        row_index = 2
        #
        for policy in policies:
            #
            #results = policy['results']
            #
            #policy_dict = results[0]
            #
            single_policy = []
            #
            for entry in policy.keys():
                #
                single_policy.append(policy[entry])
                #
            current_iter = 0
            #
            alpha_iter = 0
            #
            secondary_iter = 0
            #
            col_index = 1
            #
            secondary_index = 0
            #
            current_policy = str(single_policy[0])
            #
            print("[~] Processing policy: %s " % current_policy)
            #
            while(current_iter < limit-1):
                #
                char_index = 0
                #
                if(current_iter == limit):
                    #
                    break
                    #
                while(alpha_iter <= 25):
                    #
                    if(current_iter == limit):
                        #
                        break
                        #
                    if(current_iter > 25):
                        #
                        write_index = chars[secondary_index]+chars[alpha_iter]+str(row_index)
                        #
                        write_value = str(single_policy[current_iter])
                        #
                        current_worksheet.write(write_index,write_value)
                        #
                    if(current_iter < 25):
                        #
                        write_index = chars[alpha_iter]+str(row_index)
                        #
                        write_value = str(single_policy[current_iter])
                        #
                        current_worksheet.write(write_index,write_value)
                        #
                    current_iter += 1 ; char_index += 1 ; alpha_iter += 1
                    #
                if(current_iter > 50):
                    #
                    secondary_index += 1
                    #
                char_index = 0
                alpha_iter = 0
                #
            current_iter  = 0
            #
            single_policy = []
            #
            row_index += 1
            #
        file_path = os.path.abspath(fileName)
        #
        print("[*] Finished parsing policies ")
        #
        print("[~] The policy document is located at: %s " % file_path)
        #
        workbook.close()
        #
    except Exception as e:
        #
        print("[!] Policy parsing routine failed: %s " % e)

def CollectPolicies(addr,port,key):
    #
    headers = {'Authorization': 'Bearer {}'.format(key)}
    #
    policy_index = 1
    #
    device_url = "https://"+addr+":{0}/api/v2/cmdb/firewall/policy?datasource=true&access_token={1}".format(port,key)
    #
    response = requests.get(device_url, headers=headers, timeout=3, verify=False)
    #
    status_code = response.status_code
    #
    if(status_code != 200):
        #
        policies = None
        #
    else:
        #
        policies = response.json()
        #
        policies = policies['results']
        #
        return policies

def main():
    #
    print("[*] Fortigate Policy Collection Script ")
    #
    print("--------------------------------------")
    #
    addr = input("[+] Enter the appliance's IP address-> ")
    #
    key = input("[+] Enter the API key-> ")
    #
    port = input("[+] Enter the administrative interface port number-> ")
    #
    hostname = CollectHostname(addr,port,key)
    #
    policies = CollectPolicies(addr,port,key) 
    #
    if(policies != None):
        ParsePolicies(policies,hostname)
    else:
        print("[!] Failed to retrieve policies ")
        #
    time.sleep(5)
    #
    if(os.name == 'nt'):
        #
        suppress_stdout = os.system('cls')
        #
    else:
        #
        suppress_stdout = os.system('clear')

if(__name__ == '__main__'):
    #
    main()
