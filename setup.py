
from setuptools import setup, find_packages

setup(
    name='Mortgage Package',
    version='0.1',
    packages=find_packages(include=['Mortgage_Package', 'Mortgage_Package.*']),
    license='MIT',
    description='A package for mortgage planning and real estate affodability computation',
    url='https://github.com/lukavuko/Lab4_Testing_II',
    author='Tony Zhou and Luka Vukovic',
    author_email='luka.vuko@outlook.com'
)
    

