from dados.conexao import obter_sessao
from dados.modelos import Compra, Item
from datetime import datetime

def criar_compra(id_cliente):
    session = obter_sessao()
    compra = Compra(id_cliente=id_cliente, data_hora=datetime.now())
    session.add(compra)
    session.flush()
    session.refresh(compra)
    session.commit()
    return compra.id

def adicionar_item_compra(id_compra, id_produto, quantidade, preco):
    session = obter_sessao()
    item = Item(id_compra=id_compra, id_produto=id_produto, quantidade=quantidade, preco=preco)
    session.add(item)
    session.commit()
    return item.id

def obter_compra_por_id(id_compra):
    session = obter_sessao()
    return session.query(Compra).filter(Compra.id == id_compra).first()

def obter_compras_por_cliente(id_cliente):
    session = obter_sessao()
    return session.query(Compra).filter(Compra.id_cliente == id_cliente).order_by(Compra.data_hora.desc()).all()

def obter_itens_compra(id_compra):
    session = obter_sessao()
    return session.query(Item).filter(Item.id_compra == id_compra).all()

def obter_total_compra(id_compra):
    itens = obter_itens_compra(id_compra)
    return sum(item.total for item in itens)
