#!/usr/bin/env python3
__version__ = "2.1"
try:
	#resolve_mx
	import dns.resolver
	#resolve_ns
	import dns.message
	import dns.rdataclass
	import dns.rdatatype
	import dns.query
except ImportError:
	raise SystemExit("Please install dnspython: pip3 install dnspython")
#resolve_cname
import utilities.ip_address as ip_address
import utilities.file as file
import os
import sys

File = file.Main(print_result = False)

class Dns_response():
	def __init__(self, host = None, records = None, nameserver = None, ip_address_public_answer = ip_address.get_ip_address_public_amazon()):
		#, ip_address_public_answer = None
		self.host = host if isinstance(host, str) and host is not None else print("hostname is None or is hostname str?")
		self.records = ["A", "AAAA", "CNAME", "MX", "SOA", "TXT", "NS"] if records is None else [records] if isinstance(records, str) else records
		self.ip_address_pub = ip_address_public_answer
		
		#nameserver = [nameserver] if isinstance(nameserver, str) else nameserver
		#self.nameservers = self.__get_nameserver__() if nameserver is None else nameserver
		self.nameservers = self.__get_nameserver__() if nameserver is None else [nameserver] if isinstance(nameserver, str) else nameserver
		
		self.recv_records = {self.host:{}}
		#self.answer = None;#self.results = None;
	def __get_nameserver__(self):
		#DNS IP address Public:
		nameservers = ["1.1.1.1"]
		nameservers.extend(["8.8.4.4", "9.9.9.9", "64.6.64.6", "208.67.220.220", "209.244.0.3"])
		#nameservers.extend(["1.0.0.1","8.8.8.8","208.67.222.222"])
		
		#ip_addresses_block = File.get_request_text_as_json("https://api.github.com/repos/babyish-retired0m/functions/contents/ip_addresses_block_Provider?ref=main")
		
		parent_dir = os.path.dirname(__file__)
		ip_addresses_block_AS_9009 = File.open_as_list(parent_dir + "/ip_addresses_block_provider/AS-9009_m247.com.txt")
		ip_addresses_block_AS_42831 = File.open_as_list(parent_dir + "/ip_addresses_block_provider/AS-42831_ukservers.com.txt")
		ip_addresses_block_AS_21497 = File.open_as_list(parent_dir + "/ip_addresses_block_provider/AS-21497_vodafone.ua.txt")
		ip_addresses_block_AS_39608 = File.open_as_list(parent_dir + "/ip_addresses_block_provider/AS-39608_lanet.ua.txt")
		ip_addresses_block_AS_15895 = File.open_as_list(parent_dir + "/ip_addresses_block_provider/AS-15895_kyivstar.ua.txt")
		ip_addresses_block_AS_34058 = File.open_as_list(parent_dir + "/ip_addresses_block_provider/AS-34058_lifecell.ua.txt")
<<<<<<< Updated upstream
		ip_addresses_block_AS_44668 = File.open_as_list(parent_dir + "/ip_addresses_block_provider/AS-44668_znet.com.ua.txt")
=======
		
		
>>>>>>> Stashed changes
		#DNS IP address Lanet:
		if ip_address.check_ip_in_networks(self.ip_address_pub, ip_addresses_block_AS_39608):
			nameservers.append("194.50.85.5")
			#nameservers.extend(["194.50.85.5","194.50.85.7"])
			nameservers.remove("9.9.9.9")
			nameservers.remove("64.6.64.6")
			nameservers.remove("209.244.0.3")
		#DNS IP address Vodafone:
		elif ip_address.check_ip_in_networks(self.ip_address_pub, ip_addresses_block_AS_21497):
			nameservers.append("88.214.96.116")
		#DNS IP address Kyivstar:
		elif ip_address.check_ip_in_networks(self.ip_address_pub, ip_addresses_block_AS_15895):
			nameservers.append("193.41.60.1")
			#nameservers.extend(["88.214.96.116","88.214.96.117","88.214.96.118","88.214.96.119"])
			#nameservers.extend(["193.41.60.1","193.41.60.2"])
		#DNS IP address NordVPN
		elif ip_address.check_ip_in_networks(self.ip_address_pub, ip_addresses_block_AS_9009) or ip_address.check_ip_in_networks(self.ip_address_pub, ip_addresses_block_AS_42831):
			nameservers.append("103.86.99.99")
			#nameservers.extend(["103.86.96.100","103.86.99.99","103.86.99.100"])		
		#DNS IP address Lifecell:
		elif ip_address.check_ip_in_networks(self.ip_address_pub, ip_addresses_block_AS_34058):
			nameservers.append("212.58.161.173")
			#nameservers.extend(["212.58.161.174","2a00:1e98:1104:fd::5"])
<<<<<<< Updated upstream
		elif ip_address.check_ip_in_networks(self.ip_address_pub, ip_addresses_block_AS_44668):
			nameservers.append("91.202.104.6")
			nameservers.append("162.158.248.73")
=======

>>>>>>> Stashed changes
		#Checking DNS record propagation https://2ip.me/en/services/information-service/dns-check
		#nameservers = ['208.67.222.220', '8.8.8.8', '9.9.9.9', '98.113.146.9', '12.121.117.201', '66.206.166.2', '5.11.11.5', '163.172.107.158', '212.230.255.1', '194.209.157.109', '83.137.41.9', '194.145.241.6', '84.200.70.40', '200.56.224.11', '200.248.178.54', '103.26.250.4', '1.1.1.1', '61.8.0.113', '210.48.77.68', '164.124.101.2', '202.46.34.75', '31.7.37.37', '115.178.96.2', '58.27.149.60', '185.83.212.30', '103.146.221.20', '8.8.4.4', '64.6.64.6', '208.67.220.220', '209.244.0.3', '1.0.0.1', '208.67.222.222']
		return nameservers
	def nslookup(self, host = "www.facebook.com", record = "A"):
		try:
			results = []
			res = dns.resolver.Resolver()
			res.timeout = 0.6
			res.lifetime = 0.6
			res.nameservers = [self.nameserver]
			#if record == "NS": answers = answers.find_rrset(answers.answer, host, dns.rdataclass.IN, dns.rdatatype.NS)
			#else: answers = res.resolve(host, record)
			answers = answers.find_rrset(answers.answer, host, dns.rdataclass.IN, dns.rdatatype.NS) if record == "NS" else res.resolve(host, record)
			for rdata in answers:
				if record == "MX":
					answer = ('%s' % rdata.exchange)
					print(host + ".", "IN", record, rdata.preference, answer)
				elif record == "NS": answer = ('%s' % rdata.target)
				else: answer = ('%s' % rdata)
				if answer.endswith("."): answer = answer[:-1]
				results.append(answer)
				print(host + ".", "IN", record, answer + ".")
				#print(host + ".", "IN", record, answer + ".") if record == "CNAME" else print(host + ".", "IN", record, answer)
			return answer if record == "CNAME" else results
		except Exception as error:
			print(host + ".", "IN", record, "None")
			#raise error
			#print(host + ".", "IN", record, "None") if record!="CNAME" else print(host + ".", "IN", record, "None")
			return None
	def nslookup_record(self):
		for record in self.records:
			self.record = record
			recv = self.resolve_cname(host = self.host, nameserver = self.nameserver, results = {}) if record == "CNAME" else self.nslookup(host = self.host, record = self.record)
			if record == "CNAME":
				if not isinstance(recv[self.host], list):
					self.recv_records[self.host][self.nameserver][self.record] = recv
			elif recv is not None:
				self.recv_records[self.host][self.nameserver][self.record] = recv
		return self.recv_records
	def get_nslookup(self):
		for self.nameserver in self.nameservers:
			self.recv_records[self.host][self.nameserver] = {}
			print("Nameserver response:", self.nameserver, self.host)
			self.nslookup_record()
		return self.recv_records
	def resolve_cname(self, host, nameserver, results = {}):
		return self.resolve_cname_c(host = host, nameserver = nameserver, results = results)
	def resolve_cname_c(self, host, nameserver, results = {}):
		self.nameserver = nameserver
		answer = self.nslookup(host = host, record = "CNAME")
		if answer is not None and ip_address.get_ip_address_valid(answer[0]): return None
		elif answer == None:
			response = self.nslookup(host = host, record = "A")
			results[host] = response
		elif ip_address.get_ip_address_valid(answer) == False:
			results[host] = answer
			self.resolve_cname(host = answer, nameserver = self.nameserver, results = results)
		return results
if __name__ == '__main__':
	response = Dns_response("amazonaws.com")
	print(Response.get_nslookup())