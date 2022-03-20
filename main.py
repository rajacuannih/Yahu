#!/usr/bin/env python

import random, json, pause, pickle
from time import sleep
from icecream import ic
from MODULES.basics import *
from MODULES.download_driver import *
from MODULES.proxies import *


CWD               = os.getcwd()
DRIVER_DIRECTORY  = os.path.join(CWD, 'PATCHED_DRIVERS')
PLUGIN_FILE       = os.path.join('EXTENSION')
PROXIES           = open("GoodProxy.txt").read().splitlines()
UAS               = open("GoodUa.txt").read().splitlines()
WINDOW_SIZE       = "400,837"

ELEMENTS = {
	"SIGNUP_01":"return document.querySelector(\"#signin-menu > li:nth-child(4) > a\");",
	"SIGNUP_02":"return document.querySelector(\"#createacc\");"
}

class IsiFormException(Exception):
	pass

def click_signup():
	try:
		# click signing up..
		SIGNUP = DRIVER.execute_script(ELEMENTS['SIGNUP_01'])
		if SIGNUP:
			SIGNUP.click()
		elif not SIGNUP:
			DRIVER.execute_script(ELEMENTS['SIGNUP_02']).click()

		return True
	except Exception as e:
		return e

def chrome(USER_AGENT, PROXY):
	EXE_NUMBER = random.randint(1, 5)
	PATCHED_DRIVER = os.path.join(DRIVER_DIRECTORY, f'chromedriver_{EXE_NUMBER}.exe')
	DRIVER = get_driver(False, WINDOW_SIZE, USER_AGENT, False, PATCHED_DRIVER, PROXY, "http", PLUGIN_FILE)
	DRIVER.get("https://www.google.com/")
	return DRIVER

def store_cookie(DRIVER, USERNAME):
    with open(USERNAME + ".pkl","wb") as file:
        pickle.dump(DRIVER.get_cookies(), file)
        print(str(DRIVER.get_cookies()))
        print("Cookie String Added. You are good to go!")
    return DRIVER

def main(ARGUMENT):
	pass

if __name__=="__main__":
	ARGUMENT = sys.argv[1]
	USER_AGENT = random.choice(UAS)
	PROXY = random.choice(PROXIES)
	ARGUMENTS = ARGUMENT.split(",")
	FIRST_NAME = ARGUMENTS[0]
	LAST_NAME = ARGUMENTS[1]
	MAIL_NAME = ARGUMENTS[2]
	PHONE_NUMBER = ARGUMENTS[3]
	DRIVER = chrome(USER_AGENT, PROXY)

	PASSWORD = "hellofool31:*"
	DRIVER.get("https://mail.yahoo.com/")
	SIGNUP = click_signup()
	if SIGNUP:
		pause.seconds(random.randint(1, 5))
		try:
			input_first = DRIVER.execute_script(f"return document.querySelector(\"#usernamereg-firstName\");")
			for letter in FIRST_NAME:
				input_first.send_keys(letter)
				sleep(random.uniform(.1, .4))
			input_last = DRIVER.execute_script(f"return document.querySelector(\"#usernamereg-lastName\");")
			for LETTER in LAST_NAME:
				input_last.send_keys(LETTER)
				sleep(random.uniform(.1, .4))
			DRIVER.execute_script(f"document.querySelector(\"#usernamereg-yid\").value = \"{MAIL_NAME}\";")
			DRIVER.execute_script(f"document.querySelector(\"#usernamereg-password\").value = \"{PASSWORD}\";")
			DRIVER.execute_script(f"document.querySelector(\"#usernamereg-month\").value = \"{random.randint(1,12)}\";")
			DRIVER.execute_script(f"document.querySelector(\"#usernamereg-day\").value = \"{random.randint(1, 28)}\";")
			DRIVER.execute_script(f"document.querySelector(\"#usernamereg-year\").value = \"199{random.randint(1,9)}\";")
			DRIVER.execute_script("document.querySelector(\"#usernamereg-freeformGender\").value = \"male\";")
			DRIVER.execute_script(f"document.getElementsByName(\"shortCountryCode\")[0].value = \"ID\";var event = new Event(\"change\");document.getElementsByName(\"shortCountryCode\")[0].dispatchEvent(event);")
			input_number = DRIVER.execute_script(f"return document.querySelector(\"#usernamereg-phone\");")
			for NUMBER in PHONE_NUMBER:
				input_number.send_keys(NUMBER)
				sleep(random.uniform(.1, .4))

			pause.seconds(3)
			DRIVER.execute_script("document.querySelector(\"#reg-submit-button\").click();")
		except Exception as e:
			raise IsiFormException

	elif not SIGNUP:
		os.system(f"python main.py {ARGUMENT}")

	input("Press any key..")
	store_cookie(DRIVER, MAIL_NAME)
	DRIVER.quit()