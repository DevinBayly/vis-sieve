"""
file: hear_me_ROR_script.py
author: Ben Kruse
Adapted from: hear_me_ROR.ipynb by Devin Bayly

Takes a ROR identification of school and a range of years,
then generates a json file with the publications of the school
for that period
"""

import os
import requests as rq
import json
import argparse
from tqdm import tqdm
import math
import duckdb as db
from grabbers import strip_figures, grab_pdf
from playwright.async_api import Playwright, async_playwright, expect
import asyncio

def remove_duplicate_authors(publications, silent=False):
    """ Removes duplicate authors from a list of publications

    Args:
        publications (list): list of publications to remove duplicate authors from

    Returns:
        list: list of publications with duplicate authors removed
    """
    for pub in publications:
        authors = pub["authorships"]
        seen_ids = set()
        new_authors = []
        for a in authors:
            if a["author"]["id"] not in seen_ids:
                new_authors.append(a)
                seen_ids.add(a["author"]["id"])
            else: 
                print(f"Duplicate author in {pub['title']}: {a['author']['display_name']}")
        pub["authorships"] = new_authors
    return publications

def results_per_year(year, ror="03m2x1q45", silent=False, filter_duplicate_authors=True, testing=False):
    """ Gets the publications for a school for a year

    Args:
        year (int): year to get publications for
        ror (str): ROR identification of the school

    Returns:
        list: list of publications for the school for the year
    """
    all_res = []
    headers = {"mailto":"baylyd@arizona.edu"} ## Make command line arg
    res = rq.get(f"https://api.openalex.org/works?filter=publication_year:{year},institutions.ror:{ror}&cursor=*&per-page=200",headers=headers)
    data = res.json()
    if filter_duplicate_authors:
        data["results"] = remove_duplicate_authors(data["results"], silent=silent)
    page_count = data["meta"]["count"]/data["meta"]["per_page"]
    all_res.extend(data["results"])
    cursor = data["meta"]["next_cursor"]
    query = 0
    if not silent:
        pbar = tqdm(total=math.ceil(page_count))
    while cursor:
        query+=1
        res = rq.get(f"https://api.openalex.org/works?filter=publication_year:{year},institutions.ror:{ror}&cursor={cursor}&per-page=200")
        
        # Sometimes request fails, leave the year (find better way)
        try:
            data = res.json()
        except json.decoder.JSONDecodeError:
            print(f"Error on query {query}")
            print(res.text)
            break

        if filter_duplicate_authors:
            data["results"] = remove_duplicate_authors(data["results"], silent=silent)
        all_res.extend(data["results"])
        cursor = data["meta"].get("next_cursor",None)
        if not silent:
            pbar.update(1)
        if testing:
            break
    return all_res

def get_publications(ror: str, years: range, output_file: str, silent=False, get_authors=False):
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

    if get_authors:
        if not silent:
            print("Getting authors")
        with open("authors"+output_file,"w") as f:
            json.dump(get_all_authors(all_res, output_file), f)
        

def get_all_authors(publications, output_file):
    """ Gets the authors from a list of publications

    Args:
        publications (list): list of publications to get authors from

    Returns:
        list: list of authors from the publications
    """
    authors = {}
    author_ids = {}
    for pub in publications:
        for a in pub["authorships"]:
            publication = {"(work_)id": pub["id"], 
                           "author": {"id": a["author"]["id"], 
                                      "display_name": a["author"]["display_name"], 
                                      "orcid": a["author"]["orcid"]
                                      },
                            "open_access": pub["open_access"]
                            }
            if a["author"]["id"] not in author_ids:
                pub_array = [publication]
                author_ids[a["author"]["id"]] = pub_array
                authors[a["author"]["display_name"]] = pub_array
            else:
                author_ids[a["author"]["id"]].append(publication)

    return authors


def add_institution_to_db(con: db.DuckDBPyConnection, institution_ror: str = None, 
                          institution_name: str = None, institution_id: int = None) -> int:
    """ Adds an institution to the database

    Args:
        con (db.DuckDBPyConnection): connection to the database
        institution_roi (str): ROR identification of the institution

    Returns:
        int: id of the institution
    """

    if institution_ror is not None:
        institution_info = rq.get(f"https://api.openalex.org/institutions/https://ror.org/{institution_ror}").json()
        institution_name = institution_name or institution_info["display_name"]
        institution_id = institution_id or int(institution_info["id"].split("I")[-1])

    elif institution_id is not None:
        con.execute(f"SELECT COUNT(1) FROM institution WHERE id = {institution_id};")
        exists = con.fetchone()[0]
        if exists:
            pass
            return institution_id
        
        institution_info = rq.get(f"https://api.openalex.org/institutions/I{institution_id}").json()
        institution_name = institution_name or institution_info["display_name"]
        institution_ror = institution_ror or institution_info["ror"].split("/")[-1]
        
    institution_name = institution_name.replace("'", "")
    try:
        con.execute(f"INSERT INTO institution VALUES ({institution_id}, '{institution_ror}', '{institution_name}');")
    except db.ConstraintException:
        pass

    return institution_id
    
def populate_database(database_file: str, ror: str, years: range, content_root: str,
                      json_output: str = None, silent: bool = False) -> None:
    """ Populates a database with publications for a school for a range of years

    Args:
        database_file (str): name of the database file to populate
        ror (str): ROR identification of the school
        years (range): range of years to get publications for
        json_output (str): name of the json file to write the publications to
        silent (bool): silence output
    """
    con = db.connect(database_file)
    inst_id = add_institution_to_db(con, institution_ror=ror)

    for year in years:
        if not silent:
            print(f"Getting publications for {year}, database version")
        publications = results_per_year(year, ror, silent,testing=True)
        print("processing publications")
        for pub in tqdm(publications):

            # Add publication to database
            #await add_publication_and_figures(con, pub, content_root, playwright)
            # TODO wrap these publication table lines in a function
            
            pub_date = pub["publication_date"]
            pub_id = int(pub["id"].split("W")[-1])
            pub_title = pub["title"][:200].replace("'", "")
            pub_doi = pub["doi"]
            pub_oa_url = pub["open_access"]["oa_url"]
            pub_oa_status = pub["open_access"]["oa_status"]
            # this section is checking for whether the table has the paper in it already
            con.execute(f"SELECT COUNT(1) FROM paper WHERE id = {pub_id};")
            exists = con.fetchone()[0]
            
            print("overriding the existence check ")
            input("proceed?")
            #if exists:
            #    # want to continue to the next publication and not try to update either paper table, or the authorship tables, because this has already happened
            #    continue

                # want to modify the paper table
                con.execute(f"""INSERT INTO paper (id, title, doi, publication_date, oa_url,grabbed) VALUES ({pub_id}, '{pub_title}', '{pub_doi}', '{pub_date}', '{pub_oa_url}','false');""")
                for a in pub["authorships"]:
                    try:
                        con.execute(f"""INSERT INTO author VALUES ({a['author']['id'].split('A')[-1]}, '{a['author']['display_name'].replace("'", "")}');""")
                    except db.ConstraintException:
                        pass
                        continue

                    try:
                        con.execute(f"INSERT INTO contribution VALUES ({a['author']['id'].split('A')[-1]}, {pub['id'].split('W')[-1]});")
                    except db.ConstraintException:
                        pass
                    
                    for author_inst in a["institutions"]:
                        add_institution_to_db(con, institution_id=int(author_inst["id"].split("I")[-1]))
                        try:
                            con.execute(f"INSERT INTO residence VALUES ({a['author']['id'].split('A')[-1]}, {author_inst['id'].split('I')[-1]});")
                        except db.ConstraintException:
                            pass




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get publications for a school")
    parser.add_argument("first_year", help="First year to get publications for")
    parser.add_argument("last_year", help="Last year to get publications for")
    parser.add_argument("--ror", help="ROR of the school (UofA by default)", default="03m2x1q45")
    parser.add_argument("--output", help="Output file name", default="hear_me_ROR_out.json")
    parser.add_argument("-a", "--get_authors", help="Get authors as well as publications", action="store_true")
    parser.add_argument("-s", "--silent", help="Silence output", action="store_true")
    parser.add_argument("--database", help="Database file to store publications in")
    parser.add_argument("--content_root", help="Root directory for content")
    args = parser.parse_args()
    
    if args.database:
        asyncio.run(populate_database(args.database, args.ror, range(int(args.first_year), int(args.last_year)+1), args.content_root, args.output, args.silent))
    else:
        get_publications(args.ror, range(int(args.first_year), int(args.last_year)+1), args.output, args.silent, args.get_authors)
    

