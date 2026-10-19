/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        nordic: {
          blue: '#00A9CE',
          dark: '#002B49',
          light: '#E6F4F8'
        }
      }
    },
  },
  plugins: [],
}
