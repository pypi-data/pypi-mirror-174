import pkg_resources


path = pkg_resources.resource_filename("cnd_io", "VERSION")
__version__ = open(path).read()
