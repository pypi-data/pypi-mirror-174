# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['docx_form',
 'docx_form.constants',
 'docx_form.content_controls',
 'docx_form.enums',
 'docx_form.form_fields',
 'docx_form.globals',
 'docx_form.type_aliases']

package_data = \
{'': ['*']}

install_requires = \
['Sphinx>=5.1.1,<6.0.0', 'lxml>=4.9.1,<5.0.0', 'pytest>=7.1.2,<8.0.0']

setup_kwargs = {
    'name': 'docx-form',
    'version': '0.1.6',
    'description': 'DO NOT USE, THIS IS A WORK IN PROGRESS -- A library that allows the editing of form XML components in .docx files.',
    'long_description': '# docx-form\n\n## Description\n\nThis package allows you to easily modify the values of content controls on forms in Microsoft Word with python scripts. This project currently supports reading and editting of the combo box, check box, plain text, datepicker, and dropdown content controls through the package\'s functions. The file being modified can be overwritten with the new values or saved to a new file.\n\n## Setup For Use\n\n#### Requirements:\n\n- Pip\n- Python version 3.10.6 or higher\n\nSimply run "pip install docx-form" to install docx-form and its required dependencies. After pip is installed, all that is left to do is import the project with "from docx_form import DocxForm".\n[Link to Pip project](https://pypi.org/project/docx-form/)\n\n## Setup For Contribution\n\n#### Requirements:\n\n- Pip\n- Python version 3.10.6 or higher\n- Poetry 1.2.0\n\nClone the repository, for those who aren\'t familiar [https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/cloning-a-repository).\n\n## Poetry Installation\n\nFirst install Python using powershell.\nLink to install: [https://python-poetry.org/docs/](https://python-poetry.org/docs/)\nOnce installed, grab poetry application from the poetry script folder and manually add it to your Python scripts folder. Then in the project environment set the interpreter path to the pypoetry virtual environment. Run Poetry install to install all poetry\'s dependecies. For visual studio code, cmd + p is the command to select intepreter.\n\nThen fetch development and pull in changes and make a new branch off development to start contributing.\n',
    'author': 'Reece Bourgeois',
    'author_email': 'reecebourgeois@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
