import type { Reading, Anomaly, Station } from "../types";

interface Props {
  station: Station | undefined;
  readings: Reading[];
  anomalies: Anomaly[];
}

export function DashboardStats({ station, readings, anomalies }: Props) {
  const total = readings.length;
  const anomalyCount = anomalies.length;
  const uptimePct = total > 0 ? (((total - anomalyCount) / total) * 100).toFixed(1) : "—";
  const latest = readings[readings.length - 1];

  const stats = [
    { label: "Station", value: station?.id ?? "—" },
    { label: "Readings (24h)", value: total.toString() },
    { label: "Anomalies", value: anomalyCount.toString() },
    { label: "Uptime", value: total > 0 ? `${uptimePct}%` : "—" },
    { label: "Latest temp", value: latest ? `${latest.temperature.toFixed(1)}°C` : "—" },
  ];

  return (
    <div className="flex items-stretch gap-px bg-border border border-border rounded-sm overflow-hidden">
      {stats.map((s) => (
        <div key={s.label} className="flex-1 bg-surface px-4 py-3">
          <div className="text-xs text-muted">{s.label}</div>
          <div className="font-mono text-lg text-text mt-0.5">{s.value}</div>
        </div>
      ))}
    </div>
  );
}
