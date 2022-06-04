#!/usr/bin/env python3
__version__ = "1.5"
import time
import json
import os
import utilities.utility as utility
import utilities.file as file
File = file.Main(print_result=False)
start_time = time.time()
def __get_show_result_parameters__(parameters):
	print('{1}Advanced test parameters{6}:\nPublic IP Address: {4}{7}{0} Time: {5}{8}{0}, Execution time: {5}{9}{0}'.format(utility.Clr.RST, utility.Clr.RED2, utility.Clr.GREEN, utility.Clr.YELLOW, utility.Clr.VIOLET, utility.Clr.PINK, utility.Clr.RST2, parameters["Public IP Address"], time.ctime(parameters["Unix Epoch Time"]),parameters["Execution time Duration"]))
def __get_show_result_parameters_resolve__(parameters, host):
	print('\n\n\n{1}{10:15}{9} host: {3}{4}{0} \nPublic IP Address: {7}{5}{0} Time: {8}{6}{0}'.format(utility.Clr.RST, utility.Clr.GREY2, utility.Clr.GREEN, utility.Clr.YELLOW, host, parameters["Public IP Address"], time.ctime(parameters["Unix Epoch Time"]), utility.Clr.VIOLET, utility.Clr.PINK, utility.Clr.RST2, "Resolve test"))
def __get_show_result_verbose_ping__(verbose_ping, host):
	parameters=verbose_ping["parameters"]
	statistics=verbose_ping["statistics"]
	if statistics["packet_loss"]>0:
		print("{5}{4:15}{6} host: {0}{3:11} {2}{1}completed: False{6}".format(utility.Clr.YELLOW, utility.Clr.RED2, utility.Clr.RST, host, "Ping test", utility.Clr.GREY2, utility.Clr.RST2))
		print(f"{parameters.get('username','anonymous')}@{parameters.get('pcname','2ip')} {parameters.get('currentdirectory','~')} $ ",end='')
		print(f"ping -c {parameters['count']} {parameters['address']}")
		print(f"PING {parameters['address']}({parameters['ip_address']}): {parameters.get('payload_size','56')} data bytes")
		for record in verbose_ping["ping"]:
			if record is None: print("{1}Request timeout for icmp_seq{0}".format(utility.Clr.RST,utility.Clr.RED))
			else: print(f"{record[0]} bytes from {record[1]}: icmp_seq={record[2]} time={record[3]}")
		print("--- {1}{2}{0} ping statistics ---".format(utility.Clr.RST,utility.Clr.YELLOW,parameters['address']))
		print("{3} packets transmitted, {1}{4} packets received{2}, {0}{5:.1f}% packet loss{2}".format(utility.Clr.RED,utility.Clr.GREEN,utility.Clr.RST,statistics['packets_transmitted'],statistics['packets_received'],statistics['packet_loss']))
		print("\n")
	else: print("{5}{4:15}{6} host: {0}{3:11} {2}{1}completed: True{2}".format(utility.Clr.YELLOW, utility.Clr.GREEN, utility.Clr.RST, host, "Ping test", utility.Clr.GREY2, utility.Clr.RST2))
def __get_show_result_verbose_traceroute__(verbose_traceroute, host):
	def __get_show_traceroute__(verbose_traceroute):
		print("traceroute to "+ verbose_traceroute["parameters"]["address"],"("+verbose_traceroute["parameters"]["ip_address"]+")",verbose_traceroute["parameters"]["max_hops"],"hops max",verbose_traceroute["parameters"]["payload_size"],"byte packets")
		for (enum,record) in enumerate(verbose_traceroute["traceroute"],start=1):
			if enum<10: text=" "
			else:text=""
			if record is None: print(f"{enum}{text}  {utility.Clr.RED}* * *{utility.Clr.RST}")
			else: print(f"{enum}{text}  {record[0]} ({record[1]})  {record[2]}")
	if verbose_traceroute["host_reached"]:
		print("{3}Traceroute test{4} host: {0}{5:11}{2} {1}reached: {6}{2}".format(utility.Clr.YELLOW, utility.Clr.GREEN, utility.Clr.RST, utility.Clr.GREY2, utility.Clr.RST2, host, verbose_traceroute["host_reached"]))
	else:
		print("{7}Traceroute test{4} host: {0}{5:11}{2} {3}reached: {6}{4}".format(utility.Clr.YELLOW, utility.Clr.GREEN, utility.Clr.RST, utility.Clr.RED2, utility.Clr.RST2, host, verbose_traceroute["host_reached"], utility.Clr.GREY2))
	if None in verbose_traceroute["traceroute"]:
		print("{6}Traceroute test{4} host: {0}{5:11}{2} {3}luggage: False{4}".format(utility.Clr.YELLOW, utility.Clr.GREEN, utility.Clr.RST, utility.Clr.RED2, utility.Clr.RST2, host, utility.Clr.GREY2))
		print(utility.Clr.GREY+"https://www.freebsd.org/cgi/man.cgi?query=traceroute\n- \"TRACEROUTE System Manager's Manual:\n * * *\nA more interesting example is:\n% traceroute allspice.lcs.mit.edu.\n... only knows what's going on with * * *.\""+utility.Clr.RST)
		__get_show_traceroute__(verbose_traceroute)
	elif verbose_traceroute["host_reached"] is False and not None in verbose_traceroute["traceroute"]: __get_show_traceroute__(verbose_traceroute)
def __get_show_result_resolve__(resolve):
		for record in resolve:
			if resolve["1.1.1.1"].get("A") != None:  check_dns = resolve["1.1.1.1"]["A"][0]
			elif resolve["8.8.4.4"].get("A") != None:  check_dns = resolve["8.8.4.4"]["A"][0]
			
			if resolve[record].get("A") != None:  
				resolve[record]["A"].sort()
				if resolve[record]["A"][0] != check_dns: 
					print("{0}Check DNS record in {1}{4}NS {3:15}{5}{0} propagation {2}{1}".format(utility.Clr.RED, utility.Clr.RST, resolve[record]["A"][0], record, utility.Clr.YELLOW2, utility.Clr.RST2))
				else: print("{0}Check in NS {2:15} completed: True{1}".format(utility.Clr.GREEN, utility.Clr.RST, record))
			elif resolve[record].get("nslookup") != None: 
				resolve[record]["nslookup"]["A"].sort()
				if resolve[record]["nslookup"]["A"] != resolve[record]["nslookup"]["A"][0]: print("{0}Check  DNS record in NS {3} propagation {2}{1}".format(utility.Clr.RED, utility.Clr.RST, resolve[record]["nslookup"]["A"], record))
				else: print("{0}Check DNS record {2}{1}".format(utility.Clr.RED,utility.Clr.RST, resolve[record]["nslookup"]["A"]))
def get_show_results_hosts(results):
	for result in results:
		__get_show_result_parameters__(results[result]["parameters"])
		hosts = results[result]["advanced_test"]
		for host in hosts:
			__get_show_result_parameters_resolve__(hosts[host]["resolve"]["parameters"], host)
			__get_show_result_resolve__(hosts[host]["resolve"])
			__get_show_result_verbose_ping__(hosts[host]["verbose_ping"], host)
			__get_show_result_verbose_traceroute__(hosts[host]["verbose_traceroute"], host)

def get_show_results(results):
	print(results["parameters"])
	#print(results["advanced_test"])
	"""__get_show_result_parameters__(results["parameters"])
	for host in results[:1]:
		__get_show_result_parameters_resolve__(hosts[host]["resolve"]["parameters"], host)
		__get_show_result_resolve__(hosts[host]["resolve"])
		__get_show_result_verbose_ping__(hosts[host]["verbose_ping"], host)
		__get_show_result_verbose_traceroute__(hosts[host]["verbose_traceroute"], host)"""

if __name__ == '__main__':
	dir_parent =  os.path.dirname(__file__);dir_results = "/results/";file_result = "results_2022-05-18_16-35-48_hosts_all.json"
	path_json = dir_parent + dir_results + file_result
	results=json.load(open(path_json))
	
	import pathlib
	
	#file.dir_listing_subdirectories()
	
	def get_show_results_listing():
		#listing_results = File.dir_listing_files_in_this_directory_tree(path="./results", file_extension="json")
		listing_results = File.dir_listing_files_in_this_directory_tree(path= os.path.dirname(__file__) + "/results", file_extension="json")
		#print(file_results)
		for (enum,result) in enumerate(listing_results,start=0):
			#print(file_result.name)
			print("Num #:"+str(enum),result.stem)
		enum_input = ""
		while True:
			enum_input = input("e -EXIT, Num #: 0 - " + str(len(listing_results)-1) + str("\n") + str("Num #:"))
			if enum_input == "e" or int(enum_input)>=len(listing_results): break
			else: 
				get_contents=(listing_results[int(enum_input)])
				print(File.open_json(get_contents))
				break
	get_show_results(get_show_results_listing())
	#list(p.glob('**/*.py'))
	#get_show_results(results)
	
	#results=(file.get_request_text_as_json("https://api.github.com/repos/babyish-retired0m/hostname_advanced_testing/contents/results3?ref=main"))
	
	def github_repos():
		contents_results3=file.get_request_text_as_json("https://api.github.com/repos/babyish-retired0m/hostname_advanced_testing/contents/results?ref=main")
		if "message" in contents_results3:
			if contents_results3["message"].startswith("API rate limit exceeded for"):
				print("API rate limit exceeded, (But here's the good news: Authenticated requests get a higher rate limit. Check out the documentation for more details.), documentation_url https://docs.github.com/rest/overview/resources-in-the-rest-api#rate-limiting")
			elif contents_results3["message"].startswith("Not Found"):
				print("Not Found\nhttps://docs.github.com/rest/reference/repos#get-repository-content")
			else: print(contents_results3)
		else:
			for (enum,result) in enumerate(contents_results3,start=0):
				if result["name"] != ".gitkeep":
					print("Num #:"+str(enum),result["name"])
			enum_input = ""
			while True:
				enum_input = input("e -EXIT, Num #: 1 - "+str(len(contents_results3)-1)+str("\n")+str("Num #:"))
				if enum_input=="e" or int(enum_input)==0 or int(enum_input)>=len(contents_results3): break
				else: 
					get_contents=(contents_results3[int(enum_input)]["download_url"])
					get_show_results(file.get_request_text_as_json(get_contents))
					break
	#github_repos()