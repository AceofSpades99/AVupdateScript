import os
import platform

import dotenv


def initialize(current_version):
	env_path = platform_verify_support()
	url = 'https://antivirus.uclv.edu.cu/nod32/update_all'
	if os.path.exists(env_path):
		save_path = dotenv.get_key(env_path, 'save_path')
		url = dotenv.get_key(env_path, 'url')
		if not dotenv.get_key(env_path, 'version') or dotenv.get_key(env_path, 'version') < current_version:
			dotenv.set_key(env_path, 'version', current_version)
		version = dotenv.get_key(env_path, 'version')
		return {'save_path': save_path, 'url': url, 'env_path': env_path, 'version': version}
	else:
		save_path = input('Ubicación hacia donde descargar las actualizaciones: ')
		dotenv.set_key(env_path, 'save_path', save_path.replace('\\', '/'))
		new_url = input(
			'Cambiar la dirección de los archivos de actualización? (y/n) (por defecto: '
			'https://antivirus.uclv.edu.cu/nod32/update_all): ')
		if new_url.strip().lower() == 'y':
			url = input('Entre la nueva dirección: ')
			dotenv.set_key(env_path, 'url', url)
		else:
			dotenv.set_key(env_path, 'url', url)
		dotenv.set_key(env_path, 'version', current_version)
		return {'save_path': save_path, 'url': url, 'env_path': env_path, 'version': current_version}


def platform_verify_support():
	if platform.system() == 'Linux' or platform.system() == 'Windows':
		if os.path.exists(os.path.expanduser('~/Documents/')):
			env_path = os.path.expanduser('~/Documents/auto_up.env')
		elif os.path.exists(os.path.expanduser('~/Documentos/')):
			env_path = os.path.expanduser('~/Documentos/auto_up.env')
		else:
			env_path = os.path.expanduser(os.getcwd() + '/auto_up.env')
	else:
		raise Exception('Sistema no soportado')
	return env_path
