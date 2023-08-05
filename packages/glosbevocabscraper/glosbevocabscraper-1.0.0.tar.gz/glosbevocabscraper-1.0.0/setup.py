import setuptools
from setuptools import setup

setup(
    name='glosbevocabscraper',
    version='1.0.0',
    description='Scrapes translations, example sentences and audio from glosbe',
    url='https://github.com/dotdioscorea/glosbevocabscraper',
    author='dotdioscorea',
    author_email='git@awr.sh',
    license='MIT',
    packages=setuptools.find_packages (),
    package_data={'': ['glosbevocabscraper/*.array']},
    install_requires=['beautifulsoup4', 'requests'],
    entry_points={"console_scripts":
        {
            "gvs = glosbevocabscraper.main:main",
            "glosbevocabscraper = glosbevocabscraper.main:main"
        }},

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Education',
        'License :: OSI Approved :: MIT No Attribution License (MIT-0)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)