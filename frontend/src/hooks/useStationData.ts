import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { fetchStations, fetchReadings, fetchAnomalies, fetchExplanation } from "../api/client";

const POLL_INTERVAL_MS = 15000; // live-feeling dashboard without hammering the backend

export function useStations() {
  return useQuery({
    queryKey: ["stations"],
    queryFn: fetchStations,
    refetchInterval: POLL_INTERVAL_MS,
  });
}

export function useReadings(stationId: string | null, hours = 24) {
  return useQuery({
    queryKey: ["readings", stationId, hours],
    queryFn: () => fetchReadings(stationId as string, hours),
    enabled: !!stationId,
    refetchInterval: POLL_INTERVAL_MS,
  });
}

export function useAnomalies(stationId: string | null, limit = 50) {
  return useQuery({
    queryKey: ["anomalies", stationId, limit],
    queryFn: () => fetchAnomalies(stationId ?? undefined, limit),
    refetchInterval: POLL_INTERVAL_MS,
  });
}

export function useExplanation() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (anomalyId: number) => fetchExplanation(anomalyId),
    onSuccess: () => {
      // refresh the anomaly list so the newly-cached explanation shows up everywhere
      queryClient.invalidateQueries({ queryKey: ["anomalies"] });
    },
  });
}
