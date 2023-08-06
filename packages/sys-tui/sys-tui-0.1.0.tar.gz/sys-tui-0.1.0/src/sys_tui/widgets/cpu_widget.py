import psutil
from textual.reactive import reactive
from textual.widgets import Static


class CPUWidget(Static):
    """A widget to display CPU information."""

    cpu_times = reactive({})

    def on_mount(self) -> None:
        """Event handler called when widget is added to the app."""
        self.update_cpu_times()
        self.update_timer = self.set_interval(1, self.update_cpu_times)

    def update_cpu_times(self) -> None:
        """Method to update cpu times."""
        self.cpu_times = psutil.cpu_times()

    def watch_cpu_times(self, cpu_times) -> None:
        """Called when the cpu_times attribute changes."""
        self.update(f"{cpu_times}")
