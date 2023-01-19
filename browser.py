from config import *
import time
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import Proxy, ProxyType

class Browser:
    def __init__(self) -> None:
        capabilities = webdriver.DesiredCapabilities.CHROME
        prox = Proxy()
        prox.proxy_type = ProxyType.MANUAL
        prox.socks_proxy = f'{HOST}:{PORT}'
        prox.socks_version = 5
        prox.add_to_capabilities(capabilities)
        #self.driver = webdriver.Chrome(DRIVER_PATH)
        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        self.driver = webdriver.Chrome(DRIVER_PATH, desired_capabilities=capabilities, chrome_options=chrome_options)
        
    def change_path(self, path) -> None:
        self.driver.get(path)

    def close_driver(self) -> None:
        self.driver.close()

    def get_page_source(self) -> str:
        return self.driver.page_source
        
    def search_google(self, sentence):
        try:
            self.driver.get("https://google.com")
        except:
            return None
        time.sleep(WAITING_TIME)
        try:
            btn = self.driver.find_element(By.ID, 'L2AGLb')
            btn.click() 
        except:
            pass
        time.sleep(WAITING_TIME)
        try:
            search = self.driver.find_element(By.NAME, 'q')
            search.send_keys(sentence)
            search.send_keys(Keys.ENTER)
            results = self.driver.find_elements(By.CLASS_NAME, 'yuRUbf') 
            return results
        except:
            return None
    
    def next_page(self):
        try:
            next_btn = self.driver.find_element(By.ID, 'pnnext')
            next_btn.click()
            time.sleep(5)
            try:
                results = self.driver.find_elements(By.CLASS_NAME, 'yuRUbf') 
                return results
            except:
                print("except 1")
                return None
        except:
            print('except 2')
            return None
            
if __name__ == "__main__": # test
    b = Browser()
    results = b.search_google('پایتون چیست')
    found = False
    for i in range(SURF_PAGES):
        print("page:", i + 1)
        if results is None: 
            # new identity
            break
        for result in results:
            try:
                url = re.search("(?P<url>https?://[^\s]+)", result.text).group("url")
                print(url)
                if url.__contains__(TARGET_HOST):
                    print('found!')
                    try:
                        result.click()
                    except Exception as e:
                        print(e)
                    time.sleep(WAITING_TIME * 2)
                    found = True
                    break
            except Exception as e:
                pass
        if found: break
        results = b.next_page()
        
    print("Switching Identity...")
    b.close_driver()
    