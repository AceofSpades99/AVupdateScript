import asyncio
import os.path
import urllib3
import dotenv
from pathlib import Path
from time import sleep
from downloader import download
from parser import url_parser, file_parser
from update_checker import get_updates

env_path = os.path.expanduser('~/Documents/auto_up.env')
save_path = ''
url = 'https://antivirus.uclv.edu.cu/eset_upd/eset_nod32_antivirus_eav'
if os.path.exists(env_path):
	save_path = dotenv.get_key(env_path, 'save_path')
	url = dotenv.get_key(env_path, 'url')
else:
	with open(env_path, 'w+') as o:
		save_path = input('Ubicacion hacia donde descargar las actualizaciones: ')
		dotenv.set_key(env_path, 'save_path', save_path.replace('\\', '/'))
	new_url = input(
		'Cambiar la direccion de los archivos de actualizacion? (y/n) (por defecto: '
		'https://antivirus.uclv.edu.cu/eset_upd/eset_nod32_antivirus_eav): ')
	if new_url.strip().lower() == 'y':
		url = input('Entre la nueva direccion: ')
		dotenv.set_key(env_path, 'url', url)
	else:
		dotenv.set_key(env_path, 'url', url)

try:
	first = url_parser(url)
	if Path.is_file(Path(os.path.join(save_path, 'update.ver'))):
		second = file_parser(os.path.join(save_path, 'update.ver'))
		updates = get_updates(first, second)
	else:
		updates = get_updates(first)
	
	asyncio.run(download(os.path.join(save_path, 'update.ver'), url + '/update.ver', updates))
except KeyboardInterrupt:
	print('User interrupted the execution')
# except RuntimeError:
# 	print('User interrupted the execution')
except urllib3.exceptions.MaxRetryError:
	print('Connection timed out, check your internet connection')
except KeyError:
	key = dotenv.get_key(env_path, 'url')
	print(f'Could not reach: {key}\nMay be using a VPN')
# except:
# 	print('Unknown error')

sleep(5)
