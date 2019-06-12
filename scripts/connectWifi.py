import network
import time
from machine import Pin
import usocket
import uasyncio
import urequests as requests

from utime import ticks_ms, ticks_diff

blue = Pin(17,Pin.OUT)
red = Pin(16,Pin.OUT)
green = Pin(4,Pin.OUT)

B_PIN = 12

botao = Pin(B_PIN,Pin.IN,Pin.PULL_UP)

class Station():
	def __init__(self):
		self.sta_if = network.WLAN(network.STA_IF)

	def is_connected(self):
		return self.sta_if.isconnected()
		
	def connect(self):
		self.sta_if.active(True)
		#self.sta_if.connect('LABSINE', 'Redeneuralartificial(@$%)Labsine2018')
		self.sta_if.connect('Zaza', 'zazafullstack')
		#self.sta_if.connect('MELO', 'melo1212')

	def disconnect(self):
		self.sta_if.active(False)
		print("Wifi STA desligado")

	def request_log(self,url,json):
		resp = requests.post(url, json=json, headers={'Content-Type':'application/json;',})
		await uasyncio.sleep(1)
		if resp.status_code >= 200 and resp.status_code < 300:
			print('json enviado para o server')
		await uasyncio.sleep(1)

class Access_Point():
	def __init__(self):
		self.ap_if = network.WLAN(network.AP_IF)

	def connect(self):
		self.ap_if.active(True)
		self.ap_if.config(essid='EPOINT_AP')
		self.ap_if.config(authmode=0)

	
		if self.ap_if.isconnected():
			print("AP ja esta conectado")
			return
				
		while not self.ap_if.isconnected():
			pass

		print("AP criado")
		print(self.ap_if.ifconfig())

	def disconnect(self):
		self.ap_if.active(False)
		print("AP desativado")