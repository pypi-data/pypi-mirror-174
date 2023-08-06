# SmartParams

SmartParams is a lightweight Python framework that simplifies configuration of research projects.
Creates an abstraction that warp configurable classes, functions and extracts from them the
necessary parameters into a configuration file and then injects them initialization. SmartParams can
be easily integrated into existing projects, even if they are very complex. Takes care of loading
the configuration file from path given in code or via command line.

# What is Smart class

_Smart_ class is like as _partial_ from _functools_.
_Smart_ object called will instantiate class called with the args and kwargs. If more arguments are
supplied to the call, they are merged with initial keyword arguments.

```python
from smartparams import Smart


class SomeClass:
    def __init__(self, a: str, b: int) -> None:
        self.a = a
        self.b = b


some_class = Smart(SomeClass, a='a')
some_object = some_class(b=1)
```

### Key features:

* Wraps class to be partially or fully configurable.
* Allows setting attributes that depend on other objects.
* Creates a configuration template file based on class dependencies in the program.
* Loads configuration from json and yaml files.
* Checks unset parameters.
* Checks the type of parameters.
* Automatically convert parameters to proper types.
* Allows overriding configuration from command line.

# Installation

Install via [PyPI](https://pypi.org/project/SmartParams/) &nbsp;`pip install SmartParams`.

SmartParams requires Python 3.10 or newer.

# Example

# Documentation

* Create
* Access and manipulation
* Register

## Create

#### From keyword arguments

```python
Smart(
    a=1,
    b={'x': 2, 'y': '3'},
    c=[4, False, {'m': 5}],
)
```

#### Form dict

```python
Smart({
    'a': 1,
    'b': {'x': 2, 'y': '3'},
    'c': [4, False, {'m': 5}],
})
```

SmartParams supports only string as dictionary key type.

#### From list

```python
Smart([
    ('a', 1),
    ('b', {'x': 2, 'y': '3'}),
    ('c', [4, False, {'m': 5}]),
])
```

#### From dot list

```python
Smart([
    'a=1',
    'b.x=2',
    'b.y="3"',
    'c=[4, false, {"m": 5}]',
])
```

#### From command line arguments

```python
Smart.from_cli()
```

#### From file ('yaml', 'json')

```python
Smart.load('path/to/params.yaml')
```

#### From python object

```python
from dataclasses import dataclass, field


@dataclass
class Object:
    a: int = 1
    b: dict[str, int] = field(default_factory=lambda x: {'x': 2, 'y': '3'})
    c: tuple[int, bool, dict[str, int]] = (4, False, {'m': 5})


Smart(Object).schema()
```

## Access and manipulation

#### Configuration file - params.yaml:

```yaml
data:
  dataset: ???
  batch_size: 32

model:
  layers:
    - 256
    - 128
  optimizer:
    class: Adam
    lr: 2E-5
```

```python
>>> from smartparams import Smart
>>> params = Smart.load('params.yaml')
```

#### Access

```python
# dictionary style access
>>> params['data']['batch_size']
32

# dictionary dot-style access
>>> params['data.batch_size']
32

# object style access
>>> params.data.batch_size
32

# default values
>>> params.get('missing_key', default='a default value')
'a default value'

# access to content
>>> params.keys()  # see also: .values(), .items()
dict_keys(['data', 'model'])

# access to nested content
>>> params.keys(flatten=True)  # see also: .values(flatten=True), .items(flatten=True)
dict_keys(['data.dataset', 'data.batch_size', 'model.layers', 'model.optimizer.class', 'model.optimizer.lr'])
```

#### Manipulation

```python
# Changing existing keys
>>> params.data.batch_size = 64

# Adding new keys
>>> params['model.criterion.class'] = 'CrossEntropyLoss'

# Update from existing dict, list, Smart object
>>> params.update({
...     'data.batch_size': 128,  # merges to existing `data` dictionary
...     'model': {'layers': [128, 64]}  # overrides entire `model` dictionary
... })

# Removing keys
>>> del params['data.batch_size']
>>> params.pop('data.batch_size')
32

# Coping deeply all params
>>> params.copy()
Smart({'data': Smart({'dataset': '???', 'batch_size': 32}), 'model': Smart({'layers': [256, 128], 'optimizer': Smart({'class': 'Adam', 'lr': '2E-5'})})})

# Removing all params
>>> params.clear()
Smart({})
```

#### Merging configurations

```python
data_params = Smart.load('path/to/data.yaml')
model_params = Smart.load('path/to/model.yaml')
cli_params = Smart.from_cli()
params = Smart.merge(data_params, model_params, cli_params)
```

## Smart instantiating

## Partial utilities

#### Type

```python
Smart.type -> Type
```

Returns class or function's return type.

#### Class

```python
Smart.cls -> Callable
```

Returns class or function.

#### Params

```python
Smart.params -> Smart
```

Returns the parameters that will be provided when creating an instance of the class.

## Utility functions

#### Explode

```python
Smart.explode(
    self,
    *keys: str,
) -> Iterable[Smart]:
```

Creates combinations of params from lists assigned to givens keys.

```python
params = Smart(
    a='constant',
    b=[1, 2, 3],
    c=('x', 'y'),
)

for combination in params.explode('b', 'c'):
    print(combination)

# Smart({'a': 'constant', 'b': 1, 'c': 'x'})
# Smart({'a': 'constant', 'b': 1, 'c': 'y'})
# Smart({'a': 'constant', 'b': 2, 'c': 'x'})
# Smart({'a': 'constant', 'b': 2, 'c': 'y'})
# Smart({'a': 'constant', 'b': 3, 'c': 'x'})
# Smart({'a': 'constant', 'b': 3, 'c': 'y'})
```

#### Make directory

Creates directory in given path.

#### Save

Saves dictionary to given path.

#### To dict

Returns simple dictionary.

#### To yaml

Returns string representation of dictionary in yaml format.

#### To json

Returns string representation of dictionary in json format.

## Register

Register is used to collect classes and functions for import them by name or path.

```python
from dataclasses import dataclass
from smartparams import Smart


@Smart.register(name='my_some_class')
@dataclass
class SomeClass:
    a: str
    b: int


some_class = Smart('my_some_class', a='a')
some_object = some_class(b=1)
```

#### How to register?

As a decorator

```python
@Smart.register  # default name is 'SomeClass' what is determined based on class
class SomeClass:
  a: str
  b: int
```

As function

```python
from module import SomeClass

Smart.register(SomeClass)
```

Inplace

```python
params = Smart.load('some_class_params.yaml')
some_class = params.with_class(SomeClass)(b=1)
```

```python
params = Smart.load('some_class_params.yaml')
some_class = params[SomeClass](b=1)  # shorter equivalent for `Smart.with_class`
```

#### Auto register

Automatic registration is based on Python type annotation. All classes in union are registered,
including their subclasses. This means that all children of certain class are registered and can be
accessed by name or path.

#### Global vs local register

Smart class has global instance of register. For each instance of Smart is created deep copy of this
register. Registering new objects to instance Smart do not provide changes in global register. Also
registering classes to global register do not provide changes in already instantiated Smart objects.

#### Autodiscover

```python
SmartRegister.autodiscover(
    path: str | Path = '.',
    include: str = '',
    exclude: str = '',
) -> list[Path]
```

To register classes by decorator, all modules must be imported. The same goes for discovering
subclasses of a class. To do this, either import all modules manually or use
the `Smart.register.autodiscover` function.

#### Import class

Use it to determine import class by path (or name if registered).

#### Get class path

Use it to determine class path. You can check if class path is registered by
using `Smart.register.has_path`. You can get class by path by
using `Smart.register.get_class_by_path`.

#### Get class name

Use it to determine class name. You can check if class name is registered by
using `Smart.register.has_name`. You can get class by name by
using `Smart.register.get_class_by_name`.

#### Copy register

Created deep copy of SmartRegister object.

#### Clear register

Removed all registered objects and added resolvers.

#### Instantiate class or function

Creates instance of given class.

#### Convert argument type

Converts arguments to expected type.

#### Simplify object

Convert an object to a primitive type.

#### Smartify object

Convert an object to be a smart (recurring mapping dictionaries to smart objects).

#### Create object schema

Create an object representation based on it annotation or default value.

## Logging

## SmartObject

* cls – registered class
* name – provided or determined name for class
* path – absolute dotted path to class


* class_schema – convert from type to primitive representation based on annotation
* instance_schema – convert from type instance to primitive representation based on annotation
* simplifier – convert object to primitive type
* smartifier – convert object to be smart (recurring mapping dictionaries to smart objects)
* mapper – add special converter for some keywords in class
* converter – add type mapping from some type to another

# Contributing

Contributions are very welcome. Tests can be run with [tox](https://tox.readthedocs.io/en/latest/),
please ensure the coverage at least stays the same before you submit a merge request.

# License

Distributed under the terms of the [MIT](http://opensource.org/licenses/MIT) license,
"SmartParams" is free and open source software.

# Issues

If you encounter any problems, please email us at <mateusz.baran.sanok@gmail.com>, along with a
detailed description.
