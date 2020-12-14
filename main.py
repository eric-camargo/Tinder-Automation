from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import json

import XPaths

# Input your local variables
with open("LoginData.json") as file:
    data = json.load(file)
    FACEBOOK_LOGIN = data["facebook"]["email"]
    FABOOK_PASSWORD = data["facebook"]["password"]
    CHROME_DRIVER = data["chrome"]["driver"]

print(CHROME_DRIVER)
send_custom_message = True
LIKES_PER_SESSION = 5
SESSIONS = 3
STANDARD_WAIT = 2
TINDER_URL = "https://tinder.com/"

def signin_click():
    # Clicar em Entrar
    botoes_header = driver.find_elements_by_css_selector('header button')
    botao_entrar = botoes_header[1]
    botao_entrar.click()


def login():
    time.sleep(STANDARD_WAIT)
    if driver.current_url == TINDER_URL:
        signin_click()
        login_with_facebook()

    clear_popups()


def login_with_facebook():
    # Clicar em Entrar com Facebook
    entrar_fb = driver.find_elements_by_css_selector("#modal-manager .button")[1]
    entrar_fb.click()

    # Mudar para o Popup
    base_window = driver.window_handles[0]
    fb_login_window = driver.window_handles[-1]
    driver.switch_to.window(fb_login_window)
    print(driver.title)
    time.sleep(STANDARD_WAIT)

    # Login
    email_handle = driver.find_element_by_id("email")
    password_handle = driver.find_element_by_id("pass")

    email_handle.send_keys(FACEBOOK_LOGIN)
    password_handle.send_keys(FABOOK_PASSWORD)
    password_handle.send_keys(Keys.ENTER)

    while len(driver.window_handles) > 1:
        print("waiting Facebook to close")
        time.sleep(STANDARD_WAIT)

    # Switch back to main window
    driver.switch_to.window(base_window)
    time.sleep(STANDARD_WAIT)


def clear_popups():
    try:
        allow_btn = driver.find_element_by_xpath(XPaths.ALLOW_POPUP_BUTTON)
        allow_btn.click()
    except Exception as e:
        print(e)

    try:
        accept_btn = driver.find_element_by_xpath(XPaths.ACCEPT_LOCATION_BUTTON)
        accept_btn.click()
    except Exception as e:
        print(e)

    try:
        not_notify_btn = driver.find_element_by_xpath(XPaths.DO_NOT_NOTIFY_BUTTON)
        not_notify_btn.click()
    except Exception as e:
        print(e)

def send_likes():
    print(f"Waiting {STANDARD_WAIT} seconds to go to Next Like")
    time.sleep(STANDARD_WAIT)

    # Try to hit like
    try:
        like_btn = driver.find_element_by_xpath(XPaths.LIKE_BUTTON)
        like_btn.click()

    # Maybe it doesn't find due to a popup that must be closed
    except NoSuchElementException as e:
        print(e)
        try:
            no_thanks = driver.find_element_by_xpath(XPaths.NO_SUPERLIKE_THANKS)
            no_thanks.click()
        except Exception as e:
            print(e)
            send_likes()

    # Componente em cima do like
    except ElementClickInterceptedException as e:
        print(e)
        try:
            # Deal with popup asking if you'd like to super like someone
            no_thanks = driver.find_element_by_xpath(XPaths.NO_SUPERLIKE_THANKS)
            no_thanks.click()
        except:
            # Dealing with case where you've matched after a like
            if send_custom_message:
                # Get the name of the person
                name = driver.find_element_by_xpath(XPaths.MATCHED_PERSON_NAME).text.split()[0]

                # Automatically Send Introductory Message
                mandar_hello = driver.find_element_by_xpath(XPaths.MATCHED_POPUP_INPUT)
                mandar_hello.send_keys(f"E aí {name}, como vc tá?")
                time.sleep(2)
                mandar_hello.send_keys(Keys.ENTER)
                print("Sent Custom Message")
            else:
                # Or you can close the Match Popup everytime
                close_popup_btn = driver.find_element_by_xpath(XPaths.CLOSE_MATCH_POPUP_BUTTON)
                close_popup_btn.click()

    else:
        print(f"Like sent!")
        likes_sent += 1


chrome_driver_path = CHROME_DRIVER

# Get Chrome's Cookies, so you don't have to keep logging in
chrome_options = Options()
chrome_options.add_argument("user-data-dir=selenium")

for _ in range(SESSIONS):
    driver = webdriver.Chrome(executable_path=chrome_driver_path, options=chrome_options)
    driver.get(TINDER_URL)
    login()
    likes_sent = 0

    while likes_sent <= LIKES_PER_SESSION:
        send_likes()

    driver.close()
