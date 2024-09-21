import json
from bs4 import BeautifulSoup
from src.models.tb_om_comprasnet import IdOms
from src.models.tb_pregao import UgAuctions
from sqlalchemy.orm import Session
from src.config.logging import logger

def process_table(html_content, engine):
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find(name='table')
#Processa a tabela e pega todos os itens da tabela
    if table:
        for row in table.find_all('tr'):
            row_data = []
            #Percorrendo todas as celulas da tabela 
            for cell in row.find_all('td'):
                a_tags = cell.find_all('a')
                if cell.text.strip():
                    text = cell.text.strip()
                elif a_tags and len(a_tags) > 1:
                    text = a_tags[1]['href']
                elif a_tags:
                    text = None
                else:
                    text = ''
                row_data.append(text)

            try:
                # acessar os elementos da lista row_data
                id_usg = row_data[0]
                purchase_type = row_data[2]
                url = row_data[7]
                modality = row_data[3]
                number_year = row_data[4]

                # Separar a 1ª e 5ª posição de id_usg e o resto em ug_nome
                
                id_usg_part = id_usg[1:6]
                ug_name_part = id_usg[9:]
                
                with Session(engine) as session:
                    # Verificar se a ug existe na tabela id_oms
                    om_record = session.query(IdOms).filter_by(ug=id_usg_part).first()
                    if om_record:
                        # Criar uma instância de UgAuctions
                        bidding = UgAuctions(
                            ug=id_usg_part, 
                            ug_nome=ug_name_part, 
                            tipo_compra=purchase_type, 
                            modalidade=modality, 
                            numero_ano=number_year, 
                            url=url
                        )

                        data_record = session.query(UgAuctions).filter_by(url=url).first()
                        if data_record:
                            logger.info(f"O pregão {number_year} do(a) {ug_name_part} já existe no banco de dados")
                        else:
                            # Adicionar à sessão do banco de dados
                            session.add(bidding)
                            session.commit()
                            logger.info(f"Dados do pregão {number_year} do(a) {ug_name_part} salvos com sucesso")
                    else:
                        logger.error(f"Registro com UG {id_usg_part} não encontrado em id_oms")
            except IndexError:
                logger.error(f"A UG não possui pregões: {row_data}")
                continue
            except Exception as e:
                logger.error(f"Erro ao processar a linha: {str(e)}; Dados: {row_data}")
                continue
    else:
        logger.error("Tabela não encontrada no HTML fornecido.")
