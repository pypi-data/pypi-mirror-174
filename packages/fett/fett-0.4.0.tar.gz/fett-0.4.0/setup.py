# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fett']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'fett',
    'version': '0.4.0',
    'description': 'A fast indentation-preserving template engine.',
    'long_description': '.. |travis| image:: https://travis-ci.org/i80and/fett.svg?branch=master\n            :target: https://travis-ci.org/i80and/fett\n\n=============\nFett |travis|\n=============\n\nOverview\n--------\n\nExample\n-------\n\n.. code-block:: python\n\n   import fett\n\n   fett.Template(\'\'\'{{ for customer in customers }}\n   {{ if i even }}\n   Even: {{ customer.name }}\n   {{ else }}\n   Odd: {{ customer.name }}\n   {{ end }}\n   {{ else }}\n   No customers :(\n   {{ end }}\'\'\').render({\'customers\': [\n       {\'name\': \'Bob\'},\n       {\'name\': \'Elvis\'},\n       {\'name\': \'Judy\'}\n   ]})\n\nSyntax\n------\n\n==========================================   ===========\nTag Format                                   Description\n==========================================   ===========\n``{{ <expression> }}``                       Substitutions_\n``{{ `foo` <expression> }}``                 Substitutions_\n``{{ format <name> }}``                      Metaformatting_\n``{{ if <expression> }}``                    Conditionals_\n``{{ for <name> in <expression> }}``         Loops_\n``{{ else }}``\n``{{ end }}``                                Block termination\n``{{ # <comment> }}``                        Comments_\n==========================================   ===========\n\nSpaces between tag opening/closing delimiters are optional.\n\nExpressions\n~~~~~~~~~~~\n\nAn **expression** is given for Substitutions_, Conditionals_, and Loops_.\n\nExpressions take the following form:\n\n    <name>[.<subfield>...] [<filter> [<filter2>...]]\n\nInstead of specifying a field path, you can start an expression using\na string literal:\n\n    `<literal>` [<filter> [<filter2>...]]\n\nYou can use **filters** to modify a single value in simple ways. For example,\nthe loop iteration counter ``i`` counts from ``0``, but users often wish to\ncount from ``1``. You can obtain a count-from-1 value with the expression\n``i inc``.\n\nThe full list of filters:\n\n===========  ======\nFilter Name  Effect\n===========  ======\ncar          Returns the first element of a list.\ncdr          Returns all but the first element of a list.\ndec          Decrements a value representable as an integer by one.\neven         Returns true iff its input is representable as an even integer.\nescape       Encodes `&`, `<`, `>`, `"`, and `\'` characters with HTML entities.\ninc          Increments a value representable as an integer by one.\nlen          Returns the length of a list.\nnot          Returns the inverse of a boolean.\nodd          Returns true iff its input is representable as an odd integer.\nnegative     Returns true iff its input is representable as an integer < 0.\npositive     Returns true iff its input is representable as an integer > 0.\nsplit        Splits a value into a list by whitespace.\nstrip        Returns the input string with surrounding whitespace removed.\nstriptags    Remove HTML tags from a value.\ntimesNegOne  Returns int(input) * -1\nzero         Returns true iff the input is zero\n===========  ======\n\n===========  ======\nFilter Name  Effect\n===========  ======\nupperCase    Returns a Unicode-aware uppercase version of the input.\nlowerCase    Returns a Unicode-aware lowercase version of the input.\n===========  ======\n\n=====================  ======\nFilter Name            Effect\n=====================  ======\nadd(n)                 Increments a value representable as an integer by `n`.\nminus(n)               Decrements a value representable as an integer by `n`.\nequal(value)           Returns true iff a value equals the given value.\nlessThan(n)            Returns true iff n < the given value.\nlessThanOrEqual(n)     Returns true iff n <= the given value.\ngreaterThan(n)         Returns true iff n > the given value.\ngreaterThanOrEqual(n)  Returns true iff n >= the given value.\n=====================  ======\n\nSubstitutions\n~~~~~~~~~~~~~\n\nMetaformatting\n~~~~~~~~~~~~~~\n\nConditionals\n~~~~~~~~~~~~\n\nLoops\n~~~~~\n\nComments\n~~~~~~~~\n',
    'author': 'Heli Aldridge',
    'author_email': 'heli@heli.pet',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
