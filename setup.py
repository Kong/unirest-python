from distutils.core import setup

setup(
    name='Unirest',
    version='1.0.2',
    author='Mashape Inc.',
    author_email='support@mashape.com',
    packages=['unirest'],
    url='http://pypi.python.org/pypi/Unirest/',
    license='LICENSE.txt',
    description='Unirest, the lightweight HTTP library',
    long_description=open('README.txt').read(),
    install_requires=[
        "poster >= 0.8.1"
    ],
)
