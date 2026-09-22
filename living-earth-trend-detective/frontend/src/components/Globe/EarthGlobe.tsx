import { useEffect, useMemo, useRef } from "react";
import Globe, { GlobeMethods } from "react-globe.gl";
import { valueToColor } from "@/utils/colorScales";
import type { GlobeLayerData } from "@/types";

// Public-domain Earth texture served from a CDN at runtime (browser fetch,
// not part of the build). Swap for a locally hosted /textures/earth.jpg
// if you want zero external dependency at demo time.
const EARTH_TEXTURE = "https://unpkg.com/three-globe/example/img/earth-blue-marble.jpg";
const BUMP_TEXTURE = "https://unpkg.com/three-globe/example/img/earth-topology.png";

interface RegionPoint {
  id: string;
  lat: number;
  lng: number;
  value: number;
  name: string;
}

interface Props {
  layerData: GlobeLayerData | null;
  regionCoords: Record<string, { name: string; coordinates: [number, number] }>;
  onSelectRegion: (regionId: string) => void;
}

export default function EarthGlobe({ layerData, regionCoords, onSelectRegion }: Props) {
  const globeRef = useRef<GlobeMethods | undefined>(undefined);

  const points: RegionPoint[] = useMemo(() => {
    if (!layerData) return [];
    return Object.entries(layerData.data)
      .filter(([id]) => regionCoords[id])
      .map(([id, value]) => ({
        id,
        lat: regionCoords[id].coordinates[0],
        lng: regionCoords[id].coordinates[1],
        value,
        name: regionCoords[id].name,
      }));
  }, [layerData, regionCoords]);

  useEffect(() => {
    if (globeRef.current) {
      globeRef.current.pointOfView({ altitude: 2.2 }, 0);
      const controls = globeRef.current.controls();
      if (controls) {
        controls.autoRotate = true;
        controls.autoRotateSpeed = 0.35;
      }
    }
  }, []);

  return (
    <div className="globe-container">
      <Globe
        ref={globeRef}
        globeImageUrl={EARTH_TEXTURE}
        bumpImageUrl={BUMP_TEXTURE}
        backgroundColor="rgba(0,0,0,0)"
        pointsData={points}
        pointLat="lat"
        pointLng="lng"
        pointAltitude={0.02}
        pointRadius={0.55}
        pointColor={(d) => {
          const p = d as RegionPoint;
          if (!layerData) return "#7C6FF0";
          return valueToColor(p.value, layerData.min_value, layerData.max_value, layerData.color_scale);
        }}
        pointLabel={(d) => {
          const p = d as RegionPoint;
          return `<div style="background:rgba(18,22,36,0.95);border:1px solid #2D3448;border-radius:8px;padding:8px 12px;font-family:Inter,sans-serif;font-size:12px;color:#E8E6E1">
            <strong style="color:#F2A93B">${p.name}</strong><br/>
            ${p.value} ${layerData?.unit ?? ""}
          </div>`;
        }}
        onPointClick={(d) => {
          const p = d as RegionPoint;
          onSelectRegion(p.id);
        }}
        atmosphereColor="#7C6FF0"
        atmosphereAltitude={0.18}
      />
    </div>
  );
}
