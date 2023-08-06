# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cnext_server',
 'cnext_server.server',
 'cnext_server.server.python',
 'cnext_server.server.python.cassist',
 'cnext_server.server.python.code_editor',
 'cnext_server.server.python.dataframe_manager',
 'cnext_server.server.python.environment_manager',
 'cnext_server.server.python.executor_manager',
 'cnext_server.server.python.experiment_manager',
 'cnext_server.server.python.file_explorer',
 'cnext_server.server.python.file_manager',
 'cnext_server.server.python.jupyter_server_manager',
 'cnext_server.server.python.libs',
 'cnext_server.server.python.logs_manager',
 'cnext_server.server.python.model_manager',
 'cnext_server.server.python.project_manager',
 'cnext_server.server.python.user_space',
 'cnext_server.server.python.user_space.ipython',
 'cnext_server.server.tests',
 'cnext_server.server.tests.test_servers']

package_data = \
{'': ['*'],
 'cnext_server': ['public/*',
                  'public/_next/static/NVW5vpLnVXh5_1oABATLh/*',
                  'public/_next/static/chunks/*',
                  'public/_next/static/chunks/pages/*',
                  'public/_next/static/css/*',
                  'public/icons/*'],
 'cnext_server.server': ['build/*', 'ls/*', 'routes/*']}

install_requires = \
['cnextlib>=0.6.2,<0.7.0',
 'jupyter-client>=7.2.2,<7.3.0',
 'jupyter-resource-usage>=0.6.1,<0.7.0',
 'jupyterlab>=3.3.4,<3.4.0',
 'matplotlib-inline>=0.1.6,<0.2.0',
 'matplotlib>=3.5.1,<3.6.0',
 'mlflow>=1.29.0,<2.0.0',
 'multipledispatch>=0.6.0,<0.7.0',
 'netron>=6.0.0,<7.0.0',
 'pandas>=1.3.5,<1.4.0',
 'plotly>=5.7.0,<5.8.0',
 'protobuf==3.20.1',
 'pyreadline>=2.1,<3.0',
 'python-language-server>=0.36.2,<0.37.0',
 'pyyaml>=5.1,<6.0',
 'pyzmq>=23.2.0,<24.0.0',
 'requests>=2.27.1,<3.0.0',
 'send2trash>=1.8.0,<2.0.0',
 'sentry-sdk>=1.5.12,<2.0.0',
 'simplejson>=3.17.6,<4.0.0']

entry_points = \
{'console_scripts': ['cnext = cnext_server.__main__:main']}

setup_kwargs = {
    'name': 'cnext',
    'version': '0.10.4',
    'description': 'The data-centric workspace for AI & DS',
    'long_description': '<div align="center">\n  <a href="https://www.cnext.io">\n    <img\n      src="https://avatars.githubusercontent.com/u/105595528?s=200&v=4"\n      alt="CNext Logo"\n      height="64"\n    />\n  </a>\n  <br />\n  <p>\n    <h3>\n      <b>\n        CNext\n      </b>\n    </h3>\n  </p>\n  <p>\n    <b>\n      Open source workspace designed for DS & AI workflows\n    </b>\n  </p>\n  <p>\n     <a href="https://pepy.tech/project/cnext">\n     <img\n        src="https://static.pepy.tech/personalized-badge/cnext?period=total&units=international_system&left_color=black&right_color=green&left_text=Downloads"\n        alt="Cnext"\n      />\n      </a>\n      <a href="https://docs.cnext.io/">\n      <img\n        src="https://img.shields.io/badge/docs-GitBook-blue"\n        alt="docs"\n      />\n      </a>\n      <a href="https://www.cnext.io/">\n      <img\n        src="https://img.shields.io/badge/website-CNext-brightgreen"\n        alt="site"\n      />\n      </a>\n      <a href="https://hub.docker.com/r/cycai/cnext">\n      <img\n        src="https://img.shields.io/badge/docker-CNext-blue"\n        alt="docker"\n      />\n      </a>\n      <a href="https://www.youtube.com/watch?v=5eWPkQIUfZw">\n      <img\n        src="https://img.shields.io/badge/demo-YouTube-red"\n        alt="youtube"\n      />\n      </a>\n      <a href="https://join.slack.com/t/cnextcommunity/shared_invite/zt-1ay12cvpx-M29uASHZbFfQ989tVgCHVg">\n      <img\n        src="https://img.shields.io/badge/chat-Slack-purple"\n        alt="slack"\n      />\n      </a>\n  </p>\n  <p>\n    <sub>\n      Built with ❤︎ by\n      <a href="https://github.com/cnextio/cnext/graphs/contributors">\n        contributors\n      </a>\n    </sub>\n  </p>\n  \n  <a href="https://www.cnext.io" target="_blank">\n      <img\n        src="https://www.cnext.io/gifs/2nd.gif"\n        alt="Cnext"\n        width="80%"\n      />\n</div>\n\n\n\n\n## 🔮 Overview\n\nCNext is a workspace for DS and AI workflows. This workspace is meant to consolidate the most common tasks performed by data scientists and ML engineers. At a high level our workspace allows for:\n\n-   Data exploration & transformation\n-   Model development / exploration\n-   Production code generation\n-   Dashboard & App Generation\n-   Experiment Management\n\n## 📢 Features\n\n-   Interactive Python coding envrionment with native Python output (think Jupyter replacement)\n-   Smart code suggestion (categorical values and column names)\n-   Interactive data exploration\n-   Automative visualizations\n-   Experiment and model management\n-   Instant dashboarding\n\n🚀 **Requests:** We\'re actively developing features based off user feedback, if you\'d like to make any suggestions please feel free to hit us up on Slack. \n\n## 📄 Installation via Pip\n\nPLEASE NOTE: CNext requires npm >= 18.4 and Python >= 3.9.7 . Please ensure your environment meets the minimum requirements before beginning the installation. \n\nStep 1: Make sure `Nodejs` is available in your computer (try `npm --version`)\n\nStep 2: `run` command `pip install -U cnext`\n\nStep 3: `run` command `cnext`\n\n-   Input `Enter path to the cnext sample project created in Step 1` and hit `Enter` (Example `C:/Skywalker`)\n\n-   Web application will launch at : `http://localhost:CLIENT_PORT` or `http://127.0.0.1:CLIENT_PORT/` (CLIENT_PORT default is 4000)\n-   Stop application: `Ctrl + c | Command + c`\n-   Note: Pay attention at `CLIENT_PORT`, and `SERVER_PORT` in `.env` file (you will have to change these ports if you already use them on your machine)\n\n## 📄 Installation via Docker\n\ncnext is also available via pre-built Docker images. To get started, you can simply run the following command:\n\n```bash\ndocker run --rm -it -p 4000:4000 -p 5000:5000 -p 5011:5011 -p 5008:5008 -p 5005:5005 cycai/cnext\n```\n\nThe web application will launch at: `http://localhost:4000` or `http://127.0.0.1:4000/`\n\n## License\n\nCopyright 2022 CycAI Inc. Distributed under MIT License. \n\u200b\nPermission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:\n\u200b\nThe above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.\n\u200b\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.\n\n[website]: https://www.cnext.io/\n[docker image]: https://hub.docker.com/r/cycai/cnext\n[documentation]: https://docs.cnext.io/\n[overview video]: https://youtu.be/5eWPkQIUfZw\n[cnext]: https://drive.google.com/file/d/1ft4PmFclylOtEAQSPBqn9nUSyAkMs5R-\n[docker]: https://www.docker.com/products/docker-desktop/\n',
    'author': 'CycAI Inc',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://cyc-ai.com/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9',
}


setup(**setup_kwargs)
