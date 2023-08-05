from setuptools import setup, find_packages
from cnd_io.__version__ import (
    __version__,
)

setup(name='CndIO',
    version=__version__,
    description="Tools to manage In/Out file. Easy to add new class if you need to change source/dest (file system, git ...)",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    keywords='',
    author='Denis FABIEN',
    author_email='denis.fabien@changendevops.com',
    url='https://gitlab.com/changendevops/cnd-io',
    license='MIT/X11',
    packages=find_packages(exclude=['ez_setup', 'examples', 'spec', 'spec.*']),
    include_package_data=True,
    package_data={'cnd_io': ['VERSION']},
    zip_safe=False,
    install_requires=['clint', 'coverage'],
    test_require=['expect', 'doublex', 'doublex-expects'],
    project_urls={
        "Documentation": "https://changendevops.com",
        "Source": "https://gitlab.com/changendevops/cnd-io",
    },
)