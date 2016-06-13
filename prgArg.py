# -*- coding: utf-8 -*-

"""Para Python 2.7"""
import wikipedia
import telepot #para trabajar con telegram bot
import datetime #para trabajar con la fecha del sistema
import string
import serial #para trabajar con arduino
import emoji #para que envie emojis
import sys
import random
import pywapi
import time

def getTime(opc):
	ahora = datetime.datetime.now()
	if opc == 'dia':
		return '%s / %s / %s' % (ahora.day, ahora.month, ahora.year)
	elif opc == 'horaMinSec':
		return '%s : %s : %s' % (ahora.hour, ahora.minute, ahora.second)
	elif opc == 'hora':
		return ahora.hour

def handle(msg):
	chat_id = msg['chat']['id']
	command = msg ['text']
	print ('Got command: %s' % command)
	if command == '/roll':
		texto = random.randint(1,20)
	elif command == '/time':
		dia = getTime('dia')
		hora = getTime('horaMinSec')
		texto = emoji.emojize(':date:', use_aliases = True)+ dia + '\n'+emoji.emojize(':alarm_clock:', use_aliases = True) + hora
	elif command == '/clima':
		#yahoo_result = pywapi.get_weather_from_yahoo('ARCS0025')   #los de yahoo no estaban andando por eso utilizo el weather.com
		#estado = string.lower(yahoo_result['condition']['text'])
		#grado = yahoo_result['condition'] ['temp'] + "°C"
		weather_com_result = pywapi.get_weather_from_weather_com('ARCS0025')  #Este es Weather.com
		estado = string.lower(weather_com_result['current_conditions']['text'])
		grado = weather_com_result['current_conditions']['temperature'] 
		hora = int(getTime('hora'))
		print estado    
		if estado == 'cloudy':
			emoticon = "Nublado " + emoji.emojize(':cloud:', use_aliases = True)
		elif estado == 'mostly cloudy':
			emoticon = "Muy Nublado " + emoji.emojize(':cloud:', use_aliases = True)+" "+ emoji.emojize(':cloud:', use_aliases = True)+" "+ emoji.emojize(':cloud:', use_aliases = True)
		elif estado=='fair':
			if hora>=7 and hora <= 19:
				emoticon = "Adorable " + emoji.emojize(':sunny:', use_aliases = True)
			else:
				emoticon = "Adorable" + emoji.emojize(':first_quarter_moon_with_face:', use_aliases = True)
		texto = "El clima en Corrientes es: " + emoticon + " con " + grado + "C"
	elif command == 'Hola' or command == 'hola':
		name = msg['chat']['first_name']
		emoticon = emoji.emojize(':wave:', use_aliases = True)
		texto = "Hola " + name +emoticon+"\nEnvia /help para ver los comandos."
	elif command == '/help':
		texto = '/time - Hora y Fecha del Sistema \n/clima - Pronostico de Corrientes \n/info - Acerca de...'
	elif "Buscar " in command:
		totChar = len(command) + 1
		bus = command[7:totChar]
		wikipedia.set_lang("es")
		texto = wikipedia.summary(bus, sentences=1)
	else:
		texto = "Disculpa no conozco ese mensaje."
	bot.sendMessage(chat_id, texto)
	
bot = telepot.Bot('My Token')  #Add you TOKEN BOT
bot.notifyOnMessage(handle)
print ('i am listening...')

while 1:
	time.sleep(10)