from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Footer, Header

from sys_tui.widgets.cpu_widget import CPUWidget


class SystemApp(App):
    """A textual app to monitor system utilities."""

    BINDINGS = [
        ("d", "toggle_dark", "Toggle dark mode"),
    ]

    def compose(self) -> ComposeResult:
        """Called to add widgets to the app."""
        yield Header()
        yield Footer()
        yield Container(CPUWidget(), id="info_card")

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.dark = not self.dark


if __name__ == "__main__":
    app = SystemApp()
    app.run()
