import { useEffect, useState } from "react";
import TrendChart from "@/components/Charts/TrendChart";
import SignificanceBadge from "@/components/UI/Badge";
import { api } from "@/services/api";
import type { DataLayer, LayerMetadata, RegionData, TrendResult } from "@/types";
import { formatPValue, formatSlope } from "@/utils/formatters";

interface Props {
  layer: DataLayer;
  layerMeta: LayerMetadata | undefined;
  regionId: string;
  onClose: () => void;
}

export default function RegionSidePanel({ layer, layerMeta, regionId, onClose }: Props) {
  const [region, setRegion] = useState<RegionData | null>(null);
  const [trend, setTrend] = useState<TrendResult | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    Promise.all([api.getRegion(layer, regionId), api.getRegionTrend(layer, regionId)])
      .then(([r, t]) => {
        if (!cancelled) {
          setRegion(r);
          setTrend(t);
        }
      })
      .finally(() => !cancelled && setLoading(false));
    return () => {
      cancelled = true;
    };
  }, [layer, regionId]);

  return (
    <aside className="side-panel fixed top-0 right-0 h-full w-full sm:w-96 z-30 p-6 overflow-y-auto animate-slide-up">
      <button onClick={onClose} className="text-slate-muted hover:text-offwhite-text mb-4">
        ← Back to globe
      </button>

      {loading && <p className="text-slate-muted text-sm">Loading region data…</p>}

      {!loading && region && trend && (
        <>
          <h2 className="font-serif text-heading-lg mb-1">{region.region_name}</h2>
          <p className="text-sm text-slate-muted mb-4">{layerMeta?.display_name}</p>

          <TrendChart data={region.time_series} unit={region.time_series[0]?.unit ?? ""} />

          <div className="mt-6 space-y-3">
            <div className="flex items-center justify-between">
              <span className="text-sm text-slate-muted">Rate of change</span>
              <span className="font-semibold text-amber-warm">
                {formatSlope(trend.slope_per_decade, trend.unit)}
              </span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-slate-muted">Mann-Kendall test</span>
              <span className="text-sm">{formatPValue(trend.p_value)}</span>
            </div>
            <div className="flex items-center justify-between">
              <span className="text-sm text-slate-muted">Sample size</span>
              <span className="text-sm">
                {trend.sample_size} years ({trend.start_year}–{trend.end_year})
              </span>
            </div>
            <div className="pt-2">
              <SignificanceBadge significance={trend.significance} />
            </div>
          </div>

          {layerMeta && (
            <div className="mt-6 pt-4 border-t border-space-border text-xs text-slate-muted">
              Data: {layerMeta.sources.map((s) => s.name).join(", ")}
            </div>
          )}
        </>
      )}
    </aside>
  );
}
