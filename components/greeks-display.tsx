import { Card } from "@/components/ui/card"

interface GreeksDisplayProps {
  greeks: {
    delta: number
    gamma: number
    theta: number
    vega: number
    rho: number
  }
}

export function GreeksDisplay({ greeks }: GreeksDisplayProps) {
  const greeksData = [
    {
      name: "Delta (Δ)",
      value: greeks.delta,
      description: "Price sensitivity to underlying",
      format: (v: number) => v.toFixed(4),
    },
    {
      name: "Gamma (Γ)",
      value: greeks.gamma,
      description: "Rate of change of delta",
      format: (v: number) => v.toFixed(4),
    },
    {
      name: "Theta (Θ)",
      value: greeks.theta,
      description: "Time decay per day",
      format: (v: number) => v.toFixed(4),
    },
    {
      name: "Vega (ν)",
      value: greeks.vega,
      description: "Sensitivity to volatility",
      format: (v: number) => v.toFixed(4),
    },
    {
      name: "Rho (ρ)",
      value: greeks.rho,
      description: "Sensitivity to interest rate",
      format: (v: number) => v.toFixed(4),
    },
  ]

  return (
    <Card className="p-8 bg-card" id="greeks">
      <h2 className="font-[family-name:var(--font-fraunces)] text-3xl font-semibold mb-6">Greeks Analysis</h2>

      <div className="grid md:grid-cols-5 gap-6">
        {greeksData.map((greek) => (
          <div
            key={greek.name}
            className="p-6 rounded-lg"
            style={{ backgroundColor: "var(--color-data-panel)", color: "var(--color-data-panel-foreground)" }}
          >
            <p className="text-sm opacity-70 mb-2">{greek.name}</p>
            <p className="text-3xl font-mono font-bold mb-2">{greek.format(greek.value)}</p>
            <p className="text-xs opacity-60">{greek.description}</p>
          </div>
        ))}
      </div>

      <div className="mt-8 p-6 rounded-lg bg-muted">
        <h3 className="font-semibold mb-3">Understanding Greeks</h3>
        <p className="text-sm text-muted-foreground leading-relaxed">
          Greeks measure the sensitivity of an option's price to various factors. Delta shows how much the option price
          changes with the underlying asset. Gamma measures the rate of change of delta. Theta represents time decay.
          Vega shows sensitivity to volatility changes, and Rho measures interest rate sensitivity.
        </p>
      </div>
    </Card>
  )
}
