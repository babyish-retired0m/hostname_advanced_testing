#!/usr/bin/env python3
__version__ = "1.3"
import json
import os
import sys
# sys.path.append("/Users/jozbox/python/functions")

import pathlib
parent_dir = os.path.dirname(__file__)
# print('parent_dir',parent_dir)
parent_dir_parent = pathlib.Path(parent_dir).parent
parent_dir_parent_parent = parent_dir_parent.parent
# print('parent_dir_parent_parent', parent_dir_parent_parent)
sys.path.append(str(parent_dir_parent_parent) + "/utilities")

import file
import utility
import json
import time
#print(pathlib.Path.cwd())
#print(pathlib.Path.home())
#print(sys.path)

File = file.Main(print_result = True)


class Servers_NordVPN(object):
	"""docstring for Servers_NordVPN"""
	def __init__(self, request_servers = True, get_print = True, get_dump_all = False, get_dump_categories = False, get_dump_countries = False):
		super(Servers_NordVPN, self).__init__()

		self.request_servers = request_servers
		self.parent_dir = os.path.dirname(__file__)
		self.get_print = get_print

		self.get_dump_all = get_dump_all
		self.get_dump_categories = get_dump_categories
		self.get_dump_countries = get_dump_countries

		self.servers_categories_dict = {'Standard': 'Standard VPN servers', 'Dedicated': 'Dedicated IP', 'Obfuscated': 'Obfuscated Servers', 'Double': 'Double VPN', 'Onion': 'Onion Over VPN'}


	def get_servers_json(self):
		if self.request_servers:
			servers_json = File.get_request_text_as_json('https://api.nordvpn.com/server')
		elif servers_json is False:
			servers_json = json.load(open(self.parent_dir + "/nordvpn.com_servers.json"))
		else:
			servers_json = json.load(open(self.parent_dir + "/nordvpn.com_servers.json"))
		return servers_json


	def get_servers_categories_dict(self, servers_dict):
		# self.servers_categories = server["categories"][0]["name"]

		# self.servers_standard = []
		# self.servers_dedicated = []
		# self.servers_obfuscated = []
		# self.servers_p2p = []
		# self.servers_double = []
		# self.servers_onion = []
		# self.servers_country = {}
		
		for server in servers_dict:
			# if len(server["categories"]) > 0:
			# 	for category in server["categories"]:
			# 		if category["name"] not in categories_dict:
			# 			categories_dict[category["name"]] = { 'quantity of servers': 0, 'servers id': [] }

			for server_features in server:
				if len(server['categories']) > 0:
					for category in server['categories']:
						if category['name'] not in categories_dict:
							categories_dict[category['name']] = {'quantity_of_servers': 0, 'id': []}
		return categories_dict


	def get_servers_country_dict(self, servers_dict):
		countries_list = []
		countries_dict = {}
		for server in servers_dict:
			for server_features in server:
				if 'country' in server:
					# print("servers_dict[server]['country']", server['country'])
					# print('list(countries_dict)',list(countries_dict))
					if server['country'] not in list(countries_dict.keys()):
						countries_dict[server['country']] = {'quantity_of_servers': 0, 'id': []}
					# if server['country'] not in countries_list:
					# 	countries_list.append({'country': [server['country']], 'quantity_of_servers': 0, 'id': []})
		return countries_dict


	def get_ip_address_dict(self):
		servers_dict = self.get_servers_json()
		ip_address_dict = []
		for server in servers_dict:
			if server['id'] not in ip_address_dict:
				ip_address_dict.append({'id': server['id'], 'ip_address': server['ip_address'], 'domain': server['domain'], 'categories': server['categories']})
		return ip_address_dict

	def get_servers_domain_list(self, category = None):
		servers_dict = self.get_servers_json()
		servers_domain_list = []
		for server in servers_dict:
			if category in server['categories'] and server['domain'] not in servers_domain_list:
				servers_domain_list.append(server['domain'])
			elif category is None and server['domain'] not in servers_domain_list:
				servers_domain_list.append(server['domain'])
		return servers_domain_list


	def get_servers_print(self):
		if self.get_print:
			print('servers_json')
			print(json.dumps(self.servers_json, indent=4))

			print('quantity of servers total', len(self.servers_json))
			print('quantity of servers Standard VPN servers', len(self.servers_standard))
			print('quantity of servers Dedicated IP', len(self.servers_dedicated))
			print('quantity of servers Obfuscated Servers', len(self.servers_obfuscated))
			print('quantity of servers P2P', len(self.servers_p2p))
			print('quantity of servers Double VPN', len(self.servers_double))
			print('quantity of servers Onion Over VPN', len(self.servers_onion))
			print('quantity of servers total summary', len(self.servers_standard) + len(self.servers_dedicated) + len(self.servers_obfuscated) + len(self.servers_double) + len(self.servers_onion))
			print('quantity of servers country', len(self.servers_country))


	def get_servers_dump(self, categories_dict = None, countries_dict = None, servers_dict = None):
		time_local = time.strftime("%Y-%m-%d_%H-%M-%S", utility.get_time_local())
		if self.get_dump_all and self.request_servers and servers_dict:
			File.write_text_as_json(parent_dir + '/' + 'servers_all' + '_' + time_local, servers)

		if self.get_dump_categories and categories_dict:
			servers_list = []
			for category in categories_dict:
				for server_id in category['id']:
					servers_list.append(servers_dict[server_id])
				utility.dirs_make(path = parent_dir + '/categories/')
				File.write_text_as_json(parent_dir + '/categories/' + 'servers_' + category + '_' + time_local, servers_list)

		if self.get_dump_countries and countries_dict:
			servers = []
			for country in countries_dict:
				for server_id in country['id']:
					servers.append(servers_dict[server_id])
				utility.dirs_make(path = parent_dir + '/country/')
				File.write_text_as_json(parent_dir + '/country/' + 'servers_' + country + '_' + time_local, servers)



	def get_servers_dict(self):
		servers_dict = self.get_servers_json()
		categories_dict = self.get_servers_categories_dict(servers_dict)
		countries_dict = self.get_servers_country_dict(servers_dict)
		if servers_dict and categories_dict and country_dict:
			for server in servers_dict:
				if len(server["categories"]) > 0:
					for category in server['categories']:
						if server['id'] not in categories_dict[category]['id']:
							categories_dict[category]['id'].append(server['id'])
							categories_dict[category]['quantity_of_servers'] += 1

					if server['id'] not in countries_dict['country']['id']:
						countries_dict[server['country']]['id'].append(server['id'])
						countries_dict[server['country']]['quantity_of_servers'] += 1

					#if server['id'] not in ip_address_dict:

					if self.get_print:
						print(json.dumps('categories_dict', categories_dict, indent=4))
						print(json.dumps('countries_dict', countries_dict, indent=4))
					self.get_servers_print()

					self.get_servers_dump(servers_dict = servers_dict)
					self.get_servers_dump(categories_dict = categories_dict)
					self.get_servers_dump(countries_dict = countries_dict)

					ip_address
		else:
			print('Error')
			print('get_servers_json is False')




	def get_servers_hostnames_list(self):
		hostnames_list = []
		servers_dict = self.get_servers_json()
		if servers_dict:
			for server in servers_dict:
				if len(server["categories"]) > 0:
					hostnames_list.append(server['domain'])
		return hostnames_list


# for server_features in server:
## print('server', server_features)

# if 'country' in server:
# 	### print('server[country]', server['country'])
# 	if not server['country'] in servers_country:
# 		servers_country[server['country']]={}

# if server["categories"][0]["name"] not in self.servers_categories:
# 	self.servers_categories.append(server["categories"][0]["name"])
# if server["categories"][0]["name"] == "P2P":
# 		servers_p2p.append(server["domain"])
# for name in server["categories"]:
# 	if name["name"] == "Standard VPN servers":
# 		#print(name)
# 		#print(server["domain"])
# 		servers_standard.append(server["domain"])
# 	elif name["name"] == "Dedicated IP":
# 		#print(server["domain"])
# 		servers_dedicated.append(server["domain"])
# 	elif name["name"] == "Obfuscated Servers":
# 		#print(server["domain"])
# 		servers_obfuscated.append(server["domain"])
# 	#elif len(server["categories"]) < 2 and name["name"] == "P2P":
# 		#print(server["domain"])
# 	#	servers_p2p.append(server["domain"])
# 	elif name["name"] == "Double VPN":
# 		#print(server["domain"])
# 		servers_double.append(server["domain"])
# 	elif name["name"] == "Onion Over VPN":
# 		#print(server["domain"])
# 		servers_onion.append(server["domain"])




def servers():
	parent_dir = os.path.dirname(__file__)
	#servers_json = File.get_request_text_as_str('https://api.nordvpn.com/server') or json.load(open(parent_dir + "/nordvpn.com_servers.json"))
	servers_json = File.get_request_text_as_json('https://api.nordvpn.com/server') or json.load(open(parent_dir + "/nordvpn.com_servers.json"))
	# servers_json = servers_json[0]
	#servers_json = json.load(open(parent_dir + "/nordvpn.com_servers.json"))

	# print('servers_json',servers_json)
	# print('servers_json')
	# print(json.dumps(servers_json, indent=4))

	# print(servers_json[0][15])
	# print('servers_json[15]', servers_json[15])

	servers_standard = []
	servers_standard_path = parent_dir + "/servers_standard.txt"
	servers_dedicated = []
	servers_dedicated_path = parent_dir + "/servers_dedicated.txt"
	servers_obfuscated = []
	servers_obfuscated_path = parent_dir + "/servers_obfuscated.txt"
	servers_p2p = []
	servers_p2p_path = parent_dir + "/servers_p2p.txt"
	servers_double = []
	servers_double_path = parent_dir + "/servers_double.txt"
	servers_onion = []
	servers_onion_path = parent_dir + "/servers_onion.txt"
	servers_country = {}

	# servers_json = servers_json[0]
	### print('servers_json',servers_json)
	print('servers_json')
	print(json.dumps(servers_json, indent=4))

	# for server in servers_json:
	# 	print('server', server)
	# 	print('server["id"]', server['id'])
	# 	print('server["ip_address"]', server['ip_address'])
	# 	# if not isinstance(servers_json[server], dict):
	# 	if not isinstance(server, dict):
	# 		print('servers_json server', servers_json[server])


	for server in servers_json:
		### print('server', server)
		# print('servers_json[server]', servers_json[server_features])

		for server_features in server:
			# print('server', server_features)
			if 'country' in server:
				### print('server[country]', server['country'])
				if not server['country'] in servers_country:
					servers_country[server["country"]]={}
			if len(server["categories"]) > 0:
				if server["categories"][0]["name"] == "P2P":
						servers_p2p.append(server["domain"])
				for name in server["categories"]:
					if name["name"] == "Standard VPN servers":
						#print(name)
						#print(server["domain"])
						servers_standard.append(server["domain"])
					elif name["name"] == "Dedicated IP":
						#print(server["domain"])
						servers_dedicated.append(server["domain"])
					elif name["name"] == "Obfuscated Servers":
						#print(server["domain"])
						servers_obfuscated.append(server["domain"])
					#elif len(server["categories"]) < 2 and name["name"] == "P2P":
						#print(server["domain"])
					#	servers_p2p.append(server["domain"])
					elif name["name"] == "Double VPN":
						#print(server["domain"])
						servers_double.append(server["domain"])
					elif name["name"] == "Onion Over VPN":
						#print(server["domain"])
						servers_onion.append(server["domain"])

		# print('servers_json[server][country',servers_json[server]["country"])
		# if not server["country"] in servers_country: 
		# # if not servers_json[server]["country"] in servers_country: 
		# 	servers_country[server["country"]]={}
		# if len(server["categories"]) > 0:
		# 	if server["categories"][0]["name"] == "P2P":
		# 		servers_p2p.append(server["domain"])
		# for name in server["categories"]:
		# 	if name["name"] == "Standard VPN servers":
		# 		#print(name)
		# 		#print(server["domain"])
		# 		servers_standard.append(server["domain"])
		# 	elif name["name"] == "Dedicated IP":
		# 		#print(server["domain"])
		# 		servers_dedicated.append(server["domain"])
		# 	elif name["name"] == "Obfuscated Servers":
		# 		#print(server["domain"])
		# 		servers_obfuscated.append(server["domain"])
		# 	#elif len(server["categories"]) < 2 and name["name"] == "P2P":
		# 		#print(server["domain"])
		# 	#	servers_p2p.append(server["domain"])
		# 	elif name["name"] == "Double VPN":
		# 		#print(server["domain"])
		# 		servers_double.append(server["domain"])
		# 	elif name["name"] == "Onion Over VPN":
		# 		#print(server["domain"])
		# 		servers_onion.append(server["domain"])
	print("quantity of servers total",len(servers_json))
	print("quantity of servers Standard VPN servers",len(servers_standard))
	print("quantity of servers Dedicated IP",len(servers_dedicated))
	print("quantity of servers Obfuscated Servers",len(servers_obfuscated))
	print("quantity of servers P2P",len(servers_p2p))
	print("quantity of servers Double VPN",len(servers_double))
	print("quantity of servers Onion Over VPN",len(servers_onion))
	print("quantity of servers total summary",len(servers_standard)+len(servers_dedicated)+len(servers_obfuscated)+len(servers_double)+len(servers_onion))
	print("length servers_country",len(servers_country))

	"""file.write_list_as_text(servers_standard_path, servers_standard)
	file.write_list_as_text(servers_dedicated_path, servers_dedicated)
	file.write_list_as_text(servers_obfuscated_path, servers_obfuscated)
	file.write_list_as_text(servers_p2p_path, servers_p2p)
	file.write_list_as_text(servers_double_path, servers_double)
	file.write_list_as_text(servers_onion_path, servers_onion)"""


	# print(servers_country)
	# print('servers_json', servers_json)

if __name__ == '__main__':
	import servers_nordvpn as hosts_nordvpn
	NordVPN = hosts_nordvpn.Servers_NordVPN()
	servers_json = NordVPN.get_servers_dict()