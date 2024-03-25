import asyncio
import random
import json
import os
from pathlib import Path
from playwright.async_api import Playwright, async_playwright, expect
import uuid
import time
import argparse
## set this script up to use a json file following Carolina's format
parser = argparse.ArgumentParser()
parser.add_argument("json")
args = parser.parse_args()
json_data = json.loads(Path(args.json).read_text())
# get the oa_urls from this

out = Path("pdfs")
out.mkdir(exist_ok=True)
user_dir = Path(f"{out}/userdir")
user_dir.mkdir(exist_ok =True)
downloads_path = Path(f"{out}/downloads")
downloads_path.mkdir(exist_ok=True)
async def run(playwright: Playwright) -> None:
  authors = list(json_data.keys())
  browser = await playwright.chromium.launch_persistent_context(str(user_dir), accept_downloads=True, headless=True, slow_mo=1000)
  browser.set_default_timeout(10000)
  page = await browser.new_page()

  for author in authors:
    works = json_data[author]
    # remove the spaces between so we can save file names
    author_name_clean = author.replace(" ","_")
    # for browser_type in [p.chromium, p.firefox, p.webkit]:

    # Start waiting for the download
    lim = 6
    ## while debugging randomly sample to see waht works
    if len(works) ==0:
      continue
    if lim > len(works):
      lim=len(works)
    works = random.sample(works,lim)
    for work in works:
      file_name = work["open_access"]["oa_url"]
      work_id = work["(work_)id"].split("/")[-1]
      if not file_name:
        continue
      ## apparently some pages don't have a download event?
      try:
        async with page.expect_download() as download_info:
            try:
                await page.goto(file_name, timeout= 0)
            except:
                print("Saving file to ", downloads_path, file_name)
                # Wait for the download to start
                download = await download_info.value
                # Wait for the download process to complete
                print(await download.path())
                # Save downloaded file somewhere
                await download.save_as(f"{downloads_path}/{author_name_clean}/{work_id}")
                #await download.save_as(os.path.join(downloads_path, file_name))
            await page.wait_for_timeout(200)
      except Exception as e:
        print("failed,", author,work_id)

  await browser.close()

          # await page.screenshot(path=f'example-{browser_type.name}.png',full_page=True)
          # await browser.close()




async def main() -> None:
    async with async_playwright() as playwright:
        await run(playwright)

asyncio.run(main())

