#Esse arquivo é executado automaticamente logo em seguida do boot.py
from connectWifi import Access_Point, Station
from bancoDados import Log, Cadastro
from machine import Pin, PWM, I2C
from rfid import Mfrc522
import urequests
import web_server
import uasyncio
import machine
import btree
import ujson
import time
import asyn
import DS3231

#Classe principal que controla todas as funcoes do projeto
class Main():  
    def __init__(self):
        #Pinos led
        self.blue = Pin(17,Pin.OUT)
        self.red = Pin(16,Pin.OUT)
        self.green = Pin(4,Pin.OUT)
        #Pino botao 
        self.BOT_PIN = 12
        #Pinos RTC
        self.SDA_PIN = 21
        self.SCL_PIN = 22
        
        #Definicao do horario da Reuniao Geral
        self.horaRG = 19
        self.minRG = 10
        self.minRG_max = 20

        #Funcoes Wifi
        self.ap = Access_Point()
        self.sta = Station()

        #Funcoes das tabelas do Banco de Dados
        self.log = Log()
        self.cadastro = Cadastro()

        #Funcoes do RFID
        self.rfid = Mfrc522()

        #Botao alternador do modo de autenticacao para o modo webserver para cadastro
        self.altern = Pin(self.BOT_PIN, Pin.IN, Pin.PULL_UP)
        self.altern.irq(trigger=Pin.IRQ_FALLING, handler=self.altern_mode)

        #RTC
        self.i2c = I2C(sda = Pin(self.SDA_PIN), scl = Pin(self.SCL_PIN))
        self.rtc = DS3231.DS3231(self.i2c)

        #Criacoes dos eventos do asyn.py
        self._send_to_server = asyn.Event()
        self._server = asyn.Event() 
        self._aut = asyn.Event()
        self._sta = asyn.Event()
        self._cad = asyn.Event()
        self._ap = asyn.Event()

        #Inicializacao dos eventos que iniciam o modo autenticacao e o modo Sta do wifi
        self._aut.set()
        self._sta.set()
        
        #Corrotinas
        self.loop = uasyncio.get_event_loop()
        self.loop.create_task(self.send_to_server())
        self.loop.create_task(self.sta_connect())
        self.loop.create_task(self.ap_connect())
        self.loop.create_task(self.autenticar())
        self.loop.create_task(self.cadastrar())
        self.loop.create_task(self.server())
        self.loop.run_forever()

    def open_member_table(self):
        """Funcao para abrir a tabela de cadastro dos membros"""
        try:
            f = open("member_table", "r+b")
            db = btree.open(f, pagesize=512)
        except:
            print("member_table nao abriu")
        return f,db

    def open_log_table(self):
        """Funcao para abrir a tabela Log"""
        try:
            f = open("log_table", "r+b")
            db = btree.open(f, pagesize=512)
        except:
            print("log_table nao abriu")
        return f,db

    def altern_mode(self, toggler):
        """Funcao que alterna para o modo de cadastro"""
        if self._sta.is_set():
            self._aut.clear()
            self.sta.disconnect()
            self._sta.clear()
            self._ap.set()

    async def ap_connect(self):
        """Corrotina que conecta o modo STA do ESP32"""
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
            
    async def sta_connect(self):
        """Corrotina que conecta o modo STA do ESP32"""
        while True:
            await self._sta
            print("ligando wifi")
            while self.sta.is_connected():
                await uasyncio.sleep(1)
            if not self._ap.is_set():
                while not self.sta.is_connected():
                    self.sta.connect()
                    await uasyncio.sleep(2)
            print("Conectado com sucesso")
            self._send_to_server.set()
            print(self.sta)

    async def server(self):
        """Corrotina que inicia o servidor"""
        while True:
            await self._server
            print('Iniciou server')
            await uasyncio.sleep_ms(200)
            web_server.host_server(event=self._server,callback=self._cad)
            print('Parou server')
            await uasyncio.sleep_ms(100)

    async def send_to_server(self):
        """Corrotina que envia os dados da tabela Log para o servidor"""
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
                            #self.sta.request_log(url,json)
                            urequests.post(url, json=json, headers={'Content-Type':'application/json;',})
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
                        break
            except IndexError:
                print("sem net")
            
    async def cadastrar(self):
        """Corrotina que cadastra na tabela dos membros"""
        await self._cad
        print("entrei no _cad")
        matricula = self._cad.value()            
        id = self.rfid.read_cad()
        print(id,"---", matricula)
        self.cadastro.new_member(id, matricula)
        await uasyncio.sleep_ms(100)
        PWM(self.red).duty(0)
        await uasyncio.sleep(1)
        PWM(self.red).duty(1023)
        self._cad.clear()
    
    def get_time(self):
        """Funcao que converte o dateTime"""
        year, month, day, _, hour, minute, second = [str(i) for i in self.rtc.DateTime()]
        return "".join([year,'-',month, '-', day, ' ', hour, ':', minute, ':',second ])

    async def autenticar(self):
        """Corrotina que autentica a batida do cartao e salva na tabela Log"""
        while True:
            await self._aut
            await uasyncio.sleep(1)
            f_m, db_m = self.open_member_table()             
            while self._aut.is_set():
                hora_now = self.rtc.Hour()
                minuto_now = self.rtc.Minute()
                dateTime_now = self.get_time()
                PWM(self.red).duty(1023)
                PWM(self.green).duty(0)
                PWM(self.blue).duty(1023)
                cadastrado = 0
                id = self.rfid.read()
                if id:
                    for key in db_m:
                        matricula = key.decode()
                        if id == db_m[key].decode():
                            PWM(self.red).duty(0)
                            PWM(self.green).duty(1023)
                            PWM(self.blue).duty(0)
                            time.sleep(0.5)
                            PWM(self.green).duty(0)
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
                            self.log.new_log(id,entrou,dateTime_now,present,matricula=matricula)
                            self.log.list()
                            cadastrado = 1
                            break
                    if not cadastrado:
                        print("Cartao nao cadastrado")
                        PWM(self.red).duty(1023)
                        PWM(self.green).duty(0)
                        PWM(self.blue).duty(0)
                        time.sleep(0.5)
                        PWM(self.red).duty(0)
                await uasyncio.sleep_ms(100)
main = Main()