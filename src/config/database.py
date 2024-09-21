import os
from urllib.parse import quote_plus
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

load_dotenv()

# Função para configurar o banco de dados
def config_db():
    #Importando variáveis de ambiente
    DB_URI =os.getenv("DB_URI")

    connection_string = (
        f"postgresql+psycopg2://{DB_URI}"
    )

    # Criação do engine do SQLAlchemy
    engine = create_engine(connection_string, echo=False)

    # Criação da sessão
    db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
    

    return engine,db_session