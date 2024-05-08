from selenium import webdriver
from selenium.webdriver.common.by import By
import json

# Função para capturar o XPath do elemento clicado
def capture_xpath():
    return '''
    function capture_xpath(element) {
        var xpath = '';
        while (element) {
            var tag_name = element.tagName;
            var sibling_index = 1;
            var sibling = element.previousElementSibling;
            while (sibling) {
                if (sibling.tagName == tag_name) {
                    sibling_index++;
                }
                sibling = sibling.previousElementSibling;
            }
            xpath = '/' + tag_name.toLowerCase() + '[' + sibling_index + ']' + xpath;
            element = element.parentElement;
        }
        return xpath;
    }
    '''

# Inicializa o driver do Selenium (neste exemplo, estou usando o Chrome)
driver = webdriver.Chrome()

# Abre a página da web
driver.get("https://nextbp.jmempilhadeiras.com.br/")

# Converte a função capture_xpath em string JavaScript para passar como argumento para execute_script
capture_xpath_script = capture_xpath()

# Adiciona um event listener para capturar cliques e chamar a função capture_xpath
driver.execute_script(
    """
    document.addEventListener('click', function(e) {
        e.preventDefault();
        var xpath = e.target.getAttribute('xpath');
        if (!xpath) {
            xpath = capture_xpath(e.target);
            e.target.setAttribute('xpath', xpath);
        }
        console.log('XPath do elemento clicado:', xpath);
    });
    """ + capture_xpath_script
)

# Mantém o script em execução para capturar cliques e exibir XPaths
input("Pressione Enter para sair...")

# Fecha o navegador
driver.quit()
