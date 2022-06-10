#!/usr/bin/env python3
"""
Copyright 2022. All rights reserved.
"""
__version__ = "1.0"
import argparse
import main
class Cli_api:
	"""
	usage
	"""
	#def __init__(self):
	def get_result(self, args):
		if args.all:
			#print("get_hostnames")
			#print(args)
			#Get_hostnames_testing = main.Advanced_testing(get_nslookup = False, get_ping = False, get_traceroute = False, get_ssl_check = False, get_dump = True)
			Get_hostnames_testing = main.Advanced_testing(get_nslookup = True, get_ping = True, get_traceroute = True, get_ssl_check = True, get_dump = True)
			Get_hostnames_testing.get_hostname_advanced_testing(Get_hostnames_testing.__get_hostnames_as_list__())
		elif args.nordvpn:
			#print("get_hostnames_nordvpn")
			#print(args)
			Get_hostnames_testing_nordvpn = main.Advanced_testing(get_nslookup = True, get_ping = True, get_traceroute = True, get_ssl_check = False, records = ["A"], nameserver = "1.1.1.1", get_dump = True)
			Get_hostnames_testing_nordvpn.get_hostname_advanced_testing(Get_hostnames_testing_nordvpn.__get_hostnames_nordvpn_as_list__())
		elif args.nordvpn:
			print("get_hostnames_nordvpn")
			print(args)
		elif args.facebook:
			print("get_hostnames_facebook")
			print(args)
		elif args.linkedin:
			print("get_hostnames_linkedin")
			print(args)
		elif args.wikipedia:
			print("get_hostnames_wikipedia")
			print(args)
		elif args.yahoo:
			print("get_hostnames_yahoo")
			print(args)
		elif args.hosts:
			print("get_hostnames_hosts")
			print(args)
		elif args.google:
			print("get_hostnames_google")
			print(args)
		elif args.apple:
			print("get_hostnames_apple")
			print(args)
		elif args.amazon:
			print("get_hostnames_amazon")
			#print(args)
			Get_hostnames_testing = main.Advanced_testing(get_nslookup = True, get_ping = True, get_traceroute = True, get_ssl_check = True, get_dump = True)
			Get_hostnames_testing.get_hostname_advanced_testing(Get_hostnames_testing.__get_hostnames_amazon_2_as_list__())
		
	def get_args(self, args = {}):
		self.parser = argparse.ArgumentParser(add_help = True, description = "Collect of useful command for OpenSSL create certificate:")
		group = self.parser.add_mutually_exclusive_group(required = True)
		group.add_argument("-a", "--all", dest = "all", action = "store_true", help = "Advanced testing all hostnames get nslookup check, get ping check, get traceroute check, get SSL certificate check. Hostnames : Facebook, Bing, Linkedin, Wikipedia, Yahoo, hosts, Google, Apple, Amazon")
		group.add_argument("-n", "--nordvpn", dest = "nordvpn", action = "store_true", help = "Advanced testing nordvpn hostnames get nslookup check, get ping check, get traceroute check.")
		group.add_argument("-F", "--facebook", dest = "facebook", action = "store_true", help = "Advanced testing Facebook hostnames get nslookup check, get ping check, get traceroute check, get SSL certificate check.")
		group.add_argument("-B", "--bing", dest = "bing", action = "store_true", help = "Advanced testing Bing hostnames get nslookup check, get ping check, get traceroute check, get SSL certificate check.")
		group.add_argument("-L", "--linkedin", dest = "linkedin", action = "store_true", help = "Advanced testing Linkedin hostnames get nslookup check, get ping check, get traceroute check, get SSL certificate check.")
		group.add_argument("-W", "--wikipedia", dest = "wikipedia", action = "store_true", help = "Advanced testing Wikipedia hostnames get nslookup check, get ping check, get traceroute check, get SSL certificate check.")
		group.add_argument("-Y", "--yahoo", dest = "yahoo", action = "store_true", help = "Advanced testing Yahoo hostnames get nslookup check, get ping check, get traceroute check, get SSL certificate check.")
		group.add_argument("-H", "--hosts", dest = "hosts", action = "store_true", help = "Advanced testing Hosts hostnames get nslookup check, get ping check, get traceroute check, get SSL certificate check.")
		group.add_argument("-G", "--google", dest = "google", action = "store_true", help = "Advanced testing Google hostnames get nslookup check, get ping check, get traceroute check, get SSL certificate check.")
		group.add_argument("-A", "--apple", dest = "apple", action = "store_true", help = "Advanced testing Apple hostnames get nslookup check, get ping check, get traceroute check, get SSL certificate check.")
		group.add_argument("-AM", "--amazon", dest = "amazon", action = "store_true", help = "Advanced testing Amazon hostnames get nslookup check, get ping check, get traceroute check, get SSL certificate check.")
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