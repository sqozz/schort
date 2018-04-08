#!/usr/bin/env python3
import os
import schort
import unittest
import tempfile

class FlaskrTestCase(unittest.TestCase):
	def setUp(self):
		schort.app.config['DATABASE'] = "/home/sqozz/git/schort/data/links.sqlite"
		schort.app.testing = True
		self.app = schort.app.test_client()
		with schort.app.app_context():
			schort.initDB()

	def tearDown(self):
		os.unlink(schort.app.config['DATABASE'])

	def test_entry_page(self):
		ret = self.app.get("/")
		print(ret.data)
		assert True

if __name__ == '__main__':
	RED = '\033[91m'
	BOLD = '\033[1m'
	UNDER = '\033[4m'
	ENDC = '\033[0m'
	print("{col_start}{text}{col_end}".format(text="WARNING:\nThese tests currently destroy your database in data/links.sqlite . Really continue?", col_start=RED + BOLD + UNDER, col_end=ENDC))
	print(ENDC + "[y|" + UNDER + BOLD + "n" + ENDC + "]", end=": ")
	confirmed = input()
	if confirmed == "y":
		unittest.main()
	else:
		print("exit")

# vim: noexpandtab:ts=2:sw=2:sts=2
