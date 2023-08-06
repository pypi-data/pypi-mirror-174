# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['dirtyflags']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'dirtyflags',
    'version': '1.0.2',
    'description': 'dirtyflags is a simple Python decorator that tracks when and which instance attributes have changed.',
    'long_description': '# dirtyflags\n\n**dirtyflags** is a simple Python decorator that tracks when and which instance attributes have changed.\n\n```python\n>>> from dirtyflags import dirtyflag\n>>> @dirtyflag\n>>> class ChangingObject():\n>>>     def __init__(self, attr1: int, attr2: str = "Default Value"):\n>>>         self.attr1 = attr1\n>>>         self.attr2 = attr2\n>>> \n>>>     def __str__(self):\n>>>         return (f"attr1 = {self.attr1}, attr2=\'{self.attr2}\'")\n\n>>> # create an instance of the class\ninstance_default = ChangingObject(attr1=1)\n\n>>> print(f"instance_default is: {instance_default}")\ninstance_default is: attr1 = 1, attr2=\'Default Value\'\n\n>>> # dirtyflags tracks whether a change has occurred - in this case it has not\n>>> print(f"Has this instance changed = {instance_default.is_dirty()}")\nHas this instance changed = False\n\n>>> # now change the value of an attribute\n>>> instance_default.attr1 = 234\n>>> # now dirty flag indicates the class has changed - and tells you what has changed\n>>> print(f"Has this instance changed = {instance_default.is_dirty()}")\n>>> print(f"The attribute(s) that have changed: {instance_default.dirty_attrs()}")\nHas this instance changed = True\nThe attribute(s) that have changed: {\'attr1\'}\n\n>>> # dirtyflags even tracks changes when using __setter__\n>>> instance_default.__setattr__(\'attr2\', \'changed the default\')\n>>> print(f"Has this instance changed = {instance_default.is_dirty()}")\n>>> print(f"The attribute(s) that have changed: {instance_default.dirty_attrs()}")\nHas this instance changed = True\nThe attribute(s) that have changed: {\'attr2\', \'attr1\'}\n```\n\n## Installing dirtyflags\n\n\n```console\npip install dirtyflags\n```\ndirtyflags officially supports Python 3.8+\n\n## Supported Features and Best Practices\n- Sinmply use the `@dirtyflag` decorator\n- Supports attributes of any datatype, built-in or custom\n- Works with Python dataclasses\n- Nested classes should have the \'@dirtyflag\' decorator applied as well\n\n\n---\n',
    'author': 'jamesxcode',
    'author_email': 'james.x.johnson@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/jamesxcode/dirtyflags',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
