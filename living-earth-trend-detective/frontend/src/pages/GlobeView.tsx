import { useEffect, useMemo, useState } from "react";
import EarthGlobe from "@/components/Globe/EarthGlobe";
import GlobeControls from "@/components/Globe/GlobeControls";
import RegionSidePanel from "@/components/Globe/RegionSidePanel";
import TimeSlider from "@/components/Globe/TimeSlider";
import { api } from "@/services/api";
import { useGlobeStore } from "@/store/useGlobeStore";
import type { GlobeLayerData, LayerMetadata } from "@/types";

interface RegionCoord {
  name: string;
  coordinates: [number, number];
}

export default function GlobeView() {
  const { currentLayer, currentYear, selectedRegionId, setLayer, setYear, selectRegion } =
    useGlobeStore();

  const [layers, setLayers] = useState<LayerMetadata[]>([]);
  const [layerData, setLayerData] = useState<GlobeLayerData | null>(null);
  const [regionCoords, setRegionCoords] = useState<Record<string, RegionCoord>>({});
  const [loading, setLoading] = useState(true);

  // Load layer metadata once on mount, default to the first layer's latest year.
  useEffect(() => {
    api.getLayers().then((ls) => {
      setLayers(ls);
      const first = ls[0];
      if (first) {
        const latest = first.available_years[first.available_years.length - 1];
        setYear(latest);
      }
    });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // Fetch region coordinates whenever the active layer changes.
  useEffect(() => {
    fetch(`/api/layers/${currentLayer}/regions`)
      .then((r) => r.json())
      .then((rows: { region_id: string; region_name: string; coordinates: [number, number] }[]) => {
        const map: Record<string, RegionCoord> = {};
        rows.forEach((r) => {
          map[r.region_id] = { name: r.region_name, coordinates: r.coordinates };
        });
        setRegionCoords(map);
      });
  }, [currentLayer]);

  // Fetch overlay data whenever layer or year changes.
  useEffect(() => {
    setLoading(true);
    api
      .getLayerData(currentLayer, currentYear)
      .then(setLayerData)
      .finally(() => setLoading(false));
  }, [currentLayer, currentYear]);

  const currentLayerMeta = useMemo(
    () => layers.find((l) => l.layer === currentLayer),
    [layers, currentLayer]
  );
  const years = currentLayerMeta?.available_years ?? [];

  return (
    <div className="relative h-[calc(100vh-64px)] overflow-hidden">
      <EarthGlobe
        layerData={layerData}
        regionCoords={regionCoords}
        onSelectRegion={(id) => selectRegion(id)}
      />

      {layers.length > 0 && (
        <GlobeControls layers={layers} currentLayer={currentLayer} onSelect={setLayer} />
      )}

      {loading && (
        <div className="absolute top-4 right-4 z-20 text-xs text-slate-muted bg-space-card/80 px-3 py-1.5 rounded-full border border-space-border">
          Loading…
        </div>
      )}

      {years.length > 0 && (
        <TimeSlider years={years} currentYear={currentYear} onChange={setYear} />
      )}

      {selectedRegionId && (
        <RegionSidePanel
          layer={currentLayer}
          layerMeta={currentLayerMeta}
          regionId={selectedRegionId}
          onClose={() => selectRegion(null)}
        />
      )}
    </div>
  );
}
