#Arquivo que utiliza as funçoes criadas no bancoDados.py para adicionar o membro na tabela de log

from machine import Pin
import ujson
import btree 
import rfid
import time
import bancoDados
#import rtc

class Log_Aut():

    def __init__(self):
        self.logTable = bancoDados.Log()

        self.timeRG = [19,10,59]
        self.timeRG_max = [19,20,59]

        self.date_now = [2019,6,4] #rtc.ds.Date()
        self.time_now = [19,0,0] #rtc.ds.Time()

        self.present = 0
        self.entrou = 0

        self.blue = Pin(17,Pin.OUT)
        self.red = Pin(16,Pin.OUT)
        self.green = Pin(4,Pin.OUT)

        self.read_card = rfid.Mfrc522()
        self.f, self.db = self.open()


    def open(self):
        try:
            f = open("member_table", "r+b")
            db = btree.open(f, pagesize = 512)
        except:
            print("nao achou a tabela")
        return f, db

    def banco_log(self):
        while True:
            time.sleep(1)
            self.green.off()
            self.red.on()
            self.blue.on()
            print("aguardando o cartao..")
            id = self.read_card.read()
            control = 0
            for key in self.db:
                if id == self.db[key].decode():
                    self.blue.off()
                    self.red.off()
                    self.green.on()
                    time.sleep(0.5)
                    self.green.off()
                    print(id)
                    if self.logTable.status_entrou(id) == 0:
                        self.entrou = 1
                        if self.time_now > self.timeRG_max:
                            self.present = 0
                        elif self.time_now <= self.timeRG_max and self.time_now > self.timeRG:
                            self.present = 2
                        else:
                            self.present = 1
                    elif self.logTable.status_entrou(id) == 1:
                        self.entrou = 0
                        self.present = None
                    self.logTable.new_log(id,self.entrou,self.date_now,self.time_now,self.present)
                    self.logTable.list()
                    control=1
                    break

            if control == 0:
                print("Cartao nao cadastrado")
                self.green.off()
                self.blue.off()
                self.red.on()
                time.sleep(0.5)
                self.red.off()