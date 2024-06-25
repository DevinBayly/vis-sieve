---
title: Vis Sieve figure retrieval demo
sql:
    princetonpub: ./data/publications_princeton.db

---
## Demo explanation

This document shows how to load and retrieve images from the princeton duckdb file

## Demonstration of queries
Also beneath here is the actual listing of the number of figures that we have from the 2022 parsing of the pdfs from princeton
```sql id=total display
SELECT COUNT(*) as total_figs from princetonpub.figure
```
That's right,  ${total}  available

These are all up in cyverse with their pdf publication id associated
```sql id=figure_urls
SELECT server_path as url from princetonpub.figure LIMIT 40
```

```js
Inputs.table(figure_urls)
```
## Demonstration of plotting using query results
Following in the footsteps of the image scatter plot from here https://observablehq.com/@observablehq/plot-image-scatterplot

```js
Plot.plot({
  inset:40,
  y: {axis:null},
  x:{axis:null},
  width:800,
  marks: [
    Plot.image(figure_urls, {
      x: (d,i)=> i%8,
      y: (d,i) => Math.floor(i/8),
      src: "url",
      width: 80,
    })
  ]
})

```
