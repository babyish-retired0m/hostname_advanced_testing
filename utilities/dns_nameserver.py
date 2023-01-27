#!/usr/bin/env python3
__version__ = "1.4"

# 1.3
# get_nameserver()# DNS IP address NordVPN
if __name__ == '__main__':
    import file as file
    import ip_address as ip_address
    import get_asn_files_dict as asn_files_dict
else:
    import utilities.file as file
    import utilities.ip_address as ip_address
    import utilities.helper_asn as helper_asn

import os
import re

File = file.Main(print_result=False)
parent_dir = os.path.dirname(__file__) + "/ip_addresses_block_provider/"


def get_nameserver(nameservers=["1.1.1.1"], asn_id = None):
    # files_asn_list = get_files_names()
    
    # for asn_id in files_asn_id_list:
    #     ip_network_list = File.open_as_list(parent_dir + asn_id['file_name'])
    #     asn_ip_address = ip_address.check_ip_in_networks(ip_address_pub, ip_network_list)
    
    # open_asn_file_dict(file_path)
    # asn_info_dict = get_asn_info_dict()

    # for asn_id in asn_info_dict

    # asn_id_list = { :'lanet', :'vodafone', 15895:'JSC \"Kyivstar\"', :'datacamp'}



    # asn_files_dict = helper_asn.get_asn_files_dict()
    # asn_as_list = {}
    # for asn_file in asn_files_dict:
    #    asn_file_dict = File.open_json(asn_files_dict[asn_file]['asn_file_path'])
        # for (key, value) in asn_id_list_dict:
        #     asn

    

    asn_id = int(asn_id)
    if asn_id is None:
        return nameservers
    else:
        if asn_id == 39608: #'lanet'
            nameservers.append('194.50.85.5')# Lanet.ua
            # nameservers.remove('1.1.1.1')# Cloudflare
            # nameservers.remove('8.8.4.4')# Google
            # nameservers.remove('9.9.9.9')# Quad9
            # nameservers.remove('64.6.64.6')# Neustar
            # nameservers.remove('209.244.0.3')
            nameservers.append('76.76.2.0')# Control D
            nameservers.append('208.67.222.222')# OpenDNS Home
            nameservers.append('185.228.168.9')# CleanBrowsing
            nameservers.append('94.140.14.14')# AdGuard DNS
            nameservers.append('84.200.69.80')# DNS.WATCH
            nameservers.append('8.26.56.26')# Comodo Secure DNS
            nameservers.append('77.88.8.8')# Yandex DNS
            nameservers.append('205.171.3.65')# CenturyLimk (Level3)
        elif asn_id == 'vodafone':
            #nameservers.append('9.9.9.9')
            nameservers.remove('1.1.1.1')
            nameservers.remove('8.8.4.4')
            nameservers.remove('64.6.64.6')
            nameservers.remove('208.67.220.220')
            nameservers.remove('209.244.0.3')
            # nameservers.append('88.214.96.116')
            # nameservers.append('80.255.73.116')
            # nameservers.append('80.255.64.1172')
        elif asn_id == 15895:#'kyivstar'
            nameservers.append("193.41.60.1")
            #nameservers.append("81.23.24.66")
            #nameservers.append("88.214.96.116")
        # 'ukservers' - 42831
        elif asn_id == 'datacamp' or asn_id == 'm247' or asn_id == 'ukservers' or asn_id == 'cdn77':
            nameservers.append("103.86.99.99")
            nameservers.append("103.86.96.100")
        elif asn_id == 'lifecell': nameservers.append("212.58.161.173")
        elif asn_id == 'znet':
            nameservers.append("91.202.104.6")
            nameservers.append("162.158.248.73")
        elif asn_id == 'gigatrans': nameservers.append("172.253.1.129")
        elif asn_id == 'bilink': pass # Retorville WiFi Salateria
        elif asn_id == 'o3': pass # Retroville WiFi Retroville Guest, Master Burger
        elif asn_id == 'ukrtelecom': pass #IP address of the domain: 95.132.129.254 Retroille WiFi Multiplex
        elif asn_id == 'wnet': pass #IP address of the domain: 217.20.182.17 Retroville WiFi Rozetka
        elif asn_id == 34056:
            # https://kievnet.ua/uk/technical-settings
            nameservers.append('92.244.96.117')
            nameservers.append('92.244.96.10')
            #nameservers.append('ns3.kievnet.ua')
            #nameservers.append('ns2.kievnet.ua')
            #nameservers.append('ns1.kievnet.ua')
        else:
            nameservers.append("103.86.99.99")
            nameservers.append("103.86.96.100")
        return nameservers

# def _get_nameserver(ip_address_pub=None, nameservers=["1.1.1.1"]):
#     # ip_addresses_block = File.get_request_text_as_json(
#     # "https://api.github.com/repos/babyish-retired0m/functions/contents/ip_addresses_block_Provider?ref=main")
#     # https://sites.google.com/site/publicdnsservers

#     parent_dir = os.path.dirname(__file__) + "/ip_addresses_block_provider/"
#     ip_addresses_block_as_9009 = File.open_as_list(parent_dir + "AS-9009_m247.com.txt")
#     # DataCamp network (AS60068)
#     ip_addresses_block_as_393942 = File.open_as_list(parent_dir + "AS-393942_datacamp.co.uk.txt")
#     ip_addresses_block_as_42831 = File.open_as_list(
#         parent_dir + "AS-42831_ukservers.com.txt")
#     ip_addresses_block_as_21497 = File.open_as_list(
#         parent_dir + "AS-21497_vodafone.ua.txt")
#     ip_addresses_block_as_39608 = File.open_as_list(parent_dir + "AS-39608_lanet.ua.txt")
#     ip_addresses_block_as_15895 = File.open_as_list(
#         parent_dir + "AS-15895_kyivstar.ua.txt")
#     ip_addresses_block_as_34058 = File.open_as_list(
#         parent_dir + "AS-34058_lifecell.ua.txt")
#     ip_addresses_block_as_44668 = File.open_as_list(
#         parent_dir + "AS-44668_znet.com.ua.txt")
#     ip_addresses_block_as_44600 = File.open_as_list(
#         parent_dir + "AS-44600_gigatrans.ua.txt")
#     ip_addresses_block_as_48683 = File.open_as_list(parent_dir + "AS-48683_www.bilink.ua.txt")
#     ip_addresses_block_as_48683 = File.open_as_list(parent_dir + "AS-31148_o3.ua.txt")

#     # DNS IP address Lanet:
#     if ip_address.check_ip_in_networks(ip_address_pub, ip_addresses_block_as_39608):
#         nameservers.append("194.50.85.5")
#         # nameservers.extend(["194.50.85.5","194.50.85.7"])
#         # nameservers.remove("9.9.9.9")
#         # nameservers.remove("64.6.64.6")
#         # nameservers.remove("209.244.0.3")

#     # DNS IP address Vodafone:
#     elif ip_address.check_ip_in_networks(ip_address_pub, ip_addresses_block_as_21497):
#         nameservers.append("88.214.96.116")

#         # Vodafone Ukraine - Lviv Oblast 178.133.89.173
#         # 2a00:f50:4400::1004, 80.255.73.119, 2a00:f50:4400::1002, 80.255.73.117,
#         # 2a00:f50:4400::1001, 80.255.73.116, 2a00:f50:4400::1003, 80.255.73.118
#         nameservers.append("80.255.73.116")
#         # nameservers.append("2a00:f50:4400::1004")
#         # nameservers.extend(["80.255.73.117", "80.255.73.118", "80.255.73.119"])

#         # Vodafone Ukraine Kyiv, Ukraine 89.209.89.133
#         # ns29.vf-ua.net, 2a00:f50:5700::1001
#         nameservers.append("80.255.64.172")
#     # ns30.vf-ua.net, 2a00:f50:5700::1002
#     # nameservers.append("80.255.64.173")

# Hello 77.52.64.210  # Retorville WiFi novus-free 
# from Dnipro, Ukraine

# IP  Hostname    ISP Country
# 188.122.80.232  hosted-by.i3d.net.  i3D.net B.V Warsaw, Poland 
# 188.122.80.234  hosted-by.i3d.net.  i3D.net B.V Warsaw, Poland 
# 188.122.80.235  hosted-by.i3d.net.  i3D.net B.V Warsaw, Poland
# 2a04:c605:409:fe::235
# 2a04:c605:409:fe::234 Poland Poland - Mazovia  i3D.net B.V  54 hit
# 2a04:c605:409:fe::232
#     # DNS IP address Kyivstar:
#     elif ip_address.check_ip_in_networks(ip_address_pub, ip_addresses_block_as_15895):
#           # Hello 188.163.81.61 from Kyiv, Ukraine
#           # 81.23.24.162  81-23-24-162-nat.gprs.kyivstar.net. Kyivstar    Kyiv, Ukraine 
#           # 81.23.24.163    81-23-24-163-nat.gprs.kyivstar.net. Kyivstar    Kyiv, Ukraine 
#           # 81.23.24.66 81-23-24-66-nat.gprs.kyivstar.net.  Kyivstar    Kyiv, Ukraine 
#           # 81.23.24.67 81-23-24-67-nat.gprs.kyivstar.net. Kyivstar    Kyiv, Ukraine 
#           # Hello 188.163.82.150 from Kyiv, Ukraine
#         nameservers.append("193.41.60.1")
#         nameservers.append("81.23.24.66")
#         nameservers.append("81.23.24.67")
#         nameservers.append("81.23.24.162")
#         nameservers.append("81.23.24.163")

#         nameservers.append("88.214.96.116")
#     # nameservers.extend(["88.214.96.116","88.214.96.117","88.214.96.118","88.214.96.119"])
#     # nameservers.extend(["193.41.60.1","193.41.60.2"])

#     # 188.163.81.86 - from Kyiv, Ukraine
#     # IP	Hostname	ISP	Country
#     # 81.23.24.66	81-23-24-66-nat.gprs.kyivstar.net.	Kyivstar	Kyiv, Ukraine
#     # 81.23.24.67	81-23-24-67-nat.gprs.kyivstar.net.	Kyivstar	Kyiv, Ukraine
#     # 81.23.24.162	81-23-24-162-nat.gprs.kyivstar.net.	Kyivstar	Kyiv, Ukraine
#     # 81.23.24.163	81-23-24-163-nat.gprs.kyivstar.net.	Kyivstar	Kyiv, Ukraine

#     # DNS IP address NordVPN
#     elif ip_address.check_ip_in_networks(ip_address_pub, ip_addresses_block_as_9009) or ip_address.check_ip_in_networks(
#             ip_address_pub, ip_addresses_block_as_42831) or ip_address.check_ip_in_networks(ip_address_pub, ip_addresses_block_as_393942):
#         nameservers.append("103.86.99.99")
#         nameservers.append("103.86.96.100")
#     # nameservers.extend(["103.86.96.100","103.86.99.99","103.86.99.100"])

#     # DNS IP address Lifecell:
#     elif ip_address.check_ip_in_networks(ip_address_pub, ip_addresses_block_as_34058):
#         nameservers.append("212.58.161.173")
#     # nameservers.extend(["212.58.161.174","2a00:1e98:1104:fd::5"])

#     # DNS IP address znet.com.ua:
#     elif ip_address.check_ip_in_networks(ip_address_pub, ip_addresses_block_as_44668):
#         nameservers.append("91.202.104.6")
#         nameservers.append("162.158.248.73")

#     # DNS IP address gigatrans.ua:
#     elif ip_address.check_ip_in_networks(ip_address_pub, ip_addresses_block_as_44600):
#         nameservers.append("172.253.1.129")

#     # DNS IP address www.bilink.ua:
#     elif ip_address.check_ip_in_networks(ip_address_pub, ip_addresses_block_as_as_48683):
#         pass

#     # DNS IP address o3.ua:
        # Provider name: Freenet LTD
        # Provider website:   http://o3.ua/
        # Provider AS:    31148 (whois)
        # IP address of the domain:   109.251.113.23 (whois)
#     elif ip_address.check_ip_in_networks(ip_address_pub, ip_addresses_block_as_as_31148):
#         pass
    
#     # nameservers.extend(['172.253.1.130', '172.253.1.131', '172.253.1.132', '172.253.1.133', '172.253.206.33',
#     # '172.253.206.34', '172.253.206.35', '172.253.206.36', '172.253.206.37', '172.253.255.33', '172.253.255.34',
#     # '172.253.255.35', '172.253.255.36', '172.253.255.37'])
    
#     # Checking DNS record propagation
#     # https://2ip.me/en/services/information-service/dns-check nameservers = ['208.67.222.220', '8.8.8.8', '9.9.9.9',
#     # '98.113.146.9', '12.121.117.201', '66.206.166.2', '5.11.11.5', '163.172.107.158', '212.230.255.1',
#     # '194.209.157.109', '83.137.41.9', '194.145.241.6', '84.200.70.40', '200.56.224.11', '200.248.178.54',
#     # '103.26.250.4', '1.1.1.1', '61.8.0.113', '210.48.77.68', '164.124.101.2', '202.46.34.75', '31.7.37.37',
#     # '115.178.96.2', '58.27.149.60', '185.83.212.30', '103.146.221.20', '8.8.4.4', '64.6.64.6', '208.67.220.220',
#     # '209.244.0.3', '1.0.0.1', '208.67.222.222']


"""
https://www.lifewire.com/free-and-public-dns-servers-2626062

Best Free & Public DNS Servers
Provider    Primary DNS Secondary DNS
Google  8.8.8.8 8.8.4.4
Control D   76.76.2.0   76.76.10.0
Quad9   9.9.9.9 149.112.112.112
OpenDNS Home    208.67.222.222  208.67.220.220
Cloudflare  1.1.1.1 1.0.0.1
CleanBrowsing   185.228.168.9   185.228.169.9
Alternate DNS   76.76.19.19 76.223.122.150
AdGuard DNS 94.140.14.14    94.140.15.15

Additional DNS Servers
Here are several more public DNS servers from major providers.

More Free DNS Servers
Provider    Primary DNS Secondary DNS
DNS.WATCH   84.200.69.80    84.200.70.40
Comodo Secure DNS   8.26.56.26  8.20.247.20
CenturyLink (Level3)    205.171.3.65    205.171.2.65
CIRA Canadian Shield    149.112.121.10  149.112.122.10
SafeDNS 195.46.39.39    195.46.39.40
OpenNIC 159.89.120.99   134.195.4.2
Dyn 216.146.35.35   216.146.36.36
Yandex DNS  77.88.8.8   77.88.8.1
Hurricane Electric  74.82.42.42  
Neustar 64.6.64.6   64.6.65.6
Freenom World   80.80.80.80 80.80.81.81
DNS for Family  94.130.180.225  78.47.64.161
FlashStart  185.236.104.104 185.236.105.105
"""






# Cisco (San Jose, CA, US)

# 64.102.255.44
# 128.107.241.185


# Level 3 Communications (Broomfield, CO, US)

# 4.2.2.1
# 4.2.2.2
# 4.2.2.3
# 4.2.2.4
# 4.2.2.5
# 4.2.2.6


# Verizon (Reston, VA, US)

# 151.197.0.38
# 151.197.0.39
# 151.202.0.84
# 151.202.0.85
# 151.202.0.85
# 151.203.0.84
# 151.203.0.85
# 199.45.32.37
# 199.45.32.38
# 199.45.32.40
# 199.45.32.43


# GTE (Irving, TX, US)

# 192.76.85.133
# 206.124.64.1


# SpeakEasy (Seattle, WA, US)

# 66.93.87.2
# 216.231.41.2
# 216.254.95.2
# 64.81.45.2
# 64.81.111.2
# 64.81.127.2
# 64.81.79.2
# 64.81.159.2
# 66.92.64.2
# 66.92.224.2
# 66.92.159.2
# 64.81.79.2
# 64.81.159.2
# 64.81.127.2
# 64.81.45.2
# 216.27.175.2
# 66.92.159.2
# 66.93.87.2


# Sprintlink (Overland Park, KS, US)

# 199.2.252.10
# 204.97.212.10
# 204.117.214.10

# Взято: http://www.poltavaforum.com/ukrtelecom-ukrtelekom-215/5589-problemi-dns-dns-ukrtelekomu.html#ixzz7oZS5kpwd



#     return nameservers