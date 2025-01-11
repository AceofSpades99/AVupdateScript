from textual import on
from textual.app import ComposeResult
from textual.containers import Grid
from textual.screen import Screen
from textual.widgets import Header, Button

from app.gui.screens.quit import QuitScreen


class DashboardScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header(self.title)
        yield Grid(
            Button('Buscar actualizaciones', action='action_select'),
            Button('Configurar', id='config'),
            Button('Salir', id='quit'),
            id='dialog'
        )

    @on(Button.Pressed, "#quit")
    def action_request_quit(self) -> None:
        def check_quit(quit: bool | None) -> None:
            if quit:
                self.app.exit()

        self.app.push_screen(QuitScreen(), check_quit)

    @on(Button.Pressed, "#config")
    def button_config(self):
        self.app.switch_mode('config')
