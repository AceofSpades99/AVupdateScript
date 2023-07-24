import os

file_extensions = (
	'.nup',
	'.ver',
)


def clean_unused(update_ver, env):
	files = []
	for modules in update_ver:
		if 'file' in update_ver[modules].keys():
			files.append(update_ver[modules]['file'])
	files.append('update.ver')
	scandir(files, env)


def scandir(files, env):
	unused = []
	for items in os.scandir(env['save_path']):
		if items.name not in files and items.name.endswith(file_extensions):
			unused.append(items.name)
	print('Buscando archivos innecesarios luego de la actualización: ')
	if unused:
		print(f'Se eliminarán {len(unused)} archivos sin usar')
		for files in unused:
			os.remove(os.path.join(env['save_path'], files))
		print('Archivos eliminados')
	else:
		print('No se han encontrado archivos sin usar')
