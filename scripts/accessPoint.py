# Ativa o ESP no modo Access Point
import network

def ap_connect():
    ap_if = network.WLAN(network.AP_IF)
    ap_if.active(True)
    ap_if.config(essid='ESP-AP')