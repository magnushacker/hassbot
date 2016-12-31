#!/usr/bin/python3

# import logging
# logging.basicConfig(level=logging.DEBUG)

import telegram.ext
import homeassistant.remote
import yaml
import os

def get_status_update(what, full=False):
  entities = homeassistant.remote.get_states(api)
  lines = []
  
  for entity in entities:
    if what == "switch" and entity.domain in ("switch", "light") and not entity.entity_id.startswith("switch.sensor"):
      if entity.state == "on" or full:
        lines.append ("{} is {}".format(entity.attributes['friendly_name'], entity.state))
    elif what == "door" and entity.domain == "switch" and entity.entity_id.startswith("switch.sensor_"):
      lines.append ("{} is {}".format(entity.attributes['friendly_name'], "open" if entity.state == "on" else "closed"))
    elif what == "sensor" and entity.domain == "sensor":
      lines.append ("{} is {} {}".format(entity.attributes['friendly_name'], entity.state, entity.attributes['unit_of_measurement']))
    elif what == "people" and entity.domain == "device_tracker":
      lines.append ("{} is at {}".format(entity.attributes['friendly_name'], entity.state))
  
  return lines
  
def status(bot, update, args):
  lines = []
  if len(args) > 0:
    what = ''.join(args)
    if what == "verbose":
      lines.extend(get_status_update("switch", True))
      lines.extend(get_status_update("door", True))
      lines.extend(get_status_update("sensor", True))
      lines.extend(get_status_update("people", True))
    elif what == "switch":
      lines.extend(get_status_update("switch"))
    elif what == "sensor":
      lines.extend(get_status_update("sensor"))
    elif what == "people":
      lines.extend(get_status_update("people"))
    elif what == "door":
      lines.extend(get_status_update("door"))
    else:
      lines.append("switch, sensor, door, people or verbose?")
  else:
    lines.extend(get_status_update("switch"))
    lines.extend(get_status_update("sensor"))
    lines.extend(get_status_update("door"))
    lines.extend(get_status_update("people"))
  
  update.message.reply_text('\n'.join(lines))

def hello(bot, update):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))

# Read config file
try:
  config_file = open (os.path.expanduser("~") + "/.hassbot.yaml")
  config = yaml.load(config_file)
except:
  print ("Could not load config file")
  raise
  
# Init HA API
api = homeassistant.remote.API(config["homeassistant_host"], config["homeassistant_password"])

# Init Telegram bot
updater = telegram.ext.Updater(config["telegram_api_key"])
updater.dispatcher.add_handler(telegram.ext.CommandHandler('status', status, pass_args=True))
updater.dispatcher.add_handler(telegram.ext.CommandHandler('hello', hello))

# Start
updater.start_polling()
updater.idle()
