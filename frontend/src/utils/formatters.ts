export function formatSlope(slope: number, unit: string): string {
  const sign = slope > 0 ? "+" : "";
  return `${sign}${slope.toFixed(3)} ${unit}/decade`;
}

export function formatPValue(p: number): string {
  if (p < 0.001) return "p < 0.001";
  return `p = ${p.toFixed(3)}`;
}

export function significanceLabel(sig: string): string {
  switch (sig) {
    case "significant":
      return "Statistically significant trend";
    case "not_significant":
      return "Not statistically significant";
    default:
      return "Insufficient data";
  }
}
