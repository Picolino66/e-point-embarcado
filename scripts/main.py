#Esse arquivo é executado automaticamente logo em seguida do boot.py
from machine import Pin, PWM
import network
import machine 
import connectWifi
from connectWifi import Access_Point, Station
import web_server
import connectWifi
#from rtc import Rtc
import btree
import time
from rfid import Mfrc522
from rfid_cad import Mfrc522_cad
from bancoDados import Log, Cadastro
import bancoAut
import sendLog
import asyn
import uasyncio
import sendLog
import ujson

BOT_PIN = 12

class Main():
    def __init__(self):
        self.blue = Pin(17,Pin.OUT)
        self.red = Pin(16,Pin.OUT)
        self.green = Pin(4,Pin.OUT) 

        self.horaRG = [19]
        self.minRG = [10]
        self.minRG_max = [20]

        self.f_m, self.db_m = self.open_member_table()
        self.f_l, self.db_l = self.open_log_table()

        self.ap = Access_Point()
        self.sta = Station()

        self.log = Log()
        self.cadastro = Cadastro()

        self.rfid_cad = Mfrc522_cad()
        self.rfid = Mfrc522()
        #self.rtc = Rtc()

        self.altern = Pin(BOT_PIN, Pin.IN, Pin.PULL_UP)
        self.altern.irq(trigger=Pin.IRQ_FALLING, handler=self.altern_mode)

        #Eventos
        self._send_to_server = asyn.Event()
        self._server = asyn.Event() 
        self._aut = asyn.Event()
        self._ap = asyn.Event()
        self._sta = asyn.Event()
        self._server_off = asyn.Event()
        self._cad = asyn.Event()

        self._aut.set()
        self._sta.set()
        
        #self._ap.set()

        # Corrotinas
        self.loop = uasyncio.get_event_loop()
        self.loop.create_task(self.sta_connect())
        self.loop.create_task(self.ap_connect())
        self.loop.create_task(self.server())
        self.loop.create_task(self.autenticar())
        self.loop.create_task(self.cadastrar())
        self.loop.create_task(self.server_off())
        self.loop.create_task(self.send_to_server())
        self.loop.run_forever()

    def open_member_table(self):
        try:
            f = open("member_table", "r+b")
            db = btree.open(f, pagesize=512)
        except:
            print("member_table nao abriu")
        return f,db

    def open_log_table(self):
        try:
            f = open("log_table", "r+b")
            db = btree.open(f, pagesize=512)
        except:
            print("log_table nao abriu")
        return f,db

    def altern_mode(self, toggler):
        if self._sta.is_set():
            self._aut.clear()
            self.sta.disconnect()
            self._sta.clear()
            self._ap.set()

    async def ap_connect(self):
        while True:
            await self._ap
            PWM(self.blue).duty(0)
            PWM(self.red).duty(1023)
            PWM(self.green).duty(70)
            self.ap.connect()
            await uasyncio.sleep(1)
            self._server.set()
            while self._ap.is_set():
                await uasyncio.sleep(1)
            self.ap.disconnect()
            self._ap.clear()
            #self._sta.set()
            #self._aut.set()
            
    async def sta_connect(self):
        """ Corrotina para controle de conexões wireless no modo STA """
        while True:
            await self._sta
            while self.sta.is_connected():
                await uasyncio.sleep(1)
            if not self._ap.is_set():
                while not self.sta.is_connected():
                    self.sta.connect()
                    await uasyncio.sleep(2)
            print("Conectado com sucesso")
            #self._send_to_server.set()
            print(self.sta)

    async def server(self):
        while True:
            await self._server
            print('Iniciou server')
            await uasyncio.sleep_ms(200)
            web_server.host_server(event=self._server,callback=self._cad, off=self._server_off)
            print('Parou server')
            await uasyncio.sleep_ms(100)

    async def server_off(self):
        await self._server_off
        #machine.reset()
        self.ap.disconnect()
        self._ap.clear()
        self._server.clear()
        self._cad.clear()
        print("server desligado")
        self._sta.set()
        self._aut.set()

    async def send_to_server(self):
        url = 'http://192.168.0.9:8000/create/'
        f_l, db_l = self.open_log_table()
        while True:
            await self._send_to_server
            try:
                key=100
                for key in range(100,999):
                    try:
                        key = str(key).encode()
                        json = ujson.loads(db_l[key])
                        if json["enviado"] == 0:
                            self.sta.request_log(url,json)
                            json["enviado"] = 1
                            db_l[key] = ujson.dumps(json)
                            db_l.flush()
                    except KeyError:
                        print("Final do arquivo, limpando...")
                        for log in db_l:
                            del db_l[log]
                            db_l.flush()
                        print("Lista Limpa!!")
                        self._send_to_server.clear()
            except IndexError:
                print("sem net")
            

    async def cadastrar(self):
        await self._cad
        print("entrei no _cad")
        matricula = self._cad.value()            
        id = self.rfid_cad.read()
        print(id,"---", matricula)
        self.cadastro.new_member(id, matricula)
        await uasyncio.sleep_ms(100)
        PWM(self.red).duty(0)
        await uasyncio.sleep(1)
        PWM(self.red).duty(1023)
        self._cad.clear()

    async def autenticar(self):       
        while True:
            await self._aut
            await uasyncio.sleep(1)
            f_m, db_m = self.open_member_table()             
            while self._aut.is_set():
                ano_now = [2019]    #rtc.ds.Year()
                mes_now = [6]       #rtc.ds.Month()
                dia_now = [11]      #rtc.ds.Day()
                hora_now = [19]     #rtc.ds.Hour()
                minuto_now = [0]    #rtc.ds.Minute()
                dateTime_now = [2019,6,12,4,12,43,0]
                self.red.on()
                self.green.off()
                self.blue.on()
                cadastrado = 0
                #print("aguardando cartao ")
                id = self.rfid.read()
                if id:
                    for key in db_m:
                        if id == db_m[key].decode():
                            self.red.off()
                            self.green.on()
                            self.blue.off()
                            time.sleep(0.5)
                            self.green.off()
                            if not self.log.status_entrou(id):
                                entrou = 1
                                if hora_now > self.horaRG:
                                    present = 0
                                elif hora_now == self.horaRG:
                                    if minuto_now <= self.minRG:
                                        present = 1
                                    elif minuto_now > self.minRG and minuto_now <= self.minRG_max:
                                        present = 2
                                    else:
                                        present = 0
                                else:
                                    present = 1
                            else:
                                entrou = 0
                                present = None
                            self.log.new_log(id,entrou,dateTime_now,present)
                            self.log.list()
                            cadastrado = 1
                            break
                    if not cadastrado:
                        print("Cartao nao cadastrado")
                        self.red.on()
                        self.green.off()
                        self.blue.off()
                        time.sleep(0.5)
                        self.red.off()
                await uasyncio.sleep_ms(100)
                #print("Aguardando Cartao")
main = Main()