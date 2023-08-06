import setuptools
import os
import sys

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

#with open('requirements.txt') as f:
#    required = f.read().splitlines()
   
setuptools.setup(
    name="SEAVE", 
    author="Calum Macdonald",
    version='0.0.2',
    author_email="calmacx@gmail.com",
    description="Python package for a synthetic EAVE",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/EAVE-II/synthetic-eave",
    #entry_points = {
    #    'console_scripts':[
    #        'coconnect=coconnect.cli.cli:coconnect',
    #        'etltool=coconnect.cli.subcommands.map:run',
    #        'etl-gui=coconnect.cli.subcommands.map:gui',
    #    ],
    #},
    packages=setuptools.find_packages(),
    #extras_require = {
    #    'airflow':['apache-airflow'],
    #    'sql':['sqlalchemy','psycopg2-binary==2.8.6','sqlalchemy-utils'],
    #    'performance':['snakeviz'],
    #},
    install_requires=[
        'pandas',
        'numpy',
        'scipy',
        'matplotlib',
        'dill'
    ],
    #package_data={'coconnect': ['data/cdm/*','data/example/*/*','data/test/*/*','data/test/*/*/*']},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
