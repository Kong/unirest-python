try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='Unirest',
    version='1.0.3',
    author='Mashape Inc.',
    author_email='support@mashape.com',
    packages=['unirest'],
    url='http://pypi.python.org/pypi/unirest/',
    license='LICENSE.txt',
    description='Unirest, the lightweight HTTP library',
    install_requires=[
        "poster >= 0.8.1"
    ]
)
