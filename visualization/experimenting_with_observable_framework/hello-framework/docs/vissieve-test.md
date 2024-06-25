---
title: Vis Sieve Exploring publications
sql:
    p: penguins.csv
    author: ./data/author.csv
    institution: ./data/institution.csv
    figure: ./data/figure.csv
    pub: ./data/pub_scratch.db
    recentpub: ./data/publications_ua.db
    princetonpub: ./data/publications_princeton.db

---


<style>

.hero {
  display: flex;
  flex-direction: column;
  align-items: center;
  font-family: var(--sans-serif);
  margin: 4rem 0 8rem;
  text-wrap: balance;
  text-align: center;
}

.hero h1 {
  margin: 2rem 0;
  max-width: none;
  font-size: 14vw;
  font-weight: 900;
  line-height: 1;
  background: linear-gradient(30deg, var(--theme-foreground-focus), currentColor);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero h2 {
  margin: 0;
  max-width: 34em;
  font-size: 20px;
  font-style: initial;
  font-weight: 500;
  line-height: 1.5;
  color: var(--theme-foreground-muted);
}

@media (min-width: 640px) {
  .hero h1 {
    font-size: 90px;
  }
}

</style>
<div class="hero">
  <h1>Hello, Visualization Explorers</h1>
  <h2>Welcome to your new project! Edit&nbsp;<code style="font-size: 90%;">docs/index.md</code> to change this page.</h2>
  <a href="https://observablehq.com/framework/getting-started">Get started<span style="display: inline-block; margin-left: 0.25rem;">↗︎</span></a>
</div>

Note, if we wanted to we could look at https://talk.observablehq.com/t/loading-a-duckdb-database/8977/3


```sql
SELECT * FROM p LIMIT 10
```



```sql
SELECT * FROM pub.author LIMIT 10
```



```sql
SELECT * FROM pub.institution LIMIT 10
```



```sql
SELECT * FROM pub.paper LIMIT 10
```

```sql
SELECT * from recentpub.paper LIMIT 10
```

```sql
SELECT COUNT(*) from recentpub.paper
```


Also beneath here is the actual listing of the number of figures that we have from the 2022 parsing of the pdfs from princeton
```sql
SELECT COUNT(*) from princetonpub.figure
```
These are all up in cyverse publically available
```sql id=figure_urls
SELECT server_path as url from princetonpub.figure LIMIT 40
```

```js
Inputs.table(figure_urls)
```

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
