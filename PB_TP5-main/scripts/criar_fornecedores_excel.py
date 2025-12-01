import pandas as pd
import os

def criar_arquivo_fornecedores():
    df_fornecedores = pd.DataFrame({
        'nome': [
            'Fornecedor A',
            'Fornecedor B',
            'Fornecedor C',
            'Fornecedor D'
        ]
    })
    
    df_produtos_fornecedores = pd.DataFrame({
        'id_produto': [1, 2, 3, 1, 4],
        'id_fornecedor': [1, 1, 2, 2, 3]
    })
    
    # Criar pasta recursos se não existir
    diretorio_recursos = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'recursos')
    os.makedirs(diretorio_recursos, exist_ok=True)
    
    caminho_excel = os.path.join(diretorio_recursos, 'fornecedores.xlsx')
    
    with pd.ExcelWriter(caminho_excel, engine='openpyxl') as writer:
        df_fornecedores.to_excel(writer, sheet_name='fornecedores', index=False)
        df_produtos_fornecedores.to_excel(writer, sheet_name='produtos-fornecedores', index=False)
    
    print(f"Arquivo {caminho_excel} criado com sucesso!")
    print("\nEstrutura criada:")
    print("- Aba 'fornecedores':", len(df_fornecedores), "fornecedores")
    print("- Aba 'produtos-fornecedores':", len(df_produtos_fornecedores), "associacoes")
    print("\nIMPORTANTE: Ajuste os IDs de produtos conforme os produtos existentes no banco!")

if __name__ == '__main__':
    criar_arquivo_fornecedores()

