#!/usr/bin/env python3
__version__ = "1.7"
try:
	#resolve_mx
	import dns.resolver
	#resolve_ns
	import dns.message
	import dns.rdataclass
	import dns.rdatatype
	import dns.query
except ImportError:
	raise SystemExit("Please install dnspython")
#resolve_cname
import utilities.ip_address as ip_address
import utilities.file as file

class dns_response():
	def __init__(self,host):
		super().__init__()
		self.host = host
		self.records = ["A","AAAA","CNAME","MX","SOA","TXT","NS"]
		self.nameserver = None
		
		#DNS IP address Public:
		#self.nameservers = ["1.1.1.1"]
		self.nameservers = ["1.1.1.1","8.8.4.4","9.9.9.9","64.6.64.6","208.67.220.220","209.244.0.3"]
		
		#DNS IP address Public:
		#self.nameservers.extend(["1.0.0.1","8.8.8.8","208.67.222.222"])
		ip_addresses_block = file.get_request_text_as_json("https://api.github.com/repos/babyish-retired0m/functions/contents/ip_addresses_block_Provider?ref=main")
		
		for i in ip_addresses_block:
			#DNS IP address Lanet:
			if i["name"]=="AS-39608_lanet.ua.txt":
				if ip_address.check_ip_in_networks(ip_address.get_ip_address_public_amazon(),file.get_request_text_as_str(i["download_url"])):
					self.nameservers.append("194.50.85.5")
					#self.nameservers.extend(["194.50.85.5","194.50.85.7"])
			#DNS IP address Vodafone:
			elif i["name"]=="AS-21497_vodafone.ua.txt":
				if ip_address.check_ip_in_networks(ip_address.get_ip_address_public_amazon(),file.get_request_text_as_str(i["download_url"])):
					self.nameservers.append("88.214.96.116")
					#self.nameservers.extend(["88.214.96.116","88.214.96.117","88.214.96.118","88.214.96.119"])
			#DNS IP address Kyivstar:
			elif i["name"]=="AS-15895_kyivstar.ua.txt":
				if ip_address.check_ip_in_networks(ip_address.get_ip_address_public_amazon(),file.get_request_text_as_str(i["download_url"])):
					self.nameservers.append("193.41.60.1")
					#self.nameservers.extend(["193.41.60.1","193.41.60.2"])
			#DNS IP address NordVPN
			elif i["name"]=="AS-9009_m247.com.txt":
				if ip_address.check_ip_in_networks(ip_address.get_ip_address_public_amazon(),file.get_request_text_as_str(i["download_url"])):
					self.nameservers.append("103.86.99.99")
					#self.nameservers.extend(["103.86.96.100","103.86.99.99","103.86.99.100"])
			
		#DNS IP address Lanet:
		
		#DNS IP address Kyivstar:
		
		#DNS IP address Vodafone:
		
		
		#DNS IP address NordVPN
		
		
		#Checking DNS record propagation https://2ip.me/en/services/information-service/dns-check
		#self.nameservers = ['208.67.222.220', '8.8.8.8', '9.9.9.9', '98.113.146.9', '12.121.117.201', '66.206.166.2', '5.11.11.5', '163.172.107.158', '212.230.255.1', '194.209.157.109', '83.137.41.9', '194.145.241.6', '84.200.70.40', '200.56.224.11', '200.248.178.54', '103.26.250.4', '1.1.1.1', '61.8.0.113', '210.48.77.68', '164.124.101.2', '202.46.34.75', '31.7.37.37', '115.178.96.2', '58.27.149.60', '185.83.212.30', '103.146.221.20', '8.8.4.4', '64.6.64.6', '208.67.220.220', '209.244.0.3', '1.0.0.1', '208.67.222.222']
		self.answer=None
		self.results=None
		self.recv_records={}
		self.recv_records[host]={}
	def nslookup(self,host="amazon.com",record="A"):
		try:
			results=[]
			res=dns.resolver.Resolver()
			res.timeout = 0.6
			res.lifetime = 0.6
			res.nameservers = [self.nameserver]
			answers = res.resolve(host,record)
			if self.record==self.records[6]: answers = answers.find_rrset(answers.answer, self.host, dns.rdataclass.IN, dns.rdatatype.NS)
			for rdata in answers:
				if record=="MX":
					answer=('%s' % rdata.exchange)
					print(host+".","IN", record,rdata.preference,answer)
				elif record=="NS": answer=('%s' % rdata.target)
				else: answer=('%s' % rdata)
				if answer.endswith("."): answer=answer[:-1]
				results.append(answer)
				if record=="CNAME": print(host+".","IN",record,answer+".")
				else: print(host+".","IN",record,answer)
			if record=="CNAME": return answer
			else: return results
		except Exception as error:
			#raise error
			if record!="CNAME": print(host+".","IN",record,"None")
			return None
	def nslookup_record(self):
		for record in self.records:
			self.record=record
			if record=="CNAME": recv=self.resolve_cname(self.host,self.nameserver)
			else: recv=self.nslookup(self.host,self.record)
			if recv is not None:
				self.recv_records[self.host][self.nameserver][self.record]=recv
		return self.recv_records
	def nslookup_nameserver(self):
		for self.nameserver in self.nameservers:
			self.recv_records[self.host][self.nameserver]={}
			print("Nameserver response:",self.nameserver,self.host)
			self.nslookup_record()
		return self.recv_records
	def resolve_cname(self,host,nameserver):
		results={}
		results=self.resolve_cname_c(host,nameserver,results)
		return results
	def resolve_cname_c(self,host,nameserver,results):
		self.nameserver=nameserver
		answer = self.nslookup(host,"CNAME")
		if answer==None:
			response=self.nslookup(host,"A")
			results[host]=response
		elif ip_address.get_ip_address_valid(answer)==False: 
			results[host]=answer
			self.resolve_cname_c(answer,nameserver,results)
		return results
if __name__ == '__main__':
	w=dns_response('amazonaws.com')
	print(w.nslookup_nameserver())