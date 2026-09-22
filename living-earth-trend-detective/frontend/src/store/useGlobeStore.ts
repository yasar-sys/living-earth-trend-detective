import { create } from "zustand";
import type { DataLayer } from "@/types";

interface GlobeState {
  currentLayer: DataLayer;
  currentYear: number;
  selectedRegionId: string | null;
  setLayer: (layer: DataLayer) => void;
  setYear: (year: number) => void;
  selectRegion: (regionId: string | null) => void;
}

export const useGlobeStore = create<GlobeState>((set) => ({
  currentLayer: "temperature_anomaly",
  currentYear: 2024,
  selectedRegionId: null,
  setLayer: (layer) => set({ currentLayer: layer, selectedRegionId: null }),
  setYear: (year) => set({ currentYear: year }),
  selectRegion: (regionId) => set({ selectedRegionId: regionId }),
}));
