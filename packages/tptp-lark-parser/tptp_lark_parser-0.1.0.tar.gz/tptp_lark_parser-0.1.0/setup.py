# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tptp_lark_parser']

package_data = \
{'': ['*'],
 'tptp_lark_parser': ['resources/*',
                      'resources/TPTP-mock/Axioms/*',
                      'resources/TPTP-mock/Problems/TST/*']}

install_requires = \
['lark-parser']

extras_require = \
{':python_version < "3.9"': ['importlib_resources']}

setup_kwargs = {
    'name': 'tptp-lark-parser',
    'version': '0.1.0',
    'description': 'A TPTP parser using Lark',
    'long_description': '..\n  Copyright 2022 Boris Shminke\n\n  Licensed under the Apache License, Version 2.0 (the "License");\n  you may not use this file except in compliance with the License.\n  You may obtain a copy of the License at\n\n      https://www.apache.org/licenses/LICENSE-2.0\n\n  Unless required by applicable law or agreed to in writing, software\n  distributed under the License is distributed on an "AS IS" BASIS,\n  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n  See the License for the specific language governing permissions and\n  limitations under the License.\n\n|Binder|\\ |PyPI version|\\ |Anaconda|\\ |CircleCI|\\ |AppveyorCI|\\ |Documentation Status|\\ |codecov|\\ |Zenodo|\n\ntptp-lark-parser\n================\n\n``tptp-lark-parser`` is a parser for the `TPTP library\n<https://tptp.org>`__ language using the `Lark parser\n<https://github.com/lark-parser/lark>`__. For now, only CNF\nsublanguage is supported.\n\nHow to Install\n==============\n\nThe best way to install this package is to use ``pip``:\n\n.. code:: sh\n\n   pip install tptp-lark-parser\n\nThe package is also available on ``conda-forge``:\n   \n.. code:: sh\n\n   conda install -c conda-forge tptp-lark-parser\n   \nOne can also run it in a Docker container:\n\n.. code:: sh\n\n   docker build -t tptp-lark-parser https://github.com/inpefess/tptp-lark-parser.git\n   docker run -it --rm -p 8888:8888 tptp-lark-parser jupyter-lab --ip=0.0.0.0 --port=8888\n\nHow to Use\n==========\n\n.. code:: python\n\n   from tptp_lark_parser import TPTPParser\n\n   tptp_parser = TPTPParser()\n   parsed_text = tptp_parser.parse("cnf(test, axiom, ~ p(Y, X) | q(X, Y)).")\n   clause_literals = parsed_text[0].literals\n   \nSee `the\nnotebook <https://github.com/inpefess/tptp-lark-parser/blob/master/notebooks/usage-example.ipynb>`__\nor run it in\n`Binder <https://mybinder.org/v2/gh/inpefess/tptp-lark-parser/HEAD?labpath=usage-example.ipynb>`__\nfor more information.\n\nMore Documentation\n==================\n\nMore documentation can be found\n`here <https://tptp-lark-parser.readthedocs.io/en/latest>`__.\n\nSimilar Projects\n================\n\nThere are many TPTP parsers in different languages:\n\n* `C <https://github.com/TPTPWorld/SyntaxBNF>`__ (by TPTP\'s creator Geoff Sutcliffe)\n* `Java <https://github.com/marklemay/tptpParser>`__\n* `C++ <https://github.com/leoprover/tptp-parser>`__\n* `JavaScript <https://www.npmjs.com/package/tptp>`__\n* `Rust <https://github.com/MichaelRawson/tptp>`__\n* `Common Lisp <https://github.com/lisphacker/cl-tptp-parser>`__\n* `Scala <https://github.com/leoprover/scala-tptp-parser>`__\n* `Haskell <https://github.com/aztek/tptp>`__\n* `OCaml <https://github.com/Gbury/dolmen>`__\n\nThere also is `another parser in Python <https://github.com/AndrzejKucik/tptp_python_parser>`__ containing only the Lark syntax file.\n\nHow to Cite\n===========\n\nIf you want to cite the `tptp-lark-parser` in your research paper,\nplease use the following doi:\n`<https://doi.org/10.5281/zenodo.7040540>`__.\n\nHow to Contribute\n=================\n\nPlease read `the Code of Conduct\n<https://tptp-lark-parser.readthedocs.io/en/latest/code-of-conduct.html>`__\nand then follow `the contribution guide\n<https://tptp-lark-parser.readthedocs.io/en/latest/contributing.html>`__.\n\n.. |PyPI version| image:: https://badge.fury.io/py/tptp-lark-parser.svg\n   :target: https://badge.fury.io/py/tptp-lark-parser\n.. |CircleCI| image:: https://circleci.com/gh/inpefess/tptp-lark-parser.svg?style=svg\n   :target: https://circleci.com/gh/inpefess/tptp-lark-parser\n.. |Documentation Status| image:: https://readthedocs.org/projects/tptp-lark-parser/badge/?version=latest\n   :target: https://tptp-lark-parser.readthedocs.io/en/latest/?badge=latest\n.. |codecov| image:: https://codecov.io/gh/inpefess/tptp-lark-parser/branch/master/graph/badge.svg\n   :target: https://codecov.io/gh/inpefess/tptp-lark-parser\n.. |Binder| image:: https://mybinder.org/badge_logo.svg\n   :target: https://mybinder.org/v2/gh/inpefess/tptp-lark-parser/HEAD?labpath=usage-example.ipynb\n.. |AppveyorCI| image:: https://ci.appveyor.com/api/projects/status/7n0g3a3ag5hjtfi0?svg=true\n   :target: https://ci.appveyor.com/project/inpefess/tptp-lark-parser\n.. |Anaconda| image:: https://anaconda.org/conda-forge/tptp-lark-parser/badges/version.svg\n   :target: https://anaconda.org/conda-forge/tptp-lark-parser\n.. |Zenodo| image:: https://zenodo.org/badge/DOI/10.5281/zenodo.7040540.svg\n   :target: https://doi.org/10.5281/zenodo.7040540\n',
    'author': 'Boris Shminke',
    'author_email': 'boris@shminke.ml',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/inpefess/tptp-lark-parser',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.1,<3.12',
}


setup(**setup_kwargs)
