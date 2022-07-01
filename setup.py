try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import re
import io
import os

with open('README.md', encoding='utf-8') as readme_file:
    readme = readme_file.read()

def read(path, encoding="utf-8"):
    path = os.path.join(os.path.dirname(__file__), path)
    with io.open(path, encoding=encoding) as fp:
        return fp.read()

HERE = os.path.abspath(os.path.dirname(__file__))

def version(path):
    """Obtain the package version from a python file e.g. pkg/__init__.py
    See <https://packaging.python.org/en/latest/single_source_version.html>.
    """
    version_file = read(path)
    version_match = re.search(
        r"""^__version__ = ['"]([^'"]*)['"]""", version_file, re.M
    )
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")

def find_packages(top=HERE):
    """
    Find all of the packages.
    """
    packages = []
    for d, dirs, _ in os.walk(top, followlinks=True):
        if os.path.exists(os.path.join(d, "__init__.py")):
            packages.append(os.path.relpath(d, top).replace(os.path.sep, "."))
        elif d != top:
            # Do not look for packages in subfolders
            # if current is not a package
            dirs[:] = []
    return packages

def get_install_requirements(path):
    content = read(path)
    return [req for req in content.split("\n") if req != "" and not req.startswith("#")]

setup(
 name='smoothing',
 version = '0.0.1beta',
 url = 'https://github.com/danhamill/Smoothing',
 download_url = 'https://github.com/danhamill/Smoothing',
 author = 'Daniel Hamill',
 author_email = 'daniel.hamill@hey.com',
 description = 'Cubic spline interpolation of hydrographs',
 long_description=readme,
 packages = find_packages(),
 license='MIT',
 install_requires = get_install_requirements("requirements.txt"),
 classifiers=[
    "Development Status :: 4 - Beta",
    'Intended Audience :: Developers',
    'Intended Audience :: Science/Research',
    "License :: OSI Approved :: MIT License",
    'Operating System :: OS Independent',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    "Topic :: Utilities",
    'Topic :: Scientific/Engineering :: GIS',
]
)