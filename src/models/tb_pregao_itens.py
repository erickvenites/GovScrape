from sqlalchemy import Column, Float, ForeignKey, Integer, String
from src.models import Base
from sqlalchemy.orm import relationship

#Criação da tabela tb_pregao_itens
class AuctionItems(Base):
    __tablename__ = "tb_pregao_itens"
    id = Column(Integer, primary_key=True, autoincrement=True)
    pregao = Column(Integer, ForeignKey('tb_pregao.id'), nullable=False)
    sequencial = Column(Integer, nullable=False)
    tipo = Column(String)
    descricao = Column(String)
    descricao_detalhada = Column(String)
    quantidade_total = Column(Float)
    url_item = Column(String)

    pregao_item= relationship('UgAuctions', back_populates='auction_items')


#    def __init__(self,pregao,sequencial,tipo,descricao,descricao_detalhada,quantidade_total,url_item):
#        self.pregao=pregao
#        self.sequencial=sequencial
#        self.tipo=tipo
#        self.descricao=descricao
#        self.descricao_detalhada=descricao_detalhada
#        self.quantidade_total=quantidade_total
#        self.url_item=url_item
        
    def to_dict(self):
        return {
            'id': self.id,
            'ug_pregao_id': self.pregao,
            'sequencial': self.sequencial,
            'tipo': self.tipo,
            'descricao': self.descricao,
            'descricao_detalhada': self.descricao_detalhada,
            'quantidade_total': self.quantidade_total,
            'url_item': self.url_item
        }