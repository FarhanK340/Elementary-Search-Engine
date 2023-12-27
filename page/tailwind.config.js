/** @type {import('tailwindcss').Config} */

module.exports = {
  content: ["*"],
  theme: {
    borderRadius: {
      '4xl': '2.5rem'  
    },
    width:{
      'w-45': '45%'
    },
    extend: {
      boxShadow: {
        '4xl': '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 15px 15px -5px rgba(0, 0, 0, 1)',
      },
      transitionDelay: {
        'transitionDelay' : '1000ms'
      }
    },
  },
  plugins: [],
}
