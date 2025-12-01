from dados.conexao import obter_sessao
from dados.modelos import Fornecedor, Produto, produto_fornecedor

def obter_fornecedor_por_id(id_fornecedor):
    session = obter_sessao()
    return session.query(Fornecedor).filter(Fornecedor.id == id_fornecedor).first()

def obter_fornecedor_por_nome(nome):
    session = obter_sessao()
    return session.query(Fornecedor).filter(Fornecedor.nome == nome).first()

def salvar_fornecedor(nome):
    session = obter_sessao()
    fornecedor = Fornecedor(nome=nome)
    session.add(fornecedor)
    session.flush()
    session.refresh(fornecedor)
    session.commit()
    return fornecedor.id

def listar_todos_fornecedores():
    session = obter_sessao()
    return session.query(Fornecedor).order_by(Fornecedor.nome).all()

def associar_produto_fornecedor(id_produto, id_fornecedor):
    session = obter_sessao()
    existe = session.query(produto_fornecedor).filter(
        produto_fornecedor.c.id_produto == id_produto,
        produto_fornecedor.c.id_fornecedor == id_fornecedor
    ).first()
    
    if not existe:
        ins = produto_fornecedor.insert().values(id_produto=id_produto, id_fornecedor=id_fornecedor)
        session.execute(ins)
        session.commit()

def obter_fornecedores_produto(id_produto):
    session = obter_sessao()
    produto = session.query(Produto).filter(Produto.id == id_produto).first()
    if produto:
        return produto.fornecedores
    return []

def remover_associacao_produto_fornecedor(id_produto, id_fornecedor):
    session = obter_sessao()
    delete = produto_fornecedor.delete().where(
        produto_fornecedor.c.id_produto == id_produto,
        produto_fornecedor.c.id_fornecedor == id_fornecedor
    )
    session.execute(delete)
    session.commit()
