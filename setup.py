try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
from core.version import __version__ as myVersion
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf8")

setup(
 name='CVHSSmoothing',
 url = 'https://github.com/danhamill/CVHSSmoothing',
 download_url = 'https://github.com/danhamill/CVHSSmoothing',
 author = 'Daniel Hamill',
 author_email = 'daniel.hamill@hey.com',
 description = 'Cubic spline interpolation of hydrographs',
 long_description=long_description,
 long_description_content_type="text/markdown",
 packages = ['core'],
 license='MIT',
 version=myVersion,
 install_requires = ['numpy','pandas','scipy'],
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