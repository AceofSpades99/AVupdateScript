import asyncio
import os.path
from pathlib import Path
from time import sleep

import dotenv
from urllib3.exceptions import MaxRetryError

from app.management.env_manager import initialize
from app.update_downloader.downloader import download
from app.update_downloader.parser import url_parser, file_parser
from app.update_downloader.update_checker import get_updates


def __version__():
	return '1.6.6'


if __name__ == '__main__':
	env = initialize(__version__())  # check env to know if the app has been used before
	try:
		print('Iniciando (este proceso puede demorar unos segundos)')
		online = url_parser(env['url'])  # parse the default_url's update.ver file
		if Path.is_file(Path(os.path.join(env['save_path'], 'update.ver'))):  # if the download path has an update file:
			local = file_parser(os.path.join(env['save_path'], 'update.ver'))
			updates = get_updates(online, env, local)
		else:
			updates = get_updates(online, env)
		if updates:  # if there are updates
			print('Descargando: ')
			asyncio.run(download(os.path.join(env['save_path'], 'update.ver'), env['url'] + '/update.ver', updates))
		# clean_unused(online, env)
		else:
			print('No hay actualizaciones pendientes')
	except KeyboardInterrupt:
		print('El usuario ha interrumpido la ejecución')
	except RuntimeError:
		print('El usuario ha interrumpido la ejecución')
	except MaxRetryError:
		print('Tiempo de espera agotado, revise su conexión a internet')
	except KeyError:
		key = dotenv.get_key(env['env_path'], 'url')
		print(f'No se pudo conectar a: {key}')
	except Exception as e:
		if e is not None:
			print(e)
		else:
			print('Error desconocido')
	print('Ejecución finalizada')
	sleep(5)
