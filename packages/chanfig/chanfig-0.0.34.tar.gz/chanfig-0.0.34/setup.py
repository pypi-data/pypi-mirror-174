# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chanfig']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'chanfig',
    'version': '0.0.34',
    'description': 'Easier Configuration',
    'long_description': '# CHANfiG\n\nRead this in other language: [English](README.md)\n\n在其他语言中阅读本文：[简体中文](README.cn.md)\n\n## Introduction\n\nCHANfiG aims to make your configuration easier.\n\nThere are tons of configurable parameters in training a Machine Learning model.\nTo configure all these parameters, researchers usually need to write gigantic config files, sometimes even thousands of lines.\nMost of the configs are just replicates of the default arguments of certain functions, resulting in many unnecessary declarations.\nIt is also very hard to alter the configurations.\nOne needs to navigate and open the right configuration file, make changes, save and exit.\nThese had wasted an incountable[^incountable] amount of precious time ~~and is no doubt a crime~~.\nUsing `argparse` could relieve the burdens to some extent, however, it takes a lot of work to make it compatible with existing config files, and its lack of nesting limits its potential.\nCHANfiG would like to make a change.\n\nYou just run your experiment with arguments, and leave everything else to CHANfiG.\n\nCHANfiG is highly inspired by [YACS](https://github.com/rbgirshick/yacs).\nDifferent to the paradigm of YACS(\n`your code + a YACS config for experiment E (+ external dependencies + hardware + other nuisance terms ...) = reproducible experiment E`),\nThe paradigm of CHANfiG is:\n\n`your code + command line arguments (+ optional CHANfiG config + external dependencies + hardware + other nuisance terms ...) = reproducible experiment E (+ optional CHANfiG config for experiment E)`\n\n## Usage\n\nCHANfiG has great backward compatibility with previous configs.\n\nNo matter your old config is json or yaml, you could directly read from them.\n\nAnd if you are using yacs, just replace `CfgNode` with `Config` and enjoy all the additional benefits that CHANfiG provides.\n\n```python\nfrom chanfig import Config\n\n\nclass Model:\n    def __init__(self, encoder, dropout=0.1, activation=\'ReLU\'):\n        self.encoder = Encoder(**encoder)\n        self.dropout = Dropout(dropout)\n        self.activation = getattr(Activation, activation)\n\ndef main(config):\n    model = Model(**config.model)\n    optimizer = Optimizer(**config.optimizer)\n    scheduler = Scheduler(**config.scheduler)\n    dataset = Dataset(**config.dataset)\n    dataloader = Dataloader(**config.dataloader)\n\n\nclass TestConfig(Config):\n    def __init__(self):\n        super().__init__()\n        self.data.batch_size = 64\n        self.model.encoder.num_layers = 6\n        self.model.decoder.num_layers = 6\n        self.activation = "GELU"\n        self.optim.lr = 1e-3\n\n\nif __name__ == \'__main__\':\n    # config = Config.read(\'config.yaml\')  # in case you want to read from a yaml\n    # config = Config.read(\'config.json\')  # in case you want to read from a json\n    # existing_configs = {\'data.batch_size\': 64, \'model.encoder.num_layers\': 8}\n    # config = Config(**existing_configs)  # in case you have some config in dict to load\n    config = TestConfig()\n    config = config.parse()\n    # config.merge(\'dataset.yaml\')  # in case you want to merge a yaml\n    # config.merge(\'dataset.json\')  # in case you want to merge a json\n    # note that the value of merge will surpass current values\n    config.model.decoder.num_layers = 8\n    config.freeze()\n    print(config)\n    # main(config)\n    # config.yaml(\'config.yaml\')  # in case you want to save a yaml\n    # config.json(\'config.json\')  # in case you want to save a json\n```\n\nAll you needs to do is just run a line:\n\n```shell\npython main.py --model.encoder.num_layers 8\n```\n\nYou could also load a default configure file and make changes based on it:\n\n```shell\npython main.py --config meow.yaml --model.encoder.num_layers 8\n```\n\nIf you have made it dump current configurations, this should be in the written file:\n\n```yaml\ndata:\n  batch_size: 64\nmodel:\n  encoder:\n    num_layers: 8\n  decoder:\n    num_layers: 8\n  activation: GELU\n```\n\n```json\n{\n  "data": {\n    "batch_size": 64\n  },\n  "model": {\n    "encoder": {\n      "num_layers": 8\n    },\n    "decoder": {\n      "num_layers": 8\n    },\n  "activation": "GELU"\n  }\n}\n```\n\nDefine the default arguments in function, put alteration in CLI, and leave the rest to CHANfiG.\n\n## Installation\n\nInstall most recent stable version on pypi:\n\n```shell\npip install chanfig\n```\n\nInstall the latest version from source:\n\n```shell\npip install git+https://github.com/ZhiyuanChen/chanfig\n```\n\n\n\nIt works the way it should have worked.\n\n[^incountable]: fun fact: time is always incountable.\n',
    'author': 'Zhiyuan Chen',
    'author_email': 'this@zyc.ai',
    'maintainer': 'Zhiyuan Chen',
    'maintainer_email': 'this@zyc.ai',
    'url': 'https://chanfig.danling.org',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3,<4',
}


setup(**setup_kwargs)
