"use client";

import React from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

const DATA = [
  { rule: "Viral Bronchitis", count: 34, fill: "#B42318" },
  { rule: "Pediatric FQs", count: 28, fill: "#B42318" },
  { rule: "Renal eGFR Hold", count: 19, fill: "#B45309" },
  { rule: "Reserve Escalation", count: 12, fill: "#7C3AED" },
  { rule: "Banned FDC Combos", count: 8, fill: "#B42318" },
];

export function SafetyRuleBarChart() {
  return (
    <div className="w-full h-72">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={DATA} layout="vertical" margin={{ top: 10, right: 30, left: 30, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#E2E8F0" />
          <XAxis type="number" stroke="#627D98" fontSize={11} />
          <YAxis dataKey="rule" type="category" width={110} stroke="#627D98" fontSize={11} />
          <Tooltip
            formatter={(value: any) => [`${value}% of total alerts`, "Frequency"]}
            contentStyle={{
              backgroundColor: "#FFFFFF",
              borderRadius: "0.75rem",
              border: "1px solid #D9E2EC",
              fontSize: "12px",
            }}
          />
          <Bar dataKey="count" radius={[0, 8, 8, 0]} animationDuration={800} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}
