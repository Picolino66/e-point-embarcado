#Arquivo que controla os Bancos de Dados

import gc
import machine
#import rtc

import btree
gc.collect()

import ujson
gc.collect()

import utime
gc.collect()

import time

class Banco():
    def __init__(self, filename):
        self.filename = filename
        f, db = self.open(1)

    def open(self, _init=False):
        try:
            f = open(self.filename, "r+b")
            db = btree.open(f, pagesize = 512)
        except OSError:
            if _init:
                f = open(self.filename, "w+b")
                db = btree.open(f,pagesize = 512)
            else:
                print("db n iniciou")
                machine.reset()
                return False
        return f, db

    def close(self, f, db):
        db.flush()
        db.close()
        f.close()

    def list(self):
        f, db = self.open()
        for key in db:
            print(key + " - " + db[key])
        self.close(f, db)

    def add_json(self,json):
        f, db = self.open()
        cont = 100
        try:
            for key in db:
                cont = cont+1
            proximo = str(cont)
            db[proximo] = ujson.dumps(json)

        except OSError:
            machine.reset()
        self.close(f, db)

class Log(Banco):
    def __init__(self):
        super(Log,self).__init__('log_table')

    def new_member(self, id, entrou = 0, date=[],time=[], presente=0, enviado=0):
        json = {
            "id":id,
            "date":date,
            "time": time, 
            "entrou":entrou, 
            "presente": presente,
            "enviado": enviado
            }
        self.add_json(json)
        return json
        
    def status_entrou(self, id):
        entrou = 0
        f, db = self.open()
        try:
            for key in db:
                loads = ujson.loads(db[key])
                if id == loads["id"]:
                    entrou = loads["entrou"]
            return entrou
        except OSError:
            machine.reset()

