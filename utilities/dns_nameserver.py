#!/usr/bin/env python3
__version__ = "1.0"

import os
import utilities.file as file
import utilities.ip_address as ip_address

File = file.Main(print_result=False)


def get_nameserver(ip_address_pub=None, nameservers=["1.1.1.1"]):
    # ip_addresses_block = File.get_request_text_as_json(
    # "https://api.github.com/repos/babyish-retired0m/functions/contents/ip_addresses_block_Provider?ref=main")

    parent_dir = os.path.dirname(__file__) + "/ip_addresses_block_provider/"
    ip_addresses_block_as_9009 = File.open_as_list(parent_dir + "AS-9009_m247.com.txt")
    # DataCamp network (AS60068)
    ip_addresses_block_as_393942 = File.open_as_list(parent_dir + "AS-393942_datacamp.co.uk.txt")
    ip_addresses_block_as_42831 = File.open_as_list(
        parent_dir + "AS-42831_ukservers.com.txt")
    ip_addresses_block_as_21497 = File.open_as_list(
        parent_dir + "AS-21497_vodafone.ua.txt")
    ip_addresses_block_as_39608 = File.open_as_list(parent_dir + "AS-39608_lanet.ua.txt")
    ip_addresses_block_as_15895 = File.open_as_list(
        parent_dir + "AS-15895_kyivstar.ua.txt")
    ip_addresses_block_as_34058 = File.open_as_list(
        parent_dir + "AS-34058_lifecell.ua.txt")
    ip_addresses_block_as_44668 = File.open_as_list(
        parent_dir + "AS-44668_znet.com.ua.txt")
    ip_addresses_block_as_44600 = File.open_as_list(
        parent_dir + "AS-44600_gigatrans.ua.txt")

    # DNS IP address Lanet:
    if ip_address.check_ip_in_networks(ip_address_pub, ip_addresses_block_as_39608):
        nameservers.append("194.50.85.5")
        # nameservers.extend(["194.50.85.5","194.50.85.7"])
        # nameservers.remove("9.9.9.9")
        # nameservers.remove("64.6.64.6")
        # nameservers.remove("209.244.0.3")

    # DNS IP address Vodafone:
    elif ip_address.check_ip_in_networks(ip_address_pub, ip_addresses_block_as_21497):
        nameservers.append("88.214.96.116")

        # Vodafone Ukraine - Lviv Oblast 178.133.89.173
        # 2a00:f50:4400::1004, 80.255.73.119, 2a00:f50:4400::1002, 80.255.73.117,
        # 2a00:f50:4400::1001, 80.255.73.116, 2a00:f50:4400::1003, 80.255.73.118
        nameservers.append("80.255.73.116")
        # nameservers.append("2a00:f50:4400::1004")
        # nameservers.extend(["80.255.73.117", "80.255.73.118", "80.255.73.119"])

        # Vodafone Ukraine Kyiv, Ukraine 89.209.89.133
        # ns29.vf-ua.net, 2a00:f50:5700::1001
        nameservers.append("80.255.64.172")
    # ns30.vf-ua.net, 2a00:f50:5700::1002
    # nameservers.append("80.255.64.173")

    # DNS IP address Kyivstar:
    elif ip_address.check_ip_in_networks(ip_address_pub, ip_addresses_block_as_15895):
        nameservers.append("193.41.60.1")
    # nameservers.append("81.23.24.66")
    # nameservers.extend(["88.214.96.116","88.214.96.117","88.214.96.118","88.214.96.119"])
    # nameservers.extend(["193.41.60.1","193.41.60.2"])

    # 188.163.81.86 - from Kyiv, Ukraine
    # IP	Hostname	ISP	Country
    # 81.23.24.66	81-23-24-66-nat.gprs.kyivstar.net.	Kyivstar	Kyiv, Ukraine
    # 81.23.24.67	81-23-24-67-nat.gprs.kyivstar.net.	Kyivstar	Kyiv, Ukraine
    # 81.23.24.162	81-23-24-162-nat.gprs.kyivstar.net.	Kyivstar	Kyiv, Ukraine
    # 81.23.24.163	81-23-24-163-nat.gprs.kyivstar.net.	Kyivstar	Kyiv, Ukraine

    # DNS IP address NordVPN
    elif ip_address.check_ip_in_networks(ip_address_pub, ip_addresses_block_as_9009) or ip_address.check_ip_in_networks(
            ip_address_pub, ip_addresses_block_as_42831) or (ip_address_pub, ip_addresses_block_as_393942):
        nameservers.append("103.86.99.99")
        nameservers.append("103.86.96.100")
    # nameservers.extend(["103.86.96.100","103.86.99.99","103.86.99.100"])

    # DNS IP address Lifecell:
    elif ip_address.check_ip_in_networks(ip_address_pub, ip_addresses_block_as_34058):
        nameservers.append("212.58.161.173")
    # nameservers.extend(["212.58.161.174","2a00:1e98:1104:fd::5"])

    # DNS IP address znet.com.ua:
    elif ip_address.check_ip_in_networks(ip_address_pub, ip_addresses_block_as_44668):
        nameservers.append("91.202.104.6")
        nameservers.append("162.158.248.73")

    # DNS IP address gigatrans.ua:
    elif ip_address.check_ip_in_networks(ip_address_pub, ip_addresses_block_as_44600):
        nameservers.append("172.253.1.129")
    # nameservers.extend(['172.253.1.130', '172.253.1.131', '172.253.1.132', '172.253.1.133', '172.253.206.33',
    # '172.253.206.34', '172.253.206.35', '172.253.206.36', '172.253.206.37', '172.253.255.33', '172.253.255.34',
    # '172.253.255.35', '172.253.255.36', '172.253.255.37'])
    # Checking DNS record propagation
    # https://2ip.me/en/services/information-service/dns-check nameservers = ['208.67.222.220', '8.8.8.8', '9.9.9.9',
    # '98.113.146.9', '12.121.117.201', '66.206.166.2', '5.11.11.5', '163.172.107.158', '212.230.255.1',
    # '194.209.157.109', '83.137.41.9', '194.145.241.6', '84.200.70.40', '200.56.224.11', '200.248.178.54',
    # '103.26.250.4', '1.1.1.1', '61.8.0.113', '210.48.77.68', '164.124.101.2', '202.46.34.75', '31.7.37.37',
    # '115.178.96.2', '58.27.149.60', '185.83.212.30', '103.146.221.20', '8.8.4.4', '64.6.64.6', '208.67.220.220',
    # '209.244.0.3', '1.0.0.1', '208.67.222.222']

    return nameservers