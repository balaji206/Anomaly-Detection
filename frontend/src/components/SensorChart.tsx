import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, Dot } from "recharts";
import type { Reading } from "../types";

interface Props {
  title: string;
  unit: string;
  dataKey: keyof Reading;
  readings: Reading[];
  color?: string;
}

function formatTime(iso: string) {
  const d = new Date(iso);
  return d.toLocaleTimeString(undefined, { hour: "2-digit", minute: "2-digit" });
}

// Custom dot: only render a visible marker on anomalous points, keep the rest of the line clean
function AnomalyDot(props: any) {
  const { cx, cy, payload } = props;
  if (!payload?.is_anomaly) return null;
  return <Dot cx={cx} cy={cy} r={4} fill="var(--color-warn)" stroke="none" />;
}

export function SensorChart({ title, unit, dataKey, readings, color = "var(--color-accent)" }: Props) {
  const chartData = readings.map((r) => ({ ...r, label: formatTime(r.timestamp) }));

  return (
    <div className="border border-border bg-surface rounded-sm p-4">
      <div className="flex items-baseline justify-between mb-3">
        <h3 className="font-display text-sm font-medium text-text">{title}</h3>
        <span className="text-xs text-muted">{unit}</span>
      </div>
      <div className="h-40">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={chartData} margin={{ top: 4, right: 4, bottom: 0, left: -20 }}>
            <CartesianGrid stroke="var(--color-border)" strokeDasharray="2 4" vertical={false} />
            <XAxis
              dataKey="label"
              tick={{ fill: "var(--color-muted)", fontSize: 10 }}
              axisLine={{ stroke: "var(--color-border)" }}
              tickLine={false}
              interval="preserveStartEnd"
            />
            <YAxis
              tick={{ fill: "var(--color-muted)", fontSize: 10 }}
              axisLine={false}
              tickLine={false}
              width={36}
            />
            <Tooltip
              contentStyle={{
                background: "var(--color-surface-alt)",
                border: "1px solid var(--color-border)",
                borderRadius: 2,
                fontSize: 12,
                fontFamily: "var(--font-mono)",
              }}
              labelStyle={{ color: "var(--color-muted)" }}
            />
            <Line
              type="monotone"
              dataKey={dataKey as string}
              stroke={color}
              strokeWidth={1.75}
              dot={<AnomalyDot />}
              activeDot={{ r: 4 }}
              isAnimationActive={false}
              connectNulls
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
