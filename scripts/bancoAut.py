#Arquivo que utiliza as funçoes criadas no bancoDados.py para adicionar o membro na tabela de log

from machine import Pin
import ujson
import btree 
import rfid
import time
import bancoDados
import rtc

f = open("mydb", "r+b")
db = btree.open(f)

blue = Pin(17,Pin.OUT)
red = Pin(16,Pin.OUT)
green = Pin(4,Pin.OUT)

date_now = rtc.ds.Date()
time_now = rtc.ds.Time()
present = 0     # presente = 0 -> Faltou, presente = 1 -> Chegou na hora, presente = 2 -> Chegou atrasado

timeRG = [19,30,00]

logTable = bancoDados.Log()

while True:
    time.sleep(1)
    blue.on()
    print("aguardando o cartao..")
    id = rfid.Mfrc522().read()   
    control = 0
    for key in db:
        if id == db[key].decode():
            blue.off()
            green.on()
            time.sleep(0.5)
            green.off()
            print(id)
            if logTable.status_entrou(id) == 0:
                status = 1
                if time_now >= timeRG:
                    present = 0
                else:
                    present = 1  
            elif logTable.status_entrou(id) == 1:
                status = 0
                present = None
            logTable.new_member(id,status,date_now,time_now,present)
            logTable.list()
            control=1
            break

    if control == 0:
        print("Cartao nao cadastrado")
        blue.off()
        red.on()
        time.sleep(0.5)
        red.off()
