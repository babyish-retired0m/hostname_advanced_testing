#!/usr/bin/env python3
"""
Copyright 2022. All rights reserved.
"""
__version__ = "1.0"
if __name__ == '__main__':
	import helper_ip_ipinfo as ip_ipinfo
	import helper_ip_twoip as ip_twoip
	import ip_address as ip_address
	import file
	import utility as utility
else:
	#import utilities.helper_ip_ipinfo as ip_ipinfo
	import utilities.helper_ip_twoip as ip_twoip
	import utilities.ip_address as ip_address
	import utilities.file as file
	import utilities.utility as utility
	import utilities.dns_nameserver as dns_nameserver
	import utilities.helper_ip_ipinfo as ip_info
import re
import os
import pathlib
import time

File = file.Main(print_result=True)


def get_asn_for_a_given_ip_dict(ip_address, print_result = False):#twoip
	# asn_twoip {'ip': '185.217.69.123', 'name_ripe': 'M247 LTD', 'name_rus': '', 'site': 'http://www.m247.com/', 'as': '9009', 'ip_range_start': '3118023936', 'ip_range_end': '3118024191', 'route': '185.217.69.0', 'mask': '24'}
	try:
		asn_twoip_dict = ip_twoip.retrieve_ip_dict(ip_address)
	except RuntimeError as e:
		raise e
		print('\n\n\t\tERROR: Failed to send API request. API has reached rate limit; retry in an hour or use an API key\n\n')
	except Exception as e:
		raise e
	if print_result: 
		print('asn_twoip')
		utility.pretty_print(asn_twoip_dict)
		# map(lambda x: print(x, asn_twoip[x]) for asn_twoip)
	# if asn_twoip_dict['name_ripe'].startswith('Proxy route object for'):
	# 	result = re.search(r'AS(?P<as1>\d+) by AS(?P<as2>\d+)', asn_twoip_dict['name_ripe'])
	if 'name_ripe' in asn_twoip_dict:
		return asn_twoip_dict
	else:
		asn_ipinfo_dict = ip_info.get_lookup_ip_dict(ip_address=ip_address)
		name_ripe = asn_ipinfo_dict.get('org')
		pattern_result = r'(?P<as>AS\d+)(?P<asn>.*)'
		result_asn = re.search(pattern_result, name_ripe)
		if result_asn: name_ripe = result_asn['asn'].strip()
		asn_twoip_dict['name_ripe'] = name_ripe
		return asn_twoip_dict
		



def __get_asn_prefixes_list__(asn_id, print_result = False):
	# data call returns all announced prefixes for a given ASN. The results
	try:
		asn_response_dict = File.get_request_text_as_json(url='https://stat.ripe.net/data/announced-prefixes/data.json?resource=' + asn_id)
	except Exception as e:
		raise e
	if print_result: utility.pretty_print(asn_response_dict)
	# asn_prefixes_list = []
	# for asn_ip_subnet in asn_response_dict['data']['prefixes']:
	# 	if ip_address.is_ipv4(asn_ip_subnet['prefix']):
	# 		asn_prefixes_list.append(asn_ip_subnet['prefix'])
	# return asn_prefixes_list
	#return list(asn_ip_subnet['prefix'] for asn_ip_subnet in asn_response_dict['data']['prefixes'] if ip_address.is_ipv4(asn_ip_subnet['prefix']))
	##return list(map(ip_address.is_ipv4(asn_ip_subnet['prefix']), asn_response_dict['data']['prefixes']))
	return list(filter(ip_address.is_ipv4, list(data['prefix'] for data in asn_response_dict['data']['prefixes'])))


def __check_file_exists__(asn_id, asn_files_list):
	if asn_id not in asn_files_list:
		return asn_id
	return None


def __create_asn_file__(asn_twoip_dict, asn_list):
	#asn_list, asn_id, asn_website
	#Valid952HostnameRegex = "^(([a-zA-Z]|[a-zA-Z][a-zA-Z0-9\-]*[a-zA-Z0-9])\.)*([A-Za-z]|[A-Za-z][A-Za-z0-9\-]*[A-Za-z0-9])$";
	#asn_website = asn_twoip_dict['site'].replace('https://', '').replace('http://', '').replace('www.', '')
	file_name = 'AS-' + asn_twoip_dict['as']
	asn_dict = {'info': asn_twoip_dict, 'data_prefixes': asn_list}
	asn_dict['info']['time'] = time.ctime()
	asn_dict['info']["unix epoch time"] = time.time()
	asn_dict['info']["timezone"] = "UTC",
	asn_path = os.path.dirname(__file__) + '/ip_addresses_block_provider/' + file_name
	File.write_text_as_json(path = asn_path, text = asn_dict)
	return asn_path + '.json'


def get_asn_files_dict(print_result = False):
	files_list = File.dir_listing_files_in_this_directory_tree(path = os.path.dirname(__file__) + ('/ip_addresses_block_provider'), file_extension = "json")
	result_dict = {}
	expression_pattern = r'(?P<file_name_prefix>^AS-)(?P<asn_id>\d+)(?P<file_extension>\.json$)'
	for (enum, file_path) in enumerate(files_list, start=0):
		file_name = str(pathlib.Path(file_path).name)
		if print_result: print('file_name:', file_name, '\nfile_path:', str(file_path))
		result = re.search(expression_pattern, file_name)
		if result:
			if print_result: print('file_name result re.search:', result[0], 'asn_id:', result['asn_id'])
			result_dict[result['asn_id']] = {'asn_id': result['asn_id'],# Provider AS asn_id
											'asn_file_name': file_name,
											'asn_file_path': str(file_path)}
	if print_result: print('helper_asn.get_asn_files_dict():', result_dict)
	return result_dict

# def get_asn_info_dict():
# 	asn_files_dict = get_asn_files_dict()
# 	asn_dict = {}
# 	for asn_id in asn_files_dict:
# 		asn_dict[asn_id] = open_asn_file_dict(file_path = asn_files_dict[asn_id]['asn_file_path']).['info']
# 	return asn_dict

def open_asn_file_dict(file_path):
	return File.open_json(pathlib.Path(file_path))


def get_asn_dict(ip_address_public = None, print_result = True, get_asn_id = False, get_asn_name = False):
	asn_files_dict = get_asn_files_dict()
	if ip_address_public is None: ip_address_public = ip_address.get_ip_address_public_amazon()
	for asn_id in asn_files_dict:
		asn_dict = File.open_json(asn_files_dict[asn_id]['asn_file_path'])#asn_dict
		#if print_result: print('asn_dict', asn_dict)
		asn_ip_subnet = ip_address.check_ip_in_networks(ip_address = ip_address_public, ip_network_list = asn_dict['data_prefixes'])
		if asn_ip_subnet:
			if File.check_is_file_need_update(path = asn_files_dict[asn_id]['asn_file_path'], days_ago = 50) is False:
				if print_result: print('\n\n\tOpened asn file:', asn_files_dict[asn_id]['asn_file_path'], '\n\n')
				#return asn_files_dict[asn_id] | {'asn_ip_subnet': asn_ip_subnet, 'ip_address_public': ip_address_public}
				if get_asn_id and get_asn_name:
					data_dict = {'asn_id':asn_dict['info'].get('as'),
								'asn_name':asn_dict['info'].get('name_ripe')}
				elif get_asn_id:
					data_dict = asn_dict['info']['as']
				elif get_asn_name:
					data_dict = asn_dict['info']['name_ripe']
				else:
					data_dict = {
						'asn_id': asn_dict['info']['as'],
						'asn_name': asn_dict['info']['name_ripe'],
						'ip_address_public': asn_dict['info']['ip'],
						'asn_ip_subnet': asn_dict['info']['route'],
						'asn_file_name': pathlib.Path(asn_files_dict[asn_id]['asn_file_path']).name,
						'asn_file_path': str(asn_files_dict[asn_id]['asn_file_path'])
						}
				return data_dict
	
	asn_twoip_dict = get_asn_for_a_given_ip_dict(ip_address = ip_address_public)
	asn_id = asn_twoip_dict['as']
	#asn_id = __check_file_exists__(asn_twoip_dict['as'], list(asn_files_dict))
	
	if asn_id is not None:
		asn_list = sorted(__get_asn_prefixes_list__(asn_id))
		asn_path = __create_asn_file__(asn_twoip_dict, asn_list)
		asn_dict = File.open_json(asn_path)
		if print_result: print('\n\n\tCreated asn file', asn_path, '\n\n')
		if get_asn_id and get_asn_name:
			data_dict = {'asn_id':asn_dict['info']['as'], 'asn_name':asn_dict['info']['name_ripe']}
		elif get_asn_id:
			data_dict = asn_dict['info']['as']
		elif get_asn_name:
			data_dict = asn_dict['info']['name_ripe']
		else:
			data_dict =  {
					'asn_id': asn_dict['info']['as'],
					'asn_name': asn_dict['name']['name_ripe'],
					'ip_address_public': asn_dict['info']['ip'],
					'asn_ip_subnet': asn_dict['info']['route'],
					'asn_file_name': pathlib.Path(asn_path).name,
					'asn_file_path': str(asn_path)
			}
		return data_dict
		#{'asn_id': '51430', 'asn_file_name': 'AS-51430.json', 'asn_file_path': '/src/app/hostname_advanced_testing/utilities/ip_addresses_block_provider/AS-51430.json', 'asn_ip_subnet': '79.142.73.0', 'ip_address_public': '79.142.73.235'}
		#main_wrap()




if __name__ == '__main__':
	print(get_asn_dict())