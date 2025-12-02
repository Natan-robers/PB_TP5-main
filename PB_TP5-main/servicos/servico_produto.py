import pandas as pd
from dados.repositorio_produto import salvar_ou_atualizar_produto
from dados.modelos import Produto
from utilidades.arquivos import caminho_produtos_csv
from tabulate import tabulate

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
        print(f"CSV lido com sucesso: {len(df)} linhas encontradas\n")
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


    resumo_tabela = [
        ["Produtos novos importados", produtos_importados],
        ["Produtos atualizados", produtos_atualizados],
        ["Produtos ignorados", produtos_ignorados],
    ]

    print("\nIMPORTAÇÃO DE PRODUTOS CONCLUÍDA:\n")
    print(tabulate(
        resumo_tabela,
        headers=["Descrição", "Quantidade"],
        tablefmt="fancy_grid",
        stralign="left",
        numalign="right"
    ))

    from dados.repositorio_produto import contar_produtos, listar_todos_produtos
    total_produtos = contar_produtos()
    produtos_validos = produtos_importados + produtos_atualizados
    produtos_no_csv = len(df)

    print(f"\nTotal de produtos válidos no banco: {total_produtos}")
    print(f"Produtos processados nesta importação: {produtos_validos}")

    if total_produtos > produtos_no_csv:
        diferenca = total_produtos - produtos_no_csv
        print(f"\nAVISO: O banco possui {total_produtos} produtos, mas o CSV contém apenas {produtos_no_csv}.")
        print(f"Há {diferenca} produto(s) antigo(s) no banco de execuções anteriores.")

    if total_produtos > 0:
        print("\nAmostra dos produtos no banco (primeiros 10):\n")
        produtos = listar_todos_produtos()

        tabela_produtos = [
            [p.id, p.nome, p.quantidade, f"R$ {p.preco:.2f}"]
            for p in produtos[:10]
        ]

        print(tabulate(
            tabela_produtos,
            headers=["ID", "Nome", "Quantidade", "Preço"],
            tablefmt="grid",
            showindex=True
        ))

        if total_produtos > 10:
            print(f"\n... e mais {total_produtos - 10} produtos no banco.\n")
