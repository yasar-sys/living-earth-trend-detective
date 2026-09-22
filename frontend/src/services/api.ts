import axios from "axios";
import type {
  DataLayer,
  DetectiveCase,
  GlobeLayerData,
  LayerMetadata,
  RegionData,
  TrendResult,
} from "@/types";

const client = axios.create({
  baseURL: "/api",
  timeout: 15000,
});

export const api = {
  getLayers: () => client.get<LayerMetadata[]>("/layers").then((r) => r.data),

  getLayerMeta: (layer: DataLayer) =>
    client.get<LayerMetadata>(`/layers/${layer}`).then((r) => r.data),

  getYears: (layer: DataLayer) =>
    client.get<number[]>(`/layers/${layer}/years`).then((r) => r.data),

  getLayerData: (layer: DataLayer, year: number) =>
    client.get<GlobeLayerData>(`/layers/${layer}/data/${year}`).then((r) => r.data),

  getRegion: (layer: DataLayer, regionId: string) =>
    client.get<RegionData>(`/layers/${layer}/regions/${regionId}`).then((r) => r.data),

  getRegionTrend: (layer: DataLayer, regionId: string) =>
    client
      .get<TrendResult>(`/layers/${layer}/regions/${regionId}/trend`)
      .then((r) => r.data),

  getDetectiveCases: () =>
    client.get<DetectiveCase[]>("/detective/cases").then((r) => r.data),
};
