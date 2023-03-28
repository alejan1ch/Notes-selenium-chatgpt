from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from time import sleep
import time
import threading
import subprocess
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import subprocess
from login import Login
from messages import Message

# Set up Chrome driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
actions = ActionChains(driver)
new_message = Message()


# Linkedin LogIn
new_login = Login(driver)

sleep(1)
# Navigate to job search page
url = "https://www.linkedin.com/search/results/people/?currentCompany=%5B%223006282%22%2C%2268198%22%5D&keywords=recruiter&origin=FACETED_SEARCH&page=6&sid=R(K"
driver.get(url)
sleep(3)
while True:
    try:
        last_height = driver.execute_script("return document.body.scrollHeight")
        start_time = time.time()
        # Hacemos scroll hasta el final de la página
        while True:
            driver.execute_script(
                "window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'});"
            )
            # Esperamos a que la página se cargue
            sleep(1)
            # Calculamos la nueva altura de la página y comparamos con la altura anterior
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                driver.execute_script(
                    "window.scroll({ top: 0, left: 0, behavior: 'smooth' });"
                )
                sleep(1)
                break
            last_height = new_height
            # Salimos del bucle si han pasado 5 segundos
            if time.time() - start_time >= 5:
                driver.execute_script(
                    "window.scroll({ top: 0, left: 0, behavior: 'smooth' });"
                )
                sleep(1)
                break
    finally:
        sleep(3)
        recruiters = driver.find_elements(
            By.CLASS_NAME, "reusable-search__result-container"
        )
        print(len(recruiters))

        for i in range(0, len(recruiters)):
            name = (
                recruiters[i]
                .find_element(
                    By.CSS_SELECTOR, 'span[dir="ltr"] > span[aria-hidden="true"]'
                )
                .text.replace('"', "")
            )
            info = (
                recruiters[i]
                .find_element(
                    By.CLASS_NAME,
                    "entity-result__primary-subtitle.t-14.t-black.t-normal",
                )
                .text.replace('"', "")
            )
            print(info)
            pos_at = info.find(" at ")
            pos_en = info.find(" en ")

            if pos_at == 0 or (pos_at > 0 and info[pos_at-1] == " "):
                position = ""
                company = info[pos_at+len(" at "):].strip()
                print('a')
            elif pos_en == 0 or (pos_en > 0 and info[pos_en-1] == " "):
                position = ""
                company = info[pos_en+len(" en "):].strip()
                print('e')
            elif pos_at > 0:
                position = info[:pos_at].strip()
                company = info[pos_at+len(" at "):].strip()
                print('a')
            elif pos_en > 0:
                position = info[:pos_en].strip()
                company = info[pos_en+len(" en "):].strip()
                print('e')
            else:
                position = info.strip()
                company = "Encora"
                print('n')
            print(f"{name}, {position}, {company}")

            try:
                print('i bc')
                button_con = recruiters[i].find_element(
                    By.CSS_SELECTOR, 'button.artdeco-button.artdeco-button--2.artdeco-button--secondary.ember-view[aria-label*="Invite"]'
                )
                actions.move_to_element(button_con).click().perform()
                print('f bc')
            except NoSuchElementException:
                try:
                    print('i mg')
                    button_msg = recruiters[i].find_element(
                        By.CSS_SELECTOR,
                        'div.entry-point  button[class="artdeco-button artdeco-button--2 artdeco-button--secondary ember-view"]',
                    )
                    actions.move_to_element(button_msg).click().perform()
                    print('f mg')
                except NoSuchElementException:
                    continue
                else:
                    try:
                        print('send msg?')
                        sub = 'Inquiry about IT positions at Encora'
                        msg = new_message.message(name, position, company)
                        sleep(1)
                        sub_input = driver.find_element(By.CSS_SELECTOR, 'input.artdeco-text-input--input[type="text"]')
                        actions.move_to_element(sub_input).double_click().send_keys(sub).perform()
                        
                        msg_input = driver.find_element(By.CSS_SELECTOR, 'div.msg-form__contenteditable[role="textbox"]')
                        actions.move_to_element(msg_input).double_click().send_keys(msg).perform()
                        sleep(1)
                        send_msg = driver.find_element(By.CSS_SELECTOR, 'button.msg-form__send-button.artdeco-button.artdeco-button--1[type="submit"]')
                        actions.move_to_element(send_msg).click().perform()
                        sleep(1)
                        close_btn = driver.find_element(By.CSS_SELECTOR, 'button[class="msg-overlay-bubble-header__control artdeco-button artdeco-button--circle artdeco-button--muted artdeco-button--1 artdeco-button--tertiary ember-view"]')
                        actions.move_to_element(close_btn).click().perform()    
                    except NoSuchElementException:
                        try:
                            btn_close = driver.find_element(By.CSS_SELECTOR, 'button[class="artdeco-modal__dismiss artdeco-button artdeco-button--circle artdeco-button--muted artdeco-button--2 artdeco-button--tertiary ember-view"]')
                            actions.move_to_element(btn_close).click().perform()
                        except NoSuchElementException:
                            close_btn = driver.find_element(By.CSS_SELECTOR, 'button[class="msg-overlay-bubble-header__control artdeco-button artdeco-button--circle artdeco-button--muted artdeco-button--1 artdeco-button--tertiary ember-view"]')
                            actions.move_to_element(close_btn).click().perform()
                            continue  
                        continue
            else:
                msg = f"""Dear {name}, are there any training opportunities currently available for Python developers at {company}? I would love to learn more about how I can apply and what the necessary requirements are. Thank you for your time and I look forward to your response. Best regards, Alejandro."""
                
                
                button_note = driver.find_element(
                    By.CSS_SELECTOR, 'button[aria-label="Add a note"]'
                )
                actions.move_to_element(button_note).click().perform()

                note_container = driver.find_element(
                    By.CSS_SELECTOR, 'textarea.ember-text-area[id="custom-message"]'
                )
                actions.move_to_element(note_container).double_click().send_keys(
                    msg.strip()
                ).perform()

                button_send = driver.find_element(
                    By.CSS_SELECTOR, 'button[aria-label="Send now"]'
                )
                actions.move_to_element(button_send).click().perform()

        next_btn = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Next"]')
        actions.move_to_element(next_btn).click().perform()
        sleep(2)

driver.quit()
