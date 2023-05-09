import itertools
from string import ascii_lowercase as abc
import os


def name_gen(lenght):
    return [w for w in (''.join(word) for word in itertools.product(abc, repeat=3))][:lenght]


def obj_at_next_index(obj, stack, steps=1):
    index = stack.index(obj) + steps
    return stack[index]


def update_file(file_path, obj, _type):
    if os.path.exists(file_path):
        with open(file_path) as f:
            data = eval(f.read())
        with open(file_path, 'w') as f:
            if _type == 'dict':
                data.update(obj)
                f.write(str(data))
            elif _type == 'list':
                data.extend(obj)
                f.write(str(data))
    else:
        with open(file_path, 'w') as f:
            f.write(str(obj))
