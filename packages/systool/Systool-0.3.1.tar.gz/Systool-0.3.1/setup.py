from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.rst"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.3.1'
DESCRIPTION = 'Utilidades para Engenharia de Transporte'
LONG_DESCRIPTION = 'Reune funções úteis para o tratamento e visualização de dados. ' \
                   'Uso particular em Engenharia de Transportes.'

# Setting up
setup(
    name="Systool",
    version=VERSION,
    author="pcardoso & bcalazans",
    author_email="bcalazans@systra.com",
    package_dir={'': 'main'},
    include_package_data=True,
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    package_data={'utils': ['charts.py', 'flatt_geom.py', 'get_ftp_data.py', 'get_socioEconomic_data.py',
                            'maps.py', 'readWrite.py', 'report.py', 'linear_regression_make.py',
                            'linear_regression_plot.py', 'misFunctions.py']},
    install_requires=['pytest',
                      'pandas',
                      'numpy',
                      'matplotlib',
                      'matplotlib_scalebar',
                      'geopandas',
                      'openpyxl',
                      'seaborn',
                      'statsmodels',
                      'tqdm',
                      'scipy',
                      'plotly',
                      'shapely'],
    keywords=['systool', 'transports', 'systra', 'engineering', 'transport engineering'],
)
