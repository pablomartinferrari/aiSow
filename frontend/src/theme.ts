import { createTheme } from '@mui/material/styles';

export const theme = createTheme({
    palette: {
        primary: {
            main: '#232946',
            light: '#4a4f6d',
            dark: '#121629',
        },
        secondary: {
            main: '#eebbc3',
            light: '#ffeef2',
            dark: '#ba8a97',
        },
        background: {
            default: '#fffffe',
            paper: '#f8f8f8',
        },
        text: {
            primary: '#232946',
            secondary: '#4a4f6d',
        },
    },
    typography: {
        fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
        h1: {
            fontSize: '2.5rem',
            fontWeight: 600,
        },
        h2: {
            fontSize: '2rem',
            fontWeight: 500,
        },
        h3: {
            fontSize: '1.75rem',
            fontWeight: 500,
        },
    },
    components: {
        MuiButton: {
            styleOverrides: {
                root: {
                    borderRadius: 8,
                    textTransform: 'none',
                },
            },
        },
        MuiCard: {
            styleOverrides: {
                root: {
                    borderRadius: 12,
                    boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
                },
            },
        },
    },
});
