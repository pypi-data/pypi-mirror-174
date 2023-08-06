# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydantic_appconfig']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'boto3>=1.20.8,<2.0.0',
 'botocore>=1.23.8,<2.0.0',
 'pydantic>=1.8.2,<2.0.0']

setup_kwargs = {
    'name': 'pydantic-appconfig',
    'version': '1.0.0',
    'description': 'Helper package for using AWS App Config with Pydantic',
    'long_description': 'Pydantic AWS AppConfig\n=======================\n\n.. image:: https://badge.fury.io/py/pydantic-appconfig.svg\n    :target: https://badge.fury.io/py/pydantic-appconfig\n\n.. image:: https://img.shields.io/pypi/pyversions/pydantic-appconfig\n    :target: https://img.shields.io/pypi/pyversions/pydantic-appconfig\n\n\nEver wanted to use\n`AWS AppConfig <https://aws.amazon.com/systems-manager/features/appconfig>`_\nfor your Python app, but can\'t bear configs without\n`pydantic <https://pydantic-docs.helpmanual.io/>`_?\n\nWell, your days of using evil `.env` or `.ini` files, `ENVIRONMENT` variables or even custom providers is over!\n\nWith just a simple\n\n.. code-block:: shell\n\n    pip install pydantic-appconfig\n\nWith a lot of inspiration from this AWS `sample <https://github.com/aws-samples/sample-python-helper-aws-appconfig>`_.\n\n\nIntroducing `pydantic_appconfig`.\n\n#. Set yourself up with your favourite `pydantic.BaseModel`:\n\n    .. code-block:: python\n\n        class MyAppConfig(pydantic.BaseModel):\n            """My app config."""\n\n            test_field_string: str\n            test_field_int: int\n\n            class Config:\n                """The pydantic config, including title for the JSON schema."""\n\n                title = "MyAppConfig"\n\n#. Set up the config helper using your shiny config class:\n\n    .. code-block:: python\n\n        from pydantic_appconfig import AppConfigHelper\n\n        my_config: AppConfigHelper[MyAppConfig] = AppConfigHelper(\n            appconfig_application="AppConfig-App",\n            appconfig_environment="AppConfig-Env",\n            appconfig_profile="AppConfig-Profile",\n            max_config_age=15,\n            fetch_on_init=True,\n            config_schema_model=MyAppConfig,\n        )\n\n\n#. Use it:\n\n    .. code-block:: python\n\n        my_val = my_config.config.test_field_string\n\n\nAWS AppConfig also has support for `validators <https://docs.aws.amazon.com/appconfig/latest/userguide/appconfig-creating-configuration-and-profile-validators.html>`_.\n\nPydantic is able to generate a JSON schema for you to upload:\n\n   .. code-block:: python\n\n       print(MyAppConfig.schema_json(indent=2))\n\n   .. code-block:: JSON\n\n       {\n         "title": "MyAppConfig",\n         "description": "My app config.",\n         "type": "object",\n         "properties": {\n           "test_field_string": {\n             "title": "Test Field String",\n             "type": "string"\n           },\n           "test_field_int": {\n             "title": "Test Field Int",\n             "type": "integer"\n           }\n         },\n         "required": [\n           "test_field_string",\n           "test_field_int"\n         ]\n       }\n',
    'author': 'Validus Tech Team',
    'author_email': 'techteam@validusrm.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Validus-Risk-Management/aws-appconfig-pydantic',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
