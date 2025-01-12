from textual.app import App

from app.gui.screens.dashboard import DashboardScreen
from app.gui.screens.download import DownloadListScreen
from app.gui.screens.quit import QuitScreen
from app.gui.screens.settings import SettingsScreen
from app.management.env_manager import init_env


class TUI(App):
    BINDINGS = [
        ('q', 'request_quit', 'Salir'),
        ('m', "switch_mode('dashboard')", 'Menu principal'),
        ('d', "switch_mode('download')", 'Descargar'),
        ('c', "switch_mode('config')", 'Configurar'),
    ]
    MODES = {
        'dashboard': DashboardScreen,
        'config': SettingsScreen,
    }

    def __init__(self, version: str, title: str = 'App de descarga de actualizaciones', **kwargs):
        super().__init__(**kwargs)
        self.version = version
        # reactive items, title and subtitle
        self.title = title
        self.sub_title = version

    def on_mount(self):
        self.switch_mode('dashboard')
        env = init_env(self.app, self.version)
        self.add_mode('download', lambda: DownloadListScreen(env['url']))

    def action_request_quit(self):
        def check_quit(quit: bool | None):
            if quit:
                self.app.exit()

        self.push_screen(QuitScreen(), check_quit)
