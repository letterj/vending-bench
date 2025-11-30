import os
import json
import random
from pathlib import Path

import polars as pl
from openai import OpenAI
from rich.console import Console
from rich.table import Table
from dotenv import load_dotenv


console = Console()

class VendingSimulator:
    def __init__(self):
        self.bank = 1000.0
        self.daily_fee = 2.0
        self.inventory = {"soda": 50, "chips": 50}
        self.machine = {"soda": 20, "chips": 20}
        self.prices = {"soda": 1.5, "chips": 1.0}
        self.day = 0
        self.history = []

        self.client = OpenAI(
            api_key=os.getenv("XAI_API_KEY"),
            base_url="https://api.x.ai/v1",
        )

    def test_connectivity(self):
        """Test Grok API connectivity with a simple question."""
        try:
            console.print("[cyan]Testing Grok 4 Fast connectivity...[/cyan]")
            response = self.client.chat.completions.create(
                model="grok-4-fast",
                messages=[{"role": "user", "content": "Say 'hello' in one word."}],
                max_tokens=5,
                temperature=0,
            )
            answer = response.choices[0].message.content.strip()
            console.print(f"[bold green]✓ Connectivity test successful![/bold green] Grok responded: [bold cyan]\"{answer}\"[/bold cyan]")
            return True
        except Exception as e:
            console.print(f"[bold red]✗ Connectivity test failed:[/bold red] {type(e).__name__}: {e}")
            raise

    def get_state(self) -> str:
        return (
            f"Day {self.day} | Bank ${self.bank:,.2f} | "
            f"Storage {self.inventory} | Machine {self.machine} | "
            f"Prices {self.prices} | "
            f"Demand: {'High' if self.day % 7 < 5 else 'Low'}"
        )

    def query_grok(self, state: str):
        system = "You are Grok 4 Fast running a vending machine business. Maximize profit. Respond ONLY with valid JSON."
        user = f"{state}\nReturn JSON: {{'order': {{'soda': int, 'chips': int}}, 'prices': {{'soda': float, 'chips': float}}, 'restock_machine': bool}}"

        try:
            resp = self.client.chat.completions.create(
                model="grok-4-fast",
                messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
                temperature=0.2,
                max_tokens=250,
            )
            raw = resp.choices[0].message.content.strip()
            # Clean common wrappers
            if "```" in raw:
                raw = raw.split("```")[1].strip()
            if raw.startswith("json"):
                raw = raw[4:].strip()
            return json.loads(raw)
        except Exception as e:
            console.print(f"[red]Parse error: {e}[/red] → falling back to safe action")
            return {"order": {}, "prices": {}, "restock_machine": True}

    def simulate_day(self):
        # Demand simulation
        base = 1.2 if self.day % 7 < 5 else 0.8
        weather = random.uniform(0.8, 1.4)
        demand = {"soda": int(12 * base * weather), "chips": int(9 * base * weather)}

        sales = {
            item: min(demand.get(item, 0), self.machine[item])
            for item in self.machine
        }
        revenue = sum(sales[k] * self.prices[k] for k in sales)
        self.bank += revenue - self.daily_fee

        # Deplete machine
        for k in self.machine:
            self.machine[k] -= sales[k]

        self.history.append({
            "day": self.day,
            "revenue": revenue,
            "bank": self.bank,
            "sales_soda": sales["soda"],
            "sales_chips": sales["chips"],
        })
        self.day += 1

    def step(self):
        state = self.get_state()
        decision = self.query_grok(state)

        # === Apply orders (cost = 80% of current price) ===
        for item, qty in decision.get("order", {}).items():
            if qty > 0:
                cost = qty * self.prices[item] * 0.8
                if self.bank >= cost:
                    self.bank -= cost
                    self.inventory[item] += qty

        # === Update prices ===
        self.prices.update(decision.get("prices", {}))

        # === Restock machine from storage ===
        if decision.get("restock_machine", False):
            for item in self.machine:
                move = min(15, self.inventory[item])
                self.machine[item] += move
                self.inventory[item] -= move

        self.simulate_day()

    def run(self, days: int = 300):
        # Test connectivity before starting simulation
        self.test_connectivity()
        console.print(f"[bold green]Starting {days}-day Vending-Bench with Grok 4 Fast[/bold green]")
        for d in range(days):
            if d % 50 == 0:
                console.print(f"[cyan]=== Day {d} ===[/cyan]")
            self.step()
            if self.bank < 0:
                console.print(f"[bold red]BANKRUPT on day {self.day}[/bold red]")
                break

        self.summary()

    def summary(self):
        df = pl.from_dicts(self.history)
        final_bank = df["bank"][-1]

        table = Table(title="Vending-Bench Final Results")
        table.add_column("Metric")
        table.add_column("Value", justify="right")
        table.add_row("Final Net Worth", f"[green]${final_bank:,.2f}[/green]")
        table.add_row("Total Revenue", f"${df['revenue'].sum():,.2f}")
        table.add_row("Units Sold (Soda)", str(df["sales_soda"].sum()))
        table.add_row("Units Sold (Chips)", str(df["sales_chips"].sum()))
        table.add_row("Survival Days", str(self.day))

        console.print(table)

        # Save lightning-fast parquet + CSV
        Path("results").mkdir(exist_ok=True)
        df.write_parquet("results/history.parquet")
        df.write_csv("results/history.csv")
        console.print("[bold]Results saved → results/history.parquet (Polars-optimized)[/bold]")

if __name__ == "__main__":

    load_dotenv()  # only for local .env during dev
    xai_api_key = os.getenv("XAI_API_KEY") or Path("/run/secrets/xai_api_key").read_text().strip()

    if not xai_api_key:
        raise RuntimeError("XAI_API_KEY not found!")    


    sim = VendingSimulator()
    sim.run(days=300)