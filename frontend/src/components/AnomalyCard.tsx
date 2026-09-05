import { useState } from "react";
import { ChevronDown, Sparkles, Loader2 } from "lucide-react";
import type { Anomaly } from "../types";
import { useExplanation } from "../hooks/useStationData";

interface Props {
  anomaly: Anomaly;
}

const TYPE_LABEL: Record<string, string> = {
  spike: "Spike",
  drift: "Drift",
  missing: "Missing reading",
  flatline: "Flatline",
  normal: "Normal",
};

export function AnomalyCard({ anomaly }: Props) {
  const [expanded, setExpanded] = useState(false);
  const explainMutation = useExplanation();

  const explanationText = anomaly.explanation ?? explainMutation.data;

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
    <div className="shrink-0 border border-border bg-surface rounded-sm overflow-hidden">
      <button
        onClick={handleToggle}
        className="w-full flex items-center justify-between px-4 py-3 text-left hover:bg-surface-alt/60 transition-colors cursor-pointer"
      >
        <div className="min-w-0">
          <div className="flex items-center gap-2">
            <span className="inline-block w-1.5 h-1.5 rounded-full bg-warn shrink-0" />
            <span className="text-sm text-text font-medium">
              {TYPE_LABEL[anomaly.anomaly_type] ?? anomaly.anomaly_type}
            </span>
            <span className="text-xs text-muted">· {anomaly.station_id}</span>
          </div>
          <div className="text-xs text-muted mt-0.5">
            {time} · score {anomaly.anomaly_score.toFixed(2)}
          </div>
        </div>
        <ChevronDown
          size={16}
          className={`text-muted shrink-0 transition-transform ${expanded ? "rotate-180" : ""}`}
        />
      </button>

      {expanded && (
        <div className="px-4 pb-4 pt-1 border-t border-border">
          <div className="flex items-start gap-2 mt-3">
            <Sparkles size={14} className="text-accent shrink-0 mt-0.5" />
            {explainMutation.isPending && !anomaly.explanation ? (
              <div className="flex items-center gap-2 text-sm text-muted">
                <Loader2 size={13} className="animate-spin" />
                Generating explanation…
              </div>
            ) : explainMutation.isError && !anomaly.explanation ? (
              <div className="text-sm text-danger leading-relaxed">
                <p>Couldn't reach the explanation service.</p>
                <button
                  onClick={(e) => {
                    e.stopPropagation();
                    explainMutation.mutate(anomaly.id);
                  }}
                  className="mt-1 text-xs text-accent underline hover:text-accent/80 cursor-pointer"
                >
                  Retry
                </button>
              </div>
            ) : (
              <p className="text-sm text-text leading-relaxed">{explanationText}</p>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
