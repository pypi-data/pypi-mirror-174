
from .client import PtClient, TestTypes, BASE_URL
from . import data_formatters as formatters
from ...utils import VariableItem

PRACTI_TEST_VARIABLES = [
    VariableItem('PT_PROJECT_NAME'),
    VariableItem('PT_USER_NAME'),
    VariableItem('PT_USER_NAME_EMAIL'),
    VariableItem('PT_USER_TOKEN'),
    VariableItem('PT_ENDPOINT', False),
    VariableItem('PT_VERSION'),
    VariableItem('PT_TEST_SET_LEVEL', False, 1),
    VariableItem('PT_TEST_TAG', False, {'prefix': 'Test-'}),
    VariableItem('PT_FIELD_PREFIX', False, {'refix': 'Field-', 'delimiter': '-'}),
    VariableItem('PT_FIELDS_MAP'),
    VariableItem('TEST_FIELDS'),
    VariableItem('INSTANCE_FIELDS'),
    VariableItem('TEST_SET_FIELDS'),
    VariableItem('PT_FOREGROUND', False, True),
    VariableItem('PT_EXTERNAL_RUN_ID', False),
    VariableItem('TAG_MAPPING'),
    VariableItem('LOG_LEVEL', False, 'INFO')
]


__all__ = [
    'PtClient',
    'TestTypes',
    'BASE_URL',
    'formatters',
    'PRACTI_TEST_VARIABLES'
]
