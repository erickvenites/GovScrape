from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from .tb_om_comprasnet import IdOms
from .tb_pregao import UgAuctions
from .tb_pregao_itens import AuctionItems