import type { Station, Anomaly } from "../types";
import { Server, Activity, CheckCircle2, AlertCircle } from "lucide-react";

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
    <aside className="w-72 shrink-0 border-r border-white/10 bg-[#0e1017]/80 backdrop-blur-2xl flex flex-col h-full select-none z-20">
      {/* Sidebar Header */}
      <div className="px-5 py-5 border-b border-white/10 bg-white/[0.02]">
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-8 rounded-lg bg-indigo-500/10 border border-indigo-500/30 flex items-center justify-center text-indigo-400">
            <Activity className="w-4 h-4" />
          </div>
          <div>
            <div className="font-display font-bold text-sm tracking-tight text-text leading-tight">
              AWS Anomaly Detection System
            </div>
            <div className="text-[11px] font-mono text-muted flex items-center gap-1.5 mt-0.5">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
              Fleet Surveillance Live
            </div>
          </div>
        </div>
      </div>

      {/* Station List Header */}
      <div className="px-5 py-3 border-b border-white/10 flex items-center justify-between text-xs font-medium text-muted uppercase tracking-wider">
        <span>Weather Stations</span>
        <span className="font-mono text-[10px] bg-white/5 px-1.5 py-0.5 rounded text-slate-300 border border-white/5">
          {stations.length} Active
        </span>
      </div>

      {/* Station List Content */}
      <div className="flex-1 overflow-y-auto p-2 space-y-1">
        {isLoading && (
          <div className="px-4 py-8 text-center text-sm text-muted animate-pulse">
            Loading station fleet…
          </div>
        )}

        {isError && (
          <div className="mx-2 my-3 rounded-lg border border-red-500/30 bg-red-500/10 p-3 text-xs text-red-400 leading-relaxed flex items-start gap-2">
            <AlertCircle className="w-4 h-4 text-red-400 shrink-0 mt-0.5" />
            <div>Can't reach backend server on localhost:8000.</div>
          </div>
        )}

        {!isLoading && !isError && stations.length === 0 && (
          <div className="px-4 py-8 text-center text-sm text-muted">
            No stations found. Run <code className="text-indigo-400">seed_demo_data.py</code>.
          </div>
        )}

        {stations.map((station) => {
          const active = station.id === selectedId;
          const flagged = unresolvedByStation.has(station.id);
          return (
            <button
              key={station.id}
              onClick={() => onSelect(station.id)}
              className={`w-full text-left px-3.5 py-3 rounded-xl border transition-all duration-150 cursor-pointer flex items-center justify-between group ${
                active
                  ? "bg-indigo-500/15 border-indigo-500/40 text-text shadow-sm backdrop-blur-md"
                  : "bg-transparent border-transparent hover:bg-white/[0.04] hover:border-white/10 text-slate-300"
              }`}
            >
              <div className="min-w-0 pr-2">
                <div className="flex items-center gap-2">
                  <Server className={`w-3.5 h-3.5 ${active ? "text-indigo-400" : "text-slate-500 group-hover:text-slate-400"}`} />
                  <span className="font-mono text-sm font-semibold tracking-tight text-text">
                    {station.id}
                  </span>
                </div>
                <div className="text-xs text-muted truncate mt-0.5 pl-5">
                  {station.name}
                </div>
              </div>

              <div className="flex items-center gap-1.5">
                {flagged ? (
                  <span className="relative flex h-2.5 w-2.5" title="Unresolved Anomaly Alert">
                    <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-amber-400 opacity-75" />
                    <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-amber-500" />
                  </span>
                ) : (
                  <span title="Nominal Operation">
                    <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400/80" />
                  </span>
                )}
              </div>
            </button>
          );
        })}
      </div>

      {/* Sidebar Footer */}
      <div className="p-4 border-t border-white/10 bg-black/20 text-[11px] text-muted flex items-center justify-between">
        <span className="font-mono">SIH26073</span>
        <span className="px-2 py-0.5 rounded-full bg-indigo-500/10 text-indigo-300 border border-indigo-500/20 text-[10px] font-medium">
          v1.0.0 Production
        </span>
      </div>
    </aside>
  );
}
