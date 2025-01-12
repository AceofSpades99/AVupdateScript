import os
import platform


def platform_verify_support() -> str:
    if platform.system() == 'Linux' or platform.system() == 'Windows':
        if os.path.exists(os.path.expanduser('~/Documents/')):
            env_path = os.path.expanduser('~/Documents/auto_up.env')
        elif os.path.exists(os.path.expanduser('~/Documentos/')):
            env_path = os.path.expanduser('~/Documentos/auto_up.env')
        else:
            env_path = os.path.expanduser(os.getcwd() + '/auto_up.env')
    else:
        raise Exception('Sistema no soportado')
    return env_path
