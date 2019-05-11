def do_connect():
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connectando...')
        sta_if.active(True)
        sta_if.connect('LABSINE', 'Redeneuralartificial(@$%)Labsine2018')
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())
