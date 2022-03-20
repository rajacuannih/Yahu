#!/usr/bin/env python
import pause, selenium
import argparse, time, io
import logging, uuid, shutil
import sys, os, re, string
import datetime, pickle
import requests, random, names, download
from selenium import webdriver
from threading import Thread
from icecream import ic
from subprocess import call
import undetected_chromedriver as uc
from time import sleep
from MODULES.basics import *
from MODULES.download_driver import *
from MODULES.proxies import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from undetected_chromedriver.patcher import Patcher
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

CWD                 = os.getcwd()
UAS                 = open("GoodUa.txt").read().splitlines()
PROXIES             = open("GoodProxy.txt").read().splitlines()
PLUGIN_FILE         = os.path.join('EXTENSION')
DRIVER_DIRECTORY    = os.path.join(CWD, 'PATCHED_DRIVERS')
WINDOW_SIZE: str    = "400,837"
HEADLESS: bool      = False
CLEAR_RECENT_DRIVER = False


PICKLE_FOLDER = "YAHOO_PICKLE"
BASE_URL      = "https://login.yahoo.com/"

def all_drivers():
    drivers = []
    for root, dirname, files in os.walk(DRIVER_DIRECTORY):
        for file in files:
            drivers.append(os.path.join(DRIVER_DIRECTORY, file))
    return drivers

def delete_recent_driver():
    drivers = os.listdir(DRIVER_DIRECTORY)
    for driver in drivers:
        os.remove(os.path.join(DRIVER_DIRECTORY, driver))

    return True

def rename_all_driver(DRIVER_PREFIXS):
    i = 0
    drivers = all_drivers()
    for PREFIX in DRIVER_PREFIXS:
        PREFIX = "chromedriver_" + PREFIX + ".exe"
        os.rename(drivers[i], os.path.join(DRIVER_DIRECTORY, PREFIX))
        i += 1

def monkey_patch_exe(DRIVER_DIRECTORY):
    linect = 0
    replacement = Patcher.gen_random_cdc()
    replacement = f"  var key = '${replacement.decode()}_';\n".encode()
    with io.open(DRIVER_DIRECTORY, "r+b") as fh:
        for line in iter(lambda: fh.readline(), b""):
            if b"var key = " in line:
                fh.seek(-len(line), 1)
                fh.write(replacement)
                linect += 1
        return linect

def store_cookie(DRIVER, USERNAME):
    with open(USERNAME + ".pkl","wb") as file:
        pickle.dump(DRIVER.get_cookies(), file)
        print(str(DRIVER.get_cookies()))
        print("Cookie String Added. You are good to go!")
    return DRIVER

def redirect(BASE_URL):
    options = uc.ChromeOptions()
    if HEADLESS:
        options.add_argument('--headless')

    options.add_argument("--start-maximized")
    DRIVER = uc.Chrome(options = options)
    DRIVER.get(BASE_URL)
    return DRIVER

def akun(PICKLE_FOLDER):
    _list_ = []
    for root, dirname, files in os.walk(os.getcwd() + "/" + PICKLE_FOLDER + "/"):
        for file in files:
            _list_.append(file)
    return _list_

def load_required_pickle(DRIVER, USERNAME):
    cookies = pickle.load(open(PICKLE_FOLDER + "/" + USERNAME, "rb"))
    print(f"Pickle {USERNAME} Loaded..")
    for cookie in cookies:
        try:
            DRIVER.add_cookie(cookie)
        except selenium.common.exceptions.InvalidCookieDomainException as e:
            DRIVER.get(BASE_URL.replace("login", "mail"))
    return DRIVER

def chrome(USER_AGENT, PROXY, DRIVER_PREFIX):
    PATCHED_DRIVER = os.path.join(DRIVER_DIRECTORY, f'chromedriver_{DRIVER_PREFIX}.exe')
    DRIVER = get_driver(False, WINDOW_SIZE, USER_AGENT, False, PATCHED_DRIVER, PROXY, "socks4", PLUGIN_FILE)
    DRIVER.get(BASE_URL)
    return DRIVER

if __name__=="__main__":
    i = 0
    delete_recent_driver()
    USERNAMES = akun(PICKLE_FOLDER)
    DRIVER_PREFIXS = [v.split(".pkl")[0] for v in USERNAMES]
    DOWNLOAD_DRIVERS = download.main(len(USERNAMES))
    if DOWNLOAD_DRIVERS:
        rename_all_driver(DRIVER_PREFIXS)
        for USERNAME in USERNAMES:
            DRIVER_PREFIX = DRIVER_PREFIXS[i]
            USER_AGENT = random.choice(UAS)
            PROXY = random.choice(PROXIES)
            try:
                DRIVER = chrome(USER_AGENT, PROXY, DRIVER_PREFIX)
                load_required_pickle(DRIVER, USERNAME)
                DRIVER.refresh()
                x = input("store cookies (y/n): ")
                if "y" in x:
                    store_cookie(DRIVER, USERNAME)
                    DRIVER.quit()
                else:
                    DRIVER.quit()
                    continue
            except KeyboardInterrupt:
                sys.exit(os.system("killdrive.bat"))

            i+=1