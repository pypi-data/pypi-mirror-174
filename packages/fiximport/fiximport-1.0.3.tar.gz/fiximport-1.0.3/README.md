# fiximport

Fixes `ModuleNotFoundError` exceptions from [absolute imports](https://realpython.com/absolute-vs-relative-python-imports/) by automatically adding the entire project to `sys.path`.

This is similar to what PyCharm does when a directory is marked as `Sources Root`.

# Install

```
pip install fiximport
```

# Use

```python
import fiximport
import mymodule.userutils
import mymodule.config

[...]
```

- `fiximport` must come before the absolute imports.
- `fiximport` only needs to be added to files intended to be invoked by the CLI.  
   Eg, `python cool_script.py`.
- `fiximport` is safe and idempotent. You could add it to every file, if you wished.

# Sample Project

```
📁 coolproject
    📁 src
        📄 weather.py
    📁 scripts
        📄 printweather.py
```

## Before

```python
from src.weather import get_weather

print(f"The weather today is {get_weather('Bellingham, WA')}")
```

```
$ python printweather.py
Traceback (most recent call last):
  File "printweather.py", line 1, in <module>
    from src.weather import get_weather
ModuleNotFoundError: No module named 'src'
```

## After

```python
import fiximport
from src.weather import get_weather

print(f"The weather today is {get_weather('Bellingham, WA')}")
```

```
$ python printweather.py
The weather today is 67°F
```

# Implementation Details

1. `fiximport` identifies the project root by iterating up, until the first "root type files" are found.
2. If the project root cannot be found heuristically, it defaults to one folder above the python file that called `import fiximport`.
3. After the root is heuristically found, all folders with a `python` file inside are added to `sys.path`. This enables absolute imports to "just work".

This is not a robust permanent solution to python's import system, but it should cover simple projects nicely.

# Troubleshooting

- Avoid naming collisions within your project. If there are two folders named `utils`, eg `foo1/utils` and `foo2/utils`, add the prefix: `from foo2.utils import check_file`.
- Avoid naming collisions with common libraries. Eg `math`, `statistics`, `tempfile`, etc.
