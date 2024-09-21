import time
import json
from src.config.logging import logger
from src.config.create_browser import browser
from src.models.tb_om_comprasnet import IdOms
from .process_table import process_table
from selenium.webdriver.common.by import By
from sqlalchemy.orm import Session
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



def get_auction_ug(engine):
    try:
        with Session(engine) as session:
            # Recuperar os dados da tabela id_oms
            oms_data = session.query(IdOms).all()

            # Iterar sobre os dados da tabela id_oms
            for om_data in oms_data:
                ug = om_data.ug
                id_om_comprasnet = om_data.comprasnet
                logger.info(f'Procurando pregão da ug {ug}')

                if not ug or not id_om_comprasnet:
                    logger.error("Os parâmetros ug e id_om_comprasnet são obrigatórios")
                    return 400

                # Construir o URL com os valores de uasg e id_uasg
                url = f'https://contratos.sistema.gov.br/transparencia/compras?lei=LEI14133&lei_text=LEI14133&modalidade_id=76&modalidade_id_text=05+-+Preg%C3%A3o&unidade_origem_id={id_om_comprasnet}&unidade_origem_id_text={"7"+ug}'

                # Fazer a solicitação e processar os dados
                browser.get(url)
                
                # Espera explícita para a lista de opções ser clicável
                process_data = (By.XPATH, r'//*[@id="crudTable_length"]/label/select/option[5]')
                WebDriverWait(browser, 20).until(EC.element_to_be_clickable(process_data)).click()
                #time.sleep(3)
                
                #Garantino que as linhas da tabela carregaram antes de pegar os dados
                WebDriverWait(browser,20).until(
                    EC.visibility_of_all_elements_located((By.XPATH,'/html/body/div[2]/main/div/div/div/div/div[2]/div/div/div[2]/div/div[2]/div/table/tbody/tr')))
                
                # Espera explícita para o elemento da tabela estar presente no DOM
                table_element = (By.XPATH, '//*[@id="crudTable"]')
                element = WebDriverWait(browser, 20).until(EC.presence_of_element_located(table_element))

                
                html_content = element.get_attribute('outerHTML')
                #time.sleep(3)
                
                process_table(html_content, engine)
                
    except Exception as e:
        logger.error(f"Erro ao processar a tabela: {str(e)}")
        return 500
            
    finally:
        session.close()