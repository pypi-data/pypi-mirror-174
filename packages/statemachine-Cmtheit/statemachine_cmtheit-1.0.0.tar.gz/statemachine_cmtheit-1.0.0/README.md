This is python package that offer state machine solution by class decorator.

# install

```shell
pip install state_machine
```

# example

```python
from statemachine_Cmtheit import statemachine


@statemachine.stateDefine({
    "solid": {"gas", "fuild"},
    "fuild": {'solid', "gas"},
    "gas": {"solid", "fuild", "ionization"},
    "ionization": {"gas"}
})
class matter:
    def __init__(self):
        self.switch("solid")


mat = matter()
print(mat.state)
```

more document see:<a href="./src/statemachine/__init__.py">__ init__.py</a>