from src.config.logging import logger
from bs4 import BeautifulSoup
from src.models.tb_pregao_itens import AuctionItems
from sqlalchemy.orm import Session
from src.models.tb_pregao import UgAuctions
def process_table(html_content, ug_auction_id, engine):

    soup = BeautifulSoup(html_content, 'html.parser')

    table = soup.find(name='table')

    with Session(engine) as session:

        ug_auction = session.query(UgAuctions).filter_by(id=ug_auction_id).first()
        try:
            for row in table.find_all('tr'):
                cells = row.find_all('td')
                if cells:
                    number = cells[0].find('span').text.strip() if cells[0].find('span') else ''
                    item_type = cells[1].find('span').text.strip() if cells[1].find('span') else ''
                    description_span = cells[2].find('span', id=lambda x: x and x.startswith('textoDescricaoCompletaCompra'))
                    description = ''
                    description_detailed = ''
                    if description_span:
                        text_description = description_span.text.strip()
                        index_detailed_description = text_description.find('Descrição Detalhada:')
                        if index_detailed_description != -1:
                            description = text_description[:index_detailed_description].strip()
                            description_detailed = text_description[index_detailed_description + len('Descrição Detalhada:'):].strip()
                        else:
                            description = text_description
                    total_quantity = cells[3].find('span').text.strip() if cells[3].find('span') else ''
                    link = cells[4].find('a')['href'] if cells[4].find('a') else ''
                    
                    existing_data = session.query(AuctionItems).filter_by(url_item=link).first()

                    if existing_data:
                        logger.info(f"Os dados do pregão {ug_auction.numero_ano} da UG: {ug_auction.ug_nome} já existem no banco de dados.")
                    else:
                        # Criando o objeto AuctionItems com o ug_pregao_id definido
                        item = AuctionItems(
                            pregao=ug_auction_id, 
                            sequencial=number, 
                            tipo=item_type, 
                            descricao=description, 
                            descricao_detalhada=description_detailed, 
                            quantidade_total=total_quantity, 
                            url_item=link
                        )
                        session.add(item)
                        session.commit()
                        logger.info(f"Os dados do pregão {ug_auction.numero_ano} da UG: {ug_auction.ug_nome} Salvo com sucesso!")
                        
        except Exception as e:
            logger.error(f"Erro desconhecido ao processar tabela: {str(e)}")

