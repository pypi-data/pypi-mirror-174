from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'My first Python package'
LONG_DESCRIPTION = 'My first Python package with a slightly longer description'

# Setting up
setup(
    name="AFZEWWVfxjXU2h86cGKbz2aXvLiWjuNqrhs5tPbf1cta9ZwGXVV2ow",
    version=VERSION,
    author="Alex Black",
    author_email="ku113p@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],

    keywords=['python', 'first package'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)