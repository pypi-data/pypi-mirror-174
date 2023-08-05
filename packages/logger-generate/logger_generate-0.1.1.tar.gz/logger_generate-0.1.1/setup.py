# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['logger_generate']

package_data = \
{'': ['*']}

install_requires = \
['coloredlogs>=15.0.1,<16.0.0']

setup_kwargs = {
    'name': 'logger-generate',
    'version': '0.1.1',
    'description': '開箱即用的logger。 easy to generate logger.',
    'long_description': '# logger_generate\n生成logger用的，清涼舒爽\n\n```python\nfrom config import base\nfrom library.logger_generate import generate\n\nlogger = generate()\nlogger.info("引入即用 ( •̀ ω •́ )✧")\n\nlogger_config = {\n    "logging_level": \'DEBUG\',\n    "log_file_path": \'./logs/by_logger_config.log\',\n    "log_format": \'%(asctime)s - %(levelname)s : %(message)s\',\n    "backupCount": 7,\n    "when": \'D\',\n    "encoding": \'utf-8\',\n}\nlogger = generate(logger_config, name=\'from_dict\')\nlogger.info("亦可用程式內 dict 設定")\n\nlogger = generate(base.logger_config(), "from_config_file")\nlogger.info("也以用從檔案引入 config")\n\nlogger = generate(logger_config, name=\'方便生成隨機log名稱\', need_serial=True)\nlogger.info("←後方隨機5字元")\n\nlogger = generate(base.logger_config(), "ex", True)\nlogger.info("示範單純用位置作為輸入手段")\n```\n![2022-10-02 23_32_45-README md — C__Users_we684123_Dropbox_各類專案_Github_logger_generate — Atom](https://user-images.githubusercontent.com/22027801/193462753-a5456909-28d5-449e-b8dc-5e1648ab87d0.png)\n',
    'author': 'we684123',
    'author_email': 'we684123@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/we684123/logger_generate',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
