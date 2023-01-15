#!/usr/bin/env python3
__version__ = "2.3"
# 2.3 get_ip_address_public_amazon().timeout_count -> tries

# 2.2 check_ip_in_networks()
"""
http://ipv4.google.com/).
If all of these tests work, everything is working correctly. If not, go to the next step.
From your browser, type in a fixed IP address. You can use http://216.218.228.119/ (which points to the test-ipv6.com 
"""

if __name__ == '__main__':
	import file as file	
	import utility as utility
else:	
	import utilities.file as file
	import utilities.utility as utility

	
File = file.Main(print_result=False)
import os


import ipaddress

def get_ip_address_valid(address, print_result=False):
	# import ipaddress
	try:
		answer = ipaddress.ip_address(address)
		return True#print("appear to be an IPv4 or IPv6 address")
	#except Exception as error: return False#print("does not appear to be an IPv4 or IPv6 address")
	except Exception as e:
		if print_result: utility.print_grey('does not appear to be an IPv4 or IPv6 address')
		return False


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
	# This requires the requests library be installed.  You can learn more
	# about the Requests library here: http://docs.python-requests.org/en/latest/
	try:
		import requests
	except ImportError:
		raise SystemExit("Please install requests, pip3 install requests, You can learn more about the Requests library here: http://docs.python-requests.org/en/latest/")

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
	

def get_ip_address_public_amazon(tries = 100, timeout_sleep = 10):
	try:
		import requests
	except ImportError:
		raise SystemExit("Please install requests, pip3 install requests, You can learn more about the Requests library here: http://docs.python-requests.org/en/latest/")

	import time
	while True:
		try:
			return requests.get("https://checkip.amazonaws.com").text.strip()
		except:#import sys;#sys.exit(1)
			#print("The timeout error get_ip_address_public_amazon message has been received")
			#return None
			if tries == 1:
				print(utility.warp_red2('Check your internet connection'))
				break
			else:
				print('\n\n')
				print(utility.warp_red2('Error connecting'), 'to https://checkip.amazonaws.com.', '\n\t', utility.warp_red('Check Amazon status'), 'https://status.aws.amazon.com.')
				print('\n' + utility.warp_blue2('Check your internet connection'), 'timeout', utility.warp_yellow(timeout_sleep), 'seconds, tries out #', tries)
				print('\n\t', utility.warp_yellow('THE TIME: ' + time.ctime()))
				time.sleep(timeout_sleep)
				tries -= 1
				get_ip_address_public_amazon(tries, timeout_sleep)
				#sys.exit(1)


def check_ip_in_network(ip_address,ip_network):
	# import ipaddress
	if ipaddress.ip_address(ip_address) in ipaddress.ip_network(ip_network): return True


def check_ip_in_networks(ip_address, ip_network_list, print_result=False):
	for ip_network in ip_network_list:
		if ip_network.startswith('#'): pass
		elif check_ip_in_network(ip_address,ip_network):
			if print_result: print("Yay!",ip_address,ip_network)
			return ip_network


def check_ip_in_network_lanet_ua(ip_address):
	#print("check_ip_in_network_lanet_ua ip_address",ip_address)
	#ip_address=get_ip_address_public_amazon()
	parent_dir = os.path.dirname(__file__)
	#ip_network_list=File.open_as_list("/Users/jozbox/python/functions/ip_addresses_block_Provider/AS-39608_lanet.ua.txt")
	ip_network_list=File.open_as_list(parent_dir + "/ip_addresses_block_provider/AS-39608_lanet.ua.txt")
	ip_network = check_ip_in_networks(ip_address,ip_network_list)
	return ip_network


def get_ip_in_networks(ip_address_public, asn_list = None, print_result=True):
	# subnet and IP address subranges
	import pathlib
	if asn_list is None:
		parent_dir = os.path.dirname(__file__) + "/ip_addresses_block_provider"
		provider_asn_dict = get_provider_asn_dict(parent_dir = parent_dir)
		asn_dict = {}
		#if print_result: print('provider_asn_dict:', provider_asn_dict)
		# if print_result: print('ip_address.get_ip_in_networks().asn_dict:', asn_dict)
		
		for asn_id in provider_asn_dict:
			if asn_id.startswith('#'): pass
			else:
				# if print_result: print('ip_address.get_ip_in_networks().asn_id:', asn_id)
				
				# ip_network_asn_list = File.open_as_list(parent_dir + asn_id['file_name'])
				asn_ip_address = check_ip_in_networks(ip_address_public, File.open_as_list(provider_asn_dict[asn_id]['asn_file_name']))
				# if print_result: print('ip_address.get_ip_in_networks().asn_ip_address:', asn_ip_address)
				# asn_dict[asn_id]['asn_file_name'] = pathlib.Path(provider_asn_dict[asn_id]['asn_file_name']).stem
				
				# asn_dict[asn_id] = {'asn_file_name': pathlib.Path(provider_asn_dict[asn_id]['asn_file_name']).stem}
				if asn_ip_address:
					# asn_dict[asn_id]['asn_ip_address'] = {asn_ip_address}
					asn_dict[asn_id] = {'asn_id': asn_id,
										'asn_ip_address_subnet': asn_ip_address,
										'asn_name': provider_asn_dict[asn_id]['asn_name'],
										'asn_website': provider_asn_dict[asn_id]['asn_website'],
										'asn_file_name': str(pathlib.Path(provider_asn_dict[asn_id]['asn_file_name'].name))}
					if print_result:
						print('\n\t', utility.warp_yellow('Yay! ip in network ASN: ' + asn_dict[asn_id]['asn_name'] + 'asn_id: ' + asn_id + ' asn_website: ' + provider_asn_dict[asn_id]['asn_website'] + ' asn_file_name:' + str(pathlib.Path(provider_asn_dict[asn_id]['asn_file_name']).name)))
					return asn_dict[asn_id]
	else:
		asn_ip_address = check_ip_in_networks(ip_address_public, asn_list)
		if asn_ip_address:
			if print_result: print('\n\t', utility.warp_yellow('Yay! ip in network: ' + asn_ip_address))
			return asn_ip_address
	# print('ip_address.get_ip_in_networks() asn_dict', asn_dict)


# def _get_ip_in_networks(ip_address_public, ip_network_list = None, print_result=True):
# 	parent_dir = os.path.dirname(__file__)
# 	ip_network_listing_path = parent_dir + "ip_addresses_block_provider"
# 	ip_network_list = File.dir_listing_files_in_this_directory_tree(path = ip_network_listing_path, file_extension = "txt")
# 	for ip_network_path in ip_network_list:
# 		ip_network_listing = File.open_as_list(ip_network_path)
# 		for ip_network in ip_network_listing:
# 			if check_ip_in_network(ip_address_public, ip_network):
# 				if print_result:
# 					print('\n\t', utility.warp_yellow('Yay! ip in network: ' + ip_network_path.stem))
# 				return str(ip_network_path.stem)		
# 		# print('\n\t', utility.warp_yellow('Yay! ip_address_public: ' + ip_address_public + ' in network: None'))


def get_provider_asn_dict(parent_dir):
	import re
	files_list = File.dir_listing_files_in_this_directory_tree(path = parent_dir, file_extension = "txt")
	#print('ip_address.get_provider_asn_dict() parent_dir', parent_dir)
	#print('ip_address.get_provider_asn_dict() files_list', files_list)
	result_dict = {}
	for (enum, file_name) in enumerate(files_list, start=0):
		# result = re.findall(r'(?P<asn>\d+)\_(?P<website>.*?)\.txt', file_name)
		#print('file_name',file_name)
		result = re.findall(r'(\d+)\_(.*?)\.txt', str(file_name))
		#print('result', result)
		result_dict[result[0][0]] = {'asn_id': result[0][0],
									'asn_name': result[0][1].replace('www.','').split('.')[0],
									'asn_website': result[0][1],
									'asn_file_name': file_name}
	#print('ip_address.get_provider_asn_dict()', result_dict)
	return result_dict

def is_ipv4(address_str):
        try:
            ipaddress.IPv4Network(address_str)
            return True
        except ValueError:
            return False

def is_ipv6(address_str):
        try:
            ipaddress.IPv6Network(address_str)
            return True
        except ValueError:
            return False


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
	#ip_network_list=File.open_as_list("ip_addresses_block_provider/AS-9009_m247.com.txt")
	#ip_network_list=File.open_as_list("ip_addresses_block_provider/AS-39608_lanet.ua.txt")
	ip_network_list = File.open_as_list("ip_addresses_block_provider/AS-42831_ukservers.com.txt")
	if check_ip_in_networks(ip_address,ip_network_list): print(ip_address)
	print(check_ip_in_network_lanet_ua())