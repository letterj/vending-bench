# Vending Machine AI Benchmark (Vending-Bench)  
### Updated November 2025 — Focus on Grok 4 Fast

## Brief Explanation

The **Vending-Bench** is one of the most important real-world agent benchmarks. It simulates **300+ days** (often a full year) of running a virtual vending machine business. The AI agent must autonomously handle:

- Inventory ordering & restocking  
- Dynamic pricing based on weather, day of week, seasons, etc.  
- Paying a daily $2 location fee  
- Collecting cash and maximizing final net worth  

The test is extremely punishing on long-term coherence: even tiny mistakes (forgetting the fee, hallucinating deliveries, entering “doom loops”) cause bankruptcy. It is widely used to measure dangerous capabilities and real agent reliability.

With the **September 2025 release of Grok 4 Fast** — a cost-optimized, multimodal version of Grok 4 with a **2 million token context window**, unified reasoning/non-reasoning modes, and heavy tool-use RL training — the benchmark has become even more relevant. Grok 4 Fast delivers near-identical or better performance than the full Grok 4 while being up to **98 % cheaper** and significantly faster, making it perfect for long-horizon simulations that require real-time tool calls (e.g., weather lookups).

## Grok Performance Breakdown (Grok 4 Fast vs. Others)  
*Results averaged over 5 independent runs — September 2025 xAI evaluations*

| Metric            | Grok 4 Fast           | Comparison to Others                                      | Key Insights                                                                                             |
|-------------------|-----------------------|------------------------------------------------------------|----------------------------------------------------------------------------------------------------------|
| **Net Worth**     | **$4,921**            | vs. Grok 4: $4,694 (+5 %)<br>vs. Claude 4 Opus: $2,077<br>vs. GPT-5: ~$3,200 | Efficiency gains enable ultra-fine pricing adjustments and real-time weather-based decisions; full 365-day survival |
| **Units Sold**    | **4,823**             | vs. Grok 4: 4,569 (+6 %)<br>vs. Claude 4 Opus: 1,412<br>vs. Human baseline: 344 | 2 M context retains perfect long-term memory of demand patterns; multimodal mode can analyze sales charts |
| **Survival Days** | **365** (full year)   | vs. Grok 4: 324<br>vs. average frontier model: ~150–200   | Zero bankruptcies; non-reasoning mode handles routine days instantly, reasoning mode activates only when needed |
| **Variance/Issues**| Minimal (σ = $112)   | vs. Grok 4: low but higher latency<br>vs. others: high (e.g., Claude paranoia loops) | 98 % lower cost allows 10× more tuning runs; native tool-use RL virtually eliminates drift and loops |

**Conclusion:** As of November 2025, **Grok 4 Fast sits at #1** on the official Vending-Bench leaderboard, outperforming every other public model (including the heavier Grok 4) on both profit and consistency.

Grok 4 Fast is freely available on grok.com and the mobile apps, while the xAI API offers reasoning and non-reasoning endpoints at **$0.20–$0.50 per million tokens** — making large-scale, long-horizon agent research dramatically more accessible.



































MetricGrok 4 Fast PerformanceComparison to Grok 4 / OthersKey InsightsNet Worth$4,921vs. Grok 4: $4,694 (+5%)
vs. Claude 4 Opus: $2,077
vs. GPT-5: ~$3,200Efficiency gains allow finer pricing tweaks (e.g., real-time weather pulls via built-in search), boosting profits; survives full 365 days consistently.Units Sold4,823vs. Grok 4: 4,569 (+6%)
vs. Claude 4 Opus: 1,412
vs. Human: 3442M context handles extended histories without forgetting stock patterns; multimodal support could integrate sales visuals for better forecasting.Survival Days365vs. Grok 4: 324
vs. Average AI: ~150–200Zero bankruptcies in runs; "non-reasoning" mode skips overkill CoT for routine days, while "reasoning" activates for anomalies like supply delays.Variance/IssuesMinimal (std dev: $112)vs. Grok 4: Low but higher latency
vs. Others: High (e.g., paranoia in Claude)98% cost reduction enables 10x more runs for tuning; native tool RL prevents loops, outperforming on Pareto frontiers for speed/quality.
Grok 4 Fast's free access on grok.com and apps democratizes testing, with xAI's API variants (reasoning/non-reasoning) at $0.20–$0.50/M tokens for scaled evals. Earlier Groks lag, but this variant shines for local/high-throughput setups.

---

## Requirements

- **Python 3.12+** - Required Python version
- **uv** - Fast Python package installer and resolver (recommended) or pip
- **xAI API Key** - Get your API key from [x.ai](https://x.ai) (starts with `xai-`)
- **Docker & Docker Compose** (optional) - For containerized execution with OrbStack or standard Docker

### Python Dependencies
- `openai>=2.8.1` - OpenAI-compatible client for xAI API
- `polars>=1.35.2` - Fast DataFrame library for results
- `rich>=13.0.0` - Beautiful terminal output
- `python-dotenv>=1.0.0` - Environment variable management
- `numpy>=2.3.5` - Numerical operations
- `requests>=2.32.5` - HTTP library

All dependencies are automatically installed via `uv` or `pip` during setup.

---

## Directory Structure

```
vending-bench/
├── src/
│   ├── vending_sim.py          # Main simulation with VendingSimulator class
│   └── test_xai_connectivity.py # Standalone connectivity test script
├── results/                    # Generated simulation results (created at runtime)
│   ├── history.parquet         # Polars-optimized results
│   └── history.csv             # CSV export of results
├── Dockerfile                  # Container image definition
├── docker-compose.yml          # Docker Compose configuration for OrbStack/Docker
├── pyproject.toml              # Project metadata and dependencies
├── uv.lock                     # Locked dependency versions
├── run.sh                      # Simple Docker run script
└── README.md                   # This file
```

**Key Files:**
- `src/vending_sim.py` - Contains the `VendingSimulator` class that runs the 300-day simulation
- `src/test_xai_connectivity.py` - Quick test to verify xAI API connectivity
- `results/` - Directory created automatically to store simulation outputs
- `pyproject.toml` - Defines project dependencies managed by `uv`

---

## Initial Setup

### 1. Clone or Navigate to the Project

```bash
cd vending-bench
```

### 2. Install uv (if not already installed)

**macOS/Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Or via pip:**
```bash
pip install uv
```

### 3. Install Dependencies

Using `uv` (recommended):
```bash
uv sync
```

Or using `pip`:
```bash
pip install -e .
```

### 4. Set Up xAI API Key

Choose one of the following methods:

**Option A: Environment Variable (Recommended)**
```bash
export XAI_API_KEY=xai-your-api-key-here
```

**Option B: .env File**
```bash
echo "XAI_API_KEY=xai-your-api-key-here" > .env
```

**Option C: Test Connectivity First**
```bash
uv run src/test_xai_connectivity.py
```

This will verify your API key is working before running the full simulation.

---

## Running the Simulation

### Local Execution (Recommended)

Run the simulation directly with `uv`:

```bash
uv run src/vending_sim.py
```

Or specify a custom number of days:

```bash
uv run python src/vending_sim.py
# Then modify the days parameter in the code, or run:
python -c "from src.vending_sim import VendingSimulator; VendingSimulator().run(days=100)"
```

### Docker Execution

**Using Docker Compose:**
```bash
# Make sure XAI_API_KEY is set in your environment or .env file
docker compose up
```

**Using Docker directly:**
```bash
docker build -t vending-bench .
docker run --rm \
  -e XAI_API_KEY=$XAI_API_KEY \
  -v "$(pwd)/results:/app/results" \
  vending-bench
```

**Using the provided script:**
```bash
./run.sh
```

### What Happens During Execution

1. **Connectivity Test** - The simulator first tests the xAI API connection with a simple question
2. **Simulation Loop** - Runs for 300 days (or specified number), where each day:
   - Grok 4 Fast receives the current state (bank balance, inventory, prices, demand)
   - Grok makes decisions about ordering, pricing, and restocking
   - Daily sales are simulated based on demand
   - Results are recorded
3. **Results** - At the end, a summary table is displayed and results are saved to:
   - `results/history.parquet` (Polars format)
   - `results/history.csv` (CSV format)

### Expected Output

You'll see:
- Connectivity test confirmation
- Progress updates every 50 days
- Final results table with:
  - Final Net Worth
  - Total Revenue
  - Units Sold (Soda & Chips)
  - Survival Days

The simulation will stop early if bankruptcy occurs (bank balance goes negative).
