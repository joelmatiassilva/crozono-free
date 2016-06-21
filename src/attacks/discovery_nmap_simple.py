#!/usr/bin/env python3
"""
--------------------------------------------------------------------------------
	CROZONO - 22.02.16.20.00.00 - www.crozono.com - info@crozono.com

	Network discovery module - Run a NMap scan without parameters
--------------------------------------------------------------------------------

"""
import os
import subprocess
import src.settings as settings

from poormanslogging import info, warn, error
from src.attacks.base_attack import BaseAttack

class nmap_simple(BaseAttack):

	def __init__(self, p):
		pass

	def run(self):
		info("Running NMap -O -sV scan...")
		subprocess.call(['nmap', '-oN', 'cr0z0n0_nmap', '--exclude', settings.IP_LAN, settings.LAN_RANGE], stderr=subprocess.DEVNULL)

	def setup(self):
		# Delete old files:
		nmap_file = os.path.join(settings.OS_PATH,'cr0z0n0_nmap')
		if os.path.exists(nmap_file):
			os.remove(nmap_file)

	def check(self):
		dep = 'nmap'
		if subprocess.call(["which", dep],stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) != 0:
			error("Required binary for {bin} not found.".format(bin=dep))
			return False
		else:
			return True
