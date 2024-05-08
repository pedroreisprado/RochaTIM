from PyPDF2 import PdfReader
import re


def extract_invoice_info(text):
    invoice_info = {}
    
    # Extrair CNPJ / CPF
    cnpj_cpf_line = text[text.find("CNPJ / CPF"):]
    cnpj_cpf = cnpj_cpf_line.splitlines()[1].strip()
    invoice_info["CNPJ_CPF"] = cnpj_cpf
    
    # Extrair Total da Nota
    total_nota_line = text[text.find("V. TOTAL DA NOTA"):]
    total_nota = total_nota_line.splitlines()[1].strip()
    invoice_info["Total_Nota"] = total_nota
    
    # Extrair informações dos produtos
    start_marker = "IPI"
    end_marker = "DADOS ADICIONAIS"
    produtos_text = text[text.find(start_marker) + len(start_marker): text.find(end_marker)]
    produtos_lines = produtos_text.strip().split("\n")
    
    produtos_info = []
    for line in produtos_lines:
        # Verifica se a linha contém dados de produto usando regex
        if re.match(r'^\d+\.\d+', line):
            produtos_info.append(line.strip())
    
    invoice_info["Produtos"] = produtos_info
    
    return invoice_info



def extract_text_from_pdf(pdf_file_path):
    text = ""
    with open(pdf_file_path, "rb") as pdf_file:
        pdf_reader = PdfReader(pdf_file)
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text += page.extract_text()
    return text

def search_value_in_pdf(pdf_file_path, value_to_search):
    found = False
    extracted_text = extract_text_from_pdf(pdf_file_path)
    if value_to_search in extracted_text:
        found = True
    return found

# Exemplo de uso
pdf_file_path = "C:\\2RFP\\jm\\pdf\\32280.pdf"
text_from_pdf = extract_text_from_pdf(pdf_file_path)

value_to_search = "84834090"

found_value = search_value_in_pdf(pdf_file_path, value_to_search)
if found_value:
    print(f"O valor {value_to_search} foi encontrado no PDF.")
else:
    print(f"O valor {value_to_search} não foi encontrado no PDF.")
