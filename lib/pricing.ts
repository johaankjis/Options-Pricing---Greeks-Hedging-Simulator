// Black-Scholes pricing implementation
export function calculateBlackScholes(params: {
  spotPrice: number
  strikePrice: number
  timeToMaturity: number
  riskFreeRate: number
  volatility: number
  optionType: "call" | "put"
}) {
  const { spotPrice: S, strikePrice: K, timeToMaturity: T, riskFreeRate: r, volatility: sigma, optionType } = params

  const d1 = (Math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * Math.sqrt(T))
  const d2 = d1 - sigma * Math.sqrt(T)

  const N = (x: number) => {
    const t = 1 / (1 + 0.2316419 * Math.abs(x))
    const d = 0.3989423 * Math.exp((-x * x) / 2)
    const prob = d * t * (0.3193815 + t * (-0.3565638 + t * (1.781478 + t * (-1.821256 + t * 1.330274))))
    return x > 0 ? 1 - prob : prob
  }

  let price: number
  let delta: number

  if (optionType === "call") {
    price = S * N(d1) - K * Math.exp(-r * T) * N(d2)
    delta = N(d1)
  } else {
    price = K * Math.exp(-r * T) * N(-d2) - S * N(-d1)
    delta = N(d1) - 1
  }

  // Calculate Greeks
  const gamma = Math.exp((-d1 * d1) / 2) / (S * sigma * Math.sqrt(2 * Math.PI * T))
  const vega = (S * Math.exp((-d1 * d1) / 2) * Math.sqrt(T)) / Math.sqrt(2 * Math.PI) / 100
  const theta = -(S * Math.exp((-d1 * d1) / 2) * sigma) / (2 * Math.sqrt(2 * Math.PI * T)) / 365
  const rho =
    optionType === "call" ? (K * T * Math.exp(-r * T) * N(d2)) / 100 : (-K * T * Math.exp(-r * T) * N(-d2)) / 100

  return {
    price,
    greeks: {
      delta,
      gamma,
      theta,
      vega,
      rho,
    },
  }
}

// Binomial tree pricing implementation
export function calculateBinomial(
  params: {
    spotPrice: number
    strikePrice: number
    timeToMaturity: number
    riskFreeRate: number
    volatility: number
    optionType: "call" | "put"
  },
  steps = 100,
) {
  const { spotPrice: S, strikePrice: K, timeToMaturity: T, riskFreeRate: r, volatility: sigma, optionType } = params

  const dt = T / steps
  const u = Math.exp(sigma * Math.sqrt(dt))
  const d = 1 / u
  const p = (Math.exp(r * dt) - d) / (u - d)

  // Build price tree
  const prices: number[][] = []
  for (let i = 0; i <= steps; i++) {
    prices[i] = []
    for (let j = 0; j <= i; j++) {
      prices[i][j] = S * Math.pow(u, j) * Math.pow(d, i - j)
    }
  }

  // Calculate option values at maturity
  const values: number[][] = []
  for (let i = 0; i <= steps; i++) {
    values[i] = []
  }

  for (let j = 0; j <= steps; j++) {
    if (optionType === "call") {
      values[steps][j] = Math.max(0, prices[steps][j] - K)
    } else {
      values[steps][j] = Math.max(0, K - prices[steps][j])
    }
  }

  // Backward induction
  for (let i = steps - 1; i >= 0; i--) {
    for (let j = 0; j <= i; j++) {
      values[i][j] = Math.exp(-r * dt) * (p * values[i + 1][j + 1] + (1 - p) * values[i + 1][j])
    }
  }

  const price = values[0][0]

  // Approximate Greeks using finite differences
  const delta = (values[1][1] - values[1][0]) / (prices[1][1] - prices[1][0])
  const gamma =
    ((values[2][2] - values[2][1]) / (prices[2][2] - prices[2][1]) -
      (values[2][1] - values[2][0]) / (prices[2][1] - prices[2][0])) /
    ((prices[2][2] - prices[2][0]) / 2)

  // Use Black-Scholes for other Greeks (approximation)
  const bsResult = calculateBlackScholes(params)

  return {
    price,
    greeks: {
      delta,
      gamma,
      theta: bsResult.greeks.theta,
      vega: bsResult.greeks.vega,
      rho: bsResult.greeks.rho,
    },
  }
}
