from PIL import ImageGrab, ImageEnhance, ImageFilter, Image
import pytesseract
import os
from datetime import datetime
from functions.logger import createFolder, logger
import random
import string
import time
import sys
import glob
import pygetwindow as gw
import pyautogui
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import PyPDF2
from pynput.mouse import Controller, Button
import pyperclip


def screenShotForText(x1, y1, x2, y2, save = False):
    captura = ImageGrab.grab(bbox=(x1, y1, x2, y2))
    time.sleep(2)
    if save:
        thisFolder = createFolder()
        named = generateHash()
        named = os.path.join(thisFolder, f"{named}.png")
        captura.save(named)
 
    # Pré-processamento adicional
    captura = captura.resize((captura.width * 3, captura.height * 3))  # Aumentar o tamanho
    captura = captura.convert("L")  # Converter para escala de cinza
    captura = captura.point(lambda x: 0 if x < 128 else 255)  # Binarização
    
    # Configurações do Tesseract
    captura = captura.filter(ImageFilter.SHARPEN)
    captura = ImageEnhance.Contrast(captura).enhance(2.0)

    config = '--psm 6'  
    text = pytesseract.image_to_string(captura, config=config)
    time.sleep(4)

    if not text:
        text = pytesseract.image_to_string(captura, config=config)

    logger(f"Screenshot registrado com sucesso, string encontrada: {str(text)}")

    return text

def generateHash(length=8):
    characters = string.ascii_letters + string.digits
    random_hash = ''.join(random.choice(characters) for _ in range(length))
    return random_hash

def pathImg(folder, image_name):
    script_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    script_dir = os.path.dirname(script_dir)
    image_path = os.path.join(script_dir, folder, image_name)

    if not os.path.exists(image_path) and getattr(sys, 'frozen', False):
        temp_dir = sys._MEIPASS
        image_path = os.path.join(temp_dir, folder, image_name)
    
    return str(image_path)

def getLastArchive(path):
    todos_arquivos = glob.glob(os.path.join(path, '*'))

    # Ordena os arquivos por data de modificação (o mais recente primeiro)
    arquivos_ordenados = sorted(todos_arquivos, key=os.path.getmtime, reverse=True)
    last = arquivos_ordenados[0]
    print("ARQUIVO: "+str(last))

    return last

def findTextScreen(x1, y1, x2, y2, text, save = False):
    screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2)) 

    if save:
        thisFolder = createFolder()
        named = generateHash()
        named = os.path.join(thisFolder, f"{named}.png")
        screenshot.save(named)

    screenshot = screenshot.resize((screenshot.width * 2, screenshot.height * 2))  # Aumentar o tamanho
    screenshot = screenshot.convert("L")  # Converter para escala de cinza
    screenshot = screenshot.point(lambda x: 0 if x < 128 else 255)  # Binarização
    
    # Configurações do Tesseract
    screenshot = screenshot.filter(ImageFilter.SHARPEN)
    screenshot = ImageEnhance.Contrast(screenshot).enhance(2.0)

    config = '--psm 6'  
    extracted_text = pytesseract.image_to_string(screenshot, config=config)
    time.sleep(2)

    return str(extracted_text)
    if text in extracted_text:
        return True
    else:
        return False

def findTextPdf(path, text):
    with open(path, 'rb') as arquivo_pdf:
        leitor_pdf = PyPDF2.PdfReader(arquivo_pdf)
        time.sleep(1)
        # Itera sobre todas as páginas do PDF
        for numero_pagina in range(len(leitor_pdf.pages)):
            pagina = leitor_pdf.pages[numero_pagina]
            texto_pagina = pagina.extract_text()
            time.sleep(1)

            # Verifica se o texto procurado está na página
            if text in texto_pagina:
                return texto_pagina

    return False

def copyInPurchase():
    mouse = Controller()

    time.sleep(1)
    pyautogui.moveTo(800, 300)
    mouse.click(Button.right, 1)
    time.sleep(1)
    pyautogui.moveTo(810, 310)
    pyautogui.click(810, 310)
    time.sleep(1)

    return(str(pyperclip.paste().strip()))