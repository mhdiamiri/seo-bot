import requests
from config import *
import json
import socks
from stem import Signal
from stem.control import Controller

def print_ip():
    session = requests.Session()
    session.proxies = {
        'http': f'socks5://{HOST}:{PORT}',
        'https': f'socks5://{HOST}:{PORT}',
    }
    try:
        resp = session.get("http://ip-api.com/json/")
    except Exception as e:
        print(e)
        return False
    if resp.status_code == 200:
        d = json.loads(resp.text)
        print("your ip address:", d['query'])
        try: print("\tcountry", d['country']) 
        except: pass
        return True
    return None
        
def ip_switch():
    try:
        with Controller.from_port(port=CONTROLINIG_PORT) as controller:
            controller.authenticate()            
            controller.signal(Signal.NEWNYM)
            print("Identity Switched.")
    except Exception as i:
        print("Unable to switch Identity: {0}".format(i))

def tor_start() -> bool:
    try:
        os.system('open /Applications/Tor\ Browser.app')
        return True
    except Exception as s:
        print("Unable to start Tor Browser: {0}".format(s))
        return False
    

def set_default_proxy():
    try:
        socks.set_default_proxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", CONTROLINIG_PORT)
        print("Proxy set for Local Host at 127.0.0.1 port {}.".format(CONTROLINIG_PORT))
    except Exception as e:
        print("Error setting default proxy: {0}".format(e))
    try:
        socks_on = socks.socksocket()
        print("Secure Socket Layer initialized.")
    except Exception as e:
        print("Unable to initialise Secure Socket Layer: {0}".format(e))

def tor_quit():
    try:
        os.system('osascript -e \'quit app "Tor Browser.app"\'')
    except Exception as s:
        print("Unable to quit Tor Browser: {0}".format(s))
