import { Card } from "@/components/ui/card"

interface PricingResultsProps {
  results: {
    price: number
    greeks: any
  }
  params: any
}

export function PricingResults({ results, params }: PricingResultsProps) {
  return (
    <Card
      className="p-8"
      style={{ backgroundColor: "var(--color-data-panel)", color: "var(--color-data-panel-foreground)" }}
    >
      <h2 className="font-[family-name:var(--font-fraunces)] text-3xl font-semibold mb-6">Pricing Results</h2>

      <div className="grid md:grid-cols-3 gap-6">
        <div className="space-y-2">
          <p className="text-sm opacity-70">Option Price</p>
          <p className="text-4xl font-mono font-bold">${results.price.toFixed(4)}</p>
        </div>

        <div className="space-y-2">
          <p className="text-sm opacity-70">Intrinsic Value</p>
          <p className="text-2xl font-mono">
            $
            {Math.max(
              params.optionType === "call"
                ? params.spotPrice - params.strikePrice
                : params.strikePrice - params.spotPrice,
              0,
            ).toFixed(4)}
          </p>
        </div>

        <div className="space-y-2">
          <p className="text-sm opacity-70">Time Value</p>
          <p className="text-2xl font-mono">
            $
            {(
              results.price -
              Math.max(
                params.optionType === "call"
                  ? params.spotPrice - params.strikePrice
                  : params.strikePrice - params.spotPrice,
                0,
              )
            ).toFixed(4)}
          </p>
        </div>
      </div>

      <div className="mt-8 pt-8 border-t border-border/20">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
          <div>
            <p className="opacity-70 mb-1">Spot Price</p>
            <p className="font-mono">${params.spotPrice}</p>
          </div>
          <div>
            <p className="opacity-70 mb-1">Strike Price</p>
            <p className="font-mono">${params.strikePrice}</p>
          </div>
          <div>
            <p className="opacity-70 mb-1">Time to Maturity</p>
            <p className="font-mono">{params.timeToMaturity}y</p>
          </div>
          <div>
            <p className="opacity-70 mb-1">Volatility</p>
            <p className="font-mono">{(params.volatility * 100).toFixed(1)}%</p>
          </div>
        </div>
      </div>
    </Card>
  )
}
