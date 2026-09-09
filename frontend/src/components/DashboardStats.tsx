import type { Reading, Anomaly, Station } from "../types";
import { GlowingCard } from "@/components/ui/glowing-card";
import { Activity, AlertTriangle, ShieldCheck, Thermometer, Radio } from "lucide-react";

interface Props {
  station: Station | undefined;
  readings: Reading[];
  anomalies: Anomaly[];
}

export function DashboardStats({ station, readings, anomalies }: Props) {
  const total = readings.length;
  const anomalyCount = anomalies.length;
  const uptimeNum = total > 0 ? ((total - anomalyCount) / total) * 100 : 100;
  const uptimePct = total > 0 ? uptimeNum.toFixed(1) : "100.0";
  const latest = readings[readings.length - 1];

  return (
    <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-3.5">
      {/* Station Card */}
      <GlowingCard
        label="Active Station"
        icon={<Radio className="w-4 h-4 text-indigo-400 animate-pulse" />}
        value={station?.id ?? "—"}
        subtitle={station?.name ?? "No station selected"}
        valueColor="text-white"
      />

      {/* 24h Telemetry Count */}
      <GlowingCard
        label="24h Readings"
        icon={<Activity className="w-4 h-4 text-sky-400" />}
        value={total.toLocaleString()}
        subtitle="5-min stream intervals"
        valueColor="text-sky-400"
      />

      {/* Anomalies Detected */}
      <GlowingCard
        label="Detected Anomalies"
        icon={<AlertTriangle className={`w-4 h-4 ${anomalyCount > 0 ? "text-amber-400" : "text-emerald-400"}`} />}
        value={
          <div className="flex items-center gap-2">
            <span>{anomalyCount}</span>
            {anomalyCount > 0 && (
              <span className="text-[10px] font-semibold uppercase px-2 py-0.5 rounded-full bg-amber-500/15 text-amber-300 border border-amber-500/30 font-sans">
                Attention
              </span>
            )}
          </div>
        }
        subtitle="Isolation Forest flagged"
        valueColor={anomalyCount > 0 ? "text-amber-400" : "text-emerald-400"}
      />

      {/* System Health / Uptime */}
      <GlowingCard
        label="Signal Quality"
        icon={<ShieldCheck className="w-4 h-4 text-emerald-400" />}
        value={`${uptimePct}%`}
        subtitle={
          <div className="w-full bg-white/10 rounded-full h-1.5 mt-2 overflow-hidden border border-white/5">
            <div
              className="bg-gradient-to-r from-emerald-500 via-indigo-500 to-sky-400 h-full rounded-full transition-all duration-500"
              style={{ width: `${Math.max(5, uptimeNum)}%` }}
            />
          </div>
        }
        valueColor="text-emerald-400"
      />

      {/* Latest Temperature */}
      <GlowingCard
        label="Latest Temp"
        icon={<Thermometer className="w-4 h-4 text-rose-400" />}
        value={latest ? `${latest.temperature.toFixed(1)}°C` : "—"}
        subtitle={latest ? `Humidity: ${latest.humidity.toFixed(0)}%` : "No data"}
        valueColor="text-rose-400"
        className="col-span-2 sm:col-span-1"
      />
    </div>
  );
}
