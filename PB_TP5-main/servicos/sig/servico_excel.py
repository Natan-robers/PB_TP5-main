import pandas as pd
import os
from tabulate import tabulate
from dados.repositorio_fornecedor import (
    salvar_fornecedor,
    obter_fornecedor_por_nome,
    obter_fornecedor_por_id,
    associar_produto_fornecedor
)
from dados.repositorio_produto import obter_produto_por_id
from utilidades.arquivos import caminho_excel_fornecedores

def carregar_dados_excel():
    caminho = caminho_excel_fornecedores()

    if not os.path.exists(caminho):
        print(f"AVISO: Arquivo Excel não encontrado: {caminho}")
        print("Crie o arquivo 'recursos/fornecedores.xlsx' com as abas 'fornecedores' e 'produtos-fornecedores'")
        print("Ou execute: python scripts/criar_fornecedores_excel.py")
        return

    try:
        df_fornecedores = pd.read_excel(caminho, sheet_name='fornecedores')
        print(f"\nCarregando {len(df_fornecedores)} fornecedores...")

        fornecedores_carregados = []

        for _, row in df_fornecedores.iterrows():
            nome = str(row.get('nome', '')).strip()
            if nome and nome.lower() != 'nan':
                if not obter_fornecedor_por_nome(nome):
                    salvar_fornecedor(nome)
                    fornecedores_carregados.append(nome)

        if fornecedores_carregados:
            print("\nFornecedores carregados:")
            print(tabulate([[i+1, nome] for i, nome in enumerate(fornecedores_carregados)],
                           headers=["#", "Nome do Fornecedor"], tablefmt="grid"))
        else:
            print("Nenhum fornecedor novo carregado.")

        df_produtos_fornecedores = pd.read_excel(caminho, sheet_name='produtos-fornecedores')
        print(f"\nCarregando {len(df_produtos_fornecedores)} associações produto-fornecedor...")

        associacoes_criadas = []

        for _, row in df_produtos_fornecedores.iterrows():
            try:
                id_produto = int(row.get('id_produto', 0))
                id_fornecedor = int(row.get('id_fornecedor', 0))

                produto = obter_produto_por_id(id_produto)
                fornecedor = obter_fornecedor_por_id(id_fornecedor)

                if produto and fornecedor:
                    associar_produto_fornecedor(id_produto, id_fornecedor)
                    associacoes_criadas.append([id_produto, produto.nome, id_fornecedor, fornecedor.nome])
            except (ValueError, TypeError):
                continue

        if associacoes_criadas:
            print("\nAssociações criadas:")
            print(tabulate(associacoes_criadas,
                           headers=["ID Produto", "Produto", "ID Fornecedor", "Fornecedor"],
                           tablefmt="grid"))
        else:
            print("Nenhuma associação criada.")

        print("\nCarregamento do Excel concluído com sucesso!")

    except Exception as ex:
        print(f"Erro ao carregar Excel: {ex}")
        print("Certifique-se de que o arquivo tem as abas 'fornecedores' e 'produtos-fornecedores'")

