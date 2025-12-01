from dados.repositorio_cliente import listar_todos_clientes, obter_cliente_por_id
from dados.repositorio_compra import obter_compras_por_cliente, obter_itens_compra, obter_total_compra
from dados.conexao import obter_sessao
from dados.modelos import Cliente, Compra
from sqlalchemy import func

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
        
        print(f"\nCompras do cliente {cliente.nome} (ID: {id_cliente}):")
        print("-" * 70)
        print(f"{'ID':<5} {'Data/Hora':<20} {'Total':<15}")
        print("-" * 70)
        
        for compra in compras:
            total = obter_total_compra(compra.id)
            data_str = compra.data_hora.strftime("%d/%m/%Y %H:%M:%S")
            print(f"{compra.id:<5} {data_str:<20} R$ {total:>10.2f}")
        
        print("\n" + "-" * 70)
        id_compra = input("Digite o ID da compra para ver detalhes (ou Enter para voltar): ").strip()
        
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
    
    print("\n" + "=" * 70)
    print("NOTA FISCAL")
    print("=" * 70)
    print(f"Cliente: {compra.cliente.nome} (ID: {compra.cliente.id})")
    print(f"Compra ID: {id_compra}")
    print(f"Data/Hora: {compra.data_hora.strftime('%d/%m/%Y %H:%M:%S')}")
    print("-" * 70)
    print(f"{'Produto':<30} {'Qtd':<10} {'Preço Unit.':<15} {'Total':<15}")
    print("-" * 70)
    
    for item in itens:
        print(f"{item.produto.nome:<30} {item.quantidade:<10} R$ {item.preco:>10.2f} R$ {item.total:>10.2f}")
    
    print("-" * 70)
    print(f"{'TOTAL':<55} R$ {total:>10.2f}")
    print("=" * 70)

def clientes_que_mais_compram():
    session = obter_sessao()
    
    resultado = session.query(
        Cliente.id,
        Cliente.nome,
        func.count(Compra.id).label('total_compras')
    ).select_from(Cliente).join(Compra, Cliente.id == Compra.id_cliente).group_by(Cliente.id, Cliente.nome).order_by(func.count(Compra.id).desc()).all()
    
    if not resultado:
        print("\nNenhum cliente com compras encontrado.")
        return
    
    print("\n" + "=" * 70)
    print("CLIENTES QUE MAIS COMPRAM")
    print("=" * 70)
    print(f"{'ID':<5} {'Nome':<40} {'Total de Compras':<20}")
    print("-" * 70)
    
    for cliente_id, nome, total_compras in resultado:
        print(f"{cliente_id:<5} {nome:<40} {total_compras:<20}")
    
    print("=" * 70)

def clientes_que_mais_gastam():
    session = obter_sessao()
    from dados.modelos import Item
    
    resultado = session.query(
        Cliente.id,
        Cliente.nome,
        func.sum(Item.quantidade * Item.preco).label('total_gasto')
    ).select_from(Cliente).join(Compra, Cliente.id == Compra.id_cliente).join(Item, Compra.id == Item.id_compra).group_by(Cliente.id, Cliente.nome).order_by(func.sum(Item.quantidade * Item.preco).desc()).all()
    
    if not resultado:
        print("\nNenhum cliente com compras encontrado.")
        return
    
    print("\n" + "=" * 70)
    print("CLIENTES QUE MAIS GASTAM")
    print("=" * 70)
    print(f"{'ID':<5} {'Nome':<40} {'Total Gasto':<20}")
    print("-" * 70)
    
    for cliente_id, nome, total_gasto in resultado:
        print(f"{cliente_id:<5} {nome:<40} R$ {total_gasto:>15.2f}")
    
    print("=" * 70)

def listar_clientes_sem_compras():
    session = obter_sessao()
    clientes_sem_compras = session.query(Cliente).outerjoin(Compra, Cliente.id == Compra.id_cliente).filter(Compra.id == None).all()
    
    if not clientes_sem_compras:
        print("\nTodos os clientes possuem pelo menos uma compra.")
        return
    
    print("\n" + "=" * 70)
    print("CLIENTES SEM COMPRAS")
    print("=" * 70)
    print(f"{'ID':<5} {'Nome':<65}")
    print("-" * 70)
    
    for cliente in clientes_sem_compras:
        print(f"{cliente.id:<5} {cliente.nome:<65}")
    
    print("=" * 70)
    print(f"Total: {len(clientes_sem_compras)} cliente(s) sem compras.")
