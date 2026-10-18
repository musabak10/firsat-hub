import type { Config } from "tailwindcss";
export default {
  content: ["./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: { navy: { 900: "#0f1f3d", 800: "#1a2f5a", 700: "#24407a" }, steel: { 600: "#3b6ea5", 500: "#4a80b8", 100: "#e6eef7" } },
      fontFamily: { sans: ["var(--font-sans)", "system-ui", "sans-serif"] },
    },
  },
  plugins: [],
} satisfies Config;
