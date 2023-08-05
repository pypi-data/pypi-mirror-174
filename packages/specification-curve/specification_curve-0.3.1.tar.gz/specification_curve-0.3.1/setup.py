# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['specification_curve']

package_data = \
{'': ['*'], 'specification_curve': ['data/*']}

install_requires = \
['matplotlib>=3.6.1,<4.0.0',
 'pandas>=1.5.1,<2.0.0',
 'statsmodels>=0.13.2,<0.14.0']

entry_points = \
{'console_scripts': ['specification_curve = specification_curve.__main__:main']}

setup_kwargs = {
    'name': 'specification-curve',
    'version': '0.3.1',
    'description': 'Specification_Curve',
    'long_description': '# Specification Curve\n\nSpecification Curve is a Python package that performs specification curve analysis; it helps with the problem of the "garden of forking paths" (many defensible choices) when doing analysis by running many regressions and summarising the effects in an easy to digest chart.\n\n[![PyPI](https://img.shields.io/pypi/v/specification_curve.svg)](https://pypi.org/project/specification_curve/)\n[![Status](https://img.shields.io/pypi/status/specification_curve.svg)](https://pypi.org/project/specification_curve/)\n[![Python Version](https://img.shields.io/pypi/pyversions/specification_curve)](https://pypi.org/project/specification_curve)\n[![License](https://img.shields.io/pypi/l/specification_curve)](https://opensource.org/licenses/MIT)\n[![Tests](https://github.com/aeturrell/specification_curve/workflows/Tests/badge.svg)](https://github.com/aeturrell/specification_curve/actions?workflow=Tests)\n[![Codecov](https://codecov.io/gh/aeturrell/specification_curve/branch/main/graph/badge.svg)](https://codecov.io/gh/aeturrell/specification_curve)\n[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)\n[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Google Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/gist/aeturrell/438fb066e4471312667268669cef2c11/specification_curve-examples.ipynb)\n[![DOI](https://zenodo.org/badge/282989537.svg)](https://zenodo.org/badge/latestdoi/282989537)\n[![Downloads](https://static.pepy.tech/badge/specification-curve)](https://pepy.tech/project/Specification_curve)\n\n[![Linux](https://svgshare.com/i/Zhy.svg)](https://svgshare.com/i/Zhy.svg)\n[![macOS](https://svgshare.com/i/ZjP.svg)](https://svgshare.com/i/ZjP.svg)\n[![Windows](https://svgshare.com/i/ZhY.svg)](https://svgshare.com/i/ZhY.svg)\n\n[![Source](https://img.shields.io/badge/source%20code-github-lightgrey?style=for-the-badge)](https://github.com/aeturrell/specification_curve)\n\n[Go to the full documentation for **Specification Curve**](https://aeturrell.github.io/specification_curve/).\n\n## Quickstart\n\nYou can try out specification curve right now in [Google Colab](https://colab.research.google.com/gist/aeturrell/438fb066e4471312667268669cef2c11/specification_curve-examples.ipynb).\n\nHere\'s an example of using **Specification Curve**.\n\n```python\n# import specification curve\nimport specification_curve as specy\n\n\n# Generate some fake data\n# ------------------------\nimport numpy as np\nimport pandas as pd\n# Set seed for random numbers\nseed_for_prng = 78557\n# prng=probabilistic random number generator\nprng = np.random.default_rng(seed_for_prng)\nn_samples = 400\n# Number of dimensions\nn_dim = 4\nc_rnd_vars = prng.random(size=(n_dim, n_samples))\ny_1 = (0.4*c_rnd_vars[0, :] -  # THIS IS THE TRUE VALUE OF THE COEFFICIENT\n       0.2*c_rnd_vars[1, :] +\n       0.3*prng.standard_normal(n_samples))\n# Next line causes y_2 ests to be much more noisy\ny_2 = y_1 - 0.5*np.abs(prng.standard_normal(n_samples))\n# Put data into dataframe\ndf = pd.DataFrame([y_1, y_2], [\'y1\', \'y2\']).T\ndf["x_1"] = c_rnd_vars[0, :]\ndf["c_1"] = c_rnd_vars[1, :]\ndf["c_2"] = c_rnd_vars[2, :]\ndf["c_3"] = c_rnd_vars[3, :]\n\n# Specification Curve Analysis\n#-----------------------------\nsc = specy.SpecificationCurve(\n    df,\n    y_endog=[\'y1\', \'y2\'],\n    x_exog="x_1",\n    controls=["c_1", "c_2", "c_3"])\nsc.fit()\nsc.plot()\n```\n\nGrey squares (black lines when there are many specifications) show whether a variable is included in a specification or not. Blue or red markers and error bars show whether the coefficient is positive and significant (at the 0.05 level) or red and significant, respectively.\n\n## Installation\n\nYou can install **Specification Curve** via pip:\n\n```bash\n$ pip install specification-curve\n```\n\nTo install the development version from git, use:\n\n```bash\n$ pip install git+https://github.com/aeturrell/specification_curve.git\n```\n\n## License\n\nDistributed under the terms of the [MIT license](https://opensource.org/licenses/MIT).\n\n## Credits\n\nThe package is built with [poetry](https://python-poetry.org/), while the documentation is built with [Jupyter Book](https://jupyterbook.org). Tests are run with [nox](https://nox.thea.codes/en/stable/).\n\n## Similar Packages\n\nIn RStats, there is [specr](https://github.com/masurp/specr) (which inspired many design choices in this package) and [spec_chart](https://github.com/ArielOrtizBobea/spec_chart). Some of the example data in this package is the same as in specr, but please note that results have not been cross-checked across packages.\n',
    'author': 'aeturrell',
    'author_email': 'mail@mail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://aeturrell.github.io/specification_curve/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0.0',
}


setup(**setup_kwargs)
