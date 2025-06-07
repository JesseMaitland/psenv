from ramjam.utils import parse_args
from . import  pull, push, config, kms


def parse_psenv_args():
    modules = [pull, push, config, kms]
    modules.sort(key=lambda x: x.__name__)
    return parse_args(*modules)
