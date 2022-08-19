#!/usr/bin/env python3
__version__ = "2.6"
try:
    # resolve_mx
    import dns.resolver
    # resolve_ns
    import dns.message
    import dns.rdataclass
    import dns.rdatatype
    import dns.query
except ImportError:
    raise SystemExit("Please install dnspython: pip3 install dnspython")
# resolve_cname
import utilities.ip_address as ip_address
import utilities.file as file
import os
import sys
import utilities.dns_nameserver as dns_nameserver

File = file.Main(print_result=False)


class Dns_response():
    def __init__(self, host=None, records=None, nameserver=None,
                 ip_address_public_answer=ip_address.get_ip_address_public_amazon()):
        # , ip_address_public_answer = None
        self.host = host if isinstance(host, str) and host is not None else print(
            "hostname is None or is hostname str?")
        self.records = ["A", "AAAA", "CNAME", "MX", "SOA", "TXT", "NS"] if records is None else [records] if isinstance(
            records, str) else records
        self.ip_address_pub = ip_address_public_answer

        # nameserver = [nameserver] if isinstance(nameserver, str) else nameserver
        # self.nameservers = self.__get_nameserver__() if nameserver is None else nameserver
        self.nameservers = self.__get_nameserver__() if nameserver is None else [nameserver] if isinstance(nameserver,
                                                                                                           str) else nameserver

        self.recv_records = {self.host: {}}

    # self.answer = None;#self.results = None;
    def __get_nameserver__(self):
        # DNS IP address Public:
        nameservers = ["1.1.1.1"]
        nameservers.extend(["8.8.4.4", "9.9.9.9", "64.6.64.6", "208.67.220.220", "209.244.0.3"])
        # nameservers.extend(["1.0.0.1","8.8.8.8","208.67.222.222"])

        nameservers = dns_nameserver.get_nameserver(self.ip_address_pub, nameservers)

        return nameservers

    def nslookup(self, host="www.facebook.com", record="A"):
        try:
            results = []
            res = dns.resolver.Resolver()
            res.timeout = 0.6
            res.lifetime = 0.6
            res.nameservers = [self.nameserver]

            answers = res.resolve(host, record)
            if record == "NS": answers = answers.find_rrset(answers.answer, host, dns.rdataclass.IN, dns.rdatatype.NS)
            
            #answers = answers.find_rrset(answers.answer, host, dns.rdataclass.IN, dns.rdatatype.NS) if record == "NS" else res.resolve(host, record)


            for rdata in answers:
                if record == "MX":
                    answer = ('%s' % rdata.exchange)
                    print(host + ".", "IN", record, rdata.preference, answer)
                elif record == "NS":
                    answer = ('%s' % rdata.target)
                else:
                    answer = ('%s' % rdata)
                if answer.endswith("."): answer = answer[:-1]
                results.append(answer)
                print(host + ".", "IN", record, answer + ".")
            # print(host + ".", "IN", record, answer + ".") if record == "CNAME" else print(host + ".", "IN", record, answer)
            return answer if record == "CNAME" else results
        except Exception as error:
            print(host + ".", "IN", record, "None")
            # raise error
            # print(host + ".", "IN", record, "None") if record!="CNAME" else print(host + ".", "IN", record, "None")
            return None

    def nslookup_record(self):
        for record in self.records:
            self.record = record
            recv = self.resolve_cname(host=self.host, nameserver=self.nameserver,
                                      results={}) if record == "CNAME" else self.nslookup(host=self.host,
                                                                                          record=self.record)
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

    def resolve_cname(self, host, nameserver, results={}):
        return self.resolve_cname_c(host=host, nameserver=nameserver, results=results)

    def resolve_cname_c(self, host, nameserver, results={}):
        self.nameserver = nameserver
        answer = self.nslookup(host=host, record="CNAME")
        if answer is not None and ip_address.get_ip_address_valid(answer[0]):
            return None
        elif answer == None:
            response = self.nslookup(host=host, record="A")
            results[host] = response
        elif ip_address.get_ip_address_valid(answer) == False:
            results[host] = answer
            self.resolve_cname(host=answer, nameserver=self.nameserver, results=results)
        return results


if __name__ == '__main__':
    Response = Dns_response("amazonaws.com")
    print(Response.get_nslookup())
