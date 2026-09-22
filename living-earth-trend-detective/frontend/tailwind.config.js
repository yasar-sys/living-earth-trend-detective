/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        space: {
          base: "#0B0E1A",
          elevated: "#121624",
          card: "#1A1F2E",
          border: "#2D3448",
        },
        slate: { muted: "#6B7280" },
        amber: { warm: "#F2A93B" },
        offwhite: { text: "#E8E6E1" },
        violet: { primary: "#7C6FF0" },
        rust: { muted: "#C4544A" },
      },
      fontFamily: {
        serif: ["Fraunces", "Georgia", "serif"],
        sans: ["Inter", "system-ui", "sans-serif"],
      },
      fontSize: {
        "heading-xl": ["clamp(2.25rem, 5vw, 4rem)", { lineHeight: "1.1", letterSpacing: "-0.02em" }],
        "heading-lg": ["clamp(1.5rem, 3vw, 2.5rem)", { lineHeight: "1.2" }],
        "body-lg": ["1.125rem", { lineHeight: "1.7" }],
        caption: ["0.75rem", { lineHeight: "1.5", letterSpacing: "0.08em" }],
      },
      animation: {
        "fade-in": "fadeIn 0.6s ease-out forwards",
        "slide-up": "slideUp 0.6s ease-out forwards",
        "pulse-slow": "pulse 3s ease-in-out infinite",
      },
      keyframes: {
        fadeIn: { "0%": { opacity: 0 }, "100%": { opacity: 1 } },
        slideUp: {
          "0%": { opacity: 0, transform: "translateY(20px)" },
          "100%": { opacity: 1, transform: "translateY(0)" },
        },
      },
    },
  },
  plugins: [],
};
