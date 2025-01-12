from threading import Thread

import requests
from bs4 import BeautifulSoup
from rich.table import Table
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Footer, Header, OptionList, LoadingIndicator


class Options(OptionList):
    DEFAULT_CSS = """
        .hidden {
            display: none;
        }
    """

    def __init__(self) -> None:
        super().__init__(classes='hidden')


class DownloadListScreen(Screen):
    def __init__(self, url: str):
        super().__init__()
        self.url = url
        self.options = Options()
        self.thread = Thread(target=self.search_table).start()
        self.index = 0

    async def search_table(self):
        results = {}
        async with requests.get(self.url) as response:
            soup = BeautifulSoup(response.content, 'lxml')
            table = soup.find('table')
            if table:
                # headers
                data = {
                    'header': [th.text.strip() for th in table.find_all('th')][1:],
                    # [1:] to skip the folder or file icon
                    'rows': []
                }
                # rows
                for row in table.find_all('tr')[1:]:
                    cells = [td.text.strip() for td in row.find_all('td')][1:]
                    if len(cells) == len(data['header']):
                        if cells[-1].isnumeric() or any(ext in cells[-1] for ext in ['K', 'M', 'G', 'T']):
                            data['rows'].append(cells)
        if results:
            self.query_one(Options).add_options(
                [
                    self.table_view(row, results['header']) for row in results['rows']
                ]
            )
            await self.query_one(LoadingIndicator).remove()

    def table_view(self, row: list, header: list) -> Table:
        table = Table(title=row[0], expand=True)
        for i in header:
            table.add_column(i)
        table.add_row(*row)
        return table

    def compose(self) -> ComposeResult:
        yield Header()
        yield self.options  # todo fix display update
        yield LoadingIndicator()
        yield Footer()
