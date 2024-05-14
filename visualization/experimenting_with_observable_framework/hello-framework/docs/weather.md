# local weather forecast

```js
const forecast = FileAttachment("./data/forecast.json").json()
```

```js
display(Inputs.table(forecast.properties.periods))
```