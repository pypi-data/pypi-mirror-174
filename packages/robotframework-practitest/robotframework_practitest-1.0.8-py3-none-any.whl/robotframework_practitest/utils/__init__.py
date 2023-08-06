from . import data_service, singleton, session_wrapper, background_service, misc_utils, logger


class VariableItem:
    def __init__(self, name, mandatory=True, default=None):
        self.Name = name
        self.Default = default
        self.Mandatory = mandatory

    @property
    def as_tuple(self):
        return self.Name, self.Mandatory, self.Default


__all__ = [
    'VariableItem',
    'data_service',
    'singleton',
    'session_wrapper',
    'background_service',
    'misc_utils',
    'logger'
]
