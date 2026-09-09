import { useEffect, useState } from "react";
import { StationSidebar } from "./components/StationSidebar";
import { DashboardStats } from "./components/DashboardStats";
import { SensorChart } from "./components/SensorChart";
import { AnomalyFeed } from "./components/AnomalyFeed";
import { AdvancedMap } from "./components/ui/interactive-map";
import { SonicWaveformCanvas } from "./components/ui/sonic-waveform";
import { useStations, useReadings, useAnomalies } from "./hooks/useStationData";
import { MapPin, RefreshCw, AlertCircle, Map as MapIcon } from "lucide-react";

// Real geographic coordinates for Automatic Weather Stations
const STATION_DETAILS: Record<
  string,
  {
    lat: number;
    lng: number;
    city: string;
    state: string;
    color: string;
  }
> = {
  "AWS-001": {
    lat: 11.0168,
    lng: 76.9558,
    city: "Coimbatore",
    state: "Tamil Nadu",
    color: "#2dd4bf", // Teal
  },
  "AWS-002": {
    lat: 13.0827,
    lng: 80.2707,
    city: "Chennai",
    state: "Tamil Nadu",
    color: "#38bdf8", // Sky Blue
  },
  "AWS-003": {
    lat: 12.9716,
    lng: 77.5946,
    city: "Bengaluru",
    state: "Karnataka",
    color: "#a855f7", // Purple
  },
};

export default function App() {
  const [selectedStationId, setSelectedStationId] = useState<string | null>(null);
  const [currentTime, setCurrentTime] = useState<string>("");
  const [showMap, setShowMap] = useState<boolean>(true);

  const stationsQuery = useStations();
  const stations = stationsQuery.data ?? [];

  // Update clock
  useEffect(() => {
    const update = () => {
      setCurrentTime(
        new Date().toLocaleTimeString(undefined, { hour: "2-digit", minute: "2-digit", second: "2-digit" })
      );
    };
    update();
    const interval = setInterval(update, 1000);
    return () => clearInterval(interval);
  }, []);

  // Auto-select the first station once the list loads
  useEffect(() => {
    if (!selectedStationId && stations.length > 0) {
      setSelectedStationId(stations[0].id);
    }
  }, [stations, selectedStationId]);

  const readingsQuery = useReadings(selectedStationId, 24);
  const readings = readingsQuery.data ?? [];

  const allAnomaliesQuery = useAnomalies(null, 100);
  const stationAnomaliesQuery = useAnomalies(selectedStationId, 50);

  const selectedStation = stations.find((s) => s.id === selectedStationId);

  // Compute map center dynamically based on selected station
  const currentCoords =
    selectedStationId && STATION_DETAILS[selectedStationId]
      ? ([STATION_DETAILS[selectedStationId].lat, STATION_DETAILS[selectedStationId].lng] as [number, number])
      : ([11.0168, 76.9558] as [number, number]);

  // Build map markers for all stations in fleet
  const unresolvedByStation = new Set(
    (allAnomaliesQuery.data ?? []).filter((a) => !a.resolved).map((a) => a.station_id)
  );

  const mapMarkers = stations.map((st) => {
    const details = STATION_DETAILS[st.id] || { lat: 11.0168, lng: 76.9558, city: st.name };
    const hasAnomaly = unresolvedByStation.has(st.id);
    return {
      id: st.id,
      position: [details.lat, details.lng] as [number, number],
      color: hasAnomaly ? "red" : "green",
      size: (st.id === selectedStationId ? "large" : "medium") as "small" | "medium" | "large",
      popup: {
        title: `${st.id} — ${st.name}`,
        content: `Location: ${st.location}. Operational Status: ${
          hasAnomaly ? "⚠️ Unresolved Anomaly Flagged" : "✓ Nominal Operational Status"
        }.`,
      },
    };
  });

  // Build neat circular station coverage zones (8 km radius)
  const stationCircles = Object.entries(STATION_DETAILS).map(([stId, details]) => {
    const isSelected = stId === selectedStationId;
    const hasAnomaly = unresolvedByStation.has(stId);
    return {
      id: stId,
      center: [details.lat, details.lng] as [number, number],
      radius: 8000,
      style: {
        color: hasAnomaly ? "#f59e0b" : isSelected ? "#2dd4bf" : "#38bdf8",
        weight: isSelected ? 2.5 : 1.5,
        fillColor: hasAnomaly ? "#f59e0b" : isSelected ? "#2dd4bf" : "#38bdf8",
        fillOpacity: isSelected ? 0.12 : 0.04,
      },
      popup: `${details.city} AWS Telemetry Zone (${stId})`,
    };
  });

  return (
    <div className="h-screen flex bg-bg text-text overflow-hidden font-sans select-none relative">
      {/* Background Animated Green Sonic Waveform Canvas */}
      <SonicWaveformCanvas />

      {/* Sidebar Navigation */}
      <StationSidebar
        stations={stations}
        anomalies={allAnomaliesQuery.data ?? []}
        selectedId={selectedStationId}
        onSelect={setSelectedStationId}
        isLoading={stationsQuery.isLoading}
        isError={stationsQuery.isError}
      />

      {/* Main Content Workspace */}
      <div className="flex-1 flex flex-col min-w-0 h-full overflow-hidden relative z-10">
        {/* Top Navigation Header */}
        <header className="px-6 py-4 border-b border-white/10 bg-[#0e1017]/80 backdrop-blur-2xl flex items-center justify-between shrink-0">
          <div>
            <div className="flex items-center gap-3">
              <h1 className="font-display text-lg font-bold tracking-tight text-text">
                {selectedStation ? selectedStation.name : "AWS Anomaly Detection System"}
              </h1>
              {selectedStation && (
                <span className="font-mono text-xs font-semibold px-2.5 py-0.5 rounded-full bg-indigo-500/10 text-indigo-300 border border-indigo-500/30">
                  {selectedStation.id}
                </span>
              )}
            </div>
            <div className="text-xs text-muted flex items-center gap-2 mt-1">
              <MapPin className="w-3.5 h-3.5 text-indigo-400" />
              <span>{selectedStation ? selectedStation.location : "Select a weather station from the fleet sidebar"}</span>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <button
              onClick={() => setShowMap(!showMap)}
              className={`px-3 py-1.5 rounded-xl border text-xs font-medium transition-all cursor-pointer flex items-center gap-1.5 ${
                showMap
                  ? "bg-indigo-500/15 border-indigo-500/40 text-indigo-300 shadow-sm"
                  : "bg-white/5 border-white/10 text-slate-300 hover:bg-white/10"
              }`}
            >
              <MapIcon className="w-3.5 h-3.5" />
              <span>{showMap ? "Hide Map" : "Show Map"}</span>
            </button>

            <div className="hidden sm:flex items-center gap-2 font-mono text-xs text-muted bg-white/5 backdrop-blur-md px-3 py-1.5 rounded-xl border border-white/10">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
              <span>UTC {currentTime}</span>
            </div>

            <button
              onClick={() => {
                readingsQuery.refetch();
                stationAnomaliesQuery.refetch();
                allAnomaliesQuery.refetch();
              }}
              className="px-3 py-1.5 rounded-xl bg-white/5 hover:bg-white/10 border border-white/10 text-xs font-medium text-slate-200 transition-all flex items-center gap-1.5 cursor-pointer"
              title="Refresh telemetry feed"
            >
              <RefreshCw className={`w-3.5 h-3.5 ${readingsQuery.isFetching ? "animate-spin text-indigo-400" : ""}`} />
              <span>Refresh</span>
            </button>
          </div>
        </header>

        {/* Dashboard Workspace Grid */}
        <div className="flex-1 flex min-h-0">
          <main className="flex-1 min-w-0 overflow-y-auto p-6 flex flex-col gap-5">
            {!selectedStationId ? (
              <div className="flex items-center justify-center h-64 text-sm text-muted">
                {stationsQuery.isLoading ? "Loading stations..." : "No station selected."}
              </div>
            ) : (
              <>
                {/* Metric Summary Cards */}
                <DashboardStats
                  station={selectedStation}
                  readings={readings}
                  anomalies={stationAnomaliesQuery.data ?? []}
                />

                {/* Interactive Leaflet Map Component */}
                {showMap && (
                  <div className="glass-liquid p-4 flex flex-col gap-3">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-2">
                        <MapIcon className="w-4 h-4 text-indigo-400" />
                        <h3 className="font-display text-xs font-bold uppercase tracking-wider text-text">
                          Station Region Map — {selectedStation?.name}
                        </h3>
                      </div>
                      <div className="flex items-center gap-2 text-xs font-mono text-muted">
                        <span>Lat: {currentCoords[0]}</span>
                        <span>•</span>
                        <span>Lng: {currentCoords[1]}</span>
                      </div>
                    </div>

                    <AdvancedMap
                      center={currentCoords}
                      zoom={12}
                      markers={mapMarkers}
                      circles={stationCircles}
                      onMarkerClick={(m) => {
                        if (m.id) setSelectedStationId(m.id.toString());
                      }}
                      style={{ height: "290px", width: "100%" }}
                    />
                  </div>
                )}

                {/* Error Banner */}
                {readingsQuery.isError && (
                  <div className="rounded-2xl border border-red-500/40 bg-red-500/10 backdrop-blur-xl p-4 text-xs text-red-400 flex items-center gap-3">
                    <AlertCircle className="w-4 h-4 shrink-0" />
                    <span>Couldn't load sensor readings. Confirm the FastAPI backend server is running on port 8000.</span>
                  </div>
                )}

                {/* Sensor Telemetry Grid */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <SensorChart title="Temperature" unit="°C" dataKey="temperature" readings={readings} color="#e11d48" />
                  <SensorChart title="Humidity" unit="%" dataKey="humidity" readings={readings} color="#38bdf8" />
                  <SensorChart title="Pressure" unit="hPa" dataKey="pressure" readings={readings} color="#d97706" />
                  <SensorChart title="Wind speed" unit="m/s" dataKey="wind_speed" readings={readings} color="#10b981" />
                </div>
              </>
            )}
          </main>

          {/* Anomaly Stream Side Panel */}
          <AnomalyFeed
            anomalies={stationAnomaliesQuery.data ?? []}
            isLoading={stationAnomaliesQuery.isLoading}
            isError={stationAnomaliesQuery.isError}
          />
        </div>
      </div>
    </div>
  );
}
