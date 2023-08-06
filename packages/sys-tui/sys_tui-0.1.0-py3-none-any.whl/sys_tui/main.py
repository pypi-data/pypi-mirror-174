import sys

import typer

from sys_tui.app import SystemApp


app = typer.Typer(add_completion=False)


@app.command()
def main() -> None:
    app = SystemApp()
    app.run()

    sys.stdout.flush()
    sys.stderr.flush()
