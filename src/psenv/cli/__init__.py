from ramjam.utils import parse_args
from . import  pull, push, config


def parse_psenv_args():
    modules = [pull, push, config]
    modules.sort(key=lambda x: x.__name__)
    return parse_args(*modules)
