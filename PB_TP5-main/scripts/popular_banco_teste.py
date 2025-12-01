from dados.conexao import inicializar_banco, obter_sessao, fechar_sessao
from dados.modelos import Base, Cliente, Fornecedor, Compra, Item
from dados.repositorio_cliente import salvar_cliente, obter_cliente_por_id
from dados.repositorio_fornecedor import salvar_fornecedor, associar_produto_fornecedor
from dados.repositorio_produto import listar_todos_produtos, obter_produto_por_id
from dados.repositorio_compra import criar_compra, adicionar_item_compra
from datetime import datetime, timedelta

def popular_banco_teste():
    try:
        inicializar_banco(Base)
        session = obter_sessao()
        
        print("=" * 70)
        print("POPULANDO BANCO DE DADOS COM DADOS DE TESTE")
        print("=" * 70)
        
        produtos = listar_todos_produtos()
        if not produtos:
            print("\nAVISO: Nenhum produto encontrado no banco!")
            print("Execute primeiro o app.py para carregar produtos via web scraping.")
            return
        
        print(f"\nProdutos encontrados no banco: {len(produtos)}")
        print("Primeiros 5 produtos:", [f"ID:{p.id}" for p in produtos[:5]])
        
        print("\n" + "-" * 70)
        print("1. CRIANDO CLIENTES DE TESTE")
        print("-" * 70)
        
        id_cliente1 = salvar_cliente("cliente_teste1")
        id_cliente2 = salvar_cliente("cliente_teste2")
        id_cliente3 = salvar_cliente("cliente_teste3")
        id_cliente4 = salvar_cliente("cliente_teste4")
        id_cliente5 = salvar_cliente("cliente_teste5")
        
        print(f"  - cliente_teste1 (ID: {id_cliente1})")
        print(f"  - cliente_teste2 (ID: {id_cliente2})")
        print(f"  - cliente_teste3 (ID: {id_cliente3})")
        print(f"  - cliente_teste4 (ID: {id_cliente4})")
        print(f"  - cliente_teste5 (ID: {id_cliente5})")
        
        print("\n" + "-" * 70)
        print("2. CRIANDO FORNECEDORES DE TESTE")
        print("-" * 70)
        
        id_fornecedor1 = salvar_fornecedor("fornecedor_teste1")
        id_fornecedor2 = salvar_fornecedor("fornecedor_teste2")
        id_fornecedor3 = salvar_fornecedor("fornecedor_teste3")
        id_fornecedor4 = salvar_fornecedor("fornecedor_teste4")
        
        print(f"  - fornecedor_teste1 (ID: {id_fornecedor1})")
        print(f"  - fornecedor_teste2 (ID: {id_fornecedor2})")
        print(f"  - fornecedor_teste3 (ID: {id_fornecedor3})")
        print(f"  - fornecedor_teste4 (ID: {id_fornecedor4}) - SEM PRODUTOS")
        
        print("\n" + "-" * 70)
        print("3. CRIANDO COMPRAS PARA DEMONSTRAR FUNCIONALIDADES")
        print("-" * 70)
        
        produtos_ids = [p.id for p in produtos[:10]]
        
        id_compra1 = criar_compra(id_cliente1)
        adicionar_item_compra(id_compra1, produtos_ids[0], 5, produtos[0].preco)
        adicionar_item_compra(id_compra1, produtos_ids[1], 3, produtos[1].preco)
        adicionar_item_compra(id_compra1, produtos_ids[2], 2, produtos[2].preco)
        print(f"  - Compra 1 para cliente_teste1 (ID: {id_compra1}) - 3 itens")
        
        id_compra2 = criar_compra(id_cliente1)
        adicionar_item_compra(id_compra2, produtos_ids[3], 10, produtos[3].preco)
        adicionar_item_compra(id_compra2, produtos_ids[4], 8, produtos[4].preco)
        print(f"  - Compra 2 para cliente_teste1 (ID: {id_compra2}) - 2 itens")
        
        id_compra3 = criar_compra(id_cliente1)
        adicionar_item_compra(id_compra3, produtos_ids[5], 15, produtos[5].preco)
        adicionar_item_compra(id_compra3, produtos_ids[6], 12, produtos[6].preco)
        adicionar_item_compra(id_compra3, produtos_ids[0], 4, produtos[0].preco)
        print(f"  - Compra 3 para cliente_teste1 (ID: {id_compra3}) - 3 itens")
        
        id_compra4 = criar_compra(id_cliente2)
        adicionar_item_compra(id_compra4, produtos_ids[0], 1, produtos[0].preco)
        print(f"  - Compra 4 para cliente_teste2 (ID: {id_compra4}) - 1 item (GASTOU MENOS)")
        
        id_compra5 = criar_compra(id_cliente3)
        adicionar_item_compra(id_compra5, produtos_ids[1], 1, produtos[1].preco)
        print(f"  - Compra 5 para cliente_teste3 (ID: {id_compra5}) - 1 item")
        
        print("\n  RESUMO:")
        print(f"    - cliente_teste1: 3 compras (MAIS COMPRAS E MAIS GASTOS)")
        print(f"    - cliente_teste2: 1 compra pequena (GASTOU MENOS)")
        print(f"    - cliente_teste3: 1 compra")
        print(f"    - cliente_teste4: 0 compras (CLIENTE SEM COMPRAS)")
        print(f"    - cliente_teste5: 0 compras (CLIENTE SEM COMPRAS)")
        
        print("\n" + "-" * 70)
        print("4. ASSOCIANDO PRODUTOS A FORNECEDORES")
        print("-" * 70)
        
        associar_produto_fornecedor(produtos_ids[0], id_fornecedor1)
        associar_produto_fornecedor(produtos_ids[1], id_fornecedor1)
        associar_produto_fornecedor(produtos_ids[2], id_fornecedor1)
        print(f"  - Produtos {produtos_ids[0]}, {produtos_ids[1]}, {produtos_ids[2]} -> fornecedor_teste1")
        
        associar_produto_fornecedor(produtos_ids[3], id_fornecedor2)
        associar_produto_fornecedor(produtos_ids[4], id_fornecedor2)
        print(f"  - Produtos {produtos_ids[3]}, {produtos_ids[4]} -> fornecedor_teste2")
        
        associar_produto_fornecedor(produtos_ids[5], id_fornecedor3)
        associar_produto_fornecedor(produtos_ids[6], id_fornecedor3)
        associar_produto_fornecedor(produtos_ids[0], id_fornecedor3)
        print(f"  - Produtos {produtos_ids[5]}, {produtos_ids[6]}, {produtos_ids[0]} -> fornecedor_teste3")
        
        print(f"  - fornecedor_teste4: SEM PRODUTOS ASSOCIADOS")
        
        print("\n" + "-" * 70)
        print("5. RESUMO FINAL")
        print("-" * 70)
        print("Clientes criados:")
        print("  - cliente_teste1: Cliente que mais compra e mais gasta")
        print("  - cliente_teste2: Cliente que gastou menos")
        print("  - cliente_teste3: Cliente com 1 compra")
        print("  - cliente_teste4: Cliente sem compras")
        print("  - cliente_teste5: Cliente sem compras")
        print("\nFornecedores criados:")
        print("  - fornecedor_teste1: Com 3 produtos")
        print("  - fornecedor_teste2: Com 2 produtos")
        print("  - fornecedor_teste3: Com 3 produtos (1 produto compartilhado)")
        print("  - fornecedor_teste4: SEM produtos")
        print("\n" + "=" * 70)
        print("BANCO POPULADO COM SUCESSO!")
        print("=" * 70)
        print("\nAgora voce pode testar o SIG com:")
        print("  python sig.py")
        print("\nFuncionalidades para testar:")
        print("  - Clientes com compras")
        print("  - Clientes sem compras")
        print("  - Clientes que mais compram")
        print("  - Clientes que mais gastam")
        print("  - Produtos mais vendidos")
        print("  - Produtos menos vendidos")
        print("  - Fornecedores de um produto")
        
    except Exception as e:
        print(f"\nERRO ao popular banco: {e}")
        import traceback
        traceback.print_exc()
    finally:
        fechar_sessao()

if __name__ == '__main__':
    popular_banco_teste()

