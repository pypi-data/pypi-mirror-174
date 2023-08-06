# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['machinery']

package_data = \
{'': ['*']}

install_requires = \
['pygame>=2.1.2,<3.0.0']

setup_kwargs = {
    'name': 'mw-machinery',
    'version': '0.0.1',
    'description': 'This is the machine description framework',
    'long_description': '# machinery\n\nA meta framework\n\n## Description\n\n* OO-Drawing\n\n* Automation\n    - nodes\n    - stages\n    - environment\n    - container\n\n* monitoring\n\n* Audio\n\n### Concepts\n* FS based\n* Auto reload with inotify\n\n### Strong tool usage\n\n* Full tool coverage\n* Full paradigm coverage\n** async\n** multiprocessing\n* pydantic\n* functional\n* opt in profiling\n* on-the fly callstack\n* flexible logging\n\n* mypy / mypyc\n* platform independent\n* support IDEs\n* pyenv\n* pipenv\n* CI integration Gitlab runner\n* profiling\n* logging\n* doctest\n* documentation\n\n## Installation\n\n## Usage\n\n\n## Test and Deploy\n\nUse the built-in continuous integration in GitLab.\n\n- [ ] [Get started with GitLab CI/CD](https://docs.gitlab.com/ee/ci/quick_start/index.html)\n- [ ] [Analyze your code for known vulnerabilities with Static Application Security Testing(SAST)](https://docs.gitlab.com/ee/user/application_security/sast/)\n- [ ] [Deploy to Kubernetes, Amazon EC2, or Amazon ECS using Auto Deploy](https://docs.gitlab.com/ee/topics/autodevops/requirements.html)\n- [ ] [Use pull-based deployments for improved Kubernetes management](https://docs.gitlab.com/ee/user/clusters/agent/)\n- [ ] [Set up protected environments](https://docs.gitlab.com/ee/ci/environments/protected_environments.html)\n\n\n## Support\n\n## Roadmap\n\n## Contributing\n\n## Authors and acknowledgment\n\n## License\n\n## Project status\n\n',
    'author': 'Frans Fürst',
    'author_email': 'frans.fuerst+gitlab@protonmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://projects.om-office.de/frans/machinery.git',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
