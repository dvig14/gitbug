import sys
from typing import Any

class RichManager:
    def __init__(self):
        self.rich_available = False
        self._setup_rich()

    def _setup_rich(self):
        try:
            from rich import print as rprint
            from rich.panel import Panel
            from rich.text import Text
            self.rprint = rprint
            self.Panel = Panel
            self.Text = Text
            self.rich_available = True
        except ImportError:
            self.rich_available = False

    def print(self, content: Any, style: str = None):
        if self.rich_available:
            if style:
                self.rprint(self.Text(content, style=style))
            else:
                self.rprint(content)
        else:
            print(content)

    def panel(self, title: str, content: str, border_style: str = "dim"):
        if self.rich_available:
            self.rprint(self.Panel(content, title=title, border_style=border_style))
        else:
            print(f"\n{title.upper()}\n{'='*len(title)}\n{content}\n")

display = RichManager()

