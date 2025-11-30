#!/usr/bin/env python3
"""
Grok 4 Fast / xAI API connectivity test
Run with: uv run test_xai_connectivity.py   (or python test_xai_connectivity.py)
"""

import os
import sys
from pathlib import Path

from openai import OpenAI, APIStatusError, AuthenticationError
from rich.console import Console
from rich.panel import Panel

console = Console()

def load_api_key():
    """Support every way secrets can arrive on OrbStack / Docker / local"""
    key = (
        os.getenv("XAI_API_KEY")                        # env var (OrbStack injects this)
        or os.getenv("OPENAI_API_KEY")                  # fallback for local testing
        or (Path("/run/secrets/xai_api_key").read_text().strip() if Path("/run/secrets/xai_api_key").exists() else None)
    )
    return key

def test_connectivity():
    api_key = load_api_key()

    if not api_key:
        console.print("[bold red]✗ XAI_API_KEY not found![/bold red]")
        console.print("   • Set it with: orb secret set xai_api_key")
        console.print("   • Or export XAI_API_KEY=sk-... in your shell")
        sys.exit(1)

    if api_key.startswith("xai-") is False:
        console.print("[bold red]✗ API key does not look valid (should start with xai-)[/bold red]")
        sys.exit(1)

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.x.ai/v1",
        timeout=15.0,
    )

    try:
        # Tiny harmless request that costs < $0.0001 and uses almost no tokens
        response = client.chat.completions.create(
            model="grok-4-fast",
            messages=[{"role": "user", "content": "Say 'hello' in one word."}],
            max_tokens=5,
            temperature=0,
        )
        answer = response.choices[0].message.content.strip()
        
        usage = response.usage
        console.print(Panel(
            f"[bold green]SUCCESS! xAI API is working perfectly[/bold green]\n\n"
            f"Model: {response.model}\n"
            f"Reply: [bold cyan]\"{answer}\"[/bold cyan]\n"
            f"Tokens used: {usage.total_tokens} (prompt {usage.prompt_tokens} + completion {usage.completion_tokens})",
            title="Grok 4 Fast Connectivity Test",
            border_style="green",
        ))
        sys.exit(0)

    except AuthenticationError:
        console.print("[bold red]✗ Authentication failed – wrong or revoked API key[/bold red]")
        sys.exit(1)
    except APIStatusError as e:
        console.print(f"[bold red]✗ API returned {e.status_code}: {e.message}[/bold red]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[bold red]✗ Unexpected error: {type(e).__name__}: {e}[/bold red]")
        sys.exit(1)

if __name__ == "__main__":
    console.print("[bold blue]Testing xAI / Grok 4 Fast connectivity...[/bold blue]")
    test_connectivity()