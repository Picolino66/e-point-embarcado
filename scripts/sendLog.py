import ujson
import network
import urequests as requests
import uasyncio as asyncio
import btree
import machine
from machine import Pin



url = 'http://192.168.0.9:8000/create/' 

botao = Pin(12,Pin.IN,Pin.PULL_UP)

def send_to_server(): 
    try:
        f = open("log_table", "r+b")
    except OSError:
        f = open("log_table", "w+b")
    db = btree.open(f)
    try:
        key = 100
        for key in range(100, 999):
            try:
                key = str(key)
                json = ujson.loads(db[key])
                if json["enviado"] == 0:

                    requests.post(url, json=json,headers={'Content-Type': 'application/json;',})   #Linha q manda a request para a URL
                    
                    json["enviado"] = 1
                    db[key] = ujson.dumps(json)
                    db.flush()
                    print(key, "enviado")
                    print(db[key])
            except KeyError:
                print("Final do Arquivo, Limpando...")
                for key in db:
                    del db[key]
                    db.flush()
                print("Lista Limpa")
                break
    except IndexError:
        print("Sem net")

