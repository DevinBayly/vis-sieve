# Summary of directory contents

This script `get_pdf.py` is responsible for collecting the pdf that lies at the link or links within the `links` variable.

Honestly most of the script is a bit of a mystery to me, but can be looked at where I sourced it at https://stackoverflow.com/questions/68409249/how-to-download-pdf-files-with-playwright-python 

## Installation of playwright

The playwright program lets us perform the scrapes of pdfs that wget and curl would normally fail for

```
pip install pytest-playwright
playwright install
playwright install-deps
```

This is probably the main reason we want playwright, it simplifies the installation of the headless browsers that we need to use to download the pdfs.

## Next steps

After the pdfs have been collected then it's time to dump the figures from the pdf. `pdfimages` [https://en.wikipedia.org/wiki/Pdfimages](https://en.wikipedia.org/wiki/Pdfimages) is a great utility for this. 