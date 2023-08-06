from distutils.core import setup

packages = ['txdpy']

setup(name='txdpy',
    version='4.1.2',
    author='唐旭东',
    install_requires=['mmh3','pymysql','loguru','redis','lxml','colorama','requests','colorama','lxpy'],
    packages=packages,
    package_dir={'requests': 'requests'})