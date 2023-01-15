from twoip import TwoIP
twoip = TwoIP(key = None)

#Provider API
# Retrieve provider information for the IP address 192.0.2.0 as a dict

#def retrieve_provider_information_for_ip_dict(ip_address):
def retrieve_ip_dict(ip_address):
	return twoip.provider(ip = ip_address)