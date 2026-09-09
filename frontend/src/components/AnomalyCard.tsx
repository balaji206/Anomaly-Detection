import { useState } from "react";
import { ChevronDown, Sparkles, Loader2, Cpu, CheckCircle } from "lucide-react";
import type { Anomaly } from "../types";
import { useExplanation } from "../hooks/useStationData";

interface Props {
  anomaly: Anomaly;
}

const TYPE_CONFIG: Record<string, { label: string; badgeClass: string }> = {
  spike: { label: "Spike Detected", badgeClass: "bg-red-500/20 text-red-300 border-red-500/40" },
  drift: { label: "Sensor Drift", badgeClass: "bg-amber-500/20 text-amber-300 border-amber-500/40" },
  missing: { label: "Missing Reading", badgeClass: "bg-orange-500/20 text-orange-300 border-orange-500/40" },
  flatline: { label: "Telemetry Flatline", badgeClass: "bg-purple-500/20 text-purple-300 border-purple-500/40" },
  normal: { label: "Normal", badgeClass: "bg-emerald-500/20 text-emerald-300 border-emerald-500/40" },
};

export function AnomalyCard({ anomaly }: Props) {
  const [expanded, setExpanded] = useState(false);
  const [resolved, setResolved] = useState(anomaly.resolved);
  const explainMutation = useExplanation();

  const explanationText = anomaly.explanation ?? explainMutation.data;
  const config = TYPE_CONFIG[anomaly.anomaly_type] ?? {
    label: anomaly.anomaly_type,
    badgeClass: "bg-amber-500/20 text-amber-300 border-amber-500/40",
  };

  function handleToggle() {
    const next = !expanded;
    setExpanded(next);
    if (next && !explanationText && !explainMutation.isPending) {
      explainMutation.mutate(anomaly.id);
    }
  }

  const time = new Date(anomaly.timestamp).toLocaleString(undefined, {
    month: "short", day: "numeric", hour: "2-digit", minute: "2-digit",
  });

  return (
    <div
      className={`shrink-0 rounded-xl border transition-all duration-150 overflow-hidden ${
        resolved
          ? "bg-white/[0.02] border-white/5 opacity-50"
          : expanded
          ? "glass-liquid border-indigo-500/40 shadow-sm"
          : "glass-liquid glass-liquid-hover"
      }`}
    >
      <button
        onClick={handleToggle}
        className="w-full flex items-center justify-between p-3.5 text-left cursor-pointer select-none group"
      >
        <div className="min-w-0 flex-1 pr-2">
          <div className="flex items-center gap-2 flex-wrap">
            <span className={`text-[10px] font-semibold uppercase px-2 py-0.5 rounded-full border ${config.badgeClass}`}>
              {config.label}
            </span>
            <span className="font-mono text-xs text-slate-300 font-medium">
              {anomaly.station_id}
            </span>
            {resolved && (
              <span className="text-[10px] px-1.5 py-0.5 rounded bg-emerald-500/15 text-emerald-300 border border-emerald-500/30 flex items-center gap-1">
                <CheckCircle className="w-3 h-3" /> Resolved
              </span>
            )}
          </div>
          <div className="text-xs text-muted font-mono mt-2 flex items-center gap-2">
            <span>{time}</span>
            <span>•</span>
            <span>Score: <strong className="text-amber-400">{anomaly.anomaly_score.toFixed(2)}</strong></span>
          </div>
        </div>

        <div className="p-1 rounded-md bg-white/5 border border-white/10 text-slate-400 group-hover:text-indigo-400 transition-colors">
          <ChevronDown
            size={16}
            className={`transition-transform duration-200 ${expanded ? "rotate-180 text-indigo-400" : ""}`}
          />
        </div>
      </button>

      {expanded && (
        <div className="px-4 pb-4 pt-2 border-t border-white/10 bg-black/20 space-y-3">
          {/* AI Explanation Banner */}
          <div className="rounded-xl bg-indigo-500/10 border border-indigo-500/30 p-3.5">
            <div className="flex items-center justify-between mb-2">
              <div className="flex items-center gap-1.5 text-xs font-semibold text-indigo-300">
                <Sparkles className="w-3.5 h-3.5 text-indigo-400 animate-pulse" />
                <span>NVIDIA NIM AI Diagnostic Copilot</span>
              </div>
              <Cpu className="w-3.5 h-3.5 text-indigo-400/60" />
            </div>

            {explainMutation.isPending && !anomaly.explanation ? (
              <div className="flex items-center gap-2.5 text-xs text-slate-300 py-2">
                <Loader2 className="w-4 h-4 text-indigo-400 animate-spin" />
                Generating physical cause diagnostics…
              </div>
            ) : explainMutation.isError && !anomaly.explanation ? (
              <div className="text-xs text-red-400 leading-relaxed">
                <p>Unable to connect to AI explanation service.</p>
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    explainMutation.mutate(anomaly.id);
                  }}
                  className="mt-1.5 text-xs text-indigo-400 underline hover:text-indigo-300 cursor-pointer"
                >
                  Retry request
                </button>
              </div>
            ) : (
              <p className="text-xs text-slate-200 leading-relaxed font-sans">
                {explanationText}
              </p>
            )}
          </div>

          {/* Action buttons */}
          <div className="flex items-center justify-end gap-2 pt-1">
            {!resolved ? (
              <button
                onClick={(e) => {
                  e.stopPropagation();
                  setResolved(true);
                }}
                className="px-3 py-1.5 rounded-lg bg-emerald-500/15 hover:bg-emerald-500/25 border border-emerald-500/30 text-emerald-300 text-xs font-medium transition-colors cursor-pointer flex items-center gap-1.5"
              >
                <CheckCircle className="w-3.5 h-3.5" /> Mark Resolved
              </button>
            ) : (
              <span className="text-[11px] text-muted font-mono">Alert resolved by operator</span>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
