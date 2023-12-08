# Summary directory contents

This folder contains a few different ipynb notebooks. They are mostly concerning a search through openalex to find the number of publications by the cluster users. They do however show how to work with openalex from python

Main notebook of interest is `hear_me_ROR.ipynb` which shows how to get the total publications for an institution in a year, and does this for 6 years. The name ROR is an institutional identifier that exists outside of openalex and is a robust method of connecting to works and authors from an instution. 

The goal would be to expand on this result by the material that's written in the digital humanities notebook to gather the oa_access urls

## Dependencies

To install and run these notebooks the following dependencies should be installed

```
pip install jupyter bs4
```