from __future__ import absolute_import



# start delvewheel patch
def _delvewheel_init_patch_1_1_0():
    import os
    import sys
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, '.'))
    if sys.version_info[:2] >= (3, 8) and not os.path.exists(os.path.join(sys.base_prefix, 'conda-meta')) or sys.version_info[:2] >= (3, 10):
        os.add_dll_directory(libs_dir)
    else:
        from ctypes import WinDLL
        with open(os.path.join(libs_dir, '.load-order-pyqubo-1.3.1')) as file:
            load_order = file.read().split()
        for lib in load_order:
            WinDLL(os.path.join(libs_dir, lib))


_delvewheel_init_patch_1_1_0()
del _delvewheel_init_patch_1_1_0
# end delvewheel patch


import cpp_pyqubo
from cpp_pyqubo import *
from pyqubo.utils.asserts import *
from pyqubo.utils.solver import *
from .array import *
from .logical_constraint import *
from .logic import *
from pyqubo.integer.integer import *
from pyqubo.integer.log_encoded_integer import *
from pyqubo.integer.one_hot_enc_integer import *
from pyqubo.integer.order_enc_integer import *
from pyqubo.integer.unary_encoded_integer import *
