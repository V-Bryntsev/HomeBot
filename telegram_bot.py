#!/usr/bin/python3
# -*- coding: utf-8 -*-

import subprocess
import telebot
import time
import yaml
import requests
import os
from bs4 import BeautifulSoup

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

@bot.message_handler(commands=['transponder'])
def transponderinfo(message):
    url = 'https://avtodor-tr.ru/account/login'
    user_agent_val = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
    session = requests.Session()
    r = session.get(url, headers = {'User-Agent': user_agent_val})
    post_request = session.post(url, {
        'email': config['transponder']['email'],
        'password':config['transponder']['password'],
        'submit0': 'Подождите...', # ¯\_(ツ)_/¯
    })
    contents = post_request.text
    soup = BeautifulSoup(contents, 'lxml')
    s = soup.find("div", id="balans").find("span").text.split('.')[0]
    bot.send_message(message.from_user.id, s+' руб')

@bot.message_handler(commands=['parking'])
def handlegetsrvinfo(message):
    url = 'http://%s:%s@%s:%s/stream/snapshot.jpg' % (config['parking_camera']['username'],
                                                      config['parking_camera']['password'],
                                                      config['parking_camera']['ip'],
                                                      config['parking_camera']['port'])
    filename = url.split('/')[-1]
    if (os.system("ping -c 5 " + config['parking_camera']['ip']) is 0) :
        r = requests.get(url, allow_redirects=True)
        open(filename, 'wb').write(r.content)
        bot.send_photo(message.chat.id, open(filename, 'rb'))
    else:
        bot.send_message(message.from_user.id, 'Camera is not available')
    if os.path.exists(filename):
        os.remove(filename)

@bot.message_handler(commands=['getsrvtemp'])
def handlegetsrvinfo(message):
    p = subprocess.Popen(["ipmitool" ,"sdr"], stdout=subprocess.PIPE)
    out = p.communicate()[0]
    sens = sensors(out)
    answer = 'System Temp = %s \nCPU Temp = %s' % (sens.values['System Temp'], sens.values['CPU Temp'])
    bot.send_message(message.chat.id,answer,parse_mode= "HTML")

@bot.message_handler(content_types="text")
def handler_text(message):
    bot.send_message(message.from_user.id, 'Just_text')

while True:
    try:
        bot.polling(none_stop=True)

    except Exception as e:
        print(e)
        time.sleep(15)
