#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Python API client for advanced host name testing

This API client will retrieve DNS provider information for host name (resolve DNS), ping, traceroute, ssl_check. Provide a response in JSON. Send requests for various information to public DNS servers (name servers). 

"""

__version__ = "4.1"

import utilities.dns_resolve as dns_resolve
import utilities.ping as ping
import utilities.traceroute as traceroute
import utilities.ssl_check as ssl_check
import utilities.ip_address as ip_address
import utilities.utility as utility
import utilities.file as file
import utilities.helper_asn as helper_asn
import utilities.helper_ip_ipinfo as helper_ip_info
import hosts.nordvpn.servers_nordvpn as servers_nordvpn

import time
import os
import json
import sys
import pathlib
import pprint
#utility.get_check_package('icmplib')
import icmplib

import re

# File = file.Main(print_result = False)
File = file.Main(print_result = True)

class Advanced_testing:
	def __init__(self, 
		get_nslookup = True,
		get_ping = True,
		get_traceroute = True,
		get_ssl_check = True,
		get_dump = True,
		records = ["A", "AAAA", "CNAME", "MX", "SOA", "TXT", "NS"],
		nameserver = None,
		hostnames_dict = {},
		path_results_name = None,
		print_result = True,
		say_result = False,
		# hostnames_start_index = None,
		# pre_party_check = False
		continue_option = False):
		self.get_nslookup = get_nslookup
		self.get_ping = get_ping
		self.get_traceroute = get_traceroute
		self.get_ssl_check = get_ssl_check
		self.get_dump = get_dump
		self.records = records
		self.nameserver = nameserver
		if len(hostnames_dict) > 0:
			self.recv_records = hostnames_dict
		else:
			self.recv_records = {'parameters' : {'unix_epoch_time' : utility.get_time_unix(),
												'timezone':'utc', 'time': time.ctime(),
												'continue': False, 'continuing_chellanges': [],
												'username': utility.get_username(),
												'pcname': utility.get_pcname(),
												'currentdirectory': utility.get_currentdirectory()},
								'parameters_ping': {'count': 10,
												'interval': 0.1,
												'timeout': 1,
												'payload_size': 56},
								'parameters_traceroute': {'max_hops': 30,
												'timeout': 1,
												'interval': 500,
												'payload_size': 56}}
		self.parent_dir = os.path.dirname(__file__)

		self.path_results_name = path_results_name
		self.start_time_local = time.strftime("%Y-%m-%d_%H-%M-%S", utility.get_time_local())		

		self.ip_address_resolved = None
		self.can_not_be_resolve_path = self.parent_dir + "/utilities/can_not_be_resolve.txt"
		self.can_not_be_resolve = File.open_as_list(self.can_not_be_resolve_path)
		self.can_not_be_ssl_check_path = self.parent_dir + "/utilities/can_not_be_ssl_check.txt"
		self.can_not_be_ssl_check = File.open_as_list(self.can_not_be_ssl_check_path)

		self.print_result = print_result
		self.say_result = say_result

		# self.pre_party_check = pre_party_check
		self.continue_option = continue_option

		self.hostnames_path_results = None
		
	"""def __call__(self):
		return self.__get_hostname_advanced_testing__()"""

	def pre_party_check(self):
		pass


	def get_ip_ipinfo_dict(self, ip_address):
		ip_info = helper_ip_info.get_lookup_ip_dict(ip_address)
		return {
				'continent' : ip_info.get('continent'),
				'country' : ip_info.get('country'),
				'country_name' : ip_info.get('country_name'),
				'region' : ip_info.get('region'),
				'city' : ip_info.get('city'),
				'organisation' : ip_info.get('org'),
				'hostname' : ip_info.get('hostname')
		}


	def get_hostnames_continue_list_dict(self, asn_subnet_id, ip_country):
	# def check_result_file_status(self):

		def find_result_files_list():
			dir_results_files_list = File.dir_listing_files_in_this_directory_tree(path = self.parent_dir + '/' + 'results', file_extension = 'json')
			pattern_result_files_asn_list = []
			pattern_asn_file_name = r'(?P<file_name_prefix>^results_)(?P<date>\d*\-\d*\-\d*)(?P<separator>_)(?P<time>\d*\-\d*-\d*)(?P<file_name_as_prefix>_AS-)(?P<as>\d+)((?P<separator2>_)(?P<country>[A-Z]{2})(_hosts_)|(_hosts_))(?P<host>\w+[a-z])(\.json$)'
			#pattern_asn_file_name = r'(^results_)([0-9-]+)(_)([0-9-]+)(_)(AS-)(\d+)(_)(?P<country>[A-Z]{2})(_hosts_)(\w+)((_\w*\.\w+)?)(\.json$)'
			# fulfilling pattern_result_files_asn_list
			for file_path in dir_results_files_list:# find # ip_network_asn
				result_asn = re.search(pattern_asn_file_name, file_path.name)
				if result_asn and int(result_asn['as']) == int(asn_subnet_id) and ip_country == result_asn['country'] and result_asn['host'] == self.path_results_name:
					pattern_result_files_asn_list.append(str(file_path))
			return pattern_result_files_asn_list
		

		def get_last_file_path(files_list, print_result = self.print_result):
			if len(files_list) > 0:
				last_file_path = list(reversed(files_list))[0]
				if self.print_result: print('\n\n\tLast file path:', last_file_path, '\n\n')
				if File.check_is_file_need_update(path = last_file_path, days_ago = 5) is False:# 3
					if self.print_result: print('\n\n\tFile is actual (updated):', last_file_path, '\n\n')
					return last_file_path
				else:
					if self.print_result: print('\n\n\tFile needs update:', last_file_path, '\n\n')
			else: 
				if self.print_result: print('No last file result')
		

		def __check_is_result_file_status_completed__(last_file_json_length, hosts_list_length):
			return True if last_file_json_length >= hosts_list_length else False


		def check_file_status_complete(last_file_json):
			if __check_is_result_file_status_completed__(last_file_json_length = len(last_file_json['advanced_test']) + len(list(x for x in self.can_not_be_resolve if x in self.hostnames)), hosts_list_length = len(self.hostnames)):
				if self.print_result: 
					print('Result file status completed')
					pprint.pprint(last_file_json['parameters'])
				return True
			else:
				if self.print_result: 
					print('Result file status not completed')
					pprint.pprint(last_file_json['parameters'])
				return False


		def get_fulfilling_hostnames_continue_dict(last_file_path):
			last_file_json = File.open_json(last_file_path)
			hostnames_original_sorted_list = sorted(self.hostnames)
			hostnames_last_sorted_list = sorted(last_file_json['advanced_test'])
			hostnames_new_list = []
			hostnames_can_not_be_resolve = list(x for x in self.can_not_be_resolve if x in self.hostnames)
			#hos
			if self.print_result:
				utility.print_green2('\n\n\tFulfilling hostnames continue dict last file path'+last_file_path+'\n\n')	
				print('\n\n\tHostnames original sorted list length', len(hostnames_original_sorted_list), '\n\n')
				print('\n\n\tHostnames last sorted list length', len(hostnames_last_sorted_list), '\n\n')
			for hostname in hostnames_original_sorted_list:
				if hostname not in hostnames_last_sorted_list and hostname not in hostnames_new_list and hostname not in hostnames_can_not_be_resolve:
					hostnames_new_list.append(hostname)
			hostnames_new_list.sort()

			if self.print_result: print('\n\n\tHostnames new list length', len(hostnames_new_list), '\n\n')

			if check_file_status_complete(last_file_json) is False:
				return {'last_file_path_results': last_file_path,
						'job_done': False,
						'last_file_json': last_file_json,
						'hostnames_new_sorted_list': hostnames_new_list,
						# 'hostname_continue_index': hostnames_original_sorted_list.index(hostnames_last_sorted_list[-1])
						'hostname_continue_index': self.hostnames.index(list(last_file_json['advanced_test'])[-1])
						}

		last_file_asn_path = get_last_file_path(files_list = find_result_files_list())
		if last_file_asn_path: return get_fulfilling_hostnames_continue_dict(last_file_asn_path)
		else: utility.print_red2('\n\n\tLast file asn path: No files with matched options.\n\tASN subnet id: '+asn_subnet_id+', ip_country: '+ip_country+'\n')


		# if self.path_results_name == 'all':
		# 	last_file_path = File.get_last_file(path_dir = self.parent_dir + '/results', file_extension = 'json')
		# elif self.path_results_name == 'nordvpn':
		# 	last_file_path = File.get_last_file(path_dir = self.parent_dir + '/results', file_extension = 'json')
		# elif self.path_results_name == 'google':
		# 	last_file_path = File.get_last_file(path_dir = self.parent_dir + '/results', file_extension = 'json')

		# expression pattern, string

		# if last_file_host_name == 'all': hostnames_path = './hosts/services/'
		# elif last_file_host_name == 'nordvpn': hostnames_path = './hosts/nordvpn/'
		# elif last_file_host_name == 'google': hostnames_path = './hosts/google/'
		# for hosts in list(pathlib.Path(hostnames_path).rglob('*.txt')): hosts_list.extend([host.rstrip() for host in open(hosts, 'r').readlines()])
		

		# def pre_party_check(self):
		# 	hostnames_start_job_dict = 


	def __get_ip_public__(self, ip_address_check = False):
		def __get_ip_address_check__():
			# self.ip_address_checked = "176.36.0.0/14" if ip_address.check_ip_in_network_lanet_ua(self.ip_address_public) else self.ip_address_public
			if ip_address.check_ip_in_network_lanet_ua(self.ip_address_public):
				self.ip_address_public = "176.36.0.0" 
		self.ip_address_public = ip_address.get_ip_address_public_amazon(tries = 100, timeout_sleep = 10)
		if self.print_result: print('ip_address_public:', self.ip_address_public)
		if ip_address_check: __get_ip_address_check__()

		return self.ip_address_public
		
		
	def __get_nslookup__(self, qname, ip, asn):
		asn_id = asn.get('asn_id') if isinstance(asn, dict) else None
		Response = dns_resolve.Dns_response(host = qname, records = self.records, nameserver = self.nameserver, ip_address_public_answer = self.ip_address_public, asn_id = asn_id)
		result = Response.get_nslookup()
		recv_records = {"resolve":{"nslookup":result[qname]}}
		recv_records["resolve"]["parameters"] = {'unix_epoch_time': utility.get_time_unix(),
												#'timezone':'UTC',
												'public_ip_address': ip,
												#'pcname': utility.get_pcname(),
												#'username': utility.get_username(),
												#'currentdirectory': utility.get_currentdirectory(),
												#'ASN': asn_id
												}
		return recv_records['resolve']


	def __get_ping__(self, qname, ip, asn):
		result = ping.verbose_ping(address = qname, ip_address_resolved = self.ip_address_resolved)
		if result is not None:
			recv_records = {'verbose_ping':result[qname]}
			recv_records['verbose_ping']['parameters']['unix_epoch_time'] = utility.get_time_unix()
			recv_records['verbose_ping']['parameters']['public_ip_address'] = ip
			#recv_records['verbose_ping']['parameters']['ASN'] = asn
			return recv_records["verbose_ping"]


	def __get_traceroute__(self, qname, ip, asn):
		result = traceroute.verbose_traceroute(address = qname, ip_address_resolved = self.ip_address_resolved, interval=0.05, timeout=0.01)# timeout 0.1 -> 0.01
		if result is not None:
			recv_records = {'verbose_traceroute':result[qname]}
			recv_records['verbose_traceroute']['parameters']['unix_epoch_time'] = utility.get_time_unix()
			recv_records['verbose_traceroute']['parameters']['public_ip_address'] = ip
			#recv_records['verbose_traceroute']['parameters']['ASN'] = asn
			return recv_records['verbose_traceroute']


	def __get_ssl_check__(self, qname, ip, asn):
		if ip_address.get_ip_address_valid(qname): pass
		else:
			if qname not in self.can_not_be_ssl_check:
				sslobject = ssl_check.SSLCheck()
				try:
					result = sslobject.show_result([qname])
					if result is not None:
						recv_records = result[qname]
						return recv_records
					else:
						self.can_not_be_ssl_check.append(qname)
						File.write_list_as_text(self.can_not_be_ssl_check_path, self.can_not_be_ssl_check)
				except: 
					print('__get_ssl_check__ cannot be ssl checked')
					self.can_not_be_ssl_check.append(qname)
					File.write_list_as_text(self.can_not_be_ssl_check_path, self.can_not_be_ssl_check)
			else: pass


	def __get_ip_address_resolved__(self, qname):
		try:
			if ip_address.get_ip_address_valid(qname):
				self.ip_address_resolved = qname
				self.ip_address_flag = True
			else:
				self.ip_address_resolved = icmplib.resolve(qname)[0]
			return True
		except:
			print(utility.warp_red('The name ' + qname + ' can not be resolved'))
			self.can_not_be_resolve.append(qname)
			File.write_list_as_text(self.can_not_be_resolve_path, self.can_not_be_resolve)
			return False


	def get_hostname_advanced_testing(self, hostnames = 'amazon.com'):
		self.job_done = False
		self.start_time = time.time()
		self.recv_records["advanced_test"] = {}
		if isinstance(hostnames, str): self.hostnames = [hostnames]
		elif isinstance(hostnames, list): self.hostnames = hostnames
		else: print("Are list of hostname(s) str, list?"); sys.exit(1)
		# hostnames_start = check_hostnames_start_index()
		ip_public = self.__get_ip_public__(ip_address_check = True)
		asn_subnet = helper_asn.get_asn_dict(ip_address_public = ip_public, print_result = self.print_result, get_asn_id = True, get_asn_name = True)
		self.ip_info = self.get_ip_ipinfo_dict(ip_public)
		if self.path_results_name is not None and self.continue_option:
			
			self.start_job_dict = self.get_hostnames_continue_list_dict(asn_subnet_id = asn_subnet['asn_id'], ip_country = self.ip_info['country'])
			if self.start_job_dict:
				self.hostnames_path_results = self.start_job_dict['last_file_path_results']
				self.job_done = self.start_job_dict['job_done']
				self.recv_records = self.start_job_dict['last_file_json']
				if self.start_job_dict['job_done'] is False:
					if self.recv_records['parameters']['continue'] == False:
						# len(self.recv_records['parameters']['continuing_chellanges'])>0:
						self.recv_records['parameters']['continue'] = True
					self.recv_records['parameters']['continuing_chellanges'].append({'unix_epoch_time' : utility.get_time_unix(),
						'timezone':'utc',
						'time': time.ctime(),
						'public_ip_address': ip_public,
						'asn': asn_subnet,
						'hostname_continue_index': self.start_job_dict['hostname_continue_index'],
						'ip_info': self.ip_info,
						'username': utility.get_username(),
						'pcname': utility.get_pcname(),
						'currentdirectory': utility.get_currentdirectory()
						})
					self.recv_records['parameters']['continue'] = True
					if 'server_nordvpn' not in self.recv_records['parameters']['continuing_chellanges'][-1]:
						server_nordvpn_dict = servers_nordvpn.Servers_NordVPN().find_server_by_ip_address(ip_public)
						if server_nordvpn_dict:
							self.recv_records['parameters']['continuing_chellanges'][-1]['server_nordvpn'] = server_nordvpn_dict
				if len(self.start_job_dict['hostnames_new_sorted_list']) > 0 :
					self.hostnames = self.start_job_dict['hostnames_new_sorted_list']
		# else:
		# 	ip_public = self.__get_ip_public__(ip_address_check = True)
		# 	asn_subnet = helper_asn.get_asn_dict(ip_address_public = ip_public, print_result = self.print_result, get_asn_id = True, get_asn_name = True)
		# 	self.ip_info = self.get_ip_ipinfo_dict(ip_public)
			
			
		self.hostnames_len = len(self.hostnames)
		if self.hostnames_len > 1000: self.k = 100 # 100 -> 10
			# if self.hostnames_len % 2 == 0: self.k = 100
			# else: self.k = 50
		else: self.k = 200 # 200 -> 20
			# if self.hostnames_len % 2 == 0: self.k = 200
			# else: self.k = 150
		if 'public_ip_address' not in self.recv_records['parameters']: self.recv_records['parameters']['public_ip_address'] = ip_public
		if 'ASN' not in self.recv_records['parameters']: self.recv_records['parameters']['asn'] = asn_subnet
		if 'ip_info' not in self.recv_records['parameters']: self.recv_records['parameters']['ip_info'] = self.get_ip_ipinfo_dict(ip_public)
		if 'server_nordvpn' not in self.recv_records['parameters']:
			server_nordvpn_dict = servers_nordvpn.Servers_NordVPN().find_server_by_ip_address(ip_public)
			if server_nordvpn_dict:
				self.recv_records['parameters']['server_nordvpn'] = server_nordvpn_dict
		for enum, qname in enumerate(self.hostnames):
			qname = qname.lower().strip()
			start_time_advanced_test = time.time()
			ip_public = self.__get_ip_public__(ip_address_check = True)
			# self.ip_network_asn
			asn_subnet = helper_asn.get_asn_dict(ip_address_public = ip_public, print_result = self.print_result, get_asn_id = True, get_asn_name = True)
			if self.print_result: print('\n\nhostname qname:', enum, qname, '\n')
			if len(qname)>3 and qname not in self.can_not_be_resolve and self.__get_ip_address_resolved__(qname):
				self.recv_records['advanced_test'][qname] = {}
				print('\n\n')
				utility.print_yellow2('advanced_test start ' + time.strftime("%H:%M:%S", time.gmtime(start_time_advanced_test)))
				utility.print_percents(self.hostnames.index(qname), self.hostnames_len)

				#nslookup
				if self.get_nslookup:
					print('\n\n')
					utility.print_yellow2('NS LOOK UP testing ' + qname)
					self.recv_records["advanced_test"][qname]["resolve"] = self.__get_nslookup__(qname, ip = ip_public, asn = asn_subnet)

				#ping
				if self.get_ping:
					print('\n\n')
					utility.print_yellow2('Ping testing' + qname)
					self.recv_records["advanced_test"][qname]["verbose_ping"] = self.__get_ping__(qname, ip = ip_public, asn = asn_subnet)

				#traceroute
				if self.get_traceroute:
					print('\n\n')
					utility.print_yellow2('Traceroute to ' + qname + ' testing')
					self.recv_records["advanced_test"][qname]["verbose_traceroute"] = self.__get_traceroute__(qname, ip = ip_public, asn = asn_subnet)

				#ssl_check
				if self.get_ssl_check:
					print('\n\n')
					utility.print_yellow2('SSL check testing')
					self.recv_records["advanced_test"][qname]["verbose_ssl_cert"] = {
						'ssl_cert_info': self.__get_ssl_check__(qname, ip = ip_public, asn = asn_subnet),
						'parameters':{
							'public_ip_address': ip_public,
							'unix_epoch_time': utility.get_time_unix(),
							#'ASN': asn_subnet
						}
					}

			if qname in self.hostnames and self.hostnames.index(qname) > 0:
				if self.hostnames.index(qname) % self.k == 0: self.__get_dump__(ip_network_asn = asn_subnet)
				self.__print_result_duration__(qname)
		self.__print_result_execution_time_Duration__()
		self.__get_dump__(ip_network_asn = asn_subnet)

		return self.recv_records


	def __get_path_results__(self, ip_network_asn):
		path = self.parent_dir + "/results/"
		if File.check_dir(path) is False: File.dirs_make(path)
		if ip_network_asn: 
			if 'country' in self.ip_info:
				path_results = path + 'results' + '_' + self.start_time_local + '_' + 'AS-' + ip_network_asn['asn_id'] + '_' + self.ip_info.get('country') + '.json'
			else:
				path_results = path + 'results' + '_' + self.start_time_local + '_' + 'AS-' + ip_network_asn['asn_id'] + '.json'
		else: path_results = path + 'results' + '_' + self.start_time_local + '.json'
		if self.path_results_name: path_results = path_results.replace('.json', '_hosts_' + self.path_results_name + '.json')
		if self.job_done is False and self.continue_option and self.path_results_name is not None and self.hostnames_path_results:
			path_results = self.hostnames_path_results
		return path_results

	def __get_dump__(self, ip_network_asn):
		if self.get_dump:
			path_results = self.__get_path_results__(ip_network_asn = ip_network_asn) 
			#json.dump(self.recv_records, fp = open(path_results, 'w'), indent=4)
			json.dump(self.recv_records, fp = open(path_results, 'w'))
			if self.print_result: utility.print_green2("Results dumped:" + path_results)
			if self.say_result: utility.get_say('Results dumped')


	def __print_result_duration__(self, qname):
		if self.print_result:
			duration_seconds = time.time() - self.start_time
			duration = time.strftime("%H:%M:%S", time.gmtime(duration_seconds))
			utility.border_msg(utility.Clr.YELLOW2 + 'List ' + str(self.hostnames.index(qname)) + ' of ' + str(self.hostnames_len) + ' duration: ' + duration + utility.Clr.RST2 + ' ' + time.ctime())


	def __print_result_execution_time_Duration__(self, say_result = False):
		if self.print_result:
			duration_seconds = time.time() - self.start_time
			duration = time.strftime("%H:%M:%S", time.gmtime(duration_seconds))
			self.recv_records["parameters"]["execution_time_duration"] = str('{:.3f}'.format(duration_seconds))
			print("Duration:", duration)
		if self.say_result: utility.get_say("Dns hostnames advanced tests jobs done, time taken: " + duration)


if __name__ == '__main__':
	#Get_hostnames_testing = Advanced_testing(get_nslookup = True, get_ping = False, get_traceroute = False, get_ssl_check = False, get_dump = False, records = ["A", "CNAME"], nameserver = '1.1.1.1')
	import json

	# Get_hostnames_testing = Advanced_testing(get_nslookup = True, get_ping = True, get_traceroute = True, get_ssl_check = False, get_dump = False, records = ["A", "CNAME"], nameserver = ['1.1.1.1', '8.8.4.4'])
	Get_hostnames_testing = Advanced_testing(get_nslookup = True, get_ping = True, get_traceroute = True, get_ssl_check = False, get_dump = True, records = ["A", "CNAME"], nameserver = ['1.1.1.1', '8.8.4.4'])
	try:
		# print(Get_hostnames_testing.get_hostname_advanced_testing(hostnames = ['www.whitehouse.gov']))
		# 	'www.facebook.com',
		# 	# 'www.amzn.com',
		# 	# 'amazon.com',
		# 	# 'us2723.nordvpn.com',
		# 	# 'jp590.nordvpn.com',
		# 	# 'za110.nordvpn.com',
		# 	# 'fbi.gov',
		# 	# 'www.ic3.gov',
		# 	'ic3.gov'
		hostnames_testing = Get_hostnames_testing.get_hostname_advanced_testing(hostnames = [
			'ipv4.google.com',
			'216.218.228.119',
			'test-ipv6.com',
			'www.whitehouse.gov',
			'www.facebook.com',
			'www.amzn.com',
			'amazon.com',
			'us2723.nordvpn.com',
			'jp590.nordvpn.com',
			'za110.nordvpn.com',
			'fbi.gov',
			'www.ic3.gov',
			'ic3.gov'
		   ])
		print(json.dumps(hostnames_testing, indent=4))
		   # ])))
	except Exception as e:
		raise e
		print('KeyboardInterrupt')