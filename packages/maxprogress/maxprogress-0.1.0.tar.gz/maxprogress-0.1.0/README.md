# MaxProgress 0.1.0

Maxprogress provides a thin wrapper around rich’s Progress Bar class. It generates a custom formated progress bar.

<div style="max-width:80%;margin:auto;padding:20px;">
  <iframe src="maxprogress.gif" width="997" height="164" frameBorder="0" allowFullScreen>maxprogress</iframe>
</div>div

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