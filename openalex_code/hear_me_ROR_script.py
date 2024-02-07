"""
file: hear_me_ROR_script.py
author: Ben Kruse
Adapted from: hear_me_ROR.ipynb by Devin Bayly

Takes a ROR identification of school and a range of years,
then generates a json file with the publications of the school
for that period
"""

import requests as rq
import json
import argparse
from tqdm import tqdm
import math

def results_per_year(year, ror="03m2x1q45", silent=False):
    """ Gets the publications for a school for a year

    Args:
        year (int): year to get publications for
        ror (str): ROR identification of the school

    Returns:
        list: list of publications for the school for the year
    """
    all_res = []
    headers = {"mailto":"baylyd@arizona.edu"}
    res = rq.get(f"https://api.openalex.org/works?filter=publication_year:{year},institutions.ror:{ror}&cursor=*&per-page=200",headers=headers)
    data = res.json()
    page_count = data["meta"]["count"]/data["meta"]["per_page"]
    all_res.extend(data["results"])
    cursor = data["meta"]["next_cursor"]
    query =1
    if not silent:
        pbar = tqdm(total=math.ceil(page_count))
    while cursor:
        res = rq.get(f"https://api.openalex.org/works?filter=publication_year:{year},institutions.ror:{ror}&cursor={cursor}&per-page=200")
        data = res.json()
        all_res.extend(data["results"])
        cursor = data["meta"].get("next_cursor",None)
        query+=1
        if not silent:
            pbar.update(1)
    return all_res

def get_publications(ror: str, years: range, output_file: str, silent=False):
    """ Gets the publications for a school for a range of years and 
    writes them to a json file

    Args:
        ror (str): ROR identification of the school
        years (range): range of years to get publications for
    
    Returns:
        None
    """
    all_res = []
    for year in years:
        if not silent:
            print(f"Getting publications for {year}")
        all_res.extend(results_per_year(year, ror, silent))
    with open(output_file,"w") as f:
        json.dump(all_res,f)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get publications for a school")
    parser.add_argument("first_year", help="First year to get publications for")
    parser.add_argument("last_year", help="Last year to get publications for")
    parser.add_argument("--ror", help="ROR of the school (UofA by default)", default="03m2x1q45")
    parser.add_argument("--output", help="Output file name", default="hear_me_ROR_out.json")
    parser.add_argument("-s", "--silent", help="Silence output", action="store_true")
    args = parser.parse_args()

    get_publications(args.ror, range(int(args.first_year), int(args.last_year)+1), args.output, args.silent)