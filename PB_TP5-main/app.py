from dados.conexao import inicializar_banco, fechar_sessao, obter_sessao
from dados.modelos import Base
from servicos.servico_cliente import carregar_clientes_iniciais
from servicos.servico_produto import importar_produtos_csv_para_bd
from servicos.servico_scraping import executar_scraping_e_gerar_csv
from visualizacoes.menu_caixa import menu_abrir_caixa
from servicos.servico_atendimento import processar_atendimento_loop

def principal():
    try:
        inicializar_banco(Base)
        print("Banco inicializado (tabelas criadas).")
        
        obter_sessao()
        
        carregar_clientes_iniciais()
        executar_scraping_e_gerar_csv()
        importar_produtos_csv_para_bd()
        if menu_abrir_caixa():
            processar_atendimento_loop()
        else:
            print("Caixa não foi aberto.")
    finally:
        fechar_sessao()

if __name__ == '__main__':
    principal()


