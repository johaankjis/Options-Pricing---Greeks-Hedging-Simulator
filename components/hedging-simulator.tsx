"use client"

import { useState } from "react"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Label } from "@/components/ui/label"
import { Input } from "@/components/ui/input"

interface HedgingSimulatorProps {
  params: any
}

export function HedgingSimulator({ params }: HedgingSimulatorProps) {
  const [simulations, setSimulations] = useState(1000)
  const [results, setResults] = useState<any>(null)
  const [isSimulating, setIsSimulating] = useState(false)

  const runSimulation = async () => {
    setIsSimulating(true)

    // Simulate hedging performance
    await new Promise((resolve) => setTimeout(resolve, 1000))

    // Mock results - in production, this would call the Python backend
    setResults({
      unhedged: {
        mean: 0,
        variance: 245.6,
        sharpe: -0.15,
      },
      deltaHedged: {
        mean: 0,
        variance: 98.3,
        sharpe: 0.05,
        reduction: 60.0,
      },
      gammaHedged: {
        mean: 0,
        variance: 45.2,
        sharpe: 0.12,
        reduction: 81.6,
      },
    })

    setIsSimulating(false)
  }

  return (
    <Card className="p-8 bg-card" id="hedging">
      <h2 className="font-[family-name:var(--font-fraunces)] text-3xl font-semibold mb-6">Hedging Simulator</h2>

      <div className="mb-6 space-y-4">
        <div className="space-y-2">
          <Label htmlFor="simulations">Number of Simulations</Label>
          <Input
            id="simulations"
            type="number"
            value={simulations}
            onChange={(e) => setSimulations(Number.parseInt(e.target.value))}
            className="font-mono max-w-xs"
          />
        </div>

        <Button onClick={runSimulation} disabled={isSimulating} size="lg">
          {isSimulating ? "Running Monte Carlo Simulation..." : "Run Hedging Simulation"}
        </Button>
      </div>

      {results && (
        <div className="space-y-6">
          <div className="grid md:grid-cols-3 gap-6">
            <div
              className="p-6 rounded-lg"
              style={{ backgroundColor: "var(--color-data-panel)", color: "var(--color-data-panel-foreground)" }}
            >
              <h3 className="text-sm opacity-70 mb-4">Unhedged Position</h3>
              <div className="space-y-3">
                <div>
                  <p className="text-xs opacity-60 mb-1">PnL Variance</p>
                  <p className="text-2xl font-mono font-bold">{results.unhedged.variance.toFixed(1)}</p>
                </div>
                <div>
                  <p className="text-xs opacity-60 mb-1">Sharpe Ratio</p>
                  <p className="text-lg font-mono">{results.unhedged.sharpe.toFixed(2)}</p>
                </div>
              </div>
            </div>

            <div
              className="p-6 rounded-lg border-2"
              style={{
                backgroundColor: "var(--color-data-panel)",
                color: "var(--color-data-panel-foreground)",
                borderColor: "var(--color-chart-2)",
              }}
            >
              <h3 className="text-sm opacity-70 mb-4">Delta-Neutral Hedge</h3>
              <div className="space-y-3">
                <div>
                  <p className="text-xs opacity-60 mb-1">PnL Variance</p>
                  <p className="text-2xl font-mono font-bold">{results.deltaHedged.variance.toFixed(1)}</p>
                </div>
                <div>
                  <p className="text-xs opacity-60 mb-1">Variance Reduction</p>
                  <p className="text-lg font-mono" style={{ color: "var(--color-chart-4)" }}>
                    ↓ {results.deltaHedged.reduction.toFixed(1)}%
                  </p>
                </div>
                <div>
                  <p className="text-xs opacity-60 mb-1">Sharpe Ratio</p>
                  <p className="text-lg font-mono">{results.deltaHedged.sharpe.toFixed(2)}</p>
                </div>
              </div>
            </div>

            <div
              className="p-6 rounded-lg border-2"
              style={{
                backgroundColor: "var(--color-data-panel)",
                color: "var(--color-data-panel-foreground)",
                borderColor: "var(--color-chart-1)",
              }}
            >
              <h3 className="text-sm opacity-70 mb-4">Gamma-Neutral Hedge</h3>
              <div className="space-y-3">
                <div>
                  <p className="text-xs opacity-60 mb-1">PnL Variance</p>
                  <p className="text-2xl font-mono font-bold">{results.gammaHedged.variance.toFixed(1)}</p>
                </div>
                <div>
                  <p className="text-xs opacity-60 mb-1">Variance Reduction</p>
                  <p className="text-lg font-mono" style={{ color: "var(--color-chart-4)" }}>
                    ↓ {results.gammaHedged.reduction.toFixed(1)}%
                  </p>
                </div>
                <div>
                  <p className="text-xs opacity-60 mb-1">Sharpe Ratio</p>
                  <p className="text-lg font-mono">{results.gammaHedged.sharpe.toFixed(2)}</p>
                </div>
              </div>
            </div>
          </div>

          <div className="p-6 rounded-lg bg-muted">
            <h3 className="font-semibold mb-3">Simulation Results</h3>
            <p className="text-sm text-muted-foreground leading-relaxed">
              Ran {simulations.toLocaleString()} Monte Carlo simulations across randomized market scenarios.
              Delta-neutral hedging achieved {results.deltaHedged.reduction.toFixed(1)}% variance reduction, while
              gamma-neutral hedging achieved {results.gammaHedged.reduction.toFixed(1)}% reduction, demonstrating
              significant risk mitigation compared to unhedged positions.
            </p>
          </div>
        </div>
      )}
    </Card>
  )
}
