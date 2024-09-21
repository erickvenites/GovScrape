import os
import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime

# Cria o diretório 'logs' se não existir
log_directory = "logs"
os.makedirs(log_directory, exist_ok=True)

# Define o formato do nome do arquivo de log com data e hora
current_time = datetime.now().strftime("%d-%m-%y-%Hh%Mm")
log_filename = os.path.join(log_directory, f"scraping-pregao-comprasnet-{current_time}.log")

# Configura o logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Cria um TimedRotatingFileHandler que cria um novo arquivo de log diariamente
handler = TimedRotatingFileHandler(
    log_filename,
    when="D",  # Roda a cada dia
    interval=1,  # Intervalo de 1 dia
    backupCount=3,  # Mantém os últimos 3 arquivos de log
)

# Define o formato do log
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

# Adiciona o handler ao logger
logger.addHandler(handler)

# Adiciona um console handler para exibir os logs no console
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)