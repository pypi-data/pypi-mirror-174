
def filter_out_empty_result(ignore_cache: bool, raise_on_empty: bool = False):
    def filter_out_empty_result_(result: dict):
        if raise_on_empty:
            if ignore_cache and len(result.get('data')) > 0:
                raise AssertionError("Empty result arrived")
        return result

    return filter_out_empty_result_


def filter_test_by_name(test_name, raise_type: type = None):
    if raise_type:
        assert issubclass(raise_type, Exception), f"raise_type must be Exception subclass (Provided: {raise_type})"

    def filter_test_by_name_(test_data):
        for test in test_data['data']:
            if test['attributes']['name'] == test_name:
                return test
        if raise_type:
            raise raise_type(f"Test '{test_name}' no resolved")
        return None

    return filter_test_by_name_


def extract_test_id(test_info: dict):
    return test_info['data'][0]['id']


def extract_project_id(name):
    def _(project_data: dict):
        for project in project_data.get('data'):
            if project['attributes']['name'] == name:
                return project['id']
        raise AttributeError(f"Project '{name}' not resolved")

    return _


def extract_user_id(name):
    def _(user_data):
        for user_id in [pr.get('id') for pr in user_data.get('data')
                        if pr['attributes']['display-name'] == name]:
            return user_id
        raise AttributeError(f"User '{name}' not resolved")
    return _


def extract_field_id(name):
    def _(fields_data):
        for field_id in [pr.get('id') for pr in fields_data.get('data') if
                         pr['attributes']['name'].strip() == name]:
            return field_id
        raise AttributeError(f"Field '{name}' not resolved")
    return _


def extract_field_id_by_name(name, *fields_data):
    for field_id in [pr.get('id') for pr in fields_data if
                     pr['attributes']['name'].strip() == name]:
        return field_id
    raise AttributeError(f"Field '{name}' not resolved")


def practi_test_duration(duration_in_seconds: float):
    hours = int(duration_in_seconds/3600)
    minutes = int((duration_in_seconds - hours * 3600)/60)
    seconds = int(duration_in_seconds - hours * 3600 - minutes * 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
