from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Mapping, AnyStr, Callable


class PT_MANAGED_ITEMS(Enum):
    Test = 'TEST_FIELDS'
    TestSet = 'TEST_SET_FIELDS'
    Instance = 'INSTANCE_FIELDS'


TAG_MAPPING = {}
# TAG_MAPPING = dict(
#     TEST={'prefix': 'Test-'},
#     FIELD={'prefix': 'Custom-', 'delimiter': '-'}
# )

PT_DATE_TIME_FORMAT = "%d-%m-%Y %H:%M:%S"


def set_tag_mapping(tag_mapping):
    global TAG_MAPPING
    TAG_MAPPING = tag_mapping


def get_test_steps_info(*keywords):
    return [{'name': k.name, 'description': k.doc} for k in keywords]


def get_related_test_display_ids(*tag_list):
    test_map = TAG_MAPPING.get('TEST')
    return [t.replace(test_map.get('prefix'), '') for t in tag_list if t.startswith(test_map.get('prefix'))]


def get_related_fields(*tag_list) -> Mapping[AnyStr, AnyStr]:
    test_map = TAG_MAPPING.get('FIELD')
    field_data = [t.replace(test_map.get('prefix'), '').split('-', 1)
                  for t in tag_list if t.startswith(test_map.get('prefix'))]
    return {t[0]: t[1] for t in field_data}


def get_common_robot_tags(*tag_list, **kwargs):
    return [t for t in tag_list if all([not t.startswith(p) for p in [f.get('prefix') for f in TAG_MAPPING.values()]])]


def get_field_by_tag(name, *tags):
    return get_related_fields(*tags).get(name, None)


def update_variable_scope_from_tags(*tags, **variables):
    for var, value in variables.items():
        if isinstance(value, tuple) and isinstance(value[0], Callable):
            yield var, get_related_fields(*tags).get(var, None) or value[1]
        else:
            yield var, value


FIELD_UPDATE = {
    'TAGS': update_variable_scope_from_tags,
    'ROBOT_TAGS': get_common_robot_tags
}


def formate_test_tags(*tag_list):
    def _except_fields(item):
        return any((item.startswith(f.get('prefix')) for f in TAG_MAPPING.values()))

    field_map = TAG_MAPPING.get('FIELD')
    tags = sorted([t for t in tag_list if not _except_fields(t)])
    custom_fields = {i[0]: i[1] for i in
                     [t.replace(field_map.get('prefix'), '').split(field_map.get('delimiter'))
                      for t in tag_list if t.startswith(field_map.get('prefix'))]}
    return tags, custom_fields


def format_kw_list(kws: list):
    result = ''
    for index, item in enumerate(kws):
        if index == 0:
            result += item
        elif item == 'AND':
            result += '\n\t' + item
        else:
            result += '\n\t\t' + item
    return result


def get_robot_variables_map(fields: list, *fields_map, **variables):
    for field in [f for f in fields_map if f.get('name') in fields]:
        robot_variable = field.get('variable', None)
        if robot_variable:
            value = variables.get(robot_variable, field.get('default', None))
            yield field.get('name'), value


def get_name(name, *path, **kwargs):
    delimiter = kwargs.get('delimiter', '/')
    path = list(path)
    run_id = kwargs.get('run_id', None)
    result = []
    if path:
        result.append("{}".format(f"Path: {delimiter.join(path)}"))
    if run_id:
        if run_id == 'datetime':
            result.append(f"TS: {datetime.now().strftime(PT_DATE_TIME_FORMAT)}")
        else:
            result.append(f"ExternalID: {run_id}")
    return f"{name} ({', '.join(result)})" if result else name


