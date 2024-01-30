export default function WeatherTile () {
    const weather = require("../images/weather.avif")
    return (
        <div className="weather-tile">
            <img src={weather}/>
            <h3>United Kingdom</h3>
            <h4>Good Weather</h4>
        </div>
    )
}