import requests
from bs4 import BeautifulSoup


def get_last_update_data(url):
    with requests.get(url) as response:
        soup = BeautifulSoup(response.content, 'lxml')
        table = soup.find('table')

        # headers
        data = [
            [th.text.strip() for th in table.find_all('th')]
        ]
        # rows
        for row in table.find_all('tr')[1:]:
            cells = [td.text.strip() for td in row.find_all('td')]
            if len(cells) == len(data[0]):
                data.append(cells)
    return data
