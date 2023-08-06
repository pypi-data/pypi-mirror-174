from setuptools import setup, find_packages
setup(
    name='vaitool',
    version='0.0.0.4b1',   
    url="" ,
    description='converter tool for visionai format',
    author='LinkerNetworks',
    packages=find_packages(),
    install_requires=['pydantic'],
    python_requires='>=3.9, <4',
)