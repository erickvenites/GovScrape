#!/bin/bash

# Obter data e hora atual
current_date=$(date +"%d-%m-%y-%Hh%Mm")

# Nome base do arquivo de log
log_file_base="/home/user/GovScrape/NavyAuctionCollector/logs/scraping-ug-comprasnet-${current_date}"

# Extensão do arquivo de log
log_file_extension=".log"

# Caminho completo para o arquivo de log
log_file_path="${log_file_base}${log_file_extension}"
# Importando variáveis de ambiente
set -a
source /home/user/GovScrape/NavyAuctionCollector/.env
set +a

# Ativar o ambiente virtual
source /home/user/GovScrape/NavyAuctionCollector/.venv/bin/activate

# Definir PYTHONPATH para incluir o diretório do projeto
export PYTHONPATH="/home/user/GovScrape/NavyAuctionCollector"

# Execute a função init_get_id_ug
python3 -c "from src import start_scraping_id_ug; start_scraping_id_ug()"



