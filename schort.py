#!/usr/bin/env python3
from flask import Flask, render_template, url_for, request, redirect, abort, escape
import sqlite3, random, string, time, hashlib, base64
from urllib.parse import urlparse

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
@app.route('/<shortLink>', methods=['GET', 'POST'])
def short(shortLink=""):
	if request.method == "GET":
		if shortLink:
			noauto = shortLink[-1] == "+"
			if noauto: shortLink = shortLink[:-1]
			conn = sqlite3.connect("data/links.sqlite")
			c = conn.cursor()
			result = c.execute('SELECT longLink FROM links WHERE shortLink=?', (shortLink, )).fetchone()
			conn.close()
			if result:
				url = result[0]
				parsedUrl = urlparse(url)
				if parsedUrl.scheme == "":
					url = "http://" + url

				if "resolve" in request.args:
					return escape(url)
				else:
					if noauto:
						url = str(escape(url))
						html = "<a href=" + url + ">" + url + "</a>"
						return html
					else:
						return redirect(url, code=301) # Redirect to long URL saved in the database
			else:
				return render_template("index.html", name=shortLink, message="Enter long URL for "+ request.url_root + shortLink+":", message_type="info") # Custom link page
		else:
			return render_template("index.html", name=shortLink) # Landing page
	elif request.method == "POST": # Someone submitted a new link to short
		longUrl = request.form["url"] # required, accept the exception if the key does not exist
		wishId = request.form.get("wishId")
		if len(longUrl) <= 0:
			abort(400)
		databaseId = insertIdUnique(longUrl, idToCheck=wishId)
		return request.url_root + databaseId # Short link in plain text

def insertIdUnique(longUrl, idToCheck=None):
	hashUrl = hashlib.sha256(longUrl.encode()).digest()
	base64Url = base64.urlsafe_b64encode(hashUrl).decode()
	if idToCheck == None or idToCheck == "":
		idToCheck = base64Url[:4]

	conn = sqlite3.connect("data/links.sqlite")
	c = conn.cursor()
	try:
		c.execute('INSERT INTO links VALUES (?, ?, ?, ?, ?)', (idToCheck, longUrl, int(time.time()), request.remote_addr, "default" ))
		databaseId = idToCheck
		conn.commit()
		conn.close()
	except sqlite3.IntegrityError as e:
		print("Hash already exists, does the long URL matches?")
		longUrlDb = c.execute('SELECT * FROM links WHERE shortLink=?', (idToCheck, )).fetchone()
		if longUrl == longUrlDb[1]:
			print(longUrl + " is already in database with id " + idToCheck + ". Serving old id…")
			databaseId = idToCheck
		else:
			print("Found real hash collision for " + longUrl + " and " + longUrlDb[1])
			conn.commit()
			conn.close()
			if len(base64Url) - 1 >= len(idToCheck) + 1:
				databaseId = insertIdUnique(longUrl, idToCheck=base64Url[:len(idToCheck)+1])
			else:
				print("Can't produce a long enough hash from the new link to be unique. This should never happen")
				print("Bailing out, you are on your own. Good luck.")
				print("=========================================================================================")
				abort(500)

	return databaseId

def initDB():
	conn = sqlite3.connect("data/links.sqlite")
	c = conn.cursor()
	c.execute('''CREATE TABLE IF NOT EXISTS links (shortLink UNIQUE NOT NULL, longLink, timestamp, ip, redirectMethod);''')
	conn.commit()
	conn.close()

if __name__ == '__main__':
	initDB()
	app.run(debug=True) # If you call this file directly it will always run in debug mode. THIS IS VERY DANGEROUS!

# vim: noexpandtab:ts=2:sw=2:sts=2
