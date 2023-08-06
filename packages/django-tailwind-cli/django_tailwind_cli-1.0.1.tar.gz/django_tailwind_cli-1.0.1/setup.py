# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['django_tailwind_cli',
 'django_tailwind_cli.management',
 'django_tailwind_cli.management.commands',
 'django_tailwind_cli.templatetags']

package_data = \
{'': ['*'], 'django_tailwind_cli': ['templates/tailwind_cli/tags/*']}

install_requires = \
['certifi>=2022.9.24,<2023.0.0', 'django-click>=2.3.0,<3.0.0', 'django>=3.2']

setup_kwargs = {
    'name': 'django-tailwind-cli',
    'version': '1.0.1',
    'description': 'Django and Tailwind integration based on the prebuilt Tailwind CSS CLI.',
    'long_description': '# django-tailwind-cli\n\n![GitHub Workflow Status](https://img.shields.io/github/workflow/status/oliverandrich/django-tailwind-cli/CI?style=for-the-badge)\n[![PyPI](https://img.shields.io/pypi/v/django-tailwind-cli.svg?style=for-the-badge)](https://pypi.org/project/django-tailwind-cli/)\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge)](https://github.com/psf/black)\n![GitHub](https://img.shields.io/github/license/oliverandrich/django-tailwind-cli?style=for-the-badge)\n\nThis project provides an integration of Tailwind CSS for Django that is based on the precompiled versions of the [Tailwind CSS CLI](https://tailwindcss.com/blog/standalone-cli).\n\nIt is inspired by the implementation of the [Tailwind integration for Phoenix](https://github.com/phoenixframework/tailwind) which completely skips the neccesity of a node installation. So it is a perfect match, if you are a user of [htmx](https://htmx.org) or any other framework that tries to avoid JavaScript coding in your web app. My personal motivation was, that I discovered that I never needed any other plugin besides the official plugins, which are already included in the CLI.\n\n> If you want to use node or you have to use it because of other dependencies, then the package [django-tailwind](https://github.com/timonweb/django-tailwind) by [Tim Kamamin](https://github.com/timonweb) might be a better solution for you.\n\n## Features\n\n- Management Commands...\n  - ...to install the the CLI for your operating system and machine architecture.\n  - ...to start the CLI in watch mode to incrementally compile your style sheet.\n  - ...to create a theme app which includes a basic stylesheet and a tailwind configuration which you can extend.\n  - ...to build the production ready CSS file.\n- A template tag to include the CSS file in your base template.\n- All the official plugins (typography, form, line-clamp, and aspect-ratio) integrated in the CLI are activated in the default configuration.\n\n## Requirements\n\nPython 3.8 or newer with Django >= 3.2.\n\n## Installation\n\n1. Install the package inside your Django project.\n\n    ```shell\n    python -m pip install django-tailwind-cli\n    ```\n\n2. Add `django_tailwind_cli` to `INSTALLED_APPS` in `settings.py`.\n\n    ```python\n    INSTALLED_APPS = [\n        # other Django apps\n        "django_tailwind_cli",\n    ]\n    ```\n\n3. Run the management command to install the cli and initialize the theme app.\n\n    ```shell\n    python manage.py tailwind installcli\n    python manage.py tailwind init\n    ```\n\n    This installs the CLI to `$HOME/.local/bin/` and creates a new app in your project with the name `theme`.\n\n4. Add the new theme app to `INSTALLED_APPS` in `settings.py`.\n\n    ```python\n    INSTALLED_APPS = [\n        # other Django apps\n        "django_tailwind_cli",\n        "theme",\n    ]\n    ```\n\n5. Edit your base template to include Tailwind\'s stylesheet.\n\n    ```html\n    {% load tailwind_cli %}\n   ...\n   <head>\n      ...\n      {% tailwind_css %}\n      ...\n   </head>\n    ```\n\n6. Start the Tailwind CLI in watch mode.\n\n    ```shell\n    python manage.py tailwind startwatcher\n    ```\n\n7. (Optional) Add [django-browser-reload](https://github.com/adamchainz/django-browser-reload) if you enjoy automatic reloading during development.\n\n## Configuration\n\nThe default configuration for this package is.\n\n```python\n{\n    "TAILWIND_VERSION": "3.1.8",\n    "TAILWIND_CLI_PATH": "~/.local/bin/",\n    "TAILWIND_THEME_APP": "theme",\n    "TAILWIND_SRC_CSS": "src/styles.css",\n    "TAILWIND_DIST_CSS": "css/styles.css",\n}\n```\n\n- Set `TAILWIND_VERSION` to the version of Tailwind you want to use.\n- `TAILWIND_CLI_PATH` defines where the CLI is installed. The default makes sense on macOS or Linux. On Windows it might helpful to pick a different path.\n- `TAILWIND_THEME_APP` defines the name of the theme application created by the management command `tailwind init`.\n- `TAILWIND_SRC_CSS` and `TAILWIND_DIST_CSS` defines the internal structure of the theme app. `TAILWIND_DIST_CSS` is a path always relative to the `static` folder of the theme app.\n\n## Management Commands\n\n| Command                 | Description                                                         |\n| ----------------------- | ------------------------------------------------------------------- |\n|\xa0`tailwind installcli`   | Download the CLI version `TAILWIND_VERSION` to `TAILWIND_CLI_PATH`. |\n|\xa0`tailwind init`         | Create a new theme app with the name `TAILWIND_THEME_APP` inside the `settings.BASE_DIR` of your project. |\n|\xa0`tailwind watch`        | Start the CLI in watch and incremental compilation mode.            |\n|\xa0`tailwind build`        | Create a production ready build of the Tailwind stylesheet. You have to run this before calling the `collectstatic` command. |\n\n## Template Tags\n\nThis package provides a single template tag to include the Tailwind CSS. Depending on the value of `settings.DEBUG` it activates preload or not.\n\n```html\n{% load tailwind_cli %}\n...\n<head>\n    ...\n    {% tailwind_css %}\n    ...\n</head>\n```\n\n`DEBUG == False` creates the following output:\n\n```html\n<link rel="preload" href="/static/css/styles.css" as="style">\n<link rel="stylesheet" href="/static/css/styles.css">\n```\n\n`DEBUG == True` creates this output:\n\n```html\n<link rel="stylesheet" href="/static/css/styles.css">\n```\n\n## License\n\nThis software is licensed under [MIT license](https://github.com/oliverandrich/django-tailwind-cli/blob/main/LICENSE). Copyright (c) 2022 Oliver Andrich.\n',
    'author': 'Oliver Andrich',
    'author_email': 'oliver@andrich.me',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/oliverandrich/django-tailwind-cli',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
