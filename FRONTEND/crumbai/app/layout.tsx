import './globals.css'
import type { Metadata } from 'next'
import { Inter as FontSans } from "next/font/google"
import { cn } from "@/lib/utils"
import { ModalProvider } from '@/components/modal-provider'
import { ThemeProvider } from "@/components/theme-provider"

export const fontSans = FontSans({
  subsets: ["latin"],
  variable: "--font-sans",
})

export const metadata: Metadata = {
  title: 'CrumbAI',
  description: 'Content Generation with AI',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={cn(
          "min-h-screen bg-background font-sans antialiased",
          fontSans.variable
        )}>
          <ModalProvider />
          <ThemeProvider
            attribute="class"
            defaultTheme="system"
            enableSystem
            disableTransitionOnChange
          >
          {children}
        </ThemeProvider>
      </body>
    </html>
  )
}
