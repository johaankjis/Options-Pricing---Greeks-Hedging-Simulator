export function Header() {
  return (
    <header className="border-b border-border bg-card/50 backdrop-blur-sm sticky top-0 z-50">
      <div className="container mx-auto px-4 py-4 flex items-center justify-between max-w-7xl">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-lg bg-primary flex items-center justify-center">
            <span className="text-primary-foreground font-mono font-bold text-sm">Ω</span>
          </div>
          <span className="font-[family-name:var(--font-fraunces)] font-semibold text-lg">Options Simulator</span>
        </div>

        <nav className="hidden md:flex items-center gap-6 text-sm">
          <a href="#calculator" className="text-muted-foreground hover:text-foreground transition-colors">
            Calculator
          </a>
          <a href="#greeks" className="text-muted-foreground hover:text-foreground transition-colors">
            Greeks
          </a>
          <a href="#hedging" className="text-muted-foreground hover:text-foreground transition-colors">
            Hedging
          </a>
        </nav>

        <button className="px-4 py-2 rounded-lg bg-primary text-primary-foreground text-sm font-medium hover:opacity-90 transition-opacity">
          Documentation
        </button>
      </div>
    </header>
  )
}
