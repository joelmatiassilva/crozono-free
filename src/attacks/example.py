#!/usr/bin/env python3
"""
--------------------------------------------------------------------------------
	CROZONO - 18.06.16.20.00.00 - www.crozono.com - info@crozono.com

	Attack implementation guideline
--------------------------------------------------------------------------------

"""

from src.attacks.base_attack import BaseAttack

class example(BaseAttack):

	def __init__(self):
		pass

	def setup(self):
		print("Set up necessary for the attack to happen")

	def run(self):
		print("Code to run the attack")

	def check(self):
		print("Is this attack viable?")
		return False
