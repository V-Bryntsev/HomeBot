#!/usr/bin/python3
# -*- coding: utf-8 -*-

import subprocess
import telebot
import time
import yaml

class sensors:
	def __init__(self, cmdout):
		self.divided = cmdout.split(b'\n')
		self.values = {}
		for stri in self.divided:
			if stri:
				self.values[stri.split(b'|')[0].strip().decode("utf-8")] = stri.split(b'|')[1].split(b' ')[1].decode("utf-8")

def load_config(config_file):
	with open(config_file, 'r') as stream:
		try:
			return yaml.safe_load(stream)
		except yaml.YAMLError as exc:
 			print(exc)


config = load_config('config.yml')
bot = telebot.TeleBot(config['bot']['token'])
proxy = '%s://%s:%s@%s:%s' % (config['bot']['proxy']['protocol'],
							config['bot']['proxy']['username'],
							config['bot']['proxy']['password'],
							config['bot']['proxy']['host'],
							config['bot']['proxy']['port'])
telebot.apihelper.proxy = { 'https':proxy}


@bot.message_handler(commands=['getsrvtemp'])
def handlegetsrvinfo(message):
	p = subprocess.Popen(["ipmitool" ,"sdr"], stdout=subprocess.PIPE)
	out = p.communicate()[0]
	sens = sensors(out)
	answer = 'System Temp = %s \nCPU Temp = %s' % (sens.values['System Temp'], sens.values['CPU Temp'])
	bot.send_message(message.chat.id,answer,parse_mode= "HTML")

@bot.message_handler(content_types="text")
def handler_text(message):
    bot.send_message(message.from_user.id, 'Just_test')

while True:
	try:
		bot.polling(none_stop=True)

	except Exception as e:
		print(e)
		time.sleep(15)
