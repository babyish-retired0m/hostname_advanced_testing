#!/usr/bin/env python3
"""
Copyright 2022. All rights reserved.
"""
__version__ = "1.1"
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
		if args.all:
			Get_hostnames_testing = main.Advanced_testing(get_nslookup = True, get_ping = True, get_traceroute = True, get_ssl_check = True, get_dump = True)
			Get_hostnames_testing.get_hostname_advanced_testing(Get_hostnames_testing.__get_hostnames_as_list__())
		elif args.nordvpn:
			#hostnames = 
			#hosts_list = []
			for servers_list in ["servers_dedicated", "servers_obfuscated", "servers_p2p", "servers_double", "servers_onion", "servers_standard"]:
				Get_hostnames_testing_nordvpn = main.Advanced_testing(get_nslookup = True, get_ping = True, get_traceroute = True, get_ssl_check = False, records = ["A"], nameserver = "1.1.1.1", get_dump = True, path_results_name = "hosts_nordvpn_" + servers_list)
				Get_hostnames_testing_nordvpn.get_hostname_advanced_testing([host.rstrip() for host in (File.get_request_text_as_str("https://raw.githubusercontent.com/babyish-retired0m/hostname_advanced_testing/main/hosts/nordvpn/" + servers_list + ".txt"))])
			#Get_hostnames_testing_nordvpn = main.Advanced_testing(get_nslookup = True, get_ping = True, get_traceroute = True, get_ssl_check = False, records = ["A"], nameserver = "1.1.1.1", get_dump = True)
			#Get_hostnames_testing_nordvpn.get_hostname_advanced_testing(Get_hostnames_testing_nordvpn.__get_hostnames_nordvpn_as_list__())
		elif args.facebook:
			hosts_PATH = './hosts/hosts_facebook.txt'
			if os.path.isfile(hosts_PATH):
				Get_hostnames_testing = main.Advanced_testing(get_nslookup = True, get_ping = True, get_traceroute = True, get_ssl_check = False, get_dump = True, path_results_name = "facebook.com")
				Get_hostnames_testing.get_hostname_advanced_testing([host.rstrip() for host in open(hosts_PATH, 'r').readlines()])
		elif args.linkedin:
			hosts_PATH = './hosts/hosts_linkedin.txt'
			if os.path.isfile(hosts_PATH):
				Get_hostnames_testing = main.Advanced_testing(get_nslookup = True, get_ping = True, get_traceroute = True, get_ssl_check = False, get_dump = True, path_results_name = "facebook.com")
				Get_hostnames_testing.get_hostname_advanced_testing([host.rstrip() for host in open(hosts_PATH, 'r').readlines()])
		elif args.wikipedia:
			hosts_PATH = './hosts/hosts_wikipedia.txt'
			if os.path.isfile(hosts_PATH):
				Get_hostnames_testing = main.Advanced_testing(get_nslookup = True, get_ping = True, get_traceroute = True, get_ssl_check = False, get_dump = True, path_results_name = "facebook.com")
				Get_hostnames_testing.get_hostname_advanced_testing([host.rstrip() for host in open(hosts_PATH, 'r').readlines()])
		elif args.yahoo:
			hosts_PATH = './hosts/hosts_yahoo.txt'
			if os.path.isfile(hosts_PATH):
				Get_hostnames_testing = main.Advanced_testing(get_nslookup = True, get_ping = True, get_traceroute = True, get_ssl_check = False, get_dump = True, path_results_name = "facebook.com")
				Get_hostnames_testing.get_hostname_advanced_testing([host.rstrip() for host in open(hosts_PATH, 'r').readlines()])
		elif args.hosts:
			hosts_PATH = './hosts/hosts.txt'
			if os.path.isfile(hosts_PATH):
				Get_hostnames_testing = main.Advanced_testing(get_nslookup = True, get_ping = True, get_traceroute = True, get_ssl_check = False, get_dump = True, path_results_name = "facebook.com")
				Get_hostnames_testing.get_hostname_advanced_testing([host.rstrip() for host in open(hosts_PATH, 'r').readlines()])
		elif args.google:
			hosts_PATH = './hosts/hosts_google.txt'
			if os.path.isfile(hosts_PATH):
				Get_hostnames_testing = main.Advanced_testing(get_nslookup = True, get_ping = True, get_traceroute = True, get_ssl_check = False, get_dump = True, path_results_name = "facebook.com")
				Get_hostnames_testing.get_hostname_advanced_testing([host.rstrip() for host in open(hosts_PATH, 'r').readlines()])
		elif args.apple:
			hosts_PATH = './hosts/hosts_apple.txt'
			if os.path.isfile(hosts_PATH):
				Get_hostnames_testing = main.Advanced_testing(get_nslookup = True, get_ping = True, get_traceroute = True, get_ssl_check = True, get_dump = True, path_results_name = "googlevideo.com")
				Get_hostnames_testing.get_hostname_advanced_testing([host.rstrip() for host in open(hosts_PATH, 'r').readlines()])
		elif args.services:
			for hosts in list(pathlib.Path('./hosts/services/').rglob('**/*.txt')):
				Get_hostnames_testing = main.Advanced_testing(get_nslookup = True, get_ping = True, get_traceroute = True, get_ssl_check = True, get_dump = True, path_results_name = "services_" + hosts.stem)
				Get_hostnames_testing.get_hostname_advanced_testing([host.rstrip() for host in open(hosts, 'r').readlines()])
		elif args.amazon:
			hosts_PATH = './hosts/hosts_amazon.com_all.txt'
			if os.path.isfile(hosts_PATH):
				Get_hostnames_testing = main.Advanced_testing(get_nslookup = True, get_ping = True, get_traceroute = True, get_ssl_check = False, get_dump = True, path_results_name = "amazon.com_all")
				Get_hostnames_testing.get_hostname_advanced_testing([host.rstrip() for host in open(hosts_PATH, 'r').readlines()])
		elif args.youtube:
			hosts_youtube_PATH = './hosts/google/hosts_youtube.com.txt'
			if os.path.isfile(hosts_youtube_PATH):
				Get_hostnames_testing = main.Advanced_testing(get_nslookup = True, get_ping = True, get_traceroute = True, get_ssl_check = True, get_dump = True, path_results_name = "youtube.com")
				Get_hostnames_testing.get_hostname_advanced_testing([host.rstrip() for host in open(hosts_youtube_PATH, 'r').readlines()])
			hosts_c_youtube_PATH = './hosts/google/hosts_c.youtube.com.txt'
			if os.path.isfile(hosts_c_youtube_PATH):
				Get_hostnames_testing = main.Advanced_testing(get_nslookup = True, get_ping = True, get_traceroute = True, get_ssl_check = False, get_dump = True, path_results_name = "c.youtube.com")
				Get_hostnames_testing.get_hostname_advanced_testing([host.rstrip() for host in open(hosts_c_youtube_PATH, 'r').readlines()])
		elif args.googlevideo:
			hosts_PATH = './hosts/google/hosts_googlevideo.com.txt'
			if os.path.isfile(hosts_PATH):
				Get_hostnames_testing = main.Advanced_testing(get_nslookup = True, get_ping = True, get_traceroute = True, get_ssl_check = False, get_dump = True, path_results_name = "googlevideo.com")
				Get_hostnames_testing.get_hostname_advanced_testing([host.rstrip() for host in open(hosts_PATH, 'r').readlines()])
		elif args.play_google:
			hosts_PATH = './hosts/google/hosts_play.google.com.txt'
			if os.path.isfile(hosts_PATH):
				Get_hostnames_testing = main.Advanced_testing(get_nslookup = True, get_ping = True, get_traceroute = True, get_ssl_check = False, get_dump = True, path_results_name = "play.google.com")
				Get_hostnames_testing.get_hostname_advanced_testing([host.rstrip() for host in open(hosts_PATH, 'r').readlines()])
		elif args.pack_google:
			hosts_PATH = './hosts/google/hosts_pack.google.com.txt'
			if os.path.isfile(hosts_PATH):
				Get_hostnames_testing = main.Advanced_testing(get_nslookup = True, get_ping = True, get_traceroute = True, get_ssl_check = False, get_dump = True, path_results_name = "pack.google.com")
				Get_hostnames_testing.get_hostname_advanced_testing([host.rstrip() for host in open(hosts_PATH, 'r').readlines()])
		elif args.offline_maps_google:
			hosts_PATH = './hosts/google/hosts_offline.maps.google.com.txt'
			if os.path.isfile(hosts_PATH):
				Get_hostnames_testing = main.Advanced_testing(get_nslookup = True, get_ping = True, get_traceroute = True, get_ssl_check = False, get_dump = True, path_results_name = "offline.maps.google.com")
				Get_hostnames_testing.get_hostname_advanced_testing([host.rstrip() for host in open(hosts_PATH, 'r').readlines()])
		elif args.mail_google:
			hosts_PATH = './hosts/google/hosts_mail.google.com.txt'
			if os.path.isfile(hosts_PATH):
				Get_hostnames_testing = main.Advanced_testing(get_nslookup = True, get_ping = True, get_traceroute = True, get_ssl_check = False, get_dump = True, path_results_name = "mail.google.com")
				G
		elif args.google_inbox:
			hosts_PATH = './hosts/google/hosts_inbox.google.com.txt'
			if os.path.isfile(hosts_PATH):
				Get_hostnames_testing = main.Advanced_testing(get_nslookup = True, get_ping = True, get_traceroute = True, get_ssl_check = False, get_dump = True, path_results_name = "mail.google.com")
				Get_hostnames_testing.get_hostname_advanced_testing([host.rstrip() for host in open(hosts_PATH, 'r').readlines()])
		elif args.drive_google:
			hosts_PATH = './hosts/google/hosts_drive.google.com.txt'
			if os.path.isfile(hosts_PATH):
				Get_hostnames_testing = main.Advanced_testing(get_nslookup = True, get_ping = True, get_traceroute = True, get_ssl_check = False, get_dump = True, path_results_name = "drive.google.com")
				Get_hostnames_testing.get_hostname_advanced_testing([host.rstrip() for host in open(hosts_PATH, 'r').readlines()])
		elif args.google_usercontent_doc:
			hosts_PATH = './hosts/google/hosts_doc-0-0-sj.sj.googleusercontent.com.txt'
			if os.path.isfile(hosts_PATH):
				Get_hostnames_testing = main.Advanced_testing(get_nslookup = True, get_ping = True, get_traceroute = True, get_ssl_check = False, get_dump = True, path_results_name = "doc-0-0-sj.sj.googleusercontent.com")
				Get_hostnames_testing.get_hostname_advanced_testing([host.rstrip() for host in open(hosts_PATH, 'r').readlines()])
		elif args.google_docs:
			hosts_PATH = './hosts/google/hosts_docs.google.com.txt'
			if os.path.isfile(hosts_PATH):
				Get_hostnames_testing = main.Advanced_testing(get_nslookup = True, get_ping = True, get_traceroute = True, get_ssl_check = False, get_dump = True, path_results_name = "docs.google.com")
				Get_hostnames_testing.get_hostname_advanced_testing([host.rstrip() for host in open(hosts_PATH, 'r').readlines()])
		elif args.google_chat:
			hosts_PATH = './hosts/google/hosts_chat.google.com.txt'
			if os.path.isfile(hosts_PATH):
				Get_hostnames_testing = main.Advanced_testing(get_nslookup = True, get_ping = True, get_traceroute = True, get_ssl_check = False, get_dump = True, path_results_name = "chat.google.com")
				Get_hostnames_testing.get_hostname_advanced_testing([host.rstrip() for host in open(hosts_PATH, 'r').readlines()])
		elif args.google_apis_bigcache:
			hosts_PATH = './hosts/google/hosts_bigcache.googleapis.com.txt'
			if os.path.isfile(hosts_PATH):
				Get_hostnames_testing = main.Advanced_testing(get_nslookup = True, get_ping = True, get_traceroute = True, get_ssl_check = False, get_dump = True, path_results_name = "bigcache.googleapis.com")
				Get_hostnames_testing.get_hostname_advanced_testing([host.rstrip() for host in open(hosts_PATH, 'r').readlines()])
		elif args.google_2mdn:
			hosts_PATH = './hosts/google/hosts_2mdn.net.txt'
			if os.path.isfile(hosts_PATH):
				Get_hostnames_testing = main.Advanced_testing(get_nslookup = True, get_ping = True, get_traceroute = True, get_ssl_check = False, get_dump = True, path_results_name = "2mdn.net")
				Get_hostnames_testing.get_hostname_advanced_testing([host.rstrip() for host in open(hosts_PATH, 'r').readlines()])
		elif args.google_1e100:
			hosts_PATH = './hosts/google/hosts_1e100.net.txt'
			if os.path.isfile(hosts_PATH):
				Get_hostnames_testing = main.Advanced_testing(get_nslookup = True, get_ping = True, get_traceroute = True, get_ssl_check = False, get_dump = True, path_results_name = "1e100.net")
				Get_hostnames_testing.get_hostname_advanced_testing([host.rstrip() for host in open(hosts_PATH, 'r').readlines()])
		elif args.google_usercontent:
			hosts_PATH = './hosts/google/hosts_googleusercontent.com.txt'
			if os.path.isfile(hosts_PATH):
				Get_hostnames_testing = main.Advanced_testing(get_nslookup = True, get_ping = True, get_traceroute = True, get_ssl_check = False, get_dump = True, path_results_name = "googleusercontent.com")
				Get_hostnames_testing.get_hostname_advanced_testing([host.rstrip() for host in open(hosts_PATH, 'r').readlines()])
		elif args.google_service:
			hosts_PATH = './hosts/google/hosts_google_service.txt'
			if os.path.isfile(hosts_PATH):
				Get_hostnames_testing = main.Advanced_testing(get_nslookup = True, get_ping = True, get_traceroute = True, get_ssl_check = False, get_dump = True, path_results_name = "google_service")
				Get_hostnames_testing.get_hostname_advanced_testing([host.rstrip() for host in open(hosts_PATH, 'r').readlines()])
		elif args.google_search_home:
			hosts_PATH = './hosts/google/hosts_google_search_home.txt'
			if os.path.isfile(hosts_PATH):
				Get_hostnames_testing = main.Advanced_testing(get_nslookup = True, get_ping = True, get_traceroute = True, get_ssl_check = False, get_dump = True, path_results_name = "google_search_home")
				Get_hostnames_testing.get_hostname_advanced_testing([host.rstrip() for host in open(hosts_PATH, 'r').readlines()])
		elif args.google_search_country:
			hosts_PATH = './hosts/google/hosts_google_search_country.txt'
			if os.path.isfile(hosts_PATH):
				Get_hostnames_testing = main.Advanced_testing(get_nslookup = True, get_ping = True, get_traceroute = True, get_ssl_check = False, get_dump = True, path_results_name = "google_search_country.com")
				Get_hostnames_testing.get_hostname_advanced_testing([host.rstrip() for host in open(hosts_PATH, 'r').readlines()])
		elif args.google_source:
			hosts_PATH = './hosts/google/hosts_googlesource.com.txt'
			if os.path.isfile(hosts_PATH):
				Get_hostnames_testing = main.Advanced_testing(get_nslookup = True, get_ping = True, get_traceroute = True, get_ssl_check = False, get_dump = True, path_results_name = "googlesource.com")
				Get_hostnames_testing.get_hostname_advanced_testing([host.rstrip() for host in open(hosts_PATH, 'r').readlines()])
		elif args.google_apis:
			hosts_PATH = './hosts/google/hosts_googleapis.txt'
			if os.path.isfile(hosts_PATH):
				Get_hostnames_testing = main.Advanced_testing(get_nslookup = True, get_ping = True, get_traceroute = True, get_ssl_check = False, get_dump = True, path_results_name = "googleapis.com")
				Get_hostnames_testing.get_hostname_advanced_testing([host.rstrip() for host in open(hosts_PATH, 'r').readlines()])
		elif args.google_gmail:
			hosts_PATH = './hosts/google/hosts_gmail.txt'
			if os.path.isfile(hosts_PATH):
				Get_hostnames_testing = main.Advanced_testing(get_nslookup = True, get_ping = True, get_traceroute = True, get_ssl_check = False, get_dump = True, path_results_name = "gmail.com")
				Get_hostnames_testing.get_hostname_advanced_testing([host.rstrip() for host in open(hosts_PATH, 'r').readlines()])
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
		group.add_argument("-S", "--services", dest = "services", action = "store_true", help = "Advanced testing services hostnames get nslookup check, get ping check, get traceroute check, get SSL certificate check.")
		group.add_argument("-G", "--google", dest = "google", action = "store_true", help = "Advanced testing Google hostnames get nslookup check, get ping check, get traceroute check, get SSL certificate check.")
		group.add_argument("-GY", "--youtube", dest = "youtube", action = "store_true", help = "Advanced testing youtube hostnames get nslookup check, get ping check, get traceroute check, get SSL certificate check.")
		group.add_argument("-GV", "--googlevideo", dest = "googlevideo", action = "store_true", help = "Advanced testing googlevideo hostnames get nslookup check, get ping check, get traceroute check, get SSL certificate check.")
		group.add_argument("-GP", "--playGoogle", dest = "play_google", action = "store_true", help = "Advanced testing play_google hostnames get nslookup check, get ping check, get traceroute check, get SSL certificate check.")
		group.add_argument("-Gp", "--packGoogle", dest = "pack_google", action = "store_true", help = "Advanced testing pack_google hostnames get nslookup check, get ping check, get traceroute check, get SSL certificate check.")
		group.add_argument("-GM", "--maps_google", dest = "offline_maps_google", action = "store_true", help = "Advanced testing offline_maps_google hostnames get nslookup check, get ping check, get traceroute check, get SSL certificate check.")
		group.add_argument("-Gm", "--mail_google", dest = "mail_google", action = "store_true", help = "Advanced testing mail_google hostnames get nslookup check, get ping check, get traceroute check, get SSL certificate check.")
		group.add_argument("-Gi", "--google_inbox", dest = "google_inbox", action = "store_true", help = "Advanced testing inbox_google hostnames get nslookup check, get ping check, get traceroute check, get SSL certificate check.")
		group.add_argument("-GD", "--drive_google", dest = "drive_google", action = "store_true", help = "Advanced testing drive_google hostnames get nslookup check, get ping check, get traceroute check, get SSL certificate check.")
		group.add_argument("-GUd", "--google_usercontent_doc", dest = "google_usercontent_doc", action = "store_true", help = "Advanced testing googleusercontent_google hostnames get nslookup check, get ping check, get traceroute check, get SSL certificate check.")
		group.add_argument("-Gd", "--google_docs", dest = "google_docs", action = "store_true", help = "Advanced testing google_docs hostnames get nslookup check, get ping check, get traceroute check, get SSL certificate check.")
		group.add_argument("-GC", "--google_chat", dest = "google_chat", action = "store_true", help = "Advanced testing google_chat hostnames get nslookup check, get ping check, get traceroute check, get SSL certificate check.")
		group.add_argument("-GAB", "--google_apis_bigcache", dest = "google_apis_bigcache", action = "store_true", help = "Advanced testing google_apis_bigcache hostnames get nslookup check, get ping check, get traceroute check, get SSL certificate check.")
		group.add_argument("-G2", "--google_2mdn", dest = "google_2mdn", action = "store_true", help = "Advanced testing google_2mdn hostnames get nslookup check, get ping check, get traceroute check, get SSL certificate check.")
		group.add_argument("-G1", "--google_1e100", dest = "google_1e100", action = "store_true", help = "Advanced testing google_1e100 hostnames get nslookup check, get ping check, get traceroute check, get SSL certificate check.")
		group.add_argument("-GU", "--google_usercontent", dest = "google_usercontent", action = "store_true", help = "Advanced testing google_usercontent hostnames get nslookup check, get ping check, get traceroute check, get SSL certificate check.")
		group.add_argument("-GS", "--google_service", dest = "google_service", action = "store_true", help = "Advanced testing google_service hostnames get nslookup check, get ping check, get traceroute check, get SSL certificate check.")
		group.add_argument("-GSH", "--google_search_home", dest = "google_search_home", action = "store_true", help = "Advanced testing google_search_home hostnames get nslookup check, get ping check, get traceroute check, get SSL certificate check.")
		group.add_argument("-GSC", "--google_search_country", dest = "google_search_country", action = "store_true", help = "Advanced testing google_search_country hostnames get nslookup check, get ping check, get traceroute check, get SSL certificate check.")
		group.add_argument("-Gs", "--google_source", dest = "google_source", action = "store_true", help = "Advanced testing google_source hostnames get nslookup check, get ping check, get traceroute check, get SSL certificate check.")
		group.add_argument("-GA", "--google_apis", dest = "google_apis", action = "store_true", help = "Advanced testing google_apis hostnames get nslookup check, get ping check, get traceroute check, get SSL certificate check.")
		group.add_argument("-GGm", "--google_gmail", dest = "google_gmail", action = "store_true", help = "Advanced testing google_gmail hostnames get nslookup check, get ping check, get traceroute check, get SSL certificate check.")
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