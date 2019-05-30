#Arquivo para configurar os pinos no RTC

import DS3231
from machine import I2C, Pin

sda_pin = 21
scl_pin = 22

i2c = I2C(sda = Pin(sda_pin), scl = Pin(scl_pin))

ds = DS3231.DS3231(i2c)  #Variavel utilizada para acessar a data ou a hora.
