#!/usr/bin/env python3
"""
Copyright 2022. All rights reserved.
"""
__version__ = "1.2"
import argparse
import main
import os
import pathlib
import utilities.file as file
File = file.Main(print_result = False)
class Cli_api:
	"""
	usage
	"""
	#def __init__(self):
	def get_result(self, args):
		if args.services:
			hosts_list = []
			Get_hostnames_testing = main.Advanced_testing(get_nslookup = True, get_ping = True, get_traceroute = True, get_ssl_check = True, get_dump = True, path_results_name = "all")
			for hosts in list(pathlib.Path('./hosts/services/').rglob('*.txt')): hosts_list.extend([host.rstrip() for host in open(hosts, 'r').readlines()])
			Get_hostnames_testing.get_hostname_advanced_testing(hosts_list)
		elif args.nordvpn:
			hosts_list = []
			Get_hostnames_testing_nordvpn = main.Advanced_testing(get_nslookup = True, get_ping = True, get_traceroute = True, get_ssl_check = False, records = ["A"], nameserver = "1.1.1.1", get_dump = True, path_results_name = "nordvpn")
			for servers_list in ["servers_dedicated", "servers_obfuscated", "servers_p2p", "servers_double", "servers_onion", "servers_standard"]:
				hosts_list.extend([host.rstrip() for host in (File.get_request_text_as_str("https://raw.githubusercontent.com/babyish-retired0m/hostname_advanced_testing/main/hosts/nordvpn/" + servers_list + ".txt"))])
			Get_hostnames_testing_nordvpn.get_hostname_advanced_testing(hosts_list)
		elif args.google:
			hosts_list = []
			for servers_list in pathlib.Path("./hosts/google").rglob("*.txt"):
				hosts_list.extend([x.rstrip() for x in open(servers_list,'r').readlines()]) 
			Get_hostnames_testing = main.Advanced_testing(get_nslookup = True, get_ping = True, get_traceroute = True, get_ssl_check = False, get_dump = True, path_results_name = "google")
			Get_hostnames_testing.get_hostname_advanced_testing(hosts_list)
		elif args.hosts:
			hosts_PATH = './hosts/services/hosts.txt'
			if os.path.isfile(hosts_PATH):
				Get_hostnames_testing = main.Advanced_testing(get_nslookup = True, get_ping = True, get_traceroute = True, get_ssl_check = False, get_dump = True, path_results_name = "facebook.com")
				Get_hostnames_testing.get_hostname_advanced_testing([host.rstrip() for host in open(hosts_PATH, 'r').readlines()])
		elif args.apple:
			hosts_PATH = './hosts/services/hosts_apple.txt'
			if os.path.isfile(hosts_PATH):
				Get_hostnames_testing = main.Advanced_testing(get_nslookup = True, get_ping = True, get_traceroute = True, get_ssl_check = True, get_dump = True, path_results_name = "googlevideo.com")
				Get_hostnames_testing.get_hostname_advanced_testing([host.rstrip() for host in open(hosts_PATH, 'r').readlines()])
		elif args.amazon:
			hosts_PATH = './hosts/services/hosts_amazon.com_all.txt'
			if os.path.isfile(hosts_PATH):
				Get_hostnames_testing = main.Advanced_testing(get_nslookup = True, get_ping = True, get_traceroute = True, get_ssl_check = False, get_dump = True, path_results_name = "amazon.com_all")
				Get_hostnames_testing.get_hostname_advanced_testing([host.rstrip() for host in open(hosts_PATH, 'r').readlines()])
	def get_args(self, args = {}):
		self.parser = argparse.ArgumentParser(add_help = True, description = "Collect of useful command for OpenSSL create certificate:")
		group = self.parser.add_mutually_exclusive_group(required = True)
		#group.add_argument("-a", "--all", dest = "all", action = "store_true", help = "Advanced testing all hostnames get nslookup check, get ping check, get traceroute check, get SSL certificate check. Hostnames : Facebook, Bing, Linkedin, Wikipedia, Yahoo, hosts, Google, Apple, Amazon")
		group.add_argument("-s", "--services", dest = "services", action = "store_true", help = "Advanced testing services hostnames get nslookup check, get ping check, get traceroute check, get SSL certificate check.")
		group.add_argument("-n", "--nordvpn", dest = "nordvpn", action = "store_true", help = "Advanced testing nordvpn hostnames get nslookup check, get ping check, get traceroute check.")
		group.add_argument("-g", "--google", dest = "google", action = "store_true", help = "Advanced testing Google hostnames get nslookup check, get ping check, get traceroute check, get SSL certificate check.")
		group.add_argument("-H", "--hosts", dest = "hosts", action = "store_true", help = "Advanced testing hosts hostnames get nslookup check, get ping check, get traceroute check, get SSL certificate check.")
		group.add_argument("-a", "--apple", dest = "apple", action = "store_true", help = "Advanced testing Apple hostnames get nslookup check, get ping check, get traceroute check, get SSL certificate check.")
		group.add_argument("-A", "--amazon", dest = "amazon", action = "store_true", help = "Advanced testing Amazon hostnames get nslookup check, get ping check, get traceroute check, get SSL certificate check.")
		group.add_argument("-v", "--version", action = "version", version = "%(prog)s version: " + __version__)
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