# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['super_glass_lsp',
 'super_glass_lsp.lsp',
 'super_glass_lsp.lsp.custom',
 'super_glass_lsp.lsp.custom.features',
 'super_glass_lsp.lsp.custom.tests.e2e',
 'super_glass_lsp.lsp.custom.tests.e2e.configs',
 'super_glass_lsp.lsp.custom.tests.units']

package_data = \
{'': ['*'],
 'super_glass_lsp.lsp.custom.tests.e2e.configs': ['workspace/.gitignore']}

install_requires = \
['mergedeep>=1.3.4,<2.0.0',
 'parse>=1.19.0,<2.0.0',
 'pygls>=0.12.2,<0.13.0',
 'pyyaml>=6.0,<7.0',
 'single-source>=0.3.0,<0.4.0']

entry_points = \
{'console_scripts': ['super-glass-lsp = super_glass_lsp.main:main']}

setup_kwargs = {
    'name': 'super-glass-lsp',
    'version': '0.5.0',
    'description': 'Generic LSP to parse the output of CLI tools, linters, formatters, etc',
    'long_description': '_🚧 WIP: you\'re very welcome to try this, but I\'m breaking a lot at the moment (October 16th)_\n\n# Super Glass\n## Generic LSP Server and/or Pygls Starting Template\n\n<img src="logo.png" align="left" />\n\nThis project has 2 goals.\n\n  1. A generic LSP server that parses CLI tools, or indeed any program that outputs to STDOUT, such as  linters, formatters, style checkers, etc and converts their output to LSP-compatible behaviour.\n  2. An easily-forkable template to start your own custom LSP server using [Pygls](https://github.com/openlawlibrary/pygls).\n\nBecause the heavy-lifting of this language server is done by external tooling (think `pylint`, `jq`, `markdownlint`, etc), there is minimal implementation-specific code in this repo. That is to say that the majority of the code here is applicable to any language server built with [Pygls](https://github.com/openlawlibrary/pygls). Or at the very least, it demonstrates a reasonable starting point. Deleting the `super_glass_lsp/lsp/custom` folder should leave the codebase as close as possible to the minimum starting point for your own custom language server. Then you will also want to rename occurrences of `[C|c]ustom` to your own language server\'s name.\n\n## Installation\n\n`pip install super-glass-lsp`\n\n## Usage\n\n### Quickstart\nOnce you\'ve installed the language server and [set it up in your editor](https://github.com/tombh/super-glass#editor-setups), it should be as easy as this to add new features (this is YAML, but your editor likely has its own config format):\n```yaml\n# This is jsut an ID, so can be anything. Internally it\'s important so that you can\n# override existing configs (either the bundled defaults, or configs you have\n# created elsewhere): all configs with the same ID are automaticallly merged. \nfuzzy_similar_words_completion:\n\n  # This is the part of the language server to which the `command` will apply.\n  # The other currently supported features are: `diagnostic`.\n  lsp_feature: completion\n  \n  # This is the external command which will be triggered and parsed for every\n  # invocation of the feature. In the case of completions, editors will generally\n  # trigger it for _every_ character change, or even every key press. So be\n  # careful not to make this too expensive.\n  #\n  # Default behaviour is to pipe the entire contents of the file into the command.\n  # This can be overriden with `piped: false`. In which case you will likely want\n  # to manually do something with the file. You can access its path with the `{file}`\n  # token. Eg; `command: "cat {file} | tr ..."`.\n  #\n  # This particular command first breaks up the file into a list of words, which are\n  # then piped into a fuzzy finder, which then queries the list with the particular\n  # word currently under your cursor in the editor. Finally the results of the fuzzy\n  # search are deduplicated (with `uniq`).\n  #\n  # The command is run in a shell, so all the tools from your own machine are available.\n  command: "tr -cs \'[:alnum:]\' \'\\n\' | fzf --filter=\'{word}\' | uniq"\n```\n\n### Configuration\n\nThe server comes with a lot of [defaults](super_glass_lsp/config.default.yaml). To enable a particular tool simple provide the `enabled: true` field for that tool. For example:\n```yaml\n# This is YAML, but should be whatever format your editor\'s config is\ninitialization_options:\n  configs:\n    jqlint:\n      enabled: true\n```\n\nTODO:\n* [ ] Explain all the fields and tokens for each LSP feature\n* [ ] Remember to describe the format array lines priorities\n\n## Editor Setups\n\nBecause this is a generic language server, the filetype/language that the server applies to varies depending on the config you\'ve setup. It would be a bad idea for a generic language server to tell an editor that it wants to connect with every possible filetype/language (although this can be enabled on a per tool basis with the `language_ids: ["*"]` setting). Instead, it is better that you manually inform your editor which filetypes/languages this generic server should be enabled for. How that is done is unique to each editor\'s config, I\'ve tried to include examples for each one.\n\n<details>\n<summary>Neovim Lua (vanilla Neovim without `lspconfig`)</summary>\n\n  Since this project is very beta, we\'re not yet submitting this language server to the LSP Config plugin (the defacto way to add new language servers). Therefore, for now, we have to use Neovim\'s vanilla LSP setup (which has actually simplified a lot recently).\n\n  ```lua\n  vim.api.nvim_create_autocmd({ "BufEnter" }, {\n    -- NB: You must remember to manually put the file extension pattern matchers for each LSP filetype\n    pattern = { "*" },\n    callback = function()\n      vim.lsp.start({\n        name = "super-glass",\n        cmd = { "super-glass-lsp" },\n        root_dir = vim.fs.dirname(vim.fs.find({ ".git" }, { upward = true })[1]),\n        init_options = {\n          configs = {\n            fuzzy_buffer_tokens = {\n              lsp_feature = "completion",\n              command = "tr -cs \'[:alnum:]\' \'\\n\' | fzf --filter=\'{word}\' | uniq",\n            },\n          }\n        },\n      })\n    end,\n  })\n  ```\n</details>\n\n<details>\n<summary>Vim (`vim-lsp`)</summary>\n\n  ```vim\n  augroup LspSuperGlass\n  au!\n  autocmd User lsp_setup call lsp#register_server({\n      \\ \'name\': \'super-glass\',\n      \\ \'cmd\': {server_info->[\'super-glass-lsp\', \'--logfile\', \'path/to-logfile\']},\n      \\ \'allowlist\': [\'vim\', \'eruby\', \'markdown\', \'yaml\'],\n      \\ \'initialization_options\': { "configs":\n      \\   { "fuzzy_buffer_tokens": {\n      \\       "lsp_feature": "completion",\n      \\       "command": "tr -cs \'[:alnum:]\' \'\\n\' | fzf --filter=\'{word}\' | uniq",\n      \\     }\n      \\   }\n      \\ }})\n  augroup END\n  ```\n</details>\n\n<details>\n<summary>Neovim (`lspconfig`) TBC</summary>\n\n  Once we\'re stable, we\'ll submit ourselves for inclusion.\n</details>\n\n<details>\n<summary>Emacs (`lsp-mode`)</summary>\n\n\n  ```\n  (make-lsp-client :new-connection\n  (lsp-stdio-connection\n    `(,(executable-find "super-glass-lsp") "--logfile" "path/to/logs"))\n    :activation-fn (lsp-activate-on "json")\n    :initialization-options ; TODO: I\'m not an Emacs user, how do we provide these options?\n    :server-id \'super-glass-lsp\')))\n  ```\n</details>\n\n<details>\n<summary>Emacs (`eglot`) TBC</summary>\n  \n  Once we\'re stable, we\'ll submit ourselves for inclusion.\n</details>\n\n<details>\n<summary>VSCode TBC</summary>\n  \n  Can we copy EFM\'s VSCode extension?\n  https://github.com/Matts966/efm-langserver-vscode\n</details>\n\n\n## Testing\n\nUses [@alcarney](https://github.com/alcarney)\'s [pytest-lsp module](https://github.com/alcarney/lsp-devtools/tree/develop/lib/pytest-lsp) for end-to-end testing.\n\n`poetry run python -m pytest`\n\n## Acknowledgements\n\nThis projects takes a lot of inspiration from [@alcarney](https://github.com/alcarney)\'s fantastic Sphinx/RST LSP server [Esbonio](https://github.com/swyddfa/esbonio). \n\nLogo is from [a sticker I found on Amazon](https://www.amazon.com/-/es/Superman-S-Adhesivo-reflectante-plateado/dp/B00PEZKHV8), obviously want a proper logo before I publish.\n\n## Other generic LSP servers\n\n* https://github.com/iamcco/diagnostic-languageserver\n* https://github.com/mattn/efm-langserver\n* https://github.com/jose-elias-alvarez/null-ls.nvim (Neovim only)\n',
    'author': 'Thomas Buckley-Houston',
    'author_email': 'tom@tombh.co.uk',
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
