import gc
from machine import Pin       
gc.collect()

import uasyncio
gc.collect()
import asyn
gc.collect()

from wifi import (
    Sta,
    Ap,
)
gc.collect()
from pins import (
    Led,
    Ds3231,
    Mfrc522,
)
gc.collect()
from models import (
    Member,
    Log,
)
gc.collect()
from config import (
    PB,
    ENTRY_HOUR,
    ENTRY_MINUTES,
    EXIT_HOUR,
    EXIT_MINUTES,
    esp32_pause,
    SERVER_HOST,
    SERVER_PORT,
)
gc.collect()
import views
gc.collect()

class Main():
    def __init__(self):
        # Configurações
        self.sta = Sta()
        self.ap = Ap()

        # Banco de dados
        self.member = Member()
        self.log = Log(self.member)

        # Pinos
        # TODO: migrar para `pins.py`
        self.rdr = Mfrc522()
        self.rtc = Ds3231()
        self.toggler = Pin(PB, Pin.IN, Pin.PULL_UP)
        self.toggler.irq(trigger=Pin.IRQ_FALLING, handler=self.toggle_mode)

        # Eventos
        self._server = asyn.Event() 
        self._read_card = asyn.Event()
        self._led = asyn.Event()
        self.rgb = Led(self._led) #Pino
        self._ap = asyn.Event()
        self._sta = asyn.Event()
        self._wan = asyn.Event()
        self._send_2_server = asyn.Event()
        self._cleanup = asyn.Event()
        self._valid_time = asyn.Event()
        self._send_2_server.set([self.member, self.log]) #3
        self._read_card.set()
        
        if self.rtc.is_valid_time():
            self._valid_time.set()
        else:
            self._cleanup.set()
        self._sta.set()

        # Boas vindas
        self.greetings()

        # Corrotinas
        self.loop = uasyncio.get_event_loop()
        self.loop.create_task(self.sta_connect())
        self.loop.create_task(self.ap_connect())
        self.loop.create_task(self.server())
        self.loop.create_task(self.read_card())
        self.loop.create_task(self.led())
        self.loop.create_task(self.send_2_server())
        self.loop.create_task(self.cleanup())
        self.loop.create_task(self.check_time())
        self.loop.run_forever()

    def greetings(self):
        """ Método que indica a correta inicialização do programa """
        self.rgb.set(blue=1, red=1, time=2000, blink_delay=500)

    def toggle_mode(self, toggler):
        """ Método handler do push button. 
            
            - Desabilita a leitura do RFID;
            - Desabilita o modo STA da WLAN
            - Habilita o modo AP da WLAN (e do servidor web, consequentemente)

        """
        if self._sta.is_set():
            self._read_card.clear()
            self.sta.disconnect()
            self._sta.clear()
            self._ap.set()

    async def ap_connect(self):
        """ Corrotina para controle de conexões wireless no modo AP """
        while True:
            await self._ap
            self.ap.connect()
            await uasyncio.sleep(1)
            self._server.set()
            while self._ap.is_set():
                await uasyncio.sleep(1)
            self.ap.disconnect()
            self._ap.clear()
            self._sta.set()
            
    async def sta_connect(self):
        """ Corrotina para controle de conexões wireless no modo STA """
        while True:
            await self._sta
            while self.sta.is_connected():
                await uasyncio.sleep(1)
                wan = await self.sta.wan_ok()
                if not wan:
                    print("[IS CONNECTED] sem acesso a internet")
                    self._wan.clear()
                else: 
                    # TODO: otimizar
                    self._wan.set()
            
            if not self._ap.is_set():
                while not self.sta.is_connected():
                    self.sta.connect()
                    wan = await self.sta.wan_ok()
                    if wan:
                        print("com acesso a internet")
                        self._wan.set()
                    else:
                        print("[IS NOT CONNECTED] sem acesso a internet")
                    await uasyncio.sleep(2)

            print("Conectado com sucesso")
            print(self.sta)

    async def server(self):
        """ Corrotina que controla a execução do servidor web """
        while True:
            await self._server
            print('Iniciou server')
            self._led.clear()
            await uasyncio.sleep_ms(200)
            self.rgb.set(blue=1,blink_delay=300)
            #TODO: refatorar views e models
            views.host_server(self._server, self._read_card)
            self._ap.clear()
            print('Parou server')
            await uasyncio.sleep_ms(100)

    async def led(self):
        """ Corrotina para acionamento do led rgb """
        while True:
            await self._led
            self.loop.run_until_complete(self.rgb.handler(self._led, self._led.value()[0], self._led.value()[1], self._led.value()[2]))
            self.rgb.off()
            self._led.clear()
    
    async def send_2_server(self):
        """ Corrotina para envio de dados ao servidor """
        while True:
            print("Dentro de send_2_server")
            await self._send_2_server
            print("Passei de self._send2_server")
            await self._wan
            print("Enviando para server")
            await uasyncio.sleep(1)
            tables = self._send_2_server.value()

            for table in tables:
                pendings = table.get_pendings()
                for json, key in zip(pendings[0], pendings[1]):
                    try:
                        if json["left_empty"] :  # Tabela LOG
                            self.loop.run_until_complete(self.sta.request(content=json, host=SERVER_HOST, port=SERVER_PORT, source=table.source["EMPTY"]))
                        else:
                            self.loop.run_until_complete(self.sta.request(content=json, host=SERVER_HOST, port=SERVER_PORT, source=table.source["INSERT"]))
                    except:  # Tabela member
                        self.loop.run_until_complete(self.sta.request(content=json, host=SERVER_HOST, port=SERVER_PORT, source=table.source["INSERT"]))
                        pass
                    json["sent"] = True
                    table.update(key, json)

            self._send_2_server.clear()

    async def read_card(self):
        """ Corrotina que controla a leitura dos cartões RFID """
        while True:
            member_register = 0
            await self._read_card
            await uasyncio.sleep(1)  #Garantir que rfid libere após server
            if self._read_card.value():  #Evento possui algum valor
                member_register = 1
            while self._read_card.is_set():
                id = self.rdr.read()
                if id:
                    if member_register:
                        print("cadastro de membro")
                        
                        if self.member.new_transaction(id, name=self._read_card.value()[0][0], email=self._read_card.value()[0][1], time=self.rtc.get_datetime()):
                            self._send_2_server.set([self.member])  #1
                            await uasyncio.sleep_ms(100)
                            self.rgb.set(blue=1, time=2000, blink_delay=1900)
                        else:  #Usuário já existe
                            self.rgb.set(red=1, time=1000, blink_delay=110)
                        member_register = 0
                        
                    else:

                        if  self.rtc.is_valid_time():
                            print("Está no horário")
                            success, is_empty, is_full = self.log.new_transaction(id, time=self.rtc.get_datetime())
                            if success:  #Transação gravada com sucesso
                                self._send_2_server.set([self.log])  #2
                                self.rgb.set(green=1, time=1000, blink_delay=110)
                            elif is_empty:
                                #self.send_2_server.set([self.log])  #4
                                self.rgb.set(red=1, green=1, blue=1, time=1000, blink_delay=110)
                            elif is_full:
                                self.rgb.set(red=1, time=1000, blink_delay=110)
                            else:
                                self.rgb.set(red=1, time=1000, blink_delay=110)
                            
                        else:  #Usuário não permitido
                            print("ATRASADO!")
                            self.rgb.set(red=1, time=1000, blink_delay=110)
                        self.log.list()
                print('LENDO....')
                await uasyncio.sleep_ms(100) 

    async def cleanup(self): 
        """ Corrotina responsável por limpar os status dos membros no final do dia"""
        while True:
            await self._cleanup
            self.member.clean_status()
            print("Dados limpos!!")
            self._cleanup.clear()
            await uasyncio.sleep(1)

    async def check_time(self):
        """Corrotina responsável por analisar se o horário é válido """
        while True:
            while self._valid_time.is_set():
                if not self.rtc.is_valid_time():
                    self._cleanup.set()
                    self._valid_time.clear()
                else:
                    await uasyncio.sleep(900)
            while not self._valid_time.is_set():
                if self.rtc.is_valid_time():
                    self._valid_time.set()
                else:
                    await uasyncio.sleep(900)

main = Main()
