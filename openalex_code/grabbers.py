import sys
import os

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
                    destination
                )
                # await download.save_as(os.path.join(downloads_path, file_name))
            await page.wait_for_timeout(200)
            return True
    except Exception as e:
        return False
        
def strip_figures(pdf_path, output_dir):
    os.system('pdfimages -j ' + pdf_path + ' ' + output_dir)
    os.system('cd ' + output_dir + ' && rm ./*.ppm -f && rm ./*.pbm -f')
    return

def get_figures(pdf_dir_path, output_dir):
    for subfolder in os.listdir(pdf_dir_path)[:500]:
        subfolder_path = os.path.join(pdf_dir_path, subfolder)
        pdf_path = os.path.join(subfolder_path, os.listdir(subfolder_path)[0])
        print(pdf_path)

        sub_out_dir = os.path.join(output_dir, subfolder)
        if not os.path.exists(sub_out_dir):
            os.makedirs(sub_out_dir)
        
        strip_figures(pdf_path, sub_out_dir+'/')

if __name__ == '__main__':
    get_figures(sys.argv[1], sys.argv[2])