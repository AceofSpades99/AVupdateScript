from textual.app import ComposeResult
from textual.containers import Grid
from textual.screen import ModalScreen
from textual.widgets import Label, Button


class QuitScreen(ModalScreen[bool]):
    def compose(self) -> ComposeResult:
        yield Grid(
            Label('Esta seguro?', id='question'),
            Button('Salir', variant='error', id='quit'),
            Button('Cancelar', variant='primary', id='cancel'),
            id="dialog",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == 'quit':
            self.dismiss(True)
        else:
            self.dismiss(False)
