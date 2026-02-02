# variable_declaration_checker

> We have migrated to Flake8 as Pylint's performance becomes a bottleneck on larger projects. Since our workflow focuses on file-by-file linting rather than cross-module dependency checks, Flake8 is a better fit. If you still prefer Pylint, use `variable-declaration-checker==0.0.7`.

Installation:

```shell
pip install variable-declaration-checker
```

Usage:

```shell
flake8 --select WVarDec
```
