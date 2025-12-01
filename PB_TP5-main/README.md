# TP5 - Sistema de Supermercado

## 📁 Estrutura do Projeto

```
mercado_tp4/
├── app.py                          # Aplicação do Caixa
├── sig.py                          # Aplicação SIG
├── scripts/
│   ├── popular_banco_teste.py      # Script para popular dados de teste
│   ├── criar_fornecedores_excel.py # Script para criar fornecedores.xlsx
│   └── testar_consultas_sig.py     # Script de teste automatizado
├── dados/
│   ├── conexao.py                  # Gerenciamento de sessão única
│   ├── modelos.py                  # Modelos SQLAlchemy
│   └── repositorio_*.py            # Repositórios de dados
├── servicos/
│   ├── servico_cliente.py          # Serviços de cliente
│   ├── servico_produto.py          # Serviços de produto
│   ├── servico_scraping.py         # Web scraping
│   ├── servico_atendimento.py      # Lógica de atendimento
│   └── sig/
│       └── servico_excel.py        # Carregamento de Excel
├── visualizacoes/
│   ├── menu_caixa.py               # Menu do caixa
│   ├── interface_console.py        # Interface console
│   └── sig/
│       ├── menu_principal.py       # Menu principal SIG
│       ├── menu_clientes.py        # Menu de clientes
│       └── menu_produtos.py        # Menu de produtos
├── utilidades/
│   ├── arquivos.py                 # Utilitários de arquivos
│   └── validacoes.py               # Validações
└── recursos/
    ├── clientes.json               # Arquivo JSON com clientes iniciais
    ├── produtos.csv                # Arquivo CSV gerado pelo scraping
    ├── fornecedores.xlsx           # Arquivo Excel com fornecedores
    ├── mercado.db                  # Banco de dados SQLite
    └── modelagem_fisica.sql        # Script SQL de modelagem
```

## 🧪 Dados de Teste

Para popular o banco de dados com dados de teste, execute:

```bash
python scripts/popular_banco_teste.py
```

Este script cria:
- 5 clientes de teste
- 4 fornecedores de teste
- Várias compras para demonstrar as funcionalidades do SIG
- Associações entre produtos e fornecedores

**Ordem de Execução:**
1. Execute `app.py` para carregar produtos via web scraping
2. Execute `scripts/popular_banco_teste.py` para criar dados de teste
3. Execute `sig.py` para acessar o SIG ou `app.py` para o caixa
