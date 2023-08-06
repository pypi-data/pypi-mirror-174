from setuptools import find_packages, setup
setup(
    name='c0mradelogger',
    packages=find_packages(include=['telelogging']),
    version='0.1.0',
    description='My first Python library',
    author='c0mrade',
    license='MIT',
    install_requires=[
        'requests',
        'pymongo',
    ],

)
