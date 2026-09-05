import axios from "axios";
import type { Station, Reading, Anomaly } from "../types";

// Point this at your backend. Defaults to local dev; override with VITE_API_BASE_URL in .env for anything else.
const BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export const api = axios.create({ baseURL: BASE_URL, timeout: 10000 });

export async function fetchStations(): Promise<Station[]> {
  const { data } = await api.get<{ stations: Station[] }>("/api/stations");
  return data.stations;
}

export async function fetchReadings(stationId: string, hours = 24): Promise<Reading[]> {
  const { data } = await api.get<{ station_id: string; readings: Reading[] }>(
    `/api/sensors/${stationId}/readings`,
    { params: { hours } }
  );
  return data.readings;
}

export async function fetchAnomalies(stationId?: string, limit = 50): Promise<Anomaly[]> {
  const { data } = await api.get<{ anomalies: Anomaly[] }>("/api/anomalies", {
    params: { station_id: stationId, limit },
  });
  return data.anomalies;
}

export async function fetchExplanation(anomalyId: number): Promise<string> {
  const { data } = await api.get<{ explanation: string }>(`/api/anomalies/${anomalyId}/explain`);
  return data.explanation;
}
