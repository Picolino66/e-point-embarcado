#Arquivo para configurar os pinos no RTC

import DS3231
from machine import I2C, Pin

class Rtc():
    def __init__(self):
        self.sda_pin = 21
        self.scl_pin = 22
    
    def get_rtc(self):
        i2c = I2C(sda = Pin(self.sda_pin), scl = Pin(self.scl_pin))
        ds = DS3231.DS3231(i2c)

        
