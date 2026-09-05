import type { Anomaly } from "../types";
import { AnomalyCard } from "./AnomalyCard";

interface Props {
  anomalies: Anomaly[];
  isLoading: boolean;
  isError: boolean;
}

export function AnomalyFeed({ anomalies, isLoading, isError }: Props) {
  return (
    <div className="w-80 shrink-0 flex flex-col border-l border-border bg-bg">
      <div className="px-4 py-4 border-b border-border">
        <h2 className="font-display text-sm font-medium text-text">Anomaly feed</h2>
        <p className="text-xs text-muted mt-0.5">Tap a card for the AI explanation</p>
      </div>

      <div className="flex-1 overflow-y-auto p-3 flex flex-col gap-2">
        {isLoading && <div className="text-sm text-muted px-2 py-3">Loading…</div>}

        {isError && (
          <div className="rounded-sm border border-danger/40 bg-danger/10 px-3 py-2.5 text-xs text-danger leading-relaxed">
            Couldn't load anomalies from the backend.
          </div>
        )}

        {!isLoading && !isError && anomalies.length === 0 && (
          <div className="text-sm text-muted px-2 py-3 leading-relaxed">
            No anomalies detected for this station yet — nothing to flag right now.
          </div>
        )}

        {anomalies.map((a) => (
          <AnomalyCard key={a.id} anomaly={a} />
        ))}
      </div>
    </div>
  );
}
