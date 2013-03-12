from distutils.core import setup

setup(
    name='Unicorn',
    version='1.0.1',
    author='Mashape Inc.',
    author_email='support@mashape.com',
    packages=['unicorn'],
    url='http://pypi.python.org/pypi/Unicorn/',
    license='LICENSE.txt',
    description='Unicorn, the lightweight HTTP library',
    long_description=open('README.txt').read(),
    install_requires=[
        "poster >= 0.8.1"
    ],
)
