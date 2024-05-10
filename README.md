# Vis-Seive




This project aims to enable visualization service providers/facilitators to get a sense of the kinds of visualizations that are being produced by their institution as a whole. This provides a range of benefits
*  Informed Facility Development 
* Trend tracking
* Technique discovery/development
* Service catalog entry inspiration

The overall project covers
* the gathering of publication information
* the retrieval of open access pdfs
* the scraping of figures from pdfs
* the aggregation of figures into a largescale mosaic grouped by field and style


## Members

* Carolina Roe-Raymond
* Devin Bayly
* Ben Kruse


## Label studio
### Setting up
Install it with pip
```bash
pip install label-studio
```

For locally hosted files, set the following environment variables. Note: this
assumes you are in the vis-siev directory, otherwise set the LOCAL_FILES_DOCUMENT_ROOT to whatevers one above your content folder.
```bash
export LOCAL_FILES_SERVING_ENABLED=true
export LABEL_STUDIO_LOCAL_FILES_DOCUMENT_ROOT=$(pwd)/database
```

Then run the server
```bash
label-studio
```

### Creating a new project
Go the local host address label studio gives you after the last step.

Create a new project, adding the template code. Don't import the data here, 
well do that later.

### Importing data
Go to `settings->cloud storage->Add Source Storage` then select `Local Files` as the storage type. For `absolute local path`, put the absolute path to the database folder (for me: /home/benk/Documents/datavis/vis-sieve/database/content). Set the regex filter to `.*jpg` and enable `Treat every bucket object
as a source file`. Then click `Add Storage` (or check the connection first).

This sets up the source, to actually bring in the data, click sync storage in
the cloud storage tab (this may take a second).
