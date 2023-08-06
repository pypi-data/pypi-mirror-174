from setuptools import setup, find_packages


long_description = """
A collection of data structures and basic utilities used for Python programming. 
Copyright Xavier Mercerweiss, 2022. Licensed under GPLv3.

Project GitHub at <https://github.com/XavierFMW/goldbox>
"""

setup(
    name='goldbox',
    version='1.0.1',
    description="A package of simple Python utilities and data structures.",
    long_description=long_description,
    license='GPLv3',
    author="Xavier Mercerweiss",
    author_email='xavifmw@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/XavierFMW/goldbox',
    keywords='toolbox utilities data structures',
)

