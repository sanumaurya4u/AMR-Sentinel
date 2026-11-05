import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        ink: {
          DEFAULT: "#102A43",
          light: "#243B53",
          dark: "#0A1B2A",
        },
        slate: {
          clinical: "#627D98",
          subtle: "#829AB1",
          light: "#BCCCDC",
        },
        canvas: "#F7FAFC",
        surface: "#FFFFFF",
        primary: {
          DEFAULT: "#0F766E",
          hover: "#0D655E",
          subtle: "#CCFBF1",
        },
        info: {
          DEFAULT: "#2563EB",
          subtle: "#EFF6FF",
        },
        review: {
          DEFAULT: "#B45309",
          subtle: "#FEF3C7",
          border: "#FCD34D",
        },
        urgent: {
          DEFAULT: "#B42318",
          subtle: "#FEE2E2",
          border: "#FCA5A5",
        },
        success: {
          DEFAULT: "#15803D",
          subtle: "#DCFCE7",
          border: "#86EFAC",
        },
        border: {
          DEFAULT: "#D9E2EC",
          subtle: "#E2E8F0",
        },
      },
      fontFamily: {
        sans: ["Inter", "-apple-system", "BlinkMacSystemFont", "Segoe UI", "Roboto", "sans-serif"],
      },
    },
  },
  plugins: [],
};

export default config;
