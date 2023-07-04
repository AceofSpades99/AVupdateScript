import urllib3
from Tools.scripts.ndiff import fopen


def file_parser(file):
	return dict_builder(fopen(file))


def url_parser(url):
	url += '/update.ver'
	return dict_builder(urllib3.PoolManager().request('GET', url).data.decode('utf-8').split('\n'))


def dict_builder(file_or_url_after_opened):
	name = ''
	dict_new = {}
	# following the version file's scheme to create a two level dictionary
	for i in file_or_url_after_opened:
		key, value = '', ''
		# if the line starts with [ that means it's a module, and then it's a first level key
		if i.startswith('['):
			name = i.strip()
			dict_new[f'{name}'] = {}
		# if instead the line does not start with a [ and has an = then it's a key value pair
		elif i.__contains__('='):
			(key, value) = i.split('=')
		# if both key and value where assigned then it adds them to the dict
		if key and value:
			dict_new[name][key] = value.strip()
	return dict_new
