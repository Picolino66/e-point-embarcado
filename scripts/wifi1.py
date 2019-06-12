import gc
import network
gc.collect()
import usocket
gc.collect()
import urequests
gc.collect()
from utime import ticks_ms, ticks_diff
gc.collect()
import uasyncio
gc.collect()

from config import (
    STA_SSID,
    STA_PWD,
    AP_SSID,
    AP_PWD,
    SOCKET_POLL_DELAY,
    BUSY_ERRORS,
    RESPONSE_TIME,
    esp32_pause,
)
gc.collect()


class Sta():
    """ Classe que manipula um objeto de conexão no modo *STA_IF* """
    def __init__(self):
        self.sta_if = network.WLAN(network.STA_IF)

    def __str__(self):
        return self.sta_if.ifconfig()

    def connect(self):
        """ Estabelece, se possível, conexão com um ponto de acesso """
        self.sta_if.active(True)
        self.sta_if.connect(STA_SSID, STA_PWD)

    def disconnect(self):
        """ Desabilita a conexão wlan com um ponto de acesso """
        self.sta_if.active(False)
        print('STA desconectado')

    def is_connected(self):
        """ Método que retorna o estado da conexão Wi-Fi.
            Note que conexão Wi-Fi pode existir sem que haja
            conexão com a internet. O método `wan_ok()` é o 
            encarregado de realizar essa conferência
        """

        return self.sta_if.isconnected()

    def request(self,content=None, host="http://localhost", port="80", source=None):
        response = urequests.post("".join([host, ":", port, source]), json=content, headers={'Content-Type': 'application/json;',})
        await uasyncio.sleep(1)
        #print(response.text, response.status_code)
        #TODO: receive server response
        if response.status_code >= 200 and response.status_code < 300:
            print('Enviado')
        await uasyncio.sleep(1)

    def _timeout(self, t):
        """ Método que retorna se o tempo de repub foi estourado """
        return ticks_diff(ticks_ms(), t) > RESPONSE_TIME

    async def _as_read(self, n, sock): 
        """ Lê o conteúdo do socket estabelecido """
        data = b''
        t = ticks_ms()
        while len(data) < n:
            esp32_pause()  # necessário
            if self._timeout(t) or not self.is_connected():
                raise OSError(-1)
            try:
                msg = sock.read(n - len(data))
            except OSError as e:  # ESP32 issues weird 119 errors here
                msg = None
                if e.args[0] not in BUSY_ERRORS:
                    raise
            if msg == b'':  # conexão fechada pelo host (?)
                raise OSError(-1)
            if msg is not None:  # dados recebidos
                data = b''.join((data, msg))
                t = ticks_ms()
                #self.last_rx = ticks_ms()
            await uasyncio.sleep_ms(SOCKET_POLL_DELAY)
        return data

    async def _as_write(self, bytes_wr, length=0, sock=None):
        """ Escreve o conteúdo no socket estabelecido """
        if length:
            bytes_wr = bytes_wr[:length]
        t = ticks_ms()
        while bytes_wr:
            if self._timeout(t) or not self.is_connected():
                raise OSError(-1)
            try:
                n = sock.write(bytes_wr)
            except OSError as e:  # ESP32 issues weird 119 errors here
                n = 0
                if e.args[0] not in BUSY_ERRORS:
                    raise
            if n:
                t = ticks_ms()
                bytes_wr = bytes_wr[n:]
            esp32_pause()  # precaução
            await uasyncio.sleep_ms(SOCKET_POLL_DELAY)


    async def wan_ok(self, packet = b'$\x1a\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x03www\x06google\x03com\x00\x00\x01\x00\x01'):
        """ Método que confere se existe conexão com a internet
            enviando o lookup do DNS para um servidor (Google 8.8.8.8)
            e conferindo a resposta recebida.
        """

        length = 32  # tamanho do pacote
        s = usocket.socket(usocket.AF_INET, usocket.SOCK_DGRAM)
        s.setblocking(False)
        s.connect(('8.8.8.8', 53))
        await uasyncio.sleep(1)
        try:
            await self._as_write(packet, sock = s)
            await uasyncio.sleep(2)
            res = await self._as_read(length, s)
            if len(res) == length:
                return True  # tamanho da resposta do DNS correto
        except OSError:  # Timeout na leitura: não foi possível conectar
            return False
        finally:
            s.close()
        print("não deu bom mesmo")
        return False

class Ap():
    """ Classe que manipula um objeto de conexão no modo *AP_IF* """
    def __init__(self):
        self.ap_if = network.WLAN(network.AP_IF)

    def connect(self):
        """ Estabelece um ponto de acesso a receber clientes """
        self.ap_if.active(True) 
        esp32_pause()  # necessário
        self.ap_if.config(essid=AP_SSID)
        esp32_pause()  # necessário
        #self.ap_if.config(authmode=3, password=AP_PWD)
        self.ap_if.config(authmode=0)
        esp32_pause()  # necessário
        #self.ap_if.ifconfig(('192.168.84.1', '255.255.255.0', '192.168.84.1', '192.168.84.1'))

        if self.ap_if.isconnected() == True:
            print("Já conectado")
            return

        while self.ap_if.isconnected() == False:
            pass

        print('AP criado')
        print(self.ap_if.ifconfig())

    def disconnect(self):
        """ Desconecta o ponto de acesso """
        self.ap_if.active(False)
        print('AP desconectado')

