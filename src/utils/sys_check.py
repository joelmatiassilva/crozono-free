#!/usr/bin/env python3
"""
--------------------------------------------------------------------------------
	CROZONO - 22.02.16.20.00.00 - www.crozono.com - info@crozono.com

	Utils - Check core dependencies
--------------------------------------------------------------------------------

"""
import os
import subprocess

from poormanslogging import error

wlan_deps = ["aircrack-ng", "wash"]

def check_wlan_tools_dependencies():
	for d in wlan_deps:
		if subprocess.call(["which", d],stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) != 0:
			error("Required binary for {bin} not found. Refer to the INSTALL document for requirements for running CROZONO.".format(bin=d))
			return False
	return True

def check_root():
	return os.geteuid() == 0
