from selenium import webdriver
import time
import json

from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

# Input your local variables
with open("LoginData.json") as file:
    data = json.load(file)
    FACEBOOK_LOGIN = data["facebook"]["email"]
    FABOOK_PASSWORD = data["facebook"]["password"]
    CHROME_DRIVER = data["chrome"]["driver"]

LIKES_PER_SESSION = 15
STANDARD_WAIT = 3
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
        allow_btn = driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/button[1]')
    except:
        print("Não pediu Permissão")
    else:
        allow_btn.click()

    try:
        accept_btn = driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div/div/div[1]/button')
    except:
        print("Não pediu para Aceitar Termos")
    else:
        accept_btn.click()

    try:
        not_notify_btn = driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/button[2]')
    except:
        print('Não pediu para Notificar')
    else:
        not_notify_btn.click()


def like():
    print(f"Waiting {STANDARD_WAIT} seconds to go to Next Like")
    time.sleep(STANDARD_WAIT)



    # Try to hit like
    try:
        like_btn = driver.find_element_by_xpath(
            '//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[2]/div[4]/button')
        like_btn.click()

    # Maybe it doesn't find due to a popup that must be closed
    except NoSuchElementException as e:
        print("Like apontou a Exception NoSuchElement")
        # print(e)
        try:
            no_thanks = driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/button[2]')
            no_thanks.click()
        except Exception as e:
            # print(e)
            like()

    # Componente em cima do like
    except ElementClickInterceptedException as e:
        print("Like apontou a Exception ElementClickIntercepted")

        try:
            no_thanks = driver.find_element_by_xpath('//*[@id="modal-manager"]/div/div/button[2]')
            no_thanks.click()
        except:
            print("Mandando Mensagem de olá")
            # Get the name of the person
            name = driver.find_element_by_xpath('//*[@id="modal-manager-canvas"]/div/div/div[1]/div/div[3]/div[2]').text.split()[0]
            mandar_hello = driver.find_element_by_xpath('//*[@id="chat-text-area"]')
            mandar_hello.send_keys(f"E aí {name}, como vc tá?")
            time.sleep(2)
            mandar_hello.send_keys(Keys.ENTER)
            # close_popup_btn = driver.find_element_by_xpath('//*[@id="modal-manager-canvas"]/div/div/div[1]/div/div[4]/button')
            # close_popup_btn.click()
        else:
            print("Clicando no Não Obrigado")
    else:
        print(f"Like enviado com sucesso!")



chrome_driver_path = CHROME_DRIVER

# Get Chrome's Cookies, so you don't have to keep logging in
chrome_options = Options()
chrome_options.add_argument("user-data-dir=selenium")

driver = webdriver.Chrome(executable_path=chrome_driver_path, options=chrome_options)
driver.get(TINDER_URL)

login()

for _ in range(LIKES_PER_SESSION):
    like()