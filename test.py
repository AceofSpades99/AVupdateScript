from rich.table import Table
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer


def table_view(row: list, header: list) -> Table:
    table = Table(title=row[0], expand=True)
    for i in header:
        table.add_column(i)
    table.add_row(*row)
    return table


class ReactShow(App[None]):
    CSS = """
    Screen {
        align: center middle;
    }
    """

    BINDINGS = [
        ("s", "set_text", "Set some text"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Options()
        yield Footer()

    def action_set_text(self) -> None:
        self.query_one(Options).add_options([table_view(['a', 'b', 'c', 'd'], [''])])

if __name__ == "__main__":
    ReactShow().run()
