# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['sleepydatapeek']
install_requires = \
['pandas>=1.5.1,<2.0.0']

setup_kwargs = {
    'name': 'sleepydatapeek',
    'version': '0.1.0',
    'description': 'Peek at local datafiles fast!',
    'long_description': '# **DataPeek**\n*A quick way to peek at local datafiles.*\n\n<br />\n\n## **Welcome to PKG!**\nIn short, it\'s hand to have something be able to spit out a configurable preview of data from a file, and bonus points if you can just as easily output in markdown. It would also be nice if said tool could read all the formats.\\\n**DataPeek** has entered the chat!\n\n<br />\n\n### **Table of Contents** 📖\n<hr>\n\n  - **Get Started**\n  - Usage\n  - Technologies\n  - Contribute\n  - Acknowledgements\n  - License/Stats/Author\n\n<br />\n\n## **Get Started 🚀**\n<hr>\n\nThis repo is currently private, so adding this package is all the user needs to care about.\n\n<br />\n\n## **Usage ⚙**\n<hr>\n\nTODO\n\n<br />\n\n## **Technologies 🧰**\n<hr>\n\n  - [Pandas](https://pandas.pydata.org/docs/)\n\n<br />\n\n## **Contribute 🤝**\n<hr>\n\nAs stated in the welcome section, the corresponding GitHub repo is private. \\\nHowever, feel free to [reach out with opinions](https://github.com/anthonybench)!\n\n<br />\n\n## **Acknowledgements 💙**\n<hr>\n\nCheers to the chaos of modern life for needing personalized agility in schema assessment.\n\n<br />\n\n## **License, Stats, Author 📜**\n<hr>\n\n<img align="right" alt="example image tag" src="https://i.imgur.com/jtNwEWu.png" width="200" />\n\n<!-- badge cluster -->\n\nTODO [SHIELD](https://shields.io/)\n\n<!-- / -->\nSee [License](TODO) for the full license text.\n\nThis package was authored by *Isaac Yep*.',
    'author': 'anthonybench',
    'author_email': 'anythonybenchyep@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
