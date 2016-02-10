#!/usr/bin/env python3
from flask import Flask, render_template, url_for, request, redirect, abort
import sqlite3, random, string, time, hashlib, base64
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
@app.route('/<shortLink>', methods=['GET', 'POST'])
def short(shortLink=""):
	if request.method == "GET":
		conn = sqlite3.connect("links.sqlite")
		c = conn.cursor()
		result = c.execute('SELECT * FROM links WHERE shortLink=?', (shortLink, )).fetchone()
		if result:
			return redirect(result[1], code=302) # Redirect to long URL saved in the database
		else:
				return render_template("index.html", name=shortLink, message="Enter long URL for "+ request.url_root + shortLink+":", message_type="info") # Does the user wish to create a personel short link?
	elif request.method == "POST": # Someone submitted a new link to short
		wishId = request.form["wishId"]
		longUrl = request.form["url"]
		if not wishId:
			databaseId = insertIdUnique("", longUrl)
		else:
			databaseId = insertIdUnique(wishId, longUrl)
		return request.url_root + databaseId # TODO: Give the user a nice site where he can see his short URL

def insertIdUnique(idToCheck, longUrl):
	hashUrl = hashlib.sha256(longUrl.encode()).hexdigest()
	base64Url = base64.b64encode(hashUrl.encode()).decode()
	if len(idToCheck) == 0:
		idToCheck = base64Url[:4]

	conn = sqlite3.connect("links.sqlite")
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
				databaseId = insertIdUnique(base64Url[:len(idToCheck)+1], longUrl)
			else:
				print("Can't produce a long enough hash from the new link to be unique. This should never happen")
				print("Bailing out, you are on your own. Good luck.")
				print("=========================================================================================")
				abort(500)

	return databaseId

def initDB():
	conn = sqlite3.connect("links.sqlite")
	c = conn.cursor()
	c.execute('''CREATE TABLE IF NOT EXISTS links (shortLink UNIQUE NOT NULL, longLink, timestamp, ip, redirectMethod);''')
	conn.commit()
	conn.close()
	print("DB init")

if __name__ == '__main__':
	initDB()
	app.run(debug=True)
