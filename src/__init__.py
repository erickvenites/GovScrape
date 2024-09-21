import os

from dotenv import load_dotenv
from src.models import Base
from src.config.database import config_db
from src.scraper import run_scraping_auction_ug_and_items, run_scraping_id_ug
from src.config.logging import logger
from src.config.send_email import enviar_email, get_latest_log_file

load_dotenv()

#Envio de email para os emails definidos no .env
def send_log_email(subject, message):

    log_dir = 'logs'
    latest_log_file = get_latest_log_file(log_dir)

    EMAIL_RECIPIENTS=os.getenv("EMAIL_RECIPIENTS","")
    if EMAIL_RECIPIENTS:
        recipients=EMAIL_RECIPIENTS.split(",")

    recipients=[EMAIL_RECIPIENTS]
    
    if latest_log_file:
        enviar_email(subject, message, recipients, latest_log_file)
        
    else:
        enviar_email(subject, message + "\nNo log files found.", recipients)

#Iniciando o scraping das id das ug
def start_scraping_id_ug():
    try:
        engine, db_session = config_db()

        # Associar a sessão ao Base
        Base.query = db_session.query_property()
            
        # Criação de todas as tabelas
        Base.metadata.create_all(bind=engine)
        logger.info("Iniciando a raspagem de id das UGs, aguarde...")

        run_scraping_id_ug(engine)
        
        # Enviar email de sucesso com o último log
        send_log_email("Sucesso no Web Scraping de UG", "O web scraping de UG foi realizado com sucesso.")
    except Exception as e:
        # Registra o erro em um log ou outro método de registro de erros
        logger.error(f"Erro ao iniciar a raspagem das UG: {str(e)}")
        
        # Enviar email de erro com o último log
        send_log_email("Erro no Web Scraping de UG", f"Ocorreu um erro durante o web scraping de UG: {str(e)}")



def start_scraping_auction_and_items():
    try:
        engine, db_session = config_db()

        # Associar a sessão ao Base
        Base.query = db_session.query_property()
            
        # Criação de todas as tabelas
        Base.metadata.create_all(bind=engine)

        logger.info("Iniciando a raspagem de pregões das UGs, aguarde...")

        run_scraping_auction_ug_and_items(engine)
        
        # Enviar email de sucesso com o último log
        send_log_email("Sucesso no Web Scraping de Pregões", "O web scraping de pregões foi realizado com sucesso.")

    except Exception as e:
        # Registra o erro em um log ou outro método de registro de erros
        logger.error(f"Erro ao iniciar a raspagem de pregões: {str(e)}")
        
        # Enviar email de erro com o último log
        send_log_email("Erro no Web Scraping de Pregões", f"Ocorreu um erro durante o web scraping de pregões: {str(e)}")
