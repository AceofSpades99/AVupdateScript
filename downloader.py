import os.path
import requests
from pathlib import Path
from tqdm import tqdm


def download(file_path, url, updates):
	save_path = Path(file_path).parent
	index = 0
	headers = {'Content-Type': 'text/html'}
	status = requests.get(url, headers=headers).status_code
	if status == 200:
		for url in feed(url, updates):
			response_per_request = requests.get(url, stream=True)
			total_size_in_bytes = int(response_per_request.headers.get('content-length', 0))
			block_size = 1024  # 1 Kibibyte
			progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
			with open(os.path.join(save_path, updates[list(updates.keys())[index]]), 'wb') as file:
				for data in response_per_request.iter_content(block_size):
					progress_bar.set_description(f'downloading {response_per_request.url}')
					progress_bar.update(len(data))
					file.write(data)
			progress_bar.close()
			if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
				print("ERROR, something went wrong")
			index += 1
	else:
		print(f"ERROR, status code: {status}")


def feed(url, updates):
	url = url[:url.rindex('/') + 1:]
	urls = []
	for i in updates:
		urls.append(url + updates[i])
	return urls
