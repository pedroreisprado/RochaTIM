import pyautogui
import time
import shutil
import os
import pyperclip
import zipfile
import keyboard
import easyocr
import re

from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.common.by import By
from functions.logger import logger
from functions.helpers import pathImg
from functions.script_ocr import checkFound
#from config import DOWNLOAD_PATH,SAVE_PATH, INFO_NF_PATH, PDF_PATH,NEXT_ERP_USER,NEXT_ERP,NEXT_ERP_PWD,NEXT_ERP_USER2,NEXT_ERP_PWD2,NEXT_BP,NEXT_BP_PWD,NEXT_BP_USER,NEW_PATH,FSIST,FSIST_LOGIN,FSIST_PWD,NF_PATH,VM_ERP,VM_PW,VM_USER


def processesActivities():
    # pyautogui.press('win')
    # time.sleep(2)
    # pyautogui.write('template.xls')
    # time.sleep(2)
    # pyautogui.press('enter')
    # time.sleep(20)
    time.sleep(3)
    pyautogui.hotkey('ctrl','shift','space')
    time.sleep(1)
    pyautogui.hotkey('ctrl','c')
    

processesActivities()