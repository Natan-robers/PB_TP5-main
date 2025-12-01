import pandas as pd
from utilidades.arquivos import caminho_clientes_json
from dados.repositorio_cliente import buscar_cliente_por_nome, salvar_cliente

def carregar_clientes_iniciais():
    path = caminho_clientes_json()
    try:
        df = pd.read_json(path)
    except Exception:
        df = pd.DataFrame([{"nome":"Cliente 1"},{"nome":"Cliente 2"},{"nome":"Cliente 3"}])
        df.to_json(path, orient='records', force_ascii=False)
    for _, row in df.iterrows():
        if not buscar_cliente_por_nome(row['nome']):
            salvar_cliente(row['nome'])
    print("Clientes iniciais carregados.")
