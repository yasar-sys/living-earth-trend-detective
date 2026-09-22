import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import type { TimeSeriesPoint } from "@/types";

export default function TrendChart({ data, unit }: { data: TimeSeriesPoint[]; unit: string }) {
  return (
    <div className="w-full h-56">
      <ResponsiveContainer width="100%" height="100%">
        <LineChart data={data} margin={{ top: 8, right: 12, left: -12, bottom: 0 }}>
          <CartesianGrid stroke="#2D3448" strokeDasharray="3 3" />
          <XAxis dataKey="year" stroke="#6B7280" fontSize={11} tickLine={false} />
          <YAxis
            stroke="#6B7280"
            fontSize={11}
            tickLine={false}
            width={44}
            tickFormatter={(v) => `${v}`}
          />
          <Tooltip
            contentStyle={{
              background: "rgba(18,22,36,0.95)",
              border: "1px solid #2D3448",
              borderRadius: 8,
              fontSize: 12,
            }}
            labelStyle={{ color: "#F2A93B" }}
            formatter={(value: number) => [`${value} ${unit}`, "Value"]}
          />
          <Line
            type="monotone"
            dataKey="value"
            stroke="#7C6FF0"
            strokeWidth={2}
            dot={false}
            activeDot={{ r: 4, fill: "#F2A93B" }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
