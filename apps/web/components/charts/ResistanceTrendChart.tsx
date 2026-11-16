"use client";

import React from "react";
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

const TREND_DATA = [
  { month: "Jun", accessRate: 52.1, watchRate: 43.4 },
  { month: "Jul", accessRate: 54.8, watchRate: 41.2 },
  { month: "Aug", accessRate: 58.2, watchRate: 37.9 },
  { month: "Sep", accessRate: 60.5, watchRate: 35.1 },
  { month: "Oct", accessRate: 62.3, watchRate: 33.5 },
  { month: "Nov", accessRate: 64.2, watchRate: 31.8 },
];

export function ResistanceTrendChart() {
  return (
    <div className="w-full h-72">
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={TREND_DATA} margin={{ top: 10, right: 20, left: 0, bottom: 0 }}>
          <defs>
            <linearGradient id="accessGrad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#059669" stopOpacity={0.4} />
              <stop offset="95%" stopColor="#059669" stopOpacity={0.0} />
            </linearGradient>
            <linearGradient id="watchGrad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#D97706" stopOpacity={0.4} />
              <stop offset="95%" stopColor="#D97706" stopOpacity={0.0} />
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="#E2E8F0" />
          <XAxis dataKey="month" stroke="#627D98" fontSize={11} />
          <YAxis domain={[20, 80]} stroke="#627D98" fontSize={11} unit="%" />
          <Tooltip
            contentStyle={{
              backgroundColor: "#FFFFFF",
              borderRadius: "0.75rem",
              border: "1px solid #D9E2EC",
              fontSize: "12px",
            }}
          />
          <Area
            type="monotone"
            dataKey="accessRate"
            name="Access Class %"
            stroke="#059669"
            strokeWidth={2.5}
            fillOpacity={1}
            fill="url(#accessGrad)"
            animationDuration={800}
          />
          <Area
            type="monotone"
            dataKey="watchRate"
            name="Watch Class %"
            stroke="#D97706"
            strokeWidth={2.5}
            fillOpacity={1}
            fill="url(#watchGrad)"
            animationDuration={800}
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}
