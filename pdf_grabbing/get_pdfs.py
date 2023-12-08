import asyncio
import os
from pathlib import Path
from playwright.async_api import Playwright, async_playwright, expect
import uuid
import time
links = ['https://goldschmidtabstracts.info/2021/6756.pdf']

out = Path("pdfs")
out.mkdir(exist_ok=True)
user_dir = Path(f"{out}/userdir")
user_dir.mkdir(exist_ok =True)
downloads_path = Path(f"{out}/downloads")
downloads_path.mkdir(exist_ok=True)
async def run(playwright: Playwright) -> None:
    # for browser_type in [p.chromium, p.firefox, p.webkit]:
    browser = await playwright.chromium.launch_persistent_context(str(user_dir), accept_downloads=True, headless=True, slow_mo=1000)
    browser.set_default_timeout(10000)
    page = await browser.new_page()

    # Start waiting for the download
    file_name = links[0]
    async with page.expect_download() as download_info:
        try:
            await page.goto(links[0], timeout= 0)
        except:
            print("Saving file to ", downloads_path, file_name)
            # Wait for the download to start
            download = await download_info.value
            # Wait for the download process to complete
            print(await download.path())
            # Save downloaded file somewhere
            await download.save_as(os.path.join(downloads_path, file_name))
        await page.wait_for_timeout(200)

    await browser.close()

            # await page.screenshot(path=f'example-{browser_type.name}.png',full_page=True)
            # await browser.close()

async def main() -> None:
    async with async_playwright() as playwright:
        await run(playwright)

asyncio.run(main())


