import sys
from rich.console import Console
from rich.markdown import Markdown
from rich.live import Live
from rich.panel import Panel

def stream_response(retrieval_chain, user_input):
    console = Console()
    full_response = ""
    with Live(console=console, refresh_per_second=10, transient=True) as live:
        live.update(Panel("Searching files...", title="Architect", border_style="magenta"))
        
        for chunk in retrieval_chain.stream({"input": user_input}):
            if "answer" in chunk:
                full_response += chunk["answer"]
                live.update(Markdown(full_response))
                
    console.print(Markdown(full_response))