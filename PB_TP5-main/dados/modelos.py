from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

produto_fornecedor = Table(
    'produto_fornecedor',
    Base.metadata,
    Column('id_produto', Integer, ForeignKey('produto.id'), primary_key=True),
    Column('id_fornecedor', Integer, ForeignKey('fornecedor.id'), primary_key=True)
)

class Cliente(Base):
    __tablename__ = 'cliente'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    compras = relationship("Compra", back_populates="cliente", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Cliente id={self.id} nome='{self.nome}'>"

class Produto(Base):
    __tablename__ = 'produto'
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    quantidade = Column(Integer, default=0)
    preco = Column(Float, default=0.0)
    itens = relationship("Item", back_populates="produto")
    fornecedores = relationship("Fornecedor", secondary=produto_fornecedor, back_populates="produtos")

    def __repr__(self):
        return f"<Produto id={self.id} nome='{self.nome}' qtd={self.quantidade} preco={self.preco}>"

class Fornecedor(Base):
    __tablename__ = 'fornecedor'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    produtos = relationship("Produto", secondary=produto_fornecedor, back_populates="fornecedores")

    def __repr__(self):
        return f"<Fornecedor id={self.id} nome='{self.nome}'>"

class Compra(Base):
    __tablename__ = 'compra'
    id = Column(Integer, primary_key=True, autoincrement=True)
    data_hora = Column(DateTime, default=datetime.now, nullable=False)
    id_cliente = Column(Integer, ForeignKey('cliente.id'), nullable=False)
    cliente = relationship("Cliente", back_populates="compras")
    itens = relationship("Item", back_populates="compra", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Compra id={self.id} cliente_id={self.id_cliente} data_hora={self.data_hora}>"

class Item(Base):
    __tablename__ = 'item'
    id = Column(Integer, primary_key=True, autoincrement=True)
    quantidade = Column(Integer, nullable=False)
    preco = Column(Float, nullable=False)
    id_compra = Column(Integer, ForeignKey('compra.id'), nullable=False)
    id_produto = Column(Integer, ForeignKey('produto.id'), nullable=False)
    compra = relationship("Compra", back_populates="itens")
    produto = relationship("Produto", back_populates="itens")

    @property
    def total(self):
        return self.quantidade * self.preco

    def __repr__(self):
        return f"<Item id={self.id} produto_id={self.id_produto} quantidade={self.quantidade} preco={self.preco}>"
