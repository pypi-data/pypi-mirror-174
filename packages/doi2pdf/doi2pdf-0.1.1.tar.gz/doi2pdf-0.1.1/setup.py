# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['doi2pdf']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.11.1,<5.0.0', 'requests>=2.28.1,<3.0.0']

entry_points = \
{'console_scripts': ['doi2pdf = doi2pdf.main:main']}

setup_kwargs = {
    'name': 'doi2pdf',
    'version': '0.1.1',
    'description': 'Retrieve research paper PDF from DOI, name or URL of the research paper',
    'long_description': '# doi2pdf \n`doi2pdf` is a command line tool to download PDFs of reasearch paper from DOI, name or url, written in Python.  \nIt can be used either as a command line tool or as inside a Python script.\n\n\n## Installation\n\n```bash\npip install doi2pdf\n```\n\n\n## CLI usage\n```bash\ndoi2pdf --name "Attention is all you need" --output "Transformer.pdf" --open\ndoi2pdf --url "https://arxiv.org/abs/1706.03762" --output "Transformer.pdf" --open\ndoi2pdf --doi "10.48550/arXiv.2203.15556" --output "Chinchilla.pdf" --open\n```\n\n\nCan also be used as a library.\n\n```python\nfrom doi2pdf import doi2pdf\n\ndoi2pdf("10.48550/arXiv.2203.15556", output="Chinchilla.pdf")\n```\n\n\n## Troobleshooot\n\n- If error `DOI not found` appears it means sci hub could not retrieve the paper, you might need to override default sci-hub URL with a mirror, like so:\n\n```bash\nSCI_HUB_URL=https://sci-hub.wf/ doi2pdf --name "Attention is all you need" --open\n```\n\n- If error `Paper not found` appears, you might want to try another way to retrieve the research paper, using DOI instead of name or name instead of URL.\n\n',
    'author': 'croumegous',
    'author_email': 'cyril.roumegous@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
