"use client"

import { useState } from "react"
import { Card } from "@/components/ui/card"
import { Label } from "@/components/ui/label"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { PricingResults } from "@/components/pricing-results"
import { GreeksDisplay } from "@/components/greeks-display"
import { HedgingSimulator } from "@/components/hedging-simulator"
import { calculateBlackScholes, calculateBinomial } from "@/lib/pricing"

export function OptionsCalculator() {
  const [params, setParams] = useState({
    spotPrice: 100,
    strikePrice: 100,
    timeToMaturity: 1,
    riskFreeRate: 0.05,
    volatility: 0.2,
    optionType: "call" as "call" | "put",
    exerciseType: "european" as "european" | "american",
  })

  const [results, setResults] = useState<any>(null)
  const [model, setModel] = useState<"black-scholes" | "binomial">("black-scholes")

  const handleCalculate = () => {
    if (model === "black-scholes") {
      const result = calculateBlackScholes(params)
      setResults(result)
    } else {
      const result = calculateBinomial(params, 100)
      setResults(result)
    }
  }

  const updateParam = (key: string, value: any) => {
    setParams((prev) => ({ ...prev, [key]: value }))
  }

  return (
    <div className="space-y-8">
      <Card className="p-8 bg-card" id="calculator">
        <h2 className="font-[family-name:var(--font-fraunces)] text-3xl font-semibold mb-6">Pricing Calculator</h2>

        <div className="grid md:grid-cols-2 gap-6 mb-6">
          <div className="space-y-2">
            <Label htmlFor="spotPrice">Spot Price ($)</Label>
            <Input
              id="spotPrice"
              type="number"
              value={params.spotPrice}
              onChange={(e) => updateParam("spotPrice", Number.parseFloat(e.target.value))}
              className="font-mono"
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="strikePrice">Strike Price ($)</Label>
            <Input
              id="strikePrice"
              type="number"
              value={params.strikePrice}
              onChange={(e) => updateParam("strikePrice", Number.parseFloat(e.target.value))}
              className="font-mono"
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="timeToMaturity">Time to Maturity (years)</Label>
            <Input
              id="timeToMaturity"
              type="number"
              step="0.1"
              value={params.timeToMaturity}
              onChange={(e) => updateParam("timeToMaturity", Number.parseFloat(e.target.value))}
              className="font-mono"
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="volatility">Volatility (σ)</Label>
            <Input
              id="volatility"
              type="number"
              step="0.01"
              value={params.volatility}
              onChange={(e) => updateParam("volatility", Number.parseFloat(e.target.value))}
              className="font-mono"
            />
          </div>

          <div className="space-y-2">
            <Label htmlFor="riskFreeRate">Risk-Free Rate (%)</Label>
            <Input
              id="riskFreeRate"
              type="number"
              step="0.01"
              value={params.riskFreeRate * 100}
              onChange={(e) => updateParam("riskFreeRate", Number.parseFloat(e.target.value) / 100)}
              className="font-mono"
            />
          </div>

          <div className="space-y-2">
            <Label>Option Type</Label>
            <div className="flex gap-2">
              <Button
                variant={params.optionType === "call" ? "default" : "outline"}
                onClick={() => updateParam("optionType", "call")}
                className="flex-1"
              >
                Call
              </Button>
              <Button
                variant={params.optionType === "put" ? "default" : "outline"}
                onClick={() => updateParam("optionType", "put")}
                className="flex-1"
              >
                Put
              </Button>
            </div>
          </div>
        </div>

        <div className="flex items-center gap-4 mb-6">
          <Label>Pricing Model:</Label>
          <div className="flex gap-2">
            <Button
              variant={model === "black-scholes" ? "default" : "outline"}
              onClick={() => setModel("black-scholes")}
              size="sm"
            >
              Black-Scholes
            </Button>
            <Button
              variant={model === "binomial" ? "default" : "outline"}
              onClick={() => setModel("binomial")}
              size="sm"
            >
              Binomial Tree
            </Button>
          </div>
        </div>

        <Button onClick={handleCalculate} className="w-full" size="lg">
          Calculate Option Price
        </Button>
      </Card>

      {results && (
        <>
          <PricingResults results={results} params={params} />
          <GreeksDisplay greeks={results.greeks} />
          <HedgingSimulator params={params} />
        </>
      )}
    </div>
  )
}
