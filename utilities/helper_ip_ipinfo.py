# QUERY PARAMETER
# ipinfo.io/[IP address]?token=ec5eb2fca62245
# token=ec5eb2fca62245
# https://github.com/ipinfo/python

import ipinfo
import pprint

# IP address and basic ASN details
# curl ipinfo.io/66.87.125.72/json?token=$TOKEN
# lookup_ASN_details
# https://ipinfo.io/developers

def get_lookup_ip_dict(ip_address, access_token = 'ec5eb2fca62245', print_result = False):
	handler = ipinfo.getHandler(access_token)
	details = handler.getDetails(ip_address)
	if print_result:
		print('\n\ndetails_all:\n\n')
		pprint.pprint(details.all)
		# print('details.city', details.city)#'Mountain View'
		# print('details.loc', details.loc)#'37.3861,-122.0840'
	return details.all


def get_lookup_ip_batc_dict(ip_addresses_list, access_token = 'ec5eb2fca62245', print_result = False):
	handler = ipinfo.getHandler(access_token)
	details = handler.getDetails(ip_address)
	details_all = handler.getBatchDetails(ip_addresses_list)
	if print_result:
		print('\n\ndetails_all:\n\n')
		pprint(details.all)
	return details.all


# listoftuple=[('bob',35,'mgr'),('sue',40,'dev')]
# list(map((lambda row: row[1]), listoftuple))
# list( map( (lambda x: x**2), filter((lambda x: x % 2 ==0), range(10))) )

#dict = list(map(lambda x: x.get('A'),list(map(lambda x: x['1.1.1.1'],list(map(lambda x: adv_test[x]['resolve']['nslookup'],adv_test))))))

# dict=list(map(lambda x: adv_test[x]['resolve']['nslookup'],adv_test))
# list(filter(lambda x: x.get('1.1.1.1'), dict))

# dict = list(filter(lambda x: x.get('1.1.1.1'), list(map(lambda x: adv_test[x]['resolve']['nslookup'],adv_test))))
# list(filter(lambda x: x['1.1.1.1'].get('A'), dict))

# dict = list(filter(lambda x: x['1.1.1.1'].get('A'), list(filter(lambda x: x.get('1.1.1.1'), list(map(lambda x: adv_test[x]['resolve']['nslookup'],adv_test))))))
# list(map(lambda x: x['1.1.1.1']['A'], dict))

# #
# dict = list(map(lambda x: x['1.1.1.1']['A'], list(filter(lambda x: x['1.1.1.1'].get('A'), list(filter(lambda x: x.get('1.1.1.1'), list(map(lambda x: adv_test[x]['resolve']['nslookup'],adv_test))))))))
# #

# dict = list(map( (lambda x: x['1.1.1.1'].get('A')), filter(lambda x: x.get('1.1.1.1'), list(map( lambda x: adv_test[x]['resolve']['nslookup'],adv_test ))) ))
# list(col for row in dict for col in row)

# adv_test = json.load(open('/src/app/hostname_advanced_testing/results/results_2023-01-08_04-03-39_AS-203020_JMJ_hosts_services.json'))['advanced_test']
# list(map(lambda x: x.get('A'),list(map(lambda x: x['1.1.1.1'],list(map(lambda x: adv_test[x]['resolve']['nslookup'],adv_test))))))

# list(map(lambda x: adv_test[x]['resolve']['nslookup'], list(filter(lambda x: adv_test[x].get('resolve'), adv_test))))

###
## ip_list = list(col for row in list(map( (lambda x: x['1.1.1.1'].get('A')), filter(lambda x: x.get('1.1.1.1'), list(map( lambda x: adv_test[x]['resolve']['nslookup'], adv_test ))) )) for col in row)
# ip_list = list(col for row in list(map( (lambda x: x['1.1.1.1'].get('A')), filter(lambda x: x.get('1.1.1.1'), list(map( lambda x: adv_test[x]['resolve']['nslookup'], list(filter(lambda x: adv_test[x].get('resolve'), adv_test)) ))) )) for col in row)
# ip_list = list(col for row in list(map(lambda x: adv_test[x]['resolve']['nslookup'], list(filter(lambda x: adv_test[x].get('resolve'), adv_test)))) for col in row)




###
"""
import json
adv_test = json.load(open('/src/app/hostname_advanced_testing/results/results_2023-01-08_04-03-39_AS-203020_hosts_services.json'))['advanced_test']
ip_list_adv_test = list(col for row in list(filter((lambda x: x), map ((lambda x: x.get('A')), list(map(lambda x: x['1.1.1.1'],list(map(lambda x: adv_test[x]['resolve']['nslookup'], adv_test)))) ))) for col in row)
ip_list=[]
#list(filter(lambda x: ip_list.append(x) if not in ip_list), ip_list_adv_test)
for x in ip_list_adv_test:
	     if x not in ip_list:
	             ip_list.append(x)
list(filter((lambda x: x in ip_list), ip_list_adv_test))

list(filter((lambda x: ip_list_adv_test.remove(x) in ip_list_adv_test), ip_list_adv_test))
"""
###


# adv_test = json.load(open('/src/app/hostname_advanced_testing/results/results_2023-01-13_18-45-49_AS-15895_UA_hosts_services.json'))['advanced_test']

# ip_list_adv_test = list(col for row in list(filter((lambda x: x), map ((lambda x: x.get('A')), list(map(lambda x: x['1.1.1.1'], list(map(lambda x: adv_test[x]['resolve']['nslookup'], adv_test)))) ))) for col in row)

# list( filter(lambda x: x.get('1.1.1.1'), list(map(lambda x: adv_test[x]['resolve']['nslookup'], adv_test))) )[0]

# list(map(lambda x: x, list( filter(lambda x: x.get('1.1.1.1'), list(map(lambda x: adv_test[x]['resolve']['nslookup'], adv_test))) )[0]))

# list( filter( lambda x: x.get('A'), list(filter(lambda x: x.get('A'), list( filter(lambda x: x.get('1.1.1.1'), list(map(lambda x: adv_test[x]['resolve']['nslookup'], adv_test))) )[0])) ))

# list( map(lambda x: x.get('1.1.1.1'), list(map(lambda x: adv_test[x]['resolve']['nslookup'], adv_test))) )[0]

# #list( map(lambda x: x.get('A'), list( map(lambda x: x.get('1.1.1.1'), list(map(lambda x: adv_test[x]['resolve']['nslookup'], adv_test))) )[0] ) )
# list( map(lambda x: x, list( map(lambda x: x['1.1.1.1'].get('A'), list(map(lambda x: adv_test[x]['resolve']['nslookup'], adv_test))) )[0] ) )


# #list( filter(lambda x: x.get('A'), list( filter(lambda x: x.get('1.1.1.1', '208.67.220.220'), list(map(lambda x: adv_test[x]['resolve']['nslookup'], adv_test))) )[0] ) )
# list( filter(lambda x: x.get('A'), list( map(lambda x: x['1.1.1.1'].get('A'), list(map(lambda x: adv_test[x]['resolve']['nslookup'], adv_test))) )[0] ) )

###

#dict = list(map(lambda x: x.get('A'),lambda x: x['1.1.1.1'],list(adv_test[i]['resolve']['nslookup'] for i in adv_test)))

"""
import json
import pprint
adv_test = json.load(open('/src/app/hostname_advanced_testing/results/results_2022-12-11_10-33-30_network_AS-31148_o3.ua.json'))
pprint.pprint(adv_test)
dict = list(map(lambda x: x.get('A'),list(map(lambda x: x['1.1.1.1'],list(adv_test[i]['resolve']['nslookup'] for i in adv_test)))))
for i in dict:
...     if i is not None:
...             for x in i:
...                     if x is not None and x not in list_ip:
...                             list_ip.append(x)
"""


#query domains data separately. Check how you can find domains hosted on IP using Hosted Domains API.
# https://ipinfo.io/developers/hosted-domains
# curl ipinfo.io/domains/8.8.8.8?token=$TOKEN&limit=1000
# map((lambda x: print(x)), details_all)
# {
#   "ip": "8.8.8.8",
#   "total": 11606,
#   "domains": [
#     "41.cn",
#     "onionflix.cc",
#     "newmax.info",
#     "ftempurl.com",
#     "itempurl.com"
#   ]
# }

if __name__ == '__main__':
	get_lookup_ip_dict(ip_address='1.1.1.1', print_result = True)