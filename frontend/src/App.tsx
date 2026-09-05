import { useEffect, useState } from "react";
import { StationSidebar } from "./components/StationSidebar";
import { DashboardStats } from "./components/DashboardStats";
import { SensorChart } from "./components/SensorChart";
import { AnomalyFeed } from "./components/AnomalyFeed";
import { useStations, useReadings, useAnomalies } from "./hooks/useStationData";

export default function App() {
  const [selectedStationId, setSelectedStationId] = useState<string | null>(null);

  const stationsQuery = useStations();
  const stations = stationsQuery.data ?? [];

  // auto-select the first station once the list loads
  useEffect(() => {
    if (!selectedStationId && stations.length > 0) {
      setSelectedStationId(stations[0].id);
    }
  }, [stations, selectedStationId]);

  const readingsQuery = useReadings(selectedStationId, 24);
  const readings = readingsQuery.data ?? [];

  // sidebar/feed both need to know about anomalies across stations (for status dots) and for the selected one
  const allAnomaliesQuery = useAnomalies(null, 100);
  const stationAnomaliesQuery = useAnomalies(selectedStationId, 50);

  const selectedStation = stations.find((s) => s.id === selectedStationId);

  return (
    <div className="h-screen flex bg-bg text-text">
      <StationSidebar
        stations={stations}
        anomalies={allAnomaliesQuery.data ?? []}
        selectedId={selectedStationId}
        onSelect={setSelectedStationId}
        isLoading={stationsQuery.isLoading}
        isError={stationsQuery.isError}
      />

      <div className="flex-1 flex flex-col min-w-0">
        <header className="px-6 py-4 border-b border-border">
          <h1 className="font-display text-lg font-semibold text-text">
            {selectedStation ? selectedStation.name : "AWS Anomaly Detection"}
          </h1>
          <p className="text-xs text-muted mt-0.5">
            {selectedStation ? selectedStation.location : "Select a station to begin"}
          </p>
        </header>

        <div className="flex-1 flex min-h-0">
          <main className="flex-1 min-w-0 overflow-y-auto p-6 flex flex-col gap-4">
            {!selectedStationId ? (
              <div className="text-sm text-muted">
                {stationsQuery.isLoading ? "Loading stations…" : "No station selected."}
              </div>
            ) : (
              <>
                <DashboardStats
                  station={selectedStation}
                  readings={readings}
                  anomalies={stationAnomaliesQuery.data ?? []}
                />

                {readingsQuery.isError && (
                  <div className="rounded-sm border border-danger/40 bg-danger/10 px-4 py-3 text-sm text-danger">
                    Couldn't load sensor readings. Confirm the backend is running and reachable.
                  </div>
                )}

                {!readingsQuery.isError && readings.length === 0 && !readingsQuery.isLoading && (
                  <div className="rounded-sm border border-border bg-surface px-4 py-6 text-sm text-muted text-center">
                    No readings yet for this station. Run <code className="text-accent">seed_demo_data.py</code> on the backend.
                  </div>
                )}

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <SensorChart title="Temperature" unit="°C" dataKey="temperature" readings={readings} color="var(--color-accent)" />
                  <SensorChart title="Humidity" unit="%" dataKey="humidity" readings={readings} color="var(--color-accent)" />
                  <SensorChart title="Pressure" unit="hPa" dataKey="pressure" readings={readings} color="var(--color-accent)" />
                  <SensorChart title="Wind speed" unit="m/s" dataKey="wind_speed" readings={readings} color="var(--color-accent)" />
                </div>
              </>
            )}
          </main>

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
