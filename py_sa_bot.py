from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import logger


def firefox_proxy_driver():
    firefox_profile = webdriver.FirefoxProfile()
    firefox_profile.set_preference("network.proxy.type", 1)
    firefox_profile.set_preference("network.proxy.socks", "127.0.0.1")
    firefox_profile.set_preference("network.proxy.socks_port", 9050)
    firefox_profile.set_preference("network.proxy.socks_remote_dns", True)
    # firefox_profile.set_preference("browser.privatebrowsing.autostart", True)

    return webdriver.Firefox(
        firefox_profile=firefox_profile,
        firefox_binary="C:/Program Files (x86)/Mozilla Firefox/firefox.exe",
        executable_path="./geckodriver.exe")


def vote():
    driver = firefox_proxy_driver()
    driver.set_window_size(900, 1080)
    driver.get("http://sztuka-architektury.pl/")

    try:
        popup_close = driver.find_element_by_id("newsletter_close")
        popup_close.click()

        publiczne = driver.find_elements_by_xpath("//span[contains(text(), 'PUBLICZNE')]")
        publiczne = publiczne[0]
        print("Znalazłem PUBLICZNE")
        # publiczne = WebDriverWait(driver, 45).until(
        #     EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'PUBLICZNE')]"))
        # )

        if publiczne:
            # find "PUBLICZNE" button by query selector, since no class and no id on the button
            driver.execute_script("document.querySelector('[data-id=\"question/83\"]').click();")

            try:
                poll_numbers = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "poll-numbers"))
                )
                if poll_numbers:
                    print("znalazłem poll-numbers")
                    sleep(3)
                    driver.quit()
            except:
                print("nie znalzałem poll-numbers")

            try:
                radio = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.ID, "r443"))
                )
                print("Znalazłem RADIO")

                driver.execute_script("document.getElementById('r443').click();")

                glosuj = driver.find_element_by_class_name("sd")
                print("Znalazlem GLOSUJ")

                driver.execute_script("document.getElementsByClassName('sd')[0].click();")

            except:
                print("--> nie znalazłem RADIO/GLOSUJ")

    except:
        print("--> nie znalazłem PUBLICZNE")

    try:
        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, "//p[contains(text(), 'Dziękujemy za oddanie głosu')]"))
        )
        logger.make_log_file(True)
        sleep(5)
        driver.quit()
    except:
        logger.make_log_file(False)
        driver.quit()

    # LOOP
    try:
        vote()
    except:
        vote()


if __name__ == "__main__":
    vote()

