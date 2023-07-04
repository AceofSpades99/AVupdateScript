import os.path
import requests
import asyncio
import aiohttp
import tqdm.asyncio
from pathlib import Path

from aiohttp import ClientPayloadError


async def download(file_path, in_url, updates):
	save_path = Path(file_path).parent
	index = 0
	status = requests.get(in_url, headers={'Content-Type': 'text/html'}).status_code
	sem = asyncio.Semaphore(10)
	if status == 200:
		tasks = []
		for url in feed(in_url, updates):
			path = os.path.join(save_path, updates[list(updates.keys())[index]]).replace('\\', '/').strip()
			tasks.append(get_async(url, path, sem))
			index += 1
		if tasks:
			responses = [await f for f in tqdm.tqdm(asyncio.as_completed(tasks), total=len(tasks))]
			if responses[0] is not None:
				print(responses)
	else:
		print(f"ERROR, status code: {status}")


async def get_async(url, path, sem, retry=0, has_retried=False):
	async with sem:
		async with aiohttp.ClientSession() as session:
			async with session.get(url, timeout=None) as response:
				with open(path, 'wb') as file:
					try:
						async for data in response.content.iter_chunked(1024):
							file.write(data)
					except ClientPayloadError:
						print(f' File download incomplete for file: {url}, retrying')
						if retry == 0 and not has_retried:
							await get_async(url, path, sem, 5, True)
						elif retry == 0 and has_retried:
							print(f'Retried 5 times and failed to retrieve {url}')
							if input('Do you want to cancel the process? (y/n): ').strip().lower() == 'y':
								exit()
							else:
								await get_async(url, path, sem, 5, True)
						else:
							await get_async(url, path, sem, retry-1, True)


def feed(url, updates):
	url = url[:url.rindex('/') + 1:]
	urls = []
	for i in updates:
		if isinstance(updates[i], str):
			urls.append(url + updates[i])
	return urls
