#!/usr/bin/env python3
"""
Copyright 2022. All rights reserved.
"""
__version__ = "1.4"
"""
1.5
servers_recent_list
subdirectories_list - servers_categories_types_dict
1.4
get_result().args.nordvpn.
1.3
get_args().hostnames_start_index
"""
import argparse
import main
import os
import pathlib
import utilities.file as file
File = file.Main(print_result = False)
import re
import json
import datetime #is_test_file_updated()
class Cli_api:
	"""
	usage
	"""
	#def __init__(self):

	# subdirectories_list = File.dir_listing_subdirectories(path = self.parent_dir + '/hosts')
		# for dir_name in subdirectories_list:
		# 	if dir_name == self.path_results_name:
		# 		dir_files_list = Files.dir_listing_files_in_this_directory_tree(path = self.parent_dir + '/' + dir_name, file_extension = 'json')


	def get_result(self, args):
		if args.services:
			hosts_list = []
			Get_hostnames_testing = main.Advanced_testing(get_nslookup = True, get_ping = True, get_traceroute = True, get_ssl_check = True, get_dump = True, path_results_name = "all", 
				continue_option = True,
				# pre_party_check = True,
				)
			for hosts in list(pathlib.Path('./hosts/services/').rglob('*.txt')): hosts_list.extend([host.rstrip() for host in open(hosts, 'r').readlines()])
			Get_hostnames_testing.get_hostname_advanced_testing(hosts_list)
		

		elif args.nordvpn:
			def __get_testing__(hosts_list):
				# Solution 1
				# hosts_list = []
				Get_hostnames_testing_nordvpn = main.Advanced_testing(get_nslookup = True, get_ping = True, get_traceroute = True, get_ssl_check = False, records = ["A"], nameserver = "1.1.1.1", get_dump = True, path_results_name = "nordvpn", 
					continue_option = True,
					#pre_party_check = True,
					)
				# for servers_list in ["servers_dedicated", "servers_obfuscated", "servers_p2p", "servers_double", "servers_onion", "servers_standard"]:
				# 	hosts_list.extend([host.rstrip() for host in (File.get_request_text_as_str("https://raw.githubusercontent.com/babyish-retired0m/hostname_advanced_testing/main/hosts/nordvpn/" + servers_list + ".txt"))])
				Get_hostnames_testing_nordvpn.get_hostname_advanced_testing(hosts_list)

			# Solution 2
			def get_test_result_dict(self, update_check = True):
				servers_categories_types_dict = {'Standard': 'Standard VPN servers', 'Dedicated': 'Dedicated IP', 'Obfuscated': 'Obfuscated Servers', 'Double': 'Double VPN', 'Onion': 'Onion Over VPN'}
				path_results = pathlib.Path('/src/app/hostname_advanced_testing/results')

				
				def get_the_last_tested_file():
					files_result_list = list(map(lambda x: x if re.search(r'hosts_nordvpn', x.name.lower()) else None, (x for x in pathlib.Path(path_results).glob('**/*.'+'json'))))
					files_list = []
					for i in files_result_list:
						if i is not None:
							files_list.append(i)
					files_list.reverse()
					return files_list[0]
				

				# data_meta
				
				def is_test_file_updated(TEST_PATH = None):
					if TEST_PATH is None: TEST_PATH = path_results.joinpath('results_2022-11-06_12-36-21_hosts_nordvpn.json')
					if os.path.isfile(TEST_PATH):
					    month_ago = datetime.datetime.now() - datetime.timedelta(30)
					    # modification_date = datetime.datetime.fromtimestamp(os.path.getmtime(TEST_PATH))
					    modification_date = datetime.datetime.fromtimestamp(pathlib.Path(TEST_PATH).stat().st_mtime)
					    need_update_flag = month_ago > modification_date
					    if need_update_flag: 
					    	print("** The test result data file hasn't been update in the last month", file = sys.stderr)
					else:
					    print("** There is no test result data file", file = sys.stderr)
					    need_update_flag = True
					return need_update_flag
				
				#get_file_tested()
				#last_tested_file = get_the_last_tested_file()
				last_tested_file = File.get_last_file(path_dir = path_results, file_extension = 'json')
				if update_check and is_test_file_updated(last_tested_file):
					test_result_dict = self.get_testing(servers_domain_list)
				else: 
					test_result_dict = File.open_json(last_tested_file)#File.get_request_text_as_json
				return test_result_dict

			def get_servers_recent_list(category = None):
				import hosts.nordvpn.servers_nordvpn as hosts_nordvpn
				NordVPN = hosts_nordvpn.Servers_NordVPN()
				servers_domain_list = NordVPN.get_servers_domain_list(category = category)
				print('Cli_api get_servers_recent_list', servers_domain_list)
				print('servers_domain_list length', len(servers_domain_list))
				return servers_domain_list

				
			def check_test_result():
				hostnames_checked_list = []
				recv_records = get_test_result_dict()
				hostnames_nordvpn_dict = get_servers_recent_list()
				records = "A"
				nameserver = '1.1.1.1'

				for host in hostnames_nordvpn_dict:
					# if hostnames_nordvpn_dict[host]['domain'] == recv_records[host]:
					print(host['ip_address'])
					print(recv_records)
					print(recv_records[host])
					print(recv_records[host]['resolve'])
					print(recv_records[host]['resolve']['nslookup'])
					print(recv_records[host]['resolve']['nslookup'][nameserver])
					print(recv_records[host]['resolve']['nslookup'][nameserver][records])
					if host['ip_address'] not in recv_records[host]['resolve']['nslookup'][nameserver][records]:
						print('Error', hostnames_nordvpn_dict[host]['domain'], hostnames_nordvpn_dict[host]['ip_address'], '!=', recv_records[host]['resolve']['nslookup'][nameserver][records])
						hostnames_checked_list.append(host)

				return hostnames_checked_list

			__get_testing__(hosts_list = get_servers_recent_list())## Solution 1

			### print('servers_recent_list', servers_categories_types_dict['Standard'], get_servers_recent_list(category = servers_categories_types_dict['Standard']))

			### hostnames_checked_list = check_test_result()

			# print(json.dumps(recv_records, indent=4))

			
			# for host in hosts:
			# 	hostnames_nordvpn_list.append(host['domain'])

			# recv_records = Get_hostnames_testing.get_hostname_advanced_testing(hostnames = hostnames_nordvpn_dict, get_ssl_check = False, records = records, nameserver = nameserver, get_nslookup = True, get_ping = True, get_traceroute = True, path_results_name = 'nordvpn')
			

			### files_result_list = list(map(lambda x: x if re.search(r'hosts_nordvpn', x) else None, ((x.name).lower() for x in pathlib.Path('/src/app/hostname_advanced_testing/results').glob('**/*.' + 'json'))))
			
			# files_result_list = list(map(lambda x: x if re.search(r'hosts_nordvpn', x) else None, (x for x in pathlib.Path('/src/app/hostname_advanced_testing/results').glob('**/*.'+'json'))))
	

			# p = listing_results = File.dir_listing_files_in_this_directory_tree(path = os.path.dirname(__file__) + "/results", file_extension="json")
			
			### p = pathlib.Path('/src/app/hostname_advanced_testing/results')
			### files_result_list = list(map(lambda x: x if re.search(r'hosts_nordvpn', x) else None, ((x.name).lower() for x in pathlib.Path('/src/app/hostname_advanced_testing/results').glob('**/*.'+'json'))))
			### f = list(map(lambda x: x if re.search(r'hosts_nordvpn', x) else None, ((x.name).lower() for x in pathlib.Path('/src/app/hostname_advanced_testing/results').glob('**/*.'+'json'))))
			### f = list(map(lambda x: x if re.search(r'hosts_nordvpn', x.name.lower()) else None, (x for x in pathlib.Path('/src/app/hostname_advanced_testing/results').glob('**/*.'+'json'))))
			
			# list(map((lambda x: print(x)),f)
			# (lambda f: [print(x) for x in f])(f)



			# print(list(p.glob('**/*.' + 'json')))
			


			# files_names = [x.name for x in p.glob('**/*.' + 'json')]
			# def files_names_search(files_list):
			# 	result_list = []
			# 	for file in files_list:
			# 		result = re.search(r'hosts_nordvpn', files_list)
			# 		result_list.append(result.group(0))
			# 	return result.group(0)
			# # print(list(map(lambda x: re.search(r'hosts_nordvpn', x), ((x.name).lower() for x in p.glob('**/*.'+'json').group(0)))))
			# result = re.findall(r'(?P<asn>\d+)\_(?P<website>.*?)\.txt', file_name.lower())


		elif args.google:
			hosts_list = []
			for servers_list in pathlib.Path("./hosts/google").rglob("*.txt"):
				hosts_list.extend([x.rstrip() for x in open(servers_list,'r').readlines()]) 
			Get_hostnames_testing = main.Advanced_testing(get_nslookup = True, get_ping = True, get_traceroute = True, get_ssl_check = False, get_dump = True, records = ["A", "AAAA", "CNAME"], path_results_name = "google",
				continue_option = True,
				)
			Get_hostnames_testing.get_hostname_advanced_testing(hosts_list)
		

		elif args.hosts:
			hosts_PATH = './hosts/services/hosts.txt'
			if os.path.isfile(hosts_PATH):
				Get_hostnames_testing = main.Advanced_testing(get_nslookup = True, get_ping = True, get_traceroute = True, get_ssl_check = False, get_dump = True)
				Get_hostnames_testing.get_hostname_advanced_testing([host.rstrip() for host in open(hosts_PATH, 'r').readlines()])
		

		elif args.apple:
			hosts_PATH = './hosts/services/hosts_apple.txt'
			if os.path.isfile(hosts_PATH):
				Get_hostnames_testing = main.Advanced_testing(get_nslookup = True, get_ping = True, get_traceroute = True, get_ssl_check = True, get_dump = True, path_results_name = "apple")
				Get_hostnames_testing.get_hostname_advanced_testing([host.rstrip() for host in open(hosts_PATH, 'r').readlines()])
		

		elif args.amazon:
			hosts_PATH = './hosts/hosts_amazon.com_all.txt'
			#if os.path.isfile(hosts_PATH):
			Get_hostnames_testing = main.Advanced_testing(get_nslookup = True, get_ping = True, get_traceroute = True, get_ssl_check = False, get_dump = True, path_results_name = "amazon_all",
				continue_option = True,
				)
			Get_hostnames_testing.get_hostname_advanced_testing([host.rstrip() for host in open(hosts_PATH, 'r').readlines()])
	

	def get_args(self, args = {}):
		self.parser = argparse.ArgumentParser(add_help = True, description = "Collect of useful command for OpenSSL create certificate:")
		group = self.parser.add_mutually_exclusive_group(required = True)
		# group = self.parser.add_argument_group('group1', 'group1 description')
		#group.add_argument("-a", "--all", dest = "all", action = "store_true", help = "Advanced testing all hostnames get nslookup check, get ping check, get traceroute check, get SSL certificate check. Hostnames : Facebook, Bing, Linkedin, Wikipedia, Yahoo, hosts, Google, Apple, Amazon")
		group.add_argument("-s", "--services", dest = "services", action = "store_true", help = "Advanced testing services hostnames get nslookup check, get ping check, get traceroute check, get SSL certificate check.")
		group.add_argument("-n", "--nordvpn", dest = "nordvpn", action = "store_true", help = "Advanced testing nordvpn hostnames get nslookup check, get ping check, get traceroute check.")
		group.add_argument("-g", "--google", dest = "google", action = "store_true", help = "Advanced testing Google hostnames get nslookup check, get ping check, get traceroute check, get SSL certificate check.")
		group.add_argument("-H", "--hosts", dest = "hosts", action = "store_true", help = "Advanced testing hosts hostnames get nslookup check, get ping check, get traceroute check, get SSL certificate check.")
		group.add_argument("-a", "--apple", dest = "apple", action = "store_true", help = "Advanced testing Apple hostnames get nslookup check, get ping check, get traceroute check, get SSL certificate check.")
		group.add_argument("-A", "--amazon", dest = "amazon", action = "store_true", help = "Advanced testing Amazon hostnames get nslookup check, get ping check, get traceroute check, get SSL certificate check.")
		group.add_argument("-v", "--version", action = "version", version = "%(prog)s version: " + __version__)
		# group.add_argument('-start', dest = 'hostnames_start_index', default = 0)
		args = self.parser.parse_args()
		return args
if __name__ == '__main__':
	import start_main_api
	import sys
	try:
		Advanced_test_cli_api = Cli_api()
		Advanced_test_cli_api.get_result(Advanced_test_cli_api.get_args(args = {}))
	except KeyboardInterrupt:
		print("{}Canceling script...{}\n".format("\033[33m", "\033[39m"))
		sys.exit(1)