import duckdb
import json
export_data = json.load(open("./project-1-at-2024-06-11-16-19-61e1c2aa.json"))
con = duckdb.connect("publications.db")
con.sql("""CREATE TABLE examples AS
    SELECT *
    FROM read_json_auto('export.json');
""")

print(con.sql("SELECT * FROM examples LIMIT 10"))