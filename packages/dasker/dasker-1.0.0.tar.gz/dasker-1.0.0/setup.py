from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name='dasker',
    version='1.0.0',
    description='monadic dask client in separate process',
    long_description_content_type="text/markdown",
    license="MIT",
    long_description=long_description,
    author='Dror Speiser',
    url="http://github.com/drorspei/dasker",
    packages=['dasker'],
    install_requires=[
        "dask",
        "distributed",
    ],
    entry_points={
        'console_scripts': [
            'dasker = dasker.main:main',
        ],
    },
)
