from dados.conexao import obter_sessao
from dados.modelos import Cliente

def obter_cliente_por_id(id_cliente):
    session = obter_sessao()
    return session.query(Cliente).filter(Cliente.id == id_cliente).first()

def buscar_cliente_por_nome(nome):
    session = obter_sessao()
    return session.query(Cliente).filter(Cliente.nome == nome).first()

def salvar_cliente(nome=None):
    session = obter_sessao()
    c = Cliente(nome=nome or "Cliente")
    session.add(c)
    session.flush()
    session.refresh(c)
    if nome is None or nome == "Cliente":
        c.nome = f"Cliente {c.id}"
    session.commit()
    return c.id

def listar_todos_clientes():
    session = obter_sessao()
    return session.query(Cliente).order_by(Cliente.nome).all()
