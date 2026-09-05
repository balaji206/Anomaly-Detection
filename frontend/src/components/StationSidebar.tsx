import type { Station, Anomaly } from "../types";

interface Props {
  stations: Station[];
  anomalies: Anomaly[];
  selectedId: string | null;
  onSelect: (id: string) => void;
  isLoading: boolean;
  isError: boolean;
}

export function StationSidebar({ stations, anomalies, selectedId, onSelect, isLoading, isError }: Props) {
  const unresolvedByStation = new Set(
    anomalies.filter((a) => !a.resolved).map((a) => a.station_id)
  );

  return (
    <aside className="w-64 shrink-0 border-r border-border bg-surface flex flex-col">
      <div className="px-5 py-5 border-b border-border">
        <div className="font-display font-semibold text-lg tracking-tight text-text">Mavericks</div>
        <div className="text-xs text-muted mt-0.5">AWS fleet monitor</div>
      </div>

      <div className="flex-1 overflow-y-auto py-2">
        {isLoading && (
          <div className="px-5 py-4 text-sm text-muted">Loading stations…</div>
        )}

        {isError && (
          <div className="mx-3 my-3 rounded-sm border border-danger/40 bg-danger/10 px-3 py-2.5 text-xs text-danger leading-relaxed">
            Can't reach the backend. Confirm FastAPI is running on localhost:8000, then this list will populate.
          </div>
        )}

        {!isLoading && !isError && stations.length === 0 && (
          <div className="px-5 py-4 text-sm text-muted leading-relaxed">
            No stations yet. Run <code className="text-accent">seed_demo_data.py</code> on the backend.
          </div>
        )}

        {stations.map((station) => {
          const active = station.id === selectedId;
          const flagged = unresolvedByStation.has(station.id);
          return (
            <button
              key={station.id}
              onClick={() => onSelect(station.id)}
              className={`w-full text-left px-5 py-3 border-l-2 transition-colors ${
                active
                  ? "border-l-accent bg-surface-alt"
                  : "border-l-transparent hover:bg-surface-alt/60"
              }`}
            >
              <div className="flex items-center justify-between">
                <span className="font-mono text-sm text-text">{station.id}</span>
                <span
                  className={`inline-block w-1.5 h-1.5 rounded-full ${
                    flagged ? "bg-warn" : "bg-accent"
                  }`}
                  title={flagged ? "Unresolved anomaly" : "Nominal"}
                />
              </div>
              <div className="text-xs text-muted mt-0.5">{station.name}</div>
            </button>
          );
        })}
      </div>

      <div className="px-5 py-4 border-t border-border text-xs text-muted leading-relaxed">
        SIH26073 — AI/ML-Based Intelligent Anomaly Detection for AWS
      </div>
    </aside>
  );
}
