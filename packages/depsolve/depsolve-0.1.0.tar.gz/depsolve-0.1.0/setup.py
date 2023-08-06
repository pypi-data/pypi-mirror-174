# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['depsolve']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.10.2,<2.0.0']

setup_kwargs = {
    'name': 'depsolve',
    'version': '0.1.0',
    'description': 'Agnostic dependencies solver',
    'long_description': '# DepSolve\nThis is an asyncio agnostic dependency tree solver\n\nThe idea is to take out the problem of depencies solving from packages managers or importers\n\n## Usage\n```python\nimport asyncio\nfrom depsolve import Dependency, walk\n\n\nasync def perform_importation(dependency: Dependency):\n    # here your package/whatever is supposed to inherit from `Dependency`\n    # if any other argument is need for the command line in the package\n    # have a look to functools.partial()\n    await asyncio.sleep(2)\n\n\nasync def main():\n    dependencies = [\n        Dependency(name=\'land\'),\n        Dependency(name=\'hen\', depends_on=[\'land\']),\n        Dependency(name=\'eggs\', depends_on=[\'hen\']),\n        Dependency(name=\'sugar_cane\', depends_on=[\'land\']),\n        Dependency(name=\'plain flour\', depends_on=[\'wheat\']),\n        Dependency(name=\'sugar\', depends_on=[\'sugar_cane\']),\n        Dependency(name=\'genoise\', depends_on=[\'eggs\', \'sugar\']),\n        Dependency(name=\'strawberry\', depends_on=[\'land\']),\n        Dependency(name=\'wheat\', depends_on=[\'land\']),\n        Dependency(name=\'sirop\', depends_on=[\'strawberry\']),\n        Dependency(name=\'cake\', depends_on=[\'genoise\', \'strawberry\', \'sirop\']),\n        Dependency(name=\'cooking\', depends_on=[\'cake\'])\n    ]\n    async for items in walk(dependencies):\n        deps_names = [dep.name for dep in items]\n        print(f\'dependencies to install: {len(items)} : {", ".join(deps_names)}\')\n        tasks = asyncio.gather(*[perform_importation(dep) for dep in items])\n        await tasks\n\n\nif __name__ == "__main__":\n    asyncio.run(main())\n```\n\nwich output:\n```\ndependencies to install: 1 : land\ndependencies to install: 4 : hen, sugar_cane, strawberry, wheat\ndependencies to install: 4 : eggs, plain flour, sugar, sirop\ndependencies to install: 1 : genoise\ndependencies to install: 1 : cake\ndependencies to install: 1 : cooking\n```\n',
    'author': 'Sebastien Nicolet',
    'author_email': 'snicolet95@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
