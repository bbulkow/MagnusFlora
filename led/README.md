## Setting up the leds on a raspberry pi

### Add the fadecandy server

Either get the fadecandy github repo and build it fresh, which gives you a fcserver binary in the server directory,
or use the server checked in here, which is built for Debian jessie Raspberry PI 3.

Copy the fcserver to /usr/local/bin ( sudo of course )

Copy the magnus_flora.json , which includes the config for the 4 fade candies we have, to /usr/local/bin

### Set the fadecandy server to auto-restart using supervisord

Make sure supervisord is intalled

```
sudo apt-get install supervisor
```

Copy the configuration file

```
sudo cp fserver.conf /etc/supervisor/conf.d
```

### Validate

Reboot the rpi

1. Validate fcserver is running - ps -aux

2. Check the webpage http://host:7890/

which should have your attached web pages and allow you to do things


