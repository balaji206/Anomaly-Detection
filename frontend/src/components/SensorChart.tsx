import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, Dot } from "recharts";
import { Thermometer, Droplets, Gauge, Wind } from "lucide-react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import type { Reading } from "../types";

interface Props {
  title: string;
  unit: string;
  dataKey: keyof Reading;
  readings: Reading[];
  color?: string;
}

function getIcon(title: string) {
  const t = title.toLowerCase();
  if (t.includes("temp")) return <Thermometer className="w-4 h-4 text-rose-400" />;
  if (t.includes("humid")) return <Droplets className="w-4 h-4 text-cyan-400" />;
  if (t.includes("press")) return <Gauge className="w-4 h-4 text-amber-400" />;
  return <Wind className="w-4 h-4 text-teal-400" />;
}

function formatTime(iso: string) {
  const d = new Date(iso);
  return d.toLocaleTimeString(undefined, { hour: "2-digit", minute: "2-digit" });
}

// Custom dot: render a clean highlighted marker on anomalous points
function AnomalyDot(props: any) {
  const { cx, cy, payload } = props;
  if (!payload?.is_anomaly) return null;
  return <Dot cx={cx} cy={cy} r={3.5} fill="#f59e0b" stroke="#000000" strokeWidth={1} />;
}

export function SensorChart({ title, unit, dataKey, readings, color = "#14b8a6" }: Props) {
  const chartData = readings.map((r) => ({ ...r, label: formatTime(r.timestamp) }));
  const icon = getIcon(title);
  const gradientId = `gradient-${dataKey}`;

  return (
    <Card className="flex flex-col justify-between overflow-hidden">
      <CardHeader className="p-4 pb-2">
        <div className="flex items-center justify-between border-b border-slate-800/60 pb-2.5">
          <div className="flex items-center gap-2">
            <div className="p-1.5 rounded-lg bg-slate-950/80 border border-slate-800">
              {icon}
            </div>
            <CardTitle className="text-xs font-bold uppercase tracking-wider text-slate-200">
              {title}
            </CardTitle>
          </div>
          <span className="font-mono text-xs font-semibold px-2 py-0.5 rounded-md bg-slate-950/80 text-slate-400 border border-slate-800">
            {unit}
          </span>
        </div>
      </CardHeader>

      <CardContent className="p-4 pt-0 h-48 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={chartData} margin={{ top: 10, right: 10, bottom: 0, left: -16 }}>
            <defs>
              <linearGradient id={gradientId} x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor={color} stopOpacity={0.35} />
                <stop offset="95%" stopColor={color} stopOpacity={0.0} />
              </linearGradient>
            </defs>
            <CartesianGrid stroke="#1e2d50" strokeDasharray="3 3" vertical={false} />
            <XAxis
              dataKey="label"
              tick={{ fill: "#64748b", fontSize: 10, fontFamily: "JetBrains Mono" }}
              axisLine={{ stroke: "#1e2d50" }}
              tickLine={false}
              interval="preserveStartEnd"
            />
            <YAxis
              domain={["auto", "auto"]}
              tick={{ fill: "#64748b", fontSize: 10, fontFamily: "JetBrains Mono" }}
              axisLine={false}
              tickLine={false}
              width={40}
            />
            <Tooltip
              formatter={(value: any) => [
                typeof value === "number" ? `${value.toFixed(1)} ${unit}` : `${value} ${unit}`,
                title,
              ]}
              contentStyle={{
                background: "rgba(15, 25, 50, 0.95)",
                border: "1px solid #2e4372",
                borderRadius: "8px",
                boxShadow: "0 10px 25px -5px rgba(0, 0, 0, 0.5)",
                fontSize: "12px",
                fontFamily: "JetBrains Mono",
                color: "#f1f5f9",
              }}
              labelStyle={{ color: "#94a3b8", marginBottom: "4px", fontWeight: 600 }}
            />
            <Area
              type="monotone"
              dataKey={dataKey as string}
              stroke={color}
              strokeWidth={2}
              fillOpacity={1}
              fill={`url(#${gradientId})`}
              dot={<AnomalyDot />}
              activeDot={{ r: 5, stroke: "#ffffff", strokeWidth: 2 }}
              isAnimationActive={false}
              connectNulls
            />
          </AreaChart>
        </ResponsiveContainer>
      </CardContent>
    </Card>
  );
}
