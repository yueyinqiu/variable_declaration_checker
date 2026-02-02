# variable_declaration_checker

> We have migrated to Flake8 as Pylint's performance becomes a bottleneck on larger projects. Since our workflow focuses on file-by-file linting rather than cross-module dependency checks, Flake8 is a better fit. If you still prefer Pylint, use `variable-declaration-checker==0.0.7`.

## Installation and Basic Usage

```shell
pip install variable-declaration-checker
flake8 --select WVarDec
```

## Issue and PR GuideLine

We want this plugin to work with Visual Studio Code. Therefore, all behaviors that conflict with Pylance need to be eliminated. For example, if you find that not adding type annotations causes warnings from this plugin, while adding type annotations causes errors in Pylance, please report it to us.

However, `ast` does not provide complete type information. This necessitates expanding the scope of some features. For example, we can detect if a type has a base class called `"Enum"` and thus ignore variable definitions within it. However, it's difficult to detect if this `Enum` is actually from the system library (even parsing `imports` doesn't achieve this, as creating a module with the same name is possible). Therefore, it will also affect a custom type called `"Enum"`.