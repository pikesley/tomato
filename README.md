Simple python script to backup the config from my Tomato router
---------------------------------------------------------------

I borrowed the idea from Gregg Hansen's excellent bash script:

    http://beekl.es/5w

and rewrote it in python. My version can now handle multiple devices, too, and has got a lot more objecty.

Using it
--------

You will require:

* python-yaml (apt-get install python-yaml on Ubuntu-ish systems, there's presumably a python egg too)
* https enabled on your router (python urllib makes no pretence of validating an SSL cert so a fake one is fine)

Then it's very simple, cp config/config.yaml-sample to config/config.yaml and fill in the details, then run ./backup.py (runs fine from cron etc.)

It works for me, but please be aware that is a quick hack I threw together in about an hour. If you're using it to backup your mission-critical multi-million-dollar infrastructure, well, you probably want to test it more than I did.

This is also an excuse to play with github :)

