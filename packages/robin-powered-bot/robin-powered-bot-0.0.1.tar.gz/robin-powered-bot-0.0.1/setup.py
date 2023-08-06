from setuptools import find_packages, setup

setup(
    name='robin-powered-bot',
    version='0.0.1',
    description='Provides a set of utilities to simplify communication with robin-powered API and more easily automate bookings.',
    url='https://github.com/donatobarone/robin-powered-bot',
    author='Donato Barone',
    author_email='eng.donato.barone@gmail.com',
    packages=find_packages(),
    install_requires=[
        'requests'
    ], zip_safe=False)
