import psycopg2


def init_supermarket_db():
    conn = psycopg2.connect(
        host="localhost",
        database="airflow",
        user="airflow",
        password="airflow",
        port="5432"
    )
    cur = conn.cursor()
    
    cur.execute("DROP TABLE IF EXISTS supermarket_feedback;")
    cur.execute("""
        CREATE TABLE supermarket_feedback (
            id SERIAL PRIMARY KEY,
            setor TEXT, -- Ex: Hortifruti, Açougue, Padaria
            produto_nome_bruto TEXT,
            comentario_cliente TEXT,
            data_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    

    query = "INSERT INTO supermarket_feedback (setor, produto_nome_bruto, comentario_cliente) VALUES (%s, %s, %s)"
    samples = [
        ('Hortifruti', '  tomate cereja 200g  ', 'Alguns tomates vieram amassados no fundo da embalagem.'),
        ('Padaria', 'pao de forma artesanal', 'Muito macio e fresquinho, adorei!'),
        ('Açougue', 'carne moida patinho', 'A carne estava com muita gordura dessa vez.'),
        ('Limpeza', 'Detergente', 'O cheiro é bom, mas nao faz muita espuma.')
    ]
    
    cur.executemany(query, samples)
    conn.commit()
    print("Banco do Supermercado pronto!")
    cur.close()
    conn.close()

if __name__ == "__main__":
    init_supermarket_db()