from dados.repositorio_produto import obter_produto_por_id

def solicitar_id_cliente():
    while True:
        try:
            raw = input("Entre com o ID do cliente: ").strip()
            return int(raw)
        except ValueError:
            print('ID inválido. Digite um número.')
        except KeyboardInterrupt:
            raise

def solicitar_id_produto_e_quantidade():
    try:
        raw = input("Digite id do produto (ou 'fim' para encerrar): ").strip()
        if raw.lower() == 'fim':
            return None
        try:
            pid = int(raw)
        except ValueError:
            print('ID inválido.')
            return solicitar_id_produto_e_quantidade()
        produto = obter_produto_por_id(pid)
        if not produto:
            print('Produto não encontrado.')
            return solicitar_id_produto_e_quantidade()
        q = input(f"Quantidade para {produto.nome} (disponível {produto.quantidade}): ").strip()
        try:
            qn = int(q)
        except ValueError:
            print('Quantidade inválida.')
            return solicitar_id_produto_e_quantidade()
        return {'id': produto.id, 'nome': produto.nome, 'quantidade': qn, 'preco': produto.preco}
    except KeyboardInterrupt:
        raise

def exibir_nota_fiscal(df_grouped, cliente=None):
    print('\n--- NOTA FISCAL ---')
    if cliente:
        print(f'Cliente: {cliente.nome} (ID: {cliente.id})')
    print()
    print(df_grouped[['nome','quantidade','preco','total']].to_string(index=False))
    total_geral = df_grouped['total'].sum()
    print(f'\nTotal: R$ {total_geral:.2f}')

def mensagem_cliente_nao_encontrado():
    print('Cliente não cadastrado. Será cadastrado automaticamente.')
