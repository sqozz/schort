# schort - It's just a tiny link shortener
## Installation instructions:
1. Create a user and adjust permissions to write at least into /opt/schort/data
    1. `sudo mkdir -p /opt/schort`
    2. `sudo groupadd schort`
    3. `sudo useradd -d /opt/schort -g schort -M -s /sbin/nologin schort`
    4. `sudo chown -R schort:schort /opt/schort`
    5. `sudo -u schort git clone https://github.com/sqozz/schort.git /opt/schort`
    6. `sudo chmod 770 /opt/schort/data`
2. Install requirements:
    1. `sudo -u schort virtualenv /opt/schort/venv`
    2. `sudo -u schort -s`
    3. `source ./venv/bin/activate`
    4. `pip install -r requirements.txt`
3. Configure your wsgi or fcgi server:
    1. Check the docs of your preferred server. E.g. gunicorn, uwsgi, fastcgi, …
    2. uwsgi example: `/usr/bin/uwsgi --master --daemonize /dev/null --disable-logging --plugin python39 --wsgi-file /opt/schort/schort.wsgi --post-buffering 1 --enable-threads --socket /tmp/uwsgi_schort.sock --processes 1 --fileserve-mode /opt/schort/schort.wsgi --pidfile /var/run/uwsgi_schort/schort.pid`
4. Configure your webserver that he talks to your wsgi/fcgi server:
    1. Check the docs of your preferred webserver. E.g. nginx, apache, …
    2. nginx example (you should really look into securing your server with https):

```
server {
	listen 80;
	listen [::]:80;
	server_name schort.your.domain;

	sendfile on;
	client_max_body_size 20M;
	keepalive_timeout 0;

	location / { try_files $uri @schort; }
	location @schort {
		include uwsgi_params;
		uwsgi_pass unix:/tmp/uwsgi_schort.sock;
	}
}
```

## Requirements:

| Module        | Explanation   |
| ------------- |---------------|
| Flask         | Flask handels all HTTP-stuff in this application |
| sqlite3       | In gentoo this useflag needs to be set while compiling python3     |

## µWSGI

The schort.wsgi file can be set as UWSGI_PROGRAM if you use uWSGI.
Keep in mind, that the UWSGI_DIR needs to be set to the path where schort.py resists.
This is because schort is not installed in a global scope. Since schort.wsgi imports schort.py it needs his workspace in the same folder.
