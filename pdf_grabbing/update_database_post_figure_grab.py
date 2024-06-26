from pathlib import Path
import tqdm
import duckdb as db

connection = db.connect("publications_princeton.db")

# for each pdf that we have actual figures for we will create a bunch of entries 

# follows the logic here https://vissieve.github.io/main/documentation/site/database/database_information/

figures = sorted(Path("Princeton_content").glob("*/Figure*.png"))
for i,figure in tqdm.tqdm(enumerate(figures)):
  paper_id = int(figure.parent.name)
  try:
     connection.execute(f"""INSERT INTO figure VALUES ({i}, {paper_id}, '{figure}','https://data.cyverse.org/dav-anon/iplant/home/carolinarr/vis-sieve/{figure}');""")
  except db.ConstraintException:
      pass
      continue




