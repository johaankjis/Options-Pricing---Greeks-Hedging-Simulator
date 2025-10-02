import type React from "react"
import type { Metadata } from "next"
import { GeistSans } from "geist/font/sans"
import { GeistMono } from "geist/font/mono"
import { Fraunces } from "next/font/google"
import { Analytics } from "@vercel/analytics/next"
import "./globals.css"
import { ClientLayoutWrapper } from "./ClientLayoutWrapper"

const fraunces = Fraunces({
  subsets: ["latin"],
  variable: "--font-fraunces",
  display: "swap",
})

export const metadata: Metadata = {
  title: "Options Pricing Simulator",
  description: "Professional options pricing and hedging simulator with Black-Scholes and binomial tree models",
  generator: "v0.app",
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en">
      <body className={`font-sans ${GeistSans.variable} ${GeistMono.variable} ${fraunces.variable}`}>
        <ClientLayoutWrapper>{children}</ClientLayoutWrapper>
        <Analytics />
      </body>
    </html>
  )
}
