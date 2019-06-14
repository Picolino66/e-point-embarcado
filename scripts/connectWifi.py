import urequests as requests
from machine import Pin
import uasyncio
import network
import time

class Station():
	"""Classe que controla o modo station do Wifi do ESP32"""
	def __init__(self):
		self.sta_if = network.WLAN(network.STA_IF)

	def is_connected(self):
		"""Funcao que verifica se o Wifi esta conectado."""
		return self.sta_if.isconnected()
		
	def connect(self):
		"""Funcao responsavel por conectar na rede wifi."""
		self.sta_if.active(True)
		#self.sta_if.connect('LABSINE', 'Redeneuralartificial(@$%)Labsine2018')
		self.sta_if.connect('Zaza', 'zazafullstack')

	def disconnect(self):
		"""Funcao responsavel por desconectar o Wifi"""
		self.sta_if.active(False)
		print("Wifi STA desligado")

	def request_log(self,url,json):
		"""Funcao responsavel por fazer o request post para o servidor.\n
		Parametros:\n
		-'url' (url que recebera o request)\n
		-'json' (json com o conteudo que sera enviado para o servidor)
		"""
		resp = requests.post(url, json=json, headers={'Content-Type':'application/json;',})
		await uasyncio.sleep(1)
		if resp.status_code >= 200 and resp.status_code < 300:
			print('json enviado para o server')
		await uasyncio.sleep(1)

class Access_Point():
	"""Classe que controla o modo Access Point do Wifi do ESP32"""
	def __init__(self):
		self.ap_if = network.WLAN(network.AP_IF)

	def connect(self):
		"""Funcao responsavel por conectar o AP"""
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
		"""Funcao responsavel por desconectar o AP"""
		self.ap_if.active(False)
		print("AP desativado")