#!/usr/bin/env python3
"""
--------------------------------------------------------------------------------
	CROZONO - 22.02.16.20.00.00 - www.crozono.com - info@crozono.com

	LAN attack module - Get a Metasploit console through a reverse connection
--------------------------------------------------------------------------------

"""
import subprocess

from poormanslogging import info, warn, error
from src.attacks.base_attack import BaseAttack

class metasploit(BaseAttack):

	def __init__(self, p):
		pass

	def run(self):
		info("Running Metasploit...")
		proc = subprocess.call(["msfconsole"], stderr=subprocess.DEVNULL)

	def setup(self):
		pass

	def check(self):
		dep = 'msfconsole'
		if subprocess.call(["which", dep],stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) != 0:
			error("Required binary for {bin} not found.".format(bin=dep))
			return False
		else:
			return True
