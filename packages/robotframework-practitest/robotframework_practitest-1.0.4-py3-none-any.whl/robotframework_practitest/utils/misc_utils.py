from __future__ import annotations

import inspect
import os
import sys

from robot.libraries.BuiltIn import BuiltIn


def retrieve_name(var) -> str:
    callers_local_vars = inspect.currentframe().f_back.f_locals.items()
    return [var_name for var_name, var_val in callers_local_vars if var_val is var][0]


def get_error_info():
    exc_type, exc_obj, exc_tb = sys.exc_info()
    file_name = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    return file_name, exc_tb.tb_lineno


def read_variables(*var_names):
    return dict(_read_api_info(*var_names))


def _read_api_info(*var_names):
    robot_vars = BuiltIn().get_variables(True)
    for var_name in var_names:
        name, mandatory, default = var_name.as_tuple
        if mandatory:
            assert name in robot_vars.keys(), f"Mandatory variable '{name}' missing"
        value = robot_vars.get(name, default)
        BuiltIn().set_global_variable(f"${var_name.Name}", value)
        yield var_name.Name, value
