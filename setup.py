from distutils.core import setup

setup(
    name='MashapeRest',
    version='3.0.2',
    author='Mashape Inc.',
    author_email='support@mashape.com',
    packages=['mashaperest'],
    url='http://pypi.python.org/pypi/MashapeRest/',
    license='LICENSE.txt',
    description='Mashape Rest HTTP client library',
    long_description=open('README.txt').read(),
    install_requires=[
        "poster >= 0.8.1"
    ],
)
