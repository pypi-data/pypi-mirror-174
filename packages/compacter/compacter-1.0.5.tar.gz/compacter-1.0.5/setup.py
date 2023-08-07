from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name='compacter',
    version='1.0.5',
    description='Compact directories of parquet files to single parquet files.',
    long_description_content_type="text/markdown",
    license="MIT",
    long_description=long_description,
    author='Dror Speiser',
    url="http://github.com/drorspei/compacter",
    packages=['compacter'],
    install_requires=[
        "dask",
        "distributed",
        "fsspec",
        "s3fs",
        "pyarrow",
        "dasker",
    ],
    entry_points={
        'console_scripts': [
            'compacter = compacter.main:main',
        ],
    },
)
