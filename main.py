#!/usr/bin/env python3
__version__ = "2.0"
import utilities.dns_resolve as dns_resolve
import utilities.ping as ping
import utilities.traceroute as traceroute
try:
	import icmplib
except ImportError:
    raise SystemExit("Please install icmplib, pip3 install icmplib, (https://github.com/ValentinBELYN/icmplib)")
import utilities.ssl_check as ssl_check
import utilities.ip_address as ip_address
import utilities.utility as utility
import utilities.file as file
import time
import os
import json
import sys
import pathlib

File = file.Main(print_result = False)

class Advanced_testing:
	def __init__(self, get_nslookup = True, get_ping = True, get_traceroute = True, get_ssl_check = True, get_dump = True, records = ["A", "AAAA", "CNAME", "MX", "SOA", "TXT", "NS"], nameserver = None, hostnames_dict = {}, path_results_name = None):
		self.get_nslookup = get_nslookup
		self.get_ping = get_ping
		self.get_traceroute = get_traceroute
		self.get_ssl_check = get_ssl_check
		self.get_dump = get_dump
		self.records = records
		self.nameserver = nameserver
		self.parent_dir = os.path.dirname(__file__)
		path = self.parent_dir + "/results/"
		if File.check_dir(path) is False: File.dirs_make(path)
		self.path_results = path + "results_" + time.strftime("%Y-%m-%d_%H-%M-%S", time.gmtime()) + ".json"
		if path_results_name: self.path_results = self.path_results.replace(".json", "_hosts_" + path_results_name + ".json")
		if len(hostnames_dict) > 0:
			self.recv_records = hostnames_dict
		else:
			#self.recv_records = {"parameters" : {"Unix Epoch Time" : utility.get_unix_time(), "Public IP Address" : self.__get_ip__()}}
			self.recv_records = {"parameters" : {"Unix Epoch Time" : utility.get_unix_time()}}
		self.cannot_be_resolved = File.open_as_list(self.parent_dir + "/utilities/cannot_be_resolved.txt")
		self.cannot_be_ssl_checked = File.open_as_list(self.parent_dir + "/utilities/cannot_be_ssl_checked.txt")
	"""def __call__(self):
		return self.__get_hostname_advanced_testing__()"""
	def __get_ip_public__(self):
		self.ip_address_public = ip_address.get_ip_address_public_amazon()
		if self.ip_address_public: self.__get_ip_address_checked__()
	def __get_ip_address_checked__(self):
		if ip_address.check_ip_in_network_lanet_ua(self.ip_address_public): self.ip_address_checked = "176.36.0.0/14"
		else: self.ip_address_checked = self.ip_address_public
	def __get_nslookup__(self, qname):
		Response = dns_resolve.Dns_response(host = qname, records = self.records, nameserver = self.nameserver, ip_address_public_answer = self.ip_address_public)
		result = Response.get_nslookup()
		recv_records = {"resolve":{"nslookup":result[qname]}}
		recv_records["resolve"]["parameters"] = {"Unix Epoch Time":utility.get_unix_time(), "Public IP Address":self.ip_address_checked, "pcname":utility.getpcname(), "username":utility.getusername(), "currentdirectory":utility.getcurrentdirectory()}
		return recv_records["resolve"]
	def __get_ping__(self, qname):
		result = ping.verbose_ping(address = qname, ip_address_resolved = self.ip_address_resolved)
		if result is not None:
			recv_records = {"verbose_ping":result[qname]}
			recv_records["verbose_ping"]["parameters"]["Unix Epoch Time"] = utility.get_unix_time()
			recv_records["verbose_ping"]["parameters"]["Public IP Address"] = self.ip_address_checked
			return recv_records["verbose_ping"]
	def __get_traceroute__(self, qname):
		result = traceroute.verbose_traceroute(address = qname, ip_address_resolved = self.ip_address_resolved)
		recv_records = {"verbose_traceroute":result[qname]}
		recv_records["verbose_traceroute"]["parameters"]["Unix Epoch Time"] = utility.get_unix_time()
		recv_records["verbose_traceroute"]["parameters"]["Public IP Address"] = self.ip_address_checked
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
		if hostnames_len > 1000:
			if hostnames_len % 2 == 0: k = 100
			else: k = 50
		else:
			if hostnames_len % 2 == 0: k = 200
			else: k = 150
		for qname in self.hostnames:
			self.__get_ip_public__()
			if len(qname)>3:
				if qname in self.cannot_be_resolved: pass
				else:
					try: 
						self.ip_address_resolved = icmplib.resolve(qname)[0]
					except:
						print(f"The name '{qname}' cannot be resolved")
						self.cannot_be_resolved.append(qname)
						pass
					else:
						self.recv_records["advanced_test"][qname] = {}
						utility.percents_print(self.hostnames.index(qname), hostnames_len)
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
	Get_hostnames_testing = Advanced_testing(get_nslookup = True, get_ping = False, get_traceroute = False, get_ssl_check = False, get_dump = False, records = ["A", "CNAME"], nameserver = "1.1.1.1")
	print(Get_hostnames_testing.get_hostname_advanced_testing(hostnames = ["www.facebook.com", "amazon.com", "us2723.nordvpn.com", "jp590.nordvpn.com", "za110.nordvpn.com"]))