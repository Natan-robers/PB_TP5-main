from visualizacoes.sig.menu_clientes import menu_clientes
from visualizacoes.sig.menu_produtos import menu_produtos

def menu_principal_sig():
    while True:
        try:
            print("\n" + "=" * 50)
            print("SIG - Sistema de Informações Gerenciais")
            print("=" * 50)
            print("1. Clientes")
            print("2. Produtos")
            print("0. Sair")
            print("=" * 50)
            
            opcao = input("Escolha uma opção: ").strip()
            
            if opcao == '0':
                print("\nEncerrando SIG...")
                break
            elif opcao == '1':
                menu_clientes()
            elif opcao == '2':
                menu_produtos()
            else:
                print("\nOpção inválida. Digite 0, 1 ou 2.")
        except KeyboardInterrupt:
            print("\n\nOperação cancelada pelo usuário.")
            break
        except Exception as e:
            print(f"\nErro: {e}")
