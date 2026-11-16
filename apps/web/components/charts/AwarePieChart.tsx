"use client";

import React from "react";
import {
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
  Tooltip,
  Legend,
} from "recharts";

const DATA = [
  { name: "Access (First-line)", value: 64.2, color: "#059669", target: "≥60% Target" },
  { name: "Watch (High Resistance)", value: 31.8, color: "#D97706", target: "De-escalate" },
  { name: "Reserve (Last Resort)", value: 4.0, color: "#7C3AED", target: "Strict Hold" },
];

interface CustomTooltipProps {
  active?: boolean;
  payload?: Array<{
    name: string;
    value: number;
    payload: {
      color: string;
      target: string;
    };
  }>;
}

function CustomTooltip({ active, payload }: CustomTooltipProps) {
  if (active && payload && payload.length) {
    const data = payload[0];
    return (
      <div className="rounded-xl border border-border bg-surface p-3 shadow-lg text-xs">
        <p className="font-bold text-ink" style={{ color: data.payload.color }}>
          {data.name}
        </p>
        <p className="text-sm font-extrabold text-ink mt-0.5">{data.value}%</p>
        <p className="text-[11px] text-slate-clinical mt-0.5">
          Benchmark: {data.payload.target}
        </p>
      </div>
    );
  }
  return null;
}

export function AwarePieChart() {
  return (
    <div className="w-full h-72">
      <ResponsiveContainer width="100%" height="100%">
        <PieChart>
          <Pie
            data={DATA}
            cx="50%"
            cy="50%"
            innerRadius={65}
            outerRadius={95}
            paddingAngle={4}
            dataKey="value"
            animationDuration={800}
          >
            {DATA.map((entry) => (
              <Cell key={entry.name} fill={entry.color} stroke="#FFFFFF" strokeWidth={2} />
            ))}
          </Pie>
          <Tooltip content={<CustomTooltip />} />
          <Legend
            verticalAlign="bottom"
            height={36}
            formatter={(value) => (
              <span className="text-xs font-semibold text-ink">{value}</span>
            )}
          />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}
