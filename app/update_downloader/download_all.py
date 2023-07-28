import asyncio
import os
from urllib.request import urlopen

import tqdm
from bs4 import BeautifulSoup

from app.management.env_manager import initialize
from app.update_downloader.downloader import get_async

file_extensions = (
	'.nup',
	'.ver',
)


def execute(url):
	links, names = [], []
	response = urlopen(url)
	soup = BeautifulSoup(response, 'html.parser')
	for link in soup.findAll('a'):
		if link.getText().endswith(file_extensions):
			links.append(url + '/' + link.get('href'))
			names.append(link.get('href'))
	return links, names


async def download(updates, names, save_path):
	sem = asyncio.Semaphore(10)
	tasks = []
	index = 0
	for url in updates:
		# create a file on the hd using a path and an item from the dicts removing any special chars and replacing \\ with /
		path = os.path.join(save_path, names[index])
		# append a task to the queue
		index += 1
		tasks.append(get_async(url, path, sem))
	if tasks:
		# if tasks exists then print the progressbar, but just if it's not empty
		responses = [await f for f in tqdm.tqdm(asyncio.as_completed(tasks), total=len(tasks))]
		if responses[0] is not None:
			print(responses)


env = initialize('1.6.6')
exe = execute(env['url'])
asyncio.run(download(exe[0], exe[1], env['save_path']))
