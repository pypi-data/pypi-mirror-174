from setuptools import setup,find_packages
from pip._internal.req import parse_requirements

#Actual setup
setup(
    name="asteq-treso",
    version='0.1',
    description='Automation of the Accountability for the BDS of IMT Atlantique Nantes',
    long_description="Scrapping + Save new transactions",
    long_description_content_type='text/plain',
    license='MIT',
    author="gloxounet",
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/Gloxounet/asteq-treso',
    keywords='asteq',
    py_modules=['excel','operations','functions','cli'],
    install_requires=[
        'selenium',
        'pandas',
        'openpyxl',
        'Click',
        'webdriver_manager',
        'packaging',
        'xlsxwriter'
        ],
    python_requires='>=3',
    entry_points='''
        [console_scripts]
        asteq-treso=cli:cli
    ''',
)