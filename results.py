#!/usr/bin/env python3
__version__ = "1.1"
import time
import json
import os
import utilities.utility as utility
import utilities.file as file
start_time = time.time()
def __get_show_result_parameters__(parameters):
	print('{1}Advanced test parameters{6}:\nPublic IP Address: {4}{7}{0} Time: {5}{8}{0}, Execution time: {5}{9}{0}'.format(utility.Clr.RST, utility.Clr.RED2, utility.Clr.GREEN, utility.Clr.YELLOW, utility.Clr.VIOLET, utility.Clr.PINK, utility.Clr.RST2, parameters["Public IP Address"], time.ctime(parameters["Unix Epoch Time"]),parameters["Execution time Duration"]))
def __get_show_result_parameters_resolve__(parameters, host):
	print('{1}Resolve test{9}: {3}{4}{0} \nPublic IP Address: {7}{5}{0} Time: {8}{6}{0}'.format(utility.Clr.RST,utility.Clr.RED2,utility.Clr.GREEN,utility.Clr.YELLOW,host,parameters["Public IP Address"],time.ctime(parameters["Unix Epoch Time"]),utility.Clr.VIOLET,utility.Clr.PINK,utility.Clr.RST2))
def __get_show_result_verbose_ping__(verbose_ping, host):
	parameters=verbose_ping["parameters"]
	statistics=verbose_ping["statistics"]
	if statistics["packet_loss"]>0:
		print(f"{parameters.get('username','anonymous')}@{parameters.get('pcname','2ip')} {parameters.get('currentdirectory','~')} $ ",end='')
		print(f"ping -c {parameters['count']} {parameters['address']}")
		print(f"PING {parameters['address']}({parameters['ip_address']}): {parameters.get('payload_size','56')} data bytes")
		for record in verbose_ping["ping"]:
			if record is None: print("{1}Request timeout for icmp_seq{0}".format(utility.Clr.RST,utility.Clr.RED))
			else: print(f"{record[0]} bytes from {record[1]}: icmp_seq={record[2]} time={record[3]}")
		print("--- {1}{2}{0} ping statistics ---".format(utility.Clr.RST,utility.Clr.YELLOW,parameters['address']))
		print("{3} packets transmitted, {1}{4} packets received{2}, {0}{5:.1f}% packet loss{2}".format(utility.Clr.RED,utility.Clr.GREEN,utility.Clr.RST,statistics['packets_transmitted'],statistics['packets_received'],statistics['packet_loss']))
		print("\n")
	else: print("{0}{3} {2}{4:11} {1}completed: true{2}".format(utility.Clr.YELLOW,utility.Clr.GREEN,utility.Clr.RST,host,"ping"))
def __get_show_result_verbose_traceroute__(verbose_traceroute, host):
	if verbose_traceroute["host_reached"]: print("{0}{3} {2}{4:11} {1}completed: true{2}".format(utility.Clr.YELLOW,utility.Clr.GREEN,utility.Clr.RST,host,"traceroute"))
	else:
		for (enum,record) in enumerate(verbose_traceroute["traceroute"],start=1):
			if enum<10: text=" "
			else:text=""
			if record is None: print(f"{enum}{text}  {utility.Clr.RED}* * *{utility.Clr.RST}")
			else: print(f"{enum}{text}  {record[0]} ({record[1]})  {record[2]}")
def __get_show_result_resolve__(resolve):
		for record in resolve:
			if "A" in resolve[record]:
				resolve[record]["A"].sort()
				if resolve[record]["A"] != resolve[record]["A"][0]: print("{0}Check DNS record propagation {2}{1}".format(utility.Clr.RED,utility.Clr.RST, record))
			else: print("{0}Check DNS record {2}{1}".format(utility.Clr.RED,utility.Clr.RST, record))
def get_show_results(results):
	for result in results:
		__get_show_result_parameters__(results[result]["parameters"])
		hosts = results[result]["advanced_test"]
		for host in hosts:
			__get_show_result_parameters_resolve__(hosts[host]["resolve"]["parameters"], host)
			__get_show_result_resolve__(hosts[host]["resolve"])
			__get_show_result_verbose_ping__(hosts[host]["verbose_ping"], host)
			__get_show_result_verbose_traceroute__(hosts[host]["verbose_traceroute"], host)
			
if __name__ == '__main__':
	contents_results3=file.get_request_text_as_json("https://api.github.com/repos/babyish-retired0m/hostname_advanced_testing/contents/results3?ref=main")
	if "message" in contents_results3:
		if contents_results3["message"].startswith("API rate limit exceeded for"):
			print("API rate limit exceeded, (But here's the good news: Authenticated requests get a higher rate limit. Check out the documentation for more details.), documentation_url https://docs.github.com/rest/overview/resources-in-the-rest-api#rate-limiting")
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