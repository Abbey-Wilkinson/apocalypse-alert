export default function HeatMap() {
    const weather = require("../images/world-map.gif")
    return (
        <div class="heatmap">
            <img src={weather} />
        </div>
    )
}