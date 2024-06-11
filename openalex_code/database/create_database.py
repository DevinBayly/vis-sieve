import duckdb as db

def create(name):
    # TODO add in code to handle if the .db isn't added
    con = db.connect(f'{name}')
    con.execute('''
                DROP TABLE IF EXISTS residence;
                DROP TABLE IF EXISTS contribution;
                DROP TABLE IF EXISTS figure_property;
                DROP TABLE IF EXISTS figure;
                DROP TABLE IF EXISTS author;
                DROP TABLE IF EXISTS institution;
                DROP TABLE IF EXISTS paper;
                ''')


    con.execute('''
    CREATE TABLE author (
        id BIGINT,
        name VARCHAR(100) NOT NULL
    );
                
    CREATE TABLE institution (
        id BIGINT ,
        ror VARCHAR(20) NOT NULL,
        name VARCHAR(100) NOT NULL
    );
                
    CREATE TABLE residence (
        au_id BIGINT,
        inst_id BIGINT,
    );
                
    CREATE TABLE paper (
        id BIGINT ,
        title VARCHAR(200) NOT NULL,
        doi VARCHAR(100),
        publication_date DATE,
        oa_url VARCHAR(200),
        pdf_path VARCHAR(150),
        inst_id BIGINT,
    );
                
    CREATE TABLE contribution (
        au_id BIGINT,
        paper_id BIGINT,
    );
                
    CREATE TABLE figure (
        id BIGINT ,
        paper_id BIGINT,
        local_path VARCHAR(150),
        server_path VARCHAR(150),
    );
                
    CREATE TABLE figure_property (
        name VARCHAR(100),
        int_value INTEGER,
        string_value VARCHAR(100),
        figure_id BIGINT,
    );
                

    ''')

    con.close()