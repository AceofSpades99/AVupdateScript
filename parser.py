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
	for i in file_or_url_after_opened:
		if i.startswith('['):
			name = i.strip()
			dict_new[f'{name}'] = {}
		if i.__contains__('='):
			(key, value) = i.split('=')
		else:
			key, value = '', ''
		if key and value:
			dict_new[name][key] = value.strip()
	return dict_new
