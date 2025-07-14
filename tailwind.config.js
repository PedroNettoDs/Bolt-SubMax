/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./frontend/src/**/*.{js,ts,jsx,tsx}",
    "./Pages/templates/**/*.html",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
          800: '#1e40af',
          900: '#0d47a1', // Cor principal do projeto
        }
      }
    },
  },
  plugins: [],
}