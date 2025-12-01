import pandas as pd
from dados.repositorio_produto import salvar_ou_atualizar_produto
from dados.modelos import Produto
from utilidades.arquivos import caminho_produtos_csv

def importar_produtos_csv_para_bd():
    import os
    caminho_csv = caminho_produtos_csv()

    if not os.path.exists(caminho_csv):
        print(f"AVISO: Arquivo CSV não encontrado: {caminho_csv}")
        print("O arquivo será criado na próxima execução do web scraping.")
        return

    try:
        df = pd.read_csv(caminho_csv)
        if df.empty:
            print("AVISO: O arquivo CSV está vazio. Nenhum produto para importar.")
            return
        print(f"CSV lido com sucesso: {len(df)} linhas encontradas")
    except Exception as ex:
        print(f"Erro ao ler CSV de produtos: {ex}")
        return

    produtos_importados = 0
    produtos_atualizados = 0
    produtos_ignorados = 0

    for idx, row in df.iterrows():
        id_val = None
        for col in ['id', 'Id', 'ID', 'codigo', 'codigo_produto']:
            if col in df.columns:
                id_val = row[col]
                break
        if id_val is None:
            id_val = int(idx) + 1

        nome = None
        for col in ['nome', 'Nome', 'titulo', 'produto']:
            if col in df.columns:
                nome = row[col]
                break
        if nome is None:
            nome = str(row.get(df.columns[0], 'Produto'))

        if not nome or nome.strip() == "":
            produtos_ignorados += 1
            continue

        if nome.lower() in ['valor', 'produto']:
            nome = f"Produto {id_val}"

        qtd = 0
        for col in ['quantidade', 'quant', 'qtd']:
            if col in df.columns:
                try:
                    qtd = int(row[col])
                except (ValueError, TypeError):
                    qtd = 0
                break

        preco = 0.0
        for col in ['preco', 'preço', 'valor']:
            if col in df.columns:
                try:
                    preco = float(row[col])
                except (ValueError, TypeError):
                    preco = 0.0
                break

        from dados.repositorio_produto import obter_produto_por_id
        produto_existente = obter_produto_por_id(int(id_val))

        produto = Produto(
            id=int(id_val),
            nome=str(nome),
            quantidade=int(qtd),
            preco=float(preco)
        )
        salvar_ou_atualizar_produto(produto)

        if produto_existente:
            produtos_atualizados += 1
        else:
            produtos_importados += 1

    print("Importação de produtos concluída:")
    print(f"  - {produtos_importados} produtos novos importados")
    print(f"  - {produtos_atualizados} produtos atualizados")
    print(f"  - {produtos_ignorados} produtos ignorados (não foram salvos no banco)")

    from dados.repositorio_produto import contar_produtos, listar_todos_produtos
    total_produtos = contar_produtos()
    produtos_validos = produtos_importados + produtos_atualizados
    produtos_no_csv = len(df)

    print(f"  - Total de produtos válidos no banco: {total_produtos}")
    print(f"  - Produtos processados nesta importação: {produtos_validos} (ignorados não são salvos)")

    if total_produtos > produtos_no_csv:
        diferenca = total_produtos - produtos_no_csv
        print(f"\n AVISO: O banco tem {total_produtos} produtos, mas o CSV tem apenas {produtos_no_csv}.")
        print(f"   Há {diferenca} produto(s) antigo(s) no banco de execuções anteriores.")

    if total_produtos > 0:
        print("\nAmostra dos produtos no banco (primeiros 10):")
        produtos = listar_todos_produtos()
        for i, p in enumerate(produtos[:10], 1):
            print(f"  {i}. ID: {p.id}, Nome: {p.nome}, Qtd: {p.quantidade}, Preço: R$ {p.preco:.2f}")

        if total_produtos > 10:
            print(f"  ... e mais {total_produtos - 10} produtos no banco.")
