import sys
import os
import duckdb
import argparse
from pathlib import Path
from playwright.async_api import Playwright, async_playwright, expect
import asyncio

async def grab_pdf(oa_url, destination, playwright) -> bool:
    browser = await playwright.chromium.launch_persistent_context(
        '/tmp/playwright',
        accept_downloads=True, 
        headless=True, 
        slow_mo=1000)
    browser.set_default_timeout(10000)
    page = await browser.new_page()

    try:
        async with page.expect_download() as download_info:
            try:
                await page.goto(oa_url, timeout=0)
            except:
                print("Saving file to ", destination)
                # Wait for the download to start
                download = await download_info.value
                # Wait for the download process to complete
                print(await download.path())
                # Save downloaded file somewhere
                await download.save_as(
                    str(destination)
                )
                # await download.save_as(os.path.join(downloads_path, file_name))
            await page.wait_for_timeout(200)
            return True
    except Exception as e:
        return False
        
def strip_figures(pdf_path, output_dir):
    os.system('pdfimages ' + pdf_path + ' ' + output_dir)
    #os.system('cd ' + output_dir + ' && rm ./*.ppm -f && rm ./*.pbm -f')
    return

def get_figures(pdf_dir_path, output_dir):
    #TODO replace the os.path stuff with Path
    for subfolder in os.listdir(pdf_dir_path)[:500]:
        subfolder_path = os.path.join(pdf_dir_path, subfolder)
        pdf_path = os.path.join(subfolder_path, os.listdir(subfolder_path)[0])
        print(pdf_path)

        sub_out_dir = os.path.join(output_dir, subfolder)
        if not os.path.exists(sub_out_dir):
            os.makedirs(sub_out_dir)
        
        strip_figures(pdf_path, sub_out_dir+'/')
async def main():
    # use argparse to get information about the pdf we are gathering 
    # just a work id, and a publications.db file should be enough
    parser = argparse.ArgumentParser()
    parser.add_argument("pub_id")
    parser.add_argument("database")
    args = parser.parse_args()
    db_path = Path(args.database)
    con = duckdb.connect(str(db_path))
    id = int(args.pub_id)
    # make the content parent folder
    content_root_path = Path("content")
    content_root_path.mkdir(exist_ok=True)
    async with async_playwright() as playwright:
        pub_folder = Path(f"{content_root_path}/{pub_id}")
        pub_folder.mkdir(exist_ok=True)
        pdf_path = Path(f"{pub_folder}/{pub_id}.pdf")
        pub_oa_url = con.sql(f"SELECT * from paper where paper.id = {pub_id}")
        pdf_grab_result = await grab_pdf(pub_oa_url, pdf_path, playwright)
        # now perform the duckdb updates
if __name__ == '__main__':
    asyncio.run(main())


    # create a playwright instance
    # run the get_pdf system
    #get_figures(sys.argv[1], sys.argv[2])