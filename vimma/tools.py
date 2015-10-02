import importlib
import itertools

def subclassmodels(c, exclude_modules=[], p=lambda x: not x._meta.abstract):
    return filter(lambda x: not any(map(x.__module__.startswith, exclude_modules)),
            filter(p, subclasses(c)))

def subclasses(c):
    return list(itertools.chain.from_iterable(map(subclasses, c.__subclasses__())))\
            + c.__subclasses__()

def get_import(module, thing):
    m = importlib.import_module(module)
    return getattr(m, thing)

def get_classes(module, match):
    mo = importlib.import_module(module)
    return [getattr(mo, name) for name in dir(mo) if match in name]

def get_types(module, match, p=None):
    mo = importlib.import_module(module)
    matches = [getattr(mo, name) for name in dir(mo) if type(getattr(mo, name)) == type(match)]
    return matches if not p else filter(p, matches)