import sqlite3

conexao = sqlite3.connect('infotech.db')
cursor = conexao.cursor()


#Comando para se caso necessitar excluir a TABELA COMPLETA
#cursor.execute("DROP TABLE IF EXISTS manutencao")


cursor.execute("""
        CREATE TABLE IF NOT EXISTS manutencao (
            codigo_manutencao INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo_cliente INTEGER NOT NULL,
            data_entrada TEXT NOT NULL,
            tipo_equipamento TEXT NOT NULL,
            marca TEXT NOT NULL,
            modelo TEXT,
            numero_serie TEXT NOT NULL,
            descricao_problema TEXT NOT NULL,
            valor_orcamento REAL NOT NULL,
            status_manutencao TEXT,
            data_status DATE,
            FOREIGN KEY (codigo_cliente) REFERENCES clientes(id)
        )
""")


conexao.commit()
conexao.close()