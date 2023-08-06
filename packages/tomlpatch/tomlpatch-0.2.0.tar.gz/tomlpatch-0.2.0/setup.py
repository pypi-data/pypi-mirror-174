# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tomlpatch']

package_data = \
{'': ['*']}

install_requires = \
['dotty-dict>=1.3.1,<2.0.0', 'tomli-w>=1.0.0,<2.0.0', 'tomli>=2.0.1,<3.0.0']

entry_points = \
{'console_scripts': ['tomlpatch = tomlpatch.main:main']}

setup_kwargs = {
    'name': 'tomlpatch',
    'version': '0.2.0',
    'description': '',
    'long_description': '# tomlpatch\nDo you want to patch your toml file structurally like modifying a nested python dictionary? This is a tool for you.\n\n# Description\nSometimes, you want to edit/patch a toml file, but you don\'t want to use the [diff](https://en.wikipedia.org/wiki/Patch_(computing)#Source_code_patches) between two source files to patch the toml file since it may introduce conflicts that requires human intervention to resolve.\nFor example, `Cargo.toml` is used by Rust projects, and this tool can be used to patch the `Cargo.toml` file with an external JSON file that contains the structural patch information so that you don\'t need to manually resolve the `Cargo.toml` file.\n\n# Installation\n```\npip install tomlpatch\n```\n\n# Usage\n```\ntomlpatch original_toml_file patch_json_file\n```\n\n# Example\nSuppose you have a `Cargo.toml` file like this:\n```toml\n[package]\nname = "my_package"\nversion = "0.0.1"\n\nliberssl = { version = "0.10.42", default-features = false, features=["vendered"] }\nsources = ["s1", "s2"]\ntargets = ["t1", "t2", "t3"]\n```\n\nAnd you want to patch the `Cargo.toml` file with a JSON file like this:\n```json\n{\n  "patch": {\n    "package.version": "0.0.2",\n    "package.liberssl.features": null\n  },\n  "extend": {\n    "package.sources": ["s4", "s5"]\n  },\n  "remove": {\n    "package.targets": ["t2"]\n  }\n}\n```\n\nThen you can use the following command to patch the `Cargo.toml` file:\n```\ntomlpatch Cargo.toml patch.json\n```\n\nAfter the patch, the `Cargo.toml` file will be like this:\n```toml\n[package]\nname = "my_package"\nversion = "0.0.2"\nsources = [\n    "s1",\n    "s2",\n    "s4",\n    "s5",\n]\ntargets = [\n    "t1",\n    "t3",\n]\n\n[package.liberssl]\nversion = "0.10.42"\ndefault-features = false\n```\n\n# TODO\n* Switch to [tomkit](https://github.com/sdispater/tomlkit) for style preserving patching',
    'author': 'Yue Ni',
    'author_email': 'niyue.com@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
