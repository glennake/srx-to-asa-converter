#!/usr/bin/env python2.7

# (C) 2017, Glenn Akester
#
# Contributors: Eugene Khabarov
#
# Title: SRX to ASA Converter v1.4
# Description: Python script to convert Juniper SRX configuration to Cisco ASA.
#
# SRX to ASA Converter is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SRX to ASA Converter is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# If you don't have a copy of the GNU General Public License,
# it is available here <http://www.gnu.org/licenses/>.

# Import modules

import argparse
import netaddr
import re

# Get configuration filepath from args

parser = argparse.ArgumentParser()
parser.add_argument("inputFile", help="/full/path/to/config")
args = parser.parse_args()

# Read config file to variable

with open(args.inputFile, "r") as configFile:
    config = configFile.read()

# Define object name pattern

obj_name_pattern = "[A-Za-z0-9\/._-]{1,}"

# Convert system host name

hostname = re.search(r"(set system host-name ([A-Za-z0-9._-]{1,}))", config)
if hostname is not None:
    print "hostname " + hostname.group(2)

# Get local networks

localnetworks = {}

netnum = 0

asa_seczones = set()

for n in re.finditer(
    r"set interfaces ((pp|reth|ae|fe|ge|xe)(-[0-9]{1,2}\/[0-9]{1,2}\/)?[0-9]{1,2}) unit ([0-9]{1,4}) family inet address ([0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}\/[0-9]{1,2})",
    config,
):
    intf = n.group(1) + "." + n.group(4)
    netw = n.group(5)
    unit = n.group(4)

    localnetworks[netw] = {}
    localnetworks[netw]["intf"] = intf
    localnetworks[netw]["vlan"] = unit

    seczone = re.search(
        r"set security zones security-zone ("
        + obj_name_pattern
        + ") interfaces "
        + intf,
        config,
    )

    if seczone is not None:
        localnetworks[netw]["seczone"] = seczone.group(1)
        if seczone.group(1) not in asa_seczones:
            asa_seczones.add(seczone.group(1))
    else:
        localnetworks[netw]["seczone"] = "undefined"

    netnum += 1

# Create ASA security zones

for values in asa_seczones:
    print "zone " + str(values)

# Convert CIDR subnet mask to dot decimal

config = re.sub(
    r"([0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3})(\/32)",
    r"\1 255.255.255.255",
    config,
)
config = re.sub(
    r"([0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3})(\/31)",
    r"\1 255.255.255.254",
    config,
)
config = re.sub(
    r"([0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3})(\/30)",
    r"\1 255.255.255.252",
    config,
)
config = re.sub(
    r"([0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3})(\/29)",
    r"\1 255.255.255.248",
    config,
)
config = re.sub(
    r"([0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3})(\/28)",
    r"\1 255.255.255.240",
    config,
)
config = re.sub(
    r"([0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3})(\/27)",
    r"\1 255.255.255.224",
    config,
)
config = re.sub(
    r"([0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3})(\/26)",
    r"\1 255.255.255.192",
    config,
)
config = re.sub(
    r"([0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3})(\/25)",
    r"\1 255.255.255.128",
    config,
)
config = re.sub(
    r"([0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3})(\/24)",
    r"\1 255.255.255.0",
    config,
)
config = re.sub(
    r"([0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3})(\/23)",
    r"\1 255.255.254.0",
    config,
)
config = re.sub(
    r"([0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3})(\/22)",
    r"\1 255.255.252.0",
    config,
)
config = re.sub(
    r"([0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3})(\/21)",
    r"\1 255.255.248.0",
    config,
)
config = re.sub(
    r"([0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3})(\/20)",
    r"\1 255.255.240.0",
    config,
)
config = re.sub(
    r"([0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3})(\/19)",
    r"\1 255.255.224.0",
    config,
)
config = re.sub(
    r"([0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3})(\/18)",
    r"\1 255.255.192.0",
    config,
)
config = re.sub(
    r"([0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3})(\/17)",
    r"\1 255.255.128.0",
    config,
)
config = re.sub(
    r"([0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3})(\/16)",
    r"\1 255.255.0.0",
    config,
)
config = re.sub(
    r"([0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3})(\/15)",
    r"\1 255.254.0.0",
    config,
)
config = re.sub(
    r"([0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3})(\/14)",
    r"\1 255.252.0.0",
    config,
)
config = re.sub(
    r"([0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3})(\/13)",
    r"\1 255.248.0.0",
    config,
)
config = re.sub(
    r"([0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3})(\/12)",
    r"\1 255.240.0.0",
    config,
)
config = re.sub(
    r"([0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3})(\/11)",
    r"\1 255.224.0.0",
    config,
)
config = re.sub(
    r"([0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3})(\/10)",
    r"\1 255.192.0.0",
    config,
)
config = re.sub(
    r"([0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3})(\/9)",
    r"\1 255.128.0.0",
    config,
)
config = re.sub(
    r"([0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3})(\/8)", r"\1 255.0.0.0", config
)
config = re.sub(
    r"([0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3})(\/7)", r"\1 254.0.0.0", config
)
config = re.sub(
    r"([0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3})(\/6)", r"\1 252.0.0.0", config
)
config = re.sub(
    r"([0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3})(\/5)", r"\1 248.0.0.0", config
)
config = re.sub(
    r"([0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3})(\/4)", r"\1 240.0.0.0", config
)
config = re.sub(
    r"([0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3})(\/3)", r"\1 224.0.0.0", config
)
config = re.sub(
    r"([0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3})(\/2)", r"\1 192.0.0.0", config
)
config = re.sub(
    r"([0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3})(\/1)", r"\1 128.0.0.0", config
)
config = re.sub(
    r"([0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3})(\/0)", r"\1 0.0.0.0", config
)

# Convert interfaces

# intfnum = 0

for n in re.finditer(
    r"(set interfaces ((pp|reth|ae|fe|ge|xe)(-[0-9]{1,2}\/[0-9]{1,2}\/)?([0-9]{1,2})) unit ([0-9]{1,4}) family inet address ([0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3} [0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}))",
    config,
):
    # if intfnum <= 8:
    seczone = re.search(
        r"set security zones security-zone ("
        + obj_name_pattern
        + ") interfaces "
        + n.group(2)
        + "."
        + n.group(6),
        config,
    )

    if seczone == "trusted" or seczone == "inside":
        seclevel = "100"
    elif seczone == "untrusted" or seczone == "outside":
        seclevel = "0"
    else:
        seclevel = "50"

    if seczone is not None:
        # nameif will be seczone name + vlan to make it unique
        print "interface GigabitEthernet0/" + n.group(5) + "." + n.group(
            6
        ) + "\n vlan " + n.group(6) + "\n nameif " + seczone.group(1) + n.group(
            6
        ) + "\n zone-member " + seczone.group(
            1
        ) + "\n security-level " + seclevel + "\n ip address " + n.group(
            7
        )
    else:
        print "interface GigabitEthernet0/" + n.group(5) + "." + n.group(
            6
        ) + "\n vlan " + n.group(
            6
        ) + "\n nameif undefined\n security-level 0\n ip address " + n.group(
            7
        )

# intfnum += 1

# Convert static routes

for n in re.finditer(
    r"set routing-options static route ([0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3} [0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}) next-hop ([0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3})",
    config,
):
    for key, value in localnetworks.iteritems():
        if netaddr.IPAddress(n.group(2)) in netaddr.IPNetwork(key):
            print "route " + value["seczone"] + " " + n.group(1) + " " + n.group(2)

# Define static applications

applications = {}

applications["any"] = {}
applications["any"]["protocol"] = "ip"
applications["any"]["type"] = "object"

# Define junos default applications

applications["junos-icmp-all"] = {}
applications["junos-icmp-all"]["protocol"] = "icmp"
applications["junos-icmp-all"]["direction"] = "destination"
applications["junos-icmp-all"]["port"] = ""
applications["junos-icmp-all"]["type"] = "object"

applications["junos-icmp-ping"] = {}
applications["junos-icmp-ping"]["protocol"] = "icmp"
applications["junos-icmp-ping"]["direction"] = "destination"
applications["junos-icmp-ping"]["port"] = "echo"
applications["junos-icmp-ping"]["type"] = "object"

applications["junos-ping"] = {}
applications["junos-ping"]["protocol"] = "icmp"
applications["junos-ping"]["direction"] = "destination"
applications["junos-ping"]["port"] = "echo"
applications["junos-ping"]["type"] = "object"

applications["junos-pingv6"] = {}
applications["junos-pingv6"]["protocol"] = "icmp6"
applications["junos-pingv6"]["direction"] = "destination"
applications["junos-pingv6"]["port"] = ""
applications["junos-pingv6"]["type"] = "object"

applications["junos-bootpc"] = {}
applications["junos-bootpc"]["protocol"] = "udp"
applications["junos-bootpc"]["direction"] = "destination"
applications["junos-bootpc"]["port"] = "68"
applications["junos-bootpc"]["type"] = "object"

applications["junos-bootps"] = {}
applications["junos-bootps"]["protocol"] = "udp"
applications["junos-bootps"]["direction"] = "destination"
applications["junos-bootps"]["port"] = "67"
applications["junos-bootps"]["type"] = "object"

applications["junos-dhcp-client"] = {}
applications["junos-dhcp-client"]["protocol"] = "udp"
applications["junos-dhcp-client"]["direction"] = "destination"
applications["junos-dhcp-client"]["port"] = "68"
applications["junos-dhcp-client"]["type"] = "object"

applications["junos-dhcp-relay"] = {}
applications["junos-dhcp-relay"]["protocol"] = "udp"
applications["junos-dhcp-relay"]["direction"] = "destination"
applications["junos-dhcp-relay"]["port"] = "67"
applications["junos-dhcp-relay"]["type"] = "object"

applications["junos-dhcp-server"] = {}
applications["junos-dhcp-server"]["protocol"] = "udp"
applications["junos-dhcp-server"]["direction"] = "destination"
applications["junos-dhcp-server"]["port"] = "67"
applications["junos-dhcp-server"]["type"] = "object"

applications["junos-ssh"] = {}
applications["junos-ssh"]["protocol"] = "tcp"
applications["junos-ssh"]["direction"] = "destination"
applications["junos-ssh"]["port"] = "22"
applications["junos-ssh"]["type"] = "object"

applications["junos-http"] = {}
applications["junos-http"]["protocol"] = "tcp"
applications["junos-http"]["direction"] = "destination"
applications["junos-http"]["port"] = "80"
applications["junos-http"]["type"] = "object"

applications["junos-https"] = {}
applications["junos-https"]["protocol"] = "tcp"
applications["junos-https"]["direction"] = "destination"
applications["junos-https"]["port"] = "443"
applications["junos-https"]["type"] = "object"

applications["junos-smtp"] = {}
applications["junos-smtp"]["protocol"] = "tcp"
applications["junos-smtp"]["direction"] = "destination"
applications["junos-smtp"]["port"] = "25"
applications["junos-smtp"]["type"] = "object"

applications["junos-radius"] = {}
applications["junos-radius"]["protocol"] = "udp"
applications["junos-radius"]["direction"] = "destination"
applications["junos-radius"]["port"] = "1812"
applications["junos-radius"]["type"] = "object"

applications["junos-radacct"] = {}
applications["junos-radacct"]["protocol"] = "udp"
applications["junos-radacct"]["direction"] = "destination"
applications["junos-radacct"]["port"] = "1813"
applications["junos-radacct"]["type"] = "object"

applications["junos-sip"] = {}
applications["junos-sip"]["protocol"] = "udp"
applications["junos-sip"]["direction"] = "destination"
applications["junos-sip"]["port"] = "5060"
applications["junos-sip"]["type"] = "object"

applications["junos-syslog"] = {}
applications["junos-syslog"]["protocol"] = "udp"
applications["junos-syslog"]["direction"] = "destination"
applications["junos-syslog"]["port"] = "161"
applications["junos-syslog"]["type"] = "object"

applications["junos-ntp"] = {}
applications["junos-ntp"]["protocol"] = "udp"
applications["junos-ntp"]["direction"] = "destination"
applications["junos-ntp"]["port"] = "123"
applications["junos-ntp"]["type"] = "object"

applications["junos-ftp"] = {}
applications["junos-ftp"]["protocol"] = "tcp"
applications["junos-ftp"]["direction"] = "destination"
applications["junos-ftp"]["port"] = "21"
applications["junos-ftp"]["type"] = "object"

applications["junos-telnet"] = {}
applications["junos-telnet"]["protocol"] = "tcp"
applications["junos-telnet"]["direction"] = "destination"
applications["junos-telnet"]["port"] = "23"
applications["junos-telnet"]["type"] = "object"

applications["junos-sqlnet-v2"] = {}
applications["junos-sqlnet-v2"]["protocol"] = "tcp"
applications["junos-sqlnet-v2"]["direction"] = "destination"
applications["junos-sqlnet-v2"]["port"] = "1521"
applications["junos-sqlnet-v2"]["type"] = "object"

applications["junos-ms-sql"] = {}
applications["junos-ms-sql"]["protocol"] = "tcp"
applications["junos-ms-sql"]["direction"] = "destination"
applications["junos-ms-sql"]["port"] = "1433"
applications["junos-ms-sql"]["type"] = "object"

applications["junos-smb-session"] = {}
applications["junos-smb-session"]["protocol"] = "tcp"
applications["junos-smb-session"]["direction"] = "destination"
applications["junos-smb-session"]["port"] = "445"
applications["junos-smb-session"]["type"] = "object"

applications["junos-ms-rpc"] = {}
applications["junos-ms-rpc"]["protocol"] = "tcp"
applications["junos-ms-rpc"]["direction"] = "destination"
applications["junos-ms-rpc"]["port"] = "135"
applications["junos-ms-rpc"]["type"] = "object"

applications["junos-ms-rpc-tcp"] = {}
applications["junos-ms-rpc-tcp"]["protocol"] = "tcp"
applications["junos-ms-rpc-tcp"]["direction"] = "destination"
applications["junos-ms-rpc-tcp"]["port"] = "135"
applications["junos-ms-rpc-tcp"]["type"] = "object"

applications["junos-ms-rpc-udp"] = {}
applications["junos-ms-rpc-udp"]["protocol"] = "udp"
applications["junos-ms-rpc-udp"]["direction"] = "destination"
applications["junos-ms-rpc-udp"]["port"] = "135"
applications["junos-ms-rpc-udp"]["type"] = "object"

applications["junos-ldap"] = {}
applications["junos-ldap"]["protocol"] = "tcp"
applications["junos-ldap"]["direction"] = "destination"
applications["junos-ldap"]["port"] = "389"
applications["junos-ldap"]["type"] = "object"

applications["junos-nbds"] = {}
applications["junos-nbds"]["protocol"] = "udp"
applications["junos-nbds"]["direction"] = "destination"
applications["junos-nbds"]["port"] = "138"
applications["junos-nbds"]["type"] = "object"

applications["junos-nbname"] = {}
applications["junos-nbname"]["protocol"] = "udp"
applications["junos-nbname"]["direction"] = "destination"
applications["junos-nbname"]["port"] = "137"
applications["junos-nbname"]["type"] = "object"

applications["junos-dns-udp"] = {}
applications["junos-dns-udp"]["protocol"] = "udp"
applications["junos-dns-udp"]["direction"] = "destination"
applications["junos-dns-udp"]["port"] = "53"
applications["junos-dns-udp"]["type"] = "object"

applications["junos-dns-tcp"] = {}
applications["junos-dns-tcp"]["protocol"] = "tcp"
applications["junos-dns-tcp"]["direction"] = "destination"
applications["junos-dns-tcp"]["port"] = "53"
applications["junos-dns-tcp"]["type"] = "object"

applications["junos-pop3"] = {}
applications["junos-pop3"]["protocol"] = "tcp"
applications["junos-pop3"]["direction"] = "destination"
applications["junos-pop3"]["port"] = "110"
applications["junos-pop3"]["type"] = "object"

applications["junos-imap"] = {}
applications["junos-imap"]["protocol"] = "tcp"
applications["junos-imap"]["direction"] = "destination"
applications["junos-imap"]["port"] = "143"
applications["junos-imap"]["type"] = "object"

applications["junos-ike"] = {}
applications["junos-ike"]["protocol"] = "udp"
applications["junos-ike"]["direction"] = "destination"
applications["junos-ike"]["port"] = "500"
applications["junos-ike"]["type"] = "object"

applications["junos-tacacs"] = {}
applications["junos-tacacs"]["protocol"] = "tcp"
applications["junos-tacacs"]["direction"] = "destination"
applications["junos-tacacs"]["port"] = "49"
applications["junos-tacacs"]["type"] = "object"

applications["junos-tacacs-ds"] = {}
applications["junos-tacacs-ds"]["protocol"] = "tcp"
applications["junos-tacacs-ds"]["direction"] = "destination"
applications["junos-tacacs-ds"]["port"] = "65"
applications["junos-tacacs-ds"]["type"] = "object"

applications["junos-tftp"] = {}
applications["junos-tftp"]["protocol"] = "udp"
applications["junos-tftp"]["direction"] = "destination"
applications["junos-tftp"]["port"] = "69"
applications["junos-tftp"]["type"] = "object"

applications["junos-nfs"] = {}
applications["junos-nfs"]["protocol"] = "udp"
applications["junos-nfs"]["direction"] = "destination"
applications["junos-nfs"]["port"] = "111"
applications["junos-nfs"]["type"] = "object"

applications["junos-nfsd-tcp"] = {}
applications["junos-nfsd-tcp"]["protocol"] = "udp"
applications["junos-nfsd-tcp"]["direction"] = "destination"
applications["junos-nfsd-tcp"]["port"] = "2049"
applications["junos-nfsd-tcp"]["type"] = "object"

applications["junos-nfsd-udp"] = {}
applications["junos-nfsd-udp"]["protocol"] = "udp"
applications["junos-nfsd-udp"]["direction"] = "destination"
applications["junos-nfsd-udp"]["port"] = "2049"
applications["junos-nfsd-udp"]["type"] = "object"

applications["junos-netbios-session"] = {}
applications["junos-netbios-session"]["protocol"] = "tcp"
applications["junos-netbios-session"]["direction"] = "destination"
applications["junos-netbios-session"]["port"] = "139"
applications["junos-netbios-session"]["type"] = "object"

applications["junos-winframe"] = {}
applications["junos-winframe"]["protocol"] = "tcp"
applications["junos-winframe"]["direction"] = "destination"
applications["junos-winframe"]["port"] = "1494"
applications["junos-winframe"]["type"] = "object"

applications["junos-sccp"] = {}
applications["junos-sccp"]["protocol"] = "tcp"
applications["junos-sccp"]["direction"] = "destination"
applications["junos-sccp"]["port"] = "2000"
applications["junos-sccp"]["type"] = "object"

# applications['junos-'] = {}
# applications['junos-']['protocol'] = ''
# applications['junos-']['direction'] = ''
# applications['junos-']['port'] = ''
# applications['junos-']['type'] = 'object'

# Convert ranged src/dst port applications to service objects

for n in re.finditer(
    r"(set applications application ("
    + obj_name_pattern
    + ") protocol (tcp|udp)[\r\n]+)(set applications application "
    + obj_name_pattern
    + " (destination|source)-port ([0-9]{1,5}-[0-9]{1,5})[\r\n]+)",
    config,
):
    portrange = n.group(6).replace("-", " ")
    print "object service " + n.group(2) + "\n service " + n.group(
        3
    ) + " destination range " + portrange
    applications[n.group(2)] = {}
    applications[n.group(2)]["protocol"] = n.group(3)
    applications[n.group(2)]["direction"] = n.group(5)
    applications[n.group(2)]["port"] = portrange
    applications[n.group(2)]["type"] = "object"

# Convert single src/dst port applications to service objects

for n in re.finditer(
    r"(set applications application ("
    + obj_name_pattern
    + ") protocol (tcp|udp)[\r\n]+)(set applications application "
    + obj_name_pattern
    + " (destination|source)-port ([0-9]{1,5}|[a-z-]{3,})[\r\n]+)",
    config,
):
    print "object service " + n.group(2) + "\n service " + n.group(
        3
    ) + " destination eq " + n.group(6)
    applications[n.group(2)] = {}
    applications[n.group(2)]["protocol"] = n.group(3)
    applications[n.group(2)]["direction"] = n.group(5)
    applications[n.group(2)]["port"] = n.group(6).replace("-", " ")
    applications[n.group(2)]["type"] = "object"

# Convert ranged src/dst port applications with multiple terms to service object groups

for n in re.finditer(
    r"(set applications application ("
    + obj_name_pattern
    + ") term "
    + obj_name_pattern
    + " protocol (tcp|udp)[\r\n]+)(set applications application "
    + obj_name_pattern
    + " term "
    + obj_name_pattern
    + " (destination|source)-port ([0-9]{1,5}-[0-9]{1,5})[\r\n]+)",
    config,
):
    portrange = n.group(6).replace("-", " ")
    print "object-group service " + n.group(2) + "-" + n.group(3) + " " + n.group(
        3
    ) + "\n port-object range " + portrange
    applications[n.group(2)] = {}
    applications[n.group(2)]["protocol"] = n.group(3)
    applications[n.group(2)]["direction"] = n.group(5)
    applications[n.group(2)]["port"] = portrange
    applications[n.group(2)]["type"] = "group"

# Convert single src/dst port applications with multiple terms to service object groups

for n in re.finditer(
    r"(set applications application ("
    + obj_name_pattern
    + ") term "
    + obj_name_pattern
    + " protocol (tcp|udp)[\r\n]+)(set applications application "
    + obj_name_pattern
    + " term "
    + obj_name_pattern
    + " (destination|source)-port ([0-9]{1,5}||[a-z-]{3,})[\r\n]+)",
    config,
):
    print "object-group service " + n.group(2) + "-" + n.group(3) + " " + n.group(
        3
    ) + "\n port-object eq " + n.group(6)
    applications[n.group(2)] = {}
    applications[n.group(2)]["protocol"] = n.group(3)
    applications[n.group(2)]["direction"] = n.group(5)
    applications[n.group(2)]["port"] = n.group(6).replace("-", " ")
    applications[n.group(2)]["type"] = "group"

# Convert application sets to service object groups

for n in re.finditer(
    r"(set applications application-set ("
    + obj_name_pattern
    + ") application ("
    + obj_name_pattern
    + "))",
    config,
):
    print "object-group service " + n.group(2) + "\n service-object object " + n.group(
        3
    )
    applications[n.group(2)] = {}
    applications[n.group(2)]["protocol"] = "ip"
    applications[n.group(2)]["type"] = "group"

# Define static addresses

addresses = {}

addresses["any"] = {}
addresses["any"]["type"] = "any"

addresses["any-ipv4"] = {}
addresses["any-ipv4"]["type"] = "any"

addresses["any-ipv6"] = {}
addresses["any-ipv6"]["type"] = "any"

# Convert address book addresses to network objects

for addr in re.finditer(
    r"(set security (?:zones security-zone "
    + obj_name_pattern
    + " )?address-book(?: global)? address ("
    + obj_name_pattern
    + ") ([0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3} [0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}))",
    config,
):
    print "object network " + addr.group(2) + "\n subnet " + addr.group(3)
    addresses[addr.group(2)] = {}
    addresses[addr.group(2)]["type"] = "object"

# Convert address book dns name to network objects

for addr in re.finditer(
    r"(set security (?:zones security-zone "
    + obj_name_pattern
    + " )?address-book(?: global)? address ("
    + obj_name_pattern
    + ") dns-name ("
    + obj_name_pattern
    + "))",
    config,
):
    print "object network " + addr.group(2) + "\n fqdn " + addr.group(3)
    addresses[addr.group(2)] = {}
    addresses[addr.group(2)]["type"] = "object"

# Convert address book with network/subnet address sets to network object groups

for addrSet in re.finditer(
    r"(set security (?:zones security-zone "
    + obj_name_pattern
    + " )?address-book(?: global)? address-set ("
    + obj_name_pattern
    + ") address ([0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3} [0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}))",
    config,
):
    print "object-group network " + addrSet.group(
        2
    ) + "\n network-object " + addrSet.group(3)
    addresses[addrSet.group(2)] = {}
    addresses[addrSet.group(2)]["type"] = "group"

# Convert address book address with objects/hosts sets to network object groups

for addrSet in re.finditer(
    r"(set security (?:zones security-zone "
    + obj_name_pattern
    + " )?address-book(?: global)? address-set ("
    + obj_name_pattern
    + ") address ([.A-Za-z0-9_-]{1,}))",
    config,
):
    if re.match(
        r"([0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3})", addrSet.group(3)
    ):
        print "object-group network " + addrSet.group(
            2
        ) + "\n network-object host " + addrSet.group(3)
    else:
        print "object-group network " + addrSet.group(
            2
        ) + "\n network-object object " + addrSet.group(3)
    addresses[addrSet.group(2)] = {}
    addresses[addrSet.group(2)]["type"] = "group"

# Convert address book address sets with nested address sets to network object groups

for addrSetNested in re.finditer(
    r"(set security (?:zones security-zone "
    + obj_name_pattern
    + " )?address-book(?: global)? address-set ("
    + obj_name_pattern
    + ") address-set ("
    + obj_name_pattern
    + "))",
    config,
):
    print "object-group network " + addrSetNested.group(
        2
    ) + "\n group-object " + addrSetNested.group(3)
    addresses[addrSetNested.group(2)] = {}
    addresses[addrSetNested.group(2)]["type"] = "group"

# Convert security policies to access control lists

for policy in re.finditer(
    r"((set security policies from-zone ("
    + obj_name_pattern
    + ") to-zone "
    + obj_name_pattern
    + " policy ("
    + obj_name_pattern
    + ") match source-address ("
    + obj_name_pattern
    + ")[\r\n]+){1,}(set security policies from-zone "
    + obj_name_pattern
    + " to-zone "
    + obj_name_pattern
    + " policy "
    + obj_name_pattern
    + " match destination-address ("
    + obj_name_pattern
    + ")[\r\n]+){1,}(set security policies from-zone "
    + obj_name_pattern
    + " to-zone "
    + obj_name_pattern
    + " policy "
    + obj_name_pattern
    + " match application "
    + obj_name_pattern
    + "[\r\n]+){1,}(set security policies from-zone "
    + obj_name_pattern
    + " to-zone "
    + obj_name_pattern
    + " policy "
    + obj_name_pattern
    + " then (permit)|(reject)|(deny)){1,})",
    config,
):
    for policySrc in re.finditer(
        r"(set security policies from-zone "
        + obj_name_pattern
        + " to-zone "
        + obj_name_pattern
        + " policy "
        + obj_name_pattern
        + " match source-address ("
        + obj_name_pattern
        + "))",
        policy.group(1),
    ):
        if addresses[policySrc.group(2)]["type"] == "object":
            polSrc = policySrc.group(2)
            policySrcType = "object "
        elif addresses[policySrc.group(2)]["type"] == "group":
            polSrc = policySrc.group(2)
            policySrcType = "object-group "
        elif addresses[policySrc.group(2)]["type"] == "any":
            polSrc = "any"
            policySrcType = ""
        else:
            polSrc = policySrc.group(2)
            policySrcType = ""

        for policyDst in re.finditer(
            r"(set security policies from-zone "
            + obj_name_pattern
            + " to-zone "
            + obj_name_pattern
            + " policy "
            + obj_name_pattern
            + " match destination-address ("
            + obj_name_pattern
            + "))",
            policy.group(1),
        ):
            if addresses[policyDst.group(2)]["type"] == "object":
                polDst = policyDst.group(2)
                policyDstType = "object "
            elif addresses[policyDst.group(2)]["type"] == "group":
                polDst = policyDst.group(2)
                policyDstType = "object-group "
            elif addresses[policyDst.group(2)]["type"] == "any":
                polDst = "any"
                policyDstType = ""
            else:
                polDst = policyDst.group(2)
                policyDstType = ""

            for policyApp in re.finditer(
                r"(set security policies from-zone "
                + obj_name_pattern
                + " to-zone "
                + obj_name_pattern
                + " policy "
                + obj_name_pattern
                + " match application ("
                + obj_name_pattern
                + "))",
                policy.group(1),
            ):
                if policyApp.group(2) == "any":
                    print "access-list " + policy.group(
                        3
                    ) + "_in extended permit " + applications[policyApp.group(2)][
                        "protocol"
                    ] + " " + policySrcType + polSrc + " " + policyDstType + polDst
                else:
                    if applications[policyApp.group(2)]["type"] == "object":

                        if (
                            re.match(
                                r"[0-9]{1,5} [0-9]{1,5}",
                                applications[policyApp.group(2)]["port"],
                            )
                            is not None
                        ):
                            portOperator = " range "
                        elif (
                            re.match(
                                r"[0-9]{1,5}", applications[policyApp.group(2)]["port"]
                            )
                            is not None
                        ):
                            portOperator = " eq "
                        else:
                            portOperator = " "

                        print "access-list " + policy.group(
                            3
                        ) + "_in extended permit " + applications[policyApp.group(2)][
                            "protocol"
                        ] + " " + policySrcType + polSrc + " " + policyDstType + polDst + portOperator + applications[
                            policyApp.group(2)
                        ][
                            "port"
                        ]

                    elif applications[policyApp.group(2)]["type"] == "group":
                        print "access-list " + policy.group(
                            3
                        ) + "_in extended permit " + applications[policyApp.group(2)][
                            "protocol"
                        ] + " " + policySrcType + polSrc + " " + policyDstType + polDst + " object-group " + policyApp.group(
                            2
                        )

# Bind access control lists to interfaces

for key, value in localnetworks.iteritems():
    print "access-group " + value["seczone"] + "_in in interface " + value[
        "seczone"
    ] + value["vlan"]

