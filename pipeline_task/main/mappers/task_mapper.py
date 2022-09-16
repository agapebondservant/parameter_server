import yaml
import importlib


def from_yaml(path, params={}):
    with open(path, 'r') as stream:
        mapping = yaml.safe_load(stream)
        mapping['params'] = params
        mapping['input_args'], mapping['input_kwargs'] = process_inputs(mapping.get('inputs'), params)
        mapping['outputs'] = tuple(mapping.get('outputs'))
        mapping['method'] = process_method(mapping.get('method'))
        return mapping


def process_inputs(inputs, params):
    input_args = tuple(params.get(i) or None for i in inputs if '=' not in i)
    input_kwargs = dict(dict(i.split('=') for i in inputs if '=' in i))
    return input_args, input_kwargs


def process_method(fully_qualified_method):
    if '.' in fully_qualified_method:
        method_index = fully_qualified_method.rindex('.') + 1
        method_name = fully_qualified_method[method_index:]
        module_name = fully_qualified_method[:method_index - 1]
        module = importlib.import_module(module_name)
        method = getattr(module, method_name)
    else:
        method = globals()[fully_qualified_method]
    return method
