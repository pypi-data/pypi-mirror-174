from setuptools import setup, find_packages


setup(
    name='goldbox',
    version='1.0',
    description="A package of simple Python utilities and data structures.",
    license='GPLv3',
    author="Xavier Mercerweiss",
    author_email='xavifmw@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/XavierFMW/goldbox',
    keywords='toolbox utilities data structures',
)
