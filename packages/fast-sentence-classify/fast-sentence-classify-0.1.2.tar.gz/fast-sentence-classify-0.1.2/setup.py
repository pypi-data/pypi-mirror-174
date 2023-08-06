# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fast_sentence_classify',
 'fast_sentence_classify.core',
 'fast_sentence_classify.core.bp',
 'fast_sentence_classify.core.dmo',
 'fast_sentence_classify.core.svc',
 'fast_sentence_classify.datablock',
 'fast_sentence_classify.datablock.dmo',
 'fast_sentence_classify.datablock.dto',
 'fast_sentence_classify.datablock.svc']

package_data = \
{'': ['*']}

install_requires = \
['baseblock', 'spacy==3.3']

setup_kwargs = {
    'name': 'fast-sentence-classify',
    'version': '0.1.2',
    'description': 'Generic Sentence Classification Service',
    'long_description': '# Fast Sentence Classification (fast-sentence-classify)\n',
    'author': 'Craig Trim',
    'author_email': 'craigtrim@gmail.com',
    'maintainer': 'Craig Trim',
    'maintainer_email': 'craigtrim@gmail.com',
    'url': 'https://github.com/craigtrim/fast-sentence-classify',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '==3.8.5',
}


setup(**setup_kwargs)
