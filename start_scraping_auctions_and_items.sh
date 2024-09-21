#!/bin/bash

# Obter data e hora atual
current_date=$(date +"%d-%m-%y-%Hh%Mm")

# Nome base do arquivo de log
log_file_base="/home/user/GovScrape/logs/scraping-pregao-comprasnet-${current_date}"

# Extensão do arquivo de log
log_file_extension=".log"

# Caminho completo para o arquivo de log
log_file_path="${log_file_base}${log_file_extension}"

# Importando variáveis de ambiente
set -a
source /home/user/Documentos/Projetos/GovScrape/.env
set +a

# Ativar o ambiente virtual
source /home/user/Documentos/Projetos/GovScrape/.venv/bin/activate

# Definir PYTHONPATH para incluir o diretório do projeto
export PYTHONPATH="/home/user/GovScrape"

# Execute a função schedule_get_auction_and_items e redirecione a saída para o arquivo de log
python3 -c "from src import start_scraping_auction_and_items; start_scraping_auction_and_items()" > "${log_file_path}" 2>&1


