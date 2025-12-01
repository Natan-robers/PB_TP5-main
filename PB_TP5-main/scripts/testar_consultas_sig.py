"""
Script de teste automatizado para todas as consultas do SIG
"""
import sys
from io import StringIO
from contextlib import redirect_stdout

def testar_consultas_sig():
    """Testa todas as consultas do SIG"""
    print("=" * 70)
    print("TESTANDO TODAS AS CONSULTAS DO SIG")
    print("=" * 70)
    
    erros = []
    sucessos = []
    
    try:
        from dados.conexao import inicializar_banco, obter_sessao, fechar_sessao
        from dados.modelos import Base, Cliente, Compra, Item, Produto, Fornecedor
        from dados.repositorio_cliente import listar_todos_clientes, obter_cliente_por_id
        from dados.repositorio_compra import obter_compras_por_cliente, obter_total_compra, obter_compra_por_id, obter_itens_compra
        from dados.repositorio_produto import listar_todos_produtos, obter_produto_por_id
        from dados.repositorio_fornecedor import listar_todos_fornecedores, obter_fornecedores_produto
        from sqlalchemy import func
        
        inicializar_banco(Base)
        obter_sessao()
        
        # ============================================================
        # TESTE 1: Listar todos os clientes
        # ============================================================
        print("\n[TESTE 1] Listar todos os clientes")
        try:
            clientes = listar_todos_clientes()
            print(f"  OK - {len(clientes)} clientes encontrados")
            sucessos.append("Listar clientes")
        except Exception as e:
            print(f"  ERRO - {e}")
            erros.append(f"Listar clientes: {e}")
        
        # ============================================================
        # TESTE 2: Clientes que mais compram
        # ============================================================
        print("\n[TESTE 2] Clientes que mais compram")
        try:
            session = obter_sessao()
            resultado = session.query(
                Cliente.id,
                Cliente.nome,
                func.count(Compra.id).label('total_compras')
            ).select_from(Cliente).join(Compra, Cliente.id == Compra.id_cliente).group_by(Cliente.id, Cliente.nome).order_by(func.count(Compra.id).desc()).all()
            
            if resultado:
                print(f"  OK - {len(resultado)} clientes com compras encontrados")
                print(f"      Top cliente: {resultado[0].nome} com {resultado[0].total_compras} compras")
                sucessos.append("Clientes que mais compram")
            else:
                print("  AVISO - Nenhum cliente com compras")
                sucessos.append("Clientes que mais compram (sem dados)")
        except Exception as e:
            print(f"  ERRO - {e}")
            erros.append(f"Clientes que mais compram: {e}")
        
        # ============================================================
        # TESTE 3: Clientes que mais gastam
        # ============================================================
        print("\n[TESTE 3] Clientes que mais gastam")
        try:
            session = obter_sessao()
            resultado = session.query(
                Cliente.id,
                Cliente.nome,
                func.sum(Item.quantidade * Item.preco).label('total_gasto')
            ).select_from(Cliente).join(Compra, Cliente.id == Compra.id_cliente).join(Item, Compra.id == Item.id_compra).group_by(Cliente.id, Cliente.nome).order_by(func.sum(Item.quantidade * Item.preco).desc()).all()
            
            if resultado:
                print(f"  OK - {len(resultado)} clientes encontrados")
                print(f"      Top cliente: {resultado[0].nome} gastou R$ {resultado[0].total_gasto:.2f}")
                sucessos.append("Clientes que mais gastam")
            else:
                print("  AVISO - Nenhum cliente com compras")
                sucessos.append("Clientes que mais gastam (sem dados)")
        except Exception as e:
            print(f"  ERRO - {e}")
            erros.append(f"Clientes que mais gastam: {e}")
        
        # ============================================================
        # TESTE 4: Clientes sem compras
        # ============================================================
        print("\n[TESTE 4] Clientes sem compras")
        try:
            session = obter_sessao()
            clientes_sem_compras = session.query(Cliente).outerjoin(Compra, Cliente.id == Compra.id_cliente).filter(Compra.id == None).all()
            print(f"  OK - {len(clientes_sem_compras)} clientes sem compras")
            sucessos.append("Clientes sem compras")
        except Exception as e:
            print(f"  ERRO - {e}")
            erros.append(f"Clientes sem compras: {e}")
        
        # ============================================================
        # TESTE 5: Consultar compras de um cliente
        # ============================================================
        print("\n[TESTE 5] Consultar compras de um cliente")
        try:
            # Buscar um cliente que tenha compras
            session = obter_sessao()
            cliente_com_compra = session.query(Cliente).join(Compra).first()
            
            if cliente_com_compra:
                compras = obter_compras_por_cliente(cliente_com_compra.id)
                print(f"  OK - Cliente {cliente_com_compra.nome} tem {len(compras)} compras")
                if compras:
                    total = obter_total_compra(compras[0].id)
                    print(f"      Primeira compra (ID: {compras[0].id}) total: R$ {total:.2f}")
                sucessos.append("Consultar compras de cliente")
            else:
                print("  AVISO - Nenhum cliente com compras para testar")
                sucessos.append("Consultar compras de cliente (sem dados)")
        except Exception as e:
            print(f"  ERRO - {e}")
            erros.append(f"Consultar compras de cliente: {e}")
        
        # ============================================================
        # TESTE 6: Exibir nota fiscal de uma compra
        # ============================================================
        print("\n[TESTE 6] Exibir nota fiscal de uma compra")
        try:
            session = obter_sessao()
            compra = session.query(Compra).first()
            
            if compra:
                itens = obter_itens_compra(compra.id)
                total = obter_total_compra(compra.id)
                print(f"  OK - Compra {compra.id} tem {len(itens)} itens, total: R$ {total:.2f}")
                sucessos.append("Exibir nota fiscal")
            else:
                print("  AVISO - Nenhuma compra para testar")
                sucessos.append("Exibir nota fiscal (sem dados)")
        except Exception as e:
            print(f"  ERRO - {e}")
            erros.append(f"Exibir nota fiscal: {e}")
        
        # ============================================================
        # TESTE 7: Listar todos os produtos
        # ============================================================
        print("\n[TESTE 7] Listar todos os produtos")
        try:
            produtos = listar_todos_produtos()
            print(f"  OK - {len(produtos)} produtos encontrados")
            if produtos:
                print(f"      Primeiro produto: {produtos[0].nome} (ID: {produtos[0].id})")
            sucessos.append("Listar produtos")
        except Exception as e:
            print(f"  ERRO - {e}")
            erros.append(f"Listar produtos: {e}")
        
        # ============================================================
        # TESTE 8: Produtos mais vendidos
        # ============================================================
        print("\n[TESTE 8] Produtos mais vendidos")
        try:
            session = obter_sessao()
            resultado = session.query(
                Produto.id,
                Produto.nome,
                func.sum(Item.quantidade).label('total_vendido')
            ).select_from(Produto).join(Item, Produto.id == Item.id_produto).group_by(Produto.id, Produto.nome).order_by(func.sum(Item.quantidade).desc()).limit(10).all()
            
            if resultado:
                print(f"  OK - {len(resultado)} produtos mais vendidos encontrados")
                print(f"      Top produto: {resultado[0].nome} - {resultado[0].total_vendido} unidades")
                sucessos.append("Produtos mais vendidos")
            else:
                print("  AVISO - Nenhum produto vendido")
                sucessos.append("Produtos mais vendidos (sem dados)")
        except Exception as e:
            print(f"  ERRO - {e}")
            erros.append(f"Produtos mais vendidos: {e}")
        
        # ============================================================
        # TESTE 9: Produtos menos vendidos
        # ============================================================
        print("\n[TESTE 9] Produtos menos vendidos")
        try:
            session = obter_sessao()
            resultado = session.query(
                Produto.id,
                Produto.nome,
                func.sum(Item.quantidade).label('total_vendido')
            ).select_from(Produto).join(Item, Produto.id == Item.id_produto).group_by(Produto.id, Produto.nome).order_by(func.sum(Item.quantidade).asc()).limit(10).all()
            
            if resultado:
                print(f"  OK - {len(resultado)} produtos menos vendidos encontrados")
                sucessos.append("Produtos menos vendidos")
            else:
                print("  AVISO - Nenhum produto vendido")
                sucessos.append("Produtos menos vendidos (sem dados)")
            
            # Testar produtos nunca vendidos
            produtos_nao_vendidos = session.query(Produto).outerjoin(Item, Produto.id == Item.id_produto).filter(Item.id == None).all()
            print(f"      Produtos nunca vendidos: {len(produtos_nao_vendidos)}")
        except Exception as e:
            print(f"  ERRO - {e}")
            erros.append(f"Produtos menos vendidos: {e}")
        
        # ============================================================
        # TESTE 10: Produtos com estoque baixo
        # ============================================================
        print("\n[TESTE 10] Produtos com estoque baixo")
        try:
            session = obter_sessao()
            limite = 10
            produtos = session.query(Produto).filter(Produto.quantidade <= limite).order_by(Produto.quantidade.asc()).all()
            print(f"  OK - {len(produtos)} produtos com estoque <= {limite}")
            sucessos.append("Produtos com estoque baixo")
        except Exception as e:
            print(f"  ERRO - {e}")
            erros.append(f"Produtos com estoque baixo: {e}")
        
        # ============================================================
        # TESTE 11: Fornecedores de um produto
        # ============================================================
        print("\n[TESTE 11] Fornecedores de um produto")
        try:
            produtos = listar_todos_produtos()
            if produtos:
                fornecedores = obter_fornecedores_produto(produtos[0].id)
                print(f"  OK - Produto {produtos[0].nome} (ID: {produtos[0].id}) tem {len(fornecedores)} fornecedor(es)")
                sucessos.append("Fornecedores de um produto")
            else:
                print("  AVISO - Nenhum produto para testar")
                sucessos.append("Fornecedores de um produto (sem dados)")
        except Exception as e:
            print(f"  ERRO - {e}")
            erros.append(f"Fornecedores de um produto: {e}")
        
        # ============================================================
        # TESTE 12: Listar todos os fornecedores
        # ============================================================
        print("\n[TESTE 12] Listar todos os fornecedores")
        try:
            fornecedores = listar_todos_fornecedores()
            print(f"  OK - {len(fornecedores)} fornecedores encontrados")
            sucessos.append("Listar fornecedores")
        except Exception as e:
            print(f"  ERRO - {e}")
            erros.append(f"Listar fornecedores: {e}")
        
        fechar_sessao()
        
    except Exception as e:
        print(f"\nERRO CRITICO: {e}")
        import traceback
        traceback.print_exc()
        erros.append(f"Erro critico: {e}")
    
    # ============================================================
    # RESUMO
    # ============================================================
    print("\n" + "=" * 70)
    print("RESUMO DOS TESTES")
    print("=" * 70)
    print(f"Testes bem-sucedidos: {len(sucessos)}")
    print(f"Testes com erro: {len(erros)}")
    
    if erros:
        print("\nERROS ENCONTRADOS:")
        for erro in erros:
            print(f"  - {erro}")
    
    if sucessos:
        print("\nTESTES BEM-SUCEDIDOS:")
        for sucesso in sucessos:
            print(f"  OK - {sucesso}")
    
    print("=" * 70)
    
    return len(erros) == 0

if __name__ == '__main__':
    resultado = testar_consultas_sig()
    if resultado:
        print("\nTODOS OS TESTES PASSARAM!")
        sys.exit(0)
    else:
        print("\nALGUNS TESTES FALHARAM!")
        sys.exit(1)

