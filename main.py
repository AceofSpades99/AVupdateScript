import os.path

from app.gui.tui import TUI


def __version__():
    return '1.7.1'

if __name__ == '__main__':
    app = TUI(
        url='https://antivirus.uclv.edu.cu/nod32/update_all',
        version=__version__(),
        css_path=os.path.abspath('resources/css/style.tcss')
    )
    app.run()
