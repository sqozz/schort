#!/usr/bin/env python3
import os
import unittest
import requests
from urllib import parse

BASE_URL="http://localhost:5000"

class WebTestCase(object):
	def assertPostReq(self, url, data = {}):
		req = requests.post(url, data=data)
		self.assertEqual(req.status_code, 200, msg="Post request unsuccessful")
		return req

	def assertGetReq(self, url, params = {}):
		req = requests.get(url, params=params)
		self.assertEqual(req.status_code, 200, msg="Get request unsuccessful")
		return req

	def assertGetStatusReq(self, expected_status, url, params = {}):
		req = requests.get(url, params=params, allow_redirects=False)
		self.assertEqual(req.status_code, expected_status, msg="Returned status code does not match the expected one")

		return req


class SchortBasicTests(unittest.TestCase, WebTestCase):
	def test_entry_page(self):
		"""HTML exists in root page"""
		req = self.assertGetReq(BASE_URL + "/")
		content = req.text
		self.assertNotEqual(len(content), 0, msg="Get request content was empty.")
		self.assertRegex(content, ".*\<html.*", msg="Didn't find an opening <html tag in the response.")
		self.assertRegex(content, ".*\<div.*", msg="Didn't find any opening <div tag in the response.")


class SchortRegressionTests(unittest.TestCase, WebTestCase):
	def test_empty_wish_id(self):
		"""Test a request with an empty wish-URL"""
		req = self.assertPostReq(BASE_URL + "/", data={"url" : "https://github.com/sqozz/schort", "wishId" : ""})
		short_url = req.text
		self.assertNotEqual(short_url, BASE_URL + "/", msg="Created short link cannot be equal to the root URL")

	def test_empty_wish_id(self):
		"""Test a request with no wishId as all"""
		req = self.assertPostReq(BASE_URL + "/", data={"url" : "https://github.com/sqozz/schort"})
		self.assertEqual(req.status_code, 200, msg="Could not handle a request without wishId in the parameter-list")


class SchortShortLinkCase(object):
	pass
	shortID = ""
	shortDest = ""
	req = None

	def test_redirect(self):
		"""Test basic redirecting capabilites of schort"""
		self.assertNotEqual(len(self.shortID), 0)
		req = self.assertGetStatusReq(301, BASE_URL + "/" + self.shortID)
		loc = req.headers.get("location")
		self.assertEqual(loc, self.shortDest)

	def test_redirect_follow(self):
		"""Test if the requests-lib can follow the redirect"""
		req = requests.get(BASE_URL + "/" + self.shortID, allow_redirects=True)
		req.url = self.shortDest

	def test_resolve(self):
		"""Test the resolve parameter"""
		req = self.assertGetReq(BASE_URL + "/" + self.shortID, params = {"resolve" : ""})
		self.assertEqual(req.text, self.shortDest)

	def test_HTMLresolve(self):
		"""Test HTML displaying of the shortened URL"""
		HTML_keyword = "+"
		req = self.assertGetReq(BASE_URL + "/" + self.shortID + HTML_keyword)
		self.assertRegex(req.text, "(<a href=)({url})(>)({url})(</a>)".format(url=self.shortDest), msg="Returned HTML does not match the regex")


class SchortCustomIdTests(unittest.TestCase, SchortShortLinkCase, WebTestCase):
	def setUp(self):
		self.shortID = "custom_user_supplied_url"
		self.shortDest = "https://github.com/sqozz/schort"
		self.req = requests.post(BASE_URL + "/", data={"url" : self.shortDest, "wishId" : self.shortID})

	def test_create(self):
		"""Test short link creation with a custom supplied wish-id"""
		short_url = self.req.text
		self.assertEqual(short_url, BASE_URL + "/" + self.shortID)
		self.assertEqual(self.req.status_code, 200)


class SchortRandomIdTests(unittest.TestCase, SchortShortLinkCase, WebTestCase):
	def setUp(self):
		"""Set up a short url with a randomly assigned id"""
		self.shortDest = "https://github.com/sqozz/schort"
		self.req = requests.post(BASE_URL + "/", data={"url" : self.shortDest})
		aquiredId = parse.urlparse(self.req.text)
		aquiredId = aquiredId.path.replace("/", "", 1)
		self.shortID = aquiredId

	def test_create(self):
		"""Test short link creation with a randomly assigned id"""
		self.assertNotEqual(len(self.shortID), 0)
		self.assertEqual(self.req.status_code, 200, msg="Link creation was unsuccessful")


if __name__ == '__main__':
	suite = unittest.TestSuite()
	suite.addTests(unittest.TestLoader().loadTestsFromTestCase(SchortBasicTests))
	suite.addTests(unittest.TestLoader().loadTestsFromTestCase(SchortRegressionTests))
	suite.addTests(unittest.TestLoader().loadTestsFromTestCase(SchortCustomIdTests))
	suite.addTests(unittest.TestLoader().loadTestsFromTestCase(SchortRandomIdTests))
	unittest.TextTestRunner(verbosity=2).run(suite)

# vim: noexpandtab:ts=2:sw=2:sts=2
