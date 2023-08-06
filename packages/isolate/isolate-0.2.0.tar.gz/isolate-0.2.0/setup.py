# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['isolate',
 'isolate.backends',
 'isolate.connections',
 'isolate.connections._local',
 'isolate.connections.grpc',
 'isolate.connections.grpc.definitions',
 'isolate.connections.ipc',
 'isolate.server',
 'isolate.server.definitions']

package_data = \
{'': ['*']}

install_requires = \
['importlib-metadata>=4.4', 'virtualenv>=20.4']

extras_require = \
{'grpc': ['grpcio>=1.49', 'protobuf'], 'server': ['grpcio>=1.49', 'protobuf']}

entry_points = \
{'isolate.backends': ['conda = isolate.backends.conda:CondaEnvironment',
                      'local = isolate.backends.local:LocalPythonEnvironment',
                      'virtualenv = '
                      'isolate.backends.virtualenv:VirtualPythonEnvironment']}

setup_kwargs = {
    'name': 'isolate',
    'version': '0.2.0',
    'description': 'Managed isolated environments for Python',
    'long_description': '# Isolate\n\n> :warning: **Isolate** is still very young, and none of the APIs should be considered stable.\n\nRun any Python function, with any dependencies, in any machine you want. Isolate offers a\npluggable end-to-end solution for building, managing, and using isolated environments (virtualenv,\nconda, and possibly more).\n\n## Motivation\n\n![XKCD 1987](https://imgs.xkcd.com/comics/python_environment.png)\n\nThe fact that nearly every piece of software uses some other libraries or some\nother programs is undeniable. Each of these come with their set of dependencies,\nand this chain moves forward. Once there are enough \'nodes\' in the chain, then\nthe ["dependency mess"](https://en.wikipedia.org/wiki/Dependency_hell) starts\nto surface and our lives become much harder.\n\nPython tried to solve it by recommending the "virtual environment" concept. In\ntheory it was designed to isolate environments of different projects, so my project\nA can depend on `pandas==1.0.0` while B depends on `pandas==2.0.0` and whichever\nproject I choose to work with, I just activate its own environment.\n\nOverall this was a very nice solution that did work, and still continues to work\nfor this use case. But as with every other scoped fix, in time other problems started\nto appear that demand a much narrower scope (like defining module-level dependencies,\nor even function-level ones for cloud runtimes that allow seamless integration with the\nrest of your code running in a different machine).\n\nHowever, unlike "virtual environment" concept, each of the projects that tried to tackle\nthis problem lacked a universal interface which one can simply define a set of requirements\n(this might be dependencies, size of the machine that is needed to run it, or something completely\ndifferent) and can change it without any loss. Isolate is working towards a future where this\ntransititon is as seamless as the transition from your local environment to the remote\nenvironment.\n',
    'author': 'Features & Labels',
    'author_email': 'hello@fal.ai',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
