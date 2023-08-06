# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['random_img_api',
 'random_img_api.src',
 'random_img_api.src.config',
 'random_img_api.src.get_img']

package_data = \
{'': ['*']}

install_requires = \
['Pillow>=9.3.0,<10.0.0',
 'fastapi>=0.85.1,<0.86.0',
 'gunicorn>=20.1.0,<21.0.0',
 'pydenticon>=0.3.1,<0.4.0',
 'requests>=2.28.1,<3.0.0',
 'rich-click>=1.5.2,<2.0.0',
 'rich>=12.6.0,<13.0.0',
 'uvicorn>=0.19.0,<0.20.0']

entry_points = \
{'console_scripts': ['img_api = random_img_api.img_api_cli:cli']}

setup_kwargs = {
    'name': 'random-img-api',
    'version': '1.1.2',
    'description': 'Random Image API',
    'long_description': '# Random_Img_API\n\nA Random Img API build with FastAPI, contain post img and auto download\n\nProject for learning.\n\n## Available parameters\n\n- size: `[positive integer | ?]x[positive integer | ?]`\n    - example: `100x100`, `100x?`, `?x100`\n    - default: `?x?`\n- type: `[acg | wallpaper | avatar]`\n    - example: `acg`, `wallpaper`, `avatar`\n    - default: `None`\n\n## Setup environment\n\n```shell\npip install random_img_api\n```\n\n## Run server\n\n```shell\nimg_api run <options>\n```\n\n### Options\n- `--port` `INTEGER`\n  - Port to run on\n  - default: `8045`\n- `--threads` `INTEGER`\n  - Number of threads to run\n  - default: `2`\n- `--workers` `INTEGER`\n  - Number of workers to run\n  - default: `cpu_count() * 2 + 1`\n- `--help`\n  - Show help message and exit\n\n## Image download [Not complete yet]\n\n```shell\nimg_api get <options>\n```\n\n### Options\n- `--type` / `-t` `TEXT`\n  - the type of image to download\n  - default: `acg`\n  - choices: `acg`, `wallpaper`, `avatar`\n- `--num` / `-n`\n  - the number of images to download, 0 for unlimited\n  - default: `0`\n- `--help`\n  - Show the help message and exit\n\n\n## Config\n\n### Change Config\n\n```shell\nimg_api config <option> <CONFIG_VALUE>\n```\n\nOptions:\n- `--setup` setup config file\n\nArgument:\n- `CONFIG_VALUE` allow argument like `img_path=img` or `database_name`\n\n### Database\n- `database_name`: Name of database file\n  - stored in `config.json`\n  - default: `img_info.sqlite3`\n\n### Download\n- `img_path`: Path of img folder\n  - stored in `config.json`\n  - default: `./img`\n\n### Log\n- `log_level`: Level of log\n  - stored in `config.json`\n  - default: `INFO`\n  - choices: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`\n\n## Todo\n- [ ] Add more available parameters\n- [ ] Modulize the code\n  - [ ] allow user to config\n    - [x] read and write config file\n    - [x] change download path\n    - [ ] change download source\n    - [x] change database path\n    - [x] change config using command line\n  - [x] change structure of image download\n- [x] make a download progress bar with rich\n- [ ] use ai to generate images\n- [x] add colored log\n- [x] add more comments\n- [ ] add rsa protection or protection according to ip\n- [ ] change return url so that people will be able to review what they just look at\n- [x] using setuptools to manage dependencies and build a package\n- [x] finish download and generate image function\n  - [x] download acg\n  - [x] download wallpaper\n  - [x] generate avatar\n- [ ] format commit message',
    'author': 'BrandenXia',
    'author_email': 'xxtbranden@outlook.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/BrandenXia/Random_Img_API',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
