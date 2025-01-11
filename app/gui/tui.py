from textual.app import App

from app.gui.screens.dashboard import DashboardScreen
from app.gui.screens.settings import SettingsScreen


class TUI(App):
    BINDINGS = [
        ('escape', 'request_quit', 'Salir'),
        ('m', "switch_mode('dashboard')", 'Menu principal'),
        ('c', "switch_mode('config')", 'Configurar'),
        # ("h", "switch_mode('help')", "Help"),
    ]
    MODES = {
        'dashboard': DashboardScreen,
        'config': SettingsScreen,
    }

    def __init__(self, url: str, version: str, title: str = 'App de descarga de actualizaciones', **kwargs):
        super().__init__(**kwargs)

        # reactive items, title and subtitle
        self.title = title
        self.sub_title = version

    def on_mount(self):
        self.switch_mode('dashboard')
