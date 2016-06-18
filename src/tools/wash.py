#!/usr/bin/env python3
"""
--------------------------------------------------------------------------------
	CROZONO - 22.02.16.20.00.00 - www.crozono.com - info@crozono.com

	Tool - Wash is used by CROZONO to discover APs with WPS.
--------------------------------------------------------------------------------

"""
import os
import pexpect

import src.settings as settings

def wash_scan():
	cmd_wash = pexpect.spawn('wash -i {i}'.format(i=settings.INTERFACE_MON))
	cmd_wash.logfile = open(settings.LOG_FILE, 'wb')
	cmd_wash.expect([settings.TARGET_BSSID, pexpect.TIMEOUT, pexpect.EOF], 30)
	cmd_wash.close()

	wps = False
	parse_log_wps = open(settings.LOG_FILE, 'r')
	for line in parse_log_wps:
		if settings.TARGET_BSSID in line:
			wps = True
			break
	parse_log_wps.close()
	os.remove(settings.LOG_FILE)

	return wps