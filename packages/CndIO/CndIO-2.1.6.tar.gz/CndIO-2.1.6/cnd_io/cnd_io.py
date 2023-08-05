from cnd_io.__version__ import (
    __version__,
)
import yaml


class CndIO:
    def __init__(self, provider, print):
        self._print = print
        self._print.info_v(f"CndIO Version {__version__}")
        self._provider = provider
        self._cached_file = {}
        self._files = {}

    def _uuid(self, project_id, file_name, branch='main'):
        return f"{project_id}:{file_name}:{branch}"

    def pull_file(self, project_id, file_name, branch='main'):
        if self._uuid(project_id, file_name, branch=branch) not in self._cached_file:
            if self._provider.file_exist(project_id, file_name, branch=branch) is False:
                return False
            self._cached_file[self._uuid(project_id, file_name, branch=branch)] = self._provider.pull_file(project_id, file_name, branch=branch)
        return self._cached_file[self._uuid(project_id, file_name, branch=branch)]

    def commit_file(self, project_id, file_name, content, branch='main'):
        if project_id not in self._files:
            self._files[project_id] = {}
        if branch not in self._files[project_id]:
            self._files[project_id][branch] = {}
        self._files[project_id][branch][file_name] = content
        return len(self._files[project_id][branch])

    def commit_yaml_file(self, project_id, file_name, content, branch='main'):
        return self.commit_file(project_id, file_name, yaml.dump(content), branch='main')

    def push_files(self, project_id, branch='main', commit_message="It's a so nice day today"):
        if project_id not in self._files:
            return None
        if branch not in self._files[project_id]:
            return None
        return self._provider.push_files(project_id, self._files[project_id][branch], commit_message=commit_message)

    def push_file(self, project_id, file_name, content, branch='main', commit_message="It's a so nice day today"):
        if self._provider.push_file(project_id, file_name, content, branch=branch, commit_message=commit_message) is True:
            self._cached_file[self._uuid(project_id, file_name, branch=branch)] = content
            return True
        else:
            return False

    def pull_yaml_file(self, project_id, file_name, branch='main'):
        content = self.pull_file(project_id, file_name, branch=branch)
        if content is False:
            return False
        return yaml.safe_load(content)

    def push_yaml_file(self, project_id, file_name, content, branch='main'):
        return self.push_file(project_id, file_name, yaml.dump(content), branch=branch)
