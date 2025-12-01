from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILENAME = "mercado.db"
DB_PATH = os.path.abspath(os.path.join(BASE_DIR, '..', 'recursos', DB_FILENAME))
DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

_session = None

def inicializar_banco(Base):
    Base.metadata.create_all(bind=engine)

def obter_sessao():
    global _session
    if _session is None:
        _session = SessionLocal()
    return _session

def fechar_sessao():
    global _session
    if _session is not None:
        _session.close()
        _session = None
