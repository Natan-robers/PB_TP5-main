import os
from dados.conexao import inicializar_banco, fechar_sessao, obter_sessao,DATABASE_URL
from dados.modelos import Base
from servicos.servico_cliente import carregar_clientes_iniciais
from servicos.servico_produto import importar_produtos_csv_para_bd
from servicos.servico_scraping import executar_scraping_e_gerar_csv
from visualizacoes.menu_caixa import menu_abrir_caixa
from servicos.servico_atendimento import processar_atendimento_loop


def principal():
    try:
        db_path = DATABASE_URL.replace("sqlite:///", "")
        banco_existe = os.path.exists(db_path)

        inicializar_banco(Base)
        print("Banco inicializado (tabelas criadas).")

        obter_sessao()

        if not banco_existe:
            print("Primeira inicialização detectada — carregando dados iniciais...")
            carregar_clientes_iniciais()
            executar_scraping_e_gerar_csv()
            importar_produtos_csv_para_bd()
        else:
            print("Banco já existente — importações ignoradas.")

        if menu_abrir_caixa():
            processar_atendimento_loop()
        else:
            print("Caixa não foi aberto.")

    finally:
        fechar_sessao()


if __name__ == "__main__":
    principal()
