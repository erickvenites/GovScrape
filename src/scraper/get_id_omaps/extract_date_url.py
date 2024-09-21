import time
from src.config.logging import logger
from urllib.parse import parse_qs, urlparse
from selenium.webdriver.common.by import By
from src.config.create_browser import browser
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def extract_url_parameters(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    unidade_origem_id = query_params.get('unidade_origem_id', [None])[0]
    unidade_origem_id_text = query_params.get('unidade_origem_id_text', [None])[0]
    return unidade_origem_id, unidade_origem_id_text

def extract_searched_url(search_number):
    try:
        initial_url = browser.current_url
    
        # Espera pelo botão de busca e clica nele
        search_button_locator = (By.XPATH, r'/html/body/div[2]/main/div/div/div/div/div[2]/div/div/nav/div/ul/li[1]/a')
        WebDriverWait(browser, timeout=20).until(
            EC.element_to_be_clickable(search_button_locator)
        ).click()


        # Espera pelo campo de busca, insere o número e espera pelos resultados
        search_field_locator = (By.XPATH, r'/html/body/div[2]/main/div/div/div/div/div[2]/div/div/nav/div/ul/li[1]/div/div/span[2]/span/span[1]/input')
        search_field = WebDriverWait(browser, timeout=20, poll_frequency=2).until(
            EC.visibility_of_element_located(search_field_locator)
        )
        search_field.clear()
        search_field.send_keys("7" + search_number)
        
        time.sleep(3)
        # Espera pelos resultados e clica no primeiro item
        result_locator = (By.XPATH, r'/html/body/div[2]/main/div/div/div/div/div[2]/div/div/nav/div/ul/li[1]/div/div/span[2]/span/span[2]/ul/li')
        result = WebDriverWait(browser, timeout=20, poll_frequency=2).until(
            EC.visibility_of_element_located(result_locator)
        )
        result.click()

        # Verifica se a URL mudou
        new_url = browser.current_url
        if new_url != initial_url:
            return new_url
        else:
            return None
    except Exception as e:
        logger.error(f"Um erro ocorreu ao procurar por: {search_number}: {str(e)}")
        return 500
