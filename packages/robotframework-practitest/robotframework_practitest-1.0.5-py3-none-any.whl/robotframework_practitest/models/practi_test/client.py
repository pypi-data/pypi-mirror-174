from enum import Enum

from robotframework_practitest.models.practi_test.data_formatters import *
from robotframework_practitest.utils import *
from robotframework_practitest.utils.data_service import CacheItem, DEFAULT_ITEM_WAIT
from robotframework_practitest.utils.logger import LOGGER as logger
from robotframework_practitest.utils.misc_utils import retrieve_name, get_error_info
from robotframework_practitest.utils.session_wrapper import SessionWithCaching, SupportedMethods

BASE_URL = 'https://api.practitest.com/api/v2/'
DEFAULT_PRIORITY = '3-normal'


class TestTypes(Enum):
    ScriptedTest = 'ScriptedTest'
    ApiTest = 'ApiTest'
    FireCracker = 'FireCracker'
    xBotTest = 'xBotTest'
    EggplantTest = 'EggplantTest'


class PtClient(SessionWithCaching):
    projects_tag = "projects"
    users_tag = "users"
    fields_tag = "fields"
    custom_fields_tag = "custom_fields"
    test_tag = "tests"
    step_tag = "steps"
    test_set_tag = "sets"
    instance_tag = 'instances'
    run_tag = 'runs'

    ACCOUNT_FIELDS = ['user_email', 'user_token', 'user_email', 'project_name', 'tester_name']

    def __init__(self, base_url=None, priority=DEFAULT_PRIORITY, **account):
        self.base_url = base_url or BASE_URL
        self._priority = priority
        self.user_email = self.user_token = None
        self.project_id = self.tester_id = self.project_name = self.tester_name = None
        self.assign_parameters(**account)
        super().__init__(self.user_email, self.user_token, **account)

    def assign_parameters(self, **parameters):
        for field in self.ACCOUNT_FIELDS:
            setattr(self, field, parameters.get(field, None))

        assert all([getattr(self, f, None) is not None for f in self.ACCOUNT_FIELDS]), \
            "Verify all _get_custom_fields_list provided:\n\t{}".format('\n\t'.join(self.ACCOUNT_FIELDS))

    def initiate_session(self):
        try:
            self.project_id = self.query_project_id(self.project_name, 5)
            self.tester_id = self.query_user_id(self.tester_name, 5)
            logger.info(f"PractiTest API session started for {self}")
        except Exception as e:
            f, li = get_error_info()
            logger.error(f"Fail init PractiTest API: {e}; File: {f}:{li}")
            raise

    def terminate_session(self):
        self.project_id = None
        self.tester_id = None
        logger.info(f"PractiTest API session ended")

    def __str__(self):
        return f"URL: {self.base_url}; " \
               f"Project: {self.project_name} (ID: {self.project_id}); " \
               f"User: {self.tester_name} (ID{self.tester_id})"

    @staticmethod
    def _parse_options(*names, **arguments):
        argument = {i: arguments.get(i, None) for i in names if arguments.get(i, None)}
        assert len(argument) == 1, \
            f"Only one argument from '{names}' should be provided ({arguments})"
        for k, v in argument.items():
            return k, v

    @property
    def project_url(self):
        return f"{self.base_url}projects/{self.project_id}/"

    def query_project_id(self, name, timeout=DEFAULT_ITEM_WAIT):
        cache_item = CacheItem(self.base_url, self.projects_tag, extract_project_id(name))
        url = self.base_url + self.projects_tag + '.json'
        return self.run(SupportedMethods.GET, cache_item, url, enforce_result=True, ignore_cache=True, timeout=timeout)

    def query_user_id(self, name, timeout=DEFAULT_ITEM_WAIT):
        cache_item = CacheItem(self.base_url, self.users_tag, extract_user_id(name))
        url = self.base_url + self.users_tag + '.json'
        return self.run(SupportedMethods.GET, cache_item, url, enforce_result=True, ignore_cache=True, timeout=timeout)

    def query_test(self, **kwargs):
        query_by, query_value = self._parse_options('display-ids', 'name_exact', 'name_like', **kwargs)
        hash_tag = kwargs.get('hash_tag', query_value)
        formatter = kwargs.get('formatter', None)
        ignore_cache = kwargs.get('ignore_cache', False)
        enforce_result = kwargs.get('enforce_result', False)
        timeout = kwargs.get('timeout', DEFAULT_ITEM_WAIT)

        cache_item = CacheItem(self.test_tag, hash_tag, formatter)

        url = "{}{}.json?{}={}".format(self.project_url, self.test_tag, query_by, query_value)
        return self.run(SupportedMethods.GET, cache_item, url, ignore_cache=ignore_cache,
                        enforce_result=enforce_result, timeout=timeout)

    def get_test_set_id(self, **kwargs):
        query_by, query_value = self._parse_options('display_ids', 'name_exact', 'name_like', **kwargs)
        ignore_cache = kwargs.get('ignore_cache', False)
        formatter = kwargs.get('formatter', None)
        timeout = kwargs.get('timeout', DEFAULT_ITEM_WAIT)
        cache_item = CacheItem(self.test_set_tag, kwargs.get('hash_tag', query_value), formatter)
        url = "{}{}.json?{}={}".format(self.project_url, self.test_set_tag, query_by, query_value)
        return self.run(SupportedMethods.GET, cache_item, url, ignore_cache, enforce_result=True, timeout=timeout)

    def query_field_id(self, name):
        cache_item = CacheItem(self.fields_tag, name, extract_field_id(name))
        url = self.project_url + self.fields_tag + '.json'
        return self.run(SupportedMethods.GET, cache_item, url, enforce_result=True)

    def query_custom_field_id(self, name, timeout=DEFAULT_ITEM_WAIT):
        cache_item = CacheItem(self.custom_fields_tag, 'custom_fields', extract_field_id(name))
        url = self.project_url + self.custom_fields_tag + '.json'
        return self.run(SupportedMethods.GET, cache_item, url, enforce_result=True, timeout=timeout)

    def convert_fields_name_to_id(self, **fields):
        cache_item = CacheItem(self.custom_fields_tag, 'custom_fields')
        url = self.project_url + self.custom_fields_tag + '.json'
        field_values = self.run(SupportedMethods.GET, cache_item, url, enforce_result=True)
        result = {}
        for name, value in fields.items():
            try:
                result.update(**{f"---f-{extract_field_id_by_name(name, *field_values.get('data'))}": value})
            except Exception as e:
                logger.error(f"Cannot extract field '{name}': {e}")
        return result

    def create_test_set(self, name, *instances, version, priority=DEFAULT_PRIORITY,
                        assigned_to_id=None, author_id=None, assigned_to_type=None,
                        planned_execution=None, status=None, tags: list = None,
                        hash_tag=None, formatter=None, ignore_cache=False, enforce_result=False, **custom_fields):
        """
        Creating TestSet in PractiTest
        :param enforce_result:
        :param ignore_cache:
        :param hash_tag:
        :param formatter: 
        :param name:
        :param instances: tests system-id list
        :param version:
        :param priority:
        :param assigned_to_id:
        :param author_id:
        :param assigned_to_type:
        :param planned_execution:
        :param status:
        :param tags:
        :param custom_fields:
        :return:
        """
        cache_item = CacheItem(self.test_set_tag, hash_tag or name, formatter)

        def pay_load_create():
            data = {
                "data": {
                    "type": "sets",
                    "attributes": {
                        "name": name,
                        "version": version,
                        "priority": priority
                    },
                    "instances_type": {
                        "test-ids": []
                    }
                }
            }

            for field in (assigned_to_id, author_id, assigned_to_type, planned_execution, status, tags):
                if field:
                    data['data']['attributes'].update(**{retrieve_name(field).replace('_', '-'): assigned_to_id})

            if len(custom_fields) > 0:
                data['data']['attributes'].update(**{
                    'custom-fields': self.convert_fields_name_to_id(**custom_fields)
                })

            if len(instances) > 0:
                data['data']['instances_type']['test-ids'].extend(instances)
            return data

        return self.run(SupportedMethods.POST, cache_item, self.project_url + self.test_set_tag + '.json',
                        pay_load_create, ignore_cache=ignore_cache, enforce_result=enforce_result)

    def update_test_set(self, test_set_id, **custom_fields):
        # TODO: TBD in future
        pass

    def create_test_case(self, name, version, user_name=None, description='', test_type=TestTypes.ScriptedTest,
                         assign_to_id=None, assign_to_type=None, tags=None, hash_tag=None, formatter=None,
                         ignore_cache=False, timeout=DEFAULT_ITEM_WAIT, steps=None, **custom_fields):
        if steps is None:
            steps = []
        if tags is None:
            tags = []
        cache_item = CacheItem(self.test_tag, hash_tag or name, formatter)

        def pay_load_create(s, **f):
            def _():
                user_id = self.query_user_id(user_name or self.tester_name, 5) or self.tester_id
                data = {
                    "data": {
                        "type": "tests",
                        "attributes": {
                            "name": name,
                            "Version": version,
                            "status": "Ready",
                            "tags": tags,
                            "author-id": user_id,
                            "description": description,
                            "test-type": test_type.name,
                            "assign-to-id": assign_to_id,
                            "assign-to-type": assign_to_type,
                        }
                    }
                }

                if len(custom_fields) > 0:
                    data['data']['attributes'].update(**{
                        'custom-fields': dict(self.convert_fields_name_to_id(**f))
                    })

                if len(steps) > 0:
                    if test_type != TestTypes.ScriptedTest:
                        logger.warn("Steps relevant for type ScriptedTest only; No step will be added")
                    else:
                        data['data'].update(**{'steps': {"data": s}})
                return data
            return _
        return self.run(SupportedMethods.POST, cache_item, self.project_url + self.test_tag + '.json',
                        pay_load_create(steps, **custom_fields), ignore_cache=ignore_cache, timeout=timeout)

    def get_run_tests_instances(self, test_set_id, test_id):
        cache_item = CacheItem(self.instance_tag, test_id)
        url = f"{self.project_url}/{self.instance_tag}.json?set-ids={test_set_id}&test-ids={test_id}"
        res = self.run(SupportedMethods.GET, cache_item, url)
        return res

    def create_run(self, instance_id, status, duration, automated_execution_output='',
                   steps=None, files=None):
        if len(automated_execution_output) > 255:
            logger.warn(f"Output too long; Will cut for 255 chars\n{automated_execution_output}")

        cache_item = CacheItem(self.run_tag, instance_id)
        url = f"{self.project_url}{self.run_tag}.json"
        data = {
            "data": {
                "type": "instances",
                "attributes": {
                    "instance-id": instance_id,
                    "exit-code": status,
                    "run-duration": duration,
                    "automated-execution-output": automated_execution_output[0:255]
                }
            }
        }

        if steps:
            data['data'].setdefault('steps', {})
            data['data']['steps'].setdefault('data', steps)

        if files:
            data['data'].setdefault('files', {})
            data['data']['files'].setdefault('data', [])
            for file in files:
                data['data']['files']['data'].append({
                    'filename': file,
                    'content_encoded': f"$(base64 {file})"
                })
        return self.run(SupportedMethods.POST, cache_item, url, data)

    def create_test_instance(self, test_set_id, test_id, version, hash_tag=None,
                             formatter=None, enforce_result=False, ignore_cache=False,
                             timeout=DEFAULT_ITEM_WAIT, **custom_fields):

        cache_item = CacheItem(self.instance_tag, hash_tag or f"{test_set_id}_{test_id}", formatter)
        url = f"{self.project_url}{self.instance_tag}.json"

        def pay_load_create():
            data = {
                "data": [
                    {
                        "type": "instances",
                        "attributes": {
                            "test-id": test_id,
                            "set-id": test_set_id,
                            "version": version
                        }
                    }
                ]
            }
            if len(custom_fields) > 0:
                data['data'][0]['attributes'].update(**{
                    'custom-fields': dict(self.convert_fields_name_to_id(**custom_fields))
                })
            return data

        return self.run(SupportedMethods.POST, cache_item, url, pay_load_create,
                        ignore_cache=ignore_cache, enforce_result=enforce_result, timeout=timeout)


__all__ = [
    'PtClient',
    'TestTypes',
    'BASE_URL'
]
