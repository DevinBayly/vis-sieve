import subprocess as sp
import logging
from pathlib import Path
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("offset")
parser.add_argument("pdfs_per_task")
parser.add_argument("tasks_total")
parser.add_argument("database")
args = parser.parse_args()
logger = logging.getLogger(__name__)

logging.basicConfig(filename='myapp.log', level=logging.INFO)
offset = int(args.offset)
number_pdfs_per_task = int(args.pdfs_per_task)
tasks = int(args.tasks_total)
database = args.database
for i in range(tasks):
  row_start =i*number_pdfs_per_task + offset
  row_end = (i+1)*number_pdfs_per_task + offset
  sp.run(f"sbatch -A visteam -n 1 -t 1:00:00 -o slurm_out/%j_{i}_{row_start}_{row_end}_slurm.out -J pdf_gatherer_{i} -p standard coordinator.sh {row_start} {row_end} {database}".split(" "))
  #add information about this 

logger.info(f'{args} {row_end}')
