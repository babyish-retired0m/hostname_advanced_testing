#!/usr/bin/env python3
__version__ = "1.7"
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

class Advanced_testing:
	def __init__(self, get_nslookup = True, get_ping = True, get_traceroute = True, get_ssl_check = True, get_dump = True, hostnames_dict = {}):
		self.get_nslookup = get_nslookup
		self.get_ping = get_ping
		self.get_traceroute = get_traceroute
		self.get_ssl_check = get_ssl_check
		self.parent_dir = os.path.dirname(__file__)
		path = self.parent_dir + "/results/"
		if file.check_dir(path) is False: file.dirs_make(path)
		self.path_results = path + "results_"+time.strftime("%Y-%m-%d_%H-%M-%S", time.gmtime())+".json"
		if len(hostnames_dict) > 0:
			self.recv_records = hostnames_dict
		else:
			self.recv_records = {"parameters":{"Unix Epoch Time":utility.get_unix_time(),"Public IP Address":self.__get_ip__()}}
		self.cannot_be_resolved = file.open_as_list(self.parent_dir + "/utilities/cannot_be_resolved.txt")
		self.cannot_be_ssl_checked = file.open_as_list(self.parent_dir + "/utilities/cannot_be_ssl_checked.txt")
		self.get_dump = get_dump
	"""def __call__(self):
		return self.__get_hostname_advanced_testing__()"""
	
	def __get_hostnames_as_list__(self):
		self.path_results = self.path_results.replace(".json", "_hosts_all.json")
		hostnames = ["hosts_facebook", "hosts_bing", "hosts_linkedin", "hosts_wikipedia", "hosts_yahoo", "hosts", "hosts_google", "hosts_apple", "hosts_amazon"]
		hosts_list = []
		for servers_list in hostnames:
			hosts_list.extend(file.get_request_text_as_str("https://raw.githubusercontent.com/babyish-retired0m/hostname_advanced_testing/main/hosts/"+servers_list+".txt"))
			#hosts_list.extend(file.open_as_list(os.path.dirname(__file__) + "/hosts/"+servers_list+".txt"))
			if servers_list == "hosts_bing":
				hosts_list.remove("nrb.footprintdns.com")
			if servers_list == "hosts":
				hosts_list.append("162.158.248.55")
		return hosts_list
	
	def __get_hostnames_nordvpn_as_list__(self):
		self.path_results = self.path_results.replace(".json", "_hosts_nordvpn.json")
		hostnames = ["servers_dedicated", "servers_obfuscated", "servers_p2p", "servers_double", "servers_onion", "servers_standard"]
		hosts_list = []
		for servers_list in hostnames:
			#hosts_list.extend(file.get_request_text_as_str("https://raw.githubusercontent.com/babyish-retired0m/hostname_advanced_testing/main/hosts/nordvpn/"+servers_list+".txt"))
			hosts_list.extend(file.open_as_list(os.path.dirname(__file__) + "/hosts/nordvpn/"+servers_list+".txt"))
		return hosts_list
	
	def __get_ip__(self):
		ip = ip_address.get_ip_address_public_amazon()
		if ip is None: sys.exit(1)
		elif ip_address.check_ip_in_network_lanet_ua(): ip = "176.36.0.0/14"
		return ip
	def __get_nslookup__(self, qname):
		response = dns_resolve.dns_response(qname)
		result = response.nslookup_nameserver()
		recv_records = {"resolve":{"nslookup":result[qname]}}
		recv_records["resolve"]["parameters"]={"Unix Epoch Time":utility.get_unix_time(), "Public IP Address":self.__get_ip__(), "pcname":utility.getpcname(), "username":utility.getusername(), "currentdirectory":utility.getcurrentdirectory()}
		return recv_records["resolve"]
	def __get_ping__(self, qname):
		result = ping.verbose_ping(qname)
		if result is not None:
			recv_records = {"verbose_ping":result[qname]}
			recv_records["verbose_ping"]["parameters"]["Unix Epoch Time"] = utility.get_unix_time()
			recv_records["verbose_ping"]["parameters"]["Public IP Address"] = self.__get_ip__()
			return recv_records["verbose_ping"]
	def __get_traceroute__(self, qname):
		result = traceroute.verbose_traceroute(qname)
		recv_records = {"verbose_traceroute":result[qname]}
		recv_records["verbose_traceroute"]["parameters"]["Unix Epoch Time"] = utility.get_unix_time()
		recv_records["verbose_traceroute"]["parameters"]["Public IP Address"] = self.__get_ip__()
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
	def get_hostname_advanced_testing(self, hostnames = "amazon.com"):
		self.hostnames = hostnames
		start_time = time.time()
		self.recv_records["advanced_test"] = {}
		if isinstance(self.hostnames, str): self.hostnames = [self.hostnames]
		elif isinstance(self.hostnames, list): pass
		else: print("Are list of hostname(s) str, list?"); sys.exit(1)
		hostnames_len = len(self.hostnames)
		if hostnames_len % 2 == 0: k = 400
		else: k = 300
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
						utility.Percents(self.hostnames.index(qname), hostnames_len)
						#nslookup
						if self.get_nslookup: self.recv_records["advanced_test"][qname]["resolve"] = self.__get_nslookup__(qname)
						#ping
						if self.get_ping: self.recv_records["advanced_test"][qname]["verbose_ping"] = self.__get_ping__(qname)
						#traceroute
						if self.get_traceroute: self.recv_records["advanced_test"][qname]["verbose_traceroute"] = self.__get_traceroute__(qname)
						#ssl_check
						if self.get_ssl_check: self.recv_records["advanced_test"][qname]["ssl_cert_info"] = self.__get_ssl_check__(qname)
			if self.hostnames.index(qname) > 0:
				if self.hostnames.index(qname) % k == 0:
					duration_seconds = time.time() - start_time
					duration = time.strftime("%H:%M:%S", time.gmtime(duration_seconds))
					print("List " + str(self.hostnames.index(qname)) + " of", str(hostnames_len), "duration:", duration)
					if self.get_dump: self.__get_dump__()
		duration_seconds = time.time() - start_time
		duration = time.strftime("%H:%M:%S", time.gmtime(duration_seconds))
		self.recv_records["parameters"]["Execution time Duration"] = str('{:.3f}'.format(duration_seconds))
		print("Duration:", duration)
		os.system('say ' + "Dns hostnames advanced tests jobs done, time taken:: " + duration)
		if self.get_dump: self.__get_dump__()
		return self.recv_records
	def __get_dump__(self):
		json.dump(self.recv_records, fp = open(self.path_results, 'w'), indent=4)
		print("Results dumped:", self.path_results)
		os.system('say ' + "Results dumped")

if __name__ == '__main__':
	import os
	import time
		
	Get_hostnames_testing = Advanced_testing(get_nslookup = True, get_ping = True, get_traceroute = True, get_ssl_check = True, get_dump = True)
	Get_hostnames_testing.get_hostname_advanced_testing(Get_hostnames_testing.__get_hostnames_as_list__())
	#Get_hostnames_testing_nordvpn = Advanced_testing(get_nslookup = True, get_ping = True, get_traceroute = True, get_ssl_check = True, get_dump = True)
	#Get_hostnames_testing_nordvpn.get_hostname_advanced_testing(Get_hostnames_testing_nordvpn.__get_hostnames_nordvpn_as_list__())