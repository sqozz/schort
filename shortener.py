#!/usr/bin/env python3
from flask import Flask, render_template, url_for, request, redirect
import sqlite3, random, string, time, hashlib, base64
app = Flask(__name__)

#@app.route('/')
#def root():
#	return render_template("index.html", name=shortLink, message="Enter long URL for "+ request.url_root + shortLink+":", message_type="info")

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
		conn = sqlite3.connect("links.sqlite")
		c = conn.cursor()
		wishId = request.form["wishId"]
		longUrl = request.form["url"]
		if not wishId:
			hashUrl = hashlib.sha256(longUrl.encode()).hexdigest()
			base64Url = base64.b64encode(hashUrl.encode()).decode()
			databaseId = base64Url[:4]
		else:
			databaseId = wishId

		c.execute('INSERT INTO links VALUES (?, ?, ?, ?, ?)', (databaseId, longUrl, int(time.time()), request.remote_addr, "default" ))
		conn.commit()
		conn.close()
		return redirect(longUrl, code=302) # TODO: Give the user a nice site where he can see his short URL

def generateId():

	return ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(4))

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
