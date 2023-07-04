def get_updates(online, local=None):
	upd = {}
	if local is not None:
		for item in online:
			if 'version' in online[item] and 'file' in online[item]:
				if item in local:
					if online[item]['version'] > local[item]['version']:
						upd[item] = updater(upd, item, online)
				else:
					upd[item] = updater(upd, item, online)
	else:
		for item in online:
			if 'version' in online[item] and 'file' in online[item]:
				upd[item] = updater(upd, item, online)
	upd['[VER]'] = 'update.ver'
	return upd


def updater(upd, item, online):
	upd[item] = {}
	upd[item] = online[item]['version']
	upd[item] = online[item]['file']
	return upd[item]

# def get_updates(online, local):   #if comparing 2 local files
#     upd = {}
#     for item in online:
#         if online[item]['version'] > local[item]['version']:
#             upd['Newer'] = 'online'
#             upd[item] = {}
#             upd[item] = online[item]['version']
#             upd[item] = online[item]['file']
#         elif online[item]['version'] < local[item]['version']:
#             upd['Newer'] = 'local'
#             upd[item] = {}
#             upd[item] = local[item]['version']
#             upd[item] = local[item]['file']
#     return upd