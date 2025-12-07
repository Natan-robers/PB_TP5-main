from dados.repositorio_produto import obter_produto_por_id
from tabulate import tabulate

def solicitar_id_cliente():
    while True:
        try:
            raw = input("Entre com o ID do cliente: ").strip()
            return int(raw)
        except ValueError:
            print('ID inválido. Digite um número.')
        except KeyboardInterrupt:
            raise

def solicitar_id_produto():
    raw = input("Digite id do produto (ou 'fim' para encerrar'): ").strip()
    if raw.lower() == 'fim':
        return None
    
    try:
        pid = int(raw)
    except ValueError:
        print("ID inválido.")
        return solicitar_id_produto()

    produto = obter_produto_por_id(pid)

    if not produto:
        print("Produto não encontrado.")
        return solicitar_id_produto()

    return produto


def solicitar_quantidade(produto, estoque_temp):
    if produto.id not in estoque_temp:
        estoque_temp[produto.id] = produto.quantidade

    estoque_atual = estoque_temp[produto.id]

    if estoque_atual == 0:
        print(f" Produto '{produto.nome}' está sem estoque!")
        return 0 

    q = input(f"Quantidade para {produto.nome} (disponível {estoque_atual}): ").strip()

    try:
        qn = int(q)
    except ValueError:
        print("Quantidade inválida.")
        return solicitar_quantidade(produto, estoque_temp)

    if qn > estoque_atual:
        print("Quantidade indisponível no estoque.")
        return solicitar_quantidade(produto, estoque_temp)

    estoque_temp[produto.id] -= qn
    return qn


def solicitar_id_produto_e_quantidade(estoque_temp):
    while True:  
        produto = solicitar_id_produto()
        if produto is None:
            return None  

        quantidade = solicitar_quantidade(produto, estoque_temp)

        if quantidade == 0:
            continue  

        return {
            'id': produto.id,
            'nome': produto.nome,
            'quantidade': quantidade,
            'preco': produto.preco
        }





def exibir_nota_fiscal(df_grouped, cliente=None):
    print('\n--- NOTA FISCAL ---')

    if cliente:
        print(f'Cliente: {cliente.nome} (ID: {cliente.id})')

    print()

    colunas = ['nome', 'quantidade', 'preco', 'total']
    tabela = df_grouped[colunas]

    print(tabulate(
        tabela,
        headers=colunas,
        tablefmt="fancy_grid",   
        floatfmt=".2f",          
        showindex=False
    ))

    
    total_geral = df_grouped['total'].sum()
    print(f'\nTotal: R$ {total_geral:.2f}')


def mensagem_cliente_nao_encontrado():
    print('Cliente não cadastrado. Será cadastrado automaticamente.')
