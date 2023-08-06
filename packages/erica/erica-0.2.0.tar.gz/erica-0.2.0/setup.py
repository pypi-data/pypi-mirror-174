# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['erica']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'erica',
    'version': '0.2.0',
    'description': 'flask-like zero denpendency web server.',
    'long_description': '# erica\n\n> flask-like zero denpendency web server.\n\n## Sample\n\n```py\nfrom erica import Erica, RequestHandler\n\napp = Erica()\n\n\n@app.get("/")\ndef hello(request: RequestHandler) -> None:\n    request.response.json({"message": "Hello, World!"})\n\n\n@app.post("/")\ndef q(request: RequestHandler) -> None:\n    request.response.text(f"you posted {request.text}")\n\n\napp.run()\n```\n',
    'author': 'Ryu Juheon',
    'author_email': 'saidbysolo@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
