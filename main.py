import os.path

import dotenv
from dotenv import load_dotenv
import urllib3

from downloader import download, feed
from parser import url_parser, file_parser, dict_builder
from update_checker import get_updates

env_path = os.path.expanduser('~\\Documents\\auto_up.env')
save_path = ''
url = 'https://antivirus.uclv.edu.cu/eset_upd/eset_nod32_antivirus_eav'
if os.path.exists(env_path):
	save_path = dotenv.get_key(env_path, 'save_path')
	url = dotenv.get_key(env_path, 'url')
else:
	with open(env_path, 'w+') as o:
		save_path = input('Ubicacion hacia donde descargar las actualizaciones: ')
		dotenv.set_key(env_path, 'save_path', save_path)
	new_url = input(
		'Cambiar la direccion de los archivos de actualizacion? (Y,N) (por defecto: '
		'https://antivirus.uclv.edu.cu/eset_upd/eset_nod32_antivirus_eav): ')
	if new_url.lower() == 'y':
		url = input('Entre la nueva direccion: ')
		dotenv.set_key(env_path, 'url', url)
	else:
		dotenv.set_key(env_path, 'url', url)

first = url_parser(url)
second = file_parser(os.path.join(save_path, 'update.ver'))
updates = get_updates(first, second)
download(os.path.join(save_path, 'update.ver'), url + '/update.ver', updates)
