import asyncio
import os.path
import urllib3
import dotenv
from pathlib import Path
from time import sleep

from env_manager import initialize
from downloader import download
from garbage_collector import clean_unused
from parser import url_parser, file_parser
from update_checker import get_updates


def __version__():
	return '1.6'


if __name__ == '__main__':
	env = initialize(__version__())  # check env to know if the app has been used before
	try:
		print('Iniciando (este proceso puede demorar unos segundos)')
		online = url_parser(env['url'])  # parse the default_url's update.ver file
		if Path.is_file(Path(os.path.join(env['save_path'], 'update.ver'))):  # if the download path has an update file:
			local = file_parser(os.path.join(env['save_path'], 'update.ver'))
			updates = get_updates(online, local)
		else:
			updates = get_updates(online)
		if updates:  # if there are updates
			print('Descargando: ')
			asyncio.run(download(os.path.join(env['save_path'], 'update.ver'), env['url'] + '/update.ver', updates))
			clean_unused(online, env)
		else:
			print('No hay actualizaciones pendientes')
	except KeyboardInterrupt:
		print('User interrupted the execution')
	except RuntimeError:
		print('User interrupted the execution')
	except urllib3.exceptions.MaxRetryError:
		print('Connection timed out, check your internet connection')
	except KeyError:
		key = dotenv.get_key(env['env_path'], 'url')
		print(f'Could not reach: {key}\nMay be using a VPN')
	except:
		print('Unknown error')
	
	print('Ejecución finalizada')
	sleep(5)
