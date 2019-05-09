# This file is executed on every boot (including wake-boot from deepsleep)
imp rt esp
esp.osdebug(None)
import webrepl
webrepl.start()
