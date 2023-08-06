import os
from warnings import warn

__version__ = '2.0.0'

if os.name == 'nt':
    p = os.environ['PATH'].split(';')
    lib = os.path.join(os.path.split(__file__)[0], 'lib')
    os.environ['PATH'] = ";".join([lib] + p)
