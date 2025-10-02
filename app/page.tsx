import { OptionsCalculator } from "@/components/options-calculator"
import { Header } from "@/components/header"

export default function Home() {
  return (
    <div className="min-h-screen">
      <Header />
      <main className="container mx-auto px-4 py-12 max-w-7xl">
        <div className="text-center mb-16 space-y-6">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-card border border-border text-sm text-muted-foreground mb-4">
            <span className="w-2 h-2 rounded-full bg-accent animate-pulse" />
            Powered by Black-Scholes & Binomial Tree Models
          </div>

          <h1 className="font-[family-name:var(--font-fraunces)] text-5xl md:text-7xl font-semibold text-balance leading-tight">
            Options Pricing & Hedging Simulator
          </h1>

          <p className="text-lg md:text-xl text-muted-foreground max-w-3xl mx-auto text-pretty leading-relaxed">
            Professional-grade options pricing engine with real-time Greeks computation, hedging strategies, and Monte
            Carlo simulations. Built for quant researchers, traders, and finance students.
          </p>
        </div>

        <OptionsCalculator />
      </main>

      <footer className="border-t border-border mt-24 py-8">
        <div className="container mx-auto px-4 text-center text-sm text-muted-foreground">
          <p>Built with Black-Scholes and Binomial Tree models • Accuracy ≤ 0.5% error</p>
        </div>
      </footer>
    </div>
  )
}
