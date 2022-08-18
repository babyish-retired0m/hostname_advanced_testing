# Traceroute
In computing, traceroute and tracert are computer network diagnostic commands for displaying possible routes and measuring transit delays of packets across an Internet Protocol network.
# DNS
Is a DNS toolkit for Python. It supports almost all record types. It can be used for queries, zone transfers, and dynamic updates.
Provides both high and low level access to DNS. The high level classes perform queries for data of a given name, type, and class, and return an answer set.
# Ping

# SSL check

## Used to
Traceroute can be used to help identify incorrect routing table definitions or firewalls that may be blocking ICMP traffic, or high port UDP in Unix ping, to a site. A correct traceroute response does not guarantee connectivity for applications as a firewall may permit ICMP packets but not permit packets of other protocols.

## Used by
Traceroute is also used by penetration testers to gather information about network infrastructure and IP address ranges around a given host.

It can also be used when downloading data, and if there are multiple mirrors available for the same piece of data, each mirror can be traced to get an idea of which mirror would be the fastest to use.

## Executing and arguments
This tool requires Python 3.8 or later. 

### Install required Python packages
`pip install -r requirements.txt`

### The arguments:
 **args**       | **Description**					                                   | **Must / Optional**
-----------------| ------------------------------------------------------------------------| -------------------
`-h`, `--help` | Show help message and exit | Optional
`-s`, `--services` | Advanced testing services hostnames get nslookup check, get ping check, get traceroute check, get SSL certificate check. | Optional
`-n`, `--nordvpn` | Advanced testing services hostnames get nslookup check, get ping check, get traceroute check, get SSL certificate check. | Optional
`-g`,	`--google` | Advanced testing services hostnames get nslookup check, get ping check, get traceroute check, get SSL certificate check. | Optional
`-A`, `--amazon` | Advanced testing services hostnames get nslookup check, get ping check, get traceroute check, get SSL certificate check. | Optional
`-v`, `--version` | show program's version number and exit | Optional

## Executing examples:
 ```shell
 sudo python3 start_main_api.py --services
 sudo python3 start_main_api.py --nordvpn
 sudo python3 start_main_api.py --google
 sudo python3 start_main_api.py --amazon
 python3 start_main_api.py --version
 ```
