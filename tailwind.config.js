// Tailwind v4 uses a zero-config engine when used via CDN.
// For Vite + PostCSS, we still provide a minimal config to extend the theme.
/** @type {import('tailwindcss').Config} */
import preset from 'tailwindcss/preset'

export default {
    presets: [preset],
    content: [
        './index.html',
        './src/**/*.{vue,js,ts,jsx,tsx}',
    ],
    theme: {
        extend: {
            colors: {
                primary: {
                    DEFAULT: '#cf1d56',
                    dark: '#861f41',
                },
                secondary: {
                    DEFAULT: '#005D68',
                },
            },
        },
    },
    plugins: [],
}


