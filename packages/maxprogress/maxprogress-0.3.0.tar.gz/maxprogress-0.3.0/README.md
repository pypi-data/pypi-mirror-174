# MaxProgress 0.3.0

Updated to match dependencies with fellow helper scripts: maxconsole and maxcolor.

# MaxProgress 0.2.0

Maxprogress provides a thin wrapper around rich’s Progress Bar class. It generates a custom formatted progress bar.

<br />

![maxprogress](maxprogress.gif)

## Installation

### Pip

```bash
pip install maxprogress
```

### Pipx

```bash
pipx install maxprogress
```

### Poetry

```bash
poetry add maxprogress
```

## Usage

```python
from maxprogress import get_progress

progress = get_progress():

with progress:

    task1 = progress.add_task("[red]Downloading...", total=200)
    task2 = progress.add_task("[green]Processing...", total=200)
    task3 = progress.add_task("[cyan]Cooking...", total=200)

    while not progress.finished:
        progress.update(task1, advance=0.5)
        progress.update(task2, advance=0.3)
        progress.update(task3, advance=0.9)
        time.sleep(0.02)

```
