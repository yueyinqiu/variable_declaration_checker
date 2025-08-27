```python
# src/local_test/a.py
x = 1
```

```shell
pylint --load-plugins=variable_declaration_checker src/local_test/a.py
```

---

```python
import astroid
import variable_declaration_checker
import pylint.lint

module = astroid.parse(
    """
    x = 1
    """)
print(module)

a = astroid.extract_node(
    """
    x = 1

    class A: #@
        pass
    """)
print(a)

checker = variable_declaration_checker.VariableDeclarationChecker(pylint.lint.PyLinter())
checker._check(module)
```