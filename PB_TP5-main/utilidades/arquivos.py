import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def caminho_clientes_json():
    return os.path.abspath(os.path.join(BASE_DIR, '..', 'recursos', 'clientes.json'))

def caminho_produtos_csv():
    return os.path.abspath(os.path.join(BASE_DIR, '..', 'recursos', 'produtos.csv'))

def caminho_produtos_url():
    return 'https://pedrovncs.github.io/lindosprecos/produtos.html#'

def caminho_excel_fornecedores():
    return os.path.abspath(os.path.join(BASE_DIR, '..', 'recursos', 'fornecedores.xlsx'))
