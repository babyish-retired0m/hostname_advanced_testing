#!/usr/bin/env python3
__version__ = "1.0"
"""
    icmplib
    The power to forge ICMP packets and do ping and traceroute.
        https://github.com/ValentinBELYN/icmplib
    :copyright: Copyright 2017-2022 Valentin BELYN.
    :license: GNU LGPLv3, see the LICENSE for details.
    
    
    --- fbi.gov ping statistics ---
16 packets transmitted, 16 packets received, 0.0% packet loss
round-trip min/avg/max/stddev = 2.168/2.301/2.467/0.085 ms
"""
from time import sleep
try:
	from icmplib import ICMPv4Socket, ICMPv6Socket, ICMPRequest
	from icmplib import ICMPLibError, ICMPError, TimeoutExceeded
	from icmplib import PID, is_ipv6_address
	from icmplib import resolve, is_hostname
except ImportError:
    raise SystemExit("Please install icmplib, pip3 install icmplib (https://github.com/ValentinBELYN/icmplib)")

def verbose_ping(address, count=10, interval=0.05, timeout=0.2, id=PID):
	#count=4, interval=1, timeout=2,
	#count=10, interval=0.05, timeout=0.10
	results = {}
	# We perform a DNS lookup if a hostname or an FQDN is passed in
	# parameters.
	if is_hostname(address):
		try: ip_address = resolve(address)[0]
		except:
			print(f"The name '{address}' cannot be resolved")
			return None
	else: ip_address = address
	results[address]={}
	# A payload of 56 bytes is used by default. You can modify it using
	# the 'payload_size' parameter of your ICMP request.
	payload_size=56
	
	
	def getpcname():
		from os import environ
		from platform import node
		from socket import gethostname
		n1 = node()
		n2 = gethostname()
		n3 = environ.get("COMPUTERNAME")
		if n1 == n2 == n3:
			pcname = n1
		elif n1 == n2:
			pcname = n1
		elif n1 == n3:
			pcname = n1
		elif n2 == n3:
			pcname = n2
		else:
			raise Exception("Computernames are not equal to each other")
		if pcname.endswith('.local'): return pcname[:pcname.find('.local')]
		else: return pcname
	def getusername():
		from os import getlogin
		from getpass import getuser
		n1=getlogin()
		n2=getuser()
		if n1 == n2: user = n1
		elif n2 == 'root': user = n1
		else: raise Exception("Username are not equal to each other")
		return user
	def getcurrentdirectory():
		from os import getcwd,path
		n1=getcwd() 
		n2=path.expanduser('~')
		if n1 == n2: return '~'
		else: return n1
	results[address]['parameters']={'address':address,'ip_address':ip_address,'count':count,'interval':interval,'timeout':timeout,'id':id,'payload_size':payload_size,'username':getusername(),'pcname':getpcname(),'currentdirectory':getcurrentdirectory()}
	print(f'{getusername()}@{getpcname()} {getcurrentdirectory()}$ ping -c {count} -s {payload_size} -t {timeout} -W {interval} {address}')
	print(f'PING {address}({ip_address}): {payload_size} data bytes')
	
	# We detect the socket to use from the specified IP address
	if is_ipv6_address(address):
		sock = ICMPv6Socket()
	else:
		sock = ICMPv4Socket()
	#ttl = 1
	results[address]['ping'] = []
	for sequence in range(count):
		# We create an ICMP request
		request = ICMPRequest(
			destination=address,
			id=id,
			sequence=sequence,
			#ttl=ttl,
			payload_size=payload_size)
	
		try:
			# We send the request
			sock.send(request)
	
			# We are awaiting receipt of an ICMP reply
			reply = sock.receive(request, timeout)
	
			# We received a reply
			# We display some information
			print(f'{reply.bytes_received} bytes from '
				  f'{reply.source}: ', end='')
	
			# We throw an exception if it is an ICMP error message
			reply.raise_for_status()
	
			# We calculate the round-trip time and we display it
			round_trip_time = (reply.time - request.time) * 1000
	
			print(f'icmp_seq={sequence} '
				  f'time={round(round_trip_time, 3)} ms')
			results[address]['ping'].append([reply.bytes_received,reply.source,sequence,str(round(round_trip_time, 3))+' ms'])
	
			# We wait before continuing
			if sequence < count - 1:
				sleep(interval)
	
		except TimeoutExceeded:
			# The timeout has been reached
			print(f'Request timeout for icmp_seq {sequence}')
			results[address]['ping'].append(None)
	
		except ICMPError as err:
			# An ICMP error message has been received
			print(err)
	
		except ICMPLibError:
			# All other errors
			print('An error has occurred.')
	
	print('Completed.')
	results[address]['completed'] = True
	print(f'--- {address} ping statistics ---')
	def packets_count(replies):
		count_received=0
		for reply in replies:
			if reply is None: count_received+=1
		packets_transmitted=len(replies)
		packets_received=packets_transmitted-count_received
		packet_loss=(100/packets_transmitted)*count_received
		return packets_transmitted,packets_received,packet_loss
	packets_transmitted,packets_received,packet_loss=packets_count(results[address]['ping'])
	print(f'{packets_transmitted} packets transmitted, {packets_received} packets received, {packet_loss:.1f}% packet loss')
	results[address]['statistics']={'packets_transmitted':packets_transmitted,'packets_received':packets_received,'packet_loss':packet_loss}
	return results

# This function supports both FQDNs and IP addresses. See the 'resolve'
# function for details.
if __name__ == '__main__':
	import sys
	addresses=[]
	if len(sys.argv) != 2:
		print('usage: %s example.com' % sys.argv[0])
		#sys.exit(1)
		addresses.extend(['fbi.gov','ic3.gov','1.1.1.1','ovh.com'])
	else:
		address=str(sys.argv[1])
		addresses.append(address)
		print(address)
	for address in addresses:
		result=verbose_ping(address)
		print('result',result)