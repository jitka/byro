#!/usr/bin/env python3

from setuptools import (setup, find_packages)
from byro import __version__

setup(
	# Basic
	name='Byro',
	version=__version__,
	packages=find_packages(),
	# Entry ponit
	entry_points={
		'console_scripts': [
			'byro = byro.__main__:main',
		]
	},

	# Requirements
	install_requires=["wget", "dateutils", "markdown",
		"ConfigArgParse", "sh",
		"python-redmine", "python-docx",
		"pytesseract"],

	package_data={
		'byro': ['resource/*']
	},

	# About
	author='Ondřej Profant, Jakub Michálek',
	author_email='ondrej.profant@gmail.com',
	description='',
	license='Affero GNU-GPL v3',
	keywords="bureaucracy administration pdf git ocr markdown",
	url='https://github.com/pirati-cz/byro/',

	classifiers=[
		'Development Status :: 3 - Alpha',
		'Environment :: Console',
		'Intended Audience :: Legal Industry',
		'Intended Audience :: Users',
		'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
		'Natural Language :: English',
		'Natural Language :: Czech',
		'Operating System :: POSIX :: Linux',
		'Programming Language :: Python :: 3.4',
		'Programming Language :: Python :: 3 :: Only',
		'Topic :: Office/Business',
		'Topic :: Utilities'
	]
)
