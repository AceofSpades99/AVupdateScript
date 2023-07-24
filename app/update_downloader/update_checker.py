def get_updates(online, local=None):
    upd = {}
    # if there are files already on the destination folder
    if local is not None:
        # for each element that exists on the online versions file
        for item in online:
            # if that element has a version and a file associated to it
            if 'version' in online[item] and 'file' in online[item]:
                # if the element does not have a local version or has an outdated version, add it to the queue
                if item not in local or online[item]['version'] > local[item]['version']:
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
