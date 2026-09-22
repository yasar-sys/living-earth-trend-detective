export type DataLayer = "temperature_anomaly" | "sea_ice_extent" | "co2_concentration";

export type Significance = "significant" | "not_significant" | "insufficient_data";

export interface TimeSeriesPoint {
  year: number;
  value: number;
  unit: string;
}

export interface RegionData {
  region_id: string;
  region_name: string;
  region_type: string;
  coordinates: [number, number];
  time_series: TimeSeriesPoint[];
  metadata: Record<string, unknown>;
}

export interface TrendResult {
  region_id: string;
  region_name: string;
  layer: DataLayer;
  slope_per_decade: number;
  p_value: number;
  significance: Significance;
  tau: number;
  sample_size: number;
  start_year: number;
  end_year: number;
  unit: string;
}

export interface GlobeLayerData {
  layer: DataLayer;
  year: number;
  data: Record<string, number>;
  min_value: number;
  max_value: number;
  unit: string;
  color_scale: string[];
}

export interface DataSourceInfo {
  name: string;
  url: string;
  citation: string;
}

export interface LayerMetadata {
  layer: DataLayer;
  display_name: string;
  description: string;
  unit: string;
  sources: DataSourceInfo[];
  available_years: number[];
  regions: string[];
}

export interface DetectiveCase {
  id: string;
  title: string;
  layer: DataLayer;
  regions: string[];
  narrative: string;
  explanation: string;
  key_mechanism: string;
  comparison_years: number[];
}
