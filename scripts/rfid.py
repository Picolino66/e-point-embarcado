import mfrc522   #importa a lib do RFID
import time
from machine import Pin

#Define-se os pinos 
RF_SCK = 18  # clock
RF_SDA = 21  # data
RF_MOSI = 23  # master-out slave-in
RF_MISO = 19  # master-in slave-out
RF_RST = 22  # reset


class Mfrc522(): 
    #Funçao que inicia o RFID com os respectivos pinos 
    def __init__(self):
        self.rdr = mfrc522.MFRC522(RF_SCK, RF_MOSI, RF_MISO, RF_RST, RF_SDA)
        #self.allowed_id = allowed_id
        self.read()
        
    #Funçao responsavel pela leitura do cartao
    def read(self):
        print("Esperando cartão...")
        while True:
            (stat, tag_type) = self.rdr.request(self.rdr.REQIDL)
            if stat == self.rdr.OK:
                (stat, raw_uid) = self.rdr.anticoll()
                try:
                    read = "0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3])
                    print("O código desse cartão é: ", read)
                    #if read == self.allowed_id:
                     #   print("Usuário permitido :) -", read)
                    #else:
                     #   print("Usuário não permitido :( -", read)
                except IndexError:
                    pass
        return read
