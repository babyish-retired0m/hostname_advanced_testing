#!/usr/bin/env python3
__version__ = "1.3"
try:
	import utilities.dns_resolve as dns_resolve
	import utilities.ping as ping
	import utilities.traceroute as traceroute
except ImportError:
	raise SystemExit("Please install dnspython")
try:
	from icmplib import resolve
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
if _ip is None: sys.exit(1)

recv_records={"parameters":{"Unix Epoch Time":utility.get_unix_time(),"Public IP Address":_ip}}
parent_dir = os.path.dirname(__file__) 
cannot_be_resolved = file.open_as_list(parent_dir + "/utilities/cannot_be_resolved.txt")
cannot_be_ssl_checked = file.open_as_list(parent_dir + "/utilities/cannot_be_ssl_checked.txt")

def __get_nslookup__(qname):
	w = dns_resolve.dns_response(qname)
	result = w.nslookup_nameserver()
	recv_records = {"resolve":result[qname]}
	recv_records["resolve"]["parameters"]={"Unix Epoch Time":utility.get_unix_time(),"Public IP Address":_ip,"pcname":utility.getpcname(),"username":utility.getusername(),"currentdirectory":utility.getcurrentdirectory()}
	return recv_records["resolve"]
def __get_ping__(qname):
	result = ping.verbose_ping(qname)
	if result is not None:
		recv_records = {"verbose_ping":result[qname]}
		recv_records["verbose_ping"]["parameters"]["Unix Epoch Time"] = utility.get_unix_time()
		recv_records["verbose_ping"]["parameters"]["Public IP Address"] = _ip
		return recv_records["verbose_ping"]
def __get_traceroute__(qname):
	result=traceroute.verbose_traceroute(qname)
	recv_records = {"verbose_traceroute":result[qname]}
	recv_records["verbose_traceroute"]["parameters"]["Unix Epoch Time"] = utility.get_unix_time()
	recv_records["verbose_traceroute"]["parameters"]["Public IP Address"] = _ip
	return recv_records["verbose_traceroute"]
def __get_ssl_check__(qname):
	if qname not in cannot_be_ssl_checked:
		sslobject = ssl_check.SSLCheck()
		try:
			result = sslobject.show_result([qname])
			if result is not None:
				recv_records = result[qname]
				return recv_records
			else: cannot_be_ssl_checked.append(qname)
		except: print("__get_ssl_check__ cannot_be_ssl_checked")
	else: pass
def get_hostname_advanced_testing(qnames):
	start_time = time.time()
	recv_records["advanced_test"] = {}
	for qname in qnames:
		if len(qname)<=3: pass
		elif qname in cannot_be_resolved: pass
		else:
			try: 
				resolve(qname)
			except:
				print(f"The name '{qname}' cannot be resolved")
				cannot_be_resolved.append(qname)
				pass
			else:
				recv_records["advanced_test"][qname] = {}
				utility.Percents(qnames.index(qname),len(qnames))
				#nslookup
				recv_records["advanced_test"][qname]["resolve"] = __get_nslookup__(qname)
				#ping
				recv_records["advanced_test"][qname]["verbose_ping"] = __get_ping__(qname)
				#traceroute
				recv_records["advanced_test"][qname]["verbose_traceroute"] = __get_traceroute__(qname)
				#ssl_check
				recv_records["advanced_test"][qname]["ssl_cert_info"] = __get_ssl_check__(qname)
	recv_records["parameters"]["Execution time Duration"]='{:.3f}'.format(time.time()- start_time)
	print('duration: {:.3f}'.format(time.time()- start_time))
	os.system('say "get dns resolve jobs done"')
	return recv_records
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
		get_hostnames[hostname] = get_hostname_advanced_testing(hosts)
		json.dump(get_hostnames, fp=open(path_json,'w'),indent=4)
	duration = '{:.3f}'.format(time.time()- _start_time)
	print("Duration:",duration)
	print("cannot be resolved",cannot_be_resolved)
	print("cannot be ssl checked",cannot_be_ssl_checked)
	os.system('say '+"dns resolve jobs done, Duration"+str(duration))
if __name__ == '__main__':
	import os
	import time
	get_hostnames()
	#get_hostname_advanced_testing(["amazonaws.com"])