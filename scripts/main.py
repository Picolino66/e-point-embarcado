#Esse arquivo é executado automaticamente logo em seguida do boot.py

import cadastrar
import autenticar
import web_server
import network
import connectWifi

connectWifi.do_connect()

while True:
    autenticar.autenticado()

# Ativa o ESP no modo Access Point
#ap_if = network.WLAN(network.AP_IF)
#ap_if.active(True)
#ap_if.config(essid='ESP-AP')

# Inicia o web server
#web_server.host_server()
