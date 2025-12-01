import pandas as pd
from dados.repositorio_cliente import obter_cliente_por_id, salvar_cliente
from dados.repositorio_produto import decrementar_estoque
from dados.repositorio_compra import criar_compra, adicionar_item_compra
from visualizacoes.interface_console import solicitar_id_cliente, solicitar_id_produto_e_quantidade, exibir_nota_fiscal

def processar_atendimento_loop():
    while True:
        try:
            abrir = input("Deseja iniciar um atendimento? [s/n]: ").strip().lower()
            if abrir != 's':
                break
        except KeyboardInterrupt:
            print('\n\nOperação cancelada pelo usuário.')
            break
        
        try:
            id_cliente = solicitar_id_cliente()
            cliente = obter_cliente_por_id(int(id_cliente))
            if not cliente:
                novo_id = salvar_cliente()
                id_cliente = novo_id
                print(f'Cliente cadastrado com id {novo_id}')
                cliente = obter_cliente_por_id(novo_id)
            else:
                id_cliente = int(id_cliente)

            id_compra = criar_compra(id_cliente)
            print(f'Compra {id_compra} iniciada.')

            carrinho = []
            while True:
                try:
                    item = solicitar_id_produto_e_quantidade()
                    if item is None:
                        break
                    carrinho.append(item)
                except KeyboardInterrupt:
                    print('\n\nOperação cancelada pelo usuário.')
                    break

            if not carrinho:
                print('Atendimento cancelado (nenhum item).')
                continue

            df_carrinho = pd.DataFrame(carrinho)
            df_agrupado = df_carrinho.groupby(['id','nome','preco'], as_index=False).agg({'quantidade':'sum'})
            df_agrupado['total'] = df_agrupado['quantidade'] * df_agrupado['preco']

            exibir_nota_fiscal(df_agrupado, cliente)

            for _, linha in df_agrupado.iterrows():
                id_produto = int(linha['id'])
                quantidade = int(linha['quantidade'])
                preco = float(linha['preco'])
                adicionar_item_compra(id_compra, id_produto, quantidade, preco)
                decrementar_estoque(id_produto, quantidade)

            print(f'Compra {id_compra} registrada. Estoque atualizado e atendimento finalizado.')
        except KeyboardInterrupt:
            print('\n\nOperação cancelada pelo usuário.')
            break
        except Exception as e:
            print(f'\nErro durante o atendimento: {e}')
            continue
