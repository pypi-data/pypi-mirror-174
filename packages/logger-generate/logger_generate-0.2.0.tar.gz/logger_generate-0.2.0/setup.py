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
    'version': '0.2.0',
    'description': '開箱即用的logger。 easy to generate logger.',
    'long_description': '# logger_generate\n\n[![Codacy Badge](https://app.codacy.com/project/badge/Grade/26699f09d35542bcb96c9d0164e27a1e)](https://www.codacy.com/gh/we684123/logger_generate/dashboard?utm_source=github.com&utm_medium=referral&utm_content=we684123/logger_generate&utm_campaign=Badge_Grade)\n\n生成 logger 用的，清涼舒爽  \n開箱即用的 logger。\n\nA python package  \neasy to generate logger.\n\n## Install\n\npip\n\n```bash\npip install -U logger-generate\n```\n\npoetry\n\n```bash\npoetry add logger-generate\n```\n\n## Example\n\n```python\nfrom config import base\nfrom logger_generate import generate\n\nlogger = generate()\nlogger.info("引入即用 ( •̀ ω •́ )✧")\n\nlogger_config = {\n    "logging_level": \'DEBUG\',\n    "log_file_path": \'./logs/by_logger_config.log\',\n    "log_format": \'%(asctime)s - %(levelname)s : %(message)s\',\n    "backupCount": 7,\n    "when": \'D\',\n    "encoding": \'utf-8\',\n}\nlogger = generate(logger_config, name=\'from_dict\')\nlogger.info("亦可用程式內 dict 設定")\n\nlogger = generate(base.logger_config(), "from_config_file")\nlogger.info("也以用從檔案引入 config")\n\nlogger = generate(logger_config, name=\'方便生成隨機log名稱\', need_serial=True)\nlogger.info("←後方隨機5字元")\n\nlogger = generate(base.logger_config(), "ex", True)\nlogger.info("示範單純用位置作為輸入手段")\n\nlogger = generate(logging_level=\'DEBUG\',\n                  name=\'use_kwargs\',\n                  log_file_path=\'./logs/use_kwargs.log\')\nlogger.info("現在也可以用 kwargs 設定 logger")\n```\n\n![2022-10-29 22_38_04-logger_generate @ z170_hero](https://user-images.githubusercontent.com/22027801/198837773-27f1a516-c99a-4518-86e9-42ff9c4faab0.png)\n',
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
