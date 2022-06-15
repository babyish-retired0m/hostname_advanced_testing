#!/usr/bin/env python3
__version__ = "1.5"
import utilities.file as file	
import utilities.utility as utility
File = file.Main(print_result=False)

def get_ip_address_valid(address):
	import ipaddress
	try:
		answer = ipaddress.ip_address(address)
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
def extract_mac_address():
	import re, uuid
	print(hex(uuid.getnode()))
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
def get_local_ip():
	from netifaces import interfaces, ifaddresses, AF_INET
	for ifaceName in interfaces():
	    addresses = [i['addr'] for i in ifaddresses(ifaceName).setdefault(AF_INET, [{'addr':'No IP addr'}] )]
	    print(' '.join(addresses))
def get_ip_address_public_ipify(timeout_count = 100):
	# This example requires the requests library be installed.  You can learn more
	# about the Requests library here: http://docs.python-requests.org/en/latest/
	import requests
	
	"""ip = requests.get('https://api.ipify.org').text
	#print('My public IP address is: {}'.format(ip))
	return ip"""

	import time
	while True:
		try:
			return requests.get("https://api.ipify.org").text.strip()
		except:#import sys;#sys.exit(1)
			#print("The timeout error get_ip_address_public_amazon message has been received")
			#return None
			if timeout_count == 0:
				print("{}Check your internet connection{}".format(utility.Clr.RED2, utility.Clr.RST2))
				break				 
			else:
				print("Error connecting to https://api.ipify.org")
				print("{}Check your internet connection{}, timeout 10 seconds, timeout #".format(utility.Clr.BLUE2, utility.Clr.RST2), timeout_count)
				time.sleep(10)
				timeout_count -= 1
				get_ip_address_public_ipify(timeout_count)
				#sys.exit(1)

#def check_internet_status():
	
def get_ip_address_public_amazon(timeout_count = 100):
	import requests
	import time
	while True:
		try:
			return requests.get("https://checkip.amazonaws.com").text.strip()
		except:#import sys;#sys.exit(1)
			#print("The timeout error get_ip_address_public_amazon message has been received")
			#return None
			if timeout_count == 0:
				print("{}Check your internet connection{}".format(utility.Clr.RED2, utility.Clr.RST2))
				break				 
			else:
				print("Error connecting to https://checkip.amazonaws.com.\nCheck Amazon status https://status.aws.amazon.com")
				print("{}Check your internet connection{}, timeout 10 seconds, timeout #".format(utility.Clr.BLUE2, utility.Clr.RST2), timeout_count)
				time.sleep(10)
				timeout_count -= 1
				get_ip_address_public_amazon(timeout_count)
				#sys.exit(1)
def check_ip_in_network(ip_address,ip_network):
	import ipaddress
	if ipaddress.ip_address(ip_address) in ipaddress.ip_network(ip_network): return True
def check_ip_in_networks(ip_address,ip_network_list):
	for ip_network in ip_network_list:
		if check_ip_in_network(ip_address,ip_network): return ip_network#print("Yay!",ip_address,ip_network)
def check_ip_in_network_lanet_ua(ip_address):
	#print("check_ip_in_network_lanet_ua ip_address",ip_address)
	#ip_address=get_ip_address_public_amazon()
	ip_network_list=File.open_as_list("/Users/jozbox/python/functions/ip_addresses_block_Provider/AS-39608_lanet.ua.txt")
	ip_network=check_ip_in_networks(ip_address,ip_network_list)
	if ip_network: return ip_network
if __name__ == '__main__':
	#get_ip_address_public_ipify();print('My public IP address is: {}'.format(get_ip_address_public()))
	#get_ip_address_website()
	#get_ip_address_website_url()
	
	"""print(IP_address('127.0.0.1'))
	print(IP_address('3.96.23.237'))
	IP_Address_validation()"""
	extract_mac_address()
	#print(extract_ip())
	#get_local_ip()
	import file
	File = file.Main(print_result=False)
	ip_address = get_ip_address_public_amazon()
	#ip_address="176.37.51.215"
	#ip_network_list=File.open_as_list("/Users/johndoe/python/functions/ip_addresses_block_Provider_AS-9009_m247.com.txt")
	#ip_network_list=File.open_as_list("/Users/johndoe/python/functions/ip_addresses_block_Provider_AS-39608_lanet.ua.txt")
	ip_network_list = File.open_as_list("/Users/johndoe/python/functions/ip_addresses_block_Provider_AS-42831_ukservers.com.txt")
	if check_ip_in_networks(ip_address,ip_network_list): print(ip_address)
	print(check_ip_in_network_lanet_ua())