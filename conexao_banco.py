import psycopg2

conn = psycopg2.connect(
        host="localhost",
        database="galeria",
        user='postgres',
        password='123456')

# Abra um cursor para realizar operações de banco de dados
cur = conn.cursor()

# Execute um comando: isso cria uma nova tabela
cur.execute('DROP TABLE IF EXISTS Fotos;')
cur.execute('CREATE TABLE Fotos (id serial PRIMARY KEY,'
                                 'nome varchar (150) NOT NULL,'
                                 'autor varchar (150) NOT NULL,'
                                 'ano integer NOT NULL,'
                                 'url varchar (250));'
                                 )
cur.execute('DROP TABLE IF EXISTS Usuarios;')
cur.execute('CREATE TABLE Usuarios (id serial PRIMARY KEY,'
                                 'nome varchar (150) NOT NULL,'
                                 'username varchar (30) NOT NULL,'
                                 'senha varchar (30) NOT NULL);'
                                 )

# Insert data into the table

cur.execute('INSERT INTO Fotos (nome, autor, ano, url)'
            'VALUES (%s, %s, %s, %s)',
            ('As provações de santo Antônio',
             'Salvador Dali',
             2020,
             'teste')
            )


cur.execute('INSERT INTO Usuarios (nome, username, senha)'
            'VALUES (%s, %s, %s)',
            ('Edilva Carvalho',
             'Edilva',
             '12345')
            )

conn.commit()

cur.close()
conn.close()