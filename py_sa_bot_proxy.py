from time import sleep

import datetime
from selenium import webdriver

import logfile
import proxy_servers
from proxy_servers import Proxy


def firefox_proxy_driver(proxy: Proxy):
    firefox_profile = webdriver.FirefoxProfile()
    firefox_profile.set_preference("network.proxy.type", 1)
    firefox_profile.set_preference("network.proxy.http", proxy.server)
    firefox_profile.set_preference("network.proxy.http_port", proxy.port)
    firefox_profile.set_preference("network.proxy.ssl", proxy.server)
    firefox_profile.set_preference("network.proxy.ssl_port", proxy.port)

    return webdriver.Firefox(
        firefox_profile=firefox_profile,
        firefox_binary="C:/Program Files (x86)/Mozilla Firefox/firefox.exe",
        executable_path="./geckodriver.exe")


def vote():
    driver = None
    reason = None
    proxy = None
    start = datetime.datetime.now()

    try:
        reason = "Proxy"
        proxy = proxy_servers.getNext()

        reason = "Driver"
        driver = firefox_proxy_driver(proxy)
        driver.set_window_size(900, 1200)
        driver.implicitly_wait(45)
        driver.get("http://sztuka-architektury.pl/")

        reason = "Popup"
        popup_close = driver.find_element_by_id("newsletter_close")
        popup_close.click()

        reason = "Publiczne"
        publiczne = driver.find_elements_by_xpath("//span[contains(text(), 'PUBLICZNE')]")[0]
        # find "PUBLICZNE" button by query selector, since no class and no id on the button
        driver.execute_script("document.querySelector('[data-id=\"question/83\"]').click();")
        print("Znalazłem PUBLICZNE")

        reason = "Radio"
        radio = driver.find_element_by_id("r443")
        driver.execute_script("document.getElementById('r443').click();")
        print("Znalazłem RADIO")

        sleep(3)

        reason = "Głosuj"
        glosuj = driver.find_element_by_class_name("sd")
        driver.execute_script("document.getElementsByClassName('sd')[0].click();")
        print("Znalazlem GLOSUJ")

        reason = "Dziekujemy"
        driver.find_element_by_xpath("//p[contains(text(), 'Dziękujemy za oddanie głosu')]")
        print("Znalazłem Dziękujemy")

        reason = ""
        logfile.make_proxy_log(True, reason=reason, proxy=proxy, start=start)
        driver.quit()
        vote()

    except:
        print("--> Nie znalazłem {}".format(reason))
        if driver:
            driver.quit()
        if proxy:
            logfile.make_proxy_log(False, reason=reason, proxy=proxy, start=start)
        else: # if no proxy files, delay next try
            sleep(10)
        vote()

if __name__ == "__main__":
    try:
        vote()
    except:
        vote()
