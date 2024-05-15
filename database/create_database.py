import duckdb as db

con = db.connect('publications.db')
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
    id BIGINT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);
            
CREATE TABLE institution (
    id BIGINT PRIMARY KEY,
    ror VARCHAR(20) NOT NULL,
    name VARCHAR(100) NOT NULL
);
            
CREATE TABLE residence (
    au_id BIGINT,
    inst_id BIGINT,
    PRIMARY KEY (au_id, inst_id),
    FOREIGN KEY (au_id) REFERENCES author(id),
    FOREIGN KEY (inst_id) REFERENCES institution(id)
);
            
CREATE TABLE paper (
    id BIGINT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    doi VARCHAR(100),
    publication_date DATE,
    oa_url VARCHAR(200),
    pdf_path VARCHAR(150),
    grabbed BOOL
);
            
CREATE TABLE contribution (
    au_id BIGINT,
    paper_id BIGINT,
    PRIMARY KEY (au_id, paper_id),
    FOREIGN KEY (au_id) REFERENCES author(id),
    FOREIGN KEY (paper_id) REFERENCES paper(id)
);
            
CREATE TABLE figure (
    id BIGINT PRIMARY KEY,
    paper_id BIGINT,
    local_path VARCHAR(150),
    server_path VARCHAR(150),
    FOREIGN KEY (paper_id) REFERENCES paper(id),   
);
            
CREATE TABLE figure_property (
    name VARCHAR(100),
    int_value INTEGER,
    string_value VARCHAR(100),
    figure_id BIGINT,
    FOREIGN KEY (figure_id) REFERENCES figure(id),
    PRIMARY KEY (name, figure_id)
);
            

''')

con.close()