#Esse arquivo é executado automaticamente logo em seguida do boot.py

import web_server
import accessPoint

accessPoint.ap_connect()

# Inicia o web server
web_server.host_server()
