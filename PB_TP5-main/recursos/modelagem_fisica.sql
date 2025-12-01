-- Tabela Cliente
CREATE TABLE IF NOT EXISTS cliente (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL
);

-- Tabela Produto
CREATE TABLE IF NOT EXISTS produto (
    id INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    quantidade INTEGER DEFAULT 0,
    preco REAL DEFAULT 0.0
);

-- Tabela Fornecedor
CREATE TABLE IF NOT EXISTS fornecedor (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL
);

-- Tabela Compra
CREATE TABLE IF NOT EXISTS compra (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data_hora DATETIME NOT NULL,
    id_cliente INTEGER NOT NULL,
    FOREIGN KEY (id_cliente) REFERENCES cliente(id)
);

-- Tabela Item
CREATE TABLE IF NOT EXISTS item (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quantidade INTEGER NOT NULL,
    preco REAL NOT NULL,
    id_compra INTEGER NOT NULL,
    id_produto INTEGER NOT NULL,
    FOREIGN KEY (id_compra) REFERENCES compra(id),
    FOREIGN KEY (id_produto) REFERENCES produto(id)
);

-- Tabela de relacionamento N:N entre Produto e Fornecedor
CREATE TABLE IF NOT EXISTS produto_fornecedor (
    id_produto INTEGER NOT NULL,
    id_fornecedor INTEGER NOT NULL,
    PRIMARY KEY (id_produto, id_fornecedor),
    FOREIGN KEY (id_produto) REFERENCES produto(id),
    FOREIGN KEY (id_fornecedor) REFERENCES fornecedor(id)
);

-- Índices para melhorar performance
CREATE INDEX IF NOT EXISTS idx_compra_cliente ON compra(id_cliente);
CREATE INDEX IF NOT EXISTS idx_compra_data ON compra(data_hora);
CREATE INDEX IF NOT EXISTS idx_item_compra ON item(id_compra);
CREATE INDEX IF NOT EXISTS idx_item_produto ON item(id_produto);
CREATE INDEX IF NOT EXISTS idx_produto_fornecedor_produto ON produto_fornecedor(id_produto);
CREATE INDEX IF NOT EXISTS idx_produto_fornecedor_fornecedor ON produto_fornecedor(id_fornecedor);

