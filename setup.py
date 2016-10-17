from setuptools import setup, find_packages

setup(
	name = 'barnacles',
	version = '1.0.0',
	packages = find_packages(),
	requires = [
		"flask",
	],
)