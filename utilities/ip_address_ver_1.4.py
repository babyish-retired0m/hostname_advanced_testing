#!/usr/bin/env python3
__version__ = "1.4"
import os
import utilities.file as file
	
File = file.Main(print_result=False)

def get_ip_address_valid(address):
	import ipaddress
	try:
		answer=ipaddress.ip_address(address)
		return True#print("appear to be an IPv4 or IPv6 address")
	except Exception as error: return False#print("does not appear to be an IPv4 or IPv6 address")
def get_ip_address():
	import socket
	h_name = socket.gethostname()
	IP_addres = socket.gethostbyname(h_name)
	print("Host Name is:" + h_name)
	print("Computer IP Address is:" + IP_addres)
def get_ip_address_website():
	import socket
	host_name = input("Enter the website address: ")
	print(f'The {host_name} IP address is: {socket.gethostbyname(host_name)}')
def get_ip_address_website_url(url = "python.com"):
	import socket
	#url = "python.com"
	print("IP Address:",socket.gethostbyname(url))
def IP_address(IP: str)-> str:
	from ipaddress import ip_address
	return "Private" if (ip_address(IP).is_private)else "Public"
def IP_Address_validation(IP = '127.0.0.251'):
	import socket 
	try:
	   socket.inet_aton(IP)
	   print("Valid IP address")
	except socket.error:
	   print("Invalid IP")
def extract_MAC_address():
	import uuid
	print(hex(uuid.getnode()))
	import re, uuid
	print("MAC address in less complex and formatted way is: ", end="")
	print(':'.join(re.findall('..', '%012x' %uuid.getnode())))
def extract_ip():
    import socket
    st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:       
        st.connect(('10.255.255.255', 1))
        #st.connect(("8.8.8.8", 80))
        IP = st.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        st.close()
    return IP
def Get_Local_IP():
	import netifaces
	from netifaces import interfaces, ifaddresses, AF_INET
	for ifaceName in interfaces():
	    addresses = [i['addr'] for i in ifaddresses(ifaceName).setdefault(AF_INET, [{'addr':'No IP addr'}] )]
	    print(' '.join(addresses))
def get_ip_address_public_ipify():
	# This example requires the requests library be installed.  You can learn more
	# about the Requests library here: http://docs.python-requests.org/en/latest/
	from requests import get
	
	ip = get('https://api.ipify.org').text
	#print('My public IP address is: {}'.format(ip))
	return ip
def get_ip_address_public_amazon():
	from requests import get
	try: return get('https://checkip.amazonaws.com').text.strip()
	except:#import sys;sys.exit(1)
		print("The timeout connecting error message has been received")
		print("Error connecting to https://checkip.amazonaws.com.\nCheck your internet connection or https://status.aws.amazon.com")
		return None
def check_ip_in_network(ip_address,ip_network):
	import ipaddress
	if ipaddress.ip_address(ip_address) in ipaddress.ip_network(ip_network): return True
def check_ip_in_networks(ip_address,ip_network_list):
	for ip_network in ip_network_list:
		if check_ip_in_network(ip_address,ip_network): return ip_network#print("Yay!",ip_address,ip_network)
def check_ip_in_network_lanet_ua():
	ip_address=get_ip_address_public_amazon()
	ip_network_list=File.open_as_list(os.path.dirname(__file__) + "/ip_addresses_block_provider/AS-39608_lanet.ua.txt")
	ip_network=check_ip_in_networks(ip_address,ip_network_list)
	if ip_network: return ip_network
if __name__ == '__main__':	
	extract_MAC_address()
	print(extract_ip())
	import file
	print(get_ip_address_public_amazon())