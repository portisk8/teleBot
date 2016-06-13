# -*- coding: utf-8 -*-

"""Para Python 2.7"""

import telepot #para trabajar con telegram bot
import datetime #para trabajar con la fecha del sistema
import string
import serial #para trabajar con arduino
import emoji #para que envie emojis
import sys
import random
import pywapi
import time
import wikipedia
from telebot import util

token = 'TOKEN'
def getTime(opc):
	ahora = datetime.datetime.now()
	if opc == 'dia':
		return '%s / %s / %s' % (ahora.day, ahora.month, ahora.year)
	elif opc == 'horaMinSec':
		return '%s : %s : %s' % (ahora.hour, ahora.minute, ahora.second)
	elif opc == 'hora':
		return ahora.hour
		
def ardOn(orden):
	arduino = serial.Serial('/dev/ttyACM0', 9600)
	time.sleep(2)
	if orden!=int:
		if orden=="musica":
			arduino.write(str(6))
			time.sleep(1)
			arduino.write(str(7))
		elif orden == "fox":
			arduino.write(str(4))
			time.sleep(1)
			arduino.write(str(3))
		elif orden == "disney":
			arduino.write(str(3))
			time.sleep(1)
			arduino.write(str(3))
		elif orden=="vol+":
			for i in range(10):
				arduino.write(str(14))
				time.sleep(1)
		elif orden == "vol-":
			for i in range(10):
				arduino.write(str(15))
				time.sleep(1)
		elif orden == "on" or orden == "off":
			arduino.write(str(12))			
		else:
			if orden//10>=1 and orden //10 <= 9:
				d1 = orden //10
				d2 = orden %10
				arduino.write(str(d1))
				time.sleep(1)
				arduino.write(str(d2))
			else:
				arduino.write(str(orden))
	arduino.close()
	
def handle(msg):
	chat_id = msg['chat']['id']
	content_type, chat_type,chat_id = telepot.glance(msg)
	print(content_type,chat_type,chat_id)
	if content_type == 'text':
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
		elif command == "OnTv" or command == "OffTv":
			ardon("on")
			if command == "OnTv":
				bot.sendMessage(chat_id, "Espere que se esta encendiendo la TV")
				time.sleep(10)
				texto = "Se encendio la TV"
			else: 
				texto = "Se apago la TV"
		elif command == "Musica1":
			ardOn("musica")
			texto = "Se Cambio al canal de musica"
		elif command == "Fox":
			ardOn("fox")
			texto = "Se ha cambiado al canal Fox"
		elif command == "Disney":
			ardOn("disney")
			texto = "Se ha cambiado al canal Disney Junior"
		elif command == "TvVol+":
			ardOn("vol+")
			texto = "Se subio 10 unidades de Volumen"
		elif command == "TvVol-":
			ardOn("vol-")
			texto = "Se bajo 10 unidades de Volumen"
		elif "Canal " in command:
			try:
				canal = int(command[6:8])
				print canal
				ardOn(canal)
				texto = "Cambiado al canal "+ str(canal)
			except ValueError:
				texto = "Error no existe ese canal"
		elif "Buscar " in command:
			totChar = len(command) + 1
			bus = command[7:totChar]
			wikipedia.set_lang("es")
			try:
				texto = wikipedia.summary(bus)
				splitted_text = util.split_string(texto,3000)
				for text in splitted_text:
					bot.sendMessage(chat_id,text)
				texto = "OK"
			except wikipedia.exceptions.PageError :
				texto = "Error, pruebe con otro nombre."
		else:
			texto = "Disculpa no conozco ese mensaje."
		bot.sendMessage(chat_id, texto)
	elif content_type=='photo':
		dir = str(datetime.datetime.now())+'.png'
		bot.download_file(msg['photo'][-1]['file_id'], '/home/pi/Desktop/repositorio/Imagenes/%s' % dir)

bot = telepot.Bot(token)  #Add you TOKEN BOT
bot.message_loop(handle)
print ('i am listening...')

while 1:
	time.sleep(10)
