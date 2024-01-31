import Navbar from '../components/Navbar';
import Filters from '../components/Filters';
import HeatMap from '../components/HeatMap';
import Weather from '../components/Weather';

export default function Home() {
    return (
    <div className="fullscreen">
      <Navbar />
      <main>
        <Filters />
        <div className="heatmap-and-weather">
          <HeatMap />
          <Weather />
        </div>
      </main>
    </div>
  );
}