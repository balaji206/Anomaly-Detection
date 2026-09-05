// These mirror the backend's response shapes exactly (see backend/README.md contract table).
// If a field name changes on the backend, update it here first — everything else depends on this file.

export interface Station {
  id: string;       // station code, e.g. "AWS-001" — this IS the id, not a separate DB row number
  name: string;
  location: string;
}

export interface Reading {
  timestamp: string;          // ISO 8601
  temperature: number;
  humidity: number;
  pressure: number;
  wind_speed: number | null;  // null when the sensor simulated a "missing" fault
  is_anomaly: boolean;
}

export type AnomalyType = "spike" | "drift" | "missing" | "flatline" | "normal" | string;

export interface Anomaly {
  id: number;
  station_id: string;
  timestamp: string;
  anomaly_type: AnomalyType;
  anomaly_score: number;       // more negative = more anomalous (Isolation Forest convention)
  sensor: string;
  value: number | null;
  explanation: string | null;  // null until /explain has been called once (then cached)
  resolved: boolean;
}
