# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['icortex', 'icortex.kernel', 'icortex.services']

package_data = \
{'': ['*'], 'icortex.kernel': ['icortex/*']}

install_requires = \
['Pygments>=2.13.0,<3.0.0',
 'entrypoints>=0.4,<0.5',
 'ipykernel>=6.16.0,<7.0.0',
 'ipython>=8.5.0,<9.0.0',
 'ipywidgets>=8.0.2,<9.0.0',
 'jupyter-client>=7.4.2,<8.0.0',
 'jupyter-console>=6.4.4,<7.0.0',
 'jupyter-core>=4.11.1,<5.0.0',
 'jupyterlab-widgets>=3.0.3,<4.0.0',
 'requests>=2.28.1,<3.0.0',
 'toml>=0.10.2,<0.11.0']

entry_points = \
{'console_scripts': ['icortex = icortex.cli:main']}

setup_kwargs = {
    'name': 'icortex',
    'version': '0.1.1',
    'description': 'Jupyter kernel that can generate Python code from natural language prompts',
    'long_description': '<p align="center">\n    <a href="https://icortex.ai/"><img src="https://raw.githubusercontent.com/textcortex/icortex/main/assets/logo/banner.svg"></a>\n    <br />\n    <br />\n    <a href="https://github.com/textcortex/icortex/workflows/Build/badge.svg"><img src="https://github.com/textcortex/icortex/workflows/Build/badge.svg" alt="Github Actions Status"></a>\n    <a href="https://pypi.org/project/icortex/"><img src="https://img.shields.io/pypi/v/icortex.svg?style=flat&logo=pypi" alt="PyPI Latest Release"></a>\n    <a href="https://pepy.tech/project/icortex"><img src="https://pepy.tech/badge/icortex/month?" alt="Downloads"> </a>\n    <a href="https://icortex.readthedocs.io/en/latest/?badge=latest"><img src="https://readthedocs.org/projects/icortex/badge/?version=latest" alt="Documentation Status"></a>\n    <a href="https://github.com/textcortex/icortex/blob/main/LICENSE"><img src="https://img.shields.io/github/license/textcortex/icortex.svg?color=blue" alt="License"></a>\n    <a href="https://discord.textcortex.com/"><img src="https://dcbadge.vercel.app/api/server/QtfGgKneHX?style=flat" alt="Discord"></a>\n    <a href="https://twitter.com/TextCortex/"><img src="https://img.shields.io/twitter/url/https/twitter.com/cloudposse.svg?style=social&label=Follow%20%40TextCortex" alt="Twitter"></a>\n    <br />\n    <br />\n    <i>A Python library for <a href="https://en.wikipedia.org/wiki/Soft_computing">soft-code</a> development — program in plain English with AI code generation!</i>\n</p>\n<hr />\n\nICortex is a [Jupyter kernel](https://jupyter-client.readthedocs.io/en/latest/kernels.html) that lets you develop **soft programs**:\n\n- sets of instructions (i.e. prompts) [written in natural language](https://en.wikipedia.org/wiki/Natural-language_programming) (such as English)\n- processed by language models that generate Python code\n- to perform useful work in various contexts\n- more flexibly than regular software.\n\nTo put it simply—in goes English, out comes Python:\n\nhttps://user-images.githubusercontent.com/2453968/196814906-1a0de2a1-27a7-4aec-a960-0eb21fbe2879.mp4\n\nTODO: Prompts are given using the %prompt magic now, update the video accordingly\n\nICortex is ...\n\n- a drop-in replacement for the IPython kernel. Prompts can be executed with the [magic commands](https://ipython.readthedocs.io/en/stable/interactive/magics.html) `%prompt` or `%p` for short.\n- interactive—install missing packages directly, decide whether to execute the generated code or not, and so on, directly in the Jupyter Notebook cell.\n- open source and fully extensible—if you think we are missing a model or an API, you can request it by creating an issue, or implement it yourself by subclassing `ServiceBase` under [`icortex/services`](icortex/services).\n\nIt is similar to [Github Copilot](https://github.com/features/copilot) but with certain differences that make it stand out:\n\n| Feature | GitHub Copilot | ICortex |\n|---|:---:|:---:|\n| Generates code ... | In the text editor | In a [Jupyter kernel](https://docs.jupyter.org/en/latest/projects/kernels.html) (language backend that provides the execution environment) |\n| From ... | Existing code and comments | Plain English prompts |\n| Level of control over context used to generate code | Low | High |\n| Plain language instructions are ... | Just comments | Standalone programs |\n| The resulting program is ... | Static | Dynamic—adapts to the context it is executed in |\n| Can connect to different code generation APIs | No | Yes |\n\nThe main difference between ICortex and a code-generation plugin like GitHub Copilot is that ICortex is a programming paradigm similar to [literate programming](https://en.wikipedia.org/wiki/Literate_programming) or [natural language programming](https://en.wikipedia.org/wiki/Natural-language_programming), where the natural language prompt is the first-class citizen, and which allows for fine-grained control over the code-generation context.\n\nICortex is currently in alpha, so expect breaking changes. We are giving free credits to our first users—[join our Discord](https://discord.textcortex.com/) to help us shape it.\n\n## Installation\n\nInstall directly from PyPI:\n\n```sh\npip install icortex\n# This line is needed to install the kernel spec to Jupyter:\npython -m icortex.kernel.install\n```\n\n## Quickstart\n\n[Click here to visit the docs and get started using ICortex](https://icortex.readthedocs.io/en/latest/quickstart.html).\n\n## Getting help\n\nFeel free to ask questions in our [Discord](https://discord.textcortex.com/).\n\n## Uninstalling\n\nTo uninstall, run\n\n```bash\npip uninstall icortex\n```\n\nThis removes the package, however, it may still leave the kernel spec in Jupyter\'s kernel directories, causing it to continue showing up in JupyterLab. If that is the case, run\n\n```\njupyter kernelspec uninstall icortex -y\n```\n',
    'author': 'TextCortex Team',
    'author_email': 'onur@textcortex.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://icortex.ai/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
