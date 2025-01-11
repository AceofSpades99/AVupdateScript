import os

from textual.app import App, ComposeResult
from textual.widgets import DirectoryTree


class DirectoryTreeApp(App):
    def __init__(self):
        super().__init__()
        self.path = os.path.abspath(os.sep)
        self.dr = DirectoryTree(path=self.path)

    def compose(self) -> ComposeResult:
        yield self.dr

    def on_mount(self):
        self.dr.watch_path()


if __name__ == "__main__":
    app = DirectoryTreeApp()
    app.run()
