interface Props {
  years: number[];
  currentYear: number;
  onChange: (year: number) => void;
}

export default function TimeSlider({ years, currentYear, onChange }: Props) {
  if (years.length === 0) return null;
  const min = years[0];
  const max = years[years.length - 1];

  return (
    <div className="absolute bottom-0 left-0 right-0 z-20 px-6 py-4 bg-space-elevated/90 backdrop-blur-sm border-t border-space-border">
      <div className="flex items-center gap-4 max-w-3xl mx-auto">
        <span className="text-sm text-slate-muted w-12 text-right">{min}</span>
        <input
          type="range"
          min={min}
          max={max}
          step={1}
          value={currentYear}
          onChange={(e) => onChange(Number(e.target.value))}
          className="flex-1"
          aria-label="Select year"
        />
        <span className="text-sm text-slate-muted w-12">{max}</span>
        <span className="font-serif text-lg font-semibold text-amber-warm w-16 text-center">
          {currentYear}
        </span>
      </div>
    </div>
  );
}
