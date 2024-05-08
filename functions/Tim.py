import pyautogui
import pyperclip
import time
import subprocess
from config import TIM_LOGIN,TIM_URL, RSA_EXEC,RSA_PIN,SIEBEL,PATH_CONTAS
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from functions.logger import logger
from functions.helpers import findTextScreen, getLastArchive, findTextPdf, screenShotForText, copyInPurchase
# from bs4 import BeautifulSoup
from pynput.mouse import Controller


def getPSWRD():
    #-- ABRINDO O RSA e PEGANDO A SENHA DA TIM
    pyautogui.press('win')
    time.sleep(0.2)
    pyautogui.write(RSA_EXEC)
    time.sleep(0.2)
    pyautogui.press('enter')
    time.sleep(0.5)
    pyautogui.write(RSA_PIN)
    time.sleep(0.4)
    pyautogui.press('enter')
    time.sleep(0.4)
    pyautogui.click(1079,610)
    time.sleep(0.5)
    pwrd = pyperclip.paste()
    pyautogui.hotkey('alt','f4')
    return pwrd

def authSiebel(chrome: webdriver.Chrome, pwrd):
    #-- ABRINDO A TIM - SIEBEL
    chrome.get(SIEBEL)
    time.sleep(5)
    pyautogui.press('esc')
    chrome.find_element(By.XPATH,'/html/body/div[1]/div[1]/div/div/article/div/div/div/div[3]/form/div[1]/div/input').click()
    time.sleep(0.5)
    pyautogui.write(TIM_LOGIN)
    pyautogui.press('tab')
    time.sleep(0.5)
    pyautogui.write(pwrd)
    pyautogui.press('tab')
    pyautogui.press('enter')
    time.sleep(35)
    return True


def newAtt(chrome: webdriver.Chrome):
    #-- MUDANDO O PDV 
    # pyautogui.click(1316,280)
    chrome.find_element(By.XPATH,'/html/body/div[1]/div/div[1]/div/div[16]/ul/li[2]/span').click()
    time.sleep(10)
    for _ in range(2):
        pyautogui.press('tab')
    time.sleep(0.5)
    for _ in range(3):
        time.sleep(1)
        pyautogui.press('down')
    time.sleep(0.5)
    pyautogui.press('enter')
    time.sleep(2)
    #--Clicando me NOVO ATENDIMENTO
    # pyautogui.click(1525,283)
    chrome.find_element(By.XPATH,'/html/body/div[1]/div/div[1]/div/div[16]/ul/li[3]/span').click()
    time.sleep(10)
    return True

def searchCliente(chrome: webdriver.Chrome,numero_cliente):
    numero_cliente = str(numero_cliente)
    #-- Clicando no campo numero de acesso (TELEFONE CLIENTE)
    chrome.find_element(By.XPATH,'/html/body/div[1]/div/div[6]/div/div[9]/div/div[1]/div/div/div[1]/div[2]/div/form/div/span/div[3]/div/div/table/tbody/tr[7]/td[3]/div/input').click()
    time.sleep(1)
    pyautogui.write(numero_cliente)
    time.sleep(2)
    chrome.find_element(By.XPATH,'/html/body/div[1]/div/div[6]/div/div[9]/div/div[1]/div/div/div[1]/div[2]/div/form/div/span/div[3]/div/div/table/tbody/tr[11]/td[4]/div/button').click()
    time.sleep(15)


def getClienteinfo(chrome: webdriver.Chrome, numero_cliente):
    #--Clicando no CPF do Cliente
    pyautogui.doubleClick(530,508,button='left')
    time.sleep(0.5)
    pyautogui.hotkey('ctrl','c')
    time.sleep(0.2)
    cpf = pyperclip.paste()
    #--Clicando no nome do cliente
    pyautogui.doubleClick(1150,491,button='left')
    pyautogui.doubleClick(1150,491,button='left')
    time.sleep(0.5)
    pyautogui.hotkey('ctrl','c')
    time.sleep(0.2)
    nome = pyperclip.paste()
    print(cpf)
    print(nome)
    pyautogui.press('pagedown')
    #-- Clicando em Outro Serviços
    chrome.find_element(By.XPATH,'/html/body/div[1]/div/div[6]/div/div[9]/div/div[1]/div/div[1]/div[3]/div/form/div/span/div[3]/div[2]/div/nav/ul/li[4]').click()
    time.sleep(2)
    pyautogui.press('tab')
    chrome.find_element(By.XPATH,'/html/body/div[1]/div/div[6]/div/div[9]/div/div[1]/div/div[1]/div[3]/div/form/div/span/div[3]/div[2]/div/nav/ul/li[4]/div/div/div/ul/li[1]/button').click()
    time.sleep(10)
    return[nome,cpf]
    
    

#-- SEGUNDA VIA DA CONTA
#---TAREFAS
def downloadInvoice(chrome: webdriver.Chrome,numero_cliente):
    chrome.find_element(By.XPATH,'/html/body/div[1]/div/div[6]/div/div[7]').click()
    time.sleep(5)
    pyautogui.moveTo(114,482)
    time.sleep(1)
    pyautogui.scroll(-90)
    time.sleep(10)
    chrome.find_element(By.XPATH,'/html/body/div[1]/div/div[6]/div/div[8]/div/div/div/div/div[2]/div/div[1]/div/ul/li/ul/li/ul/li[6]/span/span[2]').click()
    #pyautogui.click(137,708)
    time.sleep(5)
    #---PESQUISAR FATURAS
    pyautogui.press('esc')
    time.sleep(5)
    chrome.find_element(By.XPATH,'/html/body/div[1]/div/div[6]/div/div[9]/div/div[1]/div/div[4]/div/form/span/div/div[1]/div[2]/button[1]').click()
    #---VISUALIZAR FATURA
    time.sleep(10)
    chrome.find_element(By.XPATH,'/html/body/div[1]/div/div[6]/div/div[9]/div/div[1]/div/div[4]/div/form/span/div/div[1]/div[2]/button[2]').click()
    time.sleep(10)
    for _ in range(7):
        pyautogui.press('tab')
    time.sleep(0.5)
    pyautogui.press('space')
    time.sleep(3)
    #-- Colocar o path de download do PDF
    pyautogui.write(f'{PATH_CONTAS}{numero_cliente}.pdf')
    time.sleep(0.5)
    pyautogui.press('enter')
    time.sleep(20)
    pyautogui.hotkey('alt','f4')
    time.sleep(5)



      

# time.sleep(100000000)


# #time.sleep(10000)