from sinai.stores.memory import MemoryMetricStore


class DebugStore(MemoryMetricStore):
    """Prints metrics out to standard output."""

    def save_metric(self, metric):
        print("DEBUG: We have a metric!\n")
        print(metric.format_message())
        super().save_metric(metric)
