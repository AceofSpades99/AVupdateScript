import os


def get_updates(online, env, local=None):
	upd = {}
	# if there are files already on the destination folder
	if local is not None:
		# for each element that exists on the online versions file
		for item in online:
			# if that element has a version and a file associated to it
			if 'versionid' in online[item] and 'file' in online[item]:
				# if the element does not have a local version, has an outdated version
				# or if the module file does not exist, add it to the queue
				if item not in local or online[item]['versionid'] > local[item]['versionid'] \
						or online[item]['file'] not in scan_local_files(env):
					upd[item] = updater(upd, item, online)
	# if there are no files just add all
	else:
		for item in online:
			if 'version' in online[item] and 'file' in online[item]:
				upd[item] = updater(upd, item, online)
	if upd:
		upd['[VER]'] = 'update.ver'
	return upd


def updater(upd, item, online):
	upd[item] = {}
	upd[item] = online[item]['version']
	upd[item] = online[item]['file']
	return upd[item]


def scan_local_files(env):
	return [file.name for file in os.scandir(env['save_path'])]
