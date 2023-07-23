import os

import dotenv


def initialize(current_version):
	env_path = os.path.expanduser('~/Documents/auto_up.env')
	url = 'https://antivirus.uclv.edu.cu/nod32/update_all'
	if os.path.exists(env_path):
		save_path = dotenv.get_key(env_path, 'save_path')
		url = dotenv.get_key(env_path, 'url')
		version = dotenv.get_key(env_path, 'version')
		if not version:
			dotenv.set_key(env_path, 'version', current_version)
			version = current_version
		return {'save_path': save_path, 'url': url, 'env_path': env_path, 'version': version}
	else:
		save_path = input('Ubicacion hacia donde descargar las actualizaciones: ')
		dotenv.set_key(env_path, 'save_path', save_path.replace('\\', '/'))
		new_url = input(
			'Cambiar la direccion de los archivos de actualizacion? (y/n) (por defecto: '
			'https://antivirus.uclv.edu.cu/nod32/update_all): ')
		if new_url.strip().lower() == 'y':
			url = input('Entre la nueva direccion: ')
			dotenv.set_key(env_path, 'url', url)
		else:
			dotenv.set_key(env_path, 'url', url)
		dotenv.set_key(env_path, 'version', current_version)
		return {'save_path': save_path, 'url': url, 'env_path': env_path, 'version': current_version}