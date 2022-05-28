#!/usr/bin/env python3
__version__ = "1.5"
try:
	import utilities.dns_resolve as dns_resolve
	import utilities.ping as ping
	import utilities.traceroute as traceroute
except ImportError:
	raise SystemExit("Please install dnspython")
try:
	import icmplib
except ImportError:
    raise SystemExit("Please install icmplib, pip3 install icmplib (https://github.com/ValentinBELYN/icmplib)")
import utilities.ssl_check as ssl_check
import utilities.ip_address as ip_address
import utilities.utility as utility
import utilities.file as file
import time
import os
import json
import sys
_start_time = time.time()

_ip = ip_address.get_ip_address_public_amazon()
if _ip is None:
	#print("Error connecting to https://checkip.amazonaws.com.\nCheck your internet connection or https://status.aws.amazon.com")
	sys.exit(1)
elif ip_address.check_ip_in_network_lanet_ua(): _ip = "176.36.0.0/14"

recv_records = {"parameters":{"Unix Epoch Time":utility.get_unix_time(),"Public IP Address":_ip}}
parent_dir = os.path.dirname(__file__) 
cannot_be_resolved = file.open_as_list(parent_dir + "/utilities/cannot_be_resolved.txt")
cannot_be_ssl_checked = file.open_as_list(parent_dir + "/utilities/cannot_be_ssl_checked.txt")

class Advanced_testing:
	def __init__(self, hostnames = ["amazon.com"], get_nslookup = True, get_ping = True, get_traceroute = True, get_ssl_check = True, dump = False):
		self.hostnames = hostnames
		self.get_nslookup = get_nslookup
		self.get_ping = get_ping
		self.get_traceroute = get_traceroute
		self.get_ssl_check = get_ssl_check
		parent_dir = os.path.dirname(__file__)
		path = parent_dir + "/results/"
		if file.check_dir(path) is False: file.dirs_make(path)
		self.path_results = path + "results_"+time.strftime("%Y-%m-%d_%H-%M-%S", time.gmtime())+".json"
		self.recv_records = {"parameters":{"Unix Epoch Time":utility.get_unix_time(),"Public IP Address":_ip}}
		self.cannot_be_resolved = file.open_as_list(parent_dir + "/utilities/cannot_be_resolved.txt")
		self.cannot_be_ssl_checked = file.open_as_list(parent_dir + "/utilities/cannot_be_ssl_checked.txt")
		self.dump = dump
	def __call__(self):
		return self.get_hostname_advanced_testing()
	def __get_nslookup__(self, qname):
		response = dns_resolve.dns_response(qname)
		result = response.nslookup_nameserver()
		recv_records = {"resolve":result[qname]}
		recv_records["resolve"]["parameters"]={"Unix Epoch Time":utility.get_unix_time(),"Public IP Address":_ip,"pcname":utility.getpcname(),"username":utility.getusername(),"currentdirectory":utility.getcurrentdirectory()}
		return recv_records["resolve"]
	def __get_ping__(self, qname):
		result = ping.verbose_ping(qname)
		if result is not None:
			recv_records = {"verbose_ping":result[qname]}
			recv_records["verbose_ping"]["parameters"]["Unix Epoch Time"] = utility.get_unix_time()
			recv_records["verbose_ping"]["parameters"]["Public IP Address"] = _ip
			return recv_records["verbose_ping"]
	def __get_traceroute__(self, qname):
		result = traceroute.verbose_traceroute(qname)
		recv_records = {"verbose_traceroute":result[qname]}
		recv_records["verbose_traceroute"]["parameters"]["Unix Epoch Time"] = utility.get_unix_time()
		recv_records["verbose_traceroute"]["parameters"]["Public IP Address"] = _ip
		return recv_records["verbose_traceroute"]
	def __get_ssl_check__(self, qname):
		if qname not in self.cannot_be_ssl_checked:
			sslobject = ssl_check.SSLCheck()
			try:
				result = sslobject.show_result([qname])
				if result is not None:
					recv_records = result[qname]
					return recv_records
				else: self.cannot_be_ssl_checked.append(qname)
			except: print("__get_ssl_check__ cannot be ssl checked")
		else: pass
	def get_hostname_advanced_testing(self):
		start_time = time.time()
		self.recv_records["advanced_test"] = {}
		if isinstance(self.hostnames, str): self.hostnames = [self.hostnames]
		elif isinstance(self.hostnames, list): pass
		else: print("Are list of hostname(s) str, list?"); sys.exit(1)
		for qname in self.hostnames:
			if len(qname)>3:
				if qname in self.cannot_be_resolved: pass
				else:
					try: 
						icmplib.resolve(qname)
					except:
						print(f"The name '{qname}' cannot be resolved")
						self.cannot_be_resolved.append(qname)
						pass
					else:
						self.recv_records["advanced_test"][qname] = {}
						utility.Percents(self.hostnames.index(qname), len(self.hostnames))
						#nslookup
						if self.get_nslookup: self.recv_records["advanced_test"][qname]["resolve"] = self.__get_nslookup__(qname)
						#ping
						if self.get_ping: self.recv_records["advanced_test"][qname]["verbose_ping"] = self.__get_ping__(qname)
						#traceroute
						if self.get_traceroute: self.recv_records["advanced_test"][qname]["verbose_traceroute"] = self.__get_traceroute__(qname)
						#ssl_check
						if self.get_ssl_check: self.recv_records["advanced_test"][qname]["ssl_cert_info"] = self.__get_ssl_check__(qname)
		self.recv_records["parameters"]["Execution time Duration"] = '{:.3f}'.format(time.time() - start_time)
		print('duration: {:.3f}'.format(time.time() - start_time))
		os.system('say "get dns resolve jobs done"')
		if self.dump: self.__dump__()
		return self.recv_records
	def __dump__(self):
		json.dump(self.recv_records, fp = open(self.path_results, 'w'),indent=4)
	
	def get_hostnames_nordvpn():
		self.path_results = self.path_results.replace(".json", "_hosts_nordvpn.json")
		get_hostnames={}
		json.dump(get_hostnames, fp=open(self.path_json,'w'),indent=4)
		hostnames = ["servers_dedicated",
					"servers_obfuscated",
					"servers_p2p",
					"servers_double",
					"servers_onion",
					"servers_standard"]
		for hostname in hostnames:
			get_hostnames = json.load(open(path_json))
			hosts = file.open_as_list("/Users/jozbox/python/functions/nordvpn/"+hostname+".txt")
			#print(hosts)
			get_advanced_testing = Advanced_testing(hostnames = hosts, get_nslookup = True, get_ping = True, get_traceroute = True, get_ssl_check = False, dump = False)
			get_hostnames[hostname] = get_advanced_testing()
			json.dump(get_hostnames, fp = open(path_json,'w'), indent = 4)

if __name__ == '__main__':
	import os
	import time
	#get_hostnames()
	
	#get_hostname_advanced_testing(["amazonaws.com"])
	
	#get_advanced_testing = Advanced_testing(hostnames = ["amazonaws.com"], get_nslookup = True, get_ping = True, get_traceroute = False, get_ssl_check = False, dump = False)
	#print(get_advanced_testing())
	
	
	
			"""
			"Standard VPN servers",
					"Dedicated IP",
					"Obfuscated Servers",
					"P2P",
					"Double VPN",
					"Onion Over VPN"
			"""
	#get_hostnames_nordvpn()
	
	def get_hostnames():
		path = parent_dir + "/results/"
		if file.check_dir(path) is False: file.dirs_make(path)
		path_json = path + "results_"+time.strftime("%Y-%m-%d_%H-%M-%S", time.gmtime())+"_hosts_all.json"
		hostnames=["hosts_facebook","hosts_bing","hosts_linkedin","hosts_wikipedia","hosts_yahoo","hosts","hosts_google","hosts_apple","hosts_amazon"]
		get_hostnames={}
		json.dump(get_hostnames, fp=open(path_json,'w'),indent=4)
		for hostname in hostnames:
			get_hostnames = json.load(open(path_json))
			hosts = file.get_request_text_as_str("https://raw.githubusercontent.com/babyish-retired0m/hostname_advanced_testing/main/hosts/"+hostname+".txt")
			if hostname == "hosts_bing":
				hosts.remove("nrb.footprintdns.com")
			if hostname == "hosts":
				hosts.append("162.158.248.55")
			get_advanced_testing = Advanced_testing(hostnames = hosts, get_nslookup = True, get_ping = True, get_traceroute = True, get_ssl_check = True, dump = False)
			get_hostnames[hostname] = get_advanced_testing()
			json.dump(get_hostnames, fp=open(path_json,'w'),indent=4)
		duration = '{:.3f}'.format(time.time()- _start_time)
		print("Duration:",duration)
		print("cannot be resolved",cannot_be_resolved)
		print("cannot be ssl checked",cannot_be_ssl_checked)
		os.system('say '+"dns resolve jobs done, Duration"+str(duration))
	
	get_hostnames()