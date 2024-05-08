from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
import pyautogui
import pyperclip
import shutil
import zipfile
import keyboard

from config import PATH_CHROME, PATH_SHEETS, NEW_PATH,NEXT_BP,NEXT_BP_PWD,NEXT_BP_USER, NEXT_ERP_USER,NEXT_ERP,NEXT_ERP_PWD,NEXT_ERP_USER,NEXT_ERP_PWD2,NEXT_ERP_USER2,FSIST,FSIST_LOGIN,FSIST_PWD,DOWNLOAD_PATH,NF_PATH,VM_ERP,VM_PW,VM_USER
from selenium.webdriver.chrome.service import Service as ChromeService


chrome_service = ChromeService(PATH_CHROME)
chrome_options = webdriver.ChromeOptions()
prefs = {'download.default_directory': PATH_SHEETS}
chrome_options.add_experimental_option('prefs', prefs)
chrome_options.add_argument("--start-maximized")
chrome = webdriver.Chrome(service=chrome_service, options=chrome_options)


# Abre a página da web
chrome.get(NEXT_BP)
time.sleep(5)
pyautogui.press('esc')
time.sleep(2)
#-- INSERT USER
chrome.find_element(By.XPATH,'//*[@id="username"]/div/div[1]/input').click()
pyperclip.copy(NEXT_BP_USER)
pyautogui.hotkey('ctrl', 'v')
time.sleep(1)

#-- INSERT PWD
chrome.find_element(By.XPATH,'//*[@id="password"]/div/div[1]/input').click()
pyperclip.copy(NEXT_BP_PWD)
pyautogui.hotkey('ctrl', 'v')
time.sleep(1)

#-- SUBMIT
chrome.find_element(By.XPATH,'//*[@id="dxButtonEntrar"]').click()
time.sleep(100000)