import duckdb as db
import pandas as pd

con = db.connect('publications.db')
con.execute('SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES')
names = con.fetchall()
print(names)

for table in names:
    df = con.table(table[0]).to_df()
    df.to_csv(f'database_csvs/{table[0]}.csv', index=False)
