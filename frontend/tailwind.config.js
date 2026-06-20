// tailwind.config.js
export default {
  content: ["./index.html", "./src/**/*.{vue,js,ts}"],
  theme: {
    extend: {
      colors: {
        income: "#22c55e",
        expense: "#ef4444",
      },
      backgroundImage: {
        "gradient-hero":
          "linear-gradient(135deg, #7c3aed 0%, #9333ea 50%, #8b5cf6 100%)",
      },
      boxShadow: {
        glow: "0 20px 40px rgba(124,58,237,0.35)",
      },
    },
  },
  plugins: [],
};
