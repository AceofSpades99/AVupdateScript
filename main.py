import os.path

from app.gui.tui import TUI


def __version__():
    return '2.0'

if __name__ == '__main__':
    app = TUI(
        version=__version__(),
        css_path=os.path.abspath('resources/css/style.tcss')
    )
    app.run()
