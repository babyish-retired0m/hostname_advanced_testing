#!/usr/bin/env python3
__version__ = "3.8"
"""
3.8
hostnames_start()
3.7
add check status on incompleted testing
3.6
__name__ == '__main__'
nordvpn_servers.py
3.5
get_hostname_advanced_testing().hostnames_start_index
3.4
__get_ip_public__.ip_network_asn()
3.3
self.ip_network_asn
3.2
# timeout= 0.01 -> 0.04 -> 0.5(default 5 sec.)
__get_traceroute__.traceroute.verbose_traceroute(timeout=0.02)
3.1
self.can_not_be_ssl_check_path
write_text_as_json self.can_not_be_ssl_check
self.can_not_be_resolve
write_text_as_json self.can_not_be_resolve

"""
import utilities.dns_resolve as dns_resolve
import utilities.ping as ping
import utilities.traceroute as traceroute
import utilities.ssl_check as ssl_check
import utilities.ip_address as ip_address
import utilities.utility as utility
import utilities.file as file
import time
import os
import json
import sys
import pathlib


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
			# self.recv_records = {"parameters" : {"Unix Epoch Time" : utility.get_time_unix(), 'timezone':'UTC'}}
			self.recv_records = {"parameters" : {"Unix Epoch Time" : utility.get_time_unix(), 'timezone':'UTC', 'time': time.ctime(), 'continue': False, 'continuing chellanges': []}}

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

		
		# self.hostnames_start_index = 0 if hostnames_start_index is None else int(hostnames_start_index)
	"""def __call__(self):
		return self.__get_hostname_advanced_testing__()"""
	def __check_is_result_file_status_completed__(self, last_file_json_length, hosts_list_length):
			# file_dict = hosts_list.index(last_file_json[last_file_json_length:])
			# if last_file_json_length == hosts_list_length or last_file_json_length >= hosts_list_length: status_completed_flag = True
			if self.print_result: 
				print('__check_is_result_file_status_completed__().last_file_json_length', last_file_json_length)
				print('__check_is_result_file_status_completed__().hosts_list_length', hosts_list_length)
			if last_file_json_length >= hosts_list_length: status_completed_flag = True
			else: status_completed_flag = False
			return status_completed_flag


	def get_hostnames_start_index(self):
	# def check_result_file_status(self):

		dir_files_list = File.dir_listing_files_in_this_directory_tree(path = self.parent_dir + '/' + 'results', file_extension = 'json')
		pattern_asn = r'(_network_AS-)(\d+)(_\w+)'
		pattern_host = r'(_hosts_)(\w+[a-z])(\.json$)'
		pattern_result_files_list = []
		pattern_result_files_host_list = []
		pattern_result_files_asn_list = []

		self.__get_ip_public__()
		
		#fulfilling pattern_result_files_host_list
		for file_path in dir_files_list:
			file_parent = file_path.parent
			file_name = file_path.name
			# find
			result_asn = re.search(r'^results_(?P<date>\d*\-\d*\-\d*)_(?P<time>\d*\-\d*-\d*)_network_AS-(?P<as>\d+)_(?P<asn>\w+)_hosts_(?P<host>\w+[a-z])\.json$', file_name)
			result_host = re.search(r'^results_(?P<date>\d*\-\d*\-\d*)_(?P<time>\d*\-\d*-\d*)_hosts_(?P<host>\w+[a-z])\.json$', file_name)

			if result_asn:
				if self.ip_network_asn:
					if int(result_asn['as']) == int(self.ip_network_asn['asn_id']) and result_asn['host'] == self.path_results_name:
						pattern_result_files_asn_list.append(str(file_path))
				elif result_asn['host'] == self.path_results_name:
					pattern_result_files_asn_list.append(str(file_path))
			elif result_host:
				if result_host['host'] == self.path_results_name:
					pattern_result_files_host_list.append(str(file_path))
		
		
		def get_last_file_path(files_list):
			if len(files_list) > 0:
				last_file_path = list(reversed(files_list))[0]
				if self.print_result: print('Advanced_testing.get_last_file_path().last_file_path)', last_file_path)
				if File.check_is_file_updated(path = last_file_path, days_ago = 3) is False:
					print('Advanced_testing.get_last_file_path().check_is_file_updated()', last_file_path)
					return last_file_path
		

		def check_file_status_complete(last_file_json):
			if self.__check_is_result_file_status_completed__(last_file_json_length = len(last_file_json['advanced_test']) + len(list(x for x in self.can_not_be_resolve if x in self.hostnames)), hosts_list_length = len(self.hostnames)):
				if self.print_result: print('result file status completed', last_file_json['parameters'])
				return True
			else:
				if self.print_result: print('result file status not completed', last_file_json['parameters'])
				return False


		def get_fulfilling_hostnames_start_dict(last_file_path):
			# get_hostnames_start_dict()
			if self.print_result: print('Advanced_testing.get_fulfilling_hostnames_start_dict.last_file_path', last_file_path)
			last_file_json = File.open_json(last_file_path)
			if self.print_result: print(self.hostnames[1])
			if self.print_result: print(list(last_file_json['advanced_test'])[1])
			hostnames_original_sorted_list = sorted(self.hostnames)
			hostnames_last_sorted_list = sorted(last_file_json['advanced_test'])
			hostnames_new_list = []
			if self.print_result: print('hostnames_original_sorted_list length', len(hostnames_original_sorted_list))
			if self.print_result: print('hostnames_last_sorted_list length', len(hostnames_last_sorted_list))
			for hostname in hostnames_original_sorted_list:
				if hostname not in hostnames_last_sorted_list and hostname not in hostnames_new_list:
					hostnames_new_list.append(hostname)
			hostnames_new_list.sort()
			print('hostnames_new_list length', len(hostnames_new_list))
			if check_file_status_complete(last_file_json) is False:
				# return {'hostnames_start_index': self.hostnames.index(list(last_file_json['advanced_test'])[-1:][0]), 'last_file_path_results': last_file_path, 'job_done': False, 'last_file_json': last_file_json}
				return {'hostnames_start_index': 0, 'last_file_path_results': last_file_path, 'job_done': False, 'last_file_json': last_file_json, 'hostnames_new_sorted_list': hostnames_new_list}
		

		last_file_asn_path = get_last_file_path(files_list = pattern_result_files_asn_list)
		last_file_host_path = get_last_file_path(files_list = pattern_result_files_host_list)
		# def robotparser():

		hostnames_start_dict = None
		
		if last_file_asn_path:
			hostnames_start_dict = get_fulfilling_hostnames_start_dict(last_file_asn_path)
			if hostnames_start_dict: return hostnames_start_dict
		elif last_file_host_path or hostnames_start_dict:
			if last_file_host_path:
				hostnames_start_dict = get_fulfilling_hostnames_start_dict(last_file_host_path)
				if hostnames_start_dict: return hostnames_start_dict
			else:
				hostnames_start_dict = {'hostnames_start_index': 0, 'last_file_path_results': None, 'job_done': True, 'last_file_json': {}}
		return hostnames_start_dict

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


	def __get_ip_public__(self):
		def __get_ip_address_check__():
			self.ip_address_checked = "176.36.0.0/14" if ip_address.check_ip_in_network_lanet_ua(self.ip_address_public) else self.ip_address_public
		self.ip_address_public = ip_address.get_ip_address_public_amazon(tries = 100, timeout_sleep = 10)
		__get_ip_address_check__()
		self.recv_records['parameters']["Public IP Address"] = self.ip_address_checked
		# ip_network_asn
		self.ip_network_asn = ip_address.get_ip_in_networks(ip_address_public = self.ip_address_public, print_result = self.print_result)
		if 'asn_website' in self.ip_network_asn: del self.ip_network_asn['asn_website']
		if 'asn_file_name' in self.ip_network_asn: del self.ip_network_asn['asn_file_name']
		if 'asn_ip_address_subnet' in self.ip_network_asn: del self.ip_network_asn['asn_ip_address_subnet']
		# if isinstance(self.ip_network_asn, dict):
		# 	print(self.ip_network_asn)
		# 	self.recv_records['parameters']['ASN'] = self.ip_network_asn
		# 	# self.recv_records['parameters']['ASN'] = {'asn_id ': self.ip_network_asn['asn_id'],
		# 	# 			'asn_name': self.ip_network_asn['asn_name'],
		# 	# 			'asn_website': self.ip_network_asn['asn_website'],
		# 	# 			'asn_filename': self.ip_network_asn['asn_file_name']}
		# else:
		# 	self.recv_records['parameters']['ASN'] = self.ip_network_asn
		self.recv_records['parameters']['ASN'] = self.ip_network_asn
		# print('Advanced_testing.__get_ip_public__().self.ip_network_asn', self.ip_network_asn)
		
		
	def __get_nslookup__(self, qname):
		asn = self.ip_network_asn.get('asn_name') if isinstance(self.ip_network_asn, dict) else None
		Response = dns_resolve.Dns_response(host = qname, records = self.records, nameserver = self.nameserver, ip_address_public_answer = self.ip_address_public, asn = asn)
		result = Response.get_nslookup()
		recv_records = {"resolve":{"nslookup":result[qname]}}
		recv_records["resolve"]["parameters"] = {'Unix Epoch Time': utility.get_time_unix(),
												'timezone':'UTC',
												'Public IP Address': self.ip_address_checked,
												'pcname': utility.get_pcname(),
												'username': utility.get_username(),
												'currentdirectory': utility.get_currentdirectory(),
												'ASN': self.ip_network_asn,
												'continuing chellanges': []}
		return recv_records["resolve"]


	def __get_ping__(self, qname):
		result = ping.verbose_ping(address = qname, ip_address_resolved = self.ip_address_resolved)
		if result is not None:
			recv_records = {'verbose_ping':result[qname]}
			recv_records['verbose_ping']['parameters']['Unix Epoch Time'] = utility.get_time_unix()
			recv_records['verbose_ping']['parameters']['Public IP Address'] = self.ip_address_checked
			recv_records['verbose_ping']['parameters']['ASN'] = self.ip_network_asn
			return recv_records["verbose_ping"]


	def __get_traceroute__(self, qname):
		result = traceroute.verbose_traceroute(address = qname, ip_address_resolved = self.ip_address_resolved, interval=0.05, timeout=0.01)# timeout 0.1 -> 0.01
		if result is not None:
			recv_records = {'verbose_traceroute':result[qname]}
			recv_records['verbose_traceroute']['parameters']['Unix Epoch Time'] = utility.get_time_unix()
			recv_records['verbose_traceroute']['parameters']['Public IP Address'] = self.ip_address_checked
			recv_records['verbose_traceroute']['parameters']['ASN'] = self.ip_network_asn
			return recv_records['verbose_traceroute']


	def __get_ssl_check__(self, qname):
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
		# self.hostnames = hostnames
		self.hostnames_start_index = 0
		self.job_done = False
		self.start_time = time.time()
		self.recv_records["advanced_test"] = {}
		if isinstance(hostnames, str): self.hostnames = [hostnames]
		elif isinstance(hostnames, list): self.hostnames = hostnames
		else: print("Are list of hostname(s) str, list?"); sys.exit(1)
		# print('get_hostname_advanced_testing().self.hostnames_len', len(self.hostnames))
		

		# hostnames_start = check_hostnames_start_index()
		if self.path_results_name is not None:
			if self.continue_option:
				# self.start_job_dict = self.continue_option()
				self.start_job_dict = self.get_hostnames_start_index()
				# if self.print_result: print('get_hostname_advanced_testing().self.start_job_dict[0]', self.start_job_dict['last_file_path_results'])
				if self.start_job_dict:
					self.hostnames_start_index = self.start_job_dict['hostnames_start_index']
					self.hostnames_path_results = self.start_job_dict['last_file_path_results']
					self.job_done = self.start_job_dict['job_done']
					if len(self.start_job_dict['last_file_json'])>0: self.recv_records = self.start_job_dict['last_file_json']
					# print('self.start_job_dict["last_file_json"]', self.start_job_dict['last_file_json'])
					# print('get_hostname_advanced_testing().check_hostnames_start_index().self.hostnames_len', len(self.hostnames))
					if self.start_job_dict['job_done']: 
						recv_records['parameters']['continue'] = self.start_job_dict['job_done']
						recv_records['parameters']['continuing chellanges'].append({'Unix Epoch Time' : utility.get_time_unix(), 'timezone':'UTC', 'time': time.ctime(), 'Public IP Address': self.ip_address_checked, 'ASN': self.ip_network_asn})
					if 'hostnames_new_sorted_list' in self.start_job_dict and len(self.start_job_dict['hostnames_new_sorted_list']) > 0 :
						self.hostnames = self.start_job_dict['hostnames_new_sorted_list']


		
		# if self.hostnames_start_index is not None: self.hostnames = self.hostnames[self.hostnames_start_index:]
		# print('get_hostname_advanced_testing().self.hostnames', self.hostnames)
		# print('get_hostname_advanced_testing().self.hostnames self.hostnames_start_index', self.hostnames_start_index)
		self.hostnames = self.hostnames[self.hostnames_start_index:]
		# print('get_hostname_advanced_testing().self.hostnames', self.hostnames)
		self.hostnames_len = len(self.hostnames)
		# print('get_hostname_advanced_testing().self.hostnames_len', self.hostnames_len)
		if self.hostnames_len > 1000: self.k = 100 # 100 -> 10
			# if self.hostnames_len % 2 == 0: self.k = 100
			# else: self.k = 50
		else: self.k = 200 # 200 -> 20
			# if self.hostnames_len % 2 == 0: self.k = 200
			# else: self.k = 150

		for enum, qname in enumerate(self.hostnames):
			start_time_advanced_test = time.time()
			self.__get_ip_public__()
			if len(qname)>3 and qname not in self.can_not_be_resolve and self.__get_ip_address_resolved__(qname):

				self.recv_records['advanced_test'][qname] = {}
				print('\n\n')
				utility.print_yellow2('advanced_test start ' + time.strftime("%H:%M:%S", time.gmtime(start_time_advanced_test)))
				utility.print_percents(self.hostnames.index(qname), self.hostnames_len)

				#nslookup
				if self.get_nslookup:
					print('\n\n')
					utility.print_yellow2('NS LOOK UP testing ' + qname)
					self.recv_records["advanced_test"][qname]["resolve"] = self.__get_nslookup__(qname)

				#ping
				if self.get_ping:
					print('\n\n')
					utility.print_yellow2('Ping testing' + qname)
					self.recv_records["advanced_test"][qname]["verbose_ping"] = self.__get_ping__(qname)

				#traceroute
				if self.get_traceroute:
					print('\n\n')
					utility.print_yellow2('Traceroute to ' + qname + ' testing')
					self.recv_records["advanced_test"][qname]["verbose_traceroute"] = self.__get_traceroute__(qname)

				#ssl_check
				if self.get_ssl_check:
					print('\n\n')
					utility.print_yellow2('SSL check testing')
					self.recv_records["advanced_test"][qname]["ssl_cert_info"] = self.__get_ssl_check__(qname)

			if self.hostnames.index(qname) > 0:
				if self.hostnames.index(qname) % self.k == 0: self.__get_dump__()
				self.__print_result_duration__(qname)
		self.__print_result_execution_time_Duration__()
		self.__get_dump__()

		return self.recv_records


	def __get_path_results__(self):
		path = self.parent_dir + "/results/"
		if File.check_dir(path) is False: File.dirs_make(path)
		if self.ip_network_asn: path_results = path + 'results_' + self.start_time_local + '_network_' + 'AS-' + self.ip_network_asn['asn_id'] + '_' + self.ip_network_asn['asn_name'] + '.json'
		else: path_results = path + 'results_' + self.start_time_local + '.json'
		if self.path_results_name: path_results = path_results.replace('.json', '_hosts_' + self.path_results_name + '.json')
		if self.job_done is False and self.continue_option and self.path_results_name is not None and self.hostnames_path_results:
			path_results = self.hostnames_path_results
		return path_results

	def __get_dump__(self):
		if self.get_dump:
			path_results = self.__get_path_results__() 
			json.dump(self.recv_records, fp = open(path_results, 'w'), indent=4)
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
			self.recv_records["parameters"]["Execution time Duration"] = str('{:.3f}'.format(duration_seconds))
			print("Duration:", duration)
		if self.say_result: utility.get_say("Dns hostnames advanced tests jobs done, time taken: " + duration)
	

	


	



if __name__ == '__main__':
	#Get_hostnames_testing = Advanced_testing(get_nslookup = True, get_ping = False, get_traceroute = False, get_ssl_check = False, get_dump = False, records = ["A", "CNAME"], nameserver = '1.1.1.1')
	import json

	Get_hostnames_testing = Advanced_testing(get_nslookup = True, get_ping = True, get_traceroute = True, get_ssl_check = False, get_dump = False, records = ["A", "CNAME"], nameserver = ['1.1.1.1', '8.8.4.4'])
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
		hostnames_testing = Get_hostnames_testing.get_hostname_advanced_testing(hostnames = ['www.whitehouse.gov',
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
		print(json.dumps(hostnames_testing), indent=4)
		   # ])))


		


	except Exception as e:
		raise e
		print('KeyboardInterrupt')