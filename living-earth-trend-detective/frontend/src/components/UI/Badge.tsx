import type { Significance } from "@/types";

const classMap: Record<Significance, string> = {
  significant: "badge-significant",
  not_significant: "badge-not-significant",
  insufficient_data: "badge-insufficient",
};

const labelMap: Record<Significance, string> = {
  significant: "Significant",
  not_significant: "Not significant",
  insufficient_data: "Insufficient data",
};

export default function SignificanceBadge({ significance }: { significance: Significance }) {
  return (
    <span
      className={`inline-block px-3 py-1 rounded-full text-xs font-medium ${classMap[significance]}`}
    >
      {labelMap[significance]}
    </span>
  );
}
