from maxconsole import get_console, get_theme
from rich.console import Console
from rich.progress import (BarColumn, MofNCompleteColumn, Progress,
                           SpinnerColumn, TextColumn, TimeElapsedColumn,
                           TimeRemainingColumn)
from rich.table import Column
from rich.style import Style, StyleType
from rich.text import Text
import time

theme = get_theme()
console = get_console(theme)

def get_progress(console: Console = console) -> Progress:
    if not console:
        theme = get_theme()
        console = get_console(theme)
    text_column = TextColumn("[progress.description]{task.description}")
    spinner_column = SpinnerColumn(
        spinner_name="point",
        style="#ffff00",
        finished_text=Text("✓", style="#00ff00"),
        table_column=Column(),
    )
    bar_column = BarColumn(
        bar_width=None,  # Full width progress bar
        style=Style(color="#249df1"),  # While in-progress
        complete_style=Style(color="#00ff00"),  # Done
        finished_style=Style(color="#333333"),  # After completion
        table_column=Column(ratio=3),
    )
    mofn_column = MofNCompleteColumn()
    time_elapsed_column = TimeElapsedColumn()
    time_remaining_column = TimeRemainingColumn()
    progress = Progress(
        text_column,
        spinner_column,
        bar_column,
        mofn_column,
        time_elapsed_column,
        time_remaining_column,
        console=console,
    )
    return progress

if __name__ == "__main__":
    time.sleep(10)
    progress = get_progress()
    console.print()
    with progress:

        task1 = progress.add_task("[red]Downloading...", total=200)
        task2 = progress.add_task("[green]Processing...", total=200)
        task3 = progress.add_task("[cyan]Cooking...", total=200)

        while not progress.finished:
            progress.update(task1, advance=0.5)
            progress.update(task2, advance=0.3)
            progress.update(task3, advance=0.9)
            time.sleep(0.02)

    console.print()
    console.print("[#00ff00]Done.[/]")