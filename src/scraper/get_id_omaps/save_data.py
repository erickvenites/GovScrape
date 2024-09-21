from src.config.logging import logger
from selenium.webdriver.support import expected_conditions as EC
from src.models.tb_om_comprasnet import IdOms
from .extract_date_url import extract_url_parameters, extract_searched_url
from src.scraper.arraylist import data
from src.config.create_browser import browser
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from sqlalchemy.orm import Session

def save_data(engine):
    browser.get('https://contratos.sistema.gov.br/transparencia/compras?modalidade_id=76&modalidade_id_text=05+-+Preg%C3%A3o&lei=LEI14133&lei_text=LEI14133')

    # Esperando a página carregar por completo
    WebDriverWait(browser, 20).until(
        EC.presence_of_element_located((By.XPATH, r'/html/body/div[2]/main/div/div/div/div/div[2]/div/div/nav/div/ul/li[1]/a'))
    )

    search_numbers = [number for number in data if "7" + number]

    try:
        with Session(engine) as session:
            for search_number in search_numbers:
                new_url = extract_searched_url(search_number)

                if new_url:
                    unidade_origem_id, unidade_origem_id_text = extract_url_parameters(new_url)

                    if unidade_origem_id and unidade_origem_id_text:
                        number_unidade_origem_id_text = unidade_origem_id_text[1:6]

                        existing_record = session.query(IdOms).filter_by(ug=number_unidade_origem_id_text).first()

                        if existing_record:
                            logger.info(f"A UG {number_unidade_origem_id_text} já existe no banco de dados")
                        else:
                            id_record = IdOms(comprasnet=unidade_origem_id, ug=number_unidade_origem_id_text)
                            session.add(id_record)
                            session.commit()
                            logger.info(f"Os dados foram salvos com sucesso: {unidade_origem_id}, {number_unidade_origem_id_text}")

    except Exception as e:
        logger.error(f"Erro inesperado ao salvar: {search_number}: {str(e)}")
        return 500
    finally:
        if session:
            session.close()
