'use client'

import { Inter } from 'next/font/google'
import { Providers } from './provider'
import { CssBaseline } from '@mui/material'
import { useTheme, ThemeProvider, createTheme } from '@mui/material/styles'
import Header from '@/components/Header'
import darkTheme from '@/themes/darkTheme';
import lightTheme from '@/themes/lightTheme'
import React from 'react'

const inter = Inter({ subsets: ['latin'] })

const ColorModeContext = React.createContext({ toggleColorMode: () => {} });

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const [mode, setMode] = React.useState<'light' | 'dark'>('dark');
  const colorMode = React.useMemo(
    () => ({
      toggleColorMode: () => {
        setMode((prevMode) => (prevMode === 'light' ? 'dark' : 'light'));
      },
    }),
    [],
  );

  const darkThemeChosen = React.useMemo(
    () =>
      createTheme({
        ...darkTheme
      }),
    [],
  );
  const lightThemeChosen = React.useMemo(
    () =>
      createTheme({
        ...lightTheme
      }),
    [],
  );

  return (
    <html lang="en">
      <body className={inter.className}>
        <ColorModeContext.Provider value={colorMode}>
          <ThemeProvider theme={mode === 'dark' ? darkThemeChosen : lightThemeChosen}>
            <CssBaseline />
            <Providers>
              <Header ColorModeContext={ColorModeContext} />
              {children}
            </Providers>
          </ThemeProvider>
        </ColorModeContext.Provider>
      </body>
    </html>
  )
}
