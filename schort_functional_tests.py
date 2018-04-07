#!/usr/bin/env python3
import os
import unittest
import requests

BASE_URL="http://localhost:5000"

class TestCase(unittest.TestCase):
	pass

	def assertPostReq(self, url, data = {}):
		req = requests.post(url, data=data)
		self.assertEqual(req.status_code, 200)
		return req

	def assertGetReq(self, url, params = {}):
		req = requests.get(url, params=params)
		self.assertEqual(req.status_code, 200)
		return req


class SchortBasicTests(TestCase):
	def test_entry_page(self):
		"""HTML exists in root page"""
		req = self.assertGetReq(BASE_URL + "/")
		content = req.text
		self.assertNotEqual(len(content), 0, msg="Get request content was empty.")
		self.assertRegex(content, ".*\<html.*", msg="Didn't find an opening <html tag in the response.")
		self.assertRegex(content, ".*\<div.*", msg="Didn't find any opening <div tag in the response.")

class SchortCustomIdTests(TestCase):
	def test_custom_creation(self):
		"""Test user supplied wish-URLs"""
		wishId = "custom_user_supplied_url"
		req = self.assertPostReq(BASE_URL + "/", data={"url" : "https://github.com/sqozz/schort", "wishId" : "custom_user_supplied_url"})
		short_url = req.text
		self.assertEqual(short_url, BASE_URL + "/" + wishId)

	def test_empty_wish_id(self):
		"""Test a request with an empty wish-URL"""
		req = self.assertPostReq(BASE_URL + "/", data={"url" : "https://github.com/sqozz/schort", "wishId" : ""})
		short_url = req.text
		self.assertNotEqual(short_url, BASE_URL + "/", msg="Created short link cannot be equal to the root URL")

class SchortRandomIdTests(TestCase):
	aquiredId = ""

	def test_default(self):
		"""Test default usage of schort"""
		req = self.assertPostReq(BASE_URL + "/", data={"url" : "https://github.com/sqozz/schort", "wishId" : ""})


if __name__ == '__main__':
	suite = unittest.TestSuite()
	suite.addTests(unittest.TestLoader().loadTestsFromTestCase(SchortBasicTests))
	suite.addTests(unittest.TestLoader().loadTestsFromTestCase(SchortRandomIdTests))
	suite.addTests(unittest.TestLoader().loadTestsFromTestCase(SchortCustomIdTests))
	unittest.TextTestRunner(verbosity=2).run(suite)

# vim: noexpandtab:ts=2:sw=2:sts=2
