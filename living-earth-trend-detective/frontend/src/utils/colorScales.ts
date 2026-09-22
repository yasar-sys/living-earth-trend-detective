/** Maps a value within [min, max] to a color from a given scale array. */
export function valueToColor(
  value: number,
  min: number,
  max: number,
  scale: string[]
): string {
  if (max === min) return scale[Math.floor(scale.length / 2)];
  const t = Math.max(0, Math.min(1, (value - min) / (max - min)));
  const idx = Math.min(scale.length - 1, Math.floor(t * scale.length));
  return scale[idx];
}
