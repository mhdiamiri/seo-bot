from tor import *
from config import *
from browser import Browser
import re
import time
import pandas as pd

def initialize_tor() -> bool:
    tor_start()
    set_default_proxy()
    for i in range(10):
        result = print_ip()
        if result: return True
        print("still not connected to proxy. working on it...")
        time.sleep(10)
    return False

def search(sentence):
    b = Browser()
    results = b.search_google(sentence)
    found = False
    for i in range(SURF_PAGES):
        print("page:", i + 1)
        if results is None: 
            break
        for result in results:
            try:
                url = re.search("(?P<url>https?://[^\s]+)", result.text).group("url")
                print(url)
                if url.__contains__(TARGET_HOST):
                    print('found!')
                    result.click()
                    time.sleep(WAITING_TIME * 2)
                    found = True
                    break
            except Exception as e:
                print(e)
        if found: break
        results = b.next_page()
    b.close_driver()

def switch():
    print("Changing your ip...")
    ip_switch()
    for i in range(10):
        result = print_ip()
        if result: return True
        print("still not connected to proxy. working on it...")
        time.sleep(10)
    return False
    
def main():
    tor = initialize_tor()
    set_default_proxy()
    tor = True
    if not tor:
        print("failed to start tor. please start it manually.")      
        return 
    df = pd.read_excel('searchs.xlsx')
    for i in range(1000):
        for r in df['searchs']:
            search(r)
            switch()

if __name__ == "__main__":
    main()
    
    
