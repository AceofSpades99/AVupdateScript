import os

file_extensions = (
	'.nup',
	'.ver',
)


def start_cleaning_process(online, offline, env):
	print('Buscando archivos innecesarios luego de la actualización: ')
	online_files, offline_files = scandir(online), scandir(offline)
	difference = list(set(offline_files) - set(online_files))
	if difference:
		print(f'Se eliminarán {len(difference)} archivos sin usar')
		print(difference)
		clean_unused(difference, env)
	else:
		print('No se han encontrado archivos sin usar')


def clean_unused(unused, env):
	for files in unused:
		os.remove(os.path.join(env['save_path'], files))
	print('Archivos eliminados')


def scandir(update_ver):
	if update_ver:
		files = []
		for modules in update_ver:
			if 'file' in update_ver[modules].keys():
				files.append(update_ver[modules]['file'])
		files.append('update.ver')
		return files
	else:
		return []
