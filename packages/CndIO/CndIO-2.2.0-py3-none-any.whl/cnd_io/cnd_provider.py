from cnd_io.__version__ import (
    __version__,
)


class CndProvider:
    def __init__(self, creds={}, print=None):
        self._print = print
        self._print_me("info_v", f"CndProvider Version {__version__}", silent_mode=True)
        self._creds = creds

    def _print_me(self, method, message, silent_mode=False):
        if self._print is None:
            if silent_mode is False:
                print(message)
            return False
        else:
            getattr(self._print, method)(message)
            return True

    def pull_file(self, source_name, file_name):
        return None

    def push_file(self, source_name, file_name, content):
        return True

    def push_files(self, source_name, files):
        return True

    def file_exist(self, source_name, file_name):
        return True
