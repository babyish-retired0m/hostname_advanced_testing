#!/usr/bin/env python3
__version__ = "3.1"
"""
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

File = file.Main(print_result = False)

class Advanced_testing:
	def __init__(self, get_nslookup = True, get_ping = True, get_traceroute = True, get_ssl_check = True, get_dump = True, records = ["A", "AAAA", "CNAME", "MX", "SOA", "TXT", "NS"], nameserver = None, hostnames_dict = {}, path_results_name = None, print_result = True, say_result = False):
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
			self.recv_records = {"parameters" : {"Unix Epoch Time" : utility.get_time_unix(), 'timezone':'UTC'}}

		self.path_results_name = path_results_name
		self.parent_dir = os.path.dirname(__file__)
		path = self.parent_dir + "/results/"
		if File.check_dir(path) is False: File.dirs_make(path)
		self.path_results = path + "results_" + time.strftime("%Y-%m-%d_%H-%M-%S", utility.get_time_local()) + ".json"
		if self.path_results_name: self.path_results = self.path_results.replace(".json", "_hosts_" + self.path_results_name + ".json")

		self.ip_address_resolved = None
		self.can_not_be_resolve_path = self.parent_dir + "/utilities/can_not_be_resolve.txt"
		self.can_not_be_resolve = File.open_as_list(self.can_not_be_resolve_path)
		self.can_not_be_ssl_check_path = self.parent_dir + "/utilities/can_not_be_ssl_check.txt"
		self.can_not_be_ssl_check = File.open_as_list(self.can_not_be_ssl_check_path)

		self.print_result = print_result
		self.say_result = say_result
	"""def __call__(self):
		return self.__get_hostname_advanced_testing__()"""


	def __get_ip_public__(self):
		def __get_ip_address_check__():
			self.ip_address_checked = "176.36.0.0/14" if ip_address.check_ip_in_network_lanet_ua(self.ip_address_public) else self.ip_address_public
		self.ip_address_public = ip_address.get_ip_address_public_amazon(timeout_count = 100, timeout_sleep = 10)
		__get_ip_address_check__()


	def __get_nslookup__(self, qname):
		Response = dns_resolve.Dns_response(host = qname, records = self.records, nameserver = self.nameserver, ip_address_public_answer = self.ip_address_public)
		result = Response.get_nslookup()
		recv_records = {"resolve":{"nslookup":result[qname]}}
		recv_records["resolve"]["parameters"] = {"Unix Epoch Time":utility.get_time_unix(), "Public IP Address":self.ip_address_checked, "pcname":utility.get_pcname(), "username":utility.get_username(), "currentdirectory":utility.get_currentdirectory()}
		return recv_records["resolve"]


	def __get_ping__(self, qname):
		result = ping.verbose_ping(address = qname, ip_address_resolved = self.ip_address_resolved)
		if result is not None:
			recv_records = {"verbose_ping":result[qname]}
			recv_records["verbose_ping"]["parameters"]["Unix Epoch Time"] = utility.get_time_unix()
			recv_records["verbose_ping"]["parameters"]["Public IP Address"] = self.ip_address_checked
			return recv_records["verbose_ping"]


	def __get_traceroute__(self, qname):
		result = traceroute.verbose_traceroute(address = qname, ip_address_resolved = self.ip_address_resolved)
		if result is not None:
			recv_records = {"verbose_traceroute":result[qname]}
			recv_records["verbose_traceroute"]["parameters"]["Unix Epoch Time"] = utility.get_time_unix()
			recv_records["verbose_traceroute"]["parameters"]["Public IP Address"] = self.ip_address_checked
			return recv_records["verbose_traceroute"]


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
						File.write_text_as_json(self.can_not_be_ssl_check_path, self.can_not_be_ssl_check)
				except: print("__get_ssl_check__ cannot be ssl checked")
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
			File.write_text_as_json(self.can_not_be_resolve_path, self.can_not_be_resolve)
			return False


	def get_hostname_advanced_testing(self, hostnames = "amazon.com"):
		self.hostnames = hostnames
		self.start_time = time.time()
		self.recv_records["advanced_test"] = {}
		if isinstance(self.hostnames, str): self.hostnames = [self.hostnames]
		elif isinstance(self.hostnames, list): pass
		else: print("Are list of hostname(s) str, list?"); sys.exit(1)
		self.hostnames_len = len(self.hostnames)
		if self.hostnames_len > 1000:
			if self.hostnames_len % 2 == 0: self.k = 100
			else: self.k = 50
		else:
			if self.hostnames_len % 2 == 0: self.k = 200
			else: self.k = 150
		for qname in self.hostnames:
			start_time_advanced_test = time.time()
			self.__get_ip_public__()

			if len(qname)>3 and qname not in self.can_not_be_resolve and self.__get_ip_address_resolved__(qname):

				self.recv_records["advanced_test"][qname] = {}
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


	def __get_dump__(self):
		if self.get_dump:
			json.dump(self.recv_records, fp = open(self.path_results, 'w'), indent=4)
			if self.print_result: utility.print_green2("Results dumped:" + self.path_results)
			if self.say_result: utility.get_say('Results dumped')


	def __print_result_duration__(self, qname):
		if self.print_result:
			duration_seconds = time.time() - self.start_time
			duration = time.strftime("%H:%M:%S", time.gmtime(duration_seconds))
			self.border_msg(utility.Clr.YELLOW2 + 'List ' + str(self.hostnames.index(qname)) + ' of ' + str(self.hostnames_len) + ' duration: ' + duration + utility.Clr.RST2 + ' ' + time.ctime())


	def __print_result_execution_time_Duration__(self, say_result = False):
		if self.print_result:
			duration_seconds = time.time() - self.start_time
			duration = time.strftime("%H:%M:%S", time.gmtime(duration_seconds))
			self.recv_records["parameters"]["Execution time Duration"] = str('{:.3f}'.format(duration_seconds))
			print("Duration:", duration)
		if self.say_result: utility.get_say("Dns hostnames advanced tests jobs done, time taken: " + duration)


	def border_msg(self, message):
		"""Print the message in the box."""
		#row = len(ord(message))
		row = len(message)
		#print('row = len(message)',row)
		row_len = 60
		row = row_len if row < row_len else row
		row_len_result = int(row / 4)
		#print('row',row,'row_len_result',row_len_result)
		i = ''.join([(row_len_result - 2) * ' '])
		h = ''.join(['+'] + ['-' * row] + ['+'])
		result = h + '\n' + '|' + i + message + i + '|' + '\n' + h
		print(result)


if __name__ == '__main__':
	#Get_hostnames_testing = Advanced_testing(get_nslookup = True, get_ping = False, get_traceroute = False, get_ssl_check = False, get_dump = False, records = ["A", "CNAME"], nameserver = '1.1.1.1')

	Get_hostnames_testing = Advanced_testing(get_nslookup = True, get_ping = True, get_traceroute = True, get_ssl_check = False, get_dump = False, records = ["A", "CNAME"], nameserver = ['1.1.1.1', '8.8.4.4'])
	try:
		print(Get_hostnames_testing.get_hostname_advanced_testing(hostnames = ['www.facebook.com',
		'amazon.com',
		 'us2723.nordvpn.com',
		  'jp590.nordvpn.com',
		   'za110.nordvpn.com',
		   'fbi.gov',
		   'www.ic3.gov',
		   'ic3.gov'
		   ]))
	except Exception as e:
		# raise e
		print('KeyboardInterrupt')