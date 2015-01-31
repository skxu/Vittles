from setuptools import setup

setup(
	name='Vittles',
	version='0.1',
	description='Yelp+Tinder',
	url='http://github.com/skxu/Vittles',
	author='Sam Xu',
	author_email='skx@berkeley.edu',
	license='MIT',
	packages=[],
	install_requires=[
		'flask',
		'flask-restful',
		'Flask-ZODB',
		'oauth2',
		'python-tk'
	],
	zip_safe=False)