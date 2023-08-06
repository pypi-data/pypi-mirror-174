# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['simplexl']

package_data = \
{'': ['*']}

install_requires = \
['openpyxl>=3.0.10,<4.0.0']

setup_kwargs = {
    'name': 'simplexl',
    'version': '1.0.1',
    'description': '',
    'long_description': '# SIMPLEXL\n\nSimplexl is a Python package which is used to create excel files dynamically using a program. This package depends on [openpyxl](https://pypi.org/project/openpyxl/) which is native python package for creating excel.\n\n# FEATURES\n\n- Generated formatted excel as ouput.\n- Automatically pick the width of column based on data size of column.\n\n\n# Installation\n```\npip install simplexl\n```\n\n# How to use\n\nThe usage of simplexl is as follows \n- \n\n```\nfrom simplexl import CreateExcel\n\nxl = CreateExcel(\n    excel_name="path/name of the excel  #  default = generate-simplexl.xlsx\n)\n\nxl.create_sheet(\n    sheet_name=sheet_name,   # optional  default = sheet1\n    sheet_index=sheet_index  # optional default = 0\n    col_data=col_data,\n    row_data=row_data\n)\n\n```\n\n# Example\n\n```\nfrom simplexl import CreateExcel\n\ncol_data = [\'col1\', \'col2\']\nrow_data = [\n    (\'col1_row1\', \'col2_row1\'),\n    (\'col1_row2\', \'col2_row2\')\n]\nxl = CreateExcel()\n\nxl.create_sheet(\n    col_data=col_data,\n    row_data=row_data\n)\n```\nIt will create a xlsx file using row and col data \n\n# License\n\nCopyright (c) 2022 Devaraju Garigapati\n\nThis repository is licensed under the [MIT](https://opensource.org/licenses/MIT) license.\nSee [LICENSE](https://opensource.org/licenses/MIT) for details.',
    'author': 'Devaraju Garigapati',
    'author_email': 'devarajugarigapati@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/devarajug/simplexl',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
