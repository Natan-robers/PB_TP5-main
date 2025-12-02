from dados.repositorio_produto import (
    listar_todos_produtos, obter_produto_por_id, salvar_ou_atualizar_produto,
    buscar_produtos_sem_estoque
)
from dados.repositorio_fornecedor import (
    listar_todos_fornecedores, obter_fornecedores_produto,
    associar_produto_fornecedor, remover_associacao_produto_fornecedor
)
from dados.modelos import Produto
from dados.conexao import obter_sessao
from dados.modelos import Item
from sqlalchemy import func
from tabulate import tabulate


def menu_produtos():
    while True:
        try:
            print("\n" + "-" * 50)
            print("MENU PRODUTOS")
            print("-" * 50)
            print("1. Consultar produtos")
            print("2. Cadastrar produto")
            print("3. Alterar produto")
            print("4. Excluir produto")
            print("5. Consultas especiais")
            print("0. Voltar")
            print("-" * 50)
            
            opcao = input("Escolha uma opção: ").strip()
            
            if opcao == '0':
                break
            elif opcao == '1':
                listar_produtos()
            elif opcao == '2':
                cadastrar_produto()
            elif opcao == '3':
                alterar_produto()
            elif opcao == '4':
                excluir_produto()
            elif opcao == '5':
                menu_consultas_produtos()
            else:
                print("\nOpção inválida.")
        except KeyboardInterrupt:
            print("\n\nOperação cancelada pelo usuário.")
            break
        except Exception as e:
            print(f"\nErro: {e}")


def listar_produtos():
    produtos = listar_todos_produtos()
    
    if not produtos:
        print("\nNenhum produto cadastrado.")
        return

    tabela = [[p.id, p.nome, p.quantidade, f"R$ {p.preco:.2f}"] for p in produtos]

    print("\nLISTA DE PRODUTOS\n")
    print(tabulate(
        tabela,
        headers=["ID", "Nome", "Quantidade", "Preço"],
        tablefmt="fancy_grid",
        stralign="left",
        numalign="right"
    ))
    print(f"\nTotal: {len(produtos)} produto(s)")


def cadastrar_produto():
    try:
        print("\n" + "-" * 50)
        print("CADASTRO DE PRODUTO")
        print("-" * 50)
        
        id_produto = int(input("ID do produto: ").strip())
        
        if obter_produto_por_id(id_produto):
            print(f"Produto com ID {id_produto} já existe.")
            return
        
        nome = input("Nome do produto: ").strip()
        if not nome:
            print("Nome é obrigatório.")
            return
        
        quantidade = int(input("Quantidade em estoque: ").strip() or "0")
        preco = float(input("Preço unitário: ").strip() or "0.0")
        
        produto = Produto(id=id_produto, nome=nome, quantidade=quantidade, preco=preco)
        salvar_ou_atualizar_produto(produto)
        
        print(f"\nProduto {id_produto} cadastrado com sucesso!")
        associar_fornecedores_produto(id_produto)
        
    except ValueError:
        print("Valor inválido. Digite números.")
    except Exception as e:
        print(f"Erro ao cadastrar: {e}")


def alterar_produto():
    try:
        id_produto = int(input("\nDigite o ID do produto a alterar: ").strip())
        produto = obter_produto_por_id(id_produto)
        
        if not produto:
            print(f"Produto {id_produto} não encontrado.")
            return
        
        print(f"\nProduto atual: {produto.nome}")
        print(f"Quantidade: {produto.quantidade}")
        print(f"Preço: R$ {produto.preco:.2f}")
        print("-" * 50)
        
        nome = input(f"Novo nome (Enter para manter '{produto.nome}'): ").strip()
        if nome:
            produto.nome = nome
        
        qtd_str = input(f"Nova quantidade (Enter para manter {produto.quantidade}): ").strip()
        if qtd_str:
            produto.quantidade = int(qtd_str)
        
        preco_str = input(f"Novo preço (Enter para manter R$ {produto.preco:.2f}): ").strip()
        if preco_str:
            produto.preco = float(preco_str)
        
        salvar_ou_atualizar_produto(produto)
        print(f"\nProduto {id_produto} alterado com sucesso!")
        
        gerenciar_fornecedores_produto(id_produto)
        
    except ValueError:
        print("Valor inválido.")
    except Exception as e:
        print(f"Erro ao alterar: {e}")


def excluir_produto():
    try:
        id_produto = int(input("\nDigite o ID do produto a excluir: ").strip())
        produto = obter_produto_por_id(id_produto)
        
        if not produto:
            print(f"Produto {id_produto} não encontrado.")
            return
        
        session = obter_sessao()
        itens_relacionados = session.query(Item).filter(Item.id_produto == id_produto).count()
        
        if itens_relacionados > 0:
            print(f"Não é possível excluir '{produto.nome}' pois há {itens_relacionados} item(s) no histórico de compras.")
            return
        
        confirmacao = input(f"Tem certeza que deseja excluir '{produto.nome}'? [s/n]: ").strip().lower()
        
        if confirmacao == 's':
            session.delete(produto)
            session.commit()
            print(f"Produto '{produto.nome}' excluído com sucesso!")
        else:
            print("Exclusão cancelada.")
            
    except ValueError:
        print("ID inválido.")
    except Exception as e:
        print(f"Erro ao excluir produto: {e}")


def associar_fornecedores_produto(id_produto):
    try:
        resposta = input("\nDeseja associar fornecedores a este produto? [s/n]: ").strip().lower()
        if resposta != 's':
            return
        
        fornecedores = listar_todos_fornecedores()
        if not fornecedores:
            print("Nenhum fornecedor cadastrado.")
            return
        
        tabela = [[f.id, f.nome] for f in fornecedores]
        print("\nFornecedores disponíveis:\n")
        print(tabulate(tabela, headers=["ID", "Nome"], tablefmt="fancy_grid"))

        while True:
            id_fornecedor = input("\nDigite o ID do fornecedor (ou 0 para sair): ").strip()
            if id_fornecedor == '0':
                break
            try:
                id_fornecedor = int(id_fornecedor)
                associar_produto_fornecedor(id_produto, id_fornecedor)
                print(f"Fornecedor {id_fornecedor} associado com sucesso!")
            except ValueError:
                print("ID inválido.")
    except Exception as e:
        print(f"Erro: {e}")


def gerenciar_fornecedores_produto(id_produto):
    try:
        fornecedores = obter_fornecedores_produto(id_produto)
        print("\nFornecedores atuais deste produto:")
        if fornecedores:
            tabela = [[f.id, f.nome] for f in fornecedores]
            print(tabulate(tabela, headers=["ID", "Nome"], tablefmt="fancy_grid"))
        else:
            print("Nenhum fornecedor associado.")
        
        print("\n1. Adicionar fornecedor")
        print("2. Remover fornecedor")
        print("0. Voltar")
        
        opcao = input("Escolha uma opção: ").strip()
        if opcao == '1':
            fornecedores_disponiveis = listar_todos_fornecedores()
            tabela = [[f.id, f.nome] for f in fornecedores_disponiveis if f not in fornecedores]
            print(tabulate(tabela, headers=["ID", "Nome"], tablefmt="fancy_grid"))
            id_fornecedor = int(input("Digite o ID do fornecedor: ").strip())
            associar_produto_fornecedor(id_produto, id_fornecedor)
            print("Fornecedor adicionado!")
        elif opcao == '2':
            id_fornecedor = int(input("Digite o ID do fornecedor a remover: ").strip())
            remover_associacao_produto_fornecedor(id_produto, id_fornecedor)
            print("Fornecedor removido!")
    except ValueError:
        print("ID inválido.")
    except Exception as e:
        print(f"Erro: {e}")


def menu_consultas_produtos():
    while True:
        try:
            print("\n" + "-" * 50)
            print("CONSULTAS ESPECIAIS - PRODUTOS")
            print("-" * 50)
            print("1. Produtos mais vendidos")
            print("2. Produtos menos vendidos")
            print("3. Produtos com estoque baixo")
            print("4. Fornecedores de um produto")
            print("0. Voltar")
            print("-" * 50)
            
            opcao = input("Escolha uma opção: ").strip()
            
            if opcao == '0':
                break
            elif opcao == '1':
                produtos_mais_vendidos()
            elif opcao == '2':
                produtos_menos_vendidos()
            elif opcao == '3':
                produtos_estoque_baixo()
            elif opcao == '4':
                fornecedores_produto()
            else:
                print("\nOpção inválida.")
        except KeyboardInterrupt:
            print("\n\nOperação cancelada pelo usuário.")
            break
        except Exception as e:
            print(f"\nErro: {e}")


def produtos_mais_vendidos():
    session = obter_sessao()
    resultado = session.query(
        Produto.id, Produto.nome, func.sum(Item.quantidade).label('total_vendido')
    ).select_from(Produto).join(Item, Produto.id == Item.id_produto)\
     .group_by(Produto.id, Produto.nome)\
     .order_by(func.sum(Item.quantidade).desc())\
     .limit(10).all()

    if not resultado:
        print("\nNenhum produto vendido encontrado.")
        return

    tabela = [[pid, nome, total] for pid, nome, total in resultado]
    print("\nTOP 10 – PRODUTOS MAIS VENDIDOS\n")
    print(tabulate(tabela, headers=["ID", "Produto", "Total Vendido"], tablefmt="grid", stralign="left", numalign="right"))


def produtos_menos_vendidos():
    session = obter_sessao()
    resultado = session.query(
        Produto.id, Produto.nome, func.sum(Item.quantidade).label('total_vendido')
    ).select_from(Produto).join(Item, Produto.id == Item.id_produto)\
     .group_by(Produto.id, Produto.nome)\
     .order_by(func.sum(Item.quantidade).asc())\
     .limit(10).all()

    if not resultado:
        print("\nNenhum produto vendido encontrado.")
        return

    tabela = [[pid, nome, total] for pid, nome, total in resultado]
    print("\nTOP 10 – PRODUTOS MENOS VENDIDOS\n")
    print(tabulate(tabela, headers=["ID", "Produto", "Total Vendido"], tablefmt="grid", stralign="left", numalign="right"))

    nao_vendidos = session.query(Produto).outerjoin(Item, Produto.id == Item.id_produto)\
        .filter(Item.id == None).all()
    if nao_vendidos:
        tabela_nv = [[p.id, p.nome] for p in nao_vendidos]
        print("\nPRODUTOS NUNCA VENDIDOS:\n")
        print(tabulate(tabela_nv, headers=["ID", "Produto"], tablefmt="simple_grid"))


def produtos_estoque_baixo():
    try:
        limite = int(input("\nDigite o limite de estoque: ").strip())
        session = obter_sessao()
        produtos = session.query(Produto).filter(Produto.quantidade <= limite).order_by(Produto.quantidade.asc()).all()

        if not produtos:
            print(f"\nNenhum produto com estoque <= {limite}.")
            return

        tabela = [[p.id, p.nome, p.quantidade] for p in produtos]
        print(f"\nPRODUTOS COM ESTOQUE BAIXO (<= {limite})\n")
        print(tabulate(tabela, headers=["ID", "Produto", "Estoque"], tablefmt="fancy_grid", stralign="left", numalign="right"))
        print(f"\nTotal: {len(produtos)} produto(s)")

    except ValueError:
        print("Limite inválido. Digite um número.")


def fornecedores_produto():
    try:
        id_produto = int(input("\nDigite o ID do produto: ").strip())
        produto = obter_produto_por_id(id_produto)
        if not produto:
            print(f"Produto {id_produto} não encontrado.")
            return

        fornecedores = obter_fornecedores_produto(id_produto)
        print(f"\nFORNECEDORES DO PRODUTO: {produto.nome} (ID {id_produto})\n")

        if fornecedores:
            tabela = [[f.id, f.nome] for f in fornecedores]
            print(tabulate(tabela, headers=["ID", "Fornecedor"], tablefmt="grid", stralign="left"))
        else:
            print("Nenhum fornecedor associado.")
        
    except ValueError:
        print("ID inválido.")
