import btree 
import rfid
import time
from machine import Pin 

green = Pin(15, Pin.OUT)
red = Pin(4, Pin.OUT)
blue = Pin(22,Pin.OUT)

f = open("mydb", "r+b")     #abre o arquivo de banco de dados "mydb"
db = btree.open(f)

def autenticado():       #funçao responsável pela autenticação do cartão
      
    while True:
        green.off()
        red.off()
        blue.off()  
        print("Aguardando o cartao para autenticar..")
        codCartao = (rfid.Mfrc522().read())                     #Faz a leitura do cartao pelo script do rfid.py
        print (codCartao)
        for i in db:  
            if codCartao == db[i].decode():                        #varre o banco de dados(1 à 1), comparando com o cartao lido
                red.off()
                blue.off()
                green.on()
                time.sleep(1)
                green.off()
                return True
            else:
                blue.off()
                green.off()
                red.on()
                time.sleep(1)
                red.off()
                pass     
        return False 
        db.close()     #fecha o banco de dados 
        f.close()