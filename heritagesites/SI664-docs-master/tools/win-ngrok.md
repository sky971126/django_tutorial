# Windows 10: Using ngrok
SI 664 autograders rely on [ngrok](https://ngrok.com/) to provide your laptop with a temporary HTTP 
tunnel and temporary a temporary internet domain in which to communicate with the web server hosting the autograder 
service.

## Create an account
Visit [ngrok](https://ngrok.com/), click the "SIGN UP" button, and create an account.

## Download
On the [Setup and Installation](https://dashboard.ngrok.com/get-started) page and choose the 
appropriate ngrok archive to download:

Windows: https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-windows-amd64.zip

## Install
Move the *.zip archive to your user's home folder, right-click on the ngrok *.zip and extract its
 contents using Unarchive.

## Copy Auth Token
Copy the `authtoken` command from the ngrok "Setup & Installation" page and run it in the 
terminal. This action will add the token to your `ngrok.yml` configuration file.

```commandline
C:\Users\arwhyte>ngrok authtoken 7rN4M37HazSBhibEKJvca_7Z1x24HRUVmWRGdVMtmAF
Authtoken saved to configuration file: C:\Users\arwhyte/.ngrok2/ngrok.yml
```

## Open a Tunnel on Port 8000

```commandline
C:\Users\arwhyte>ngrok http 8000

```

```commandline
ngrok by @inconshreveable                                                         (Ctrl+C to quit)

Session Status                online
Account                       Anthony Whyte (Plan: Free)
Version                       2.2.8
Region                        United States (us)
Web Interface                 http://127.0.0.1:4040
Forwarding                    http://cb5c9b81.ngrok.io -> localhost:8000
Forwarding                    https://cb5c9b81.ngrok.io -> localhost:8000

Connections                   ttl     opn     rt1     rt5     p50     p90
                              0       0       0.00    0.00    0.00    0.00
```

Type "Control" + "C" (CTRL+C) to close the tunnel.

:warning: Remember that each time you start ngrok, it will assign you a different random address.

## ngrok Inspector
Once you have opened a tunnel open a new browser tab and visit localhost:4040 to 
review tunnel activity. You can inspect HTTP headers and responses as well as replay a request.

## Tweek Django Settings
Open mysite `settings.py` and add a wildcard character ('*') to the `ALLOWED_HOSTS` list property.

```python
ALLOWED_HOSTS = ['*']
``` 

Otherwise you are likely to encounter a `DisallowedHost` exception when using the ngrok temporary 
domain.

## Check ngrok Connection
Construct the ngrok URL by removing the "http://localhost:8000" and replacing it with the 
ngrok-provided URL:

example: `http://localhost:8000/polls/` to `http://cb5c9b81.ngrok.io/polls/`

## Assignments
Whenever you encounter an SI 664 assignment that involves an autograder do the following:

1. Read the exercise directions carefully.
2. Activate your Django project virtual environment.
3. Start the Django development server.
4. Perform the exercise, making changes to your Django app instance as required.
5. Start an ngrok tunnel. 
6. When interacting with the autograder over HTTP replace http://localhost:8000 with the ngrok domain.
7. Make frequent use of the ngrok inspector to monitor the HTTP request/response cycle.
8. After submitting your assignment and receiving a grade close the tunnel.

## ngrok Documentation

The ngrok online [documentation](https://ngrok.com/docs) is well-written and worth exploring.  You can also access the documentation from the terminal:
 
```commandline
C:\Users\arwhyte>ngrok help
```

## License
<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>.