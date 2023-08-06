# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cfn_lsp_extra',
 'cfn_lsp_extra.completions',
 'cfn_lsp_extra.decode',
 'cfn_lsp_extra.resources',
 'cfn_lsp_extra.scrape']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'aiohttp[speedups]>=3.8,<4.0',
 'cfn-lint>=0.61,<0.62',
 'click>=8.1.3,<9.0.0',
 'platformdirs>=2.5,<3.0',
 'pydantic>=1.8,<2.0',
 'pygls>=0.11,<0.12',
 'tqdm>=4.64,<5.0',
 'types-PyYAML>=6.0,<7.0']

entry_points = \
{'console_scripts': ['cfn-lsp-extra = cfn_lsp_extra.__main__:main']}

setup_kwargs = {
    'name': 'cfn-lsp-extra',
    'version': '0.4.2',
    'description': 'Cfn Lsp Extra',
    'long_description': '# Cfn Lsp Extra\n\n![Python Version](https://img.shields.io/pypi/pyversions/cfn-lsp-extra) [![PyPI](https://img.shields.io/pypi/v/cfn-lsp-extra)](CHANGELOG.md) [![codecov](https://codecov.io/gh/LaurenceWarne/cfn-lsp-extra/branch/master/graph/badge.svg?token=48ixiDIBpq)](https://codecov.io/gh/LaurenceWarne/cfn-lsp-extra)\n\nAn experimental cloudformation lsp server (with support for SAM templates) built on top of [cfn-lint](https://github.com/aws-cloudformation/cfn-lint) aiming to provide hovering, completion, etc.  YAML and JSON are supported, though YAML has more features currently implemented (for example snippets) and will give a better experience.  Trust me.\n\nhttps://user-images.githubusercontent.com/17688577/176939586-df1d9ed8-5ec6-46d5-9f26-7222644047bd.mp4\n\n## Features\n\n| Method                            | Status                                                                                                               |\n|-----------------------------------|----------------------------------------------------------------------------------------------------------------------|\n| `textDocument/hover`              | Done for resources, resource properties, subproperties and `!Ref`s. *TODO* `!GetAtt`s, intrinsic functions.          |\n| `textDocument/completion`         | Done for resources, resource properties, subproperties, refs, !GetAtts and intrinsic functions. *TODO* `Fn::GetAtt`. |\n| `textDocument/definition`         | Done for `!Ref`s.  *TODO* mappings.                                                                                  |\n| `textDocument/publishDiagnostics` | Done through `cfnlint`.                                                                                              |\n\n## Installation\n\nFirst install the executable, [`pipx`](https://pypa.github.io/pipx/) is recommended, but you can use `pip` instead if you like to live dangerously:\n\n```bash\npipx install cfn-lsp-extra\n```\n\nOr get the bleeding edge from source:\n\n```bash\npipx install git+https://github.com/laurencewarne/cfn-lsp-extra.git@$(git ls-remote git@github.com:laurencewarne/cfn-lsp-extra.git | head -1 | cut -f1)\n```\n\nUpdating:\n\n```bash\npipx upgrade cfn-lsp-extra\n```\n\n### Emacs\n\nInstall the [lsp-cfn.el](https://github.com/LaurenceWarne/lsp-cfn.el) package.\n\n### Neovim\n\nMake sure you\'re running at least `0.8`, then add the following in `~/.config/nvim/filetype.lua`:\n\n```lua\nvim.filetype.add {\n  pattern = {\n    [\'.*\'] = {\n      priority = math.huge,\n      function(path, bufnr)\n        local line1 = vim.filetype.getlines(bufnr, 1)\n        local line2 = vim.filetype.getlines(bufnr, 2)\n        if vim.filetype.matchregex(line1, [[^AWSTemplateFormatVersion]] ) then\n          return \'yaml.cloudformation\'\n        elseif vim.filetype.matchregex(line1, [[["\']AWSTemplateFormatVersion]] ) or\n\t\t   vim.filetype.matchregex(line2, [[["\']AWSTemplateFormatVersion]] ) then\n          return \'json.cloudformation\'\n        end\n      end,\n    },\n  },\n}\n```\n\nThen you can use [LanguageClient-neovim](https://github.com/autozimu/LanguageClient-neovim) to start the server on those file types:\n\n```vim\nlet g:LanguageClient_serverCommands = {\n    \\ \'yaml.cloudformation\': [\'~/.local/bin/cfn-lsp-extra\'],\n    \\ \'json.cloudformation\': [\'~/.local/bin/cfn-lsp-extra\']\n    \\ }\n```\n\n\nPatches documenting integration for other editors are very welcome!\n\n## Alternatives\n\n### [vscode-cfn-lint](https://github.com/aws-cloudformation/cfn-lint-visual-studio-code)\n\n### [cfn-lint](https://github.com/aws-cloudformation/cfn-lint)\n\nNote this is used by `cfn-lsp-extra` under the hood to generate [diagnostics](https://microsoft.github.io/language-server-protocol/specifications/lsp/3.17/specification/#diagnostic).  One difference with `cfn-lsp-extra` is that diagnostics will be refreshed every time you make a change to the document, in other words you don\'t need to save the file.\n\n### [yamlls](https://github.com/redhat-developer/yaml-language-server)\n\nYou can use `yamlls` in conjunction with the Cloudformation schema at https://www.schemastore.org/json/ as an alternative.  For Emacs, `lsp-mode` can install `yamlls` for you, from there you could do something like:\n\n```elisp\n(defun my-yamlls-cloudformation-setup ()\n  ;; There\'s also one for serverless\n  (lsp-yaml-set-buffer-schema "https://raw.githubusercontent.com/awslabs/goformation/master/schema/cloudformation.schema.json")\n  (setq-local\n   lsp-yaml-custom-tags\n   ["!And"\n    "!Base64"\n    "!Cidr"\n    "!Equals"\n    "!FindInMap sequence"\n    "!GetAZs"\n    "!GetAtt"\n    "!If"\n    "!ImportValue"\n    "!Join sequence"\n    "!Not"\n    "!Or"\n    "!Ref Scalar"\n    "!Ref"\n    "!Select"\n    "!Split"\n    "!Sub"\n    "!fn"]))\n\n;; Using the mode defined by https://www.emacswiki.org/emacs/CfnLint\n(add-hook \'cfn-yaml-mode-hook #\'my-yamlls-cloudformation-setup)\n(add-hook \'cfn-yaml-mode-hook #\'lsp-deferred)\n```\n\nThis will give you completions (and some support for value completions?), though no hover documentation.\n',
    'author': 'Laurence Warne',
    'author_email': 'laurencewarne@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/laurencewarne/cfn-lsp-extra',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
