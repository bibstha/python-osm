from distutils.core import setup

setup(
	name = 'python-osm',
	version = '1.0',
	url = 'https://github.com/bibstha/python-osm',
	author = 'Bibek Shrestha',
	author_email = 'bibek.shrestha@gmail.com',
	description = 'Provides model objects for OSM primitives',
	package_dir = {'': 'src'},
	py_modules = ['pyosm']
)