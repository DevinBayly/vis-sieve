const longitude = -144.77;
const latitude = 64.83

async function json(url) {
    const response = await fetch(url)
    if (!response.ok) throw new Error(`fetch failed:${response.status}`)
    return await response.json()
}

const station = await json(`https://api.weather.gov/points/${latitude},${longitude}`)

const forecast = await json(station.properties.forecastHourly)

process.stdout.write(JSON.stringify(forecast))

