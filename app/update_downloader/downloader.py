import asyncio
import os.path
from pathlib import Path

import aiohttp
import requests
import tqdm.asyncio
from aiohttp import ClientPayloadError


async def download(file_path, in_url, updates):
	save_path = Path(file_path).parent
	index = 0
	status = requests.get(in_url, headers={'Content-Type': 'text/html'}).status_code
	sem = asyncio.Semaphore(10)  # start a semaphore with 10 connections as max
	if status == 200:
		tasks = []
		for url in feed(in_url, updates):
			# create a file on the hd using a path and an item from the dicts removing any special chars and replacing \\ with /
			path = os.path.join(save_path, updates[list(updates.keys())[index]]).replace('\\', '/').strip()
			# append a task to the queue
			tasks.append(get_async(url, path, sem))
			index += 1
		if tasks:
			# if tasks exists then print the progressbar, but just if it's not empty
			responses = [await f for f in tqdm.tqdm(asyncio.as_completed(tasks), total=len(tasks))]
			if responses[0] is not None:
				print(responses)
	else:
		print(f'ERROR, status code: {status}')


async def get_async(url, path, sem, retry=0, has_retried=False):
	# asycn using the semaphore declared earlier
	async with sem:
		# with a new http session
		async with aiohttp.ClientSession() as session:
			# with the url and without timeout
			async with session.get(url, timeout=None) as response:
				# open a new file to write in binary
				with open(path, 'wb') as file:
					# try to iterate through the file if there's an error while receiving the data:
					try:
						async for data in response.content.iter_chunked(1024):
							file.write(data)
					# mark the file as incomplete and retry 5 times
					except ClientPayloadError:
						print(f' Descarga incompleta del archivo: {url}, reintentando')
						if retry == 0 and not has_retried:
							await get_async(url, path, sem, 5, True)
						elif retry == 0 and has_retried:
							# if retrying fails ask the user if he wants to continue, otherwise close the app
							print(f'Se ha intentado descargar 5 veces el archivo: {url}')
							if input('Quiere cancelar el proceso? (y/n): ').strip().lower() == 'y':
								exit()
							else:
								await get_async(url, path, sem, 5, True)
						else:
							await get_async(url, path, sem, retry - 1, True)


def feed(url, updates):
	url = url[:url.rindex('/') + 1:]
	urls = []
	for i in updates:
		# if the update is a well composed string, cause updates might vary unexpectedly, append it to the queue
		if isinstance(updates[i], str):
			urls.append(url + updates[i])
	return urls
