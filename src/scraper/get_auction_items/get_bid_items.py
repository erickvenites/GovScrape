from src.config.logging import logger
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from src.models.tb_pregao import UgAuctions
from .process_table import process_table
from src.config.create_browser import browser
from sqlalchemy.orm import Session


def get_bid_items(engine):
    with Session(engine) as session:
        ug_auctions_data = session.query(UgAuctions).all()
        try:
            for ug_auction_data in ug_auctions_data:
                ug_auctions_data_ref = ug_auction_data.url
                logger.info(f"Processando o pregão {ug_auction_data.numero_ano} do(a) {ug_auction_data.ug_nome}, Aguarde...")

                if not ug_auctions_data_ref:
                    logger.error("Referência inexistente")
                    return 400
            
                url_base = f'https://contratos.sistema.gov.br{ug_auctions_data_ref}'

                browser.get(url_base)
                
                # Espera explícita para que a lista de opções seja clicável
                WebDriverWait(browser, 30).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="crudTable_length"]/label/select/option[5]'))
                ).click()
                
                # Espera explícita para o indicador de processamento desaparecer
                WebDriverWait(browser, 30).until(
                    EC.invisibility_of_element_located((By.ID, 'crudTable_processing'))
                )
                
                # Clicar nos botões "btn-default"
                buttons = WebDriverWait(browser, 30).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "btn-default"))
                )

                for button in buttons:
                    button.click()
                
                # Espera explícita para o elemento da tabela estar presente no DOM
                WebDriverWait(browser, 30).until(
                    EC.presence_of_element_located((By.TAG_NAME, 'table'))
                )
                
                html_content = browser.page_source

                process_table(html_content, ug_auction_data.id, engine)
                
        except TimeoutException as te:
            logger.error(f"Tempo limite excedido ao carregar a página: {str(te)}")
            return 500
            
        except NoSuchElementException as nse:
            logger.error(f"Elemento não encontrado: {str(nse)}")
            return 500
            
        except Exception as e:
            logger.error(f"Erro desconhecido: {str(e)}")
            return 500
        
        finally:
            logger.info("Processo finalizado")
            session.close()
           # browser.quit()
            return 200
