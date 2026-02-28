# Optimal Market Making on Crypto Markets
### Cartea-Jaimungal Framework — BTC/USDT 1-Second Data

[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## Overview

This project implements and backtests three market-making strategies on BTC/USDT 1-second candle data (Binance, Jul–Dec 2025), following the theoretical framework of **Cartea & Jaimungal (2015)**.

The core idea: a market maker posts limit orders at optimal bid/ask quotes derived from the HJB equation, balancing spread capture against inventory risk. We progressively relax the pure martingale assumption by introducing a stochastic alpha signal driven by **Order Flow Imbalance (OFI)**.

**Three model specifications, in increasing complexity:**

| Model | Alpha signal | OOS Net P&L | Sharpe (OOS) | Frictions/session |
|---|---|---|---|---|
| AS pure | None | −$428 | −1.85 | $79 |
| CJ + EWMA | EWMA of OFI | +$15,281 | +3.79 | $132 |
| CJ + OU-Jumps | OU process + marked Poisson jumps | +$8,745 | +2.34 | $67 |

> **IS**: Jul–Nov 2025 (153 sessions, 13.2M candles) · **OOS**: Dec 2025 (31 sessions, 2.7M candles)

---

## Theoretical Framework

### Asset price dynamics

$$dS_t = (\nu + \alpha_t)\,dt + \sigma\,dW_t$$

where $\nu = 0$ at the intraday horizon, and $\alpha_t$ is the stochastic drift signal.

### Optimal quotes — Guéant, Lehalle & Fernandez-Tapia (2013)

```math
r(t,q) = S_t + \frac{\alpha_t}{\rho}\left(1 - e^{-\rho(T-t)}\right) - q\gamma\sigma^2(T-t)
```
```math
\psi^*(t) = \gamma\sigma^2(T-t) + \frac{2}{\gamma}\ln\left(1 + \frac{\gamma}{\kappa}\right)
```
```math
b^* = r - \frac{\psi^*}{2}, \quad a^* = r + \frac{\psi^*}{2}
```

### Alpha signal models

**Model 2 — EWMA:**
$$\hat{\alpha}_t = \text{EWMA}(\text{OFI}_t, \text{span}^*)$$

**Model 3 — OU + Jumps (Cartea-Jaimungal §10.4.2):**
$$d\alpha_t = -\zeta\,\alpha_t\,dt + \eta\,dW_t^\alpha + \xi^+\,dM^+_t - \xi^-\,dM^-_t$$

where $M^\pm$ are Poisson processes counting buy/sell market orders and $\xi^\pm \sim \text{Exp}(\bar{\xi}^\pm)$.

---

## Calibration — Method of Moments

All parameters are calibrated from in-sample data only (strict IS/OOS split):

| Parameter | Method | Value |
|---|---|---|
| $\kappa$ | Brentq on stationary spread equation | 2,251,049 |
| $A$ | Fill prob target at half-spread | 0.091 fills/sec |
| $\rho$, $\zeta$ | $-\ln(\text{autocorr}(\text{OFI}, 1))$ | 1.96 /sec |
| $\eta$ | Innovation variance of OU residuals | 0.836 |
| $\lambda^\pm$ | Fraction of candles with \|OFI\| > 0.5 | 0.40 /sec |
| $\xi^\pm$ | Conditional mean OFI above threshold | 0.93 |
| span* | Grid search over corr(EWMA(OFI), $r_{t+1}$) | 2 seconds |

> Signal half-life: **0.35 seconds** — consistent with the microstructure literature on OFI predictability.

---

## Friction Model

Three components of realistic transaction costs are modelled explicitly:

| Component | Implementation | OOS avg (CJ+EWMA) |
|---|---|---|
| Commission | Binance maker: $0.02 × lot_size | $9.1/session |
| Slippage | $\mathcal{N}(0,\, \sigma_{\text{exec}})$, lag ~ U[50ms, 200ms] | $66.3/session |
| Adverse selection | Fraction of forward price move post-fill | $56.5/session |

**Key finding:** frictions represent 147% of gross P&L for AS pure, but only 11–12% for the CJ models — the alpha signal makes the strategy viable.

---

## Repository Structure

```
.
├── src/
│   ├── visualization.py     # plot_results() — shared across models
│   └── utils.py             # export_trade_logs()
│
├── scripts/
│   ├── AS_MM_Engine.ipynb
│   ├── CJ_EWMA_MM_Engine.ipynb
│   └── CJ_Jumps_MM_Engine.ipynb
│
├── results/
│   ├── metrics/
│   ├── plots/
│   └── trade_logs/
│
├── data.zip                    # not tracked (Parquet files)
├── requirements.txt
└── README.md
```

---
## Data

* BTC/USDT 1-second OHLCV candles sourced from the [Binance Data Portal](https://data.binance.vision/).
* ETH/USDT 1-second OHLCV candles sourced from the [Binance Data Portal](https://data.binance.vision/).

Each candle includes a pre-computed **Order Flow Imbalance** column:

$$\text{OFI}_t = \frac{V_t^{\text{buy}} - V_t^{\text{sell}}}{V_t^{\text{buy}} + V_t^{\text{sell}}}$$

---

## Requirements

```
numpy
pandas
scipy
scikit-learn
matplotlib
pyarrow
```

---

## References

- Avellaneda, M. & Stoikov, S. (2008). *High-frequency trading in a limit order book.* Quantitative Finance, 8(3), 217–224.
- Cartea, Á. & Jaimungal, S. (2015). *Algorithmic and High-Frequency Trading.* Cambridge University Press. (§10.4)
- Guéant, O., Lehalle, C.-A. & Fernandez-Tapia, J. (2013). *Dealing with the inventory risk.* Mathematics and Financial Economics, 7(4), 477–507.
- Cont, R., Kukanov, A. & Stoikov, S. (2014). *The price impact of order book events.* Journal of Financial Econometrics, 12(1), 47–88.

---

## License

MIT
