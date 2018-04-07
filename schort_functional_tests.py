#!/usr/bin/env python3
import os
import unittest
import requests

class SchortFunctionalTestCase(unittest.TestCase):
	def setUp(self):
		pass

	def tearDown(self):
		pass

	def assertPostReq(self, url, data = {}):
		req = requests.post(url, data=data)
		self.assertEqual(req.status_code, 200)
		return req

	def test_entry_page(self):
		req = requests.get("http://localhost:5000/")
		self.assertEqual(req.status_code, 200)

	def test_custom_creation(self):
		req = requests.get("http://localhost:5000/")
		self.assertEqual(req.status_code, 200)

	def test_easy_api(self):
		req = self.assertPostReq("http://localhost:5000/", data={"url" : "https://github.com/sqozz/schort"})





if __name__ == '__main__':
	unittest.main()

# vim: noexpandtab:ts=2:sw=2:sts=2
