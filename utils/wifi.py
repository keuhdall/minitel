import network
import time

def connect(ssid, password, timeout=30):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        print("Connexion au WiFi...")
        wlan.connect(ssid, password)

        # On attend la connexion
        max_wait = timeout
        while max_wait > 0:
            if wlan.isconnected():
                break
            max_wait -= 1
            print("En attente...")
            time.sleep(1)

    if wlan.isconnected():
        print("Connecté !")
        print("Adresse IP:", wlan.ifconfig()[0])
        return True
    else:
        print("Échec de connexion.")
        return False