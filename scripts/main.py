#Esse arquivo é executado automaticamente logo em seguida do boot.py

import cadastrar
import network
import connectWifi
import web_server
import connectWifi

connectWifi.do_connect()

import bancoAut

# AP configuration
#ap_if = network.WLAN(network.AP_IF)
#ap_if.config(essid='ESP-AP')
#ap_if.active(True)

#web_server.host_server()




