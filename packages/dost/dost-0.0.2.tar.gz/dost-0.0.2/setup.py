# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dost']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.2.0,<10.0.0',
 'PyPDF2>=2.11.0,<3.0.0',
 'PyQRCode>=1.2.1,<2.0.0',
 'PyScreeze>=0.1.28,<0.2.0',
 'barcode>=1.0.2,<2.0.0',
 'currency-symbols>=2.0.3,<3.0.0',
 'geopy>=2.2.0,<3.0.0',
 'gspread-dataframe>=3.3.0,<4.0.0',
 'gspread>=5.6.2,<6.0.0',
 'imageio>=2.22.1,<3.0.0',
 'oauth2client>=4.1.3,<5.0.0',
 'openpyxl>=3.0.10,<4.0.0',
 'pandas>=1.5.0,<2.0.0',
 'pdfplumber>=0.7.5,<0.8.0',
 'phonenumbers>=8.12.56,<9.0.0',
 'pygetwindow>=0.0.9,<0.0.10',
 'pyshorteners>=1.0.1,<2.0.0',
 'pytesseract>=0.3.10,<0.4.0',
 'pyttsx3>=2.90,<3.0',
 'pytube>=12.1.0,<13.0.0',
 'pywhatkit>=5.4,<6.0',
 'pywinauto>=0.6.8,<0.7.0',
 'pyzbar>=0.1.9,<0.2.0',
 'requests>=2.28.1,<3.0.0',
 'typeguard>=2.13.3,<3.0.0',
 'xls2xlsx>=0.1.5,<0.2.0',
 'xlsx2html>=0.4.0,<0.5.0',
 'xlwt>=1.3.0,<2.0.0',
 'yagmail>=0.15.293,<0.16.0']

setup_kwargs = {
    'name': 'dost',
    'version': '0.0.2',
    'description': 'My-DOST is a Python based Utility platform as an Open Source project. We strive to liberate humans from mundane, repetitive tasks, giving them more time to use their intellect and creativity to solve higher-order business challenges and perform knowledge work.',
    'long_description': '# My-DOST \n',
    'author': 'PyBots',
    'author_email': 'support@pybots.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': '',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.0,<=3.10.40',
}


setup(**setup_kwargs)
