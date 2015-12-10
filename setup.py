try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='UnirestModified',
    version='1.1.8',
    author='Mashape',
    author_email='opensource@mashape.com',
    packages=['unirestmodified'],
    url='https://github.com/codyrice/unirest-python.git',
    license='LICENSE',
    description='Simplified, lightweight HTTP client library',
    install_requires=[
        "poster >= 0.8.1"
    ]
)
