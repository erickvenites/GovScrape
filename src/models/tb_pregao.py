from src.models import Base
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

#Criação da tabela tb_pregao
class UgAuctions(Base):
    __tablename__ = 'tb_pregao'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ug = Column(String, ForeignKey('tb_om_comprasnet.ug'), nullable=False)
    ug_nome = Column(String, nullable=False)
    tipo_compra = Column(String)
    modalidade = Column(String)
    numero_ano = Column(String)
    url = Column(String)

    auction_items = relationship('AuctionItems', back_populates='pregao_item', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'ug': self.ug,
            'ug_nome': self.ug_nome,
            'tipo_compra': self.tipo_compra,
            'modalidade': self.modalidade,
            'numero_ano': self.numero_ano,
            'url': self.url,
        }