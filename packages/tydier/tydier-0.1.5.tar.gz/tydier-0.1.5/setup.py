# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['tydier']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.4.4,<2.0.0']

setup_kwargs = {
    'name': 'tydier',
    'version': '0.1.5',
    'description': 'Python package for easy data cleaning operations.',
    'long_description': '# tydier\n\n`tydier` is a Python package that facilitates data cleaning and wrangling operations on `pandas` dataframes.\n\n- Project repo hosted on [GitHub](https://github.com/antobzzll/tydier).\n- Last version is [`0.1.5`](https://pypi.org/project/tydier/). Please refer to [CHANGELOG.md](https://github.com/antobzzll/tydier/blob/dev/CHANGELOG.md) for details on updates.\n\n## Installation\n\n```bash\n$ pip install tydier\n```\n\n## Why use `tydier`?\n\n\n\n### Use `tydier` to automatically **identify and fix incorrect categorical variable values**\n\n```python\nimport tydier as ty\nimport pandas as pd\n\ndirty_cats = [\'monday\', \'Tusday\', \'Wednesday\', \'thurda\', \'Firday\', \'saty\', \'Sunday\']\nclean_cats = [\'Monday\', \'Tuesday\', \'Wednesday\', \'Thursday\', \'Friday\', \'Saturday\', \'Sunday\']\n\ndf = pd.DataFrame({\'dirty_cats\': dirty_cats, \'clean_cats\': clean_cats})\n\nty.inconsistent_categories(dirty_cats, clean_cats)\n```\n```\n[\'Firday\', \'Tusday\', \'thurda\', \'saty\', \'monday\']\n```\nSetting `mapping_dict` to `True`, will return a dictionary which we can pass to `pandas.Series.replace()` to automatically replace inconsistent categorical values in a `pandas.Series`:\n```python\nmapping = ty.inconsistent_categories(dirty_cats, clean_cats, mapping_dict=True)\ndf[\'cleaned_dirty_cats\'] = df[\'dirty_cats\'].replace(mapping)\ndf\n```\n|dirty_cats\t| clean_cats | cleaned_dirty_cats|\n| --- | ---| --- |\n| monday | Monday | Monday|\n| Tusday | Tuesday | Tuesday|\n| Wednesday | Wednesday | Wednesday|\n| thurda | Thursday | Thursday|\n| Firday | Friday | Friday|\n| saty | Saturday | Saturday|\n| Sunday | Sunday | Sunday|\n\n### Use `tydier` to automatically transform into `float` a **currency `string` variable**, containing symbols and inconsistent spaces\n```python\nprices = ["  23,000.12 $", "123,000.56USD", "$45", "$ 56,90"]\n\nv, c = ty.currency_to_float(prices)\nprint("Values:")\nprint(v)\nprint("Currencies:")\nprint(c)\n```\n```\nValues:\n[23000.12, 123000.56, 45.0, 56.9]\nCurrencies:\n[\'$\', \'USD\', \'$\', \'$\']\n```\n\n### Use `tydier` to automatically **clean column names**\n```python\ndf.columns = [\'    Dirty  categorieS\', \'Clean Categories\']\ndf.columns = ty.clean_col_names(df.columns)\nprint(df.columns)\n```\n```\nIndex([\'dirty_categories\', \'clean_categories\'], dtype=\'object\')\n```\nFor complete usage examples please check the [example notebook](https://github.com/antobzzll/tydier/blob/dev/docs/example.ipynb).\n\n## Contributing\n\n**Found a bug?** Please report it [here](https://github.com/antobzzll/tydier/issues).\n\n**Have an idea and want to make a suggestion?** Feel free to update the [TODO list](https://github.com/antobzzll/tydier/blob/dev/TODO.md).\n\n**Interested in contributing?** Check out what\'s on the [TODO list](https://github.com/antobzzll/tydier/blob/dev/TODO.md) and the [contributing guidelines](https://github.com/antobzzll/tydier/blob/dev/CONTRIBUTING.md). Please note that this project is released with a [Code of Conduct](https://github.com/antobzzll/tydier/blob/dev/CONDUCT.md). By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`tydier` was created by [Antonio Buzzelli](https://github.com/antobzzll). It is licensed under the terms of the MIT license.\n\n## Credits\n\n`tydier` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the [`py-pkgs-cookiecutter` template](https://github.com/py-pkgs/py-pkgs-cookiecutter).\n',
    'author': 'Antonio Buzzelli',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
