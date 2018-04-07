#!/usr/bin/env python3
import os
import unittest
import requests

BASE_URL="http://localhost:5000"

class SchortFunctionalTestCase(unittest.TestCase):
	def setUp(self):
		# maybe later
		pass

	def tearDown(self):
		# maybe later
		pass

	def assertPostReq(self, url, data = {}):
		req = requests.post(url, data=data)
		self.assertEqual(req.status_code, 200)
		return req

	def assertGetReq(self, url, params = {}):
		req = requests.get(url, params=params)
		self.assertEqual(req.status_code, 200)
		return req

	def test_entry_page(self):
		req = self.assertGetReq(BASE_URL + "/")
		content = req.text
		self.assertNotEqual(len(content), 0, msg="Get request content was empty.")
		self.assertRegex(content, ".*\<html.*", msg="Didn't find an opening <html tag in the response.")
		self.assertRegex(content, ".*\<div.*", msg="Didn't find any opening <div tag in the response.")

	def test_custom_creation(self):
		req = self.assertPostReq(BASE_URL + "/", data={"url" : "https://github.com/sqozz/schort", "wishId" : "custom_user_supplied_url"})

	def test_easy_api(self):
		'''
		Test if the api is intuitive/easy to implement
		
		While creating the custom_creation test, out of pure laziness, I left out the whishId parameter.
		For intuitive use of the API from a script, this shouldn't be neccessary.
		'''
		req = self.assertPostReq("http://localhost:5000/", data={"url" : "https://github.com/sqozz/schort"})


if __name__ == '__main__':
	unittest.main()

# vim: noexpandtab:ts=2:sw=2:sts=2
