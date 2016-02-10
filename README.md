# schort - It's just is a tiny link shortener
## Installation instructions:
1. Clone this repo into e.g. /opt/schort
2. Create a "data" folder inside the repo which is writable by the webserver
2. Install requirements (see below)
3. Configure your wsgi or fcgi server
4. Configure your webserver that he talks to your wsgi/fcgi server

## Requirements:

| Module        | Explanation   |
| ------------- |---------------|
| Flask         | Flask handels all HTTP-stuff in this application |
| sqlite3       | In gentoo this useflag needs to be set while compiling python3     |

## µWSGI

The schort.wsgi file can be set as UWSGI_PROGRAM if you use uWSGI.
Keep in mind, that the UWSGI_DIR needs to be set to the path where schort.py resists.
This is because schort is not installed in a global scope. Since schort.wsgi imports schort.py it needs his workspace in the same folder.
