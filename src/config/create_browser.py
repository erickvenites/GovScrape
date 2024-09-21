import os
from dotenv import load_dotenv
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from seleniumwire import webdriver

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

browser = None

#Configuração do navegador 
def create_browser():
    global browser
    firefox_options = Options()
    firefox_options.add_argument("--headless")
    servico = Service('/usr/local/bin/geckodriver')
    #servico = Service(webdriver_path)
    

    #configuração do  proxy
    proxy_username = os.getenv('PROXY_USERNAME')
    proxy_password = os.getenv('PROXY_PASSWORD')
    proxy_ip = os.getenv('PROXY_IP')
    proxy_port = os.getenv('PROXY_PORT')

    if proxy_username and proxy_password and proxy_ip and proxy_port:
        options = {
            'proxy': {
                'http': f'http://{proxy_username}:{proxy_password}@{proxy_ip}:{proxy_port}',
                'https': f'http://{proxy_username}:{proxy_password}@{proxy_ip}:{proxy_port}',
                'no_proxy': 'localhost,127.0.0.1,dev_server:8080'
            }
        }
        browser = webdriver.Firefox(service=servico, seleniumwire_options=options, options=firefox_options)
    else:
        browser = webdriver.Firefox(service=servico, options=firefox_options)
    
    return browser

# Usar o navegador
browser = create_browser()
