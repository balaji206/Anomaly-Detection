import type { Anomaly } from "../types";
import { AnomalyCard } from "./AnomalyCard";
import { ShieldAlert, AlertTriangle, RefreshCw } from "lucide-react";

interface Props {
  anomalies: Anomaly[];
  isLoading: boolean;
  isError: boolean;
}

export function AnomalyFeed({ anomalies, isLoading, isError }: Props) {
  const activeCount = anomalies.filter((a) => !a.resolved).length;

  return (
    <div className="w-88 shrink-0 flex flex-col border-l border-white/10 bg-[#0e1017]/80 backdrop-blur-2xl h-full select-none z-20">
      {/* Header */}
      <div className="px-5 py-4 border-b border-white/10 bg-white/[0.02]">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <ShieldAlert className="w-4 h-4 text-amber-400" />
            <h2 className="font-display text-sm font-bold text-text">Anomaly Stream</h2>
          </div>
          {activeCount > 0 && (
            <span className="font-mono text-xs font-semibold px-2 py-0.5 rounded-full bg-amber-500/15 text-amber-300 border border-amber-500/30">
              {activeCount} Unresolved
            </span>
          )}
        </div>
        <p className="text-xs text-muted mt-1">Select an alert for physical root-cause diagnostic analysis</p>
      </div>

      {/* Feed list */}
      <div className="flex-1 overflow-y-auto p-3 space-y-2.5">
        {isLoading && (
          <div className="flex items-center justify-center gap-2 py-12 text-sm text-muted">
            <RefreshCw className="w-4 h-4 animate-spin text-teal-400" />
            Polling telemetry stream…
          </div>
        )}

        {isError && (
          <div className="rounded-xl border border-red-500/30 bg-red-500/10 p-4 text-xs text-red-400 leading-relaxed flex items-start gap-2.5">
            <AlertTriangle className="w-4 h-4 text-red-400 shrink-0 mt-0.5" />
            <div>Couldn't fetch anomaly stream from backend server.</div>
          </div>
        )}

        {!isLoading && !isError && anomalies.length === 0 && (
          <div className="text-center py-12 px-4 rounded-xl border border-dashed border-border bg-slate-900/20">
            <div className="w-10 h-10 rounded-full bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-emerald-400 mx-auto mb-3">
              ✓
            </div>
            <div className="text-xs font-semibold text-text">All Sensors Nominal</div>
            <div className="text-[11px] text-muted mt-1">No anomalies flagged for this station in the current telemetry window.</div>
          </div>
        )}

        {anomalies.map((a) => (
          <AnomalyCard key={a.id} anomaly={a} />
        ))}
      </div>
    </div>
  );
}
