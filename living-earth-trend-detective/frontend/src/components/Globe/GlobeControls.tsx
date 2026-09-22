import type { DataLayer, LayerMetadata } from "@/types";

interface Props {
  layers: LayerMetadata[];
  currentLayer: DataLayer;
  onSelect: (layer: DataLayer) => void;
}

export default function GlobeControls({ layers, currentLayer, onSelect }: Props) {
  return (
    <div className="absolute top-4 left-4 z-20 flex flex-col gap-2 max-w-xs">
      {layers.map((layer) => {
        const active = layer.layer === currentLayer;
        return (
          <button
            key={layer.layer}
            onClick={() => onSelect(layer.layer)}
            className={`layer-toggle text-left px-4 py-3 rounded-xl border transition-all ${
              active
                ? "border-violet-primary bg-violet-primary/15"
                : "border-space-border bg-space-card/80 hover:border-space-border"
            }`}
          >
            <div className="font-serif font-semibold text-sm">{layer.display_name}</div>
            <div className="text-xs text-slate-muted mt-0.5">
              {layer.available_years[0]}–{layer.available_years[layer.available_years.length - 1]}
              {" · "}
              {layer.unit}
            </div>
            {layer.sources[0] && (
              <div className="text-[10px] text-slate-muted mt-1 truncate">
                Source: {layer.sources[0].name}
              </div>
            )}
          </button>
        );
      })}
    </div>
  );
}
