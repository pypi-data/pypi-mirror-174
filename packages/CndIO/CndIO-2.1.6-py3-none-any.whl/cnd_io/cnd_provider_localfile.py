from os.path import exists
from cnd_io.cnd_provider import CndProvider
from pathlib import Path


class CndProviderLocalfile(CndProvider):
    def _full_path(selft, project_id, file_name):
        return f"{project_id}/{file_name}"

    def pull_file(self, project_id, file_name, **kwargs):
        self._print_me("trace_c", f"Opening file {self._full_path(project_id, file_name)} now")
        f = open(self._full_path(project_id, file_name), "r")
        return f.read()

    def push_file(self, project_id, file_name, content, **kwargs):
        self._print_me("trace_c", f"Creation file {self._full_path(project_id, file_name)} now")
        folders = self._full_path(project_id, file_name).split('/')
        folders.pop()
        Path('/'.join(folders)).mkdir(parents=True, exist_ok=True)        
        with open(self._full_path(project_id, file_name), 'w') as f:
            f.write(content)
        return True

    def push_files(self, project_id, files, **kwargs):
        for file_name in files:
            self.push_file(project_id, file_name, files[file_name])
        return True

    def file_exist(self, project_id, file_name, **kwargs):
        self._print_me("trace_c", f"Checking file {self._full_path(project_id, file_name)} now")
        return exists(self._full_path(project_id, file_name))
