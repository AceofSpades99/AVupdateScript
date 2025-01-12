from textual import on
from textual.app import ComposeResult
from textual.containers import Grid
from textual.screen import Screen
from textual.widgets import Header, Button


class DashboardScreen(Screen):
    def compose(self) -> ComposeResult:
        yield Header(self.title)
        yield Grid(
            Button('Buscar actualizaciones', id='download'),
            Button('Configurar', id='config'),
            Button('Salir', id='quit'),
            id='dialog'
        )

    @on(Button.Pressed, '#download')
    def button_download(self):
        self.app.switch_mode('download')

    @on(Button.Pressed, "#config")
    def button_config(self):
        self.app.switch_mode('config')

    @on(Button.Pressed, "#quit")
    def button_quit(self):
        self.parent.action_request_quit()
