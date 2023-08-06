# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mui',
 'mui.v5',
 'mui.v5.grid',
 'mui.v5.grid.filter',
 'mui.v5.grid.link',
 'mui.v5.grid.pagination',
 'mui.v5.grid.sort',
 'mui.v5.integrations',
 'mui.v5.integrations.flask',
 'mui.v5.integrations.flask.filter',
 'mui.v5.integrations.flask.pagination',
 'mui.v5.integrations.flask.sort',
 'mui.v5.integrations.sqlalchemy',
 'mui.v5.integrations.sqlalchemy.pagination',
 'mui.v5.integrations.sqlalchemy.resolver',
 'mui.v5.integrations.sqlalchemy.sort']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1,<2', 'typing-extensions>=4.4.0,<5']

setup_kwargs = {
    'name': 'mui-data-grid',
    'version': '0.3.0',
    'description': "Unofficial backend utilities for using Material-UI's X-Data-Grid component",
    'long_description': '# MUI Data Grid\n\nThis is an unofficial toolbox to make integrating a Python web application with Material UI\'s data grid simpler.\n\n## Documentation\n\n- [Material-UI Data Grid](https://mui.com/x/react-data-grid/)\n\n## Requirements\n\n- Python 3.7+\n\n## Installation\n\n### Pip\n\n```sh\npython -m pip install -U \'mui-data-grid\'\n```\n\nor with extras:\n\n```sh\npython -m pip install -U \'mui-data-grid[flask]\'\npython -m pip install -U \'mui-data-grid[sqlalchemy]\'\npython -m pip install -U \'mui-data-grid[flask, sqlalchemy]\'\n```\n\n### Poetry\n\n```sh\npoetry add mui-data-grid\n```\n\n## Usage\n\n### Integrations\n\n#### Flask\n\n```python\n#!/usr/bin/env python\n# examples/main.py\n\nfrom flask import Flask, jsonify\nfrom flask.wrappers import Response\n\nfrom mui.v5.integrations.flask import get_grid_models_from_request\n\napp = Flask(__name__)\n\nFILTER_MODEL_KEY = "filter_model"\nSORT_MODEL_KEY = "sort_model[]"\nPAGINATION_MODEL_KEY = None  # stored inline in the query string, not encoded as an obj\n\n\n@app.route("/")\ndef print_sorted_details() -> Response:\n    # models will return default values if the keys don\'t exist,\n    # so you can choose what features you integrate, and when.\n    models = get_grid_models_from_request(\n        filter_model_key=FILTER_MODEL_KEY,\n        pagination_model_key=PAGINATION_MODEL_KEY,\n        sort_model_key=SORT_MODEL_KEY,\n    )\n    return jsonify(\n        {\n            # sort_model is a list[GridSortItem]\n            SORT_MODEL_KEY: [model.dict() for model in models.sort_model],\n            # filter_model is GridFilterModel\n            FILTER_MODEL_KEY: models.filter_model.dict(),\n            # pagination_model is a GridPaginationModel\n            # providing a consistent interface to pagination parameters\n            PAGINATION_MODEL_KEY: models.pagination_model,\n        }\n    )\n\n\nif __name__ == "__main__":\n    app.run()\n```\n\n#### SQLAlchemy\n\nDocumentation coming soon!\n',
    'author': 'Kevin Kirsche',
    'author_email': 'kev.kirsche@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/kkirsche/mui-data-grid',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
