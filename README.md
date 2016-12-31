# hassbot
Telegram bot for Home Assistant

View status of your Home Assistant installation via Telegram (from your phone, desktop or anywhere else). Currently, it only understands
two commands: /hello and /status:

/hello:
Only to test that the bot is actually responding
  
/status:
Prints various bits of information about the entities in your system. Optionally, provide a parameter (switch, sensor, door, people
or verbose) to ask for specific information. Without the parameter, it will print a list of all switches that are on, as well as the status
of all other types of supported entities. Special note about "doors": I have magnetic sensors on doors and since they actually show up in
HA as switches I simply prefixed their IDs with "sensor_" (e.g the full entitiy ID is switch.sensor_front_door etc). The bot knows
about this and will print "Front Door is open" rather than "Front Door is on".

Setup:
* You first need to create a bot following [these instructions](https://core.telegram.org/bots#6-botfather) (if you have Telegram
notifications set up in Home Assistant, you have already done this step). 
* Create a config file called <code>.hassbot.yaml</code> (use the
example file as a template) and put in your home directory. 
* At this point you can start the bot with the command <code>python3 hassbot.py</code> and access it in Telegram
* If you wish, set up a service to autostart the bot when your server starts. If you're using a systemd-based OS, you can use
the included example service file (put it in /etc/systemd/system and enable it with
<code>sudo systemctl enable homeassistant@YOURUSERNAME</code>
and start it with <code>sudo systemctl start homeassistant@YOURUSERNAME</code>

![Hassbot screenshot](/hassbot1.png)
