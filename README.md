# **GoVScrape**

## Web Scraping do Site de Contratações do Governo

Este projeto realiza um web scraping no site de contratações do governo para extrair informações de pregões da Marinha do Brasil.

### Descrição

Este script Python utiliza BeautifulSoup e Selenium para acessar o site de contratações do governo, navegar pelas páginas de resultados de pesquisa, e extrair dados relevantes sobre pregões. As informações coletadas são armazenadas em um banco de dados Postgresql

### Funcionalidades

- **Acesso automatizado**: Utiliza Selenium para simular interações de navegação como um usuário real.
- **Extração de dados**: Coleta dados como UG, descrição dos  itens, valor do contrato,quantidade total,numero e ano do pregão.
- **Armazenamento**: Salva os dados em banco de dados postgresql.

### Pré-requisitos

- Python 3.10.12
- Bibliotecas Python: BeautifulSoup, Selenium, sqlachemy, cronjob, psycopg2
- WebDriver: Recomenda-se o uso do GeckoDriver para Firefox. Certifique-se de baixar e configurar o WebDriver compatível com a versão do seu navegador.

### Instalação

1. instale o ambiente virtual
```bash
    python3 -m venv .venv
```
2. Execute o venv
```bash
 $. /.env/bin/activate
```
3. Instale as dependências do projeto
```bash
    pip install -r requirements.txt
```

4. Instale o geckodriver (verifique a versão do seu firefox)
```bash
$ wget https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz

$ tar -xvzf geckodriver-v0.30.0-linux64.tar.gz

$ sudo mv geckodriver /usr/local/bin/

$ export HTTP_PROXY=http://seu-usuario:sua-senha@seu-proxy:porta
$ export HTTPS_PROXY=http://seu-usuario:sua-senha@seu-proxy:porta

$ geckodriver --version

```
### Configurações

1. Crie o diretório `.env`:
```bash
    nano .env
```

1. Configure as variáveis de ambiente para o postgres, para os emails e para o proxy, se necessário, no arquivo `.env`:

```python

    USER_EMAIL="email_pgadmin"
    USER_PASSWORD="sua_senha_pgadmin"

    POSTGRES_PASSWORD="senha_do_postgres"
    POSTGRES_DB="seu_banco_de_dados"


    HTTP_PROXY=http://seu-proxy:porta
    HTTPS_PROXY=http://seu-proxy:porta

    PROXY_USERNAME = usuario
    PROXY_PASSWORD = senha_de_acesso
    PROXY_IP= ip
    PROXY_PORT = porta



    smtp_server=server_do_email
    email_from=email_que_envia
    senha=senha_do_email_que_envia
    porta=porta

    #### Emails que receberam a resposta do scraping
    EMAIL_RECIPIENTS=exemplo@gmail.com,exemplo2@marinha.mil.br

    DB_URI=user:senha@host:porta/db 
```
    #### OBS.: não esqueça de escapar o caracter especial EX.: @=%40


### Uso

1. Defina essas configurações no crontab -e

```bash
#### Executar o script todo dia 2 de cada mês às 00:00 e registrar a saída em um arquivo de log
0 0 2 * * /caminho/do/codigo/GovScrape/start_scraping_auctions_and_items.sh > /caminho/do/codigo/GovScrape/logs/cronjob_auction.log 2>&1

#### Executar o script a cada dois meses, no primeiro dia do mês às 00:00 e registrar a saída em um arquivo de log
0 0 1 */2 * /caminho/do/codigo/GovScrape/start_scraping_uasg_IDs.sh > /caminho/do/codigo/GovScrape/cronjob_id_ug.log 2>&1
```
Isso fara com que o web_scraping esteja agendado

2. modifique o arquivo `start_scraping_auction_and_items.sh` para executar de acordo com o caminho relativo ao projeto


3. Faça o mesmo para `start_scraping_UG_IDs.sh`

4. Dê permissão de execução aos arquivos:
```bash
$ chmod +x /caminho/do/codigo/NavyAuctionCollector/start_scraping_auction_and_items.sh
$ chmod +x /caminho/do/codigo/NavyAuctionCollector/start_scraping_UG_IDs.sh
```
5. Não esqueça de colocar as uasg que deseja pegar os dados em `src/scraper/arraylist.py`
### Contribuições

Contribuições são bem-vindas!

### Notas

- **Respeito aos termos de uso**: Verifique os termos de uso do site de contratações do governo para garantir conformidade legal ao realizar web scraping.
- **Manutenção**: Este projeto pode necessitar de atualizações periódicas conforme o site alvo muda sua estrutura ou políticas.
