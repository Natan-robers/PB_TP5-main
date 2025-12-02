from dados.repositorio_cliente import listar_todos_clientes, obter_cliente_por_id
from dados.repositorio_compra import (
    obter_compras_por_cliente, obter_itens_compra, obter_total_compra
)
from dados.conexao import obter_sessao
from dados.modelos import Cliente, Compra
from sqlalchemy import func
from tabulate import tabulate


def menu_clientes():
    while True:
        try:
            print("\n" + "-" * 50)
            print("MENU CLIENTES")
            print("-" * 50)
            print("1. Clientes com compras")
            print("2. Clientes sem compras")
            print("0. Voltar")
            print("-" * 50)
            
            opcao = input("Escolha uma opção: ").strip()
            
            if opcao == '0':
                break
            elif opcao == '1':
                menu_clientes_com_compras()
            elif opcao == '2':
                listar_clientes_sem_compras()
            else:
                print("\nOpção inválida. Digite 0, 1 ou 2.")
        except KeyboardInterrupt:
            print("\n\nOperação cancelada pelo usuário.")
            break
        except Exception as e:
            print(f"\nErro: {e}")


def menu_clientes_com_compras():
    while True:
        try:
            print("\n" + "-" * 50)
            print("CLIENTES COM COMPRAS")
            print("-" * 50)
            print("1. Consultar compras de um cliente")
            print("2. Clientes que mais compram")
            print("3. Clientes que mais gastam")
            print("0. Voltar")
            print("-" * 50)
            
            opcao = input("Escolha uma opção: ").strip()
            
            if opcao == '0':
                break
            elif opcao == '1':
                consultar_compras_cliente()
            elif opcao == '2':
                clientes_que_mais_compram()
            elif opcao == '3':
                clientes_que_mais_gastam()
            else:
                print("\nOpção inválida.")
        except KeyboardInterrupt:
            print("\n\nOperação cancelada pelo usuário.")
            break
        except Exception as e:
            print(f"\nErro: {e}")


def consultar_compras_cliente():
    try:
        id_cliente = int(input("\nDigite o ID do cliente: ").strip())
        cliente = obter_cliente_por_id(id_cliente)
        
        if not cliente:
            print(f"Cliente {id_cliente} não encontrado.")
            return
        
        compras = obter_compras_por_cliente(id_cliente)
        if not compras:
            print(f"\nCliente {cliente.nome} não possui compras registradas.")
            return
        
        tabela = [
            [c.id, c.data_hora.strftime("%d/%m/%Y %H:%M:%S"), f"R$ {obter_total_compra(c.id):.2f}"]
            for c in compras
        ]
        print(f"\nCompras do cliente {cliente.nome} (ID: {id_cliente}):\n")
        print(tabulate(tabela, headers=["ID", "Data/Hora", "Total"], tablefmt="fancy_grid", stralign="left", numalign="right"))

        id_compra = input("\nDigite o ID da compra para ver detalhes (ou Enter para voltar): ").strip()
        if id_compra:
            try:
                exibir_nota_fiscal_compra(int(id_compra))
            except ValueError:
                print("ID inválido.")
    except ValueError:
        print("ID inválido. Digite um número.")
    except Exception as e:
        print(f"Erro: {e}")


def exibir_nota_fiscal_compra(id_compra):
    from dados.repositorio_compra import obter_compra_por_id
    
    compra = obter_compra_por_id(id_compra)
    if not compra:
        print(f"Compra {id_compra} não encontrada.")
        return
    
    itens = obter_itens_compra(id_compra)
    total = obter_total_compra(id_compra)

    tabela = [
        [item.produto.nome, item.quantidade, f"R$ {item.preco:.2f}", f"R$ {item.total:.2f}"]
        for item in itens
    ]
    
    print("\nNOTA FISCAL\n")
    print(f"Cliente: {compra.cliente.nome} (ID: {compra.cliente.id})")
    print(f"Compra ID: {id_compra}")
    print(f"Data/Hora: {compra.data_hora.strftime('%d/%m/%Y %H:%M:%S')}\n")
    print(tabulate(tabela, headers=["Produto", "Qtd", "Preço Unit.", "Total"], tablefmt="fancy_grid", stralign="left", numalign="right"))
    print(f"\nTOTAL: R$ {total:.2f}")


def clientes_que_mais_compram():
    session = obter_sessao()
    
    resultado = session.query(
        Cliente.id,
        Cliente.nome,
        func.count(Compra.id).label('total_compras')
    ).select_from(Cliente).join(Compra, Cliente.id == Compra.id_cliente)\
     .group_by(Cliente.id, Cliente.nome)\
     .order_by(func.count(Compra.id).desc()).all()
    
    if not resultado:
        print("\nNenhum cliente com compras encontrado.")
        return
    
    tabela = [[cid, nome, total] for cid, nome, total in resultado]
    print("\nCLIENTES QUE MAIS COMPRAM\n")
    print(tabulate(tabela, headers=["ID", "Nome", "Total de Compras"], tablefmt="fancy_grid", stralign="left", numalign="right"))


def clientes_que_mais_gastam():
    session = obter_sessao()
    from dados.modelos import Item
    
    resultado = session.query(
        Cliente.id,
        Cliente.nome,
        func.sum(Item.quantidade * Item.preco).label('total_gasto')
    ).select_from(Cliente).join(Compra, Cliente.id == Compra.id_cliente).join(Item, Compra.id == Item.id_compra)\
     .group_by(Cliente.id, Cliente.nome)\
     .order_by(func.sum(Item.quantidade * Item.preco).desc()).all()
    
    if not resultado:
        print("\nNenhum cliente com compras encontrado.")
        return
    
    tabela = [[cid, nome, f"R$ {total:.2f}"] for cid, nome, total in resultado]
    print("\nCLIENTES QUE MAIS GASTAM\n")
    print(tabulate(tabela, headers=["ID", "Nome", "Total Gasto"], tablefmt="fancy_grid", stralign="left", numalign="right"))


def listar_clientes_sem_compras():
    session = obter_sessao()
    clientes_sem_compras = session.query(Cliente).outerjoin(Compra, Cliente.id == Compra.id_cliente).filter(Compra.id == None).all()
    
    if not clientes_sem_compras:
        print("\nTodos os clientes possuem pelo menos uma compra.")
        return
    
    tabela = [[c.id, c.nome] for c in clientes_sem_compras]
    print("\nCLIENTES SEM COMPRAS\n")
    print(tabulate(tabela, headers=["ID", "Nome"], tablefmt="fancy_grid", stralign="left"))
    print(f"\nTotal: {len(clientes_sem_compras)} cliente(s) sem compras.")

