import os

import dotenv
from packaging.version import Version
from textual.app import App

from app.gui.screens.first_config import FirstConfig
from app.management.platform_support import platform_verify_support


def init_env(app: App, current_version: str) -> dict:
	env_path = platform_verify_support()
	url = 'https://antivirus.uclv.edu.cu/nod32/'
	if os.path.exists(env_path):
		old_url = dotenv.get_key(env_path, 'url')
		if (
				not dotenv.get_key(env_path, 'version') or
				Version(dotenv.get_key(env_path, 'version')) < Version(current_version)
		):
			dotenv.set_key(env_path, 'version', current_version)
			if old_url != url:
				dotenv.set_key(env_path, 'url', url)
	else:
		dotenv.set_key(env_path, 'version', current_version)
		dotenv.set_key(env_path, 'url', url)
		app.push_screen(FirstConfig())
	save_path = dotenv.get_key(env_path, 'save_path')
	version = dotenv.get_key(env_path, 'version')
	return {'save_path': save_path, 'url': url, 'env_path': env_path, 'version': version}
