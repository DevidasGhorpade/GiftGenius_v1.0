module.exports = {
  content: [
    './static/**/*.html',
    '.static/**/*.{html,js}'
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('@tailwindcss/forms','@tailwindcss/aspect-ratio')
  ],
}
