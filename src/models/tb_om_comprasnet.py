from sqlalchemy import Column, Integer, String
from src.models import Base

#Criação da tablea tb_om_comprasnet
class IdOms(Base):
    __tablename__ = "tb_om_comprasnet"
    id = Column(Integer, primary_key=True)
    comprasnet = Column(String(10), nullable=False)
    ug = Column(String(10), nullable=False, unique=True)
    
    def __init__(self, comprasnet, ug):
        self.comprasnet = comprasnet
        self.ug = ug
        
    def to_dict(self):
        return {
            'id': self.id,
            'id_om': self.comprasnet,
            'uasg': self.ug
        }


    