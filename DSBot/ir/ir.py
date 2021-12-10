import importlib
import inspect
import logging
import pkgutil

import ir.impl
from ir.ir_operations import IROpOptions


def run(ir, dataset, session_id, **kwargs):
    if len(ir) == 1:
        return ir[0].run(dataset, session_id, **kwargs)
    else:
        return run(ir[1:], ir[0].run(dataset, session_id, **kwargs), session_id)


def create_IR(pipeline, message_queue):
    dict_pipeline = []
    for item in pipeline:
        try:
            print(generic_classes, item, item in generic_classes)
            if item in generic_classes:
                print(modules)
                print(modules[item])
                print(item)
            module = modules[item]()
            module.set_message_queue(message_queue)

            module.set_model(item)
            module.actual_model.set_message_queue(message_queue)
            dict_pipeline.append(module)
        except KeyError:
            logging.getLogger(__name__).error('Missing module implementation for: %s', item)
    return dict_pipeline


def is_generic(value):
    return inspect.isclass(value) and 'ir.impl.' in value.__module__ and issubclass(value, IROpOptions)


modules = []
generic_classes = []
for loader, module_name, is_pkg in pkgutil.walk_packages(ir.impl.__path__, ir.impl.__name__ + '.'):
    generic_class = inspect.getmembers(importlib.import_module(module_name), is_generic)
    generic_classes.append(generic_class[0][0])
    modules.extend(generic_class)


modules = {m: r[1] for r in modules for m in r[1]().get_models()}
