from setuptools import setup

setup(
    name='diltools',
    version='0.1dev',
    description='',
    author='Arthur Nishikawa',
    author_email='nishikawa.poli@gmail.com',
    url='https://github.com/arthursn/diltools',
    packages=['diltools'],
    install_requires=['numpy', 'matplotlib',
                      'scipy', 'pandas'],
    long_description=open('README.md').read(),
)
