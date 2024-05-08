import easyocr
import os
import re


def getValueNF(item):
    os.chdir('S:\\2RFP\\JM_DOC ALTERAÇOES\\jm\\functions')
    # Inicializa o EasyOCR
    reader = easyocr.Reader(['pt'])  # Especifique o idioma desejado

    # Carrega a imagem
    
    image_path = f'value\\{item}.png'
    result = reader.readtext(image_path)

    # Processa o resultado para obter o texto
    texto_extraido = ' '.join([entry[1] for entry in result])

    # Use uma expressão regular para encontrar números (incluindo vírgulas e pontos)
    numeros_decimais = re.findall(r"\d+,\d+", texto_extraido)

    # Se houver números decimais encontrados, pegue o primeiro
    if numeros_decimais:
        valor_decimal = float(numeros_decimais[0].replace(',', '.'))  # Substitua a vírgula por ponto
        valor_formatado = f"{valor_decimal:.2f}".replace('.', ',')  # Formate para duas casas decimais e substitua ponto por vírgula
        return valor_formatado
    
def checkFound():
    print('a')
