import gc
import sys
import os
import time
import pyautogui
import pyperclip
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

from threading import Thread
# from navigator import processesActivities, getData, getNFInfo,declineRequest,getPrintValue,getERPInfo,getItemNumber,bpDeclineAuth,enterNFE,getFSIST,putXML,approveRequest
from config import PATH_CHROME, PATH_SHEETS, NEW_PATH
from pynput.mouse import Controller, Button


from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By

from functions.pandas_script import readClient,extract_text_from_pdf
from functions.logger import logger
from functions.Tim import getPSWRD,authSiebel,newAtt,searchCliente,getClienteinfo,downloadInvoice
from functions.initConfig import initSplash
#from functions.script_ocr import getValueNF


os.chdir(NEW_PATH)
print(NEW_PATH)
print(os.getcwd())

##--- INIT PROCESS
if __name__ == "__main__":
    app, message_window = initSplash()

    def run_main_program():
        gc.collect()
        mouse = Controller()

        logger(f"PROCESSO INICIADO")  

        #ROCHA ROCHA ROCHA ROCHA ROCHA ROCHA

        #--- INIT PROCESS
        chrome_service = ChromeService(PATH_CHROME)
        chrome_options = webdriver.ChromeOptions()
        prefs = {'download.default_directory': PATH_SHEETS}
        chrome_options.add_experimental_option('prefs', prefs)
        chrome_options.add_argument("--start-maximized")
        chrome = webdriver.Chrome(service=chrome_service, options=chrome_options)
        

        #--- AUTHENTICATE -- SIEBEL
        logger(f'Etapa de coletar a senha no RSA')
        pwrd = getPSWRD()
        if pwrd is None:
            logger(f'Não foi possivel coletar a SENHA no RSA')
            return
        logger(f'Etapa de coletar a senha no RSA Finalizada')

        logger(f'Etapa de entrar o SIEBEL')
        auth = authSiebel(chrome,pwrd)
        if not auth:
            logger(f'Não foi possivel fazer o login no SIEBEL')
            return
        logger(f'Etapa de entrar no SIEBEL Finalizada')

        logger(f'Etapa de entrar em Nova Solicitação')
        nova_att = newAtt(chrome)
        if not nova_att:
            logger(f'Não foi possivel entrar em nova Solicitação')
            return
        logger(f'Etapa de entrar em Nova Solicitação Finalizada')

        logger(f'Etapa de coletar os numeros dos clientes')
        base_cliente = []
        base_cliente = readClient()
        if len(base_cliente) <= 0:
            logger(f'Erro ao coletar os numeros dos clientes')
            return
        logger(f'Etapa de coletar os numeros dos clientes finalizada')

        os.chdir(NEW_PATH)
        logger(f'Etapa de pesquisar os clientes no SIEBEL')
        for cliente in base_cliente:
            logger(f'Etapa de Pesquisar Cliente {cliente}')
            cliente_pesquisado = searchCliente(chrome, cliente)
            logger(f'Etapa de Pesquisar Cliente {cliente} Finalizada')
            logger(f'Inicio da etapa de Coletar informações do Cliente {cliente}')
            infos_cliente = getClienteinfo(chrome,cliente)
            logger(f'Etapa da coleta de informação do cliente {cliente} Finalizado')
            logger(f'Etapa de download da Fatura')
            baixar_fatura = downloadInvoice(chrome, cliente)
            logger(f'Colocando informações no Excel')
            extract_text_from_pdf(numero_cliente=cliente,nome=infos_cliente[0],cpf=infos_cliente[1])
            time.sleep(1000000)

        
        
        

#         #--- NAVIGATE ATIVIDADES DE PROCESSOS 
#         time.sleep(2)
#         navigator = processesActivities(chrome)
#         if not navigator:
#             logger(f"Não foi possivel navegar para a tela de atividades. O processo foi finalizado.")
#             return
#         logger(f'ProcessesActivities Finalizado com Sucesso!')

#         #--- EXTRACT DATA FILE 

#         time.sleep(1)
#         logger(f'getData Iniciado!')
#         save_data = getData(chrome)
#         if save_data is None or not save_data.startswith('Exportacao_'):
#             logger(f'Falha ao baixar o arquivo')
#             return
#         logger(f'getData Finalizado com Sucesso!')

#         #--- GET NUMBER WITH PANDAS
#         number = []
#         number = getNumber(save_data)
#         logger(f'{number}')
#         if not number:
#             logger(f'Nenhum valor encontrado na lista')
#             return
#         logger(f'GetNumber Finalizado com Sucesso!')
        
#         logger(f'GetNFInfo Iniciado!')
#         for item in number:
#             getNFInfo(chrome,item)
#             if not getNFInfo:
#                 logger(f'Erro ao baixar PDF')
#                 return
#         logger(f'GetNFInfo Finalizado')
        
#         logger(f'Inicio da primeira Verificação')
#         for item in number:
#             status = firstApprove(item)
#             if status is not None and 'diferente' in status:
#                 logger(f'Pedido não é de consumo, indo para o próximo')
#                 continue
#             if status is not None and 'nao' in status:
#                 decline = declineRequest(chrome,item,status)
#                 if not decline:
#                     logger(f'Nao foi possivel recusar a solicitação')
#                     return
#         logger(f'Final da Primeira  Verificação')

#         indice = 1
#         for item in number:
#             verif = orderStatus(item,status = '99')
#             if 'exec' not in verif:
#                 continue
#             infosNF = []
#             infosNF = getInfoERP(item)
#             financeiro = infosNF[0]
#             estoque = infosNF[1]
#             order = infosNF[2]
#             filial = infosNF[3]
#             empresa = infosNF[4]
#             tipo = infosNF[5]
#             nf = infosNF[6]
#             #if 'CONSUMO' not in tipo:
#             #    logger(f'{item}, não é uma solicitação de consumo')
#             #    continue
#             #logger(f'Iniciando o FSIST')
#             #fsis = getFSIST(chrome,number=nf, indice = indice)
#             #indice = indice +1
#             #if fsis is None or 'nao' in fsis:
#             #    error = (f'Não foi possivel baixar o XML de {nf} do pedido {item}')
#             #    putResult(item, error)
#             #    updateStatus(item, status= '99')
#             #    continue
            
#         #logger(f'Iniciando o processo XML')
#         #statusxml = putXML(chrome)
#         #if not statusxml:
#         #    logger(f'Erro ao passar o XML para pasta')
#         #    return
#         #logger(f'Final da etapa PutXML')
        
#         logger(f'Inicio da etapa dados ERP')
#         for item in number:
#             verif = orderStatus(item,status = '99')
#             if 'exec' not in verif:
#                 continue
#             infosNF = []
#             infosNF = getInfoERP(item)
#             financeiro = infosNF[0]
#             estoque = infosNF[1]
#             order = infosNF[2]
#             filial = infosNF[3]
#             empresa = infosNF[4]
#             tipo = infosNF[5]
#             nf = infosNF[6]
#             logger(f'{tipo}')
#             logger(f'{estoque}')
#             logger(f'{financeiro}')
#             if 'COMPRA CONSUMO' not in tipo:
#                 logger(f'{item}, não é uma solicitação de consumo')
#                 continue
#             tm = getTM(desc=tipo,estoque=estoque,finan=financeiro)
#             if tm == 0:
#                 logger(f'TM não foi encontrado no DEPARA')
#                 pyautogui.click(616,23)
#                 continue
#             getERP = getERPInfo(chrome,item,order,filial,empresa)
#             if not getERP:
#                 error = (f'Erro ao coletar informaçoes da request {item}, verifique se o pedido {order} esta correto!')
#                 pyautogui.click(616,23)
#                 putResult(item, error)
#                 updateStatus(item, status= '99')
#                 continue
#             print = getPrintValue(item)
#             if not print:
#                 logger(f'Erro ao tentar coletar print do Valor da Nota')
#                 return
#             blank = clearBlankSpace(item,action='ncm')
#             if not blank:
#                 logger(f'Erro ao retirar espaços em branco')
#                 return
#             logger(f'Pegando valor da nota {item}')
#             valor_total = getValueNF(item)
#             logger(f'Coletando NCM {item}')
#             ncm = []
#             ncm = getInTXT(item,action='ncm')
#             if not ncm:
#                 logger(f'Não foi possivel coletar o NCM')
#                 return
#             logger(f'Verificando informações na NF {item}')
#             check_pdf = erpAprrove(item,valor_total,ncm)
#             if 'nao' in check_pdf:   
#                 pyautogui.click(616,23)
#                 error = check_pdf
#                 putResult(item, error)
#                 updateStatus(item, status= '99')
#                 continue
#             logger(f'Coletando o iD dos itens')
#             num_produto = getItemNumber(chrome,item)
#             if not num_produto:
#                 logger(f'Não foi possivel coletar o ID do Item')
#                 return
#             number_item = []
#             item_blank = clearBlankSpace(item,action='item')
#             if not item_blank:
#                 logger(f'Não foi possivel tirar blank do item')
#                 return
#             number_item = getInTXT(item,action='item')
#             if not number_item:
#                 logger(f'Não foi possivel coletar o numero do item')
#                 return
#             result = enterNFE(nf,number_item,order,tm)
#             if result is None or 'nao' in result:
#                 logger(f'Erro ao tentar dar entrada na NF')
#                 pyautogui.click(616,23)
#                 updateStatus(item, status= '99')
#                 if result is None:
#                     putResult(item,status = 'Erro ao dar entrada na NF')
#                     continue
#                 putResult(item,status = result)
#                 continue
#             putResult(item,status = 'finalizado')
#             updateStatus(item, status= '99')
#         logger(f'Final da etapa dados ERP')

#         final = finalFiles()
#         bpDeclineAuth(chrome)
#         final_navigator = processesActivities(chrome)
#         if not final_navigator:
#             logger(f"Não foi possivel navegar para a tela de atividades. O processo foi finalizado.")
#             return
        

#         for item in final:
#             result = finalResult(item)
#             if 'finalizado' in result:
#                 approve = approveRequest(chrome,item)
#                 if not approve:
#                     logger(f'Não foi possivel finalizar a solicitação')
#                     return
#             if not 'finalizado' in result:
#                 decline = declineRequest(chrome,item,result)
#                 if not decline:
#                     logger(f'Não foi possivel Recusar a solicitação')
#                     return
#         logger(f'Final do Fluxo')



main_thread = Thread(target=run_main_program)
main_thread.start()

sys.exit(app.exec_())       